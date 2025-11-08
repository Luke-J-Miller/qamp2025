# Twitter Interaction Network for the US Congress (2023)

## Usage

This folder contains the following comma separated text files 

- n: total number of nodes = 475
- m: total number of edges = 13,289
- N: number of graphs = 50

	(1) 	SNAP_A.txt (m lines) 
	sparse (block diagonal) adjacency matrix for all graphs,
	each line corresponds to (row, col) resp. (node_id, node_id)

	(2) 	SNAP_graph_indicator.txt (n lines)
	column vector of graph identifiers for all nodes of all graphs,
	the value in the i-th line is the graph_id of the node with node_id i

	(3) 	SNAP_graph_labels.txt (N lines) 
	class labels for all graphs in the dataset,
	the value in the i-th line is the class label of the graph with graph_id i

	(4) 	SNAP_node_labels.txt (n lines)
	column vector of node labels,
	the value in the i-th line corresponds to the node with node_id i

There are OPTIONAL files if the respective information is available:

	(5) 	SNAP_edge_labels.txt (m lines; same size as SNAP_A_sparse.txt)
	labels for the edges in SNAP_A_sparse.txt 

	(6) 	SNAP_edge_attributes.txt (m lines; same size as SNAP_A.txt)
	attributes for the edges in SNAP_A.txt 

	(7) 	SNAP_node_attributes.txt (n lines) 
	matrix of node attributes,
	the comma seperated values in the i-th line is the attribute vector of the node with node_id i

	(8) 	SNAP_graph_attributes.txt (N lines) 
	regression values for all graphs in the dataset,
	the value in the i-th line is the attribute of the graph with graph_id i

## Description of the dataset

This network represents the Twitter interaction network for the 117th United States Congress, both House of Representatives and Senate. The base data was collected via the Twitter’s API, then the empirical transmission probabilities were quantified according to the fraction of times one member retweeted, quote tweeted, replied to, or mentioned another member’s tweet.

## References

- C.G. Fink, N. Omodt, S. Zinnecker, and G. Sprint: A Congressional Twitter network dataset quantifying pairwise probability of influence. Data in Brief, 2023.

- C.G. Fink, K. Fullin, G. Gutierrez, N. Omodt, S. Zinnecker, G. Sprint, and S. McCulloch: A centrality measure for quantifying spread on weighted, directed networks. Physica A, 2023.
