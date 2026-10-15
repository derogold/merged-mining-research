# Rolling work estimator — pre-run specification

Compare signed event-update baseline against lane-local rolling30 and60interval work/time estimators, each with and without proposed same-lane monotonic timestamps. Retain prior wall/header separation, median11/future1800s validation, fixed weights and probabilistic PoW model. No selective-publication or receiver-clock-skew extension in this estimator pass; previous fork metrics retained as regression controls.

For each lane store accepted(timestamp,cumulative actual difficulty). For last n intervals, nextD=max(initialD/1024,600 * deltaWork / max(1,deltaTimestamp) * (n-1)/n). First9intervals retain starting difficulty. No per-solve-time clipping; no upper/lower per-block adjustment cap. Thirty/60interval windows, actual history, no synthetic past blocks.

The (n-1)/n factor corrects the inverse-gamma time-denominator bias ONLY for constant difficulty with independent exponential arrivals. Adaptive work and timestamps violate that simple proof; empirical calibration is mandatory, not presumed. The max1second denominator handles nonpositive spans explicitly but can create huge targets under hostile timestamps—measure rather than hide it.

Use same240-style scenario structure per rule:4behaviour scenarios×20seeds;4timestamp strategies×20seeds;4hash splits×4strategies×50seeds. Five rules =>400behaviour,400stress,4000paired fork trials. Baseline200T,disturbance200T,recovery400T. Report whether60block window fills during warm-up as a limitation if not. Current score uses mined difficulty, never next difficulty.

Predeclared assessment: honest steady rate within±5%nominal desirable; outage first20Treturn ideally<=25blocks on average;100xdrop must preserve other-lane liveness; timestamp stress must not create major rate distortion. These are exploratory design targets, not proof or production release gates. No daemon or mainnet changes. Failure is an acceptable research outcome.
