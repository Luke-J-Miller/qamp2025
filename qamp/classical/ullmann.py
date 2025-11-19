from typing import List, Tuple, Optional, Dict
# import random
# import numpy as np

# # ---------- helpers to convert adjacency-lists/matrices into bitmasks ----------

# def adjacency_list_to_bitmasks(adj: np.array, n: Optional[int] = None) -> List[int]:
#     """Given adjacency list `adj` where adj[v] is list of neighbors, return list of bitmasks neighbors_mask[v]."""
#     if n is None:
#         n = len(adj)
#     masks = [0] * n
#     for v, neighs in enumerate(adj):
#         m = 0
#         for u in neighs:
#             m |= (1 << u)
#         masks[v] = m
#     return masks

# def adjacency_matrix_to_bitmasks(mat: np.array) -> List[int]:
#     n = len(mat)
#     masks = [0] * n
#     for i in range(n):
#         m = 0
#         for j in range(n):
#             if mat[i][j]:
#                 m |= (1 << j)
#         masks[i] = m
#     return masks

# # ---------- Ullman algorithm implementation ----------

# class Ullman:
#     def __init__(self,
#                  G_neigh_masks: List[int],  # neighbors bitmask for G vertices
#                  P_neigh_masks: List[int],  # neighbors bitmask for P vertices
#                  induced: bool = False):
#         """
#         G_neigh_masks: list of int bitmasks: neighbors of each vertex in G
#         P_neigh_masks: list of int bitmasks: neighbors of each vertex in P
#         induced: if True, search for induced subgraph isomorphism; otherwise non-induced (P <= mapped subgraph)
#         """
#         self.G = G_neigh_masks
#         self.P = P_neigh_masks
#         self.nG = len(G_neigh_masks)
#         self.nP = len(P_neigh_masks)
#         self.induced = induced

#         # degrees
#         self.degG = [popcount(m) for m in self.G]
#         self.degP = [popcount(m) for m in self.P]

#         # prepare initial M0 (list of bitmasks, one per P-vertex)
#         # M0[i] has bit j set iff deg(P_i) <= deg(G_j)
#         self.M0 = [0] * self.nP
#         for i in range(self.nP):
#             mask = 0
#             for j in range(self.nG):
#                 if self.degP[i] <= self.degG[j]:
#                     mask |= (1 << j)
#             self.M0[i] = mask

#         # order P vertices by descending degree to improve pruning early
#         # `order` maps ordered index -> original P vertex index
#         self.order = sorted(range(self.nP), key=lambda i: -self.degP[i])
#         # `inv_order` maps original P index -> position in ordered list
#         self.inv_order = [0] * self.nP
#         for pos, orig in enumerate(self.order):
#             self.inv_order[orig] = pos

#         # reorder P_neigh_masks to match order
#         self.P_ord = [self.P[i] for i in self.order]
#         self.degP_ord = [self.degP[i] for i in self.order]

#         # reorder initial M0 to match pattern ordering
#         self.M0_ord = [self.M0[i] for i in self.order]

#         # Precompute neighbors masks for G (already given) for quick access
#         self.G_neigh_masks = self.G

#         # to record first found mapping
#         self.found_mapping: Optional[List[int]] = None

#     def search(self, find_one: bool = True) -> List[List[int]]:
#         """
#         Run the Ullman algorithm.
#         If find_one True: stops on first found mapping and returns list with single mapping.
#         Otherwise returns list of all mappings found (may be exponential).
#         Each mapping is returned as a list `mapP2G` of length nP where mapP2G[i] is the G vertex assigned to P vertex i (original P order).
#         """
#         solutions = []

#         # Working M is list of bitmasks, one per ordered P-row
#         M = list(self.M0_ord)

#         # prune initial matrix
#         if not self._prune(M):
#             return solutions  # no possible mappings

#         # used columns bitmask
#         used_cols = 0

#         # recursion
#         def recurse(cur_row: int, M_local: List[int], used_cols_local: int):
#             # early exit if we found one and just need one
#             if find_one and solutions:
#                 return

