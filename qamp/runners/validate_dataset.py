# # runners/validate_dataset.py
# import sys
# from pathlib import Path
# from qamp.data.checks import validate_parquet_schema, validate_meta_and_splits, validate_and_write_summary

# def main(dataset_dir):
#     d = Path(dataset_dir)
#     nodes = d/"nodes.parquet"
#     edges = d/"edges.parquet"
#     meta = d/"meta.yaml"
#     splits = d/"splits.yaml"
#     ok1, m1 = validate_parquet_schema(nodes, edges)
#     if not ok1:
#         print(f"INVALID: schema check failed: {m1}")
#         return 1
#     ok2, m2 = validate_meta_and_splits(meta, splits, nodes)
#     if not ok2:
#         print(f"INVALID: meta/splits check failed: {m2}")
#         return 1
#     ok3, m3 = validate_and_write_summary(dataset_dir)
#     if not ok3:
#         print(f"INVALID: summary generation failed: {m3}")
#         return 1
#     print(f"VALID: {dataset_dir} -> summary.json written")
#     return 0

# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Usage: python runners/validate_dataset.py path/to/dataset_dir")
#         sys.exit(2)
#     sys.exit(main(sys.argv[1]))
