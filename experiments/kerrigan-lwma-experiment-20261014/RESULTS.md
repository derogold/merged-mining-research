# Verdict

Use the verified Kerrigan LWMA as the next research baseline; our custom rolling-work estimator is not justified by these comparative results. Do NOT blindly adopt its rescue/floor constants or HMP architecture.

- Normal production: plain/rescue LWMA~0.99–1.00nominal in these scenarios, without the~21%slowdown of our naïve clipped rule.
- Plain LWMA outage return:~20–21blocks per20T, versus~39for our plain60work-window and~20for our explicit dormancy reset.
- Rescue with tighter16×targetcap:~24outage-return blocks, but~39after recovery from100×hashloss. Weak-lane blocks improve~1.2->4.55over200T.
- Rescue with permissive1024×targetcap:~76–77outage-return blocks and~86after recovery from100×hashloss. Weak-lane blocks improve~0.9->12.95. Recovery helps but bursts can be large.
- Timestamp minimum/sawtooth strategies still distort cadence in full-branch stress (~0.15/~0.76nominal). No blanket timestamp-security claim. Private-fork simulation excludes HMP and publication/network effects.

This establishes a useful implementation reference, not production approval. Keep integer port and golden/native checks as reusable evidence. Next concrete implementation work can use this LWMA as an isolated testnet baseline while keeping rescue policy explicit and configurable for research. Floors need DEGO-specific calibration, and lane encoding/chain-work/activation rules still require specification. No daemon changes in this task.

# Kerrigan LWMA: verified port, exploratory DEGO adaptation

## Verified arithmetic

Nine selected upstream regression cases matched exact compact target outputs.256generated histories matched an isolated native oracle using the unchanged pinned LwmaPerAlgo function and original256bit arithmetic. Tests cover typical/negative/large timestamp intervals, sparse histories, bootstrap, rescue flag and floor flag. This is not the entire upstream Boost test suite, legacy dispatcher, daemon validation or live-network activation proof.

## Adaptation

Four variants: plain/rescue LWMA with easiest targets16×or1024×initial targets. Two algorithms,300second overall target,600second lane target. Rescue at20other-chain blocks,4×easier per2additionalblocks, per direct parameter scaling of Kerrigan's4algorithm policy. No claim that this scaling is optimal.

The original hardware floors cannot be copied blindly: they are treated as sensitivity parameters. Both lanes' next targets recompute from the new parent; other-lane progress can trigger rescue. The exact integer retarget is retained, but event timing and hashpower are stochastic model values. Chain weights and timestamp validation come from our DEGO research model, not HMP.

## Behaviour (20seed means)

Rate1=nominal300seconds/block; first20T means first100minutes of recovery, nominal20blocks.

| Variant | Scenario | Disturbance rate | Recovery rate | First20T recovery blocks |
|---|---|---:|---:|---:|
|lwma_plain_floor16|steady|0.997|0.993|19.35|
|lwma_plain_floor16|upx_offline|0.499|1.004|20.85|
|lwma_plain_floor16|turtle_offline|0.506|1.001|20.40|
|lwma_plain_floor16|upx_100x_drop|0.504|1.022|22.90|
|lwma_rescue_floor16|steady|0.997|0.993|19.35|
|lwma_rescue_floor16|upx_offline|0.499|1.039|24.35|
|lwma_rescue_floor16|turtle_offline|0.506|1.036|23.85|
|lwma_rescue_floor16|upx_100x_drop|0.518|1.108|39.25|
|lwma_plain_floor1024|steady|1.004|0.993|19.25|
|lwma_plain_floor1024|upx_offline|0.509|1.004|21.10|
|lwma_plain_floor1024|turtle_offline|0.502|1.008|21.20|
|lwma_plain_floor1024|upx_100x_drop|0.514|1.016|22.00|
|lwma_rescue_floor1024|steady|1.004|0.993|19.25|
|lwma_rescue_floor1024|upx_offline|0.509|1.218|76.40|
|lwma_rescue_floor1024|turtle_offline|0.502|1.227|77.20|
|lwma_rescue_floor1024|upx_100x_drop|0.574|1.265|85.65|

