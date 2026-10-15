from model import *
from pathlib import Path
import json
p=Path(__file__).resolve().parent
# Adaptation boundary: one stale lane block followed by19/20/22other-lane blocks.
hard=encode((1<<256)//int(D0[0]*SCALE)-1);limit=decode(hard)*1024
for gap,shift in [(20,2),(22,4)]:
 chain=[(0,hard,0)]+[(i*300,hard,1) for i in range(1,gap+1)]
 assert next_bits(chain,0,limit,limit,algos=2,spacing=300,rescue=True,floor_active=True)==encode(decode(hard)<<shift)
chain=[(0,hard,0)]+[(i*300,hard,1) for i in range(1,20)]
assert next_bits(chain,0,limit,limit,algos=2,spacing=300,rescue=True,floor_active=True)==encode(limit)
for mode in MODES:
 c=Chain(mode);before=c.d[:];credit=c.accept(0,300,300);assert credit==before[0]*W[0]
 assert all(0<decode(c.bits[i])<=c.limits[i] for i in range(2))
 c=Chain(mode);b=copy.deepcopy(c);assert advance(c,random.Random(7),0,10*T,H)==advance(b,random.Random(7),0,10*T,H)
 try:c.accept(0,100,100+1801)
 except ValueError:pass
 else:raise AssertionError('future timestamp accepted')
d=json.loads((p/'results.json').read_text());assert len(d['behaviour'])==320 and len(d['stress'])==320 and sum(len(f['trials']) for f in d['forks'])==3200
(p/'checks.json').write_text(json.dumps({'status':'passed','checks':['adapted20block4xrescue','adapted22block16xrescue','insufficienthistorybootstrapbeforegap','creditactualpreupdatecompactwork','targetspositiveandbounded','seedreplay','futuretimestampreject','runcounts']},indent=2));print('ADAPTATION_CHECKS_PASS')
