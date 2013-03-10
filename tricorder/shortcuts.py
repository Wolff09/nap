#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
from collections import Counter


################################### degrees ###################################
def degree(graph):
	return [int(graph.degree(node)) for node in graph]

def degree_distribution(graph, *args, **kwargs):
	return Counter(degree(graph, *args, **kwargs)) # Counter is a dict subclass


################################## distances ##################################
# see: http://networkx.github.com/documentation/latest/reference/algorithms.distance_measures.html

def diameter(graph, *args, **kwargs):
	return nx.distance_measures.diameter(graph, *args, **kwargs)

def eccentricity(graph, *args, **kwargs):
	return nx.distance_measures.eccentricity(graph, *args, **kwargs)


################################# clustering ##################################
# see: http://networkx.github.com/documentation/latest/reference/algorithms.clustering.html

def clustering(graph, *args, **kwargs):
	return nx.clustering(graph, *args, **kwargs)

def average_clustering(graph, *args, **kwargs):
	return nx.average_clustering(graph, *args, **kwargs)

def transitivity(graph, *args, **kwargs):
	return nx.transitivity(graph, *args, **kwargs)


################################# centrality ##################################
# see: http://networkx.github.com/documentation/latest/reference/algorithms.centrality.html

def degree_centrality(graph, *args, **kwargs):
	return nx.centrality.degree_centrality(graph, *args, **kwargs)

def closeness_centrality(graph, *args, **kwargs):
	return nx.centrality.closeness_centrality(graph, *args, **kwargs)

def betweenness_centrality(graph, *args, **kwargs):
	return nx.centrality.betweenness_centrality(graph, *args, **kwargs)
