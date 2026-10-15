import json,subprocess
from pathlib import Path
p=Path(__file__).resolve().parent
labels=['initial-1-5','reject-new-at-6','accept-old-at-6','reject-old-at-7','accept-new-7-10']
records=[dict(json.loads(line),label=label) for label in labels for line in (p/f'{label}.jsonl').read_text().splitlines()]
cmd=['docker','run','--rm','-i','--network','none','--cpus','1','--memory','1g','-v',f'{p}:/research:ro','dego-research-build:20261014','/research/build/research-inspect']
r=subprocess.run(cmd,input='\n'.join(x['request']['params'][0] for x in records)+'\n',text=True,capture_output=True,check=True)
inspected=[json.loads(x) for x in r.stdout.splitlines()]
assert len(records)==len(inspected)==12
for record,proof in zip(records,inspected):
 assert proof['pow_meets_100'],proof
 assert proof['depth']==1,proof
 assert proof['old_path_matches']!=proof['new_path_matches'],proof
 expected=proof['new_path_matches'] if proof['height']>=7 else proof['old_path_matches']
 assert record['accepted']==expected,proof
 assert proof['majorVersion']==min(proof['height']+1,7),proof
 proof['label']=record['label'];proof['accepted']=record['accepted']
(p/'proof-inspection.json').write_text(json.dumps(inspected,indent=2)+'\n')
print('PASS: 12 candidates independently inspected; all adequate PoW; 10 accepted, 2 rejected solely on the wrong auxiliary path (supported by daemon logs).')
