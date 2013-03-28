from models import Partition, Node
import component_iterator as iterator
import shortcuts as sc
import networkx as nx

def get_top_artists(path):
	with open(path, "r") as file:
		return set([a for a in file.read().split("\r")])

def calculate(path_data, path_artists, talky=False):
	"""
	Reads all connected components from the given dataset and computes the
	following measures:
		- size (number of nodes)
		- diameter
		- density
		- degree
		- closeness_centrality
		- betweenness_centrality
		- eccentricity

	The first three measures are computed for each connected component.
	The remaining ones are computed for each node.

	The result is written to a database (see tricorder.models).
	Note: the database must exists but needs to be empty (should be empty).
	"""
	top_artists = get_top_artists(path_artists)
	for i, graph in enumerate(iterator.components(path_data)):
		is_real_graph = graph.number_of_edges() > 0
		num_artists = 0
		num_top_artists = 0

		# calculate measures (only if we have edges!)
		density = nx.density(graph) if is_real_graph else 0
		diameter = nx.diameter(graph) if is_real_graph else 0
		degree = sc.degree_centrality(graph) if is_real_graph else {}
		closeness = sc.closeness_centrality(graph) if is_real_graph else {}
		betweenness = sc.betweenness_centrality(graph) if is_real_graph else {}
		eccentricity = sc.eccentricity(graph) if is_real_graph else {}

		# create Node DB entries
		for id, attrs in graph.node.items():
			if attrs['type'] == 'artist':
				num_artists += 1
				if attrs['name'] in top_artists:
					num_top_artists += 1
			ecc = 1/eccentricity[id] if id in eccentricity else 0 # need an extra variable here since division by zero is evil
			Node.create(nid=int(id), pid=graph.graph['pid'], node_type=attrs["type"],
				name=attrs["name"], degree=degree.get(id, 0), closeness=closeness.get(id, 0),
				eccentricity=ecc, betweenness=betweenness.get(id, 0))

		# create Partition DB entry
		Partition.create(pid=graph.graph['pid'], diameter=diameter,
			num_nodes=graph.number_of_nodes(), num_edges=graph.number_of_edges(),
			num_artists=num_artists, num_top_artists=num_top_artists, density=density)

		if talky and i % 500 == 0: print i
