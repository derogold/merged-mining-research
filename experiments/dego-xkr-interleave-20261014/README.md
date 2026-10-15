# DEGO × XKR interleaved-mixing experiment

Research-only native AES-NI variant-2 worker, 2026-10-14. No pool-side mining, network/consensus changes or mainnet submissions. It computes both complete PoWs; it does not make one hash satisfy both algorithms.

## Controls and scope

`pair.c` includes pinned DEGO crypto helpers and uses their light=2 shuffle for DEGO, light=1 shuffle for XKR. Independent original DEGO and XKR library outputs are the correctness oracles. It initializes separate scratchpads (no shared-initialization optimization), performs 16,384 DEGO and 65,536 XKR mixing iterations, and independently folds/finalizes both.

Three comparisons are distinct:

1. Original independent libraries, sequential execution.
2. Restructured fixed-variant pair implementation, sequential mixing (`chunk=0`).
3. Same restructured implementation, alternating `chunk` DEGO iterations and `4*chunk` XKR iterations. Chunks 1,4,16,64,256,1024.

Any improvement of (2) over (1) is code specialization/restructuring, NOT proof of interleaving benefit. The interleaving test is (3) versus (2). This is chunked scheduling in one native thread, not a hand-scheduled dual-lane assembly kernel. Compiler may spill context between chunks. No instruction-level overlap is guaranteed.

Allocation uses two aligned buffers per pair. No cross-algorithm scratchpad aliasing, no reuse of mutated state. x86/AES-NI only; no ARM or software-AES claims.

## Reproduction

On Kobe with the prior pinned labs available in /tmp:

- python3 build.py
- python3 check.py
- python3 benchmark.py

The source include path and harness dependencies are explicit in the scripts. Flags: GCC -O2 -g -fPIC -Wl,-Bsymbolic -maes -msse2. CPU affinity2, sibling not reserved. Existing services remain running.

`check.py`: 64 varied inputs across seven schedules, plus three real work blobs ×64 nonces ×seven schedules =1,792 paired hashes matching both original algorithms.

`benchmark.py`: exploratory screen across3blobs,4 rotated/reversed rounds,256 pairs/run; verifies all output arrays. Selection from this screen must be confirmed in fresh balanced measurements, not reported as an unbiased best-of-seven win.

## Assembly diagnosis

perf cycle sampling at499Hz, bounded2048 pairs per mode, uninstrumented original baseline/direct-handoff libraries. Baseline: XKR function75.79%, DEGO18.13% of samples. Direct: XKR78.45%, DEGO19.40%. Annotated hot regions include scratchpad accesses, stack spills/TLS lookup, and the dependent square-root/correction sequence. Sampling skid means a hot following instruction is not proof it causes the stall. Hot loops contain division and sqrt alongside memory operations; cache misses alone cannot explain performance.

The previously observed24.5% retired-instruction difference is not explained by these samples. The XKR mixing disassembly is substantially similar between baseline/direct. Treat the four-run counter observation as unresolved, not as a proven instruction-saving mechanism or causal cache result. Precise AMD event validation and repeated controlled counters remain future work.

## Fresh confirmation protocol

`confirm.py` selects the lowest aggregate CPU-time interleaving chunk from screening, then collects NEW timing samples: original libraries, same-code sequential control and selected interleaving schedule. Three real blobs ×four palindromic six-run blocks ×512 pairs/run =72 runs. Each mode occurs twice per block; positions rotate. All output bytes must match. No screen samples enter confirmation totals. This confirms one selected implementation on one host, not generality across platforms.

Known limitations: shared host, unreserved SMT sibling, no governor/frequency lock, no power measurement, no comparison with best available production miners, and no independently optimized single-coin control. Faster than these reference libraries is not synonymous with beating an optimized miner. New worker uses independent initialization, so any speedup cannot be credited to shared scratchpad initialization. No new blocks are mined/submitted during this experiment; correctness is against both pinned native implementations and previously accepted real parent-work blobs.
