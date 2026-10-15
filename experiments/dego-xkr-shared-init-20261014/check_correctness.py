from harness import *
from concurrent.futures import ThreadPoolExecutor
h=Harness();report={}
known=bytes.fromhex('0100fb8e8ac805899323371bb790db19218afd8db8e3755d8b90f39b3d5506a9abce4fa912244500000000ee8146d49fa93ee724deb57d12cbc6c6f3b924d946127c7a97418f9348828f0f02')
expected={'d':'38591572f820d4de253cf55a2192b622b0289e2e5c3616e61e787a8fe462ec5a','x':'b2172ec9466e1aee70ec8572a14c233ee354582bcb93f869d429744de5726a26'}
assert h.calc('d',known).hex()==expected['d'];assert h.calc('x',known).hex()==expected['x'];assert h.calc('f',known).hex()==expected['d'];assert h.calc('r',known).hex()==expected['x'];report['known_answers']=expected
for n in range(256):
 data=hashlib.shake_256(('shared-init-correctness-'+str(n)).encode()).digest(76+n%65)
 d=h.calc('d',data);x=h.calc('x',data);assert h.calc('f',data)==d;assert h.calc('r',data)==x
report['variable_input_pairs']=256
jobs=json.loads((p.parent/'dego-xkr-dual-testnet-20261014/dual-results.json').read_text());rows=[]
for j,job in enumerate(jobs):
 work=bytes.fromhex(job['worker']['work'])
 for ratio in [1,2,4,8]:
  a,ar=h.run('baseline',work,offset(work),0,512,ratio);b,br=h.run('shared',work,offset(work),0,512,ratio);assert ar==br
  rows.append({'job':j,'ratio':ratio,'nonces':512,'digest':a['digest']})
report['real_work_batches']=rows
cpus=sorted(os.sched_getaffinity(0))
def thread_check(t):
 os.sched_setaffinity(0,{cpus[(t+2)%len(cpus)]})
 for n in range(128):
  data=hashlib.shake_256(f'thread-{t}-{n}'.encode()).digest(100)
  d=h.calc('d',data);x=h.calc('x',data);assert h.calc('f',data)==d;time.sleep(0);assert h.calc('r',data)==x
 return 128
with ThreadPoolExecutor(max_workers=4) as ex:report['threaded_pairs']=sum(ex.map(thread_check,range(4)))
report['status']='passed';(p/'correctness.json').write_text(json.dumps(report,indent=2)+'\n');print('CORRECTNESS_PASS',flush=True)
