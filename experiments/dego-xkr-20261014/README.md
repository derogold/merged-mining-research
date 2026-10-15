# DEGO × Kryptokrona: coordinated cross-algorithm mining

Research date: 2026-10-14. Scope: Linux source review and bounded native hash experiments; no production, wallet or consensus changes.

## Executive finding

The owner's vision—one miner, a CryptoNight-tools abstraction, one pool, independently qualifying blocks on DEGO and Kryptokrona—has a credible tooling-only research path. Both inspected chains already validate embedded parent-work envelopes with auxiliary Merkle commitments. They apply different PoW functions to that envelope. A shared envelope could therefore be evaluated with both algorithms, with each result checked against its own chain's target.

More importantly, a small experiment **demonstrates reusable initialization**: DEGO's initialized 128 KiB scratchpad is identical to the first 128 KiB initialized by Kryptokrona for the same input. Reusing that prefix, and continuing Kryptokrona initialization from its last 128-byte text block, reproduces Kryptokrona's original complete hash on 16 fixtures.

This is **not a complete fused miner**, block acceptance proof, profitability measurement, or one hash satisfying both algorithms. The strongest current description is **shared-envelope, dual-PoW mining with demonstrated partial setup reuse**. No consensus fork is established as necessary by this investigation.

## Pinned sources

- DEGO: https://github.com/derogold/derogold-core/tree/c502139f6ec02928c20dd2c8683c40daf97f352f
- Kryptokrona: https://github.com/kryptokrona/kryptokrona/tree/cf5a63e16b64200adb5445ea97d4186a0fdcb88a

These were repository HEADs fetched during this investigation. Deployed-node version/height has not been verified. The Kryptokrona website uses both Turtle and Pico terminology on different pages; consensus code is the basis of this analysis.

## Exact algorithm comparison

| Property | DEGO block version 7 | Kryptokrona block version 5 |
|---|---|---|
| Wrapper | `cn_upx` | `cn_turtle_lite_slow_hash_v2` |
| Variant | 2 | 2 |
| `light` argument | 2, special UPX behavior | 1 |
| Allocated/initialized scratchpad | 131072 bytes | 262144 bytes |
| Addressable main mixing region on tested x86 path | 131072 bytes | 131072 bytes |
| Iterations parameter | 32768 | 131072 |
| Actual loop iterations (`iterations/2`) | 16384 | 65536 |
| Main address mask | explicit `0x1fff0` | derived `0x1fff0` |
| Shuffle source offsets | first/third reversed for light==2 | ordinary variant-2 order |
| Foldback | 128 KiB | 256 KiB |

Kryptokrona's `lightFlag=2` halves the addressable region of its 256 KiB allocation. Its upper half is still initialized and participates in foldback. Do not equate allocated memory with random mixing address range.

The shuffle difference is decisive: DEGO reads chunk1 at offset XOR 0x30 and chunk3 at XOR 0x10; Kryptokrona reads them at XOR 0x10 and XOR 0x30 respectively. Both use XOR 0x20 for chunk2. Thus CN-UPX is not just a shorter prefix of Kryptokrona's loop. Our probes find different lower-region contents after the first complete hardware-AES mixing iteration on every tested input.

Relevant paths (relative to pinned repositories):
- DEGO `src/config/CryptoNoteConfig.h:311`, `src/crypto/hash.h:357`, `src/crypto/slow-hash-x86.c:78`, `src/crypto/slow-hash-common.h:118`.
- XKR `src/cryptonote_core/cached_block.cpp:58`, `src/crypto/hash.h:163`, `src/crypto/slow-hash.c:264`, `:706`, `:106`.

## What was actually tested

Native GCC 12.5.0, Linux x86_64, on Kobe; shared libraries built at `-O2 -maes -msse2`. Hardware AES path. Sixteen deterministic synthetic inputs, lengths 76–91 bytes. Inputs are hash fixtures, **not accepted block fixtures**.

| Check | Result |
|---|---|
| DEGO upstream CN-UPX known-answer vector | pass |
| XKR upstream Turtle-Lite-v2 known-answer vector | pass |
| Lower 128 KiB initialization digest equal | 16/16 |
| Lower 128 KiB digest after first mixing iteration equal | 0/16 |
| Complete original DEGO/XKR hashes equal | 0/16 |
| XKR with DEGO initialization prefix substituted equals original XKR | 16/16 |

`results.json` contains exact inputs, outputs, expected known answers and summaries. `probe.py` creates separate full and instrumented C copies, builds them and asserts the results. Full baseline routines are unmodified. Instrumented variants stop after initialization or the first mixing iteration and hash the lower 128 KiB. The reuse variant replaces the first 1024 initialization rounds with the DEGO-produced snapshot, resumes from the saved tail text, and completes the normal XKR algorithm.

This bounded experiment validates the mechanism on these fixtures; it does not certify all inputs, compilers or CPU paths. It also does not prove speedup. Python/ctypes copying, extra snapshot calls and early-return instrumentation are research plumbing, not production optimization. No timing or watts claim is derived from this harness.

