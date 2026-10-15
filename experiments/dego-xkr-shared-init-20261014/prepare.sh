#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
# Requires both prior lab source directories and completed dual-results.json.
test -f ../dego-xkr-dual-testnet-20261014/dual-results.json
python3 build_baselines.py
python3 build_fused.py
gcc -O2 -shared -fPIC batch.c -o batch.so
python3 check_correctness.py > correctness.log
python3 benchmark.py > benchmark.log
python3 run_shared_live.py > shared-live.log

python3 summarize.py > summary.log
python3 build_direct.py > direct-build.log
python3 check_direct.py > direct-correctness.log
python3 benchmark_direct.py > direct-benchmark.log
python3 run_direct_live.py > direct-live.log
