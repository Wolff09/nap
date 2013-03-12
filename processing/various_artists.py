#!/usr/bin/env python
# -*- coding: utf-8 -*-

from progress import StatusBar
import re

def find_ids(nodes, *args):
	if not args:
		return [-1]
	bar = StatusBar(len(nodes))
	regex = re.compile(r'^.*?\tartist\t(%s)\n' % '|'.join(args), re.IGNORECASE)
	ids = []
	for index, row in enumerate(nodes):
		if regex.match(row):
			ids.append(index)
		if index % 10000 == 0: bar.update(index)
	bar.close()
	return ids

def delete(nodes, edges, *deletion_indices):
	from datetime import datetime
	for index in deletion_indices:
		nodes[index] = None
	bar = StatusBar(len(edges))
	deletion_indices = set(deletion_indices) # set for constant time 'in' check
	for i, row in enumerate(edges):
		data = row.split("\t", 2)
		left = int(data[0])
		right = int(data[1])
		if left in deletion_indices or right in deletion_indices:
			edges[i] = None
		if i % 10000 == 0: bar.update(i)
	bar.close()