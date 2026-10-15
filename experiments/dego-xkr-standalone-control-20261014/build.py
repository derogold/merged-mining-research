from pathlib import Path
import subprocess
p=Path(__file__).resolve().parent;r=Path('/tmp/dego-aux-testnet-20261014/source');c=r/'src/crypto'
files=['hash.c','keccak.c','aesb.c','oaes_lib.c','blake256.c','groestl.c','jh.c','skein.c','hash-extra-blake.c','hash-extra-groestl.c','hash-extra-jh.c','hash-extra-skein.c','tree-hash.c']
cmd=['gcc','-shared','-fPIC','-Wl,-Bsymbolic','-O2','-g','-maes','-msse2','-DFORCE_USE_HEAP','-Wno-deprecated-declarations','-I'+str(r/'src'),'-I'+str(c),'-I'+str(r/'include'),'-I'+str(r/'external'),str(p/'pair.c')]+[str(c/f) for f in files]+['-o',str(p/'pair.so')]
subprocess.run(cmd,check=True)
