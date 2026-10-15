# Result: ordinary implementation gains, small paired advantage

72 comparator runs in12balancedblocks, three real work blobs,512pairednonces/run. All output arrays matched both original native algorithms.

| Comparator | Total CPU seconds |
|---|---:|
| Original reference libraries |34.109455|
| Equivalent optimized standalone DEGO+XKR |23.861287|
| Optimized paired worker |23.745133|

Standalone optimization reduced CPU time30.04% versus originals; paired reduced30.39%. Pairing itself reduced measured CPU time **0.4868%** versus equivalent standalone work. Paired won12/12blocks, with reductions0.198–0.764%. Wall time corroborated0.4863% reduction. Thus the small effect was consistent within this run, not merely an aggregate cancellation; cross-host/general applicability is unproven.

Standalone DEGO cost4.363926CPU seconds, XKR19.497361CPU seconds for equal nonce counts. Both complete PoW computations still execute. The experiment does not measure energy, skip algorithm work, or demonstrate two coins for one coin's computation.

**Interpretation:** practically all the large prior improvement is available without pairing. A small implementation/scheduling benefit remains in this measured setup; cause not isolated (compiler code shape, allocation lifetime, cache state and batch boundaries differ). Do not describe the0.49% as cryptographic shared-work savings. No comparison with optimized production miners or ARM hardware.

No further performance experiments were triggered. No daemon/consensus/network changes or new block submissions. Reproducible scripts and raw timing/correctness data accompany this report; prerequisite pinned labs are documented in README.
