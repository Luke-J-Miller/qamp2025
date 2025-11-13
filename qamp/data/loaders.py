# qamp/data/loaders.py
import pickle
import gzip
from pathlib import Path
from typing import Any#, List, Dict



def load_benchmark(pkl_path: str | Path) -> dict[int | str, dict[str, Any]]:
    """
    Load a QAMP benchmark dataset from a pickle file.
    
    Parameters
    ----------
    pkl_path : str or Path
        Path to the benchmark `.pkl` or `.pkl.gz` file. Only recognized
        benchmark files are allowed. These include:
        
        - mutag_benchmark.pkl
        - snap_benchmark.pkl
        - ba_benchmark.pkl
        - er_benchmark.pkl
    It will also accept any of these ['mutag', 'snap', 'ba', 'er']
    Returns
    -------
    dict[int | str, dict[str, Any]]
        The benchmark data structure loaded from the pickle file.

    Raises
    ------
    FileNotFoundError
        If the provided path does not exist.

    ValueError
        If the filename is not in the list of allowed benchmark datasets.

    Notes
    -----
    Automatically uses gzip if the file ends with `.gz`.
    """
    _ALLOWED_BENCHMARKS = {
        "mutag_benchmark.pkl",
        "snap_benchmark.pkl",
        "ba_benchmark.pkl",
        "er_benchmark.pkl",
    }
    if pkl_path.lower() in ['mutag', 'snap', 'ba', 'er']:
        match pkl_path.lower():
            case 'mutag':
                pkl_path = "mutag_benchmark.pkl"
            case 'snap':
                pkl_path = "snap_benchmark.pkl"
            case 'ba':
                pkl_path = "ba_benchmark.pkl"
            case 'er':
                pkl_path = "er_benchmark.pkl"


    if not pkl_path.exists():
        
        raise FileNotFoundError(f"Benchmark file not found: {pkl_path}")


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






