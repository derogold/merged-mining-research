import ctypes as C,sys,json,hashlib,os
from pathlib import Path
p=Path(__file__).resolve().parent;sys.path.insert(0,'/tmp/dego-xkr-shared-init-20261014')
from harness import Harness,offset
h=Harness();lib=C.CDLL(str(p/'pair.so'));fn=lib.pair_hash;fn.argtypes=[C.c_void_p,C.c_size_t,C.c_void_p,C.c_uint];fn.restype=None
batch=lib.pair_batch;batch.argtypes=[C.c_void_p,C.c_size_t]+[C.c_uint]*4+[C.c_void_p];batch.restype=C.c_int
chunks=[0,1,4,16,64,256,1024]
def calc(data,chunk):
 out=C.create_string_buffer(64);fn(data,len(data),out,chunk);return out.raw
if __name__=='__main__':
 os.sched_setaffinity(0,{2});n=0
 for i in range(64):
  data=hashlib.shake_256(str(i).encode()).digest(43+i%90);ref=h.calc('d',data)+h.calc('x',data)
  for chunk in chunks:assert calc(data,chunk)==ref,(i,chunk);n+=1
 jobs=json.loads(Path('/tmp/dego-xkr-dual-testnet-20261014/dual-results.json').read_text())
 for job in jobs:
  work=bytes.fromhex(job['worker']['work']);off=offset(work);_,ref=h.run('baseline',work,off,500000,64,1)
  for chunk in chunks:
   out=C.create_string_buffer(64*64);assert batch(work,len(work),off,500000,64,chunk,out)==0;assert out.raw==ref; n+=64
 (p/'correctness.json').write_text(json.dumps({'status':'passed','paired_hashes':n,'chunks':chunks}));print('PASS',n,flush=True)
