# Pool-side orchestration fixture. No nonce loops here; the separate worker mines.
import json,subprocess,time,urllib.request
from pathlib import Path
p=Path(__file__).resolve().parent;dego=p.parent/'dego-aux-testnet-20261014'
roots={'dego':dego,'xkr':p.parent/'dego-xkr-dual-testnet-20261014'};nets={'dego':247,'xkr':248};ports={'dego':43170,'xkr':43370}
def rpc(coin,method,params=None,n=1):
 data=json.dumps({'jsonrpc':'2.0','id':'research','method':method,'params':{} if params is None else params}).encode()
 return json.load(urllib.request.urlopen(urllib.request.Request(f'http://172.30.{nets[coin]}.{10+n}:{ports[coin]+n}/json_rpc',data,{'Content-Type':'application/json'}),timeout=10))
def adapter(coin,j):
 cmd=['docker','run','--rm','-i','--network','none','--cpus','1','--memory','1g','-v',f'{roots[coin]}:/research:ro',f'{coin}-research-build:20261014',f'/research/build/{coin}-template']
 r=subprocess.run(cmd,input=json.dumps(j)+'\n',text=True,capture_output=True,check=True,timeout=30);return json.loads(r.stdout)
def synced(coin,height):
 for _ in range(60):
  h=[rpc(coin,'getlastblockheader',n=n)['result']['block_header'] for n in range(1,4)]
  if all(x['height']==height for x in h) and len({x['hash'] for x in h})==1:return h
  time.sleep(1)
 raise RuntimeError('sync timeout '+coin)
report=[]
for round in range(3):
 templates={};leaves={};stamp=int(time.time())
 for coin in roots:
  address=(roots[coin]/'test-address.txt').read_text().strip()
  t=rpc(coin,'getblocktemplate',{'wallet_address':address,'reserve_size':0})['result'];assert t['difficulty']==100
  templates[coin]=t;leaves[coin]=adapter(coin,{'blob':t['blocktemplate_blob'],'timestamp':stamp})
 paths={'dego':b'DEGO-AUX-TESTNET-20261014'.ljust(32,b'\0').hex(),'xkr':'7fb97df81221dd1366051b2d0bc7f49c66c22ac4431d879c895b06d66ef66f4c'}
 jobs={c:{'blob':templates[c]['blocktemplate_blob'],'timestamp':stamp,'sibling':leaves['xkr' if c=='dego' else 'dego']['leaf'],'path':paths[c],'nonce':0} for c in roots}
 prepared={c:adapter(c,jobs[c]) for c in roots};assert prepared['dego']['work']==prepared['xkr']['work']
 worker=subprocess.run(['python3',str(p/'direct_worker.py')],input=json.dumps({'work':prepared['dego']['work'],'max_nonces':1000000}),text=True,capture_output=True,timeout=180,check=True)
 solved=json.loads(worker.stdout);candidates={};replies={};negative={}
 for coin in roots:
  job=dict(jobs[coin],nonce=solved['nonce'],verify_pow=True);cand=adapter(coin,job);candidates[coin]=cand
  assert cand['work']==solved['work'] and cand['pow']==solved[coin+'_pow']
  if round==0:
   bad=adapter(coin,dict(job,corrupt_branch=True));assert bad['work']==cand['work'] and bad['pow']==cand['pow']
   response=rpc(coin,'submitblock',[bad['blob']]);assert 'error' in response,response
   negative[coin]={'candidate':bad,'reply':response}
  response=rpc(coin,'submitblock',[cand['blob']]);assert response.get('result',{}).get('status')=='OK',response
  replies[coin]=response
 tips={c:synced(c,candidates[c]['height']) for c in roots}
 record={'round':round,'templates':templates,'leaves':leaves,'worker':solved,'candidates':candidates,'negative':negative,'replies':replies,'tips':tips};report.append(record)
 (p/'direct-live.json').write_text(json.dumps(report,indent=2)+'\n')
 print('DIRECT_LIVE_PASS',round,{c:candidates[c]['height'] for c in roots},solved['hash_calls'],flush=True)
print('ALL_THREE_SHARED_INITIALIZATION_ROUNDS_PASSED',flush=True)
