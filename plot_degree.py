#!/usr/bin/env python
# -*- coding: utf-8 -*-

from read_csv import read_as_dict as read
import matplotlib
import pylab

def main():
	counter = {} # nodeId: degree
	for data in read("private_data/musicbrainzGraph/musicbrainzRelations.csv"):
		left = int(data['nodeId0'])
		right = int(data['nodeId1'])
		counter[left] = counter.get(left, 0) + 1
		counter[right] = counter.get(right, 0) + 1
	
	m = max(counter.values())
	l = [key for key, val in counter if val == m] # iter over key, value pairs not by default!!
	print l

	distribution = {} # val: number of occurrence
	for val in counter.values():
		distribution[val] = distribution.get(val, 0) + 1

	print str(distribution).replace(",", ",\n")

if __name__ == '__main__':
	main()