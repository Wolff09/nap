#!/usr/bin/env python
# -*- coding: utf-8 -*-

from progress import StatusBar
import re

def find_ids(nodes, *args):
	if not args:
		return [-1]
	bar = StatusBar(len(nodes))
	regex = re.compile(r'.*?\tartist\t(%s)' % '|'.join(args), re.IGNORECASE)
	ids = []
	for index, row in enumerate(nodes):
		if regex.match(row):
			ids.append(index)
		if index % 10000 == 0: bar.update(index)
	bar.close()
	return ids

def delete(nodes, edges, *deletion_indices):
	bar = StatusBar(len(deletion_indices))
	for i, index in enumerate(deletion_indices):
		nodes[index] = None
		if i % 100 == 0: bar.update(i)
	bar.close()
	bar = StatusBar(len(edges))
	# TODO: use a set for deletion_indices for constant time in lookupo
	for i, row in enumerate(edges):
		data = row.split("\t", 2)
		left = int(data[0])
		right = int(data[1])
		if left in deletion_indices or right in deletion_indices:
			edges[i] = None
		if i % 10000 == 0: bar.update(i)
	bar.close()

#def delete(nodes, edges, deletion_id):
#	""" assumes: no self loops """
#	bar = StatusBar(len(edges))
#	if deletion_id < 0 or deletion_id >= len(nodes):
#		return
#	# swap various_artists to the end of the nodes and delete it
#	nodes[deletion_id] = nodes[-1]
#	del nodes[-1]
#	# due to swapping nodes[deletion_id] has the wrong id now
#	first_delimiter = nodes[deletion_id].find("\t")
#	old_id = nodes[deletion_id][:first_delimiter]
#	nodes[deletion_id] = str(deletion_id) + nodes[deletion_id][first_delimiter:]
#	# all edges with deletion_id have to be deleted
#	search_string_del = "%s\t" % deletion_id
#	search_string_rename = "%s\t" % old_id
#	delete_indices = []
#	for index, line in enumerate(edges):
#		first_delimiter = line.find("\t")
#		# search for edges that want to be deleted
#		if line.startswith(search_string_del) or line.startswith(search_string_del, first_delimiter + 1):
#			delete_indices.append(index)
#		# edges adjacent to the swapped node need the new id
#		elif line.startswith(search_string_rename) or line.startswith(search_string_rename, first_delimiter + 1):
#			edges[index] = edges[index].replace(search_string_rename, search_string_del, 1)
#		if index % 10000 == 0: bar.update(index)
#	bar.close()
#	# remove edge strings
#	bar = StatusBar(len(delete_indices))
#	for i, index in enumerate(delete_indices):
#		edges[index] = None
#		if i % 50 == 0: bar.update(i)
#	bar.close()
#	# remove None objects from list
#	bar = StatusBar(len(edges))
#	def edge_with_update(i, edge, bar):
#		if i % 10000 == 0: bar.update(i)
#		return edge
#	edges[:] = [edge_with_update(i, edge, bar) for i, edge in enumerate(edges) if edge]
#	bar.close()
