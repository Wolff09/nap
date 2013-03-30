#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx

def read(path_merge):
	with open(path_merge, 'r') as file:
		file.readline() # pop header
		for row in file:
			yield row.split('\t', 6)

def components(path_merge):
	"""
	Generator for iterating over connected components of
	the musicbrainz graph.

	Each graph contains the pid of the connected component.
	Nodes do have a `type` and a `name` attribute. Edges
	do not have any attributes.
	"""
	current_graph = None
	current_pid = -1
	for data in read(path_merge):
		pid = int(data[0])
		if pid != current_pid:
			if current_graph:
				yield current_graph
			current_pid = pid
			current_graph = nx.Graph(pid=current_pid)
		add_to_graph(current_graph, data)
	yield current_graph

def add_to_graph(graph, data):
	if data[1] == 'n':
		graph.add_node(int(data[2]), type=data[5], name=data[6].strip())
	else: # data[1] == 'e'
		graph.add_edge(int(data[2]), int(data[3])) # type=int(data[4]), name=' '.join(data[5:])