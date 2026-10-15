# Kerrigan LWMA: integer oracle and two-lane experiment

Pinned upstream:7c4d3e5fa11525827f8152d168c6ca7a127e16bf.

## Evidence layers

1. vectors.py reproduces9selected upstream expected compact-target values. This is not the complete upstream test suite.
2. build_oracle.py extracts the **unchanged** LwmaPerAlgo body from pinned pow.cpp and compiles it with original arith_uint256.cpp, plus minimal chain/parameter stubs. C++20 is required. Initial C++17 attempt failed at compile time; no results came from it.
3. crosscheck.py compares256deterministic generated histories with native oracle, including rescue/floor flags, sparse/insufficient history, negative/large time intervals, and arithmetic edges. Exact compact values matched.
4. model.py adapts2algorithms and300second overall target, with arbitrary floor sensitivity. run.py drives prior scenario grid; checks.py tests adaptation boundaries.

Reproduce:

    python3 vectors.py
    python3 build_oracle.py
    python3 crosscheck.py
    python3 run.py
    python3 checks.py

The native build script expects the pinned repo at/tmp/kerrigan-research-20261014 and uses macOS clang++/dead_strip flags. The Python port/simulation needs only standard library. Changing host linker flags is required elsewhere. Model clock validation is DEGO-like; HMP is omitted, so no inference about Kerrigan's complete fork security is justified.

Original4algorithm oracle and2algorithm adaptation remain separate. No mainnet, daemon or mining workload changes. Raw timing/scoring figures are simulation outputs, not measurements on live Kerrigan.
