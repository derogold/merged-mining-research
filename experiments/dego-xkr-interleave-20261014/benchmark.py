from check import *
import time,statistics
assert json.loads((p/'correctness.json').read_text())['status']=='passed'
os.sched_setaffinity(0,{2})
jobs=json.loads(Path('/tmp/dego-xkr-dual-testnet-20261014/dual-results.json').read_text())
def run(mode,w,off,start,count):
 if mode=='original':return h.run('baseline',w,off,start,count,1)
 out=C.create_string_buffer(count*64);t=time.thread_time();wall=time.perf_counter();assert batch(w,len(w),off,start,count,int(mode),out)==0
 return {'cpu_s':time.thread_time()-t,'wall_s':time.perf_counter()-wall,'digest':hashlib.sha256(out.raw).hexdigest()},out.raw
rows=[];modes=['original']+chunks
for j,job in enumerate(jobs):
 w=bytes.fromhex(job['worker']['work']);off=offset(w)
 for m in modes:run(m,w,off,600000,32)
 for rep in range(4):
  order=modes[rep:]+modes[:rep]
  if rep%2:order=list(reversed(order))
  ref=None
  for m in order:
   timing,o=run(m,w,off,610000+rep*256,256)
   if ref is None:ref=o
   assert o==ref;rows.append(dict(job=j,rep=rep,mode=m,**timing))
  print('BLOCK',j*4+rep+1,12,flush=True)
summary={str(m):sum(r['cpu_s'] for r in rows if r['mode']==m) for m in modes}
(p/'screen.json').write_text(json.dumps({'protocol':'3 blobs,4 rotated/reversed rounds,256 pairs/run; exploratory selection only','rows':rows,'cpu_totals':summary},indent=2));print('DONE',summary,flush=True)
