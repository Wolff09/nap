#!/usr/bin/env python
# -*- coding: utf-8 -*-

from read_csv import read_as_dict as read
from union_find import *

NODE_MOD = 200000
CREATE_MOD = 100000
MAKE_MOD = 200000
EDGE_MOD = 1000

def main(length=0):
	##################### find number of nodes if not provided #####################
	if length == 0:
		print "Starting to read nodes..."
		for data in read("private_data/musicbrainzGraph/musicbrainzNodes.csv"):
			length += 1
			if length % NODE_MOD == 0: print "...reading nodes (%s)" % length
		print "Number of Nodes: %s" % len(nodes) # TODO: why does wc -l provide a (very) different result??
	

	######################### creating UnionFind structure #########################
	print "%sCreating UninoFind Nodes..." % ("" if length > 0 else "\n")
	nodes = [i for i in range(0, length)] # create array of length length
	for i in range(0, length):
		nodes[i] = Node(i)
		if i % CREATE_MOD == 0: print "...creating Nodes (%s)" % i
	print "Making Initial UnionFind Sets..."
	counter = 0
	for node in nodes:
		MakeSet(node)
		counter += 1
		if counter % MAKE_MOD == 0: print "...making Sets (%s)" % counter


	##################### merge partitions according to edges ######################
	counter = 0
	print "\nStarting to read edges..."
	for data in read("private_data/musicbrainzGraph/musicbrainzRelations.csv"):
		left = nodes[int(data['nodeId0'])]
		right = nodes[int(data['nodeId1'])]
		Union(left, right)
		counter += 1
		if counter % EDGE_MOD: print "...reading edges (%s)" % counter

	
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
	# it seems as if there are 9904458 nodes
	number_of_nodes = 9904458
	import sys
	if len(sys.argv) > 1 and sys.argv[1] == "-i":
		# use initial knowledge
		main(number_of_nodes)
	else:
		main()