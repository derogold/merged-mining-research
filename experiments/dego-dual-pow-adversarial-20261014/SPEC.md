# Timestamp-aware dual-PoW simulation: pre-run specification

Research model, not daemon consensus. Reuse T300s, baseline H=(3,1), fixed W=(1/3,1), initial D=(1800,600). Weights arbitrary. Candidate current-height timestamp bounds from pinned DEGO: timestamp >= median of previous11blocks (inclusive), timestamp <= validation wall clock+1800s. Real code also has historical activation/sync-floor exceptions; they are not modeled. Honest miner template chooses max(wall,median), matching inspected logic.

Two clocks: actual discovery time and integer header timestamp. Difficulty of a candidate is fixed by parent state; accepted timestamp affects NEXT difficulty of its lane. Expected arrival rate H/D. No target chosen using the child timestamp. Header choices are modeled adaptively at discovery, approximating miners updating timestamp templates continuously, not post-hash header mutation in an implementation.

DAA candidates:
- signed: prior event-update rule, Dnext=max(D0/1024,D*2^clip((600-delta)/6000,-2,2)). Delta is signed header difference from previous same-lane block.
- clipped: same but delta first clipped[0,1200]. Limits one long outage's difficulty cut, but discards negative timestamp differences.
- monotonic_clipped: clipped plus header >= previous same-lane timestamp. Equality allowed; no forced1second progress. This is a NEW proposed validation constraint, not existing DEGO consensus.

Strategies on the attacker's branch: honest; maximum permitted future timestamp; minimum permitted median timestamp; alternate future/minimum. All constrained by candidate timestamp rules. No claim these are optimal strategies. Difficulty floors/float arithmetic retained; exact integer production rules remain open.

Tests:
1. Honest outage/re-entry and100xhashdrop:200Twarm-up,200Tdisturbance,400Trecovery,20seeds per DAA/scenario.
2. Whole-branch timestamp stress: warm-up then600Tusing each strategy,20seeds. This is a hostile-clock stress control, not an assertion a minority miner owns all public blocks.
3. Common-ancestor forks: shared200Thonest warm-up; honest capacity remainder, attacker fractions(.1,.1),(.4,.4),(.8,0),(0,.8). Independent random streams thereafter.600Thorizon,50seeds per DAA/strategy/split =2400pairedtrials. Score fixed-normalized expected work. Count endpoint lead AND any lead after public branch has at least6post-fork blocks; no publication, propagation, honest switch or subsequent adaptive strategy modeled.

Guardrails: invalid past/future stamps rejected; target derived from parent before hash arrival; current block score uses its pre-update difficulty; same prefix state for forks; no work gained from merely advancing timestamps. Steady calibration and deterministic replay controls. No power/security proof, no mainnet/daemon changes.
