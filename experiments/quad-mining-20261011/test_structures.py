"""Native hash/branch routines; source-derived serialization models, NOT full daemon validation."""
import ctypes as C,pathlib,json
p=pathlib.Path(__file__).resolve().parent
libs={n:C.CDLL(str(p/(n+'.dylib')),mode=C.RTLD_LOCAL) for n in ['dego','wrkz','upx','xfg']}
for l in libs.values():
 l.cn_fast_hash.argtypes=[C.c_void_p,C.c_size_t,C.c_void_p];l.cn_fast_hash.restype=None
for n in ['dego','wrkz','xfg']:
 libs[n].tree_hash_from_branch.argtypes=[C.c_void_p,C.c_size_t,C.c_void_p,C.c_void_p,C.c_void_p];libs[n].tree_hash_from_branch.restype=None
def H(b,n='dego'):
 o=C.create_string_buffer(32);libs[n].cn_fast_hash(b,len(b),o);return o.raw
def branch_hash(n,b,leaf,key):
 o=C.create_string_buffer(32);libs[n].tree_hash_from_branch(b''.join(b),len(b),leaf,key,o);return o.raw
def varint(n):
 b=bytearray()
 while n>=128:b.append((n&127)|128);n>>=7
 b.append(n);return bytes(b)
def bit(k,d):return (k[d//8]>>(d%8))&1
rows=[]
def check(name,value):
 rows.append({'test':name,'passed':bool(value)});assert value,name
check('native Keccak empty known answer',H(b'').hex()=='c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470')
for count in [2,3,4]:
 keys=[H(('chain-'+str(i)).encode()) for i in range(count)];leaves=[H(('block-'+str(i)).encode()) for i in range(count)]
 depth=next(d for d in range(1,32) if len({int.from_bytes(k,'little')&((1<<d)-1) for k in keys})==count)
 proofs={i:[] for i in range(count)}
 def node(ids,level):
  if not ids:return bytes(32)
  if level==depth:return leaves[ids[0]]
  sides=[[i for i in ids if bit(keys[i],level)==s] for s in [0,1]]
  roots=[node(ids,level+1) for ids in sides]
  for s in [0,1]:
   for i in sides[s]:proofs[i].insert(0,roots[1-s])
  return H(roots[0]+roots[1])
 root=node(list(range(count)),0)
 for n in ['dego','wrkz','xfg']:
  for i in range(count):
   check(f'{count}-leaf/{n}/chain-{i} accepted branch root',branch_hash(n,proofs[i],leaves[i],keys[i])==root)
   bad=bytes([leaves[i][0]^1])+leaves[i][1:]
   check(f'{count}-leaf/{n}/chain-{i} rejects changed leaf',branch_hash(n,proofs[i],bad,keys[i])!=root)
   changed=proofs[i].copy();changed[0]=bytes([changed[0][0]^1])+changed[0][1:]
   check(f'{count}-leaf/{n}/chain-{i} rejects changed branch',branch_hash(n,changed,leaves[i],keys[i])!=root)
# Synthetic source-derived coinbase prefix: version, unlock, gen input height, one key output, extra.
extra=b'\x01'+bytes.fromhex('58'+'66'*31)+b'\x03'+varint(33)+varint(0)+H(b'aux-root')
def prefix(version):return varint(version)+varint(1000060)+b'\x01\xff'+varint(1000000)+b'\x01'+varint(1000000)+b'\x02'+bytes.fromhex('58'+'66'*31)+varint(len(extra))+extra
v1={n:H(prefix(1),n) for n in libs}
check('v1 coinbase hashes equal across native fast hashes',len(set(v1.values()))==1)
v2_upx=H(H(prefix(2),'upx')+H(b'\x00','upx')+bytes(32),'upx')
v2_dego=H(H(prefix(2))+bytes.fromhex('bc36789e7a1e281436464229828f817d6612f7b477d66591ff96a9e064bcc98a')+bytes(32))
v2_xfg=H(prefix(2),'xfg')
check('v2 UPX hash model matches DEGO special case',v2_upx==v2_dego)
check('v2 Fuego serialized hash model differs from UPX',v2_xfg!=v2_upx)
# Native tree construction and source-derived work bytes, 1,2,3,7 transactions.
work=[]
for count in [1,2,3,7]:
 leaves=[v1['upx']]+[H(('tx-'+str(i)).encode()) for i in range(count-1)]
 roots={}
 for n,l in libs.items():
  o=C.create_string_buffer(32);l.tree_hash.argtypes=[C.c_void_p,C.c_size_t,C.c_void_p];l.tree_hash.restype=None;l.tree_hash(b''.join(leaves),count,o);roots[n]=o.raw
 check(f'{count} tx native roots equal',len(set(roots.values()))==1)
 blobs={n:varint(12)+varint(12)+varint(1791700000)+H(b'UPX previous')+(42).to_bytes(4,'little')+roots[n]+varint(count) for n in libs}
 check(f'{count} tx source-derived work bytes equal',len(set(blobs.values()))==1)
 work.append({'transactions':count,'blob':blobs['upx'].hex()})
(p/'structure-results.json').write_text(json.dumps({'tests':rows,'work_fixtures':work,'v2_hashes':{'upx':v2_upx.hex(),'dego':v2_dego.hex(),'xfg':v2_xfg.hex()},'limitations':'serialization modeled from source; no daemon acceptance'},indent=2))
print('PASS',len(rows),'checks; native crypto + explicitly modeled serialization')
