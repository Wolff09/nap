#!/usr/bin/env python
# -*- coding: utf-8 -*-

def merge(node_file, edge_file, output_file, components):
	node_file.seek(0)
	edge_file.seek(0)
	for file, type in ((node_file, 'n'), (edge_file, 'e')):
		for line in file:
			output_file.write("%s\t%s\t%s\n" % (components[get_id(line)], type, line.strip()))

def get_id(line):
	first_delimiter = line.find("\t")
	return int(line[0:first_delimiter])