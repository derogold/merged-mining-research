from harness import *
import statistics,platform,subprocess
cpu=2 if 2 in os.sched_getaffinity(0) else min(os.sched_getaffinity(0));os.sched_setaffinity(0,{cpu});h=Harness()
assert json.loads((p/'correctness.json').read_text())['status']=='passed'
jobs=json.loads((p.parent/'dego-xkr-dual-testnet-20261014/dual-results.json').read_text())
meta={'cpu_affinity':[cpu],'clock':'thread CPU time; wall time also retained','batch_nonces':2048,'repetitions':7,'jobs':3,'ratios':[1,2,4,8],'order':'alternating per matched pair','warmup_nonces_per_mode':256,'host':platform.platform(),'lscpu':subprocess.check_output(['lscpu'],text=True),'uptime_before':subprocess.check_output(['uptime'],text=True)}
rows=[]
for j,job in enumerate(jobs):
 work=bytes.fromhex(job['worker']['work']);off=offset(work)
 for mode in ['baseline','shared']:h.run(mode,work,off,90000,256,1)
 for rep in range(7):
  for ratio in [1,2,4,8]:
   order=['baseline','shared'] if (j+rep+ratio)%2 else ['shared','baseline'];pair={};outputs={}
   for mode in order:pair[mode],outputs[mode]=h.run(mode,work,off,100000+rep*2048,2048,ratio)
   assert outputs['baseline']==outputs['shared']
   row={'job':j,'repetition':rep,'ratio':ratio,'order':order,**pair};row['cpu_saving_pct']=100*(1-pair['shared']['cpu_s']/pair['baseline']['cpu_s']);rows.append(row)
   (p/'benchmark-progress.json').write_text(json.dumps({'finished_pairs':len(rows),'total_pairs':84})+'\n')
  print('BENCHMARK_PROGRESS',len(rows),84,flush=True)
summary={}
for ratio in [1,2,4,8]:
 rr=[x for x in rows if x['ratio']==ratio];base=sum(x['baseline']['cpu_s'] for x in rr);shared=sum(x['shared']['cpu_s'] for x in rr);sv=[x['cpu_saving_pct'] for x in rr]
 summary[ratio]={'baseline_cpu_s':base,'shared_cpu_s':shared,'aggregate_cpu_saving_pct':100*(1-shared/base),'throughput_speedup':base/shared,'median_paired_saving_pct':statistics.median(sv),'min_paired_saving_pct':min(sv),'max_paired_saving_pct':max(sv),'paired_trials':len(rr),'shared_wins':sum(x>0 for x in sv)}
meta['uptime_after']=subprocess.check_output(['uptime'],text=True)
(p/'benchmark.json').write_text(json.dumps({'metadata':meta,'summary':summary,'trials':rows},indent=2)+'\n');print('BENCHMARK_DONE',json.dumps(summary),flush=True)
