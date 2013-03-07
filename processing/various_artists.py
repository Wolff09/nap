#!/usr/bin/env python
# -*- coding: utf-8 -*-

def delete_node(node_file, tmp_file, various_artists_id):
	# TODO: continuous ids!
	search_string = "%s\t" % various_artists_id
	node_file.readline() # kill header
	new_id = 0
	for line in node_file:
		if not line.startswith(search_string):
			first_delimiter = line.find("\t")
			tmp_file.write("%s\t%s" % (new_id, line[first_delimiter+1:]))
			new_id += 1

def delete_adjacent_edges(edge_file, tmp_file, various_artists_id):
	search_string = "%s\t" % various_artists_id
	edge_file.readline() # kill header
	for line in edge_file:
		first_delimiter = line.find("\t")
		if not line.startswith(search_string) and not line.startswith(search_string, first_delimiter):
			tmp_file.write(line)