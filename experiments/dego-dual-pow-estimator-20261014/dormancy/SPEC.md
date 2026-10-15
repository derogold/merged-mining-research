# Follow-up candidate, specified AFTER initial rolling-estimator results

The initial30/60work-window models calibrated normally but worsened outage-return bursts. New hypothesis: distinguish absence from a slow solve using OTHER-LANE BLOCK PROGRESS, not a clipped timestamp interval.

Use60interval estimator. If parent chain contains at least30blocks since this lane's last accepted block (all necessarily other-lane), declare lane dormant for this transition. Validate returned block at previously stored difficulty. Credit that actual work. Keep the same difficulty after it and reset the estimator window at its timestamp/cumulative work. Subsequent first9intervals retain that difficulty; resume ordinary estimator at10intervals. Threshold30chosen as a research parameter, not optimized from a threshold search.

Test with/without same-lane monotonic timestamps using EXACT previous scenario/seed/strategy grid. Two modes =>160behaviour,160stress,1600pairedfork trials. Report lack of down-adjustment for genuinely weakened/sparse lanes; do not call liveness of the remaining lane recovery of the absent lane. This is a NEW explicit inactivity consensus policy, not an estimator-only optimization. No daemon change.
