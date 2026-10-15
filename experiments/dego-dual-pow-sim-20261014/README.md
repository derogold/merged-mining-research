# DEGO dual-PoW consensus exploration

Read RESULTS.md for findings and limitations, SPEC.md for model rules. This is a Python-standard-library simulation, not a consensus implementation.

Reproduce:

    python3 sim.py
    python3 checks.py
    python3 forks.py
    python3 report.py

All outputs are deterministic for the supplied seeds and Python environment. Rates/weights are arbitrary simulation units; only T=300seconds was taken from current pinned DEGO config. All algorithms are represented by probabilistic work rates, not real hashes. Prior native hash/testnet experiments are separate evidence.

Artifacts: results.json (560behavior runs +constructed scoring), forks.json(1600paired fork trials), checks.json(9checks), RESULTS.md. No third-party package required. No cryptographic security certification, profitability or energy claim.
