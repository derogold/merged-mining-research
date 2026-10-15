# DEGO dual-PoW: adversarial timestamps and forks

Read RESULTS.md for findings, SPEC.md for frozen model rules. Python standard library only.

Reproduce:

    python3 run.py
    python3 checks.py
    python3 report.py

model.py contains separate wall/header clocks, candidate timestamp checks and DAA rules. run.py produces raw deterministic seeded results. No external service, real mining or daemon consensus modification. Paths are relative to this folder, so this experiment is standalone.

The preceding honest-time simulator is a separate experiment. Neither is proof that production DEGO/XKR is vulnerable. This experiment tests proposed dual-PoW rules and identifies reasons not to implement them yet.
