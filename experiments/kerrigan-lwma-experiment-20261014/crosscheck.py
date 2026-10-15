from lwma import *
from pathlib import Path
import random,json,subprocess
p=Path(__file__).resolve().parent;r=random.Random(20261014);inputs=[];expected=[]
for case in range(256):
 n=r.choice([1,2,61,80,250,1960,2100]);lane=r.randrange(4);limitbits=r.choice([0x1d010000,0x1f100000,0x203fffff]);floorbits=encode(decode(limitbits)//r.choice([1,16,256]));rescue=case%2;active=(case//2)%2;t=1700000000;chain=[]
 for i in range(n):
  t+=r.choice([-4000,0,120,480,2880,9999]);a=r.randrange(4) if case%4 else lane if i<n//2 else (lane+1)%4;bits=encode(decode(floorbits)//r.choice([1,2,16,256]));chain.append((t,bits,a))
 inputs.append(f'{n} {lane} {rescue} {active} {limitbits} {floorbits}\n'+''.join(f'{t} {b} {a}\n' for t,b,a in chain));expected.append(next_bits(chain,lane,decode(limitbits),decode(floorbits),rescue=rescue,floor_active=active))
z=subprocess.run([str(p/'oracle')],input=''.join(inputs),text=True,capture_output=True,check=True);got=[int(v) for v in z.stdout.split()];assert got==expected,[(i,hex(a),hex(b)) for i,(a,b) in enumerate(zip(got,expected)) if a!=b][:5]
(p/'crosscheck.json').write_text(json.dumps({'status':'passed','cases':len(got),'seed':20261014,'scope':'exact LwmaPerAlgo body with original arith_uint256; minimal chain/params shim, not full daemon','expected_nbits':[hex(v) for v in got]},indent=2));print('NATIVE_CROSSCHECK_PASS',len(got))
