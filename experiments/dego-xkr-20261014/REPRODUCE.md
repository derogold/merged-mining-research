# Reproduce on Linux x86_64 with AES-NI

Prerequisites: git, Python 3, GCC and ordinary C development headers. Research scripts execute C builds in their own directory; inspect before use. No daemons, wallets or live network submissions.

```sh
git clone https://github.com/derogold/derogold-core.git /tmp/dego-xkr-research-dego
git -C /tmp/dego-xkr-research-dego checkout c502139f6ec02928c20dd2c8683c40daf97f352f
git clone https://github.com/kryptokrona/kryptokrona.git /tmp/dego-xkr-research-xkr
git -C /tmp/dego-xkr-research-xkr checkout cf5a63e16b64200adb5445ea97d4186a0fdcb88a
python3 probe.py
```

Use an isolated machine/container if these /tmp names already exist. On Kobe, run the Python command inside tmux. Output: generated instrumented C copies, seven shared libraries, build logs, results.json. Hardware AES required for the reuse checkpoint placement; no ARM/NO_AES claims. Early-return variants intentionally omit normal cleanup and are short-lived test-only probes.

Expected summary: full=0, init=16, round1=0, reuse_matches_xkr=16. Both known answers must pass; assertions fail otherwise.
