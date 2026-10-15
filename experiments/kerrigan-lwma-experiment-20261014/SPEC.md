# Kerrigan LWMA oracle and two-lane adaptation

Pinned source7c4d3e5fa11525827f8152d168c6ca7a127e16bf. Nine selected upstream regression cases reproduced in Python integer port.256generated histories compared against exact upstream LwmaPerAlgo function body compiled with original arith_uint256 and minimal chain/params shim. This is not a full upstream test-suite or daemon build; legacy Hivemind dispatcher/activation not reproduced. Rescue flag/floor flag supplied explicitly.

Only after oracle agreement, adapt NUM_ALGOS4->2 and global spacing120->300seconds: laneT600,60same-lane intervals, gap40->20chainblocks, rescue rounds4->2blocks. Recompute BOTH lanes after each accepted parent because rescue depends on other-lane progress. Preserve compact integer quantization,256bit wrapping,sumTarget,predivision,solve clamps[-5T,6T],k/20floor,history walk=(61*2*8)=976blocks,bootstrap.

Floors cannot be copied from X11/GPU networks. Research sensitivity: easiest permitted target16× or1024×initiallane target, with rescue off/on. These arbitrary caps do not claim hardware calibration. Scale reference hashes/difficulties by2^32 so targets andeasyfloor arithmetic remain within256bits; normalize measured rate back to earlier model units. Score uses actual mined compact target-derived work, not requested future difficulty. Initial state presets initial targets; first accepted block onward exact adapted retarget/bootstrap applies;200Twarm-up included before metrics.

Retain DEGO-like median11/future1800s rules from prior simulator, NOT Kerrigan's complete timestamp/HMP consensus. Retain fixed toy lane weights, NOT HMP seal-weighted selection. This isolates DAA performance; any fork result pertains to adapted model, not live Kerrigan security.

Fourvariants x4behaviour scenarios x20seeds=320behaviourruns; fourvariants x4timestampstrategies x20=320stress; fourvariants x4strategies x4splits x50=3200pairedforktrials. Same seeds/horizons as previous model. Compare outage returns/100xdrop/normal calibration, plus prior60window+dormancy results. No selectivepublication/clockskew extension. No daemon edits.
