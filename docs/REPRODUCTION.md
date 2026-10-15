# Reproduction and retained laboratory

## Current inventory, checked 15 October 2026

Six containers remain running on the laboratory host, with restart policy `no`. This repository publication did not alter them.

| Lab | Containers | P2P ports | RPC ports | Node 1 observed tip |
|---|---|---|---|---|
| DEGO | dego-aux-testnet-node1/2/3 | 43071–43073 | 43171–43173 | 19, v7, difficulty 100 |
| XKR | xkr-aux-testnet-node1/2/3 | 43271–43273 | 43371–43373 | 15, v5, difficulty 100 |

DEGO node 1 tip: `ada947db0e833ffc96065b605e19b2695fdb0ff38f740cb8cc2d984811dfa471`.
XKR node 1 tip: `32897ee80554d1b019847ffbd8ab5ca8b8bad176a16f2b8548574d64020ecc2e`.
Only node 1 RPC tips were rechecked for this publication; historical all-node convergence evidence is in the experiment bundles.

Host paths remain `/tmp/dego-aux-testnet-20261014/` and `/tmp/dego-xkr-dual-testnet-20261014/`. Internal Docker subnets are 172.30.247.0/24 and 172.30.248.0/24. RPC access was verified through private container IPs, not assumed from Compose host-port declarations. No public peers are configured. All six existing containers were observed running; no new miner was started for this publication.

**Preservation caveat:** `/tmp` and restart=no are not durable backup/automatic recovery policies. Existing runtime state is deliberately left intact. The repository preserves reconstruction recipes and recorded evidence, not a crash-consistent snapshot of live RocksDB databases. Do not clean these paths or use `docker compose down -v`. Moving/persisting live databases should be a separate controlled operation, not a silent archival side effect.

## Evidence-first reproduction

1. Run `python3 tools/verify_archive.py` from repository root to verify archived bytes.
2. Read the chosen experiment's README, RESULTS or REPORT and its source-pin receipts.
3. Use Linux/x86 for native mining conclusions. The tested host is a Ryzen 9 5900X; an earlier inventory description was stale.
4. Prepare a separate checkout and non-overlapping Docker names/subnets/ports. Existing scripts are one-shot research fixtures and can conflict with a retained lab.
5. Use tmux for long remote builds. Preserve full logs, exit statuses, compiler versions and known-answer tests.
6. Re-run prerequisites in dependency order; many harnesses reference historical `/tmp` source/probe paths. They are documented research recipes, not a single hermetic installer.

## Dependency map

- Quad study: pinned source trees → native x86 libraries → published known answers → carrier/structure fixtures. No full-node acceptance claim.
- DEGO/XKR source study → native probes → common-envelope pilot → DEGO selector testnet → XKR dual-network testnet.
- Shared initialization/profile/interleaving/standalone controls depend on those pinned source trees and generated helper libraries.
- Python difficulty suites are model-level work, separate from daemon binaries. Read SPEC files before changing parameters.
- Kerrigan oracle requires its exact source revision; `build_oracle.py` extracts the original function and links original arithmetic with a minimal shim. Generated executable omitted; source and receipts retained.

## What the archive excludes

Generated `.so`/`.dylib` libraries, the platform-specific oracle executable and Python caches are listed in `excluded-artifacts.json`. They can be regenerated from the corresponding sources and environment, subject to the reproduction limits above. Blockchain databases, wallet secrets and entire upstream Git histories are not included. Pinned revisions, patches and retained upstream source excerpts provide provenance, not a complete offline build mirror.

Original reports may use historical absolute paths and earlier tips. Those are preserved evidence, not current operational instructions. No old script should be launched blindly against the retained lab.

## Verification levels

The archive verifier checks bytes and links in newly authored documentation. It does not re-run multi-hour measurements, rebuild native daemons, validate economic security, or certify that third-party dependencies remain available. Historical reports preserve their own checks and limitations. Result reproducibility and byte preservation are distinct claims.
