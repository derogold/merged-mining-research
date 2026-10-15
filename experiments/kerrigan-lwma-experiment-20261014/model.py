from base import *
from lwma import *
SCALE=2**32
BaseChain=Chain
MODES=['lwma_plain_floor16','lwma_rescue_floor16','lwma_plain_floor1024','lwma_rescue_floor1024']
class Chain(BaseChain):
 def __init__(self,mode):
  super().__init__(mode);self.chain=[];self.bits=[encode((1<<256)//int(d*SCALE)-1) for d in D0];factor=1024 if '1024' in mode else 16;self.limits=[decode(b)*factor for b in self.bits]
  self.d=[((1<<256)//(decode(b)+1))/SCALE for b in self.bits]
 def accept(self,lane,wall,stamp):
  if stamp<self.lower(lane) or stamp>int(wall)+1800:raise ValueError('timestamp')
  used=self.d[lane];self.negative+=stamp<self.last[lane];self.last[lane]=stamp;self.stamps=(self.stamps+[stamp])[-11:];self.count+=1;self.score+=used*W[lane];self.max_skew=max(self.max_skew,stamp-wall);self.chain.append((stamp,self.bits[lane],lane))
  for i in range(2):
   self.bits[i]=next_bits(self.chain,i,self.limits[i],self.limits[i],algos=2,spacing=300,rescue='rescue' in self.mode,floor_active=True)
   self.d[i]=((1<<256)//(decode(self.bits[i])+1))/SCALE;self.min_d=min(self.min_d,self.d[i]/D0[i])
  return used*W[lane]
def warm(mode,seed):
 c=Chain(mode);advance(c,random.Random(seed),0,200*T,H);return c
