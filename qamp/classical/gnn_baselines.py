from typing import Any, Dict
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GINConv, global_add_pool
from torch_geometric.data import Data
from numpy.typing import NDArray

class GraphPairBaseline(nn.Module):
    def __init__(self, hidden_dim=32, num_layers=3):
        super().__init__()
        self.convs = nn.ModuleList()
        for i in range(num_layers):
            mlp = nn.Sequential(
                nn.Linear(hidden_dim if i>0 else 1, hidden_dim),
                nn.ReLU(),
                nn.Linear(hidden_dim, hidden_dim)
            )
            self.convs.append(GINConv(mlp))
        
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim*2, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )

    def encode(self, x, edge_index):
        for conv in self.convs:
            x = conv(x, edge_index)
            x = F.relu(x)
        return global_add_pool(x, torch.zeros(x.size(0), dtype=torch.long))  # graph embedding

    def forward(self, x_G, edge_index_G, x_H, edge_index_H):
        h_G = self.encode(x_G, edge_index_G)
        h_H = self.encode(x_H, edge_index_H)
        combined = torch.cat([h_G, h_H], dim=1)
        out = self.classifier(combined)
        return torch.sigmoid(out)  # probability


def adj_mat_to_edge_list(adj_mat):
    for row in graph:
        for elem in graph:
            if elem == 1:
                if (elem, row) not in edge_tuples:
                    edge_tuples.append((row, elem))
    for (u,v) in edge_tuples:
        graph_edge_index[0].append(u)
        graph_edge_index[1].append(v)
    return torch.tensor(graph_edge_index, dtype=torch.long)
def run_gnn_baseline(graph: NDArray, subgraph: NDArray) -> bool:
    graph_edge_index = adj_mat_to_edge_list(graph)
    X_graph = graph.shape[0]
    subgraph_edge_index = adj_mat_to_edge_list(subgraph)
    X_subgraph = subgraph.shape[0]
    model = GraphPairBaseline()
    prob = model(X_graph, graph_edge_index, X_subgraph, subgraph_edge_index)

    return prob > 0.5
