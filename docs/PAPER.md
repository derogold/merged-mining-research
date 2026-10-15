# Shared work, distinct consensus: a DEGO research paper

## 1. Research question and boundaries

The initiating vision was: miner → CryptoNight tools abstraction → mining pool → independently valid blocks in several networks. The pool constructs commitments, schedules jobs, validates shares and submits candidates. Miners perform nonce searching. “Pool does no computation” is interpreted as no mining workload, not literally zero serialization, hashing or verification.

The desired outcome was more supported chains for the same hashing work, not a profitability forecast. Testing targeted Linux/x86 on Kobe. Historical OrangePi hash-rate recollections motivated the discussion but were not treated as measured results. No watt-hour measurements were collected.

Two research questions must remain separate:

- Can different chains accept a common proof carrier evaluated with the **same** hash function?
- Can related but different CryptoNight functions reuse enough computation to materially reduce paired cost?

A third question arose later: could DEGO accept either UPX2 or Turtle proof, while maintaining reasonable difficulty and branch-selection behaviour? That requires a new consensus design, rather than a pool adapter alone.

## 2. Source provenance and evidence hierarchy

Pinned core revisions include:

| Project | Revision |
|---|---|
| DEGO | `c502139f6ec02928c20dd2c8683c40daf97f352f` |
| Kryptokrona | `cf5a63e16b64200adb5445ea97d4186a0fdcb88a` |
| WRKZ | `364df861cdf6f1383a3240469a6fb0b85c72d579` |
| Fuego/XFG | `8a15ebaf8c9895da452d08ad71f0913e9810badd` |
| uPlexa/UPX | `78d16bad909c820c19765517fe57be61c6e1faaa` |
| Kerrigan | `7c4d3e5fa11525827f8152d168c6ca7a127e16bf` |

The experiment folders contain exact revision receipts and source anchors. Repository source at a pinned revision does not establish the version running on a public network.

We distinguish source inspection, modeled serialization, extracted native predicates, full daemon acceptance, replay/synchronization, and mature reward spending. Evidence at one level does not automatically advance to the next. Test counts refer to their actual units, not a single interchangeable “tests passed” score.

## 3. Same-algorithm quad candidate

The first study examined DEGO, WRKZ, XFG and UPX. On the tested Linux/x86 path, their native CN-UPX routines produced matching outputs when invoked with the correct project-specific parameter conventions. Evidence comprises 16 deterministic comparisons, four published WRKZ known-answer checks, four carrier-work fixtures and 93 structural checks: 117 focused checks, not 117 daemon acceptance tests.

The proposed carrier is an UPX-valid standalone block containing commitments to the other three chains. DEGO can lead product identity and pool accounting while UPX occupies the technical parent-proof role. These roles are not interchangeable.

A serialization mismatch matters: XFG's parent coinbase hash path differs from the UPX v2 null-RCT model. A v1 coinbase removes that mismatch in the source-derived model. Full unchanged-daemon acceptance remains unproven. Moreover, the inspected UPX wallet immediately skips incoming transactions with version ≤1. Discovering a valid reward therefore requires a narrowly scoped wallet change or another validated design. A scanner change alone is insufficient: maturity, legacy input bookkeeping, same-amount decoys, transaction acceptance, recipient receipt and subsequent spend must all pass.

Mac build paths disagreed between implementation pairs while Linux/x86 agreed against an independent known answer. That discrepancy is retained as platform/build evidence, not rewritten as a consensus mismatch. Linux is the intended deployment scope; successful Linux checks do not certify every compiler or CPU path.

## 4. DEGO and XKR: similar family, distinct work

The inspected DEGO v7 path uses CN-UPX variant 2; XKR v5 uses CN-Turtle-Lite-v2. Both share CryptoNight ancestry, but their parameters and transformations differ:

