#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
# Requires sibling DEGO experiment already built and mined through h10.
DEGO_LAB="$(cd ../dego-aux-testnet-20261014 && pwd)"
test ! -e source || { echo 'Use a fresh directory: source already exists.' >&2; exit 1; }
git clone https://github.com/kryptokrona/kryptokrona.git source
git -C source checkout cf5a63e16b64200adb5445ea97d4186a0fdcb88a
python3 patch_xkr.py source
cp ResearchCMake.txt source/CMakeLists.txt
cp xkr-template.cpp source/
cp dego-template.cpp "$DEGO_LAB/source/"
if ! grep -q 'add_executable(dego-template' "$DEGO_LAB/source/CMakeLists.txt"; then
cat >> "$DEGO_LAB/source/CMakeLists.txt" <<'EOF'
add_executable(dego-template dego-template.cpp)
target_include_directories(dego-template PRIVATE external/nlohmann-json)
target_link_libraries(dego-template CryptoNoteCore)
EOF
fi
docker build -t xkr-research-build:20261014 .
docker run --rm --cpus 4 --memory 8g -v "$PWD:/research" xkr-research-build:20261014 bash -c 'cmake -S /research/source -B /research/build -G Ninja -DCMAKE_BUILD_TYPE=Release && cmake --build /research/build --target kryptokronad miner crypto_test xkr-template -j4'
docker run --rm --cpus 2 --memory 4g -v "$DEGO_LAB:/research" dego-research-build:20261014 cmake --build /research/build --target dego-template -j2
docker run --rm --network none --cpus 1 --memory 1g -v "$PWD:/research:ro" xkr-research-build:20261014 /research/build/src/crypto_test > cryptotest-o2.log
# Native reference hashes; run this Linux host script with gcc installed.
python3 build_hashlibs.py
mkdir -p data/node{1,2,3}
docker compose -f compose.json up -d
python3 run_xkr.py
python3 run_dual.py
python3 verify_replay.py
