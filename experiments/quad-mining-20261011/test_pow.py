import ctypes as C,json,pathlib,hashlib
p=pathlib.Path(__file__).resolve().parent
libs={n:C.CDLL(str(p/(n+'.dylib')),mode=C.RTLD_LOCAL) for n in ['dego','wrkz','upx','xfg']}
for n,l in libs.items():
 l.cn_slow_hash.restype=None
 l.cn_slow_hash.argtypes=[C.c_void_p,C.c_size_t,C.c_void_p,C.c_int,C.c_int,C.c_int]+([C.c_uint32,C.c_uint32,C.c_uint32,C.c_uint64] if n in ('dego','wrkz') else [])
def powhash(n,b):
 out=C.create_string_buffer(32)
 args=[b,len(b),out,1 if n=='xfg' else 2,2,0]
 if n in ('dego','wrkz'):args +=[131072,131072,32768,0x1fff0]
 libs[n].cn_slow_hash(*args)
 return out.raw.hex()
fixtures=[bytes(range(76)),b'\x0c\x0c'+bytes(range(74))]+[hashlib.shake_256(('quad-vector-'+str(i)).encode()).digest(76+i%5) for i in range(14)]
rows=[]
for i,b in enumerate(fixtures):
 hashes={n:powhash(n,b) for n in libs};r={'fixture':i,'input':b.hex(),'hashes':hashes,'equal':len(set(hashes.values()))==1};rows.append(r);print(i,r['equal'],hashes,flush=True)
(p/'pow-results.json').write_text(json.dumps(rows,indent=2))
print('MATCH',sum(r['equal'] for r in rows),'/',len(rows))
