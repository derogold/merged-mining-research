# DEGO-led four-coin research — 2026-10-11

## Verdict
A shared UPX-valid work carrier with a v1 coinbase is a plausible compatibility route for DEGO/WRKZ/XFG/UPX. Native x86 PoW and Merkle primitives support the idea. Full block acceptance, payout spendability, and actual deployed-network version matching are NOT proven. No consensus changes or live service modifications were made.

DEGO remains the user-required lead coin. A valid UPX work carrier technically occupies the parent-proof role, even if DEGO controls pool identity and accounting. Do not silently equate these roles or assume Leo approved a protocol-role change.

## Evidence
Pinned core/library commits: `revisions.json`.

- 16/16 deterministic input comparisons: all four original x86 CN-UPX routines match, with each coin's actual parameter convention.
- 4/4 published WRKZ CN_UPX known-answer comparisons pass (one per native implementation).
- 4/4 modeled carrier-work fixtures (1/2/3/7 transactions) produce equal native PoW across all four implementations.
- 93/93 structure checks: native fast-hash known answer, 2/3/4-leaf tree branch reconstruction and mutated-leaf/branch rejection, plus explicitly source-derived coinbase and work-serialization models. These are not 93 full consensus tests.
- Total 117 passing focused checks on x86. See `x86/*.json`.

Compiled unmodified source files into isolated shared libraries on local Mac and Kobe /tmp/quad-research-20261011. Added only build/test harnesses; no daemon source edits. Kobe jobs ran in tmux. No blockchain data, wallets, Docker services or public repos touched.

## Platform scope
Leo confirmed Linux is the deployment target. macOS support is out of scope unless explicitly reopened. Preserve Mac observations as historical evidence, not release blockers. The tested x86/Linux build passed; other compiler versions, optimization levels and CPU paths have not been certified by that result.

## Important failed/preliminary tests
Mac selected build paths yielded DEGO/WRKZ matching each other, UPX/XFG matching each other, but pairs differed on all 16 inputs. On x86 all four matched, including a published independent expected hash. The Mac discrepancy is unresolved build-path/architecture evidence, not proof of different network algorithms. DEGO's unmodified NO_AES portable source also failed compilation due to array/bitmask expressions. The successful Mac DEGO build used its ARM implementation. Initial x86 WRKZ link needed the repository's slow-hash-state.cpp, then passed. Do not use the preliminary Mac outputs to claim chain incompatibility.

## Per-chain review
### DEGO
- `CachedBlock.cpp`: modern block PoW hashes embedded parent work; auxiliary header separately committed.
- `Core.cpp` around 2311: parent major-version <=1 rule applies specifically to outer block version 2, not universally to later blocks. Parent proof limit 2048 bytes.
- `common/CryptoNoteTools.h:81`: BaseTransaction version >=2 uses prefix hash + Keccak(00) + null hash, then Keccak; compatible with UPX's null-RCT coinbase model.
- `serialization/CryptoNoteSerialization.cpp:223`: special BaseTransaction serializer, unlike ordinary transaction serializer.

### WRKZ
- Same relevant modern parent-proof and special coinbase-hash machinery.
- Core parent proof size limit 2048 bytes; version restriction similarly conditional on outer v2.
- Current hash implementation validated against its published CN_UPX test vector.

### UPX
- `cryptonote_format_utils.cpp:1362`: own header + transaction tree root + transaction count are work bytes; no embedded parent proof in block type.
- `cryptonote_tx_utils.cpp:257`: template builder uses coinbase v2 for mainnet HF12.
- `blockchain.cpp:86`: inspected mainnet schedule ends at HF12; HF13 entry commented out. This is a source snapshot, not a live-network status check.
- `cryptonote_basic.h:179`: transaction prefix reader accepts v1 (subject to other validation).
- `blockchain.cpp:1130`: coinbase prevalidation checks single generation input, height, unlock time and overflow, without an explicit v2 requirement.
- Main-chain acceptance calls this separately from ordinary transaction input checks. Coinbase reward validation and hooks must still pass. Utility-node hook returns early below HF13.
- v1 wallet/DB code paths exist; neither their existence nor source inspection proves payment spendability today.

### Fuego
- Currency validator reconstructs auxiliary root through genesis-hash-directed branch.
- Parent header layout matches broad work layout. Parent proof size <=2048 bytes; v1 parent-version restriction only applies to outer v2 blocks in inspected check.
- Parent coinbase hashed as serialized Transaction. This differs from UPX v2 null-RCT transaction hashing.
- v1 coinbase removes that particular mismatch in our source-derived model. No claim of full Fuego block acceptance.

