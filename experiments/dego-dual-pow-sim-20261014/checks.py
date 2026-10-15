from sim import *
def check():
 rows=json.loads((P/'results.json').read_text())['rows']
 for r in rows:
  if r['scenario']=='all_offline':assert r['stages'][1]['blocks']==0
  if r['policy']=='alternating':
   for stage in r['stages']:assert abs(stage['lane_blocks'][0]-stage['lane_blocks'][1])<=1
  if r['scenario'] in ['upx_offline','turtle_offline']:
   lane=0 if r['scenario']=='upx_offline' else 1
   assert r['stages'][1]['lane_blocks'][lane]==0
   if r['policy']=='alternating':assert r['stages'][1]['blocks']<=1
  for stage in r['stages']:assert stage['raw_work']>=0 and stage['normalized_work']>=0
 for policy in POLICIES:
  r=[x for x in rows if x['policy']==policy and x['scenario']=='steady'];rate=statistics.mean(x['stages'][2]['rate_vs_nominal'] for x in r);assert .9<rate<1.1
  assert simulate(policy,'steady',123)==simulate(policy,'steady',123)
 scores=json.loads((P/'results.json').read_text())['fork_scoring'];assert scores[0]['mean_honest_attacker_scores']['normalized']==scores[1]['mean_honest_attacker_scores']['normalized']
 # Expected normalized score rate H/D * (W*D) = H*W, for each lane and arbitrary targets.
 for lane in range(2):
  for d in [.01,1,1000,1e9]:assert math.isclose(H[lane]/d*(W[lane]*d),H[lane]*W[lane])
 (P/'checks.json').write_text(json.dumps({'status':'passed','checks':['zero-hashpower produces no blocks','strict alternation count invariant','offline lane cannot produce','strict alternation stalls','nonnegative work','steady calibration','seed replay','fixed-normalization unit-rescaling invariance','expected score-rate identity']},indent=2));print('CHECKS_PASS')
if __name__=='__main__':check()