| Property | DEGO | XKR |
|---|---:|---:|
| Initialized scratchpad | 128 KiB | 256 KiB |
| Tested mixing address range | 128 KiB | 128 KiB |
| Iteration parameter | 32,768 | 131,072 |
| Actual main-loop iterations | 16,384 | 65,536 |
| Foldback extent | 128 KiB | 256 KiB |
| Variant-2 shuffle | UPX-specific ordering | ordinary ordering |

Allocated memory and randomly addressed memory are different quantities. XKR's upper scratchpad portion still participates in initialization/foldback even where the tested mixing path addresses only the lower half.

For identical input bytes, DEGO's initialized 128 KiB matched XKR's initial 128 KiB. Capturing the intermediate state and continuing initialization reproduced full XKR hashes on initial fixtures. This established a reusable computation, not a valid common network input or an economically useful optimization.

## 5. Common-envelope failure: identical auxiliary identities

Native genesis reconstruction produced the same DEGO/XKR genesis hash:

`7fb97df81221dd1366051b2d0bc7f49c66c22ac4431d879c895b06d66ef66f4c`

The shared `GENESIS_COINBASE_TX_HEX` is serialized coinbase transaction data, not itself a block hash. The native reconstruction and proof-path examination established the relevant full-block identity.

Both validators use genesis-derived bits to select an auxiliary Merkle path. Different candidate leaves therefore occupy the same slot in the ordinary shared tree. Increasing depth cannot create different selector bits. This is a collision in chain identity assignment, not a cryptographic hash collision.

Thirty paired fixtures covered depths 1, 2, 8, 16 and 32, both root-owner choices and three nonces. All paired native work serializations matched; the root owner passed the extracted proof predicate and the other chain failed. Sixty mutated-branch checks and sixty high-difficulty controls rejected. These were native serializers plus extracted proof predicates, not complete Core validation.

This superseded initial source-only optimism. Duplicate merge-mining tags were not adopted as a parser trick. No universal impossibility theorem was claimed, but no supported unchanged-consensus shared-tree solution was demonstrated.

The separate genesis audit found distinct DEGO/WRKZ/XFG selector identities for the quad route. WRKZ reconstruction matched its checkpoint; XFG/UPX reconstructed hashes remain provisional until independently confirmed by a native daemon/live node. Their relevant prefix divergence requires properly constructed branches, not arbitrary leaf-slot assignment.

## 6. Isolated consensus experiment and real nodes

Rather than change genesis, the DEGO lab introduced a height-gated auxiliary selector: zero-padded ASCII `DEGO-AUX-TESTNET-20261014`, 32 bytes, activated at height 7. Historical rules remained below activation. Early upgrades reached DEGO v7 at height 6. Difficulty was fixed at 100 to isolate proof/activation behaviour.

Three DEGO containers ran on an internal network with independent P2P/RPC ports and data directories. Premature new-selector proofs failed before activation; legacy proofs succeeded before it and failed afterward; new-selector proofs succeeded afterward. Replay/synchronization checked persistence of the fork boundary.

Three XKR nodes were then built on a separate private network, reaching Turtle v5 at height 6. XKR retained its genesis and auxiliary selector. Three paired rounds accepted DEGO heights 11–13 and XKR heights 7–9. Each pair committed both real candidate leaves in one parent envelope with a shared nonce, but evaluated both full PoWs separately. Corrupting a sibling preserved the work/PoW while causing rejection, isolating membership enforcement. All nodes agreed, and XKR restart/fresh-peer replay passed.

The fixture searched for a nonce satisfying both targets and short-circuited XKR work after a DEGO miss. That simplifies correctness testing; a production pool must also submit independently qualifying single-chain solutions. It is not a production scheduling policy or throughput benchmark.

Build failures were informative: a custom GCC11 `-O3` XKR crypto build failed an upstream known-answer assertion; `-O2` passed the suite with assertions enabled. The reported run restarted from fresh data after correction. UPnP was disabled in the isolated build after a header/library mismatch. These observations do not establish bugs in every deployed XKR binary.

## 7. Performance: what was saved, and what was not

### 7.1 Initialization reuse

