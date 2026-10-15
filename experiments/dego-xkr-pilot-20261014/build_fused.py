import pathlib,subprocess
out=pathlib.Path(__file__).resolve().parent
files=['hash.c','keccak.c','aesb.c','oaes_lib.c','blake256.c','groestl.c','jh.c','skein.c','hash-extra-blake.c','hash-extra-groestl.c','hash-extra-jh.c','hash-extra-skein.c','tree-hash.c']
for coin in ['dego','xkr']:
 root=pathlib.Path('/tmp/dego-xkr-research-'+coin);c=root/'src/crypto';src=c/('slow-hash-x86.c' if coin=='dego' else 'slow-hash.c');s=src.read_text()
 if coin=='dego':
  s='static __thread unsigned char prefix[131072];\nconst unsigned char* get_dego_prefix(void){return prefix;}\n'+s.replace('void cn_slow_hash(', 'void dego_capture(')
  pos=s.index('    U64(a)',s.index('void dego_capture('));s=s[:pos]+'    memcpy(prefix, hp_state, 131072);\n'+s[pos:]
 else:
  s='extern const unsigned char* get_dego_prefix(void);\n'+s.replace('void cn_slow_hash(', 'void xkr_reuse(')
  pos=s.index('for (i = 0; i < init_rounds; i++)',s.index('void xkr_reuse('));s=s[:pos]+s[pos:].replace('for (i = 0; i < init_rounds; i++)','memcpy(hp_state, get_dego_prefix(), 131072); memcpy(text, get_dego_prefix() + 131072 - 128, 128); for (i = 1024; i < init_rounds; i++)',1)
 p=out/(coin+'-fused.c');p.write_text(s)
 cmd=['gcc','-shared','-fPIC','-O2','-maes','-msse2','-DFORCE_USE_HEAP','-Wno-deprecated-declarations','-I'+str(root/'src'),'-I'+str(c),'-I'+str(root/'include'),'-I'+str(root/'external'),str(p)]+[str(c/f) for f in files]+['-o',str(out/(coin+'-fused.so'))]
 if coin=='xkr':cmd +=[str(out/'dego-fused.so'),'-Wl,-rpath,'+str(out)]
 r=subprocess.run(cmd,capture_output=True,text=True);(out/(coin+'-fused-build.log')).write_text(r.stdout+r.stderr);assert r.returncode==0,r.stderr[-2000:]
print('fused libraries built')