## Candidate design and unresolved gates
1. Construct valid UPX header/coinbase with a commitment to DEGO/WRKZ/XFG. Use a valid v1 coinbase only if unchanged UPX acceptance and wallet spendability are demonstrated.
2. Reconstruct exactly that work for all three auxiliary validators; respect common timestamp constraints, per-chain outer versions and 2 KB proof limits.
3. New utility must replace current pinned helper's unconditional parent-version <=1 parser restriction; it cannot override daemon consensus.
4. Immutable job snapshots must preserve coinbase, roots and branches; regeneration on chain changes, stale handling and per-chain target rules remain pool work.
5. Necessary next gate is controlled unchanged-daemon acceptance at relevant hard-fork state and legitimate reward outputs. No weakened validation, fake acceptance or genesis-only tests advertised as current-mainnet proof.
6. Test the selected Linux production/miner compiler, optimization flags and CPU paths against known-answer vectors and representative work blobs. Mac agreement is not an acceptance gate. The Mac discrepancy has not been causally linked to earlier GCC incidents.

## Reproduction
`build_hashes.py` uses source snapshots under /tmp on Mac; `build_hashes_x86.py` uses extracted repos beside the script on Kobe. Crypto sources compile without semantic patches. `test_pow.py`, `test_structures.py`, `test_cross_work.py` write receipts. Source-derived serializers are clearly marked; they do not call full C++ block serializers or daemons.

## Decision
Technically credible candidate, not production-ready or consensus-acceptance-proven. Previous blanket dismissal of a utility-layer solution was unsupported. Conversely, successful shared hashes are insufficient to promise reliable four-chain mining.

## UPX pool-wallet inspection follow-up
Source remains UPX 78d16bad909c820c19765517fe57be61c6e1faaa.

**Concrete scan blocker found:** wallet2.cpp:1421 immediately returns from process_new_transaction for tx.version <= 1. Earlier broad claims about scanner capability omitted this entry guard. Legacy accounting below it exists but is unreachable for these incoming transactions in the current code.

A proposed minimal patch must admit specifically valid v1 coinbase transactions (or deliberately restore wider v1 history scanning), without accepting invalid version zero. No patch made. Use full coinbase refresh, not no-coinbase; rescan historical reward heights using existing rescan_blockchain functionality. Do not mistake rescan_spent for discovering outputs.

Existing downstream support:
- wallet2.cpp:1643 and 1765: v2 coinbase becomes m_rct=true; visible v1 output falls through to m_rct=false with identity mask. Keep the true output type; do not relabel v1 as RingCT.
- wallet2.cpp:5214: unlock checking uses transaction unlock time and minimum age.
- wallet2.cpp:8593: create_transactions_2 chooses RingCT based on fork rules. At 8671, RingCT mode permits both legacy and RingCT input types. 7759 records src.rct from actual transfer type.
- cryptonote_tx_utils.cpp:503: ordinary construction selects tx.version = rct ? 2 : 1 absent per-output-unlock mode. At 883 only RingCT inputs get amount zeroed; at 887 output amounts zeroed for RCT. Evidence for legacy-to-modern spending plumbing, not full accepted spend proof.
- wallet_rpc_server.cpp:878: transfer_split uses create_transactions_2 and can return do_not_relay transaction data. Existing rescan_blockchain/store/rescan_spent endpoints available.
- wallet2 get_outs uses actual visible amount for non-RCT input buckets (e.g. 7394), and fails on insufficient outputs. Core blockchain.cpp:2658 enforces ten decoys from HF_VERSION_MIN_MIXIN_10=8. Same-amount legacy decoy availability is a real spending constraint; denomination planning belongs in coinbase construction, not a scanner flag.

Leo reports Bob22 has modified dvandal tooling with UPX parent and says v1 accepted but wallet scanning requires a patch. This is user-relayed external evidence, not our daemon proof.

Pool-wallet proposed shape: narrowly patched existing wallet2 + wallet RPC, enabled full reward scan, truthful legacy input bookkeeping, normal fork-aware transaction construction, existing RPC payouts plus pool-side reliable payment ledger. Rebuild/rescan, persistence/reorg, mature input selection, unchanged-daemon acceptance, recipient stock-wallet receipt and spend tests are needed. No new wallet cryptography or second wallet required by the inspected architecture. Exact Bob22 patch not obtained.
