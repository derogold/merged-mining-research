import sys,json,os
sys.path.insert(0,'/tmp/dego-xkr-shared-init-20261014')
from direct_harness import Harness,offset,p
os.sched_setaffinity(0,{2})
h=Harness();j=json.loads((p.parent/'dego-xkr-dual-testnet-20261014/dual-results.json').read_text())[0];w=bytes.fromhex(j['worker']['work']);t,out=h.run(sys.argv[1],w,offset(w),700000,2048,1);print(json.dumps(t))