#             if cur_row == self.nP:
#                 # extract mapping and verify
#                 mapping_ord = [bit_index(row_mask) for row_mask in M_local]  # each row_mask should have exactly one bit
#                 if None in mapping_ord:
#                     return
#                 # convert ordered mapping back to original P indices
#                 mapping_orig = [None] * self.nP
#                 for pos_in_ord, g_vertex in enumerate(mapping_ord):
#                     orig_p_idx = self.order[pos_in_ord]
#                     mapping_orig[orig_p_idx] = g_vertex

#                 if self._verify_mapping(mapping_orig):
#                     solutions.append(mapping_orig)
#                 return

#             # choose possible columns for this row (bits not used)
#             candidates = M_local[cur_row] & (~used_cols_local)
#             # iterate over set bits
#             while candidates:
#                 j = candidates & -candidates
#                 candidates -= j
#                 col_idx = bit_index(j)
#                 # create new M copy
#                 M_next = M_local[:]  # shallow copy of list of ints
#                 # set this row to exact column j and DO NOT clear this column from other rows here;
#                 # pruning will remove it from others if necessary
#                 M_next[cur_row] = j
#                 used_next = used_cols_local | j

#                 # prune
#                 ok = self._prune(M_next, used_next)
#                 if ok:
#                     recurse(cur_row + 1, M_next, used_next)
#                     # maybe early stop
#                     if find_one and solutions:
#                         return

#         recurse(0, M, used_cols)
#         return solutions

#     def _prune(self, M: List[int], used_cols_mask: int = 0) -> bool:
#         """
#         Iteratively remove impossible placements:
#         For each (i,j) where M[i] has bit j:
#             for every neighbor x of P-vertex i, there must exist some neighbor y of G-vertex j such that M[x] has bit y.
#         If a row becomes zero => return False.
#         Optionally used_cols_mask can be provided to force columns already used (so even if other rows have that bit they'd be impossible),
#         but we don't clear those bits explicitly here; we treat used columns as unavailable by considering them absent.
#         """
#         changed = True
#         n = self.nP
#         while changed:
#             changed = False
#             for i in range(n):
#                 row_mask = M[i]
#                 # remove used columns from consideration
#                 row_mask &= ~used_cols_mask
#                 if row_mask != M[i]:
#                     M[i] = row_mask
#                     changed = True
#                 if row_mask == 0:
#                     return False  # no possible mapping for row i

#                 # iterate through candidate columns (bits)
#                 # We'll build a new mask of columns that are still valid for i
#                 valid_mask = 0
#                 candidate_mask = row_mask
#                 while candidate_mask:
#                     bit = candidate_mask & -candidate_mask
#                     candidate_mask -= bit
#                     g_j = bit_index(bit)
#                     # neighbors of the P-vertex i (in ordered indices):
#                     neighP_mask = self.P_ord[i]
#                     # we must check each neighbor x of P-i has at least one candidate y among neighbors of g_j (in G)
#                     # BUT our M uses ordered P rows, so we need to check M[x_pos] & neighbors_of_g_j != 0
#                     # The bits in M[x_pos] correspond to G vertices; neighbors_of_g_j is bitmask in G domain.
#                     ok_for_all_neighbors = True
#                     # iterate neighbor positions of i in P (these are bits in neighP_mask)
#                     nb_mask = neighP_mask
#                     while nb_mask:
#                         nb_bit = nb_mask & -nb_mask
#                         nb_mask -= nb_bit
#                         p_neighbor_idx = bit_index(nb_bit)  # original index in P
#                         # convert to ordered position
#                         pos_in_order = self.inv_order[p_neighbor_idx]
#                         # check if there exists y neighbor of g_j such that M[pos_in_order] has that bit
#                         if (M[pos_in_order] & self.G_neigh_masks[g_j]) == 0:
#                             ok_for_all_neighbors = False
#                             break
#                     if ok_for_all_neighbors:
#                         valid_mask |= bit
#                 if valid_mask != M[i]:
#                     M[i] = valid_mask
#                     changed = True
#                     if valid_mask == 0:
#                         return False
#         return True

