import json,statistics as s
from pathlib import Path
p=Path(__file__).resolve().parent;initial=json.loads((p/'results.json').read_text());reset=json.loads((p/'dormancy/results.json').read_text());datasets=[initial,reset]
text='''# Difficulty estimator results

## Verdict

The plain rolling-work estimator fixes the earlier clipping calibration bias, but worsens return bursts. An explicit **dormancy reset** is the first tested candidate that preserves approximately normal calibration AND removes the tested outage-return burst. It sacrifices fast difficulty recovery for sparse/weakened lanes. It is a research candidate, not approved daemon consensus.

Initial predeclared experiment:5rules,400behaviour,400stress,4000pairedfork trials. Follow-up specified after initial results:2dormancy rules,160behaviour,160stress,1600pairedfork trials. Nine initial harness checks and seven reset checks passed. Constant-difficulty bias-correction controls returned means0.9985/0.9987; that limited mathematical control does not prove adaptive estimator unbiasedness. All20warm-up seeds filled the selected30/60interval windows.

## Honest behavior

Rates relative to300s/block target;20seeds each. First20T is100minutes after disturbance ends, expected20blocks at nominal rate.

| Rule | Scenario | Disturbance rate | Recovery rate | First20T blocks |
|---|---|---:|---:|---:|
'''
for d in datasets:
 for mode in dict.fromkeys(a['mode'] for a in d['behaviour']):
  for scenario in ['steady','upx_offline','turtle_offline','upx_100x_drop']:
   r=[a for a in d['behaviour'] if a['mode']==mode and a['scenario']==scenario]
   text+=f'|{mode}|{scenario}|{s.mean(a["during_rate"] for a in r):.3f}|{s.mean(a["recovery_rate"] for a in r):.3f}|{s.mean(a["first20T"] for a in r):.2f}|\n'
text+='''
Plain30/60windows returned roughly45/39blocks in the first20Tafter outage, versus31for the signed baseline. Reusing a long silent interval to estimate active hashpower causes underestimation on return; smoothing alone cannot tell whether hardware left or became slower.

## Dormancy rule and trade-off

After30other-lane blocks since the lane's last block, its next block is validated at the retained difficulty, credited that actual work, and its estimator window restarts at that accepted block. It does NOT get easier work merely because it was absent. First9new intervals retain difficulty;10intervals restart estimation. The threshold is proposed protocol state based on chain progress, not local wall-clock detection or a hidden pool decision.

With60interval window, return averages20.05blocks(UPXoutage),19.8(Turtleoutage), versus nominal20. Normal long stress rate1.010nominal; ordinary future/sawtooth strategies near1.02/1.006. Same-lane monotonic version gives similar honest results. This passes the stated honest calibration/re-entry goals in this sample.

Cost: during100×UPXhashpower reduction, UPXfound~1.05blocks over200T(16h40m) and retained~93%ofits prior difficulty on average. The surviving Turtle lane preserved roughly half-rate chain operation. This is **not successful difficulty recovery of the weak lane**. A genuine long-lived hashpower loss can leave that lane nearly unusable. Before choosing this design, decide whether that is acceptable or requires a separately specified slow recovery mechanism.

## Timestamp stress and forks

| Rule | Strategy | Rate / nominal |
|---|---|---:|
'''
for d in datasets:
 for mode in dict.fromkeys(a['mode'] for a in d['stress']):
  for strategy in ['honest','future','minimum','saw']:
   r=[a for a in d['stress'] if a['mode']==mode and a['strategy']==strategy];text+=f'|{mode}|{strategy}|{s.mean(a["rate"] for a in r):.3f}|\n'
text+='''
Minimum permitted timestamps still produce slow/high-difficulty/high-variance private branches (~0.17–0.18nominal for60window variants). Dormancy does not solve this. Whole-branch timestamp stress is not proof of public-chain minority control.

Fork regression uses previous model: common ancestor, fixed normalized weights, honest/private capacity split, endpoint and transient lead after6public blocks. In800mixed scenario trials per variant, endpoint private leads occurred6times for60window and6times for60window+reset;7times for corresponding monotonic variants. These aggregates mix strategies/hash splits and are **not security probabilities** or evidence of significant equivalence. Full per-scenario trials are retained. No selective publication, network reception or clock-skew model was added in this estimator-only pass.

## Decision / next boundary

Keep60window+dormancy reset as a candidate for further testing, not production code. Need threshold sensitivity and deliberate lane-starvation/reactivation strategies, prolonged hashpower loss, timestamp-aware selective publication/receiver clock skew, and exact integer/lane-tag/activation specification. Preserve fixed-normalized work accounting while examining weights explicitly; all weights remain arbitrary model calibration.

No daemon, testnet or mainnet consensus changed. No energy claim. This simulation does not make distinct PoWs identical; the target remains DEGO accepting either algorithm while one lane can share work with XKR.
'''
(p/'RESULTS.md').write_text(text)
