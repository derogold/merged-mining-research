# DEGO × XKR common-envelope gate: blocked by shared auxiliary identity

2026-10-14. Linux x86_64 / GCC 12.5.0. No live mining, wallet operations, daemon changes or service changes.

## Result

**The ordinary shared-commitment-tree design fails its compatibility gate on the pinned sources.** Both chains use the same genesis hash to select their auxiliary Merkle path:

`7fb97df81221dd1366051b2d0bc7f49c66c22ac4431d879c895b06d66ef66f4c`

Their different candidate headers produce different auxiliary leaves, but the path selector is identical at every bit. They therefore claim the same tree slot. A root constructed for one candidate fails the other's membership check.

This corrects the earlier source-only optimism: having similar parent-proof machinery was necessary but not sufficient. The previous scratchpad experiment was explicitly conditional on identical work inputs. It does not establish a work input acceptable to both networks.

## Evidence and scope

Sources remain DEGO `c502139f6ec02928c20dd2c8683c40daf97f352f` and XKR `cf5a63e16b64200adb5445ea97d4186a0fdcb88a`.

The harness compiles the repositories' actual CachedBlock, binary input/output serializers, transaction-extra parsers, target comparator and hashing implementations. It reconstructs native genesis from each configured coinbase, version 1, timestamp zero and nonce 70, matching each Currency::generateGenesisBlock path. DEGO's height-zero checkpoint independently matches the resulting hash. Both source configurations contain the identical genesis coinbase bytes.

The harness extracts each source's **checkProofOfWorkV2 function body** into a standalone wrapper, removing only logger statements and supplying its native genesis CachedBlock. It does NOT construct the full Currency object or invoke Core/blockchain validation. The generated C++ files are included for inspection. This distinction matters: these are serializer and extracted native proof-predicate tests, not accepted blocks.

Fixtures use modern outer versions (DEGO 7, XKR 5), synthetic transactions, a fixed synthetic timestamp and difficulty 1 to isolate membership checking. Their coinbases are not certified valid rewards. Passing this predicate would not prove block acceptance or spendability.

### Results: 30 paired envelope cases

Five branch depths (1, 2, 8, 16, 32), two choices of root owner, three nonces (0, 1, 12345).

- 30/30 paired native work serializations are byte-identical.
- 30/30 root-owner proof predicates accept at diagnostic difficulty 1.
- 30/30 other-chain proof predicates reject at the same difficulty.
- All 60 mutated-branch checks reject.
- All 60 maximum-uint64-difficulty controls reject for these fixtures.
- All 60 parent-proof serializations are below the 2048-byte cap.
- The two full PoWs are computed independently; this is not a reused-hash shortcut.

Exact work bytes, PoW hashes, roots, siblings, depths, lengths and predicate outcomes: `envelope-results.json`.

The same genesis path prevents assigning these distinct leaves to separate slots in an ordinary common tree. A deeper tree does not introduce differing selector bits. Different-depth or adversarial serialization constructions were not exhaustively explored; this is not a universal impossibility theorem. No deployable alternative common envelope is established.

## Why two merge-mining tags do not solve the normal case

Both inspected `getMergeMiningTagFromExtra` implementations parse the extra and use `findTransactionExtraFieldByType`; both parsers track duplicate merge-mining tags. There is no chain-specific tag selection in this path. We did not build a parser-differential exploit or treat malformed inputs as a supported protocol design.

## Implications for the pool-directed architecture

The user's boundary remains: the pool builds/schedules/verifies/submits; miners perform all nonce searching. The primary target is Kobe, not an OrangePi requirement, and economic profitability is outside scope. Energy savings need measurements, not a process-count claim.

Three honest routes remain:

1. **Unchanged chains, distinct envelopes:** one connection and pool-directed DEGO/XKR jobs, with independent inputs and computation. This provides coordinated mining but does not inherit the demonstrated same-input 128 KiB reuse. It must not be marketed as having that saving.
2. **Explicit auxiliary identity separation:** research an upgrade in which at least one chain uses a chain-specific, domain-separated auxiliary path identifier rather than the shared genesis hash. This would change consensus acceptance and needs deliberate coordination. Do not change either chain's actual genesis block. New and old proof rules need an activation/compatibility design. This may remove the membership blocker; it does not itself prove miner efficiency or full block acceptance.
3. **Another partner:** assess a chain with a distinct existing auxiliary path identity if unchanged consensus and same-envelope sharing are both firm requirements. Its PoW and serializer compatibility still need their own tests.

Recommended next research: a narrowly scoped, explicitly hypothetical chain-identifier experiment, alongside documenting the zero-consensus-change dual-job fallback. Do not launch a production pool from the existing positive hash tests.

## Worker work: prepared, not validated

`build_fused.py` successfully built separate native capture/reuse libraries on Kobe. `worker.py` is an **unexecuted prototype scaffold** for JSON-lines job plans, miner-only searching, a bounded eight-entry scratchpad cache, cache-miss/regeneration responses and retirement. No correctness/performance/protocol claims are made for it. The common-envelope gate failed before worker benchmarking or coordinator integration; those stages were intentionally not advanced as a deployable shared-work design.

The previous initialization-reuse results still stand for their same-input fixtures. No new paired-hash rate, speedup, energy saving or accepted-block result was measured in this pilot.

## Reproduction

1. Clone the exact source revisions into `/tmp/dego-xkr-research-dego` and `/tmp/dego-xkr-research-xkr`.
2. Run `probe.py` from the earlier `dego-xkr-20261014` bundle under `/tmp/dego-xkr-probe` to create known-answer-checked full hash shared libraries.
3. Install/use a Linux C++17 compiler and Boost headers. Source trees provide nlohmann-json and rapidjson. The build script uses XKR's bundled rapidjson for both and enables the projects' `RAPIDJSON_HAS_STDSTRING` option; no installed services are modified.
4. In this pilot folder, run `python3 build_native.py`, then `python3 test_envelopes.py`. On Kobe, use tmux.
5. Expected result: 30 paired envelopes, owner passes, other chain rejects, mutation and high-difficulty controls reject.

`build_fused.py` and `worker.py` are preparatory only. Generated executables and libraries remain in isolated `/tmp` directories on Kobe. This bundle contains sources and evidence, not executable binaries.

## Source anchors

- DEGO `src/config/CryptoNoteCheckpoints.h:32`, `src/config/CryptoNoteConfig.h` genesis coinbase; `src/cryptonotecore/Currency.cpp:553` proof predicate; `src/common/TransactionExtra.cpp:243` tag selection.
- XKR `src/config/cryptonote_config.h:103`; `src/cryptonote_core/currency.cpp:721` proof predicate; `src/cryptonote_core/transaction_extra.cpp:236` tag selection.
- Both `src/crypto/tree-hash.c`, `tree_hash_from_branch`: path bits come from the supplied genesis hash.
