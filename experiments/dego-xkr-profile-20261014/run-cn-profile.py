import sys,ctypes as C,json,os,time
from pathlib import Path
p=Path('/tmp/dego-xkr-shared-init-20261014');sys.path.insert(0,str(p))
from harness import Harness,offset
os.sched_setaffinity(0,{2});h=Harness();q=p/'profile'
libs={}
for mode in ['full','direct']:
 for coin in ['xkr','dego']:
  l=C.CDLL(str(q/(coin+'-'+mode+'.so')));f=getattr(l,'cn_slow_hash' if mode=='full' else coin+'_direct');f.argtypes=h.fn['d' if coin=='dego' else 'x'].argtypes;f.restype=None
  libs[mode,coin]=(l,f)
batch=h.batch
jobs=json.loads((p.parent/'dego-xkr-dual-testnet-20261014/dual-results.json').read_text());rows=[]
for j,job in enumerate(jobs):
 w=bytes.fromhex(job['worker']['work']);off=offset(w)
 for rep in range(4):
  ref=None
  for mode in (['full','direct','direct','full'] if rep%2==0 else ['direct','full','full','direct']):
   d=libs[mode,'dego'][1];x=libs[mode,'xkr'][1]
   out=C.create_string_buffer(256*64)
   batch(d,x,d,w,len(w),off,800000,32,1,out)
   for coin in ['dego','xkr']:libs[mode,coin][0].profile_reset()
   t=time.thread_time();batch(d,x,d,w,len(w),off,900000+rep*256,256,1,out);elapsed=time.thread_time()-t
   _,reference=h.run('baseline',w,off,900000+rep*256,256,1)
   assert out.raw==reference
   phases={}
   for coin in ['dego','xkr']:
    vals=(C.c_double*5)();libs[mode,coin][0].profile_read(vals);phases[coin]=list(vals)
   rows.append(dict(job=j,rep=rep,mode=mode,cpu_s=elapsed,phases_ns=phases))
  print('BLOCK',j*4+rep+1,12,flush=True)
(q/'results.json').write_text(json.dumps(dict(phases=['setup','initialization_including_dego_handoff','mixing','fold','finalize'],nonces_per_run=256,correctness='all outputs match uninstrumented independent baseline',rows=rows),indent=2))
for mode in ['full','direct']:
 for coin in ['dego','xkr']:
  rr=[r for r in rows if r['mode']==mode];v=[sum(r['phases_ns'][coin][i] for r in rr)/len(rr)/256/1000 for i in range(5)]
  print(mode,coin,'microseconds_per_hash',v,'percent',[100*a/sum(v) for a in v],flush=True)
print('DONE',flush=True)
