from typing import Any, Dict
import networkx as nx

# qamp/classical/vf2.py
from typing import Any
import numpy as np
import networkx as nx


def run_vf2(graph: Any, subgraph: Any) -> bool:
    """
    VF2 exact subgraph matcher.

    Inputs:
      graph, subgraph: either numpy.ndarray adjacency matrices (preferred)
                       or NetworkX Graph-like objects (already a Graph).

    Returns:
      bool -- True if `subgraph` is isomorphic to a subgraph of `graph`.
    """
    # If inputs are numpy arrays, convert to NetworkX graphs
    if isinstance(graph, np.ndarray):
        G = nx.from_numpy_array(graph)
    elif isinstance(graph, nx.Graph):
        G = graph
    else:
        raise TypeError("`graph` must be a numpy.ndarray or a networkx.Graph")

    if isinstance(subgraph, np.ndarray):
        H = nx.from_numpy_array(subgraph)
    elif isinstance(subgraph, nx.Graph):
        H = subgraph
    else:
        raise TypeError("`subgraph` must be a numpy.ndarray or a networkx.Graph")

    isomorphism_checker = nx.isomorphism.GraphMatcher(G, H)
    # GraphMatcher.subgraph_is_isomorphic() returns a bool
    is_subgraph: bool = isomorphism_checker.subgraph_is_isomorphic()
    return is_subgraph


