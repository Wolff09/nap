#!/usr/bin/env python
# -*- coding: utf-8 -*-

from read_csv import read_as_dict as read
import networkx as nx


def main():
	node_file = "private_data/musicbrainzGraph/musicbrainzNodes.csv"
	edge_file = "private_data/musicbrainzGraph/musicbrainzRelations.csv"

	G = nx.Graph()
	print "-- adding nodes --"
	for data in read(node_file):
		G.add_node(int(data['nodeId']), nodeType=data[nodeType], name=data[name])
	print "-- adding edges --"
	for data in read(edge_file):
		G.add_edge(int(data['nodeId0']), int(data['nodeId1']), lLinkTypeId=data['lLinkTypeId'])

	print "-- Jobs Done! --"

if __name__ == '__main__':
	main()
