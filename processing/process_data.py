#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tempfile import NamedTemporaryFile as TemporaryFile
from various_artists import delete_node, delete_adjacent_edges
from connected_components import find_connected_components
from merge import merge

VARIOUS_ARTISTS_ID = -1

def process_data(path_to_nodes, path_to_edges, path_to_output):
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

	tmp_nodes = TemporaryFile(mode="r+w")
	tmp_edges = TemporaryFile(mode="r+w")
	tmp_merge = TemporaryFile(mode="r+w")

	# Step 1 and 2
	print ">>> Deleting 'Various Artists'"
	with open(path_to_nodes, "r") as nodes_file, open(path_to_edges, "r") as edges_file:
		delete_node(nodes_file, tmp_nodes, VARIOUS_ARTISTS_ID)
		delete_adjacent_edges(edges_file, tmp_edges, VARIOUS_ARTISTS_ID)
		nodes_file.close()
		edges_file.close()

	# Step 3
	print ">>> Searching for connected components"
	tmp_nodes.flush()
	tmp_edges.flush()
	components = find_connected_components(tmp_nodes, tmp_edges)

	# Step 4
	print ">>> Merging nodes and edges into one file"
	merge(tmp_nodes, tmp_edges, tmp_merge, components)
	tmp_nodes.close()
	tmp_edges.close()

	# Step 5 and 6
	print ">>> Sorting according to partition"
	tmp_merge.flush()
	sort_cmd = "cat %s | sort -k 2 -n > %s" % (tmp_merge.name, path_to_output)
	os.system(sort_cmd)

	# Clean up
	tmp_merge.close()
	print ">>> No header written..."
	print ">>> Jobs Done!"
