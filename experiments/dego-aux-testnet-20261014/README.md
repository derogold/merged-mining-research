# DEGO auxiliary-identity research testnet

Isolated experiment, not a production fork proposal. No mainnet state or XKR source is changed.

## Hypothesis
A height-gated DEGO auxiliary Merkle-path selector can remove the DEGO/XKR shared-genesis slot collision while preserving the real genesis and historical proof rules. This alone does not provide free cross-algorithm work or prove mining efficiency.

## Network and rules
- Three DEGO containers on an internal Docker network, unique network UUID, no seeds.
- P2P ports 43071–43073; RPC 43171–43173, Compose requests loopback-only host bindings, but this Docker internal network does not publish them. Verified RPC access is via the private container IPs on Kobe (172.30.247.11–13); no public listeners.
- Separate data directories. No public P2P bindings. No automatic restart policy.
- Genesis unchanged; only genesis checkpoint retained, avoiding checkpoint bypass of PoW.
- Early upgrades advance one major version per height: h1/v2 through h6/v7. CN-UPX begins at h6.
- Auxiliary path identifier changes at h7, independent of major version. Below h7 uses genesis hash. New research ID is the 32-byte zero-padded ASCII `DEGO-AUX-TESTNET-20261014`; deliberately distinct first path bit.
- Difficulty fixed at 100 solely to keep private testing bounded. Monetary and PoW checks otherwise retained.
- Miner uses depth-one proofs with a zero sibling. This is a validation fixture, not a second live chain commitment.
- Pool performs no nonce search. This first test uses the upstream CLI miner directly; pool integration follows only after the consensus boundary passes.

## Source and build
Pinned DEGO source: c502139f6ec02928c20dd2c8683c40daf97f352f.
`patch_testnet.py` applies consensus and network isolation edits. `patch_miner_receipts.py` fixes test-harness submission reporting: HTTP 200 alone is not block acceptance; RPC result must say OK. Every candidate and reply is recorded.
`patch_compat.py` adapts this research build to Ubuntu 22.04 system packages: RocksDB synchronous flush, miniupnpc older signature, cxxopts exception type, RapidJSON GetObject spelling. These are not upstream production changes. cpp-httplib v0.18.7 is used header-only.
ResearchCMake bypasses upstream vcpkg dependency bootstrap, retains upstream source targets, and enables assertions in cryptotest.
Dockerfile uses the official Ubuntu image via ECR because Docker Hub returned HTTP429.

## Planned acceptance evidence
- CLI miner and all three real daemons run, mine and synchronize across h6/h7.
- Premature new-ID proof rejected at h6; legacy proof accepted at h6.
- Legacy proof rejected at h7; new-ID proof accepted at h7.
- Independent candidate inspection confirms adequate PoW and path membership, so a rejection cannot be mistaken for insufficient work.
- Node restart/replay preserves preactivation chain and converges to the same tip.

Results: see RESULTS.md. All listed acceptance checks passed on Kobe.

## Reproduce / operate
On a fresh Linux x86-64 Docker host with AES support, copy this directory and run `./prepare.sh`. Existing `source/` causes an intentional stop. Uses fixed Docker names/subnet; do not overlap another copy. After mining, run `python3 verify_receipts.py` and `python3 verify_replay.py`. The replay script archives node3 data and recreates only that test node. These scripts are one-shot fixtures, not idempotent maintenance jobs.

Stop only this lab with `docker compose -f compose.json stop`. Start it with `docker compose -f compose.json up -d`. No miner stays running after tests. No real wallet was used: test-address.txt uses publicly known keys and must never receive real funds. make_address.py documents address derivation using the earlier native probe library; the included address means that probe is not needed for reproduction.

The build is source-pinned, with binary hashes and installed package inventory in evidence/. Ubuntu apt versions are recorded rather than snapshot-locked, so this is a reproducible procedure, not a bit-for-bit hermetic build. source-changes.patch contains tracked-source changes; new ResearchAux.h and helper files are generated/copied by the included scripts.

The daemon's informational /info upgrade list is upstream hardcoded mainnet metadata and was not rewritten. Use observed block header versions and the patched UpgradeManager constants as the evidence for this private fork schedule.
