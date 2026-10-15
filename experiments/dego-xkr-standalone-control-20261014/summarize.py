from pathlib import Path
import json,statistics
p=Path(__file__).resolve().parent;d=json.loads((p/'results.json').read_text());t=d['cpu_totals'];blocks=d['rows']
r={'blocks':len(blocks),'cpu_totals_s':t,'paired_vs_standalone_cpu_change_pct':100*(t['paired']/t['standalone']-1),'paired_wins_vs_standalone':sum(b['totals']['paired']<b['totals']['standalone'] for b in blocks),'standalone_vs_original_cpu_reduction_pct':100*(1-t['standalone']/t['original']),'paired_vs_original_cpu_reduction_pct':100*(1-t['paired']/t['original']),'block_paired_vs_standalone_change_pct':[100*(b['totals']['paired']/b['totals']['standalone']-1) for b in blocks]}
r['standalone_dego_cpu_s']=sum(v['dego_cpu_s'] for b in blocks for v in b['runs'] if v['mode']=='standalone');r['standalone_xkr_cpu_s']=sum(v['xkr_cpu_s'] for b in blocks for v in b['runs'] if v['mode']=='standalone')
r['paired_vs_standalone_wall_change_pct']=100*(sum(v['wall_s'] for b in blocks for v in b['runs'] if v['mode']=='paired')/sum(v['wall_s'] for b in blocks for v in b['runs'] if v['mode']=='standalone')-1)
(p/'summary.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
