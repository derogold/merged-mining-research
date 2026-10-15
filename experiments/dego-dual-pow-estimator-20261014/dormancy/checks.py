from model import *
from pathlib import Path
import json
p=Path(__file__).resolve().parent
for mode in MODES:
 c=Chain(mode);c.count=31;c.last_height=[0,31];c.d=[1234,600];prior=c.score
 credit=c.accept(0,15000,15000);assert credit==1234*W[0] and c.score==prior+credit and c.d[0]==1234 and len(c.history[0])==1 and c.resets==1
 for i in range(1,10):c.accept(0,15000+i*600,15000+i*600);assert c.d[0]==1234
 c.accept(0,21000,21000);assert math.isclose(c.d[0],1234*.9)
 c=Chain(mode);c.count=29;c.last_height=[0,29];c.accept(0,15000,15000);assert c.resets==0
 c=Chain(mode);c.count=30;c.last_height=[0,30];c.accept(0,15000,15000);assert c.resets==1
 c=warm(mode,3);b=copy.deepcopy(c);assert advance(c,random.Random(3),200*T,300*T,H,'saw')==advance(b,random.Random(3),200*T,300*T,H,'saw')
rows=[]
for mode in MODES:
 for seed in range(20):
  c=warm(mode,seed);r=random.Random(seed+1000);before=c.d[0];ev=advance(c,r,200*T,400*T,[H[0]*.01,H[1]])
  rows.append(dict(mode=mode,seed=seed,upx_blocks=sum(e[1]==0 for e in ev),turtle_blocks=sum(e[1]==1 for e in ev),upx_difficulty_ratio=c.d[0]/before,resets=c.resets))
(p/'weak_lane.json').write_text(json.dumps(rows,indent=2));(p/'checks.json').write_text(json.dumps({'status':'passed','checks':['dormant block credited at old target','difficulty retained and history reset','first9intervals retain difficulty','estimator resumes on10thinterval','29blocks do not trigger reset','30blocks trigger reset','deterministic replay']},indent=2));print('RESET_CHECKS_PASS')
