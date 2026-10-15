# DEGO dual-PoW exploratory model — frozen before measurement

Objective: one DEGO history accepts explicitly tagged UPX2 or Turtle PoW, retaining separate proof validation and auxiliary commitments. This is a consensus-policy simulation, NOT a daemon or cryptographic implementation.

DEGO pinned config uses current target300seconds; use T=300. Placeholder baseline hash rates H=(3,1), not measured security or energy conversion. These units are deliberately arbitrary. PoW arrivals are independent exponential races with rate H_i/D_i; target modeled as expected hashes. All miners follow the simulated branch unless in the separate fork model.

Policies:
1. Alternating: required lane alternates; only its hashpower progresses the chain. Initial D_i=H_i*T. Per-lane retarget based on observed inter-lane-block time2T.
2. Independent/event: either lane can win. Initial D_i=H_i*2T. After a lane wins, its next difficulty multiplies by 2^((2T - actual lane interval)/(20T)), with each update clamped[1/4,4]. Other lane unchanged. This deliberately simple log feedback is NOT DEGO's production DAA.
3. Parent-clock: either lane; D_i=D0_i*2^((n_i*2T-parent_elapsed)/(20T)), recomputed from parent state, not prospective child time. Global lower floorD0/1024. Tests decay of an absent lane; not production ASERT.
4. Parent-clock capped: same, but next difficulty cannot be below1/4 of that lane's last accepted difficulty. Tests whether a seemingly sensible per-block cap suffices on return.

All policies floor difficulty at initialD/1024. Honest timestamps equal event time. Hashpower changes occur at deterministic boundaries; races resample at boundaries by exponential memorylessness. Parent-time-based difficulty stays constant between block events. Baseline stage200T, disturbance200T, recovery400T. Twenty fixed seeds per policy/scenario.

Scenarios: unchanged; UPX absent; Turtle absent; UPX drops100x; Turtle increases10x; miners switch normalized capacity between lanes (UPX0.1x,Turtle1.9x, then reverse in recovery); all miners absent (liveness control). Report per-stage blocks/time and lane share, gaps, short-gap counts, re-entry delay. No energy model.

Fork tests, separately: compare block-count, raw-difficulty and fixed-normalization chain scores for independently sampled competing branches. Normalize with fixed coefficients1/Hbaseline solely as a protocol thought experiment. No dynamic hardware-price oracle. Demonstrate score dependence on algorithm units and Poisson variance, NOT universal economic equivalence or a security proof. Include a low-difficulty block-count attack and unit-rescaling invariance control. These finite-horizon races start at a common ancestor and omit networking/selfish mining/timestamp manipulation.

Before real-daemon consensus code: an explicit chain-work formula, timestamp rules, difficulty initialization/rounding/overflow, outage recovery and adversarial reorg model must be agreed and validated. A successful honest simulation alone does not satisfy this gate. Do not silently deploy or hardfork mainnet.
