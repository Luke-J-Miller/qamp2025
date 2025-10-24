from typing import Any, Dict

def run_vf2(dataset: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    VF2 exact subgraph matcher.

    Inputs:
      dataset: dict from load_dataset(...)
      config:  dict with at least a 'seed' key

    Returns dict with keys:
      - backend, resources, metrics, artifacts
    """
    raise NotImplementedError("Week 3")