## Timestamp stress

Full-branch strategy control, not an assertion a minority owns public timestamps. Score/sec expected~2in the arbitrary normalized units.

| Variant | Strategy | Rate / nominal | Normalized work/sec |
|---|---|---:|---:|
|lwma_plain_floor16|honest|0.991|1.987|
|lwma_plain_floor16|future|1.001|1.987|
|lwma_plain_floor16|minimum|0.147|2.104|
|lwma_plain_floor16|saw|0.756|1.994|
|lwma_rescue_floor16|honest|0.991|1.987|
|lwma_rescue_floor16|future|1.001|1.987|
|lwma_rescue_floor16|minimum|0.147|2.104|
|lwma_rescue_floor16|saw|0.756|1.994|
|lwma_plain_floor1024|honest|0.993|1.987|
|lwma_plain_floor1024|future|1.004|1.990|
|lwma_plain_floor1024|minimum|0.149|2.071|
|lwma_plain_floor1024|saw|0.757|1.996|
|lwma_rescue_floor1024|honest|0.993|1.987|
|lwma_rescue_floor1024|future|1.004|1.990|
|lwma_rescue_floor1024|minimum|0.149|2.071|
|lwma_rescue_floor1024|saw|0.757|1.996|

## Fork regression

These are adapted-model results, not Kerrigan security measurements: HMP seal-weighted selection, selective publication, receiver clock skew and network propagation are absent. Finite endpoint/transient lead counts are not a general double-spend probability. All raw per-seed trials retained in results.json.

