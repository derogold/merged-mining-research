# Results

{
  "selected_chunk": 1024,
  "sequential_vs_original_cpu_reduction_pct": 31.485731181107866,
  "interleave_vs_sequential_cpu_increase_pct": 5.584808500633609,
  "sequential_wins_vs_original": 12,
  "interleave_wins_vs_sequential": 0,
  "blocks": 12,
  "cpu_seconds": {
    "original": 34.688836423000026,
    "0": 23.766802637000005,
    "1024": 25.094133050999993
  }
}

All1,792 preliminary paired hashes and all timing-run output arrays matched both original native algorithms. Screen96runs; fresh confirmation72runs.

Interleaving failed to beat the restructured sequential control. Restructuring/specialization beat the original reference libraries on this host. This does not demonstrate cross-coin work reuse, energy savings, or competitiveness against optimized production miners. Both complete algorithms still execute.

Assembly sampling localized most cost to XKR mixing and showed dependent arithmetic/spill/load regions. It did not resolve the earlier retired-instruction discrepancy or prove a cache bottleneck.

The useful next control, if authorized, is separately optimized standalone DEGO and XKR workers versus this paired worker, with equivalent allocation and compiler settings. That separates ordinary per-algorithm improvements from genuine pairing advantage. No production rollout recommended from this experiment alone.
