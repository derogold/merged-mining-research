# Miner process only: controller supplies work, algorithm parameters and limits.
# Reference correctness worker: no shared-init optimization or energy claim.
import ctypes as C,json,sys,time
from pathlib import Path
p=Path(__file__).resolve().parent;j=json.load(sys.stdin);work=bytearray.fromhex(j['work']);offset=0
for _ in range(3):
 while work[offset]&128:offset+=1
 offset+=1
offset+=32
libs={}
for coin in ['dego','xkr']:
 fn=C.CDLL(str(p/(coin+'-full.so'))).cn_slow_hash
 fn.argtypes=[C.c_void_p,C.c_size_t,C.c_void_p]+[C.c_int]*3+[C.c_uint32]*3+([C.c_uint64] if coin=='dego' else [])
 libs[coin]=fn
buf=C.create_string_buffer(32);target=(2**256-1)//100;counts={'dego':0,'xkr':0};start=time.monotonic()
def hashit(coin):
 raw=bytes(work);args=[2,2,0,131072,131072,32768,0x1fff0] if coin=='dego' else [1,2,0,262144,262144,131072]
 libs[coin](raw,len(raw),buf,*args);counts[coin]+=1;return buf.raw
for nonce in range(j.get('max_nonces',1000000)):
 work[offset:offset+4]=nonce.to_bytes(4,'little');d=hashit('dego')
 if int.from_bytes(d,'little')>target:continue
 x=hashit('xkr')
 if int.from_bytes(x,'little')<=target:
  print(json.dumps({'nonce':nonce,'nonce_offset':offset,'work':work.hex(),'dego_pow':d.hex(),'xkr_pow':x.hex(),'hash_calls':counts,'elapsed_seconds':time.monotonic()-start}));break
else:raise RuntimeError('Bounded search exhausted')