Snapshot/reuse and direct prefix handoff preserved hash correctness, but measured paired CPU costs were about 1.07% and 1.14% worse respectively in their experiments. A shared computation can be too small, or impose enough overhead, to yield no net gain.

### 7.2 Profiling

Instrumented decomposition attributed roughly 94% of cost to mixing and 2.2% to initialization; the reusable portion represented roughly 0.7% of paired time. Instrumentation changes code generation, so these are diagnostic estimates. Perf follow-up showed approximately 24.5% fewer retired instructions but 2.94% more cycles for direct reuse, with higher generic cache-miss counts. This is not sufficient to infer DRAM bandwidth or energy use. The exact cause remained unresolved.

### 7.3 Specialized kernels and interleaving

Specialized helpers dramatically improved performance relative to the original harness. In one confirmation set, original execution took 34.6888 CPU seconds, specialized sequential execution 23.7668, and the best interleaving 25.0941. Interleaving lost to specialized sequential execution in all 12 confirmation blocks. The experiment included 1,792 paired correctness checks, 96 screening runs and 72 confirmation runs.

### 7.4 The crucial standalone control

Using the same specialized helpers in standalone implementations exposed the confound. Original execution took 34.1095 seconds; optimized standalone totals were 23.8613 (DEGO 4.3639 + XKR 19.4974); paired execution was 23.7451. The paired advantage was only about 0.4868%, despite consistent direction in 12 blocks.

Thus nearly all of the roughly 30% improvement was ordinary implementation optimization. This is not evidence that two algorithms cost one hash, nor a comparison against the best production miner. No energy-saving claim is supported.

## 8. Dual-PoW DEGO: acceptance is only the beginning

The research direction then changed: retain UPX2 and also accept Turtle proofs in DEGO. This could enable a genuine same-algorithm merged-mining route for each lane. It creates consensus questions about independent targets, sparse-lane recovery, rewards, timestamp rules and cross-lane branch weight.

Initial simulations used overall T=300 seconds, illustrative hash rates (3,1), and normalization weights (1/3,1). These are toy calibration parameters, not measured hardware/economic equivalences. A difficulty unit from one algorithm cannot simply be assumed to represent the same attacker cost as a unit from another.

Strict alternation stalls if a lane vanishes. Independent lanes preserve progress but may run at roughly half the full-network block rate with only one lane active. Parent-clock easing can recover dormant lanes but creates cheaper return work. Block-count chain selection was vulnerable in constructed already-eased states; reachability was not proven. Raw-work selection favoured the faster lane under the toy scaling. An attacker with 80% of that lane had 60% of raw work, so winning there was not a submajority attack against that metric.

Initial tests counted final private-branch leads only. Follow-up also counted any lead after six public post-fork blocks. That is a more revealing path statistic, but still not a general six-confirmation double-spend probability: publication strategy, propagation, honest switching and clock skew were not fully modeled.

## 9. Timestamp, estimator and dormancy experiments

Adversarial models separated wall time from header timestamps and applied a DEGO-like median-of-11 lower bound and 1,800-second future limit. Strategies included honest, minimum, future and alternating extremes. Signed, clipped and monotonic variants produced materially different calibration and branch behaviour. Clipping apparently awkward negative intervals is not automatically an improvement.

Rolling work/time estimators used 30/60 windows, including a finite-sample correction justified only for constant-difficulty independent exponential arrivals. The adaptive process is not covered by that derivation. Approximate steady calibration improved, while disappearance/return and sparse-lane behaviour still needed attention.

A dormancy reset after 30 other-lane blocks retained the old difficulty for the returning block, credited its actual work, reset history and held the difficulty for the first nine intervals. This controlled the studied return burst but stranded a lane after a 100× hash-rate drop: roughly one block over 200 target intervals, with most old difficulty retained. Preventing a cheap return and allowing weak-lane recovery are competing objectives.

The archived suites comprise 560 behaviour + 1,600 fork + 1,000 constructed-score trials initially; 240 behaviour + 240 stress + 2,400 fork trials in the adversarial follow-up; 400 + 400 + 4,000 for estimator comparisons; and 160 + 160 + 1,600 for dormancy follow-up. Counts describe model runs, not real blocks or independent production validations.

