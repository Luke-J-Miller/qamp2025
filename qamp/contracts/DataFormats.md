# Data Formats

Normalized dataset folder contains:
- nodes.parquet   (required: node_id:int; optional: node attributes)
- edges.parquet   (required: u:int, v:int; optional: edge attributes)
- meta.yaml       ({ name, domain, directed, weighted, attributes:{nodes,edges}, seed, source, license })
- splits.yaml     ({ train/val/test } or { eval })
- hashes.parquet  (SHA256 per graph from canonical sorted edgelist)
