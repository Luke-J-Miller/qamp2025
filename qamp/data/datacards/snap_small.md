# Dataset Card — SNAP small

- Domain: social
- Tasks: Subgraph Matching
- Source: [link](https://snap.stanford.edu/data/congress-twitter.html)
- License: [BSD](https://snap.stanford.edu/snap/license.html)

## Size
- |G| = 50
- |V| = 30
- |E| = ...

## Features
- node: username (string), graph_id (int)
- edge: weight (float), graph_id (int)
- Directed: true
- Weighted: true

## Split policy
- graph-level random split
  - train: 40 graphs
  - val: 5 graphs
  - test: 5 graphs
- seed: 42

## Preprocessing
Already cleaned

## Known Issues
- imbalance: ?
- sparsity: ?
- artifacts: ?

## Repro Notes
- seeds
- hashing policy
- checksums

## Provenance
See `PROVENANCE.md` in dataset folder.
