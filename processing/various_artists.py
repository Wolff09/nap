#!/usr/bin/env python
# -*- coding: utf-8 -*-

from progress import StatusBar

def delete(nodes, edges, various_artists_id):
	""" assumes: no self loops """
	bar = StatusBar(len(edges))
	if various_artists_id < 0 or various_artists_id >= len(nodes):
		return
	# swap various_artists to the end of the nodes and delete it
	nodes[various_artists_id] = nodes[-1]
	del nodes[-1]
	# due to swapping nodes[various_artists_id] has the wrong id now
	first_delimiter = nodes[various_artists_id].find("\t")
	old_id = nodes[various_artists_id][:first_delimiter]
	nodes[various_artists_id] = str(various_artists_id) + nodes[various_artists_id][first_delimiter:]
	# all edges with various_artists_id have to be deleted
	search_string_del = "%s\t" % various_artists_id
	search_string_rename = "%s\t" % old_id
	delete_indices = []
	for index, line in enumerate(edges):
		first_delimiter = line.find("\t")
		# search for edges that want to be deleted
		if line.startswith(search_string_del) or line.startswith(search_string_del, first_delimiter + 1):
			delete_indices.append(index)
		# edges adjacent to the swapped node need the new id
		elif line.startswith(search_string_rename) or line.startswith(search_string_rename, first_delimiter + 1):
			edges[index] = edges[index].replace(search_string_rename, search_string_del, 1)
		if index % 10000 == 0: bar.update(index)
	# we have to delete the last index first, otherwise all indexes are compromised after deleting the very first
	bar.close()
	bar = StatusBar(len(delete_indices))
	delete_indices.sort(reverse=True)
	for i, index in enumerate(delete_indices):
		del edges[index]
		if i % 100 == 0: bar.update(i)
	bar.close()