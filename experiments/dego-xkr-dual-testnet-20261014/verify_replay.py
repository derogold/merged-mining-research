import json,subprocess,time,urllib.request
from pathlib import Path
p=Path(__file__).resolve().parent
compose=['docker','compose','-f',str(p/'compose.json')]
def rpc(n,method,params=None):
 data=json.dumps({'jsonrpc':'2.0','id':'test','method':method,'params':params or {}}).encode()
 return json.load(urllib.request.urlopen(urllib.request.Request(f'http://172.30.248.{10+n}:{43370+n}/json_rpc',data,{'Content-Type':'application/json'}),timeout=5))['result']
def capture():
 return [[rpc(n,'getblockheaderbyheight',{'height':h})['block_header'] for h in range(10)] for n in range(1,4)]
def wait(expected):
 for _ in range(90):
  try:
   got=capture()
   if all([x['hash'] for x in chain]==expected for chain in got):return got
  except Exception:pass
  time.sleep(1)
 raise RuntimeError('Replay failed to converge')
before=capture();expected=[x['hash'] for x in before[0]]
assert all([x['hash'] for x in chain]==expected for chain in before)
subprocess.run(compose+['restart'],check=True)
restarted=wait(expected);print('PASS all three restarted with identical headers 0–9',flush=True)
subprocess.run(compose+['stop','node3'],check=True)
(p/'data/node3').rename(p/'data/node3-before-resync')
(p/'data/node3').mkdir()
subprocess.run(compose+['up','-d','--force-recreate','node3'],check=True)
resynced=wait(expected);print('PASS fresh node3 revalidated and synchronized headers 0–9',flush=True)
(p/'replay-results.json').write_text(json.dumps({'before':before,'after_restart':restarted,'after_fresh_sync':resynced},indent=2)+'\n')
