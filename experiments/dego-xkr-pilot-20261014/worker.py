"""Local JSON-lines research worker. No sockets, wallets, or block submission.
One process/thread; library prefix is TLS. Cache bounded to 8 entries.
"""
import ctypes as C,json,sys,pathlib,time,hashlib,os,collections
p=pathlib.Path(__file__).resolve().parent
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
libs={name:C.CDLL(str(path)) for name,path in {'d':pathlib.Path('/tmp/dego-xkr-probe/dego-full.so'),'x':pathlib.Path('/tmp/dego-xkr-probe/xkr-full.so'),'f':p/'dego-fused.so','r':p/'xkr-fused.so','i':pathlib.Path('/tmp/dego-xkr-probe/dego-init.so')}.items()}
func={k:getattr(libs[k],{'f':'dego_capture','r':'xkr_reuse'}.get(k,'cn_slow_hash')) for k in libs}
for k,f in func.items():f.restype=None;f.argtypes=[C.c_void_p,C.c_size_t,C.c_void_p]+[C.c_int]*3+[C.c_uint32]*3+([C.c_uint64] if k in 'dfi' else [])
libs['f'].get_dego_prefix.restype=C.c_void_p
cache=collections.OrderedDict();jobs={};searches=0

def calc(k,b):
 out=C.create_string_buffer(32);a=[2,2,0,131072,131072,32768,0x1fff0] if k in 'dfi' else [1,2,0,262144,262144,131072];func[k](b,len(b),out,*a);return out.raw

def blob(job,n):
 b=bytearray.fromhex(job['blob']);i=job['nonce_offset'];b[i:i+4]=n.to_bytes(4,'little');return bytes(b)

def run(q):
 global searches
 op=q['op']
 if op=='job':
  j=q['job'];assert j['nonce_offset']>=0 and j['nonce_offset']+4<=len(bytes.fromhex(j['blob']));jobs[j['id']]=j;return {'status':'ready','job':j['id']}
 if op=='retire':
  jobs.pop(q['job'],None)
  for k in list(cache):
   if k[0]==q['job']:del cache[k]
  return {'status':'retired'}
 if q['job'] not in jobs:return {'status':'stale_job'}
 j=jobs[q['job']];n=q.get('nonce',0);b=blob(j,n);key=(j['id'],n)
 if op=='upx':
  h=calc('f',b);cache[key]=(time.monotonic(),C.string_at(libs['f'].get_dego_prefix(),131072))
  while len(cache)>8:cache.popitem(last=False)
  searches+=1;return {'status':'ok','upx':h.hex(),'cached':True}
 if op=='expire':cache.pop(key,None);return {'status':'expired'}
 if op=='turtle':
  hit=key in cache and time.monotonic()-cache[key][0]<30
  if hit:C.memmove(libs['f'].get_dego_prefix(),cache[key][1],131072)
  elif q.get('regenerate',False):
   calc('i',b);a=(C.c_ubyte*131072).in_dll(libs['i'],'shared_init');C.memmove(libs['f'].get_dego_prefix(),a,131072)
  else:return {'status':'cache_miss'}
  h=calc('r',b);searches+=1;return {'status':'ok','turtle':h.hex(),'cache_hit':hit,'regenerated':not hit}
 if op in ('batch','benchmark'):
  mode=q['mode'];count=q['count'];assert 0<count<=20000;ratio=q.get('ratio',1);assert ratio in [1,2,4,8];start=q.get('start',0);digest=hashlib.sha256();samples=[];t=time.perf_counter();cpu=time.process_time();xcount=0
  for n in range(start,start+count):
   b=blob(j,n);paired=(n-start)%ratio==0
   dh=calc('f' if mode=='fused' and paired else 'd',b);digest.update(dh)
   xh=calc('r' if mode=='fused' else 'x',b) if paired else b'';digest.update(xh);xcount+=int(paired)
   if op=='batch':samples.append({'nonce':n,'upx':dh.hex(),'turtle':xh.hex() if paired else None})
  searches+=count+xcount
  return {'status':'ok','mode':mode,'upx_count':count,'turtle_count':xcount,'wall_s':time.perf_counter()-t,'cpu_s':time.process_time()-cpu,'digest':digest.hexdigest(),'samples':samples,'cpu':list(os.sched_getaffinity(0)),'searches_total':searches}
 raise ValueError(op)
for line in sys.stdin:
 try:print(json.dumps(run(json.loads(line))),flush=True)
 except Exception as e:print(json.dumps({'status':'error','error':str(e)}),flush=True)
