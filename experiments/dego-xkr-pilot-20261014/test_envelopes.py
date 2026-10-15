import pathlib,subprocess,ctypes as C,json
p=pathlib.Path(__file__).resolve().parent
lib=C.CDLL('/tmp/dego-xkr-probe/dego-full.so');lib.cn_fast_hash.argtypes=[C.c_void_p,C.c_size_t,C.c_void_p]
def h(b):
 o=C.create_string_buffer(32);lib.cn_fast_hash(b,len(b),o);return o.raw
info={}
for c in ['dego','xkr']:
 lines=subprocess.check_output([str(p/(c+'-native'))],text=True).splitlines();info[c]={'genesis':lines[0],'aux_leaf':lines[1]}
assert info['dego']['genesis']==info['xkr']['genesis']
assert info['dego']['aux_leaf']!=info['xkr']['aux_leaf']
zero=bytes(32);path=bytes.fromhex(info['dego']['genesis'])
def check(c,root,nonce,branches):
 lines=subprocess.check_output([str(p/(c+'-native')),root,str(nonce)]+[b.hex() for b in branches],text=True).splitlines();return dict(zip(['work','pow','parent_bytes','proof_diff1','proof_maxdiff','mutated_branch'],lines))
rows=[]
for depth in [1,2,8,16,32]:
 branches=[h(('sibling-'+str(i)).encode()) for i in range(depth)]
 roots={}
 for c,v in info.items():
  node=bytes.fromhex(v['aux_leaf'])
  for i in reversed(range(depth)):
   bit=(path[i//8]>>(i%8))&1;node=h(branches[i]+node if bit else node+branches[i])
  roots[c]=node.hex()
 for root_owner in ['dego','xkr']:
  for nonce in [0,1,12345]:
   results={c:check(c,roots[root_owner],nonce,branches) for c in info}
   assert results['dego']['work']==results['xkr']['work']
   assert results[root_owner]['proof_diff1']=='1'
   assert results['xkr' if root_owner=='dego' else 'dego']['proof_diff1']=='0'
   assert all(v['mutated_branch']=='0' and v['proof_maxdiff']=='0' for v in results.values())
   assert all(int(v['parent_bytes'])<=2048 for v in results.values())
   rows.append({'depth':depth,'root_owner':root_owner,'root':roots[root_owner],'branches':[b.hex() for b in branches],'nonce':nonce,'results':results})
(p/'envelope-results.json').write_text(json.dumps({'info':info,'same_genesis':True,'rows':rows,'scope':'native serializers, native long hashes, source-extracted unchanged proof predicate except logging; synthetic fixtures, difficulty 1; NOT full block validation'},indent=2))
print(str(len(rows))+' paired envelopes: identical work bytes; owner proof passes, other chain rejects; mutation and max difficulty controls reject.')