| Variant | Strategy | Attacker fractions UPX,Turtle | Endpoint leads/50 | Transient leads after6publicblocks/50 |
|---|---|---|---:|---:|
|lwma_plain_floor16|honest|[0.1, 0.1]|0|0|
|lwma_plain_floor16|honest|[0.4, 0.4]|0|17|
|lwma_plain_floor16|honest|[0.8, 0]|0|18|
|lwma_plain_floor16|honest|[0, 0.8]|0|15|
|lwma_plain_floor16|future|[0.1, 0.1]|0|0|
|lwma_plain_floor16|future|[0.4, 0.4]|0|16|
|lwma_plain_floor16|future|[0.8, 0]|0|19|
|lwma_plain_floor16|future|[0, 0.8]|0|17|
|lwma_plain_floor16|minimum|[0.1, 0.1]|0|0|
|lwma_plain_floor16|minimum|[0.4, 0.4]|0|19|
|lwma_plain_floor16|minimum|[0.8, 0]|3|26|
|lwma_plain_floor16|minimum|[0, 0.8]|2|25|
|lwma_plain_floor16|saw|[0.1, 0.1]|0|0|
|lwma_plain_floor16|saw|[0.4, 0.4]|0|20|
|lwma_plain_floor16|saw|[0.8, 0]|0|20|
|lwma_plain_floor16|saw|[0, 0.8]|0|18|
|lwma_rescue_floor16|honest|[0.1, 0.1]|0|0|
|lwma_rescue_floor16|honest|[0.4, 0.4]|0|17|
|lwma_rescue_floor16|honest|[0.8, 0]|0|18|
|lwma_rescue_floor16|honest|[0, 0.8]|0|15|
|lwma_rescue_floor16|future|[0.1, 0.1]|0|0|
|lwma_rescue_floor16|future|[0.4, 0.4]|0|16|
|lwma_rescue_floor16|future|[0.8, 0]|0|19|
|lwma_rescue_floor16|future|[0, 0.8]|0|17|
|lwma_rescue_floor16|minimum|[0.1, 0.1]|0|0|
|lwma_rescue_floor16|minimum|[0.4, 0.4]|0|19|
|lwma_rescue_floor16|minimum|[0.8, 0]|3|27|
|lwma_rescue_floor16|minimum|[0, 0.8]|2|25|
|lwma_rescue_floor16|saw|[0.1, 0.1]|0|0|
|lwma_rescue_floor16|saw|[0.4, 0.4]|0|20|
|lwma_rescue_floor16|saw|[0.8, 0]|0|20|
|lwma_rescue_floor16|saw|[0, 0.8]|0|18|
|lwma_plain_floor1024|honest|[0.1, 0.1]|0|0|
|lwma_plain_floor1024|honest|[0.4, 0.4]|0|16|
|lwma_plain_floor1024|honest|[0.8, 0]|0|20|
|lwma_plain_floor1024|honest|[0, 0.8]|0|18|
|lwma_plain_floor1024|future|[0.1, 0.1]|0|0|
|lwma_plain_floor1024|future|[0.4, 0.4]|0|16|
|lwma_plain_floor1024|future|[0.8, 0]|0|19|
|lwma_plain_floor1024|future|[0, 0.8]|0|15|
|lwma_plain_floor1024|minimum|[0.1, 0.1]|0|0|
|lwma_plain_floor1024|minimum|[0.4, 0.4]|0|22|
|lwma_plain_floor1024|minimum|[0.8, 0]|4|28|
|lwma_plain_floor1024|minimum|[0, 0.8]|3|28|
|lwma_plain_floor1024|saw|[0.1, 0.1]|0|0|
|lwma_plain_floor1024|saw|[0.4, 0.4]|0|17|
|lwma_plain_floor1024|saw|[0.8, 0]|0|21|
|lwma_plain_floor1024|saw|[0, 0.8]|0|20|
|lwma_rescue_floor1024|honest|[0.1, 0.1]|0|0|
|lwma_rescue_floor1024|honest|[0.4, 0.4]|0|16|
|lwma_rescue_floor1024|honest|[0.8, 0]|0|20|
|lwma_rescue_floor1024|honest|[0, 0.8]|0|18|
|lwma_rescue_floor1024|future|[0.1, 0.1]|0|0|
|lwma_rescue_floor1024|future|[0.4, 0.4]|0|16|
|lwma_rescue_floor1024|future|[0.8, 0]|0|19|
|lwma_rescue_floor1024|future|[0, 0.8]|0|15|
|lwma_rescue_floor1024|minimum|[0.1, 0.1]|0|0|
|lwma_rescue_floor1024|minimum|[0.4, 0.4]|0|22|
|lwma_rescue_floor1024|minimum|[0.8, 0]|4|28|
|lwma_rescue_floor1024|minimum|[0, 0.8]|3|28|
|lwma_rescue_floor1024|saw|[0.1, 0.1]|0|0|
|lwma_rescue_floor1024|saw|[0.4, 0.4]|0|17|
|lwma_rescue_floor1024|saw|[0.8, 0]|0|21|
|lwma_rescue_floor1024|saw|[0, 0.8]|0|20|

## Comparison reference

Previous signed toy baseline: normal~0.998nominal, outage-return~31blocks/20T. Previous60work-window+dormancy-reset: normal~1.010, outage-return~20, but100×weakenedUPXfound~1block/200Tand barely adjusted difficulty. Those are separate measured simulation runs with same scenario/seeds, not native Kerrigan behavior.

No code was deployed or consensus changed. The supplied integer port is a research comparator, not a production library. Bounds/rounding/bootstrap source fidelity was checked for selected/generated histories; exhaustive correctness/security was not proven.

## Weak-lane recovery (same100×UPXloss scenario)

| Variant | UPXblocks over200T | End UPXdifficulty / pre-loss |
|---|---:|---:|
|lwma_plain_floor16|1.20|0.856|
|lwma_rescue_floor16|4.55|0.238|
|lwma_plain_floor1024|0.90|0.875|
|lwma_rescue_floor1024|12.95|0.055|

More weak-lane blocks does not imply full recovery to50%share, nor no outage-return burst. Floor choice is a consensus/security parameter, not a free optimization.
