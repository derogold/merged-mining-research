# Kerrigan source review — relevance to DEGO dual-PoW

Pinned upstream https://github.com/kerrigan-network/kerrigan commit7c4d3e5fa11525827f8152d168c6ca7a127e16bf. Read-only source review; no upstream binary or tests executed. Live chain tip and deployed activation NOT verified.

## Findings

- Four algorithms explicitly encoded in block version: X11, KawPoW, Equihash200,9 and Equihash192,7 (src/primitives/block.h). This is multi-algorithm acceptance, not computation of four algorithms for one hash.
- Overall120s target, per-algorithm480s target. Source mainnet activation of LWMA at151000; rearm at148000. Height-gated behavior must be preserved when reproducing it; presence on main is not proof of live activation.
- Prior Hivemind DAA used global40block timing and per-algo rebalance. Source documents contamination from burst/abandon hopping and unwanted survivor-lane tightening; LWMA removes both. These are upstream explanations, not independently reproduced incident findings.
- Current LwmaPerAlgo uses60same-algo intervals, recent intervals linearly weighted; solve times clipped[-5T,+6T], weighted sum floored at k/20; average compact-decoded target multiplied by weighted time/k, with integer predivision/overflow precautions. This is NOT our rolling sum-work/sum-time estimator and NOT the naïve [0,4T]clipped feedback model we rejected. They should be compared faithfully, not conflated.
- Bounded history scan (61*4*8=1952chainblocks). Fewer than2same-algo blocks falls back to effective easiest target. Long-absence fallback remains a distinct edge to test.
- After40other-chain blocks since last algorithm block, rearm path eases its last target4×, then another4× per additional4chainblocks, bounded by algorithm-specific effective easiest target. This is target multiplication/difficulty reduction. It is an explicit recovery policy; unlike our reset, it does not keep old difficulty forever.
- Per-algo hardware-calibrated minimum difficulties (maximum targets) limit how easy rescue can become. Porting arbitrary floors to DEGO without calibration would not preserve behavior.
- GetBlockProof uses ordinary inverse target. nChainWork accumulates it without the fixed cross-algorithm normalization used in our toy model. Primary comparator uses nChainSealWork, weighted by HMP seal multiplier; raw nChainWork is secondary. Do NOT describe Kerrigan as simply our fixed-weight model or assume DAA alone captures its security architecture. HMP introduces cryptographic participation/privilege/seal machinery outside this review's audit scope.
- pow_tests.cpp contains golden LWMA vectors, clamps/floors/overflow/activation checks, stranded-algo reset and hopper-defense cases. Tests were inspected, not run. Upstream comments claim cross-checks against independent reference/scenarios; not independently confirmed here.

## Recommended change of approach

Use pinned Kerrigan LWMA+rescue as a concrete external reference before inventing another estimator. First reproduce its integer outputs against its golden vectors, including pre/postactivation boundaries. Then parameterize a two-algo,300s-global/600s-lane adaptation and compare honest cadence, single-lane disappearance,100xloss,return burst,timestamp games and deliberate gap-triggering against our60window+dormancy candidate.

Do not blindly copy40blocks/4blockround/algorithm floors or HMP. Keep original four-algo oracle separate from adapted DEGO experiments. No assertion Kerrigan solved all attacks; code and tests are a better starting point than marketing, not a security certificate.

## Key pinned references

- https://github.com/kerrigan-network/kerrigan/blob/7c4d3e5fa11525827f8152d168c6ca7a127e16bf/src/pow.cpp
- https://github.com/kerrigan-network/kerrigan/blob/7c4d3e5fa11525827f8152d168c6ca7a127e16bf/src/chainparams.cpp
- https://github.com/kerrigan-network/kerrigan/blob/7c4d3e5fa11525827f8152d168c6ca7a127e16bf/src/node/blockstorage.cpp
- https://github.com/kerrigan-network/kerrigan/blob/7c4d3e5fa11525827f8152d168c6ca7a127e16bf/src/test/pow_tests.cpp
