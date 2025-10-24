# APIs

## load_dataset(cfg: dict) -> dict
Returns:
- target: graph-like (single graph or list)
- pattern: graph-like or null
- gt_mapping: dict[int,int] or null
- splits: dict
- meta: dict

## Method runners
- run_ullmann(dataset: dict, config: dict) -> dict
- run_vf2(dataset: dict, config: dict) -> dict
- run_wl_kernel(dataset: dict, config: dict) -> dict
- run_gnn_baseline(dataset: dict, config: dict) -> dict
- run_qaoa_gi(dataset: dict, config: dict) -> dict
- run_quantum_kernel(dataset: dict, config: dict) -> dict
- run_qgnn(dataset: dict, config: dict) -> dict

Return dicts must include: { backend, resources, metrics, artifacts } and be writable as one JSONL record
conforming to `qamp/eval/logging_schema.json`.
