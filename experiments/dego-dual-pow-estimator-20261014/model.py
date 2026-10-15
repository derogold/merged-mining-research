import math,random,statistics,copy
T=300.;H=[3.,1.];W=[1/3,1.];D0=[1800.,600.];MODES=['signed','clipped','monotonic_clipped'];STRATEGIES=['honest','future','minimum','saw']
class Chain:
 def __init__(self,mode):
  self.mode=mode;self.d=D0[:];self.last=[0,0];self.stamps=[0]*11;self.count=0;self.score=0.;self.negative=0;self.clips=0;self.min_d=1.;self.max_skew=0
 def lower(self,lane):return max(statistics.median(self.stamps[-11:]),self.last[lane] if self.mode=='monotonic_clipped' else 0)
 def choose(self,lane,wall,strategy):
  lo=int(self.lower(lane));hi=int(wall)+1800
  if strategy=='future' or strategy=='saw' and self.count%2==0:return hi
  if strategy=='minimum' or strategy=='saw':return lo
  return max(int(wall),lo)
 def accept(self,lane,wall,stamp):
  if stamp<self.lower(lane) or stamp>int(wall)+1800:raise ValueError('timestamp')
  used=self.d[lane];delta=stamp-self.last[lane];self.negative+=delta<0
  if self.mode!='signed':
   bounded=max(0,min(1200,delta));self.clips+=bounded!=delta;delta=bounded
  exp=max(-2,min(2,(600-delta)/6000));self.d[lane]=max(D0[lane]/1024,used*2**exp)
  self.last[lane]=stamp;self.stamps=(self.stamps+[stamp])[-11:];self.count+=1;self.score+=used*W[lane];self.min_d=min(self.min_d,self.d[lane]/D0[lane]);self.max_skew=max(self.max_skew,stamp-wall)
  return used*W[lane]
def advance(c,rng,start,end,hashes,strategy='honest'):
 t=start;events=[]
 while t<end:
  rates=[hashes[i]/c.d[i] for i in range(2)];total=sum(rates)
  if not total:break
  t+=rng.expovariate(total)
  if t>=end:break
  lane=0 if rng.random()*total<rates[0] else 1;stamp=c.choose(lane,t,strategy);before=c.d[lane];credit=c.accept(lane,t,stamp)
  assert math.isclose(credit,before*W[lane]);events.append((t,lane,credit,stamp))
  assert len(events)<200000
 return events
def warm(mode,seed):
 c=Chain(mode);advance(c,random.Random(seed),0,200*T,H);return c
# Estimator experiment: preserve signed baseline, add rolling-work controls.
BaseChain=Chain
MODES=['signed','window30','window60','window30_monotonic','window60_monotonic']
class Chain(BaseChain):
 def __init__(self,mode):
  super().__init__(mode);self.history=[[(0,0.)],[(0,0.)]];self.cumulative=[0.,0.]
 def lower(self,lane):
  return max(statistics.median(self.stamps[-11:]),self.last[lane] if self.mode.endswith('_monotonic') else 0)
 def accept(self,lane,wall,stamp):
  if self.mode=='signed':return super().accept(lane,wall,stamp)
  if stamp<self.lower(lane) or stamp>int(wall)+1800:raise ValueError('timestamp')
  used=self.d[lane];delta=stamp-self.last[lane];self.negative+=delta<0
  self.cumulative[lane]+=used;hist=self.history[lane];hist.append((stamp,self.cumulative[lane]));window=30 if '30' in self.mode else 60
  if len(hist)>window+1:del hist[0]
  n=len(hist)-1
  if n>=10:
   elapsed=max(1,stamp-hist[0][0]);work=self.cumulative[lane]-hist[0][1]
   self.d[lane]=max(D0[lane]/1024,600*work/elapsed*(n-1)/n)
  self.last[lane]=stamp;self.stamps=(self.stamps+[stamp])[-11:];self.count+=1;self.score+=used*W[lane];self.min_d=min(self.min_d,self.d[lane]/D0[lane]);self.max_skew=max(self.max_skew,stamp-wall)
  return used*W[lane]
