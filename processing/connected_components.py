#!/usr/bin/env python
# -*- coding: utf-8 -*-

from union_find import *

def find_connected_components(node_file, edge_file):
	node_file.seek(0)
	edge_file.seek(0)

	length = 0
	for line in node_file:
		length += 1
	
	# create UnionFind structure
	nodes = [Node(i) for i in range(0, length)]
	for node in nodes:
		MakeSet(node)

	# merge according to edges
	for line in edge_file:
		first_delimiter = line.find("\t")
		second_delimiter = line.find("\t", first_delimiter + 1)
		left = nodes[int(line[0:first_delimiter])]
		right = nodes[int(line[first_delimiter:second_delimiter])]
		Union(left, right)
	
	# return dict with: node_id x partition_id
	parents = [Find(node).id for node in nodes]
	return parents