## 10. Kerrigan as an implementation reference

Kerrigan encodes X11, KawPoW and two Equihash variants. Its inspected design targets 120-second overall blocks and 480 seconds per algorithm. Each LWMA uses 60 same-algorithm intervals, linearly increasing weights, solve-time bounds [-5T,+6T], and a weighted-time floor k/20. It averages decoded targets rather than simply averaging difficulty. Integer operation ordering, compact encoding and 256-bit arithmetic are consensus-significant.

A separate rescue policy activates after a 40-block gap: the lane's target becomes 4× easier, with another factor of four per additional four chain blocks, bounded by an algorithm-specific easiest target. Other lanes therefore provide a recovery clock; if all lanes stop, that block-based clock also stops. Source specifies activation heights, but live activation was not verified.

The selected port matched nine upstream exact-output cases and 256 generated histories against a native C++ oracle containing the unchanged LWMA function body and original arithmetic implementation. This is stronger than a formula-level comparison, but is not the full upstream test suite or a full-node security audit.

The two-lane adaptation used overall T=300, lane T=600, rescue gap 20, subsequent rounds every two blocks, and arbitrary easiest-target caps of 16× or 1,024× initial target. It ran 320 behaviour, 320 timestamp-stress and 3,200 fork trials, plus 80 weak-lane replays. Plain LWMA was close to calibrated; rescue improved weak-lane recovery and changed return transients substantially.

Kerrigan's chain selection additionally prioritizes HMP seal-weighted work, with raw work secondary. Our fixed-weight simulation did not reproduce HMP. Difficulty findings must not be presented as validation or refutation of Kerrigan's full security model.

## 11. Correction to the evaluation criterion

On 15 October, Leo challenged the emphasis on block counts during the first 20 target intervals after return. That correction is adopted here. A burst or slow period is not by itself failure: difficulty estimates necessarily lag, and overshoot can produce compensating slow intervals. The configured target remains fixed; LWMA does not guarantee exact integral repayment of earlier excess production.

The relevant questions are convergence after hashpower settles, settling time, cumulative production deviation over the complete trajectory, damping versus persistent oscillation, and repeated hopping advantage per unit of hashing work. Longer-window aggregate rates exist in the archive, but a complete trajectory/settling analysis was not performed. Earlier labels based mainly on return-burst magnitude should not be read as final policy rankings.

A proposed real-daemon experiment retains one steady thread, adds seven threads, removes only the extra miner and observes recovery. Actual hashrate must be measured rather than assumed proportional to thread count. Repeated difficulty-triggered entry/exit should be compared against steady participation under matched work budgets. This test was discussed but **not launched**: the retained testnet still has fixed difficulty 100.

Inspection of DEGO's existing LWMA-2 showed per-block bounds near 0.67×/1.50× previous difficulty and an 8% minimum increase when the last three solve times sum to less than 0.8T. Candidate tuning should vary one lever at a time. The weighted-time denominator lacks an explicit local positive floor in the inspected function; caller invariants and reachable timestamp states require investigation before any vulnerability claim.

## 12. Conclusions and stopping point

The project produced real negative and positive evidence: a native common-tree incompatibility, a working isolated consensus workaround, six-node acceptance/replay, correct but marginal setup sharing, a benchmark confound caught by standalone controls, and reproducible multi-algorithm difficulty experiments.

It did not produce a production pool, a deployable dual-PoW fork, proof of energy savings, mature quad-mined payouts or a complete anti-hopping solution. Public miner identities were recognized as poor proxies for independent hashpower/control. Production adoption was not established, and dual-algorithm deployment was deliberately parked.

The surviving practical directions are (a) measured tightening of existing single-algorithm DEGO LWMA and (b) a DEGO-led same-UPX quad product with full acceptance and payout gates. The preserved lab remains available for curiosity-driven continuation. This is a research stopping point, not an instruction to retire the testnets.
