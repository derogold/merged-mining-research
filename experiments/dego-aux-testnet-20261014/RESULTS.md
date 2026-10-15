# Results — 2026-10-14, Kobe

## Passed
1. Research-only DeroGoldd, CLI miner and independent candidate inspector built inside Docker. Upstream cryptotest completed successfully with assertions enabled, including CN-UPX known-answer check.
2. Three separately stored/networked daemons mined/synchronized 10 non-genesis blocks. Headers show v2 at h1, v6 at h5 and v7/CN-UPX from h6.
3. **h6, premature new path:** valid difficulty-100 PoW, depth-one proof, rejected by real daemon RPC; tip stayed h5.
4. **h6, legacy path:** accepted; all three reached h6.
5. **h7, legacy path:** valid difficulty-100 PoW, depth-one proof, rejected by real daemon RPC; tip stayed h6.
6. **h7–10, new path:** accepted; all three reached the same h10 hash.
7. All 12 candidates independently deserialized: sufficient PoW, depth one, exactly one of old/new path roots matches. 10 accepted and 2 rejected as expected. Daemon logs explicitly report auxiliary Merkle-root failure for the two negatives.
8. All three daemons restarted and retained identical hashes at every height 0–10.
9. Node3 started with a fresh data directory and synced all 11 headers from peers, crossing both rule boundaries.
10. Actual genesis remains `7fb97df81221dd1366051b2d0bc7f49c66c22ac4431d879c895b06d66ef66f4c`.

## Interpretation
The shared-genesis auxiliary-slot problem can be addressed by a separately activated DEGO auxiliary path identity, without changing genesis. In this isolated chain, preactivation rules remain valid and the new rules activate at h7.

This is not yet a merged-mining pool or an accepted XKR block. The second Merkle leaf is a dummy fixture. CN-UPX and CN-Turtle still require their divergent mixing work. No speed, energy-saving, profitability, production-hardfork safety, deep reorg or adversarial peer claims are made.

## Harness repairs discovered
- Original CLI submission reporting accepted HTTP200 without checking the RPC error body, and even treated a missing response as success. Research miner now requires an OK result and saves exact requests/replies.
- Original bounded miner left a reporter thread joinable at shutdown and main would relaunch indefinitely. Research runs disable that reporter and exit once the requested count is reached or rejection occurs. First-attempt data is retained on Kobe under attempt1/; reported results are from the fresh rerun.
- Build-only adapters for distro package APIs are isolated in patch_compat.py. No upstream/mainnet repository was edited.

## What persists
Kobe: `/tmp/dego-aux-testnet-20261014/` contains source, binaries, logs, chain data and build image receipts. Three test daemon containers remain up on the internal `dego-aux-testnet-lab` network; miner has exited. Restart policy is `no`. Their configured limits are 1 CPU / 2GiB each. Build image and artifacts remain; existing services were untouched.

## Next gate
Replace the dummy sibling with an XKR auxiliary header and exercise a common parent work blob under both actual proof validators. Then integrate pool-issued branch/continuation jobs, with nonce search solely at the miner. Only after validity passes measure shared initialization against two independent mining paths on equal CPU and energy budgets.
