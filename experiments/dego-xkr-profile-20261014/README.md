# DEGO / XKR phase profiling — 2026-10-14

Scope: CPU-only AES-NI on Kobe Ryzen 9 5900X, logical CPU 2, GCC 12.5 -O2. No mainnet, consensus, daemon, governor or kernel-policy changes. No energy measurements.

## Method

Instrument the existing pinned baseline and direct-handoff sources at five phase boundaries with CLOCK_THREAD_CPUTIME_ID. Three actual shared-parent work blobs, four ABBA/BAAB blocks per blob, 256 paired nonces per run. Every measured output is checked against the uninstrumented independent baseline. Warm up each instrumented run with 32 pairs. Phase totals include timer/instrumentation overhead; fine-grained setup/finalization figures should be interpreted cautiously. These profiles identify large cost centres, not a replacement for the earlier uninstrumented speed comparison.

Scripts use existing /tmp/dego-xkr-shared-init-20261014 and its two source sibling directories on Kobe. Run make-cn-profile.py, then run-cn-profile.py. The builder additionally emits unused snapshot artifacts; measurements cover baseline and direct-handoff only. Original sources and production binaries are not edited.

## Memory operations: static source accounting, NOT measured DRAM traffic

- Baseline initialization writes 128 KiB DEGO + 256 KiB XKR per paired nonce.
- Direct handoff avoids generating the first 128 KiB of XKR expansion, but copies 128 KiB from DEGO into XKR: same total scratchpad initialization writes, plus 128 KiB source reads. The gain sought is AES computation avoided, not fewer scratchpad writes.
- Folding reads the entire initialized scratchpad on each algorithm: 384 KiB combined, unchanged by handoff.
- Variant-2 mixing performs two random accesses per iteration, each with a 16-byte principal read/write plus three neighbouring 16-byte shuffle reads/writes. Source-level total: 256 bytes of scratchpad loads+stores per iteration; 16,384 DEGO and 65,536 XKR iterations => 4 MiB + 16 MiB per paired nonce. Repeated accesses/cache reuse/compiler transformations mean this is NOT external memory bandwidth.
- Mixing traverses different evolving states; no mixing reuse is implemented.

## Counter limitation

`perf` is absent; `/proc/sys/kernel/perf_event_paranoid` is 4. Hardware cache-miss, stall, and DRAM traffic measurements were not obtained. No attempt to relax host policy. Timings alone cannot distinguish bandwidth, cache latency, dependency chains or integer arithmetic as the cause of mixing cost.

No claim of energy saving, cache bottleneck, or two-coins-for-one-hash follows from this profile.

Allocation is retained exactly as implemented: setup includes allocation, finalization includes freeing. Direct handoff allocates XKR's buffer inside DEGO initialization; interpreting the paired totals avoids misattributing that transferred cost to DEGO's algorithm itself. Mixing phase includes the small register-state setup immediately before its loop. Fold phase includes key expansion for the fold.

## Follow-up: perf installed

After Leo's correction, installed kernel-matching linux-tools-5.15.0-198-generic with linux-tools-common, linux-tools-5.15.0-198 and hwdata (4 new packages, no upgrades/removals). perf reports version 5.15.216. Privileged per-process user-space counters work without changing perf_event_paranoid=4. The earlier counter limitation is therefore superseded for supported generic events. No manually requested service restart or kernel change.

Bounded follow-up: one real blob, 2048 pairs per process, baseline/direct/direct/baseline, original uninstrumented libraries, CPU2. Generic cycles, instructions, cache-references and cache-misses measured across the entire Python process, including startup. This is a diagnostic counter sample, not a replacement performance benchmark; generic cache events are architecture-dependent and do not establish DRAM bytes, bandwidth or precise cache level bottlenecks.
