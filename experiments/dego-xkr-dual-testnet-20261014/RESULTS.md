# Results — 2026-10-14

## Real-daemon gate passed

- Three isolated XKR daemons built and run alongside three isolated DEGO daemons on Kobe.
- Fresh XKR chain mined h1–6 at difficulty100 using the bounded CLI miner. Actual header versions: 2,3,4,4,4,5. CN-Turtle-Lite-v2 from h6. Genesis and auxiliary-path identity unchanged.
- Three successive shared-parent rounds accepted on **both actual daemon RPCs**:
  - DEGO h11 / XKR h7
  - DEGO h12 / XKR h8
  - DEGO h13 / XKR h9
- Each pair uses real current templates, a real auxiliary leaf from each chain, one shared parent-work byte sequence and the same nonce. DEGO uses its new testnet selector; XKR uses the legacy genesis selector.
- Native serializers and native CachedBlock hashing independently reproduce both worker hash results.
- Before the first acceptance, corrupting the auxiliary sibling in each candidate leaves the parent work and valid PoW unchanged. Both daemons reject those candidates, with auxiliary-root errors in logs. Unmodified candidates are then accepted.
- All three nodes in each network agree on each accepted tip.
- XKR nodes restart with identical headers0–9; a fresh node3 synchronizes and validates the whole chain, including all three dual-commitment blocks.

## Precisely what this establishes
The height-gated DEGO identity change removes the common-tree slot collision in this laboratory setup. A single miner job can commit both real chains, execute the two algorithms and return solutions accepted by real validators on both networks. Pool-side orchestration need not perform nonce search.

The controller is a fixture, not a production Stratum pool. The worker computes complete DEGO and XKR hashes separately; shared initialization is not implemented here. It short-circuits XKR evaluation after a DEGO miss and searches for a nonce satisfying both targets, deliberately simplifying correctness testing. Production scheduling should also submit valid single-chain results. This experiment does **not** establish free second-coin hashing, energy savings, profitability, fork deployment safety or resilience to deep reorganizations.

## Build findings kept visible
The initial custom GCC11 -O3 crypto build failed the upstream CN-Lite-v1 known-answer assertion. Crypto rebuilt at -O2 passes the full upstream suite with assertions enabled. The initial chain was archived, then the reported experiment reran from fresh data on the corrected build. This establishes a compiler-setting sensitivity in this build; it is not proof every deployed XKR binary has the issue.

The bundled miniupnpc header/distro-library combination failed during UPnP startup. The research tree disables UPnP entirely, appropriate for private container-only networking. RocksDB wrapper RTTI and transitive linking were adapted to distro packages. Submission reporting and bounded miner lifecycle fixes are in patch_xkr.py. XKR's auxiliary consensus verification was not changed.

## Evidence
- evidence/dual-results.json: templates, both leaves, work blobs, worker receipts, candidate blobs, RPC replies and all node tips for each round.
- evidence/replay-results.json: all XKR headers before/after restart and fresh peer sync.
- evidence/xkr-initial.jsonl: CLI block submissions1–6.
- evidence/cryptotest-o2.log: successful full suite. cryptotest.log retains the failed initial build for comparison.
- evidence/data/node1/daemon.log and evidence/dego-daemon.log: real validation paths and rejections.
- source-changes.patch, scripts, package inventory and binary hashes: build/reproduction provenance.

## What remains running
Six isolated daemons, two separate internal Docker networks, no published XKR ports or external peer connections. DEGO tip13, XKR tip9. All miners/workers exited. No automatic restart policy. Data retained under `/tmp/dego-aux-testnet-20261014/` and `/tmp/dego-xkr-dual-testnet-20261014/` on Kobe, including archived failed-attempt data.

Next: implement shared-initialization in the worker against this working validation harness, measure the extra work honestly, and then map jobs/continuations onto a pool protocol. Keep nonce search in workers.
