#!/usr/bin/env python
# -*- coding: utf-8 -*-

def read_as_array(path, delimiter="\t"):
	"""
	Reads a file line by line. The first line is supposed to
	contain a header. However, the values of the header are
	ignored - only the number of values matters.

	Yields every row, except the header (first line), of the
	file found at the given path as array. The array contains
	the values which are split by the given delimiter (default:
	the \t tab char). Note that the array is at most of the same
	length as the header.
	"""
	file = open(path, "r")
	len_head = len(file.readline().strip().split(delimiter))
	for line in file:
		yield line.strip().split(delimiter, len_head)

def read_as_dict(path, delimiter="\t"):
	"""
	Similar to read_as_array but yields a dict instead of
	an array. The key-value pairs are created with the
	header entry.
	"""
	file = open(path, "r")
	head = file.readline().strip().split(delimiter)
	len_head = len(head)
	for line in file:
		array = line.strip().split(delimiter, len_head)
		yield {head[i]: array[i] for i in range(len_head)}

