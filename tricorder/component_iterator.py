#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
from read_csv import read_as_array as read


def components(path_merge, delimiter="\t"):
	"""
	Generator for iterating over connected components of
	the musicbrainz graph.

	Each graph contains the pid of the connected component.
	"""
	current_graph = None
	current_pid = -1
	for row in read(path_merge):
		pid = int(row[0])
		if pid != current_pid:
			if current_graph:
				yield current_graph
			current_pid = pid
			current_graph = nx.Graph(pid=current_pid)
		add_to_graph(current_graph, row[1], row[2])

def add_to_graph(graph, type, data, delimiter="\t"):
	if type == "n":
		parsed = parse(data, 5, delimiter)
		graph.add_node(int(parsed[0]), type=parsed[3], name=parsed[4])
	elif type == "e":
		parsed = parse(data, 4, delimiter)
		graph.add_edge(int(parsed[0]), int(parsed[1]), type=int(parsed[2]), name=parsed[3])

def parse(data, length, delimiter):
	return data.strip().split(delimiter, length)