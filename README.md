# QAMP — Quantum Subgraph Matching Benchmark (Scaffold)

Week 1 is scaffolding only: stable structure, dependencies declared, contracts written, logging fields frozen.

## Install (handled by GitHub Actions on push)
Dependencies are declared in `pyproject.toml`. Local install (optional):

How to import in colab
```
%pip install -q -U setuptools wheel
%pip install -q "git+https://github.com/Luke-J-Miller/qamp2025.git@pin_environments"

import qamp
getattr(qamp, "__version__", "installed")
```
