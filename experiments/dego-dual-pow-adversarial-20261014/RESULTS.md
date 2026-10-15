# Timestamp-aware adversarial results

## Decision

**Do not promote either clipped candidate into daemon consensus.** They reduce honest outage-return bursts but fail baseline calibration and permit substantial timestamp-dependent block rates. The signed original is better calibrated but retains outage recovery problems and timestamp/fork-variance concerns. No production-ready rule emerged.

Completed240outage/control runs,240timestamp-stress runs and2400paired private/public fork trials. Nine model/invariant checks passed. “Checks passed” means the harness followed its rules, not that the candidate consensus is safe. No daemon, mainnet or existing testnet modified.

## Honest throughput and re-entry

T=300seconds; first20Treturn means100minutes. Means over20seeds.

| Rule | Scenario | Disturbance rate / nominal | Recovery rate / nominal | First20T recovery blocks |
|---|---|---:|---:|---:|
|signed|steady|1.004|0.997|18.75|
|signed|upx_offline|0.503|1.051|31.05|
|signed|turtle_offline|0.501|1.052|31.15|
|signed|upx_100x_drop|0.550|1.096|50.80|
|clipped|steady|0.790|0.784|14.80|
|clipped|upx_offline|0.409|0.785|16.45|
|clipped|turtle_offline|0.404|0.786|16.30|
|clipped|upx_100x_drop|0.413|0.787|16.40|
|monotonic_clipped|steady|0.790|0.784|14.80|
|monotonic_clipped|upx_offline|0.409|0.785|16.45|
|monotonic_clipped|turtle_offline|0.404|0.786|16.30|
|monotonic_clipped|upx_100x_drop|0.413|0.787|16.40|

The clipped rules do not deserve a “fixed recovery” label: their reduced bursts accompany a generally slower chain (~0.79nominal). Clipping long intervals changes the feedback's expectation under exponential block arrivals. Increasing one constant to restore the mean would need fresh attack testing; it does not by itself eliminate manipulation.

## Timestamp stress

This deliberately gives the whole simulated branch the chosen clock strategy. It is a stress test, not proof a minority can force the public chain to follow it. Allowed timestamps respect current-height-style median11/future1800second bounds; monotonic_clipped additionally enforces per-lane nondecrease.

| Rule | Strategy | Blocks / nominal | Normalized work / second | Negative lane timestamp deltas across20runs |
|---|---|---:|---:|---:|
|signed|honest|0.998|1.987|0|
|signed|future|1.010|1.989|0|
|signed|minimum|0.145|2.061|37|
|signed|saw|0.998|1.980|4131|
|clipped|honest|0.790|1.989|0|
|clipped|future|0.793|1.992|0|
|clipped|minimum|0.141|2.072|40|
|clipped|saw|1.109|2.000|4474|
|monotonic_clipped|honest|0.790|1.989|0|
|monotonic_clipped|future|0.793|1.992|0|
|monotonic_clipped|minimum|0.143|2.081|0|
|monotonic_clipped|saw|0.445|1.988|0|

For clipped, the future/minimum sawtooth raises rate from~0.79to~1.11nominal with unchanged hashpower. This is a concrete rate-distortion counterexample in the model; it does not create extra expected normalized work. Nondecreasing per-lane timestamps remove negative deltas, but the sawtooth still distorts rate (downward in that variant). Minimum timestamps create slow, high-difficulty/high-variance branches.

## Forks: intermediate leads matter

Branches share the exact warm-up state; capacity splits at a common ancestor. Honest branch uses actual-time templates. Private branch follows one tested timestamp strategy. Fixed normalized score credits each block's PRE-update difficulty. Endpoint lead and any lead after at least6public post-fork blocks are separate metrics. Ties are not wins.

| Rule | Attacker strategy | Fractions UPX,Turtle | Endpoint leads /50 | Any lead after6publicblocks /50 |
|---|---|---|---:|---:|
|signed|honest|[0.1, 0.1]|0|0|
|signed|honest|[0.4, 0.4]|0|18|
|signed|honest|[0.8, 0]|0|18|
|signed|honest|[0, 0.8]|0|15|
|signed|future|[0.1, 0.1]|0|0|
|signed|future|[0.4, 0.4]|0|19|
|signed|future|[0.8, 0]|0|19|
|signed|future|[0, 0.8]|0|20|
|signed|minimum|[0.1, 0.1]|0|0|
|signed|minimum|[0.4, 0.4]|0|23|
|signed|minimum|[0.8, 0]|2|27|
|signed|minimum|[0, 0.8]|2|26|
|signed|saw|[0.1, 0.1]|0|0|
|signed|saw|[0.4, 0.4]|0|17|
|signed|saw|[0.8, 0]|0|21|
|signed|saw|[0, 0.8]|0|19|
|clipped|honest|[0.1, 0.1]|0|0|
|clipped|honest|[0.4, 0.4]|0|18|
|clipped|honest|[0.8, 0]|0|17|
|clipped|honest|[0, 0.8]|0|18|
|clipped|future|[0.1, 0.1]|0|0|
|clipped|future|[0.4, 0.4]|0|18|
|clipped|future|[0.8, 0]|0|16|
|clipped|future|[0, 0.8]|0|17|
|clipped|minimum|[0.1, 0.1]|0|0|
|clipped|minimum|[0.4, 0.4]|0|19|
|clipped|minimum|[0.8, 0]|1|26|
|clipped|minimum|[0, 0.8]|2|23|
|clipped|saw|[0.1, 0.1]|0|0|
|clipped|saw|[0.4, 0.4]|0|17|
|clipped|saw|[0.8, 0]|0|18|
|clipped|saw|[0, 0.8]|0|16|
|monotonic_clipped|honest|[0.1, 0.1]|0|0|
|monotonic_clipped|honest|[0.4, 0.4]|0|18|
|monotonic_clipped|honest|[0.8, 0]|0|17|
|monotonic_clipped|honest|[0, 0.8]|0|18|
|monotonic_clipped|future|[0.1, 0.1]|0|0|
|monotonic_clipped|future|[0.4, 0.4]|0|18|
|monotonic_clipped|future|[0.8, 0]|0|16|
|monotonic_clipped|future|[0, 0.8]|0|17|
|monotonic_clipped|minimum|[0.1, 0.1]|0|0|
|monotonic_clipped|minimum|[0.4, 0.4]|0|20|
|monotonic_clipped|minimum|[0.8, 0]|1|26|
|monotonic_clipped|minimum|[0, 0.8]|2|23|
|monotonic_clipped|saw|[0.1, 0.1]|0|0|
|monotonic_clipped|saw|[0.4, 0.4]|0|19|
|monotonic_clipped|saw|[0.8, 0]|0|17|
|monotonic_clipped|saw|[0, 0.8]|0|17|

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
