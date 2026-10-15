from pathlib import Path
p=Path('/tmp/dego-xkr-shared-init-20261014')
out=p/'profile';out.mkdir(exist_ok=True)
import subprocess
files=['hash.c','keccak.c','aesb.c','oaes_lib.c','blake256.c','groestl.c','jh.c','skein.c','hash-extra-blake.c','hash-extra-groestl.c','hash-extra-jh.c','hash-extra-skein.c','tree-hash.c']
header='''#include <time.h>
static __thread double phase_ns[5];
static inline double stamp(void) { struct timespec t; clock_gettime(CLOCK_THREAD_CPUTIME_ID,&t); return (double)t.tv_sec*1e9+t.tv_nsec; }
void profile_reset(void) { for(int i=0;i<5;i++) phase_ns[i]=0; }
void profile_read(double *p) { for(int i=0;i<5;i++) p[i]=phase_ns[i]; }
'''
for coin in ['xkr','dego']:
 root=p.parent/('dego-aux-testnet-20261014/source' if coin=='dego' else 'dego-xkr-dual-testnet-20261014/source');c=root/'src/crypto'
 for mode in ['full','direct','fused']:
  src=(c/('slow-hash-x86.c' if coin=='dego' else 'slow-hash.c')) if mode=='full' else p/(coin+'-'+mode+'.c')
  s=src.read_text();fn='cn_slow_hash' if mode=='full' else (coin+'_direct' if mode=='direct' else ('dego_capture' if coin=='dego' else 'xkr_reuse'))
  start=s.index('void '+fn+'(');brace=s.index('{',start);end=s.index('    slow_hash_free_state(page_size);',brace)+len('    slow_hash_free_state(page_size);')
  body=s[brace:end]
  body=body.replace('{','{ double pt=stamp(), pn;',1)
  marks=['    /* CryptoNight Step 2:', '    U64(a)', '    /* CryptoNight Step 4:', '    /* CryptoNight Step 5:']
  for i,m in enumerate(marks):
   assert m in body,(coin,mode,m)
   body=body.replace(m,'    pn=stamp(); phase_ns[%d]+=pn-pt; pt=pn;\n'%i+m,1)
  body+='\n    pn=stamp(); phase_ns[4]+=pn-pt;\n'
  s=header+s[:brace]+body+s[end:];f=out/(coin+'-'+mode+'.c');f.write_text(s)
  cmd=['gcc','-shared','-fPIC','-Wl,-Bsymbolic','-O2','-maes','-msse2','-DFORCE_USE_HEAP','-Wno-deprecated-declarations','-I'+str(root/'src'),'-I'+str(c),'-I'+str(root/'include'),'-I'+str(root/'external'),str(f)]+[str(c/x) for x in files]+['-o',str(out/(coin+'-'+mode+'.so'))]
  if mode=='direct' and coin=='dego':cmd +=[str(out/'xkr-direct.so'),'-Wl,-rpath,'+str(out)]
  if mode=='fused' and coin=='xkr':continue
  r=subprocess.run(cmd,capture_output=True,text=True);assert r.returncode==0,r.stderr
print('BUILD_OK')
