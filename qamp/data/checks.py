def validate_parquet_schema(nodes_path, edges_path, required_cols):
	# enforce node_id on nodes; u, v on edges; dtypes; no nans in ids
	pass

def validate_meta_and_splits(meta_yaml, splits_yaml):
	# required keys, seed is int, split indices exist in nodes
	pass
	
def compute_summary(nodes, edges):
	# write/overwrite summary.json
	pass
