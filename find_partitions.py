#!/usr/bin/env python
# -*- coding: utf-8 -*-

from read_csv import read_as_array as read
from union_find import *
import os, shutil
from collections import Counter


# configuration
# PATH_TO_NODES = "private_data/musicbrainzGraph/musicbrainzNodes.csv"
# PATH_TO_EDGES = "private_data/musicbrainzGraph/musicbrainzRelations.csv"
# PATH_TO_OUTPUT_NODES = "private_data/musicbrainzGraph/nodes.csv"
# PATH_TO_OUTPUT_EDGES = "private_data/musicbrainzGraph/edges.csv"
# test configuration
PATH_TO_NODES = "public_data/find_partitions_test/nodes.csv"
PATH_TO_EDGES = "public_data/find_partitions_test/edges.csv"
PATH_TO_OUTPUT_NODES = "public_data/find_partitions_test/output_nodes"
PATH_TO_OUTPUT_EDGES = "public_data/find_partitions_test/output_edges"


# How talky shall I be ?
BARRIER_NODE_READING = 1000000
BARRIER_OBJECT_CREATION = 500000
BARRIER_MAKING_SETS = 500000
BARRIER_EDGE_READING = 400000
BARRIER_NODE_WRITING = 200000
BARRIER_EDGE_WRITING = 200000


def main(length=0):
	######################### print current configuration ##########################
	print ">>> I am finding your partitions!"
	print ">>> nodes: %s" % PATH_TO_NODES
	print ">>> edges: %s" % PATH_TO_EDGES
	print ">>> output nodes: %s" % PATH_TO_OUTPUT_NODES
	print ">>> output edges: %s" % PATH_TO_OUTPUT_EDGES
	print "---------------------------------------------------------------------\n"


	##################### find number of nodes if not provided #####################
	if length == 0:
		print "\n>>> Starting to read nodes..."
		for data in read(PATH_TO_NODES):
			length += 1
			if length % BARRIER_NODE_READING == 0: print "     - %s" % length
	print "Number of Nodes: %s" % length
	

	######################### creating UnionFind structure #########################
	print "\n>>> Creating UnionFind Nodes..."
	nodes = [i for i in range(0, length)] # create array of length length
	for i in range(0, length):
		nodes[i] = Node(i)
		if i+1 % BARRIER_OBJECT_CREATION == 0: print "     - %s" % i

	print "\n>>> Making Initial UnionFind Sets..."
	counter = 0
	for node in nodes:
		MakeSet(node)
		counter += 1
		if counter % BARRIER_MAKING_SETS == 0: print "     - %s" % counter


	##################### merge partitions according to edges ######################
	counter = 0
	print "\n>>> Starting to read edges..."
	for data in read(PATH_TO_EDGES):
		left = nodes[int(data[0])]
		right = nodes[int(data[1])]
		Union(left, right)
		counter += 1
		if counter % BARRIER_EDGE_READING == 0: print "     - %s" % counter
	print "Number of edges: %s" % counter

	
	############################ search for partitions #############################
	print "\n>>> Searching for partitions..."
	parents = [Find(node).id for node in nodes]

	
	############################ writing new node file #############################
	print "\n>>> Writing partitions to nodes..."
	counter = 0
	with open(PATH_TO_OUTPUT_NODES, "w") as file:
		for data in read(PATH_TO_NODES):
			node_id = int(data[0])
			partition_id = parents[node_id]
			new_data = "%s\t%s\t%s\n" % (node_id, partition_id, "\t".join(data[1:]))
			file.write(new_data)
			counter += 1
			if counter % BARRIER_NODE_WRITING == 0: print "     - %s" % counter
		file.close()
	print ">>> Note: I did not wrote a header to the file (column 2 is the partition id)."


	############################ writing new edge file #############################
	print "\n>>> Writing partitions to edges..."
	counter = 0
	with open(PATH_TO_OUTPUT_EDGES, "w") as file:
		for data in read(PATH_TO_EDGES):
			node_left = int(data[0])
			partition_id = parents[node_left]
			new_data = "%s\t%s\t%s\t%s\n" % (node_left, data[1], partition_id, "\t".join(data[2:]))
			file.write(new_data)
			counter += 1
			if counter % BARRIER_EDGE_WRITING == 0: print "     - %s" % counter
		file.close()
	print ">>> Note: I did not wrote a header to the file (column 3 is the partition id)."


	################# statistical information about the partitions #################
	print "\n>>> Statistical Information..."
	count_parents = Counter(parents)
	print "Number of Partitions: %s" % len(count_parents)
	print "PartitionId x PartitionSize: \n     - %s" % str(count_parents).replace(",", ",\n               ")
	count_size = Counter(count_parents.values())
	print "PartitionSize x NumberOfOccurrences: \n     - %s" % str(count_size).replace(",", ",\n               ")



if __name__ == '__main__':
	import sys
	if len(sys.argv) > 1 and sys.argv[1] == "-i":
		# we know that there are 9909276 nodes
		main(9909276)
	else:
		main()