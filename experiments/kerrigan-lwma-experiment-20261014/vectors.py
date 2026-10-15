from lwma import *
import json
from pathlib import Path
p=Path(__file__).resolve().parent;hard=0x1c07f420;medium=0x1c3fa100;limit=decode(0x1d010000);floor=decode(0x1c7f4200);rows=[]
def test(name,chain,expected,**kw):
 got=next_bits(chain,1,limit,floor,**kw);assert got==expected,(name,hex(got),hex(expected));rows.append(dict(name=name,got=hex(got),expected=hex(expected)))
def blocks(times,bits=hard):return [(t,bits,1) for t in times]
test('upstream_steady',blocks([1700000000+i*480 for i in range(65)]),0x1c07f41f)
test('upstream_bootstrap',blocks([1700000000]),0x1d010000)
t=1700000000;times=[t]
for i in range(1,80):t+=999999 if i==77 else -4000 if i==79 else 480;times.append(t)
test('upstream_clamps',blocks(times),0x1c07a63d)
test('upstream_weighted_floor',blocks([1700000000+(79-i)*3000 for i in range(80)]),0x1b65ce66)
test('upstream_hardware_floor',blocks([1700000000+i*2880 for i in range(65)],medium),0x1c7f4200,floor_active=True)
eqlimit=decode(0x1f100000);got=next_bits(blocks([1700000000+i*480 for i in range(62)],0x1f100000),1,eqlimit,eqlimit);assert got==0x1f0fffff;rows.append(dict(name='upstream_eq192_overflow',got=hex(got),expected='0x1f0fffff'))
chain=blocks([1700000000+i*480 for i in range(70)]);chain +=[(1700000000+70*480+i*120,hard,0) for i in range(44)]
test('upstream_gap44_rearm',chain,encode(decode(hard)<<4),rescue=True)
chain=blocks([1700000000])+[(1700000480+i*120,hard,0) for i in range(41)]
test('upstream_single_gap41_pre',chain,0x1d010000)
test('upstream_single_gap41_post',chain,encode(decode(hard)<<2),rescue=True)
(p/'vectors.json').write_text(json.dumps(rows,indent=2));print('GOLDENS_PASS',len(rows))
