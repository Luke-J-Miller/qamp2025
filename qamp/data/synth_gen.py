# qamp/data/synth_gen.py
import random
import numpy as np
import pandas as pd
from qamp.data.io import write_parquet, write_meta, write_splits, write_hashes, compute_summary, write_summary
from pathlib import Path

def er_planted_subgraph(n_target, n_pattern, p, seed=None, noise=None):
    """
    Generate target graph with n_target nodes (Erdos-Renyi p) and plant a pattern subgraph of size n_pattern.
    Returns nodes_df, edges_df, gt_mapping (pattern_node -> target_node)
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    # create target nodes
    nodes = list(range(n_target))
    # edges from ER model
    edges = set()
    for i in range(n_target):
        for j in range(i+1, n_target):
            if np.random.rand() < p:
                edges.add((i,j))
    # build pattern as a small clique (or ER)
    pattern_nodes = list(range(n_pattern))
    pattern_edges = set()
    for i in range(n_pattern):
        for j in range(i+1, n_pattern):
            pattern_edges.add((i,j))
    # choose injection mapping
    placement = random.sample(nodes, n_pattern)
    gt_mapping = {i: placement[i] for i in pattern_nodes}
    # plant pattern edges into edges set (map pattern -> placement)
    for (u,v) in pattern_edges:
        tu, tv = gt_mapping[u], gt_mapping[v]
        edges.add(tuple(sorted((tu,tv))))
    # optionally apply noise
    if noise and noise.get("edge_flip_p",0)>0:
        flip_p = noise["edge_flip_p"]
        # flip each pair: if exists remove, else add with prob flip_p
        for i in range(n_target):
            for j in range(i+1, n_target):
                if np.random.rand() < flip_p:
                    if (i,j) in edges:
                        edges.remove((i,j))
                    else:
                        edges.add((i,j))
    # build dataframes
    nodes_df = pd.DataFrame({"node_id": nodes})
    edges_df = pd.DataFrame([{"u": u, "v": v} for (u,v) in sorted(edges)])
    return nodes_df, edges_df, gt_mapping

def ba_planted_subgraph(n_target, n_pattern, m, seed=None, noise=None):
    """
    Barabasi-Albert preferential attachment with m edges per new node, then plant clique of size n_pattern.
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    # simple BA: use networkx for generation if available; fallback simple model
    try:
        import networkx as nx
        G = nx.barabasi_albert_graph(n_target, m, seed=seed)
        edges = set(tuple(sorted(e)) for e in G.edges())
    except Exception:
        # fallback: connect each new node to 'm' earlier nodes uniformly
        edges = set()
        for new in range(m, n_target):
            targets = random.sample(range(new), m)
            for t in targets:
                edges.add(tuple(sorted((new,t))))
    nodes = list(range(n_target))
    # create pattern and mapping like ER (clique)
    pattern_nodes = list(range(n_pattern))
    pattern_edges = set((i,j) for i in pattern_nodes for j in pattern_nodes if i<j)
    placement = random.sample(nodes, n_pattern)
    gt_mapping = {i: placement[i] for i in pattern_nodes}
    for (u,v) in pattern_edges:
        edges.add(tuple(sorted((gt_mapping[u], gt_mapping[v]))))
    # noise optional same as ER
    if noise and noise.get("edge_flip_p",0)>0:
        flip_p = noise["edge_flip_p"]
        for i in range(n_target):
            for j in range(i+1, n_target):
                if np.random.rand() < flip_p:
                    if (i,j) in edges:
                        edges.remove((i,j))
                    else:
                        edges.add((i,j))
    nodes_df = pd.DataFrame({"node_id": nodes})
    edges_df = pd.DataFrame([{"u": u, "v": v} for (u,v) in sorted(edges)])
    return nodes_df, edges_df, gt_mapping

def write_synth_bundle(out_dir, nodes_df, edges_df, meta, splits):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    write_parquet(nodes_df, edges_df, out_dir)
    write_meta(meta, out_dir)
    write_splits(splits, out_dir)
    write_hashes(nodes_df, edges_df, out_dir)
    summary = compute_summary(nodes_df, edges_df)
    write_summary(summary, out_dir)
    return out_dir

if __name__ == "__main__":
    # example: produce tiny + small for ER and BA
    base = "data/synth"
    for name, fn in [("er_planted_small", lambda: er_planted_subgraph(200, 8, p=0.02, seed=42)),
                     ("er_planted_tiny", lambda: er_planted_subgraph(60, 6, p=0.04, seed=43)),
                     ("ba_planted_small", lambda: ba_planted_subgraph(200, 8, m=2, seed=44)),
                     ("ba_planted_tiny", lambda: ba_planted_subgraph(60, 6, m=2, seed=45))]:
        nodes_df, edges_df, gt_mapping = fn()
        out = f"{base}/{name}"
        meta = {
            "name": name,
            "domain": "synth",
            "generator": "er_planted" if "er" in name else "ba_planted",
            "seed": int(meta_seed := (42 if "er" in name else 44)),
            "directed": False,
            "weighted": False,
            "params": {"n_nodes": int(len(nodes_df)), "n_edges": int(len(edges_df))},
        }
        splits = {"train": [], "val": [], "test": list(nodes_df["node_id"][:int(0.2*len(nodes_df))])}
        # include gt mapping for pattern injection
        meta["gt_mapping"] = gt_mapping
        write_synth_bundle(out, nodes_df, edges_df, meta, splits)
        print("Wrote", out)
