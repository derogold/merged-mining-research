from pathlib import Path
import subprocess
p=Path(__file__).resolve().parent
files=['hash.c','keccak.c','aesb.c','oaes_lib.c','blake256.c','groestl.c','jh.c','skein.c','hash-extra-blake.c','hash-extra-groestl.c','hash-extra-jh.c','hash-extra-skein.c','tree-hash.c']
for coin in ['xkr','dego']:
 root=p.parent/('dego-aux-testnet-20261014/source' if coin=='dego' else 'dego-xkr-dual-testnet-20261014/source');c=root/'src/crypto';s=(c/('slow-hash-x86.c' if coin=='dego' else 'slow-hash.c')).read_text()
 if coin=='xkr':
  s=s.replace('void cn_slow_hash(', 'void xkr_direct(')
  start=s.index('void xkr_direct(')
  # Allocator and TLS scratchpad exist before the x86 hash function.
  s=s[:start]+'''void xkr_accept_prefix(const unsigned char *prefix) {
    slow_hash_allocate_state(262144);
    memcpy(hp_state, prefix, 131072);
}
''' +s[start:]
  start=s.index('void xkr_direct(');pos=s.index('for (i = 0; i < init_rounds; i++)',start)
  s=s[:pos]+s[pos:].replace('for (i = 0; i < init_rounds; i++)','memcpy(text, hp_state + 131072 - 128, 128); for (i = 1024; i < init_rounds; i++)',1)
 else:
  s='extern void xkr_accept_prefix(const unsigned char*);\n'+s.replace('void cn_slow_hash(', 'void dego_direct(')
  pos=s.index('    U64(a)',s.index('void dego_direct('));s=s[:pos]+'    xkr_accept_prefix(hp_state);\n'+s[pos:]
 f=p/(coin+'-direct.c');f.write_text(s)
 cmd=['gcc','-shared','-fPIC','-Wl,-Bsymbolic','-O2','-maes','-msse2','-DFORCE_USE_HEAP','-Wno-deprecated-declarations','-I'+str(root/'src'),'-I'+str(c),'-I'+str(root/'include'),'-I'+str(root/'external'),str(f)]+[str(c/x) for x in files]+['-o',str(p/(coin+'-direct.so'))]
 if coin=='dego':cmd +=[str(p/'xkr-direct.so'),'-Wl,-rpath,'+str(p)]
 r=subprocess.run(cmd,text=True,capture_output=True);(p/(coin+'-direct-build.log')).write_text(r.stdout+r.stderr);assert r.returncode==0,r.stderr[-2000:]
print('DIRECT_BUILD_PASS')
