from typing import Any, Dict

def load_dataset(cfg: Dict[str, Any]) -> Dict[str, Any]:
    """
    Load a normalized dataset into in-memory graph objects.

    Expected cfg keys (see contracts/ConfigSpec.md):
      - paths: {nodes, edges, meta, splits}
      - directed: bool
      - weighted: bool
      - attributes: {nodes: [...], edges: [...]}
      - seed: int

    Returns:
      {
        "target": graph-like (nx.Graph or list thereof),
        "pattern": graph-like or None,
        "gt_mapping": dict[int,int] or None,
        "splits": dict,
        "meta": dict
      }

    Implement in Week 2.
    """
    raise NotImplementedError("Implement in Week 2")
