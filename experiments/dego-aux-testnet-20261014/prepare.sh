#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
test ! -e source || { echo 'Use a fresh working directory; source already exists.' >&2; exit 1; }
git clone https://github.com/derogold/derogold-core.git source
git -C source checkout c502139f6ec02928c20dd2c8683c40daf97f352f
python3 patch_testnet.py source
python3 patch_miner_receipts.py source
python3 patch_bounded_miner.py source
python3 patch_compat.py source
cp ResearchCMake.txt source/CMakeLists.txt
cp research_inspect.cpp source/
curl -fLsS https://raw.githubusercontent.com/yhirose/cpp-httplib/v0.18.7/httplib.h -o source/external/httplib.h
printf '%s  %s\n' '4770f8ea3d3fcd27b0b713c783d9b53bce3baddbd5adad13714011df96142526' 'source/external/httplib.h' | sha256sum -c -
docker build -t dego-research-build:20261014 .
docker run --rm --cpus 4 --memory 8g -v "$PWD:/research" dego-research-build:20261014 bash -c 'cmake -S /research/source -B /research/build -G Ninja -DCMAKE_BUILD_TYPE=Release && cmake --build /research/build --target DeroGoldd miner cryptotest research-inspect -j4'
docker run --rm --network none --cpus 1 --memory 1g -v "$PWD:/research:ro" dego-research-build:20261014 /research/build/src/cryptotest > cryptotest.log
mkdir -p data/node{1,2,3}
docker compose -f compose.json up -d
python3 run_boundary.py
