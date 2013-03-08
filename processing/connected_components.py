#!/usr/bin/env python
# -*- coding: utf-8 -*-

from union_find import make_sets, find, union

def compute(nodes, edges):
	parents = make_sets(len(nodes))

	counter = 0
	for line in edges:
		first_delimiter = line.find("\t")
		second_delimiter = line.find("\t", first_delimiter + 1)
		left = int(line[:first_delimiter])
		right = int(line[first_delimiter:second_delimiter])
		union(parents, left, right)
		counter += 1
		if counter % 100000 == 0: print counter

	# TODO: can we really do this in place?
	# find the root of every node
	for counter, x in enumerate(parents):
		parents[counter] = find(parents, x)
	return parents