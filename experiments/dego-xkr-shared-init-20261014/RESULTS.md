# Shared initialization: correct, but no net CPU saving on Kobe

## Finding
The common initialization prefix can be reused without changing either PoW result. Two implementations were tested. **Neither beats independent hashing on this host.** This is a negative performance result, not a failure of the shared-parent consensus construction.

Hardware: AMD Ryzen9 5900X, Linux x86-64 AES-NI, native libraries compiled with GCC12.5 -O2. One worker pinned to logical CPU2; SMT sibling14 was not reserved. Governor remained schedutil; other services remained running. No power measurement or all-core test.

## Candidate A: intermediate snapshot
DEGO saves128KiB to an extra thread-local buffer; XKR copies it into its own scratchpad and continues expansion. Two copies, one extra128KiB buffer.

84matched comparisons across3real parent blobs,7repetitions and4preplanned schedules. Each mode evaluates the same nonces and algorithms; native loops are timed. All outputs match byte-for-byte.

| XKR evaluation schedule | Change in CPU time versus independent hashes |
|---|---:|
| Every nonce | **+1.07%** |
| Every second nonce | +0.39% |
| Every fourth nonce | +0.67% |
| Every eighth nonce | +0.31% |

Positive numbers here mean **slower**, not savings. Original summary.json uses the opposite sign for its explicitly named saving metric. These are aggregate paired times, not selected best samples.

Dense timings exhibited a strong order effect: median saving was -2.95% with baseline first and +0.88% with candidate first. Therefore the follow-up used balanced four-run blocks. Small sparse differences should not be overinterpreted; empirical intervals and all raw measurements are retained.

## Candidate B: direct scratchpad handoff
DEGO copies the pristine prefix directly into XKR's own scratchpad before DEGO mixing. Removes the intermediate buffer and one copy.

Follow-up defined before its timings:3blobs ×4balanced ABBA/BAAB blocks ×1024nonces per run;48timed runs, two per mode per block. Dense schedule only.

- Independent hashing:68.7036 thread-CPU seconds across the measured work.
- Direct handoff:69.4893 thread-CPU seconds.
- **CPU time increased1.14%; throughput decreased about1.13%.**
- All12balanced blocks were slower; block regressions ranged1.01–1.28%.
- Wall-time change agrees:approximately+1.14%.

Do not rank the tiny difference between A and B: their measurement protocols differ. Both separately fail to demonstrate savings against their own equivalent-work baseline.

## Correctness
Both candidates passed known-answer hashes,256varied input pairs, real-work batches over3blobs and4schedules, and512pairs across4threads with explicit yields between producer/consumer. Shared state is per-thread; no prefixes move over the network.

Native baseline and candidate output arrays match throughout every timed comparison. No shortcut replaces or skips either algorithm's required mixing/finalization. XKR still initializes the remaining128KiB and performs its own mixing.

Candidate A also produced three block pairs accepted by full daemons: DEGOh14–16 / XKRh10–12. Native adapters independently reproduced worker hashes; corrupted-sibling candidates with unchanged valid PoW were rejected; all three nodes per network agreed. Candidate B passed the same real-daemon gate for three more pairs: DEGO h17–19 / XKR h13–15, including native hash reproduction, corrupted-sibling rejection and three-node agreement on each network.

## Interpretation / next step
The shared computation exists, but these implementations spend more total CPU time than they save. We have not isolated whether copying, cache behavior, call boundaries or changed code layout dominates; timing alone cannot attribute the cause.

Do not ship either as a performance optimization or market this as greener mining. Retain the real-daemon harness and profile initialization, memory traffic and divergent mixing before another implementation. The pool can still orchestrate the two branches; all nonce search remains in workers. A production pool protocol, energy savings, alternative CPUs and all-core throughput remain unproven.


## Retained state
Six isolated daemons remain running, DEGO tip19 and XKR tip15. All miners and benchmark workers have exited. Both earlier testnet directories and this experiment remain under /tmp on Kobe; the accompanying archive preserves scripts, measurements and receipts. No mainnet changes or unattended work are pending.
