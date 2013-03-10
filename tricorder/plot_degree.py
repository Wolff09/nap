#!/usr/bin/env python
# -*- coding: utf-8 -*-

from read_csv import read_as_array as read
from collections import Counter
from pylab import *

PATH_TO_NODES = "private_data/musicbrainzGraph/musicbrainzNodes.csv"
PATH_TO_EDGES = "private_data/musicbrainzGraph/musicbrainzRelations.csv"

BARRIER_READ_NODES = 500000
BARRIER_READ_EDGES = 500000

def main():
	print ">>> Reading nodes..."
	number_of_nodes = 0
	for data in read(PATH_TO_NODES):
		number_of_nodes += 1
		if number_of_nodes % BARRIER_READ_NODES == 0: print "     - %s nodes read" % number_of_nodes
	print ">>> Number of nodes: %s" %number_of_nodes

	print "\n>>> Reading edges..."
	degrees = [0 for i in range(number_of_nodes)]
	number_of_edges = 0
	for data in read("private_data/musicbrainzGraph/musicbrainzRelations.csv"):
		degrees[int(data[0])] += 1
		degrees[int(data[1])] += 1
		number_of_edges += 1
		if number_of_edges % BARRIER_READ_EDGES == 0: print "     - %s edges read" % number_of_edges
	print ">>> Number of edges: %s" % number_of_edges

	print "\n>>> Calculating degree distribution"
	degree_distribution = Counter(degrees) # dict: {degree: number_of_nodes_with_that_degree }
	# print str(degree_distribution).replace(",", ",\n")

	print ">>> Plotting degree distribution"
	bar_graph(degree_distribution, name='Degree Distribution')

def bar_graph(name_value_dict, name='', show_output=True, output=False, output_name=None):
	#taken from: http://www.goldb.org/goldblog/2007/03/23/PythonCreatingBarGraphsWithMatplotlib.aspx
    figure(figsize=(16, 8)) # image dimensions   
    title(name, size='x-small')
    
    # add bars
    for i, key in zip(range(len(name_value_dict)), name_value_dict.keys()):
        bar(i + 0.25 , name_value_dict[key], color='red')
    
    # axis setup
    xticks(arange(0.65, len(name_value_dict)), 
        [('%s: %d' % (name, value)) for name, value in 
        zip(name_value_dict.keys(), name_value_dict.values())], 
        size='xx-small')
    max_value = max(name_value_dict.values())
    tick_range = arange(0, max_value, (max_value / 7))
    yticks(tick_range, size='xx-small')
    formatter = FixedFormatter([str(x) for x in tick_range])
    gca().yaxis.set_major_formatter(formatter)
    gca().yaxis.grid(which='major') 
    
    if output and output_name:
		savefig(output_name)
    if show_output:
		show()

if __name__ == '__main__':
	main()