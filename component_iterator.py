#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
from read_csv import read_as_array as read


def components(path_nodes, path_edges, delimiter="\t"):
	"""
	Iterates over the connected components of a graph
	given by two files containing nodes and edges.

	This method loads the complete data set into
	memory and then yields networkx graphs containing
	connected components.
	"""
	nodes = [row for row in read(path_nodes, delimiter)]
	edges = [row for row in read(path_edges, delimiter)]
	partition_nodes = {}
	for counter, row in enumerate(nodes):
		component_id = int(row[1])
		if component_id in partition_nodes:
			partition_nodes[component_id].append(counter)
		else:
			partition_nodes[component_id] = [counter]
	partition_edges = {}
	for counter, row in enumerate(edges):
		component_id = int(row[2])
		if component_id in partition_edges:
			partition_edges[component_id].append(counter)
		else:
			partition_edges[component_id] = [counter]
	for key in partition_nodes:
		graph = nx.Graph()
		for node_index in partition_nodes[key]:
			data = nodes[node_index]
			graph.add_node(int(data[0]), nodeType=data[-2], name=data[-1])
		for edge_index in partition_edges[key]:
			data = edges[edge_index]
			graph.add_edge(int(data[0]), int(data[1]), linkType=data[-2], linkName=data[-1])
		yield graph
	del nodes
	del edges
	del partition_nodes
	del partition_edges
