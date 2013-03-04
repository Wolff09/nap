#!/usr/bin/env python
# -*- coding: utf-8 -*-

from read_csv import read_as_array as read
from union_find import *
import os, shutil
from collections import Counter


# configuration
# PATH_TO_NODES = "private_data/musicbrainzGraph/musicbrainzNodes.csv"
# PATH_TO_EDGES = "private_data/musicbrainzGraph/musicbrainzRelations.csv"
# PATH_TO_OUTPUT_DIR = "private_data/musicbrainzGraph/own/"
# test configuration
PATH_TO_NODES = "public_data/find_partitions_test/nodes.csv"
PATH_TO_EDGES = "public_data/find_partitions_test/edges.csv"
PATH_TO_OUTPUT_DIR = "public_data/find_partitions_test/output/"


# How talky shall I be ?
BARRIER_NODE_READING = 1000000
BARRIER_OBJECT_CREATION = 500000
BARRIER_MAKING_SETS = 500000
BARRIER_EDGE_READING = 400000
BARRIER_SEARCH_PARTS = 100000
BARRIER_WRITE_PARTS = 80000


def main(length=0):
	######################### print current configuration ##########################
	print ">>> I am finding your partitions!"
	print ">>> nodes: %s" % PATH_TO_NODES
	print ">>> edges: %s" % PATH_TO_EDGES
	print ">>> output: %s" % PATH_TO_OUTPUT_DIR
	print "---------------------------------------------------------------------\n"


	##################### find number of nodes if not provided #####################
	if length == 0:
		print "\n>>> Starting to read nodes..."
		for data in read(PATH_TO_NODES):
			length += 1
			if length % BARRIER_NODE_READING == 0: print "...reading nodes (%s)" % length
	print "Number of Nodes: %s" % length
	

	######################### creating UnionFind structure #########################
	print "\n>>> Creating UninoFind Nodes..."
	nodes = [i for i in range(0, length)] # create array of length length
	for i in range(0, length):
		nodes[i] = Node(i)
		if i+1 % BARRIER_OBJECT_CREATION == 0: print "...creating Nodes (%s)" % i

	print "\n>>> Making Initial UnionFind Sets..."
	counter = 0
	for node in nodes:
		MakeSet(node)
		counter += 1
		if counter % BARRIER_MAKING_SETS == 0: print "...making Sets (%s)" % counter


	##################### merge partitions according to edges ######################
	counter = 0
	print "\n>>> Starting to read edges..."
	for data in read(PATH_TO_EDGES):
		left = nodes[int(data[0])]
		right = nodes[int(data[1])]
		Union(left, right)
		counter += 1
		if counter % BARRIER_EDGE_READING == 0: print "...reading edges (%s)" % counter
	print "Number of edges: %s" % counter

	
	########################## find remaining partitions ###########################
	print "\n>>> Searching for partitions..."
	sets = [Find(node).id for node in nodes]
	c = Counter(sets)
	# del nodes # release memory
	# remaining = []
	# counter = 0
	# for p in sets:
	#	if not p in remaining:
	#		remaining += [p]
	#	counter += 1
	#	if counter % BARRIER_SEARCH_PARTS == 0: print "..searching for partitions (%s, %s)" % (counter, len(remaining))
	# print "Number of Partitions: %s" % len(remaining)
	# print "Partitions (id of one contained node): %s" % remaining
	print "Number of Partitions: %s" % len(c)
	print "Partitions (id of one contained node): \n%s" % str(c).replace(",", ",\n")


	##################### write partitions to dedicated files ######################
	# print "\n>>> Start writing partitions..."
	# shutil.rmtree(PATH_TO_OUTPUT_DIR, ignore_errors=True)
	# os.mkdir(PATH_TO_OUTPUT_DIR)
	# def make_path(partition):
	# 	return os.path.join(PATH_TO_OUTPUT_DIR, '%s.csv' % partition)
	# files = {partition: open(make_path(partition), 'w') for partition in remaining}
	# counter = 0
	# for data in read(PATH_TO_NODES):
	# 	node_id = int(data[0])
	# 	node = nodes[node_id] # we need the node which knows the partition
	# 	partition_id = Find(node).id
	# 	data_row = ('\t'.join(data)).encode('UTF-8')
	# 	files[partition_id].write(data_row)
	# 	files[partition_id].write("\n")
	# 	counter += 1
	# 	if counter % BARRIER_WRITE_PARTS == 0: print "...writing nodes (%s)" % counter
	# [file.close() for file in files.values()]
	# print "Number of files written: %s" % len(files)


	########################### some information at end ############################
	# print "\n\n---------------------------------------------------------------------"
	# print ">>> I have written a file for every partition!"
	# print ">>> Note: I did not write the partition id to the data rows!"
	# print ">>> Note: I did not write headers to the files!"



if __name__ == '__main__':
	import sys
	if len(sys.argv) > 1 and sys.argv[1] == "-i":
		# we know that there are 9909276 nodes
		main(9909276)
	else:
		main()