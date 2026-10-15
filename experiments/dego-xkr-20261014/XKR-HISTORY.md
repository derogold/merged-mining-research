# Kryptokrona PoW history follow-up — 2026-10-14

Full repository history fetched; examined early tag 0.0.1 (cce76c18, 2019-04-14) against pinned HEAD cf5a63e1 (2026-09-23).

- April 2 2019 commit 37c2bda58f3bed2319ceeb5d68ad6765cfbf79c4 changes inherited V4/V5 upgrade constants from 350000/1200000 to 3/4. V2/V3 were already 1/2.
- Both early tag and current mainnet configure 1/2/3/4. UpgradeManager selects a new version when upgradeIndex < blockIndex: V1 heights 0–1, V2 height 2, V3 height 3, V4 height 4, V5 from height 5.
- Both early tag and current code map V1–V3 to CN v0, V4 to CN-Lite-v1, V5 to Turtle-Lite-v2. Current v5 constants equal early tag: 262144-byte page/scratchpad, 131072 iterations, light=1, variant=2.
- src/crypto/slow-hash.c at 0.0.1 and HEAD compares exactly equal after stripping comments, include directives, whitespace and escaped newlines. This is a source comparison, not a binary or live-chain audit; dependencies/compiler differences are outside the normalized comparison.
- Old 2018 history includes inherited TurtleCoin CN-Turtle-at-1200000 work. Do not present that as a later Kryptokrona mainnet algorithm fork.
- Other height-dependent consensus rules exist (mixin/fusion/extra-size/block-blob/signature checks); FORK_HEIGHTS support metadata is not a list of PoW changes.
- Recent development exists: a953237d (2026-08-11) p2pool compatibility, b4ed4577 (2026-08-22) RPC concurrency, 7d068efd (2026-09-23) mempool cache. No basis to call project development absent merely because PoW remained stable.

Conclusion: current source history strongly supports stable Turtle-Lite-v2 for essentially all XKR mining since initial bootstrap. Leo's recalled historical CN-Turtle rate is therefore a more relevant baseline than the earlier generic variant caution suggested, but exact miner settings/hardware throughput remain unverified. No live chain replay was performed.
