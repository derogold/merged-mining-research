# Source-derived genesis serialization model, not full native daemon reconstruction.
import ctypes as C,json,pathlib
p=pathlib.Path(__file__).resolve().parent;d=json.loads((p/'inputs.json').read_text());l=C.CDLL('/tmp/dego-xkr-probe/dego-full.so');l.cn_fast_hash.argtypes=[C.c_void_p,C.c_size_t,C.c_void_p]
def h(x):
 b=C.create_string_buffer(32);l.cn_fast_hash(x,len(x),b);return b.raw
for c,v in d.items():
 tx=bytes.fromhex(v['tx']);work=b'\x01\x00\x00'+bytes(32)+v['nonce'].to_bytes(4,'little')+h(tx)+b'\x01';assert len(work)<128;v['modeled_hash']=h(bytes([len(work)])+work).hex();v['work']=work.hex()
assert d['dego']['modeled_hash']=='7fb97df81221dd1366051b2d0bc7f49c66c22ac4431d879c895b06d66ef66f4c'
assert d['wrkz']['modeled_hash']=='877e55b4e902b9bf4c9e0a7c16440f449339d56679c49d62261ae5c92596a6ce'
(p/'results.json').write_text(json.dumps(d,indent=2));print({c:v['modeled_hash'] for c,v in d.items()})
