# qamp/data/io.py
import os
import json
import hashlib
from pathlib import Path
import pandas as pd
import yaml

def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def write_parquet(nodes_df: pd.DataFrame, edges_df: pd.DataFrame, out_dir: str):
    ensure_dir(out_dir)
    nodes_path = Path(out_dir) / "nodes.parquet"
    edges_path = Path(out_dir) / "edges.parquet"
    nodes_df.to_parquet(nodes_path, index=False)
    edges_df.to_parquet(edges_path, index=False)
    return str(nodes_path), str(edges_path)

def write_meta(meta_dict: dict, out_dir: str):
    ensure_dir(out_dir)
    meta_path = Path(out_dir) / "meta.yaml"
    with open(meta_path, "w", encoding="utf8") as f:
        yaml.safe_dump(meta_dict, f, sort_keys=False)
    return str(meta_path)

def write_splits(split_dict: dict, out_dir: str):
    ensure_dir(out_dir)
    splits_path = Path(out_dir) / "splits.yaml"
    # Ensure indices are lists (yaml-serializable)
    serial = {k: list(v) for k,v in split_dict.items()}
    with open(splits_path, "w", encoding="utf8") as f:
        yaml.safe_dump(serial, f, sort_keys=False)
    return str(splits_path)

def compute_edgehash(edges_df: pd.DataFrame):
    """
    Canonicalize as sorted tuple list of (u,v) strings, then SHA256.
    """
    # Ensure u,v columns exist
    if not {"u","v"}.issubset(edges_df.columns):
        raise ValueError("edges_df must contain columns 'u' and 'v'")
    # Create canonical string (directedness will be preserved; for undirected sort (min,max))
    tuples = edges_df[["u","v"]].astype(str).apply(lambda r: f"{r['u']} {r['v']}", axis=1).tolist()
    tuples_sorted = sorted(tuples)
    blob = "\n".join(tuples_sorted).encode("utf8")
    return hashlib.sha256(blob).hexdigest()

def write_hashes(nodes_df: pd.DataFrame, edges_df: pd.DataFrame, out_dir: str):
    ensure_dir(out_dir)
    h = compute_edgehash(edges_df)
    hashes_path = Path(out_dir) / "hashes.parquet"
    df = pd.DataFrame([{"sha256_edgelist": h}])
    df.to_parquet(hashes_path, index=False)
    return str(hashes_path)

def compute_summary(nodes_df: pd.DataFrame, edges_df: pd.DataFrame):
    import numpy as np
    summary = {}
    n = len(nodes_df)
    m = len(edges_df)
    summary["num_nodes"] = int(n)
    summary["num_edges"] = int(m)
    # degree stats (approx) - compute deg from edges assuming undirected for stats
    degs = None
    if {"u","v"}.issubset(edges_df.columns):
        edges = edges_df[["u","v"]].astype(int)
        # safe degree compute (works for undirected and directed approximate)
        deg_series = pd.Series(list(edges["u"]) + list(edges["v"]))
        degs = deg_series.value_counts().astype(int)
        summary["degree_mean"] = float(degs.mean()) if not degs.empty else 0.0
        summary["degree_median"] = float(degs.median()) if not degs.empty else 0.0
        summary["degree_min"] = int(degs.min()) if not degs.empty else 0
        summary["degree_max"] = int(degs.max()) if not degs.empty else 0
    # attribute coverage: fraction non-null per column
    summary["node_attr_coverage"] = {c: float(nodes_df[c].notna().mean()) for c in nodes_df.columns if c!="node_id"}
    summary["edge_attr_coverage"] = {c: float(edges_df[c].notna().mean()) for c in edges_df.columns if c not in ("u","v")}
    return summary

def write_summary(summary: dict, out_dir: str):
    ensure_dir(out_dir)
    summary_path = Path(out_dir) / "summary.json"
    with open(summary_path, "w", encoding="utf8") as f:
        json.dump(summary, f, indent=2)
    return str(summary_path)
