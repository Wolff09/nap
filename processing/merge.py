#!/usr/bin/env python
# -*- coding: utf-8 -*-

from progress import StatusBar

def merge(nodes, edges, components):
	merged = []
	for list, type in ((nodes, 'n'), (edges, 'e')):
		bar = StatusBar(len(list))
		counter = 0
		while list:
			line = list.pop() # modify input list to reduce memory consumption
			if line:
				merged.append("%s\t%s\t%s" % (components[get_id(line)], type, line))
			counter += 1
			if counter % 10000 == 0: bar.update(counter)
		bar.close()
	return merged

def get_id(line):
	first_delimiter = line.find("\t")
	return int(line[:first_delimiter])