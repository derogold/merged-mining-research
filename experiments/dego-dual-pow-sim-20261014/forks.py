from sim import *
# Branches share exact first200T history. At200T miner capacity splits.
# Post-split RNG independent. Honest timestamps, valid policy targets on each fork.
rows=[]
for policy in POLICIES:
 for attacker in [[.1,.1],[.4,.4],[.8,0],[0,.8]]:
  wins={k:0 for k in ['blocks','raw_work','normalized_work']};ratios=[]
  for seed in range(100):
   honest=simulate(policy,'steady',seed,[1-x for x in attacker]);private=simulate(policy,'steady',seed,attacker,100000)
   assert honest['stages'][0]==private['stages'][0]
   def score(r,k):return sum(r['stages'][i][k] for i in [1,2])
   for k in wins:wins[k]+=score(private,k)>score(honest,k)
   ratios.append(score(private,'normalized_work')/score(honest,'normalized_work'))
  rows.append({'policy':policy,'attacker_fraction_each_lane':attacker,'horizon_after_split_T':600,'trials':100,'private_strictly_ahead_at_end':wins,'mean_normalized_score_ratio':statistics.mean(ratios)})
 print(policy,'FORKS_DONE',flush=True)
(P/'forks.json').write_text(json.dumps(rows,indent=2));print('FORKS_ALL_DONE',flush=True)
