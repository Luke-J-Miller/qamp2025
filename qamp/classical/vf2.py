from typing import Any, Dict
import networkx as nx

def run_vf2(graph: Dict[str, Any], subgraph: Dict[str, Any]) -> bool:
    """
    VF2 exact subgraph matcher.

    Inputs:
      graph: dict from load_dataset(...)
      subgraph:  dict from load_dataset(...)

    Returns bool
    """
    G = nx.from_numpy_array(graph)
    H = nx.from_numpy_array(subgraph)
    isomorphism_checker = nx.isomorphism.GraphMatcher(G, H)
    return isomorphsim_checker.subgraph_is_isomorphic()


