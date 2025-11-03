# qamp/data/loaders.py
import os
import pickle
from pathlib import Path
import pandas as pd
from qamp.data.io import compute_summary
from hashlib import sha256

def _file_hash(paths):
    h = sha256()
    for p in sorted(paths):
        with open(p, "rb") as f:
            # read in chunks
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                h.update(chunk)
    return h.hexdigest()

def load_dataset(cfg: dict, cache_dir=".cache/qamp", use_cache=True):
    """
    cfg keys: path (repo-relative), directed, weighted
    returns dict with 'target','pattern','gt_mapping','splits','meta'
    """
    import rustworkx as rx  # primary in-memory representation
    from pathlib import Path
    path = Path(cfg["path"])
    nodes_path = path / "nodes.parquet"
    edges_path = path / "edges.parquet"
    meta_path = path / "meta.yaml"
    splits_path = path / "splits.yaml"

    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    # compute hash key for cache
    key = _file_hash([str(nodes_path), str(edges_path)])
    cache_file = cache_dir / f"{path.name}_{key}.pkl"

    if use_cache and cache_file.exists():
        with open(cache_file, "rb") as f:
            return pickle.load(f)

    nodes = pd.read_parquet(nodes_path)
    edges = pd.read_parquet(edges_path)
    meta = {}
    try:
        import yaml
        with open(meta_path, "r") as f:
            meta = yaml.safe_load(f)
    except Exception:
        meta = {}

    # Build rustworkx Graph or DiGraph
    directed = meta.get("directed", cfg.get("directed", False))
    G = rx.PyGraph() if not directed else rx.PyDiGraph()

    # nodes: ensure deterministic ordering: sort by node_id
    nodes_sorted = nodes.sort_values("node_id").reset_index(drop=True)
    node_id_to_index = {}
    for i, row in nodes_sorted.iterrows():
        node_id = int(row["node_id"])
        attrs = row.to_dict()
        G.add_node(attrs)
        node_id_to_index[node_id] = i

    # edges: add edges respecting directed/weighted
    for _, r in edges.iterrows():
        u = int(r["u"]); v = int(r["v"])
        iu = node_id_to_index.get(u)
        iv = node_id_to_index.get(v)
        if iu is None or iv is None:
            continue
        attr = {k:v for k,v in r.items() if k not in ("u","v")}
        if directed:
            G.add_edge(iu, iv, attr)
        else:
            G.add_edge(iu, iv, attr)

    # optional conversion helper: to torch_geometric.Data (import locally)
    def to_pyg(graph):
        try:
            import torch
            from torch_geometric.data import Data
        except Exception as e:
            raise RuntimeError("To convert to PyG, install torch and torch_geometric") from e
        # minimal conversion: node features empty, edge_index from graph edges
        edges_list = list(graph.edge_list())
        if not edges_list:
            return Data()
        u = [e[0] for e in edges_list]
        v = [e[1] for e in edges_list]
        edge_index = torch.tensor([u, v], dtype=torch.long)
        return Data(edge_index=edge_index)

    result = {
        "target": G,
        "pattern": None,
        "gt_mapping": meta.get("gt_mapping"),
        "splits": (Path(splits_path).read_text() if Path(splits_path).exists() else {}),
        "meta": meta
    }
    # cache
    with open(cache_file, "wb") as f:
        pickle.dump(result, f)
    return result
