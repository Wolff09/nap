#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import various_artists, connected_components, merge

VARIOUS_ARTISTS_ID = -1
HEADER = "pid\ttype\tdata\n"

def process_data(path_to_nodes, path_to_edges, path_to_output, various_artist_id=VARIOUS_ARTISTS_ID):
	"""
	Process the given data to be able to use the graph structure
	with networkx while not allocating over 9000MB of RAM.

	The data undergoes the following steps.
		Step 1: delete node "various artists"
		Step 2: delete edges adjacent to "various artists" node
		Step 3: find connected components
		Step 4: merge files and add connected component id
		Step 5: sort files
		Step 6: output to file
	"""

	# TODO: more memory releasable?
	# TODO: more time optimization?
	# TODO: progressbar ftw: http://code.google.com/p/python-progressbar/

	def read_lines(path):
		with open(path) as file:
			file.readline() # drop header
			lines = file.readlines()
			if not lines[-1].endswith("\n"):
				lines[-1] += "\n"
			return lines
	nodes = read_lines(path_to_nodes)
	edges = read_lines(path_to_edges)

	# Step 1 and 2
	print ">>> Deleting 'Various Artists'..."
	various_artists.delete(nodes, edges, various_artist_id)

	# Step 3
	print ">>> Searching for connected components..."
	components = connected_components.compute(nodes, edges)

	# Step 4
	print ">>> Merging nodes and edges..."
	merged = merge.merge(nodes, edges, components)
	del nodes
	del edges

	# Step 5 and 6
	print ">>> Sorting according to connected components..."
	merged.sort()

	# Write to file
	print ">>> Writing to file..."
	with open(path_to_output, "w") as file:
		file.write(HEADER)
		for line in merged:
			file.write(line)
		file.close()
	del merged

	print ">>> Jobs Done!"
