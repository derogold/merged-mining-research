import json,subprocess,time,urllib.request
from pathlib import Path
p=Path(__file__).resolve().parent
address=(p/'test-address.txt').read_text().strip()
cmd=['docker','run','--rm','--name','xkr-research-miner','--network','xkr-aux-testnet-lab','--cpus','2','--memory','1g','-v',f'{p}:/research','-e','XKR_TEST_RECEIPTS=/research/xkr-initial.jsonl','xkr-research-build:20261014','/research/build/src/miner','--address',address,'--daemon-address','172.30.248.11:43371','--threads','1','--limit','6']
with (p/'xkr-miner.log').open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=120)
assert r.returncode==0,r.returncode
records=[json.loads(s) for s in (p/'xkr-initial.jsonl').read_text().splitlines()];assert len(records)==6 and all(x['accepted'] for x in records)
print('CLI_MINER_PASS',[(x['height'],x['version']) for x in records],flush=True)
