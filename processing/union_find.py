#!/usr/bin/env python
# -*- coding: utf-8 -*-

def find(array, x):
	""" get the root of the tree containing x """
	if array[x] == x:
		return x
	else:
		# the recursion depth is too damn high
		node = array[x]
		node_parent = array[node]
		while node != node_parent:
			node = node_parent
			node_parent = array[node]
		array[x] = node # path compression
		return node

def union(array, x, y):
	root_x = find(array, x)
	root_y = find(array, y)
	if root_x != root_y:
		array[root_x] = root_y

def make_sets(length):
	return [i for i in range(length)]