from sim import *
d=json.loads((P/'results.json').read_text());rows=d['rows'];f=json.loads((P/'forks.json').read_text())
s='''# Dual-PoW DEGO: exploratory findings

## Verdict

Independent UPX2/Turtle lanes are a credible design direction, with significant policy decisions still open. Strict alternation fails the desired outage-liveness property. Parent-clock difficulty decay produces recovery bursts; the tested cap does not cure them. The per-lane event-update model is the most promising **research baseline**, not a validated consensus DAA.

560 behaviour runs (4policies ×7scenarios ×20seeds),1,600 paired fork trials (4policies ×4hashpower splits ×100seeds), plus1,000 constructed scoring trials;9model checks passed. All simulation work completed. **No daemon, testnet chain or mainnet consensus changed.**

## Outage and return

Rate=1 means target300seconds/block. Each outage lasts200T, preceded by200Tbaseline, followed by400Trecovery. “First20T” is the first100minutes after miners return; nominal expectation20blocks. Values are20seed means.

| Policy | UPX outage rate | Turtle outage rate | UPX return first20T blocks | Turtle return first20T blocks |
|---|---:|---:|---:|---:|
'''
for policy in POLICIES:
 vals=[]
 for scenario in ['upx_offline','turtle_offline']:
  r=[a for a in rows if a['policy']==policy and a['scenario']==scenario]
  vals.append((statistics.mean(a['stages'][1]['rate_vs_nominal'] for a in r),statistics.mean(a['first_20T_recovery_blocks'] for a in r)))
 s+=f'|{policy}|{vals[0][0]:.3f}|{vals[1][0]:.3f}|{vals[0][1]:.1f}|{vals[1][1]:.1f}|\n'
s+='''
The independent policy preserves liveness at roughly half throughput when one lane vanishes. That is a deliberate consequence of target2T/lane, not a bug to hide. It still exhibits a moderate return burst, so recovery needs work. Parent-clock policies accumulate an issuance backlog for the absent lane: around111blocks instead of20in the first100minutes. A per-accepted-block cap can be traversed quickly through multiple blocks and does not prevent the aggregate burst.

## Hashpower shocks and switching

| Policy | Scenario | Disturbance rate | Recovery rate |
|---|---|---:|---:|
'''
for policy in POLICIES:
 for scenario in ['upx_100x_drop','turtle_10x_surge','switch_capacity']:
  r=[a for a in rows if a['policy']==policy and a['scenario']==scenario]
  s+=f'|{policy}|{scenario}|{statistics.mean(a["stages"][1]["rate_vs_nominal"] for a in r):.3f}|{statistics.mean(a["stages"][2]["rate_vs_nominal"] for a in r):.3f}|\n'
s+='''
## Fork scoring

Two distinct exercises must not be conflated:

1. **Constructed low-difficulty branches:** a weak miner is *given* an already-eased target. Block-count scoring chooses its branch500/500trials. Work-based scoring does not. This is a counterexample to treating blocks as equal work, NOT evidence that an attacker can reach that target under DEGO rules.
2. **Actual modeled retarget branches:** honest/private branches start from identical200Twarm-up histories, split hashpower, and follow the selected policy with honest timestamps for600T. These test the model's own targets and common ancestor; no artificial target injection.

With baseline rates(3,1), an attacker controlling80% of UPX and0% of Turtle has40% of *assumed normalized* capacity but60% of raw expected work rate. Under independent policy, raw-work scoring favours its private branch100/100trials, fixed-normalized scoring0/100. This is not a paradox or proof of a submajority attack against raw scoring: **the attacker is a majority under the raw metric**. It illustrates that choosing weights chooses the security balance. The Turtle-only mirror does not receive the same raw advantage.

Fixed coefficients(1/3,1) make the model invariant when UPX hash/difficulty units are rescaled together. They do NOT establish actual economic/energy equivalence, cannot be inferred from the simulator, and are not a production recommendation. Difficulty-adjusting targets cannot themselves serve as a continually changing normalization denominator without a new security analysis.

No normalized-score attacker was ahead at the finite horizon in these tested splits. This is NOT a security proof or a measured zero reorg probability: attacks are limited, timestamps honest, propagation instantaneous, and only endpoint lead is counted. An attacker could temporarily lead earlier; that was not measured. No network partitions, selfish mining, timestamp manipulation, release strategy or adversarial calibration changes modeled.

## Recommended specification direction

- Explicit, commitment-bound lane tag; select exactly one algorithm and expected target before verifying a proof.
- Separate lane difficulty histories; retain existing auxiliary-ID distinction and actual native PoW validators.
- Permit either lane to extend the same chain. Research baseline accepts half-rate operation if one lane disappears; preserving full rate would require a separately tested rule.
- Accumulate expected work with explicit, fixed protocol lane coefficients; do not use longest chain by block count or blindly add incomparable scores while claiming equal security contribution.
- Do not allow unbounded difficulty catch-up for an idle lane. Re-entry behavior and timestamp policy need an explicit design and adversarial tests.

## Why no daemon patch yet

There is an honest-liveness survivor, but no fully specified consensus survivor. The lane weights, inactivity/re-entry rule, timestamp bounds, exact integer difficulty/chain-work arithmetic, activation/migration handling, and adversarial reorg criteria remain unresolved. Implementing arbitrary defaults now would bake policy choices into a daemon and falsely elevate this toy simulation into validation.

Next experiment: a timestamp-aware, common-ancestor fork simulator for the independent-lane design, comparing explicit re-entry rules and fixed-weight sensitivity. Parameterize weights rather than silently treating the3:1model calibration as reality. Then build an isolated dual-lane daemon once those rules are concrete. Mainnet changes remain out of scope.
'''
(P/'RESULTS.md').write_text(s)
