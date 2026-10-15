from model import *
from pathlib import Path
import json
p=Path(__file__).resolve().parent;rows=[]
for mode in MODES:
 for seed in range(20):
  c=warm(mode,seed);r=random.Random(seed+1000);prior=c.d[0];ev=advance(c,r,200*T,400*T,[H[0]*.01,H[1]])
  rows.append(dict(mode=mode,seed=seed,upx_blocks=sum(e[1]==0 for e in ev),turtle_blocks=sum(e[1]==1 for e in ev),upx_difficulty_ratio=c.d[0]/prior))
(p/'weak_lane.json').write_text(json.dumps(rows,indent=2))
for mode in MODES:
 r=[a for a in rows if a['mode']==mode];print(mode,'UPXblocks',statistics.mean(a['upx_blocks'] for a in r),'Drelative',statistics.mean(a['upx_difficulty_ratio'] for a in r),flush=True)
