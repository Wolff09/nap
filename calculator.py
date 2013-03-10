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

def calculate(path):
	counter = 0
	for graph in iterator.components(path):
		pid = graph.graph["pid"]
		# Because networkx sucks
		if graph.number_of_edges() == 0:
			part = Partition(pid=pid, diameter=0, num_nodes=graph.number_of_nodes(), density=nx.density(graph))
			Node.create(nid=int(graph.nodes()[0]), pid=pid, degree=0, closeness=0, eccentricity=0, betweenness=0)
			continue
		else:
			part = Partition(pid=pid, diameter=nx.diameter(graph), num_nodes=graph.number_of_nodes(), density=nx.density(graph))

		part.save()

		degree = sc.degree_centrality(graph)
		close = sc.closeness_centrality(graph)
		between = sc.betweenness_centrality(graph)
		ecc = sc.eccentricity(graph)
		for node in graph.nodes():
			n = Node(nid=int(node),  pid=pid, degree=degree[node], closeness=close[node], eccentricity=1/ecc[node], betweenness=between[node])
			n.save()
		counter += 1
		if counter % 1000 == 0:
			print counter

