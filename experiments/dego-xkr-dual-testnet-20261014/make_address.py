# Test-only address, both public keys = Ed25519 basepoint (publicly known secret 1).
# NEVER use for real funds. Uses existing native cn_fast_hash probe library.
import ctypes as C
l=C.CDLL('/tmp/dego-xkr-probe/dego-full.so');l.cn_fast_hash.argtypes=[C.c_void_p,C.c_size_t,C.c_void_p]
b=bytes([0x96,0xd6,0x88,0x01])+bytes.fromhex('58'+'66'*31)*2
h=C.create_string_buffer(32);l.cn_fast_hash(b,len(b),h);b+=h.raw[:4]
a='123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';sizes=[0,2,3,5,6,7,9,10,11]
def enc(x):
 n=int.from_bytes(x,'big');s=''
 while n:s=a[n%58]+s;n//=58
 return s.rjust(sizes[len(x)],'1')
print(''.join(enc(b[i:i+8]) for i in range(0,len(b),8)))
