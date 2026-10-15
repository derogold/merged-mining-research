import ctypes as C,sys,json,os,time,hashlib
from pathlib import Path
p=Path(__file__).resolve().parent;sys.path.insert(0,'/tmp/dego-xkr-shared-init-20261014')
from harness import Harness,offset
os.sched_setaffinity(0,{2});h=Harness();lib=C.CDLL(str(p/'pair.so'))
pair=lib.pair_batch;single=lib.single_batch
for f in [pair,single]:f.argtypes=[C.c_void_p,C.c_size_t]+[C.c_uint]*4+[C.c_void_p];f.restype=C.c_int
jobs=json.loads(Path('/tmp/dego-xkr-dual-testnet-20261014/dual-results.json').read_text())
def run(mode,w,off,start,n,reverse=False):
 if mode=='original':return h.run('baseline',w,off,start,n,1)
 if mode=='paired':
  o=C.create_string_buffer(n*64);t=time.thread_time();wall=time.perf_counter();assert pair(w,len(w),off,start,n,0,o)==0
  return dict(cpu_s=time.thread_time()-t,wall_s=time.perf_counter()-wall),o.raw
 outputs={};times={};walls={}
 for coin in ([1,0] if reverse else [0,1]):
  o=C.create_string_buffer(n*32);t=time.thread_time();wall=time.perf_counter();assert single(w,len(w),off,start,n,coin,o)==0
  times[coin]=time.thread_time()-t;walls[coin]=time.perf_counter()-wall;outputs[coin]=o.raw
 # Repacking excluded from timed hash work.
 output=b''.join(outputs[0][i*32:(i+1)*32]+outputs[1][i*32:(i+1)*32] for i in range(n))
 return dict(cpu_s=sum(times.values()),wall_s=sum(walls.values()),dego_cpu_s=times[0],xkr_cpu_s=times[1]),output
# Independent correctness over three accepted work blobs,64 nonces each.
for job in jobs:
 w=bytes.fromhex(job['worker']['work']);off=offset(w);_,ref=run('original',w,off,400000,64)
 for m in ['paired','standalone']:
  for reverse in [False,True]:assert run(m,w,off,400000,64,reverse)[1]==ref
# Varied input-length standalone checks independently against original libraries.
for i in range(64):
 w=hashlib.shake_256(str(i).encode()).digest(43+i);ref=h.calc('d',w)+h.calc('x',w)
 for coin,name in [(0,'dego_single'),(1,'xkr_single')]:
  f=getattr(lib,name);f.argtypes=[C.c_void_p,C.c_size_t,C.c_void_p];f.restype=None;o=C.create_string_buffer(32);f(w,len(w),o);assert o.raw==ref[coin*32:(coin+1)*32]
(p/'correctness.json').write_text(json.dumps({'status':'passed','real_blobs':3,'nonces_per_blob':64,'varied_inputs':64,'standalone_orders':['dego-first','xkr-first']}));print('CORRECTNESS_PASS',flush=True)
rows=[];modes=['original','paired','standalone']
for j,job in enumerate(jobs):
 w=bytes.fromhex(job['worker']['work']);off=offset(w)
 for m in modes:run(m,w,off,900000,64)
 for rep in range(4):
  rot=(j+rep)%3;first=modes[rot:]+modes[:rot];order=first+list(reversed(first));times=[];ref=None;occurrence=0
  for m in order:
   reverse=(occurrence%2==1)
   if m=='standalone':occurrence+=1
   t,o=run(m,w,off,910000+rep*512,512,reverse)
   if ref is None:ref=o
   assert o==ref;t['digest']=hashlib.sha256(o).hexdigest();times.append(dict(mode=m,reverse=reverse,**t))
  totals={m:sum(t['cpu_s'] for t in times if t['mode']==m) for m in modes}
  rows.append(dict(job=j,rep=rep,runs=times,totals=totals));print('BLOCK',len(rows),12,flush=True)
summary={m:sum(r['totals'][m] for r in rows) for m in modes}
(p/'results.json').write_text(json.dumps(dict(protocol='3blobs x4 palindromic6run blocks x512pairs; same helpers/compiler; both standalone orders within each block',rows=rows,cpu_totals=summary),indent=2));print('DONE',summary,flush=True)
