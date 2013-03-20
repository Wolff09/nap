""" 
Iterates over all connected components and calculates basic measures such as: 
	-size (in Nodes)
	-diameter
	-density
And for every node:
	-degree
	-closeness centrality
	-betweenness centrality
	-eccentricity centrality
"""

from models import Partition, Node
import component_iterator as iterator
import shortcuts as sc
import networkx as nx

def get_top_artists(path):
	with open(path, "r") as file:
		return set([a for a in file.read().split("\r")])

def calculate(merged, tops):
	counter = 0
	top_artists = get_top_artists(tops)
	for graph in iterator.components(merged):
		pid = graph.graph["pid"]
		artists = 0
		num_top_artists = 0
		# Because networkx sucks
		if graph.number_of_edges() == 0:
			nid = graph.nodes()[0]
			if graph.node[nid]["type"] == "artist":
				artists = 1
				if graph.node[nid]["name"] in top_artists:
					num_top_artists = 1
			part = Partition(pid=pid, diameter=0, num_nodes=graph.number_of_nodes(), num_edges=graph.number_of_edges, num_artists=artists, num_top_artists=num_top_artists, density=nx.density(graph))
			Node.create(nid=int(nid), pid=pid, name=graph.node[nid]["name"], node_type=graph.node[nid]["type"] ,degree=0, closeness=0, eccentricity=0, betweenness=0)
			continue
		else:
			degree = sc.degree_centrality(graph)
			close = sc.closeness_centrality(graph)
			between = sc.betweenness_centrality(graph)
			ecc = sc.eccentricity(graph)
			for key, attr in graph.node.items():
				if attr["type"] == "artist":
					artists += 1
					if attr["name"] in top_artists:
						num_top_artists += 1
				n = Node(nid=key,  pid=pid, node_type=attr["type"], name=attr["name"], degree=degree[key], closeness=close[key], eccentricity=1/ecc[key], betweenness=between[key])
				n.save()
			part = Partition(pid=pid, diameter=nx.diameter(graph), num_nodes=graph.number_of_nodes(), num_edges=graph.number_of_edges(), num_artist=artists, num_top_artists=num_top_artists, density=nx.density(graph))

		part.save()

		counter += 1
		if counter % 1000 == 0:
			print counter

