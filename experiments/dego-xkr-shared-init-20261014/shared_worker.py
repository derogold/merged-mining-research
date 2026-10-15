# Miner-only immediate paired execution: one saved128KiB initialization prefix.
from harness import *
import sys
os.sched_setaffinity(0,{2 if 2 in os.sched_getaffinity(0) else min(os.sched_getaffinity(0))})
j=json.load(sys.stdin);work=bytes.fromhex(j['work']);off=offset(work);h=Harness();target=(2**256-1)//100;start=time.perf_counter()
limit=j.get('max_nonces',1000000)
for first in range(0,limit,512):
 count=min(512,limit-first);_,outputs=h.run('shared',work,off,first,count,1)
 for i in range(count):
  d=outputs[i*64:i*64+32];x=outputs[i*64+32:i*64+64]
  if int.from_bytes(d,'little')<=target and int.from_bytes(x,'little')<=target:
   nonce=first+i;raw=bytearray(work);raw[off:off+4]=nonce.to_bytes(4,'little')
   print(json.dumps({'implementation':'shared-initialization-128KiB-copy','nonce':nonce,'nonce_offset':off,'work':raw.hex(),'dego_pow':d.hex(),'xkr_pow':x.hex(),'hash_calls':{'dego':first+count,'xkr':first+count},'batch_size':512,'elapsed_seconds':time.perf_counter()-start}));sys.exit(0)
raise RuntimeError('Bounded search exhausted')
