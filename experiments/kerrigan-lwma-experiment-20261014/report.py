from pathlib import Path
import json,statistics as s
p=Path(__file__).resolve().parent;d=json.loads((p/'results.json').read_text());modes=list(dict.fromkeys(x['mode'] for x in d['behaviour']));summary=[]
text='''# Kerrigan LWMA: verified port, exploratory DEGO adaptation

## Verified arithmetic

Nine selected upstream regression cases matched exact compact target outputs.256generated histories matched an isolated native oracle using the unchanged pinned LwmaPerAlgo function and original256bit arithmetic. Tests cover typical/negative/large timestamp intervals, sparse histories, bootstrap, rescue flag and floor flag. This is not the entire upstream Boost test suite, legacy dispatcher, daemon validation or live-network activation proof.

## Adaptation

Four variants: plain/rescue LWMA with easiest targets16×or1024×initial targets. Two algorithms,300second overall target,600second lane target. Rescue at20other-chain blocks,4×easier per2additionalblocks, per direct parameter scaling of Kerrigan's4algorithm policy. No claim that this scaling is optimal.

The original hardware floors cannot be copied blindly: they are treated as sensitivity parameters. Both lanes' next targets recompute from the new parent; other-lane progress can trigger rescue. The exact integer retarget is retained, but event timing and hashpower are stochastic model values. Chain weights and timestamp validation come from our DEGO research model, not HMP.

## Behaviour (20seed means)

Rate1=nominal300seconds/block; first20T means first100minutes of recovery, nominal20blocks.

| Variant | Scenario | Disturbance rate | Recovery rate | First20T recovery blocks |
|---|---|---:|---:|---:|
'''
for mode in modes:
 for scenario in ['steady','upx_offline','turtle_offline','upx_100x_drop']:
  r=[a for a in d['behaviour'] if a['mode']==mode and a['scenario']==scenario];v=dict(mode=mode,scenario=scenario,during=s.mean(a['during_rate'] for a in r),recovery=s.mean(a['recovery_rate'] for a in r),first20=s.mean(a['first20T'] for a in r));summary.append(v)
  text+=f'|{mode}|{scenario}|{v["during"]:.3f}|{v["recovery"]:.3f}|{v["first20"]:.2f}|\n'
text+='''
## Timestamp stress

Full-branch strategy control, not an assertion a minority owns public timestamps. Score/sec expected~2in the arbitrary normalized units.

| Variant | Strategy | Rate / nominal | Normalized work/sec |
|---|---|---:|---:|
'''
for mode in modes:
 for strategy in ['honest','future','minimum','saw']:
  r=[a for a in d['stress'] if a['mode']==mode and a['strategy']==strategy];text+=f'|{mode}|{strategy}|{s.mean(a["rate"] for a in r):.3f}|{s.mean(a["score_per_second"] for a in r):.3f}|\n'
text+='''
## Fork regression

These are adapted-model results, not Kerrigan security measurements: HMP seal-weighted selection, selective publication, receiver clock skew and network propagation are absent. Finite endpoint/transient lead counts are not a general double-spend probability. All raw per-seed trials retained in results.json.

| Variant | Strategy | Attacker fractions UPX,Turtle | Endpoint leads/50 | Transient leads after6publicblocks/50 |
|---|---|---|---:|---:|
'''
for f in d['forks']:
 text+=f'|{f["mode"]}|{f["strategy"]}|{f["alpha"]}|{sum(t["endpoint_lead"] for t in f["trials"])}|{sum(t["lead_after_six_public_blocks"] for t in f["trials"])}|\n'
text+='''
## Comparison reference

Previous signed toy baseline: normal~0.998nominal, outage-return~31blocks/20T. Previous60work-window+dormancy-reset: normal~1.010, outage-return~20, but100×weakenedUPXfound~1block/200Tand barely adjusted difficulty. Those are separate measured simulation runs with same scenario/seeds, not native Kerrigan behavior.

No code was deployed or consensus changed. The supplied integer port is a research comparator, not a production library. Bounds/rounding/bootstrap source fidelity was checked for selected/generated histories; exhaustive correctness/security was not proven.
'''
(p/'RESULTS.md').write_text(text);(p/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
w=json.loads((p/'weak_lane.json').read_text())
with (p/'RESULTS.md').open('a') as f:
 f.write('\n## Weak-lane recovery (same100×UPXloss scenario)\n\n| Variant | UPXblocks over200T | End UPXdifficulty / pre-loss |\n|---|---:|---:|\n')
 for mode in modes:
  rr=[a for a in w if a['mode']==mode];f.write(f'|{mode}|{s.mean(a["upx_blocks"] for a in rr):.2f}|{s.mean(a["upx_difficulty_ratio"] for a in rr):.3f}|\n')
 f.write('\nMore weak-lane blocks does not imply full recovery to50%share, nor no outage-return burst. Floor choice is a consensus/security parameter, not a free optimization.\n')
