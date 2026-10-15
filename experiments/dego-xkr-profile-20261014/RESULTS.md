# Results

48 instrumented runs, 12 balanced blocks, 3 real work blobs; every output matched the uninstrumented baseline. All profiling workers finished.

| Mode / coin | Setup µs | Initialization µs | Mixing µs | Fold µs | Finalize µs |
|---|---:|---:|---:|---:|---:|
| full / dego | 6.45 | 11.94 | 547.73 | 12.05 | 2.87 |
| full / xkr | 6.06 | 23.45 | 944.51 | 23.79 | 2.87 |
| direct / dego | 6.77 | 46.81 | 528.37 | 12.06 | 2.91 |
| direct / xkr | 1.74 | 11.89 | 1019.60 | 23.78 | 2.91 |

Baseline mixing share: **94.34%**. Baseline combined initialization: **2.24%**. Half of XKR initialization: **0.74%** of total paired time. This last number is a rough opportunity estimate, not a demonstrated saving or universal upper bound.

Direct mode reduces XKR initialization but adds handoff/allocation cost to DEGO initialization. Instrumented mixing times also shift despite unchanged mixing source. Timer calls alter code generation/register allocation and runtime conditions; no precise causal attribution of the earlier ~1.1% slowdown is supported. Prior uninstrumented balanced benchmarks remain the performance verdict.

**Recommendation:** initialization reuse is a small target here. Investigate mixing dependency/compute/cache behaviour with hardware counters when available, before changing it. Neither substantial work reuse nor energy savings is established. Source-level memory-operation accounting is in README; actual cache/DRAM traffic remains unmeasured. No new optimization was implemented.

## Hardware-counter follow-up

Four uninstrumented whole-process ABBA samples completed, matching output digests. Direct versus baseline mean counters: cycles:u: +2.94%, instructions:u: -24.49%, cache-references:u: +6.55%, cache-misses:u: +32.59%. No multiplexing reported. Baseline IPC ~1.36, direct ~1.00. Generic cache-miss ratios ~0.52–0.59% versus ~0.68–0.70%. These are architecture-dependent generic events, not DRAM bandwidth measurements. Fewer instructions did not translate to fewer cycles. Four runs cannot establish a causal cache explanation; sampling hot instructions and identifying AMD event semantics are needed before optimizing.
