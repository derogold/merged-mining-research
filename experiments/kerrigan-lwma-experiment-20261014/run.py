from model import *
import json
from pathlib import Path
p=Path(__file__).resolve().parent;behaviour=[];stress=[];forks=[]
for mode in MODES:
 for scenario,mult in [('steady',[1,1]),('upx_offline',[0,1]),('turtle_offline',[1,0]),('upx_100x_drop',[.01,1])]:
  for seed in range(20):
   c=warm(mode,seed);rng=random.Random(seed+1000);during=advance(c,rng,200*T,400*T,[H[i]*mult[i] for i in range(2)]);after=advance(c,rng,400*T,800*T,H)
   behaviour.append(dict(mode=mode,scenario=scenario,seed=seed,during_rate=len(during)/200,recovery_rate=len(after)/400,first20T=sum(e[0]<420*T for e in after),return_wait_T={str(i):next(((e[0]-400*T)/T for e in after if e[1]==i),None) for i in range(2)}))
 for strategy in STRATEGIES:
  for seed in range(20):
   c=warm(mode,seed);s=c.score;e=advance(c,random.Random(seed+2000),200*T,800*T,H,strategy)
   stress.append(dict(mode=mode,strategy=strategy,seed=seed,rate=len(e)/600,score_per_second=(c.score-s)/(600*T),negative_deltas=c.negative,clipped_deltas=c.clips,min_relative_difficulty=c.min_d,max_future_offset_s=c.max_skew))
  for alpha in [[.1,.1],[.4,.4],[.8,0],[0,.8]]:
   trials=[]
   for seed in range(50):
    prefix=warm(mode,seed);honest=copy.deepcopy(prefix);att=copy.deepcopy(prefix)
    he=advance(honest,random.Random(seed+3000),200*T,800*T,[H[i]*(1-alpha[i]) for i in range(2)])
    ae=advance(att,random.Random(seed+4000),200*T,800*T,[H[i]*alpha[i] for i in range(2)],strategy)
    merged=sorted([(e[0],0,e[2]) for e in he]+[(e[0],1,e[2]) for e in ae]);scores=[0.,0.];hc=0;lead=False;maxlead=0.
    for t,side,credit in merged:
     scores[side]+=credit;hc+=side==0
     if hc>=6:lead |= scores[1]>scores[0];maxlead=max(maxlead,scores[1]-scores[0])
    trials.append(dict(seed=seed,endpoint_lead=scores[1]>scores[0],lead_after_six_public_blocks=lead,max_lead_normalized_work=maxlead,honest_score=scores[0],attacker_score=scores[1],honest_blocks=len(he),attacker_blocks=len(ae)))
   forks.append(dict(mode=mode,strategy=strategy,alpha=alpha,trials=trials))
  print(mode,strategy,'DONE',flush=True)
(p/'results.json').write_text(json.dumps(dict(behaviour=behaviour,stress=stress,forks=forks),indent=2));print('ALL_DONE',flush=True)
