from direct_harness import *
import statistics,subprocess
assert json.loads((p/'direct-correctness.json').read_text())['status']=='passed'
cpu=2 if 2 in os.sched_getaffinity(0) else min(os.sched_getaffinity(0));os.sched_setaffinity(0,{cpu});h=Harness()
jobs=json.loads((p.parent/'dego-xkr-dual-testnet-20261014/dual-results.json').read_text())
meta={'cpu_affinity':[cpu],'batch_nonces':1024,'repetitions_per_job':4,'jobs':3,'ratio':1,'order':'ABBA/BAAB balanced within each blob; two runs per mode per block','reason':'Initial snapshot benchmark exhibited order-dependent timing; direct-handoff follow-up predeclared balanced four-run blocks before measurement.','warmup_nonces_per_mode':256}
rows=[]
for j,job in enumerate(jobs):
 work=bytes.fromhex(job['worker']['work']);off=offset(work)
 for mode in ['baseline','shared']:h.run(mode,work,off,90000,256,1)
 for rep in range(4):
  order=['baseline','shared','shared','baseline'] if rep%2==0 else ['shared','baseline','baseline','shared']
  runs=[];reference=None
  for mode in order:
   timing,output=h.run(mode,work,off,200000+rep*1024,1024,1)
   if reference is None:reference=output
   assert output==reference;runs.append({'mode':mode,**timing})
  totals={mode:{key:sum(r[key] for r in runs if r['mode']==mode) for key in ['cpu_s','wall_s']} for mode in ['baseline','shared']}
  row={'job':j,'repetition':rep,'ratio':1,'order':order,'runs':runs,**totals};row['cpu_saving_pct']=100*(1-totals['shared']['cpu_s']/totals['baseline']['cpu_s']);rows.append(row)
  (p/'direct-progress.json').write_text(json.dumps({'finished_blocks':len(rows),'total_blocks':12})+'\n');print('DIRECT_PROGRESS',len(rows),12,flush=True)
b=sum(x['baseline']['cpu_s'] for x in rows);s=sum(x['shared']['cpu_s'] for x in rows);sv=[x['cpu_saving_pct'] for x in rows]
summary={'aggregate_cpu_saving_pct':100*(1-s/b),'baseline_cpu_s':b,'shared_cpu_s':s,'throughput_speedup':b/s,'median_block_saving_pct':statistics.median(sv),'min_block_saving_pct':min(sv),'max_block_saving_pct':max(sv),'wins':sum(x>0 for x in sv),'blocks':len(rows),'aggregate_wall_saving_pct':100*(1-sum(x['shared']['wall_s'] for x in rows)/sum(x['baseline']['wall_s'] for x in rows))}
(p/'direct-benchmark.json').write_text(json.dumps({'metadata':meta,'summary':summary,'trials':rows},indent=2)+'\n');print('DIRECT_DONE',json.dumps(summary),flush=True)
