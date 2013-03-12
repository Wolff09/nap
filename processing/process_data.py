#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import various_artists, connected_components, merge
from progress import StatusBar
from datetime import datetime, timedelta

HEADER = "pid\ttype\tdata\n"

def process_data(path_to_nodes, path_to_edges, path_to_output, *deletion_names):
	"""
	Process the given data to be able to use the graph structure
	with networkx while not allocating over 9000MB of RAM.

	The nodes of the input data must have continuous ids.
	Furthermore, artist entries are expected to not end with
	a \t. Otherwise an entry which should be deleted might not
	be deleted.

	The data undergoes the following steps.
		Step 1: read data into memory
		Step 2: delete nodes that match a given name
		Step 3: delete edges adjacent to nodes deleted in Step 2
		Step 4: find connected components
		Step 5: merge nodes and edges
		Step 6: sort
		Step 7: output to file
	"""
	begin = datetime.now()

	# Step 1
	def read_lines(path, approx=10000000):
		bar = StatusBar(approx)
		lines = []
		counter = 0
		with open(path) as file:
			file.readline() # drop header
			for line in file:
				lines.append(line)
				counter += 1
				if counter % 10000 == 0: bar.update(counter)
			if not lines[-1].endswith("\n"):
				lines[-1] += "\n"
		bar.close()
		return lines
	print ">>> Reading nodes and edges..."
	nodes = read_lines(path_to_nodes, approx=10000000)
	edges = read_lines(path_to_edges, approx=27000000)

	# Step 2 and 3
	if deletion_names:
		print ">>> Searching ids voted for deletion..."
		deletion_ids = various_artists.find_ids(nodes, *deletion_names)
		print ">>> Deleting nodes and edges..."
		various_artists.delete(nodes, edges, *deletion_ids)

	# Step 4
	print ">>> Searching for connected components..."
	components = connected_components.compute(nodes, edges)

	# Step 5
	print ">>> Merging nodes and edges..."
	merged = merge.merge(nodes, edges, components)
	del nodes
	del edges

	# Step 6
	print ">>> Sorting according to connected components..."
	merged.sort()

	# Step 7
	print ">>> Writing to file..."
	bar = StatusBar(len(merged))
	counter = 0
	with open(path_to_output, "w") as file:
		file.write(HEADER)
		for line in merged:
			file.write(line)
			counter += 1
			if counter % 10000 == 0: bar.update(counter)
		file.close()
	bar.close()

	# say goodbye
	diff = datetime.now() - begin
	print ">>> Jobs Done! [%s]" % str(timedelta(seconds=int(diff.total_seconds())))
