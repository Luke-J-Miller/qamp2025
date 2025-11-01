# Config Spec

## Dataset config (configs/datasets/*.yaml)
```
name: str
domain: str
paths: { nodes, edges, meta, splits }
directed: bool
weighted: bool
attributes: { nodes:[...], edges:[...] }
seed: int
split_policy: str
```

## Backend config (configs/backends/*.yaml)
```
type: sim|ibm
name: str
transpile_opt_level: int
shots: int
```

## Run config (configs/runs/*.yaml)
```
dataset_ref: str
method: str
method_params: {}
backend_ref: str
seed: int
output_dir: path
```