## Proposed work-envelope architecture

1. Obtain immutable DEGO and XKR templates, keeping each chain's coinbase, reward, difficulty, parent tip, transaction set and version separate.
2. Compute each auxiliary header hash and a common auxiliary commitment tree. Construct branches using each validator's genesis-hash-directed path convention, not arbitrary leaf order. Handle path-prefix collisions correctly.
3. Put the common root into a parent-envelope coinbase merge-mining tag. The inspected parent serializers have the same field sequence: major/minor version, timestamp, previous hash, nonce, parent transaction root, count. Both use matching v1/v2 parent coinbase hash constructions in the inspected helpers.
4. Give the miner a shared work blob/nonce space plus two algorithm and target descriptors.
5. Initialize common state and scratchpad prefix once; preserve an immutable copy before either mixing loop writes to it. Continue XKR expansion and run two private mixing/foldback paths.
6. Return tagged results; the pool independently recomputes the correct PoW and checks each target. A DEGO solution does not imply an XKR solution. Do not compute/check XKR only on DEGO-winning nonces unless intentionally accepting the resulting lost XKR opportunities.
7. Build the appropriate outer block and auxiliary proof for each qualifying chain and submit independently. An update to either template changes the shared commitment, so keep old job snapshots and per-chain stale policy.

### Why a common envelope is credible

Both `CachedBlock` implementations select parent hashing bytes for modern blocks. Both `Currency::checkProofOfWorkV2` implementations check that chain's own long hash and reconstruct the merge-mining commitment using its genesis hash. Both enforce a 2048-byte parent proof cap in core validation. The inspected functions do not require a live external parent-chain confirmation.

A neutral/synthetic work envelope is therefore a candidate; a separately operating third parent network is not established as a requirement. This remains a source-derived hypothesis until full serialization and daemon acceptance tests pass. It also does not make a DEGO-native outer block the literal parent proof. **DEGO-led pool/product identity and technical parent-proof identity must remain distinct**, per the owner's earlier requirement.

Sources: DEGO `src/CryptoNoteCore/CachedBlock.cpp:60`, `Currency.cpp:553`, `Core.cpp:2300`, `src/serialization/CryptoNoteSerialization.cpp:362`, `src/common/CryptoNoteTools.h:81`; XKR `src/cryptonote_core/cached_block.cpp:58`, `currency.cpp:721`, `core.cpp:2460`, `cryptonote_serialization.cpp:340`, `cryptonote_tools.h:145`.

## Cost, hardware and realistic upside

Independent initialization generates 128 + 256 = 384 KiB per paired nonce. Shared expansion could generate 256 KiB and copy/fork the shared 128 KiB state. That removes **one third of initialization expansion**, not one third of total mining cost. Both mixing loops, both foldbacks, output hashing and snapshot traffic remain. Shared Keccak/key expansion is another candidate not optimized or benchmarked here.

The mixed workload requires more live memory than DEGO alone. The prototype still allocates separate scratchpads and snapshots. On small SBCs, cache capacity and memory traffic could eliminate the saving or reduce DEGO throughput badly. Sequential reuse, per-core scheduling and CPU/GPU placement should be measured, not assumed.

No estimate of earnings, aggregate security, energy saving or speedup is justified yet. A dual-output nonce rate must not be compared directly with a single-algorithm hashrate. Report each chain's rate, accepted shares, wall power, temperature and rejected/stale work separately.

## Recommended next experiments, in order

1. **Common-envelope serializer proof:** construct one parent blob with two genesis-directed branches; use both native serializers and validators to reconstruct identical work bytes. Test mutated root, nonce, path, count and timestamp rejection. Respect 2 KiB cap. This is the key missing bridge from hash fixtures to actual jobs.
2. **Isolated current-rule acceptance:** feed candidate outer blocks through unchanged daemon validation with the relevant version schedules and legitimate reward outputs. Do not lower validation or use genesis-era results as current-network proof. Verify unlock, wallet scan and accepted reward spending. No live submission without separate authorization.
3. **In-process fused kernel:** reuse initial state/prefix without ctypes snapshots, compare every output against independent known-answer-backed implementations, then benchmark against an equally optimized independent pair.
4. **SBC gate:** x86 for development; a real ARM SBC for the product claim. Compare DEGO-only, independent dual mining, fused dual mining and scheduled mining at equal power/thermal conditions. Report DEGO throughput sacrificed per XKR throughput gained.
5. **Pool adapter:** only after acceptance and hardware evidence, implement per-algorithm share targets, immutable snapshots, chain-specific accounting/payouts, nonce allocation, reorg handling and bounded stale work.

### Decision

Proceed first with the **shared-envelope serializer/validator experiment**, not an immediate hard fork. The evidence is stronger than mere common ancestry: existing auxiliary-proof structures plus demonstrably reusable initialization. The unanswered question is whether this delivers accepted multi-chain jobs and worthwhile SBC economics.

Ryo/Conceal are outside this source/test slice. No generic CryptoNight-family compatibility claim follows from these two chains.