#     def _verify_mapping(self, mapping_orig: List[int]) -> bool:
#         """
#         mapping_orig: list of length nP mapping P-original-index -> G-index
#         Verifies that for every edge (u,v) in P, (mapping[u], mapping[v]) is an edge in G.
#         If induced flag is True, also ensures there are no extra edges between mapped vertices in G.
#         """
#         # build adjacency quick tests
#         for u in range(self.nP):
#             mu = mapping_orig[u]
#             neigh_mask_p = self.P[u]
#             nb_mask = neigh_mask_p
#             while nb_mask:
#                 bit = nb_mask & -nb_mask
#                 nb_mask -= bit
#                 v = bit_index(bit)
#                 mv = mapping_orig[v]
#                 # check edge present in G adjacency
#                 if (self.G_neigh_masks[mu] >> mv) & 1 == 0:
#                     return False
#         if self.induced:
#             # also ensure no extra edges among mapped G vertices that are not in P
#             # for each pair u<v: if G has edge between mu,mv but P does not between u,v -> reject
#             for u in range(self.nP):
#                 mu = mapping_orig[u]
#                 for v in range(u+1, self.nP):
#                     mv = mapping_orig[v]
#                     g_has = ((self.G_neigh_masks[mu] >> mv) & 1)
#                     p_has = ((self.P[u] >> v) & 1)
#                     if g_has and not p_has:
#                         return False
#         return True

# # ---------- small utility functions ----------

# def popcount(x: int) -> int:
#     return x.bit_count()

# def bit_index(bitmask: int) -> Optional[int]:
#     """Return index of single set bit in bitmask (0-based). If bitmask has multiple bits, returns index of least significant set bit.
#        If zero, returns None."""
#     if bitmask == 0:
#         return None
#     return (bitmask & -bitmask).bit_length() - 1

# # ---------- example usage and simple tests ----------

# def example_1():
#     # G: a small graph (undirected)
#     # adjacency list for G (6 vertices)
#     G_adj = [
#         [1, 2],      # 0
#         [0, 2, 3],   # 1
#         [0, 1, 3],   # 2
#         [1, 2, 4, 5],# 3
#         [3],         # 4
#         [3]          # 5
#     ]
#     G_masks = adjacency_list_to_bitmasks(G_adj)

#     # P: triangle (3-cycle)
#     P_adj = [
#         [1,2],
#         [0,2],
#         [0,1]
#     ]
#     P_masks = adjacency_list_to_bitmasks(P_adj)

#     ull = Ullman(G_masks, P_masks, induced=False)
#     sols = ull.search(find_one=False)
#     print("Example 1: triangle in G, found mappings (P->G indices):")
#     for s in sols:
#         print(s)

# def example_2():
#     # G: a path of length 4 (5 nodes)
#     nG = 5
#     G_adj = [[i-1] if i>0 else [] for i in range(nG)]
#     for i in range(nG-1):
#         G_adj[i].append(i+1)
#     G_masks = adjacency_list_to_bitmasks(G_adj)

#     # P: path of length 3 (4 nodes)
#     P_adj = [[1],[0,2],[1,3],[2]]
#     P_masks = adjacency_list_to_bitmasks(P_adj)

#     ull = Ullman(G_masks, P_masks, induced=False)
#     sols = ull.search(find_one=False)
#     print("Example 2: path of 4 in path of 5, mappings count =", len(sols))
#     for s in sols:
#         print(s)

# def random_test():
#     # small random graphs to sanity-check (non-induced)
#     nG = 8
#     nP = 4
#     # random G
#     G_adj = [[] for _ in range(nG)]
#     for i in range(nG):
#         for j in range(i+1, nG):
#             if random.random() < 0.35:
#                 G_adj[i].append(j)
#                 G_adj[j].append(i)
#     G_masks = adjacency_list_to_bitmasks(G_adj)

#     # random P; ensure connected-ish
#     P_adj = [[] for _ in range(nP)]
#     for i in range(nP):
#         for j in range(i+1, nP):
#             if random.random() < 0.6:
#                 P_adj[i].append(j)
#                 P_adj[j].append(i)
#     P_masks = adjacency_list_to_bitmasks(P_adj)

#     ull = Ullman(G_masks, P_masks, induced=False)
#     sols = ull.search(find_one=False)
#     print("Random test G size", nG, "P size", nP, "found", len(sols), "mappings")

def run_ullmann(dataset: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    pass






