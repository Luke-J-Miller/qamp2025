# qamp/data/loaders.py
import pickle
import gzip
from pathlib import Path
from typing import Any#, List, Dict

def load_benchmark(pkl_path: str | Path) -> dict[int | str, dict[str, Any]]:
    pkl_path = Path(pkl_path)
    if not pkl_path.exists():
        raise FileNotFoundError(pkl_path)

    opener = gzip.open if pkl_path.suffix == ".gz" else open
    with opener(pkl_path, "rb") as f:
        data: dict[int | str, dict[str, Any]] = pickle.load(f)
    return data



def iter_instances(
    data: dict[int | str, dict[str, Any]],
    seed: int | None = 42,
) -> list[dict[str, Any]]:
    import random
    rng = random.Random(seed)
    instances = []

    # This now works because key can be str
    global_meta: dict[str, Any] = data.get("__metadata__", {})

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





