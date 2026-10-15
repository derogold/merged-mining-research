# Equivalent standalone controls — DEGO × XKR

Goal: distinguish ordinary native implementation improvements from a genuine paired-mining benefit. Research-only CPU benchmark; no consensus change, daemon changes or block submissions.

## Implementation

`pair.c` retains the previous native paired kernel and adds `dego_single` and `xkr_single`, using exactly the same begin/mix/finish helpers and fixed algorithm parameters. Same compilation unit, GCC12.5 -O2 -g -fPIC -Wl,-Bsymbolic -maes -msse2. Same per-hash aligned allocation/free policy; paired execution holds both buffers concurrently, standalone frees each independently. Both algorithms execute all iterations and full independent initialization/finalization. No cross-coin work reuse implemented.

## Comparators

- Original independent libraries (reference control, not best available miner).
- Restructured paired kernel, sequential mixing, chunk0.
- Equivalent optimized standalone DEGO batch plus XKR batch; sum their measured CPU time. Repacking output for correctness is outside timed region. Both DEGO-first and XKR-first orders occur once per balanced block.

Native batch loops avoid per-nonce Python overhead. Standalone has two batch calls versus paired's one; at512hashes/batch this is a small boundary difference, not silently removed. Allocator lifetime/cache state can differ legitimately between standalone and paired schedules.

## Protocol

Three real accepted-parent work blobs; four palindromic six-run blocks per blob; each comparator twice/block; positions rotate.512paired nonces/run,64warmup per mode/blob.72 timed comparator runs,24 per mode. Same input and nonce ranges within each block; all output bytes match original independent algorithms. Pinned CPU2, SMT sibling unreserved, existing host services/governor unchanged. No energy/power measurement.

Separate correctness:64varied input lengths against independent algorithms;3real blobs×64nonces,paired and standalone in both ordering settings. Initial run stopped before a completed timing block due to duplicate Python digest keyword in logging; fixed and restarted all measurements, no failed-run timings retained.

## Reproduce

Requires previous pinned lab sources and shared-init harness on Kobe under /tmp. Copy this directory there, run `python3 build.py`, then `python3 run.py`. Source paths are explicit. No dependencies or miner deployment changed.

Source revisions: DEGO `c502139f6ec02928c20dd2c8683c40daf97f352f`, XKR `cf5a63e16b64200adb5445ea97d4186a0fdcb88a`; research patches described in prior lab artifacts. Reproduction depends on those lab directories, not just clean upstream clones. Native controls are not full production miners. Faster/slower schedule results must not be equated with skipping consensus-required computation.
