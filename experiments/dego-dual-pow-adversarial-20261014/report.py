from model import *
import json
from pathlib import Path
p=Path(__file__).resolve().parent;d=json.loads((p/'results.json').read_text())
s='''# Timestamp-aware adversarial results

## Decision

**Do not promote either clipped candidate into daemon consensus.** They reduce honest outage-return bursts but fail baseline calibration and permit substantial timestamp-dependent block rates. The signed original is better calibrated but retains outage recovery problems and timestamp/fork-variance concerns. No production-ready rule emerged.

Completed240outage/control runs,240timestamp-stress runs and2400paired private/public fork trials. Nine model/invariant checks passed. “Checks passed” means the harness followed its rules, not that the candidate consensus is safe. No daemon, mainnet or existing testnet modified.

## Honest throughput and re-entry

T=300seconds; first20Treturn means100minutes. Means over20seeds.

| Rule | Scenario | Disturbance rate / nominal | Recovery rate / nominal | First20T recovery blocks |
|---|---|---:|---:|---:|
'''
for mode in MODES:
 for scenario in ['steady','upx_offline','turtle_offline','upx_100x_drop']:
  r=[a for a in d['behaviour'] if a['mode']==mode and a['scenario']==scenario]
  s+=f'|{mode}|{scenario}|{statistics.mean(a["during_rate"] for a in r):.3f}|{statistics.mean(a["recovery_rate"] for a in r):.3f}|{statistics.mean(a["first20T"] for a in r):.2f}|\n'
s+='''
The clipped rules do not deserve a “fixed recovery” label: their reduced bursts accompany a generally slower chain (~0.79nominal). Clipping long intervals changes the feedback's expectation under exponential block arrivals. Increasing one constant to restore the mean would need fresh attack testing; it does not by itself eliminate manipulation.

## Timestamp stress

This deliberately gives the whole simulated branch the chosen clock strategy. It is a stress test, not proof a minority can force the public chain to follow it. Allowed timestamps respect current-height-style median11/future1800second bounds; monotonic_clipped additionally enforces per-lane nondecrease.

| Rule | Strategy | Blocks / nominal | Normalized work / second | Negative lane timestamp deltas across20runs |
|---|---|---:|---:|---:|
'''
for mode in MODES:
 for strategy in STRATEGIES:
  r=[a for a in d['stress'] if a['mode']==mode and a['strategy']==strategy]
  s+=f'|{mode}|{strategy}|{statistics.mean(a["rate"] for a in r):.3f}|{statistics.mean(a["score_per_second"] for a in r):.3f}|{sum(a["negative_deltas"] for a in r)}|\n'
s+='''
For clipped, the future/minimum sawtooth raises rate from~0.79to~1.11nominal with unchanged hashpower. This is a concrete rate-distortion counterexample in the model; it does not create extra expected normalized work. Nondecreasing per-lane timestamps remove negative deltas, but the sawtooth still distorts rate (downward in that variant). Minimum timestamps create slow, high-difficulty/high-variance branches.

## Forks: intermediate leads matter

Branches share the exact warm-up state; capacity splits at a common ancestor. Honest branch uses actual-time templates. Private branch follows one tested timestamp strategy. Fixed normalized score credits each block's PRE-update difficulty. Endpoint lead and any lead after at least6public post-fork blocks are separate metrics. Ties are not wins.

| Rule | Attacker strategy | Fractions UPX,Turtle | Endpoint leads /50 | Any lead after6publicblocks /50 |
|---|---|---|---:|---:|
'''
for f in d['forks']:
 end=sum(t['endpoint_lead'] for t in f['trials']);ever=sum(t['lead_after_six_public_blocks'] for t in f['trials'])
 s+=f'|{f["mode"]}|{f["strategy"]}|{f["alpha"]}|{end}|{ever}|\n'
s+='''
Example: signed rule,80%ofUPX and0%ofTurtle (40%ofassumed normalized baseline capacity), honest private timestamps:0/50endpoint leads but18/50temporary leads after6publicblocks. Minimum timestamps:2/50endpoint leads and27/50temporary leads. These finite samples do not establish a significant strategy advantage. A minority can lead stochastically; this is not by itself a consensus failure. The minimum-timestamp strategy changes difficulty/variance and merits targeted follow-up.

**These are not general six-confirmation double-spend probabilities.** Attack starts at the common ancestor; no transaction-arrival process, publication timing, honest switching, network propagation, branch survival after release, adaptive strategy selection or real market hashpower modeled. No receiver clock skew modeled. The endpoint metric previously used missed transient opportunities; this pass corrects that limitation.

## Source correspondence and limitations

Inspected pinned DEGO config/Core: current-height future allowance6×300seconds, previous11timestamp median lower bound inclusive; honest template max(wall,median). Historical activation/sync-floor exceptions omitted. Independent-lane difficulty and monotonic rule are proposed simulation rules, not existing DEGO behavior. Header selection at discovery approximates continuous template refresh; no post-proof header changes are permitted in real mining.

Real times and header times are separate; timestamps integer, difficulty/score floating point. Actual native PoW, exact256bit target rounding, overflow, lane-tag encoding and commitment binding, activation, public replay, topology and clock drift remain unimplemented. Weight(1/3,1) is arbitrary calibration, not a verified economic conversion. No energy claim.

## Next design work

1. Do not simply cap elapsed times and declare re-entry solved. Compare a specified, bias-aware per-lane estimator against this signed baseline, including100×hash changes and timestamp strategies.
2. Add selective publication/clock-skew and minimum-timestamp high-variance cases; evaluate outcomes at release, not only endpoint or temporary score lead.
3. Select explicit chain-work weights and what “equal lanes” is intended to mean; do not infer that policy from benchmark speed.
4. Only then freeze integer consensus rules and implement isolated daemon tests. Keeping either lane usable remains the design goal; no return to strict alternation is recommended on these results.
'''
(p/'RESULTS.md').write_text(s)
