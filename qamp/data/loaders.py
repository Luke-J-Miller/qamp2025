# qamp/data/loaders.py
import pickle
import gzip
from pathlib import Path
from typing import Any
import urllib.parse
import requests
import io






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
    """
    if str(pkl_path).lower() in ['mutag', 'snap', 'ba', 'er']:
        match str(pkl_path).lower():
            case 'mutag':
                url = "https://github.com/Luke-J-Miller/qamp2025/raw/refs/heads/week3/qamp/data/molecular/mutag_graphs.pkl"
            case 'snap':
                url = "https://github.com/Luke-J-Miller/qamp2025/raw/refs/heads/week3/qamp/data/snap/snap_graphs.pkl"
            case 'ba':
                url = "https://github.com/Luke-J-Miller/qamp2025/raw/refs/heads/week3/qamp/data/synth/ba/ba_graphs.pkl"
            case 'er':
                url = "https://github.com/Luke-J-Miller/qamp2025/raw/refs/heads/week3/qamp/data/synth/er/er_graphs.pkl"
            case _:
                raise ValueError("Supported datasets are ['mutag', 'snap', 'ba', 'er']. Please reattempt with one of these options")

    try:
        resp = requests.get(url, stream=True, timeout=30)
        resp.raise_for_status()
        # read a small prefix to check gzip magic if present, then read remainder
        content = resp.content  # servers typically small here; benchmark pickles are usually not huge
    except Exception as exc:
        raise RuntimeError(f"Failed to download benchmark from URL '{url}': {exc}") from exc


    bio = io.BytesIO(content)
    data: dict[int | str, dict[str, Any]]
    try:
        data = pickle.load(bio)
    except Exception as exc:
        raise RuntimeError(f"Failed to unpickle data from URL '{url}': {exc}") from exc


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

















