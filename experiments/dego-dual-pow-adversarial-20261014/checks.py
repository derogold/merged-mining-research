from model import *
import json
from pathlib import Path
p=Path(__file__).resolve().parent;passed=[]
for mode in MODES:
 c=Chain(mode);c.stamps=[100]*11;c.last=[100,100]
 for bad in [99,1901]:
  try:c.accept(0,100,bad)
  except ValueError:pass
  else:raise AssertionError('bad timestamp accepted')
 c.accept(0,100,100);c.accept(1,100,1900)
 # Same-lane backwards timestamp rejected only by added monotonic rule;
 # equal median is valid under existing-style median rule.
 c=Chain(mode);c.stamps=[100]*10+[500];c.last=[500,100]
 if mode=='monotonic_clipped':
  try:c.accept(0,500,100)
  except ValueError:pass
  else:raise AssertionError('lane rewind accepted')
 else:c.accept(0,500,100)
 c=Chain(mode);before=c.d[:];credit=c.accept(0,10000,10000);assert credit==before[0]*W[0] and c.d[1]==before[1]
 c=warm(mode,99);b=copy.deepcopy(c);e1=advance(c,random.Random(7),200*T,220*T,H,'saw');e2=advance(b,random.Random(7),200*T,220*T,H,'saw');assert e1==e2 and c.__dict__==b.__dict__
 c=warm(mode,3);before=copy.deepcopy(c.__dict__);assert advance(c,random.Random(1),200*T,400*T,[0,0])==[] and c.__dict__==before
 assert c.d[0]>0 and c.d[1]>0
passed=['past and future timestamps rejected','inclusive median/future boundaries accepted','lane monotonicity only where explicitly enabled','block credited pre-update work','other lane difficulty unchanged','deterministic replay','zero hashpower leaves chain unchanged']
d=json.loads((p/'results.json').read_text());assert len(d['behaviour'])==240 and len(d['stress'])==240 and sum(len(x['trials']) for x in d['forks'])==2400
assert all(r['max_future_offset_s']<=1800 for r in d['stress']);passed+=['run counts','future bound respected in stress runs']
(p/'checks.json').write_text(json.dumps({'status':'passed','checks':passed},indent=2));print('CHECKS_PASS',len(passed))
