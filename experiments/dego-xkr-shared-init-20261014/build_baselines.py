import subprocess
from pathlib import Path
p=Path(__file__).resolve().parent
roots={'dego':p.parent/'dego-aux-testnet-20261014/source','xkr':p.parent/'dego-xkr-dual-testnet-20261014/source'}
files=['hash.c','keccak.c','aesb.c','oaes_lib.c','blake256.c','groestl.c','jh.c','skein.c','hash-extra-blake.c','hash-extra-groestl.c','hash-extra-jh.c','hash-extra-skein.c','tree-hash.c']
for coin,root in roots.items():
 c=root/'src/crypto';slow=c/('slow-hash-x86.c' if coin=='dego' else 'slow-hash.c')
 cmd=['gcc','-shared','-fPIC','-Wl,-Bsymbolic','-O2','-maes','-msse2','-DFORCE_USE_HEAP','-Wno-deprecated-declarations','-I'+str(root/'src'),'-I'+str(c),'-I'+str(root/'include'),'-I'+str(root/'external'),str(slow)]+[str(c/f) for f in files]+['-o',str(p/(coin+'-full.so'))]
 subprocess.run(cmd,check=True)
