# MUTAG subset — datacard

**Source:** MUTAG subset (original dataset source link / license here)

**Counts**
- |V|: TBD
- |E|: TBD
- # graphs: TBD

**Attributes**
- node: atom (string), charge (int), graph_id (int)
- edge: bond_type (string), graph_id (int)

**Split policy**
- graph-level random split with seed=42:
  - train: X graphs
  - val: Y graphs
  - test: Z graphs

**Known issues**
- class imbalance (describe)
- missing charges on some atoms

**Provenance**
See `PROVENANCE.md` in dataset folder.
