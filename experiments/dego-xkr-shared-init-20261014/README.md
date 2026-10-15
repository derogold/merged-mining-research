# DEGO × XKR shared-initialization experiment

## Question
Does reusing the common first128KiB scratchpad initialization reduce CPU time when computing CN-UPX and CN-Turtle-Lite-v2 for the same parent-work bytes, while retaining exact hashes and actual daemon acceptance?

## Candidate (frozen before timing)
- DEGO computes its ordinary128KiB initialized scratchpad, copies the pristine prefix into thread-local storage, then runs its own mixing/finalization unchanged.
- XKR copies that saved prefix to its own scratchpad, seeds its initialization text from the last128-byte block and continues expansion from initialization round1024 to2048. XKR's different mixing/finalization remains unchanged.
- Snapshot stays in the worker, never sent to the controller. It must belong to the exact same input/nonce and thread. This harness invokes the two branches immediately in sequence; it is not an asynchronous cache/continuation implementation.
- This simple candidate uses two128KiB copies and one extra128KiB TLS buffer per thread. No attempt is made to share divergent mixing or final hashes.
- Tested x86-64 AES-NI hardware branch only. Do not advertise portable ARM or software-AES optimization from this experiment.

## Fair comparator
Baseline and candidate use the same pinned DEGO/XKR sources, GCC -O2, AES-NI flags and -Bsymbolic symbol binding. Baseline computes the two ordinary hashes separately. Native C loops eliminate per-nonce Python/FFI calls from timing. Returned output arrays are compared byte-for-byte outside the timed sections.

All workloads evaluate DEGO on every nonce; XKR on every1st/2nd/4th/8th nonce, known upfront. On DEGO-only nonces both modes use the ordinary DEGO function, avoiding pointless snapshots. This is a pool-directed branch-plan model, not the earlier success-conditioned dual-target worker. Do not compare their elapsed times as equivalent workloads.

## Correctness gates
Known-answer hashes;256 deterministic varied inputs;3 real parent blobs ×4 schedules ×512nonces;4 threads ×128pairs with explicit yielding between producer/consumer to test TLS isolation. CPU benchmarking starts only after all pass. Live optimized-worker blocks must be independently hashed by native template adapters and accepted by both full daemons.

## Benchmark protocol
Three real parent-work blobs from the earlier accepted dual-chain rounds. CPU affinity2 if available, otherwise first allowed CPU. Same process;256nonce warm-up per mode per blob. Seven paired repetitions per blob and scheduling ratio,2048DEGO nonces per repetition. Alternating baseline/candidate order.84matched pairs total; record thread CPU time, wall time, output digest, all per-trial values. No tuning based on measured outcomes; no changing CPU governor or stopping other services.

This is single-worker CPU efficiency on this host, not package energy, all-core capacity, pool profitability or a mainnet-security claim. CPU governor/turbo and other host activity can affect results; report the distribution, not just the best run.

## Layout
- build_baselines.py / build_fused.py: pinned-source native libraries, independent and snapshot-reuse versions.
- batch.c / harness.py: timed native batches and reference wrappers.
- check_correctness.py / benchmark.py: assertions and predeclared measurement protocol.
- shared_worker.py: bounded immediate-pair miner, all nonce search here.
- run_shared_live.py: template orchestration, native verification and submission. No nonce loops in the controller.
- Evidence and RESULTS.md are populated after execution.

## Reproduce
Use the three sibling research directories in this archive. Build/run the DEGO lab first, then the dual-testnet lab, then run `./prepare.sh` here on Kobe-like Linux x86-64 with GCC and Docker. The previous stage produces live daemons and dual-results.json. The benchmark itself performs no submissions; live submission runs afterward. Source/image dependencies and their limits are documented in the earlier directories.

Baseline/shared libraries are built with the same host compiler. On the measured host that is GCC12.5; daemon binaries use their recorded Docker toolchain. Native daemon hashing provides the independent check for live solutions. `environment.json` records governor and SMT sibling placement. No host power readings were taken.

The scripts assume the supported hardcoded CN-UPX/CN-Turtle parameter pair. They are laboratory code, not safe generic plugin entry points for arbitrary algorithms, inputs from untrusted clients, stale prefix caches or other platforms.

`summary.json` retains an empirical95% paired-resampling interval, stratified by input blob. This describes these repeated runs; it does not justify generalizing to other CPUs, all-core saturation or electricity use.

## Focused follow-up: direct handoff
The initial snapshot variant showed no aggregate CPU saving and a strong run-order effect. A second candidate, defined after that result, removes the intermediate128KiB TLS snapshot and one copy: DEGO calls xkr_accept_prefix to copy its pristine prefix directly into XKR's own thread-local scratchpad, then continues independently. XKR resumes initialization from that stored prefix. -Bsymbolic keeps the two libraries' internal scratchpads separate.

The direct candidate repeats the same correctness gates. Its focused dense-pair benchmark uses3blobs ×4balanced ABBA/BAAB blocks,1024nonces per timed run, two runs of each mode per block;12blocks/48timed runs total. This protocol was set before collecting its timings, specifically to address the order effect seen in the first run. It is not pooled with the earlier84comparisons. Sparse direct-handoff schedules, all-core scaling and power remain unmeasured.

The live tests of each candidate use three rounds of actual daemon acceptance, with native output checks and corrupted-branch controls. They run outside timing windows.
