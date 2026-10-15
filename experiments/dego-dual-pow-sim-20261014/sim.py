import random,math,json,statistics
from pathlib import Path
P=Path(__file__).resolve().parent;T=300.;H=[3.,1.];W=[1/3,1.];HALF=20*T
POLICIES=['alternating','independent','parent_clock','parent_clock_capped']
SCENARIOS={'steady':([1,1],[1,1]),'upx_offline':([0,1],[1,1]),'turtle_offline':([1,0],[1,1]),'upx_100x_drop':([.01,1],[1,1]),'turtle_10x_surge':([1,10],[1,1]),'switch_capacity':([.1,1.9],[1.9,.1]),'all_offline':([0,0],[1,1])}
def simulate(policy,scenario,seed,branch_multipliers=None,branch_rng_offset=0):
 rng=random.Random(seed);initial=[h*T*(1 if policy=='alternating' else 2) for h in H];difficulty=initial[:];lastd=initial[:];last=[0.,0.];counts=[0,0];parent=0.;now=0.;events=[]
 bounds=[0,200*T,400*T,800*T];multipliers=[[1,1],*SCENARIOS[scenario]]
 if branch_multipliers is not None:multipliers=[[1,1],branch_multipliers,branch_multipliers]
 for stage in range(3):
  if stage==1 and branch_rng_offset:rng.seed(seed+branch_rng_offset)
  end=bounds[stage+1];hashes=[H[i]*multipliers[stage][i] for i in range(2)]
  while now<end:
   if policy.startswith('parent_clock'):
    for i in range(2):
     exp=max(-100.,min(100.,(counts[i]*2*T-parent)/HALF));difficulty[i]=max(initial[i]/1024,initial[i]*2**exp)
     if policy.endswith('capped'):difficulty[i]=max(difficulty[i],lastd[i]/4)
   active=[sum(counts)%2] if policy=='alternating' else [0,1]
   rates=[hashes[i]/difficulty[i] if i in active else 0 for i in range(2)];total=sum(rates)
   if total==0:now=end;break
   wait=rng.expovariate(total)
   if now+wait>=end:now=end;break
   now+=wait;lane=0 if rng.random()*total<rates[0] else 1;used=difficulty[lane];gap=now-parent
   events.append({'t':now,'stage':stage,'lane':lane,'gap':gap,'difficulty':used})
   if policy in ['alternating','independent']:
    exponent=max(-2.,min(2.,(2*T-(now-last[lane]))/HALF));difficulty[lane]=max(initial[lane]/1024,used*2**exponent)
   lastd[lane]=used;last[lane]=now;counts[lane]+=1;parent=now
   assert len(events)<100000,'runaway block production'
 stages=[]
 for stage in range(3):
  ee=[e for e in events if e['stage']==stage];duration=bounds[stage+1]-bounds[stage]
  stages.append({'lane_blocks':[sum(e['lane']==i for e in ee) for i in range(2)],'raw_work':sum(e['difficulty'] for e in ee),'normalized_work':sum(e['difficulty']*W[e['lane']] for e in ee),'blocks':len(ee),'rate_vs_nominal':len(ee)*T/duration,'upx_share':sum(e['lane']==0 for e in ee)/len(ee) if ee else None,'gaps_under_T_over_10':sum(e['gap']<T/10 for e in ee),'max_interblock_gap_T':max((e['gap']/T for e in ee),default=None),'tail_silence_T':(bounds[stage+1]-max([bounds[stage]]+[e['t'] for e in ee]))/T})
 return {'policy':policy,'scenario':scenario,'seed':seed,'stages':stages,'reentry_delay_T':{str(i):next(((e['t']-bounds[2])/T for e in events if e['stage']==2 and e['lane']==i),None) for i in range(2)},'first_20T_recovery_blocks':sum(bounds[2]<=e['t']<bounds[2]+20*T for e in events)}
def races():
 # Fixed 600T horizon. Main honest branch: baseline H=(3,1), D=(1800,600).
 # Weak attacker: only Turtle H=.2 with target D=6, modeling an already-eased private branch.
 # Reaching that target legitimately is not modeled; this is a scoring-unit test.
 out=[]
 for scale in [1,1000]:
  wins={k:0 for k in ['blocks','raw','normalized']};totals={k:[0.,0.] for k in wins}
  for seed in range(500):
   rng=random.Random(seed+90000);scores=[]
   for hs,ds in [([3*scale,1],[1800*scale,600]),([0,.2],[1800*scale,6])]:
    t=0.;v={'blocks':0.,'raw':0.,'normalized':0.};rates=[hs[i]/ds[i] for i in range(2)]
    while True:
     t+=rng.expovariate(sum(rates))
     if t>=600*T:break
     i=0 if rng.random()*sum(rates)<rates[0] else 1
     v['blocks']+=1;v['raw']+=ds[i];v['normalized']+=ds[i]*([1/(3*scale),1][i])
    scores.append(v)
   for k in wins:
    wins[k]+=scores[1][k]>scores[0][k];totals[k][0]+=scores[0][k];totals[k][1]+=scores[1][k]
  out.append({'upx_unit_scale':scale,'attacker_wins_of_500':wins,'mean_honest_attacker_scores':{k:[x/500 for x in v] for k,v in totals.items()}})
 return out
if __name__=='__main__':
 rows=[]
 for policy in POLICIES:
  for scenario in SCENARIOS:
   rows += [simulate(policy,scenario,seed) for seed in range(20)]
  print(policy,'DONE',flush=True)
 (P/'results.json').write_text(json.dumps({'target_seconds':T,'seeds':20,'rows':rows,'fork_scoring':races()},indent=2))
 print('ALL_DONE',len(rows),flush=True)
