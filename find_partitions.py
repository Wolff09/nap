#!/usr/bin/env python
# -*- coding: utf-8 -*-

from read_csv import read_as_array as read
from union_find import *

# configuration
PATH_TO_NODES = "private_data/musicbrainzGraph/musicbrainzNodes.csv"
PATH_TO_EDGES = "private_data/musicbrainzGraph/musicbrainzRelations.csv"

# How talky shall I be ?
BARRIER_NODE_READING = 1000000
BARRIER_OBJECT_CREATION = 500000
BARRIER_MAKING_SETS = 500000
BARRIER_EDGE_READING = 200000

def main(length=0):
	##################### find number of nodes if not provided #####################
	if length == 0:
		print "Starting to read nodes..."
		for data in read(PATH_TO_NODES):
			length += 1
			if length % BARRIER_NODE_READING == 0: print "...reading nodes (%s)" % length
		print "Number of Nodes: %s" % length
	

	######################### creating UnionFind structure #########################
	print "%sCreating UninoFind Nodes..." % ("" if length > 0 else "\n")
	nodes = [i for i in range(0, length)] # create array of length length
	for i in range(0, length):
		nodes[i] = Node(i)
		if i % BARRIER_OBJECT_CREATION == 0: print "...creating Nodes (%s)" % i

	print "\nMaking Initial UnionFind Sets..."
	counter = 0
	for node in nodes:
		MakeSet(node)
		counter += 1
		if counter % BARRIER_MAKING_SETS == 0: print "...making Sets (%s)" % counter


	##################### merge partitions according to edges ######################
	counter = 0
	print "\nStarting to read edges..."
	for data in read(PATH_TO_EDGES):
		left = nodes[int(data[0])]
		right = nodes[int(data[1])]
		Union(left, right)
		counter += 1
		if counter % BARRIER_EDGE_READING == 0: print "...reading edges (%s)" % counter

	
	########################## find remaining partitions ###########################
	del nodes # release memory
	print "\nSearching for partitions..."
	sets = [Find(node) for node in nodes]
	remaining = []
	for p in sets:
		if not p in remaining:
			remaining += [p]
	print "Number of Partitions: %s" % len(remaining)
	print "Partitions (id of one contained node): %s" % remaining


if __name__ == '__main__':
	# it seems as if there are 9909276 nodes
	# number_of_nodes = 9909276
	number_of_nodes = 2309276
	import sys
	if len(sys.argv) > 1 and sys.argv[1] == "-i":
		# use initial knowledge
		main(number_of_nodes)
	else:
		main()