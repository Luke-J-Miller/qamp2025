# qamp/data/loaders.py
import pickle
import gzip
from pathlib import Path
from typing import Any, List, Dict

def load_benchmark(pkl_path: str | Path) -> dict[int, dict[str, Any]]:
# def load_benchmark(pkl_path: str | Path) -> Dict[int, Dict[str, Any]]:
    """
    Load a benchmark file created by your generation script.

    Returns the raw dictionary:
        {
            0: {
                "graph_adj_mat": np.ndarray,
                "positive_subgraph_adj_mats": [np.ndarray, ...],
                "negative_subgraph_adj_mats": [np.ndarray, ...],
                "pos_nodes": [[int, ...], ...],        # optional
                ...                                 # any other keys you added
            },
            ...
            "__metadata__": { ... }                   # optional global metadata
        }
    """
    pkl_path = Path(pkl_path)
    if not pkl_path.exists():
        raise FileNotFoundError(pkl_path)

    opener = gzip.open if pkl_path.suffix == ".gz" else open
    with opener(pkl_path, "rb") as f:
        return pickle.load(f)


def iter_instances(
    data: Dict[int, Dict[str, Any]],
    seed: int | None = 42,
) -> List[Dict[str, Any]]:
    """
    Flatten the raw benchmark dict into a list of instances.

    Each instance contains:
        - "target_adj":          np.ndarray   (host graph)
        - "pattern_adj":         np.ndarray   (subgraph)
        - "gt_mapping":          dict | None  {pattern_idx → target_idx}
        - "label":               1 | 0
        - "meta":                dict          (source, graph_id, type, etc.)
    """
    import random
    rng = random.Random(seed)
    instances = []

    global_meta = data.get("__metadata__", {})

    for graph_id, entry in data.items():
        if graph_id == "__metadata__":
            continue

        target_adj = entry["graph_adj_mat"]

        # --- positives -------------------------------------------------
        pos_adjs = entry.get("positive_subgraph_adj_mats", [])
        pos_nodes = entry.get("pos_nodes", [None] * len(pos_adjs))

        for pat_adj, nodes in zip(pos_adjs, pos_nodes):
            gt_map = (
                {i: nodes[i] for i in range(pat_adj.shape[0])}
                if nodes is not None else None
            )
            instances.append({
                "target_adj": target_adj,
                "pattern_adj": pat_adj,
                "gt_mapping": gt_map,
                "label": 1,
                "meta": {
                    "source": "benchmark",
                    "graph_id": graph_id,
                    "type": "positive",
                    **global_meta,
                },
            })

        # --- negatives -------------------------------------------------
        neg_adjs = entry.get("negative_subgraph_adj_mats", [])
        for pat_adj in neg_adjs:
            instances.append({
                "target_adj": target_adj,
                "pattern_adj": pat_adj,
                "gt_mapping": None,
                "label": 0,
                "meta": {
                    "source": "benchmark",
                    "graph_id": graph_id,
                    "type": "negative",
                    **global_meta,
                },
            })

    rng.shuffle(instances)
    return instances

