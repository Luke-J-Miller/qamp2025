# Do not import heavy libs (qiskit, torch, etc.) at package import time.
__all__: list[str] = []

# Optional but helpful: a package version so the import check can verify it's the right module.
__version__ = "0.1.1"

