import json,statistics,random
from pathlib import Path
p=Path(__file__).resolve().parent;r=json.loads((p/'benchmark.json').read_text());out={};rng=random.Random(20261014)
for ratio in [1,2,4,8]:
 rows=[x for x in r['trials'] if x['ratio']==ratio];summary=dict(r['summary'][str(ratio)])
 b=sum(x['baseline']['wall_s'] for x in rows);s=sum(x['shared']['wall_s'] for x in rows);summary['aggregate_wall_saving_pct']=100*(1-s/b)
 # Stratified paired resampling describes run-to-run uncertainty here, not hardware generalization.
 groups=[[x for x in rows if x['job']==j] for j in range(3)];samples=[]
 for _ in range(2000):
  sample=[rng.choice(group) for group in groups for n in range(len(group))]
  b=sum(x['baseline']['cpu_s'] for x in sample);s=sum(x['shared']['cpu_s'] for x in sample);samples.append(100*(1-s/b))
 samples.sort();summary['empirical_paired_resampling_95pct']=[samples[50],samples[1949]]
 summary['per_job_cpu_saving_pct']={str(j):100*(1-sum(x['shared']['cpu_s'] for x in group)/sum(x['baseline']['cpu_s'] for x in group)) for j,group in enumerate(groups)}
 out[str(ratio)]=summary
(p/'summary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
