# QAMP — Quantum Subgraph Matching Benchmark (Scaffold)

This repository scaffolds a resource-aware benchmarking suite for quantum graph matching
(QAOA, quantum kernels, QGNN) with fair classical baselines. **Week 1 is scaffolding only**:
stable structure, dependencies declared, contracts written, and logging fields frozen.

---

## Installation

### Colab / default installation
The default dependencies are pinned to match Google Colab’s stack (Torch 2.8.0 trio + jedi), so you can install with a single command:

pip install "git+https://github.com/Luke-J-Miller/qamp2025.git"

This should install without dependency warnings on Colab and similar environments.

### Non-Colab or custom Torch
If you need a different Torch build (e.g., CUDA-specific), install without dependencies and bring your own Torch:

# Install package only (no dependencies)
pip install --no-deps "git+https://github.com/Luke-J-Miller/qamp2025.git"

# Then install your preferred Torch stack (examples)

# CPU:
pip install torch torchvision torchaudio -f https://download.pytorch.org/whl/torch_stable.html

# CUDA (example; consult https://pytorch.org/get-started/ for versions that match your driver):
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

Note: heavy imports (e.g., Qiskit, Torch) are not executed at package import time; they are imported lazily inside the functions that use them.

---

## What is intentionally NOT done in Week 1
- No dataset downloads or normalization
- No algorithms executed (classical or quantum)
- No tests beyond formatting/linting/typing
- No backend tokens or device runs

---

## Repo structure (high-level)
```
qamp/
  data/                 # loaders, (Week 2) generators, dataset cards
  classical/            # Ullmann, VF2, WL, GNN baselines (Week 3)
  quantum/              # QAOA, quantum kernels, QGNN (Weeks 4–9)
  eval/                 # logging schema, metrics/tables/plots
  backends/             # notes + later backend configs
  contracts/            # APIs, DataFormats, ConfigSpec (frozen in Week 1)
configs/                # dataset/backend/run configs (placeholders now)
docs/                   # ROADMAP and project docs
.github/workflows/      # Continuous Integration (checks only)
```

Key files:
- qamp/eval/logging_schema.json — JSONL record fields (frozen in Week 1)
- qamp/contracts/* — API and format contracts (authoritative)
- .github/workflows/continuous-integration.yml — format/lint/type + import check

---

## Continuous Integration (checks only)
Every push/PR runs:
- Formatting (ruff, black --check)
- Linting (ruff check)
- Typing (mypy)
- A fast import qamp check

No datasets, algorithms, or devices are touched by CI in Week 1.

---

## Roadmap (high-level)
- Week 1: Scaffolding (this)
- Week 2: Datasets (normalize to Parquet; implement loaders)
- Week 3: Classical baselines (Ullmann, WL, GNN)
- Weeks 4–5: QAOA (setup + refinement/noise)
- Weeks 6–7: Quantum kernels (setup + refinement/noise)
- Weeks 8–9: QGNN (setup + refinement/noise)
- Week 10: Consolidation
- Week 11: Draft + working figures
- Week 12: Edits, repro bundle, release
