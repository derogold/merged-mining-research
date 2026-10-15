# Decisions, corrections and resumable work

## Current disposition

- Keep isolated DEGO/XKR testnets intact for future experimentation.
- Park production dual-algorithm DEGO work. No adoption commitment or consensus deployment was established.
- Do not label coordinated two-algorithm hashing as same-work merged mining.
- Do not infer energy savings from instruction counts, process count or CPU-time alone.
- Preserve failed hypotheses and benchmark controls rather than polishing them out of the story.

## Methodological decisions

The pool owns templates, commitments, job state, verification, accounting and submission. Miners own nonce searching. Avoid turning an expensive server-side continuation into hidden pool mining.

Same algorithm means matching consensus computations and accepted carrier serialization, not merely matching CryptoNight marketing names. Count independent accepted blocks and spendable rewards separately from proof-predicate fixtures.

A fast return burst is an observation, not an automatic failure. Evaluate full trajectories and repeated exploitation. Difficulty remains a historical estimator; it cannot instantly distinguish a lucky sequence from new hashpower. Faster response trades estimation noise, overshoot and manipulation sensitivity against recovery time.

Pool worker identities/addresses are not independent miner counts. More reported identities need not improve decentralization. Adoption and independent control were not demonstrated by this research.

## Track A: incremental DEGO LWMA

Before any candidate tuning, restore real adjustment in a separate lab build. Existing retained nodes deliberately use difficulty 100.

Baseline experiment: one persistent thread, then seven additional threads, then withdrawal of those seven. Measure actual hashrate, blocks, timestamps, assigned difficulty, submission outcomes and miner attribution. Warm up the estimator and preserve the entire recovery. Repeat with fixed schedules and difficulty-triggered entry/exit. Do not assume 8 threads produce 8× hashrate.

Compare baseline with isolated changes to window length, fast-burst trigger/response and adjustment bounds. Freeze metrics before choosing a winner: hopper reward/work relative to matched steady work, steady-miner delays, settling, oscillations under constant hashpower, and integrated production deviation. Hold reward rules and test conditions explicit. Real 300-second-target tests take hours; accelerated tests debug mechanics but do not replace them.

Audit arithmetic and reachable timestamp bounds independently. No local-denominator observation alone establishes exploitability. Any consensus candidate needs activation, replay, malformed-input and reorg tests. None of this track's real-hashpower experiment has run yet.

## Track B: same-UPX quad product

1. Refresh deployed-version compatibility against pinned research assumptions.
2. Prove the carrier using unchanged daemon validation at relevant fork rules, with legitimate rewards.
3. Resolve v1 coinbase compatibility and narrowly scoped wallet scanning, preserving true legacy output types.
4. Prove maturity, decoy/input selection, accepted payout, stock recipient receipt and spending.
5. Build immutable multi-chain job snapshots and per-chain submission, target and stale handling.
6. Add payout reconciliation, reorg recovery and restart persistence before public operation.
7. Product remains DEGO-led; UPX parent-proof role is explicit rather than silently described as DEGO being protocol parent.

No production pool or wallet patch is delivered by this archive.

## Optional research return: dual PoW

Use the verified Kerrigan integer implementation as a reference, not its full consensus/security architecture. Evaluate independent lanes, bounded rescue, cross-lane work normalization and repeated rocking. HMP was not ported. Any rescue floor needs justified calibration; arbitrary 16×/1024× limits were sensitivity experiments. No obligation to continue this route exists merely because the testnets work.
