import ctypes as C,hashlib,json,time,os
from pathlib import Path
p=Path(__file__).resolve().parent
class Harness:
 def __init__(self):
  self.libs={k:C.CDLL(str(p/f)) for k,f in {'d':'dego-full.so','x':'xkr-full.so','f':'dego-fused.so','r':'xkr-fused.so','b':'batch.so'}.items()}
  self.fn={k:getattr(self.libs[k],{'f':'dego_capture','r':'xkr_reuse'}.get(k,'cn_slow_hash')) for k in ['d','x','f','r']}
  for k,f in self.fn.items():f.restype=None;f.argtypes=[C.c_void_p,C.c_size_t,C.c_void_p]+[C.c_int]*3+[C.c_uint32]*3+([C.c_uint64] if k in 'df' else [])
  self.batch=self.libs['b'].batch;self.batch.argtypes=[C.c_void_p]*4+[C.c_size_t]+[C.c_uint32]*4+[C.c_void_p];self.batch.restype=C.c_int
 def calc(self,k,data):
  out=C.create_string_buffer(32);params=[2,2,0,131072,131072,32768,0x1fff0] if k in 'df' else [1,2,0,262144,262144,131072]
  self.fn[k](data,len(data),out,*params);return out.raw
 def run(self,mode,work,offset,start,count,ratio):
  out=C.create_string_buffer(count*64);a='f' if mode=='shared' else 'd';b='r' if mode=='shared' else 'x'
  wall=time.perf_counter();cpu=time.thread_time()
  ret=self.batch(self.fn[a],self.fn[b],self.fn['d'],work,len(work),offset,start,count,ratio,out)
  cpu=time.thread_time()-cpu;wall=time.perf_counter()-wall;assert ret==0
  return {'cpu_s':cpu,'wall_s':wall,'digest':hashlib.sha256(out.raw).hexdigest()},out.raw

def offset(work):
 n=0
 for _ in range(3):
  while work[n]&128:n+=1
  n+=1
 return n+32
