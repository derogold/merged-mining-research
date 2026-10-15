# DEGO × XKR isolated dual-daemon experiment

Goal: three XKR testnet nodes alongside the three DEGO nodes from ../dego-aux-testnet-20261014, and actual block acceptance using a common parent-work blob with both real auxiliary leaves.

Pinned XKR: cf5a63e16b64200adb5445ea97d4186a0fdcb88a. Genesis and auxiliary selector remain unchanged. Uses upstream USE_TESTNET, distinct lab UUID, exclusive private peers, existing empty checkpoint list; difficulty100 instead of upstream testnet1; CN-Turtle from height6. Upstream testnet coinbase unlock window1 remains. No mainnet connection or mutation.

XKR P2P ports43271–43273, RPC43371–43373, private Docker subnet172.30.248.0/24 (internal), no host publishing. Node IPs .11/.12/.13. Each node capped at1CPU/2GiB, no restart policy.

Build-only system-package CMake uses the previous DEGO build image plus Boost packages. RocksDB wrapper compiled without RTTI to match distro library. UPnP is disabled in this isolated build: its bundled header versus distro library caused startup failure at discovery, and lab daemons should never create router mappings. Bounded miner fixes RPC acceptance reporting, disables its detached reporter and stops after its limit.

`run_dual.py` is an orchestration fixture, NOT a production pool: fetches both native templates, puts their real auxiliary leaves into a depth-one tree, constructs matching parent work, gives the work to `dual_worker.py`, then verifies/submits to both real daemons. The controller has no nonce search. Worker is bounded and implements two full native algorithm branches, not shared-initialization optimization. It searches for a nonce meeting both targets, short-circuiting XKR after a DEGO miss; this is correctness testing, not an optimal payout policy.

No energy savings or equal-cost dual mining claim is implied. Initial build/run failures and any cryptographic self-test failures must be resolved or explicitly reported before accepting results.

## Reproduction and operation
See RESULTS.md for observed outcomes. The archive includes both the preceding DEGO testnet directory and this directory. On a fresh Linux x86-64 host with Docker, git, Python3 and GCC, first run the DEGO directory's prepare.sh (ends at h10), then this directory's prepare.sh. Both are one-shot lab procedures and refuse an existing source checkout. Fixed container names/subnets must be unused. No binaries or chain database are needed from the original machine.

The build uses source commits and records package versions, but apt is not snapshot-pinned: this is a reproducible procedure, not a bit-identical hermetic image.

The test address uses publicly known keys and is exclusively for this disposable network. No real funds. `docker compose -f compose.json stop` stops this XKR lab; the DEGO lab has its own compose file. Do not run both prepare scripts again against existing chains: the acceptance schedule assumes fresh state.

The worker's elapsed times and hash counts are diagnostic receipts, not controlled performance or energy benchmarks.
