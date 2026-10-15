# Mainnet genesis audit — 2026-10-14

Pinned sources (same HEADs as prior quad study): WRKZ 364df861cdf6f1383a3240469a6fb0b85c72d579, Fuego 8a15ebaf8c9895da452d08ad71f0913e9810badd, uPlexa 78d16bad909c820c19765517fe57be61c6e1faaa. DEGO reference c502139f6ec02928c20dd2c8683c40daf97f352f.

- WRKZ mainnet genesis checkpoint: 877e55b4e902b9bf4c9e0a7c16440f449339d56679c49d62261ae5c92596a6ce. Source-derived reconstruction matches. Different genesis tx from DEGO, timestamp0, nonce70. Its aux predicate uses genesis as path.
- XFG source-derived genesis hash: ef32c9b0c293a377f4e5c796c833285226c78ff0195d5f9f9eb55c011863c14b. Different genesis tx, timestamp0, nonce70. Its aux predicate uses genesis as path. Not yet independently native-daemon/live-node confirmed.
- UPX source-derived mainnet genesis hash: c0b5b2b75795fee292f4ec6fddf772f7605518cf03c976767d53fd63cbe78bb9. Different genesis tx, timestamp0, configured nonce10000; generation calls nonce finder at difficulty1. Monero-derived standalone block/work layout, not the same embedded-parent aux path. Not independently native-daemon/live-node confirmed.
- DEGO/XKR native hash previously obtained: 7fb97df81221dd1366051b2d0bc7f49c66c22ac4431d879c895b06d66ef66f4c. Source-derived model also matches DEGO's checkpoint.

model_hashes.py uses native cn_fast_hash and a source-derived v1 genesis serializer (header, tx-root and count, then length-prefixed block hashing blob). It does NOT instantiate three native daemons. Inputs/outputs in JSON. Exact XFG/UPX values remain provisional pending independent native/live verification. No mainnet queries were made.

All three candidate auxiliary identities DEGO/WRKZ/XFG have distinct reconstructed paths. Their first divergence is later than bit0: DEGO 0x7f, WRKZ 0x87, XFG 0xef. Do not assign arbitrary sibling slots; construct genesis-directed branches at sufficient depth. This removes the observed identical-identity concern from the previous quad candidate, not its remaining serializer/block-acceptance/wallet-spendability gates. UPX is the proposed standalone carrier and need not be a fourth auxiliary leaf.

Source anchors: WRKZ src/config/CryptoNoteCheckpoints.h:33, CryptoNoteConfig.h:90; src/cryptonotecore/Currency.cpp:752. XFG src/CryptoNoteConfig.h:528; src/CryptoNoteCore/Currency.cpp:111 and :1563, CryptoNoteFormatUtils.cpp:607. UPX src/cryptonote_config.h:206; src/cryptonote_core/cryptonote_tx_utils.cpp:950; src/cryptonote_basic/cryptonote_format_utils.cpp:1362 and serialization/string.h.
