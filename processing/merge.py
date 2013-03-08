#!/usr/bin/env python
# -*- coding: utf-8 -*-


def merge(nodes, edges, components):
	merged = []
	for list, type in ((nodes, 'n'), (edges, 'e')):
		while list:
			line = list.pop() # modify input list to reduce memory consumption
			merged.append("%s\t%s\t%s" % (components[get_id(line)], type, line))
	return merged

def get_id(line):
	first_delimiter = line.find("\t")
	return int(line[:first_delimiter])