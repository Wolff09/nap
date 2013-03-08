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
import shortcuts

def calculate(path):
	counter = 0
	for graph in iterator.components(path):
		pid = graph.Graph["pid"]
		part = Partition(pid, diameter(graph), graph.number_of_nodes(), nx.density(graph))
		part.save()

		degree = degree_centrality(graph)
		close = closeness_centrality(graph)
		between = betweenness_centrality(graph)
		ecc = eccentricity(graph)
		for node in graph.nodes():
			n = Node(int(node),  pid, degree[node], close[node], 1/ecc[node], between[node])
			n.save()
		counter += 1
		if counter % 1000 == 0:
			print counter

