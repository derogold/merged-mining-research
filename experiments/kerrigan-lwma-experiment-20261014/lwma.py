MASK=(1<<256)-1

def decode(bits):
 size=bits>>24;word=bits&0x7fffff
 return word>>(8*(3-size)) if size<=3 else (word<<(8*(size-3)))&MASK

def encode(value):
 size=(value.bit_length()+7)//8
 word=value<<(8*(3-size)) if size<=3 else value>>(8*(size-3))
 if word&0x800000:word>>=8;size+=1
 return (size<<24)|(word&0x7fffff)

def next_bits(chain,lane,powlimit,floor,*,algos=4,spacing=120,rescue=False,floor_active=False):
 # chain entries: (timestamp, compact target, algorithm); height=index.
 effective=floor if floor_active else powlimit;N=60;T=spacing*algos
 recent=[]
 for height in range(len(chain)-1,max(-1,len(chain)-1-(N+1)*algos*8),-1):
  ts,bits,a=chain[height]
  if a==lane:recent.append((height,ts,bits))
  if len(recent)>=N+1:break
 if rescue and recent:
  gap=len(chain)-1-recent[0][0];threshold=algos*10
  if gap>=threshold:
   target=decode(recent[0][2]);limit=decode(encode(effective));steps=1+(gap-threshold)//algos
   for _ in range(steps):
    if target>=limit:break
    if target>limit>>2:target=limit;break
    target=(target<<2)&MASK
   return encode(min(target,limit))
 if len(recent)<2:return encode(effective)
 n=min(N,len(recent)-1);k=n*(n+1)//2*T;weighted=0;total=0
 for i in range(1,n+1):
  cur,prev=recent[n-i],recent[n-i+1];dt=max(-5*T,min(6*T,cur[1]-prev[1]));weighted+=dt*i;total=(total+decode(cur[2]))&MASK
 weighted=max(k//20,weighted)
 target=((total//n//k)*(weighted&0xffffffff))&MASK
 target=min(target,powlimit)
 if floor_active:target=min(target,floor)
 if target==0:target=floor
 return encode(target)
