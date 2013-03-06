#!/usr/bin/env python
# -*- coding: utf-8 -*-

from read_csv import read_as_array as read

PATH_TO_NODES = "private_data/musicbrainzGraph/nodes.csv"
PATH_TO_EDGES = "private_data/musicbrainzGraph/edges.csv"
PATH_TO_OUTPUT = "private_data/musicbrainzGraph/merged.csv"

def main():
	print ">>> Writing merged file to: %s" % PATH_TO_OUTPUT
	output = open(PATH_TO_OUTPUT, "w")
	output.write("pid\ttpye\tdata")
	counter = 0

	print "\n>>> Writing nodes..."
	for row in read(PATH_TO_NODES):
		# write: pid, type, nodeid, globMBid, MBtabid, name
		output.write("%s\t%s\t%s\t%s\n" % (row[1], "n", row[0], "\t".join(row[2:])))
		counter += 1
		if counter % 250000 == 0: print "     - %s" % counter

	print "\n>>> Writing edges..."
	for row in read(PATH_TO_EDGES):
		# write: pid, type, leftId, rightId, linkType, linkName
		output.write("%s\t%s\t%s\t%s\t%s\n" % (row[2], "e", row[0], row[1], "\t".join(row[3:])))
		counter += 1
		if counter % 250000 == 0: print "     - %s" % counter

	output.close()
	print "\n>>> Jobs Done!"

if __name__ == '__main__':
	main()