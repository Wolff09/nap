#!/usr/bin/env python
# -*- coding: utf-8 -*-

from union_find import make_sets, find, union
from progress import StatusBar

PATH_COMPRESSION = 500000 # beat (without): 0:14:46.256371

def compute(nodes, edges):
	parents = make_sets(len(nodes))

	bar = StatusBar(len(edges))
	counter = 0
	for line in edges:
		if line:
			first_delimiter = line.find("\t")
			second_delimiter = line.find("\t", first_delimiter + 1)
			left = int(line[:first_delimiter])
			right = int(line[first_delimiter:second_delimiter])
			union(parents, left, right)
		counter += 1
		if counter % 5000 == 0: bar.update(counter)
		if counter % PATH_COMPRESSION == 0:
			for i, x in enumerate(parents):
				parents[i] = find(parents, x)

	bar.close()
	bar = StatusBar(len(parents))
	for counter, x in enumerate(parents):
		parents[counter] = find(parents, x)
		if counter % 10000 == 0: bar.update(counter)
	bar.close()
	return parents