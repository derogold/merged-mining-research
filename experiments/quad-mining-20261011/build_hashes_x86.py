import subprocess,pathlib,json
out=pathlib.Path(__file__).resolve().parent
repos={'dego':'dego-core','wrkz':'wrkz','upx':'uplexa','xfg':'fuego'}
results={}
for coin,repo in repos.items():
 root=out/repo; c=root/'src/crypto'
 files=['hash.c','keccak.c','aesb.c','oaes_lib.c','blake256.c','groestl.c','jh.c','skein.c','hash-extra-blake.c','hash-extra-groestl.c','hash-extra-jh.c','hash-extra-skein.c','tree-hash.c']
 files+=['slow-hash-x86.c'] if coin in ('dego','wrkz') else ['slow-hash.c']
 cmd=['cc','-shared','-fPIC','-O2','-maes','-msse2','-DFORCE_USE_HEAP','-Wno-deprecated-declarations','-Wno-incompatible-pointer-types','-I'+str(root/'src'),'-I'+str(c),'-I'+str(root/'include'),'-I'+str(root/'contrib/epee/include'),'-I'+str(root/'external')]+[str(c/f) for f in files]+['-o',str(out/(coin+'.dylib'))]
 
 if coin=='wrkz':
  subprocess.run(['c++','-std=c++17','-fPIC','-O2','-c',str(c/'slow-hash-state.cpp'),'-o',str(out/'wrkz-state.o')],check=True)
  cmd += [str(out/'wrkz-state.o'),'-lstdc++']
 p=subprocess.run(cmd,text=True,capture_output=True);(out/(coin+'-build.log')).write_text(p.stdout+p.stderr)
 results[coin]=p.returncode
 print(coin,p.returncode,(p.stderr[-1800:] if p.returncode else ''),flush=True)
(out/'build-results.json').write_text(json.dumps(results,indent=2))
