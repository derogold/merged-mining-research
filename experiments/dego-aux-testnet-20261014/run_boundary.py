import json,subprocess,time,urllib.request
from pathlib import Path
p=Path(__file__).resolve().parent
address=(p/'test-address.txt').read_text().strip()
def rpc(n,method,params=None):
 data=json.dumps({'jsonrpc':'2.0','id':'test','method':method,'params':params or {}}).encode()
 return json.load(urllib.request.urlopen(urllib.request.Request(f'http://172.30.247.{10+n}:{43170+n}/json_rpc',data,{'Content-Type':'application/json'}),timeout=5))
def tips():return [rpc(n,'getlastblockheader')['result']['block_header'] for n in range(1,4)]
def sync(height):
 for i in range(60):
  try:
   h=tips()
   if all(x['height']==height for x in h) and len({x['hash'] for x in h})==1:
    (p/f'tips-{height}.json').write_text(json.dumps(h,indent=2));return h
  except Exception:pass
  time.sleep(1)
 raise RuntimeError(f'Nodes did not converge at {height}')
def mine(label,count,mode='auto',expected=True):
 print('START',label,flush=True)
 cmd=['docker','run','--rm','--name','dego-aux-testnet-miner','--network','dego-aux-testnet-lab','--cpus','2','--memory','1g','-v',f'{p}:/research','-e',f'DEGO_TEST_AUX_MODE={mode}','-e',f'DEGO_TEST_RECEIPTS=/research/{label}.jsonl','dego-research-build:20261014','/research/build/src/miner','--address',address,'--daemon-address','172.30.247.11:43171','--threads','1','--limit',str(count)]
 with (p/f'{label}.log').open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=90)
 records=[json.loads(x) for x in (p/f'{label}.jsonl').read_text().splitlines()]
 assert len(records)==count,(label,len(records))
 assert all(x['accepted']==expected for x in records),label
 assert (r.returncode==0)==expected,(label,r.returncode)
 print('PASS',label,[(x['height'],x['version'],x['accepted']) for x in records],flush=True)
 return records
sync(0)
mine('initial-1-5',5);sync(5)
mine('reject-new-at-6',1,'new',False);sync(5)
mine('accept-old-at-6',1,'legacy');sync(6)
mine('reject-old-at-7',1,'legacy',False);sync(6)
mine('accept-new-7-10',4);sync(10)
print('BOUNDARY_PASS',flush=True)
