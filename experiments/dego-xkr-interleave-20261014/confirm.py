# Fresh confirmation; does not reuse screen timing samples.
from check import *
import time
os.sched_setaffinity(0,{2});screen=json.loads((p/'screen.json').read_text());best=min([1,4,16,64,256,1024],key=lambda k:screen['cpu_totals'][str(k)])
modes=['original',0,best];jobs=json.loads(Path('/tmp/dego-xkr-dual-testnet-20261014/dual-results.json').read_text());rows=[]
def run(m,w,off,start,n):
 if m=='original':return h.run('baseline',w,off,start,n,1)
 o=C.create_string_buffer(n*64);t=time.thread_time();wall=time.perf_counter();assert batch(w,len(w),off,start,n,int(m),o)==0
 return dict(cpu_s=time.thread_time()-t,wall_s=time.perf_counter()-wall),o.raw
print('SELECTED',best,flush=True)
for j,job in enumerate(jobs):
 w=bytes.fromhex(job['worker']['work']);off=offset(w)
 for m in modes:run(m,w,off,800000,64)
 for rep in range(4):
  rot=(j+rep)%3;first=modes[rot:]+modes[:rot];order=first+list(reversed(first));ref=None;times=[]
  for m in order:
   t,o=run(m,w,off,810000+rep*512,512)
   if ref is None:ref=o
   assert o==ref;times.append(dict(mode=m,**t))
  totals={str(m):sum(t['cpu_s'] for t in times if t['mode']==m) for m in modes}
  rows.append(dict(job=j,rep=rep,runs=times,totals=totals));print('BLOCK',len(rows),12,flush=True)
summary={str(m):sum(r['totals'][str(m)] for r in rows) for m in modes}
(p/'confirmation.json').write_text(json.dumps(dict(selected_chunk=best,protocol='Fresh512pair runs,3blobs,4palindromic6run blocks each,rotating position; outputs exact',rows=rows,cpu_totals=summary),indent=2));print('DONE',summary,flush=True)
