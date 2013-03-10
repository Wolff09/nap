#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models import Partition, Node, DATABASE_PATH, create_tables, clear_tables, connect
from shortcuts import (
		degree, degree_distribution,
		diameter,
		eccentricity, clustering, average_clustering, transitivity,
		degree_centrality, closeness_centrality, betweenness_centrality
	)
from calculator import calculate

try:
	connect()
except:
	# dies silently
	pass