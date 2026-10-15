# DEGO merged-mining and multi-algorithm research

**Research notebook and technical evidence archive · 11–15 October 2026**

Research direction and experimental design: Leo Stehlik. Implementation, measurements and documentation assistance: Francis (AI agent). This is an engineering research record, not a peer-reviewed paper or an audited production release.

## Abstract

We investigated whether a DEGO-led pool could support multiple CryptoNight-family networks with one miner connection and, ideally, one hashing workload. We explored two distinct routes: same-algorithm DEGO/WRKZ/XFG/UPX merged mining, and cross-algorithm DEGO/Kryptokrona (XKR) coordination. Native primitives supported the first route but did not establish full block acceptance or reward spendability. The second exposed a shared-genesis auxiliary-path collision, which we resolved in an isolated, height-gated DEGO testnet. Six real daemons then accepted paired commitments, with two separate PoW computations. Shared scratchpad initialization was correct but did not deliver the hoped-for large computational saving. Controlled benchmarks attributed most subsequent speedup to ordinary implementation optimization.

We then studied DEGO accepting both UPX2 and Turtle PoW, using bounded simulations of difficulty, dormancy, timestamps and branch selection. An independent port of Kerrigan's per-algorithm LWMA matched selected upstream vectors and 256 native C++ oracle cases. No dual-algorithm production fork was implemented. A final methodological correction refocused evaluation from short-window block counts to adjustment response, steady-miner recovery and repeated hopping advantage.

**Current decision:** preserve the dual-algorithm route as research, without a production commitment. The practical follow-ups are incremental DEGO LWMA evaluation and a same-algorithm quad-mining acceptance/payout proof. Neither follow-up is completed here.

## Read this archive

- [Technical paper](docs/PAPER.md): architecture, methods, results, failures and limits.
- [Chronological experiment ledger](docs/EXPERIMENTS.md): all 15 evidence bundles and their entry points.
- [Claim/evidence matrix](docs/CLAIMS.md): exactly what has and has not been demonstrated.
- [Preserved testnets and reproduction](docs/REPRODUCTION.md): lab state, safety boundaries and dependencies.
- [Decisions and future experiments](docs/ROADMAP.md): where the research stopped and how to resume.
- [Evidence integrity manifest](evidence-manifest.json): SHA-256 and byte length for archived experiment files.
- [Verification tool](tools/verify_archive.py): validates evidence and local Markdown links.

The `experiments/` folders preserve original reports, source patches, harnesses, receipts, raw measurements and failure logs. Earlier reports are historical snapshots, **not silently revised to match later discoveries**. Read the paper and ledger before treating an earlier recommendation as the latest conclusion.

## Critical distinctions

1. One miner process is not one hashing workload.
2. One shared parent envelope is not one PoW when validators apply different algorithms.
3. Matching hash primitives is not full daemon acceptance.
4. Accepted testnet blocks are not proven mainnet compatibility or spendable rewards.
5. CPU-time improvement is not an energy measurement.
6. A simulated branch lead is not a general double-spend probability.
7. A transient production burst alone does not establish a bad difficulty adjustment.

## Scope and licensing

No mainnet consensus, real wallets or live pool service was changed by these experiments. The existing isolated lab nodes are retained; this publication does not restart, delete or migrate them. Current binaries/data are not bundled. Source provenance and deployment limitations are documented below.

Upstream code retains its original copyrights and licensing. This archive does not relicense copied code; see [licensing notes](docs/LICENSING.md). No blanket software license is asserted for the entire collection.
