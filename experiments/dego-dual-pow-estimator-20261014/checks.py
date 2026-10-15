from model import *
from pathlib import Path
import json
p=Path(__file__).resolve().parent;checks=[];warm_counts={}
for mode in MODES:
 c=Chain(mode);c.stamps=[100]*11;c.last=[100,100]
 for bad in [99,1901]:
  try:c.accept(0,100,bad)
  except ValueError:pass
  else:raise AssertionError('invalid stamp accepted')
 c.accept(0,100,100);c.accept(1,100,1900)
 c=Chain(mode);c.stamps=[100]*10+[500];c.last=[500,100]
 if mode.endswith('_monotonic'):
  try:c.accept(0,500,100)
  except ValueError:pass
  else:raise AssertionError('rewind accepted')
 else:c.accept(0,500,100)
 c=warm(mode,17);b=copy.deepcopy(c);assert advance(c,random.Random(19),200*T,220*T,H,'saw')==advance(b,random.Random(19),200*T,220*T,H,'saw')
 c=Chain(mode);before=c.d[:];credit=c.accept(0,10000,10000);assert credit==before[0]*W[0] and c.d[1]==before[1]
 if mode!='signed':
  c=Chain(mode)
  for k in range(1,11):c.accept(0,k*600,k*600)
  assert math.isclose(c.d[0],D0[0]*.9)
  assert len(c.history[0])==11
  states=[warm(mode,seed) for seed in range(20)];warm_counts[mode]=[min(len(c.history[i])-1 for c in states) for i in range(2)]
checks=['timestamp boundaries','explicit monotonic constraint','seed replay','credit pre-update work','other lane unchanged','ten-interval formula','actual warm-up history recorded']
# Verify bias correction only in the setting it actually proves: fixed difficulty.
rng=random.Random(33);bias={}
for n in [30,60]:
 values=[(n-1)/sum(rng.expovariate(1) for _ in range(n)) for _ in range(20000)];bias[str(n)]=statistics.mean(values);assert abs(bias[str(n)]-1)<.01
checks.append('constant-difficulty inverse-time bias control')
d=json.loads((p/'results.json').read_text());assert len(d['behaviour'])==400 and len(d['stress'])==400 and sum(len(f['trials']) for f in d['forks'])==4000;checks.append('run counts')
(p/'checks.json').write_text(json.dumps({'status':'passed','checks':checks,'constant_D_mean_ratio':bias,'minimum_warm_history_intervals_per_lane':warm_counts},indent=2));print('CHECKS_PASS',bias,warm_counts)
