# DEGO dual-PoW estimator comparison

Read RESULTS.md. SPEC.md is the frozen initial experiment. dormancy/SPEC.md is a separately frozen follow-up prompted by initial results. Both specifications retain their pre-run hashes.

Reproduce, Python standard library only:

    python3 run.py
    python3 checks.py
    python3 dormancy/run.py
    python3 dormancy/checks.py
    python3 report.py

Standalone model, no daemon dependencies. Previous signed candidate retained as baseline. Current difficulty/chain-work arithmetic is floating point, not production integer consensus. Raw results/checks and weak-lane measurements included. No mainnet changes.
