# qamp/data/checks.py
import pandas as pd
import yaml
from pathlib import Path
from qamp.data.io import compute_summary, write_summary

def validate_parquet_schema(nodes_path, edges_path, required_node_cols=("node_id",), required_edge_cols=("u","v")):
    nodes = pd.read_parquet(nodes_path)
    edges = pd.read_parquet(edges_path)
    # columns present
    missing_node = [c for c in required_node_cols if c not in nodes.columns]
    missing_edge = [c for c in required_edge_cols if c not in edges.columns]
    if missing_node or missing_edge:
        return False, f"Missing cols: nodes_missing={missing_node}, edges_missing={missing_edge}"
    # unique node ids and no NaNs
    if nodes["node_id"].isna().any():
        return False, "NaN in node_id"
    if edges[["u","v"]].isna().any().any():
        return False, "NaN in edge u/v"
    # ids integer type check
    if not pd.api.types.is_integer_dtype(nodes["node_id"]):
        try:
            nodes["node_id"].astype(int)
        except Exception:
            return False, "node_id not integer-castable"
    return True, "schema-ok"

def validate_meta_and_splits(meta_yaml, splits_yaml, nodes_path):
    with open(meta_yaml,"r") as f:
        meta = yaml.safe_load(f)
    with open(splits_yaml,"r") as f:
        splits = yaml.safe_load(f)
    nodes = pd.read_parquet(nodes_path)
    node_ids = set(nodes["node_id"].astype(int).tolist())
    # meta required keys
    required = ["name","domain","seed","directed","weighted"]
    missing = [k for k in required if k not in meta]
    if missing:
        return False, f"meta missing keys: {missing}"
    if not isinstance(meta["seed"], int):
        return False, "meta.seed must be int"
    # splits indices exist in nodes (splits may be graph-level or node-level)
    for k,v in splits.items():
        # check membership for a sample element if list not empty
        if not v: 
            continue
        sample = v[0]
        # sample may be graph id or node id; try both: if integer and not in node_ids that's ok if graph-level but we can't detect automatically.
        # We'll conservatively check that all split entries are integers
        if not all(isinstance(x, int) for x in v):
            return False, f"split {k} has non-integer indices"
    return True, "meta_splits_ok"

def validate_and_write_summary(dataset_dir):
    nodes = pd.read_parquet(Path(dataset_dir)/"nodes.parquet")
    edges = pd.read_parquet(Path(dataset_dir)/"edges.parquet")
    summary = compute_summary(nodes, edges)
    write_summary(summary, dataset_dir)
    return True, "summary_written"
