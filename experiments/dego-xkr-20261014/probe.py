import pathlib,subprocess,ctypes,json,hashlib
base=pathlib.Path('/tmp');out=pathlib.Path(__file__).resolve().parent
results={};libs={}
files=['hash.c','keccak.c','aesb.c','oaes_lib.c','blake256.c','groestl.c','jh.c','skein.c','hash-extra-blake.c','hash-extra-groestl.c','hash-extra-jh.c','hash-extra-skein.c','tree-hash.c']
for coin in ['dego','xkr']:
 root=base/('dego-xkr-research-'+coin);c=root/'src/crypto';slow=c/('slow-hash-x86.c' if coin=='dego' else 'slow-hash.c');s=slow.read_text()
 for stage in (['full','init','round1'] + (['reuse'] if coin=='xkr' else [])):
  code=s
  if stage in ['init','reuse']: code='unsigned char shared_init[131072];\n'+code
  if stage=='init':
   marker='    U64(a)'
   pos=code.index(marker,code.index('void cn_slow_hash('))
   code=code[:pos]+'    memcpy(shared_init, hp_state, 131072); cn_fast_hash(hp_state, 131072, hash); return;\n'+code[pos:]
  elif stage=='round1':
   pos=code.index('            post_aes();',code.index('void cn_slow_hash('))+len('            post_aes();')
   code=code[:pos]+'\n            cn_fast_hash(hp_state, 131072, hash); return;'+code[pos:]
  if stage=='reuse':
   start=code.index('void cn_slow_hash(');pos=code.index('for (i = 0; i < init_rounds; i++)',start)
   code=code[:pos]+code[pos:].replace('for (i = 0; i < init_rounds; i++)','memcpy(hp_state, shared_init, 131072); memcpy(text, shared_init + 131072 - 128, 128); for (i = 1024; i < init_rounds; i++)',1)
  p=out/(coin+'-'+stage+'.c');p.write_text(code);lib=out/(coin+'-'+stage+'.so')
  cmd=['gcc','-shared','-fPIC','-O2','-maes','-msse2','-DFORCE_USE_HEAP','-Wno-deprecated-declarations','-I'+str(root/'src'),'-I'+str(c),'-I'+str(root/'include'),'-I'+str(root/'external'),str(p)]+[str(c/f) for f in files]+['-o',str(lib)]
  r=subprocess.run(cmd,capture_output=True,text=True);(out/(coin+'-'+stage+'-build.log')).write_text(r.stdout+r.stderr)
  if r.returncode:raise RuntimeError(r.stderr[-2000:])
  libs[coin,stage]=ctypes.CDLL(str(lib)).cn_slow_hash
  libs[coin,stage].argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p]+[ctypes.c_int]*3+[ctypes.c_uint32]*3+([ctypes.c_uint64] if coin=='dego' else [])
rows=[]
for n in range(16):
 data=hashlib.shake_256(('dego-xkr-'+str(n)).encode()).digest(76+n)
 row={'input':data.hex()}
 for coin in ['dego','xkr']:
  for stage in ['full','init','round1']:
   buf=ctypes.create_string_buffer(32)
   params=[2,2,0,131072,131072,32768,0x1fff0] if coin=='dego' else [1,2,0,262144,262144,131072]
   libs[coin,stage](data,len(data),buf,*params);row[coin+'_'+stage]=buf.raw.hex()
 snapshot=(ctypes.c_ubyte*131072).in_dll(ctypes.CDLL(str(out/'dego-init.so')),'shared_init')
 target=(ctypes.c_ubyte*131072).in_dll(ctypes.CDLL(str(out/'xkr-reuse.so')),'shared_init');ctypes.memmove(target,snapshot,131072)
 buf=ctypes.create_string_buffer(32);libs['xkr','reuse'](data,len(data),buf,1,2,0,262144,262144,131072);row['xkr_reuse']=buf.raw.hex()
 rows.append(row)
summary={stage:sum(r['dego_'+stage]==r['xkr_'+stage] for r in rows) for stage in ['full','init','round1']}
summary['reuse_matches_xkr']=sum(r['xkr_reuse']==r['xkr_full'] for r in rows)
known={}
data=bytes.fromhex('0100fb8e8ac805899323371bb790db19218afd8db8e3755d8b90f39b3d5506a9abce4fa912244500000000ee8146d49fa93ee724deb57d12cbc6c6f3b924d946127c7a97418f9348828f0f02')
for coin,expected in [('dego','38591572f820d4de253cf55a2192b622b0289e2e5c3616e61e787a8fe462ec5a'),('xkr','b2172ec9466e1aee70ec8572a14c233ee354582bcb93f869d429744de5726a26')]:
 buf=ctypes.create_string_buffer(32);params=[2,2,0,131072,131072,32768,0x1fff0] if coin=='dego' else [1,2,0,262144,262144,131072];libs[coin,'full'](data,len(data),buf,*params);known[coin]={'expected':expected,'actual':buf.raw.hex(),'passed':buf.raw.hex()==expected}
assert all(v['passed'] for v in known.values())
assert summary=={'full':0,'init':16,'round1':0,'reuse_matches_xkr':16}
(out/'results.json').write_text(json.dumps({'comparisons':16,'equal':summary,'known_answers':known,'rows':rows},indent=2));print(summary)
