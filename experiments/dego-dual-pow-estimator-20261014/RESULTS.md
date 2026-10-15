# Difficulty estimator results

## Verdict

The plain rolling-work estimator fixes the earlier clipping calibration bias, but worsens return bursts. An explicit **dormancy reset** is the first tested candidate that preserves approximately normal calibration AND removes the tested outage-return burst. It sacrifices fast difficulty recovery for sparse/weakened lanes. It is a research candidate, not approved daemon consensus.

Initial predeclared experiment:5rules,400behaviour,400stress,4000pairedfork trials. Follow-up specified after initial results:2dormancy rules,160behaviour,160stress,1600pairedfork trials. Nine initial harness checks and seven reset checks passed. Constant-difficulty bias-correction controls returned means0.9985/0.9987; that limited mathematical control does not prove adaptive estimator unbiasedness. All20warm-up seeds filled the selected30/60interval windows.

## Honest behavior

Rates relative to300s/block target;20seeds each. First20T is100minutes after disturbance ends, expected20blocks at nominal rate.

| Rule | Scenario | Disturbance rate | Recovery rate | First20T blocks |
|---|---|---:|---:|---:|
|signed|steady|1.004|0.997|18.75|
|signed|upx_offline|0.503|1.051|31.05|
|signed|turtle_offline|0.501|1.052|31.15|
|signed|upx_100x_drop|0.550|1.096|50.80|
|window30|steady|1.019|1.012|18.45|
|window30|upx_offline|0.509|1.081|45.75|
|window30|turtle_offline|0.508|1.078|45.05|
|window30|upx_100x_drop|0.517|1.081|45.90|
|window60|steady|1.017|1.007|20.30|
|window60|upx_offline|0.515|1.121|38.75|
|window60|turtle_offline|0.512|1.118|38.70|
|window60|upx_100x_drop|0.522|1.122|40.65|
|window30_monotonic|steady|1.019|1.012|18.45|
|window30_monotonic|upx_offline|0.509|1.081|45.75|
|window30_monotonic|turtle_offline|0.508|1.078|45.05|
|window30_monotonic|upx_100x_drop|0.517|1.081|45.90|
|window60_monotonic|steady|1.017|1.007|20.30|
|window60_monotonic|upx_offline|0.515|1.121|38.75|
|window60_monotonic|turtle_offline|0.512|1.118|38.70|
|window60_monotonic|upx_100x_drop|0.522|1.122|40.65|
|window60_reset|steady|1.017|1.007|20.30|
|window60_reset|upx_offline|0.515|1.013|20.05|
|window60_reset|turtle_offline|0.512|1.006|19.80|
|window60_reset|upx_100x_drop|0.520|1.037|21.60|
|window60_reset_monotonic|steady|1.017|1.007|20.30|
|window60_reset_monotonic|upx_offline|0.515|1.013|20.05|
|window60_reset_monotonic|turtle_offline|0.512|1.006|19.80|
|window60_reset_monotonic|upx_100x_drop|0.520|1.037|21.60|

Plain30/60windows returned roughly45/39blocks in the first20Tafter outage, versus31for the signed baseline. Reusing a long silent interval to estimate active hashpower causes underestimation on return; smoothing alone cannot tell whether hardware left or became slower.

## Dormancy rule and trade-off

After30other-lane blocks since the lane's last block, its next block is validated at the retained difficulty, credited that actual work, and its estimator window restarts at that accepted block. It does NOT get easier work merely because it was absent. First9new intervals retain difficulty;10intervals restart estimation. The threshold is proposed protocol state based on chain progress, not local wall-clock detection or a hidden pool decision.

With60interval window, return averages20.05blocks(UPXoutage),19.8(Turtleoutage), versus nominal20. Normal long stress rate1.010nominal; ordinary future/sawtooth strategies near1.02/1.006. Same-lane monotonic version gives similar honest results. This passes the stated honest calibration/re-entry goals in this sample.

Cost: during100×UPXhashpower reduction, UPXfound~1.05blocks over200T(16h40m) and retained~93%ofits prior difficulty on average. The surviving Turtle lane preserved roughly half-rate chain operation. This is **not successful difficulty recovery of the weak lane**. A genuine long-lived hashpower loss can leave that lane nearly unusable. Before choosing this design, decide whether that is acceptable or requires a separately specified slow recovery mechanism.

## Timestamp stress and forks

| Rule | Strategy | Rate / nominal |
|---|---|---:|
|signed|honest|0.998|
|signed|future|1.010|
|signed|minimum|0.145|
|signed|saw|0.998|
|window30|honest|1.018|
|window30|future|1.030|
|window30|minimum|0.087|
|window30|saw|0.993|
|window60|honest|1.010|
|window60|future|1.020|
|window60|minimum|0.173|
|window60|saw|1.006|
|window30_monotonic|honest|1.018|
|window30_monotonic|future|1.030|
|window30_monotonic|minimum|0.097|
|window30_monotonic|saw|1.022|
|window60_monotonic|honest|1.010|
|window60_monotonic|future|1.020|
|window60_monotonic|minimum|0.181|
|window60_monotonic|saw|1.017|
|window60_reset|honest|1.010|
|window60_reset|future|1.020|
|window60_reset|minimum|0.173|
|window60_reset|saw|1.006|
|window60_reset_monotonic|honest|1.010|
|window60_reset_monotonic|future|1.020|
|window60_reset_monotonic|minimum|0.181|
|window60_reset_monotonic|saw|1.017|

Minimum permitted timestamps still produce slow/high-difficulty/high-variance private branches (~0.17–0.18nominal for60window variants). Dormancy does not solve this. Whole-branch timestamp stress is not proof of public-chain minority control.

Fork regression uses previous model: common ancestor, fixed normalized weights, honest/private capacity split, endpoint and transient lead after6public blocks. In800mixed scenario trials per variant, endpoint private leads occurred6times for60window and6times for60window+reset;7times for corresponding monotonic variants. These aggregates mix strategies/hash splits and are **not security probabilities** or evidence of significant equivalence. Full per-scenario trials are retained. No selective publication, network reception or clock-skew model was added in this estimator-only pass.

## Decision / next boundary

Keep60window+dormancy reset as a candidate for further testing, not production code. Need threshold sensitivity and deliberate lane-starvation/reactivation strategies, prolonged hashpower loss, timestamp-aware selective publication/receiver clock skew, and exact integer/lane-tag/activation specification. Preserve fixed-normalized work accounting while examining weights explicitly; all weights remain arbitrary model calibration.

No daemon, testnet or mainnet consensus changed. No energy claim. This simulation does not make distinct PoWs identical; the target remains DEGO accepting either algorithm while one lane can share work with XKR.
