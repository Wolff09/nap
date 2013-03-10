#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models import Partition, Node
from shortcuts import (
		degree, degree_distribution,
		diameter,
		eccentricity, clustering, average_clustering, transitivity,
		degree_centrality, closeness_centrality, betweenness_centrality
	)
from legacy.plot_degree import main as plot_degree
from calculator import calculate