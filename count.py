#!/usr/bin/env python
# -*- coding: utf-8 -*-

from read_csv import read_as_dict as read

def print_counter(counter):
	print str(counter).replace(",", ",\n")

def index_counter(index, printer):
	if printer > 0 and index % printer == 0:
		print index
	return index + 1

def count(path, key_name, converter=None, printer=100000):
	counter = {}
	index = 0
	for data in read(path):
		key = data[key_name] if not converter else converter(data[key_name])
		counter[key] = counter.get(key, 0) + 1
		index = index_counter(index, printer)
	print_counter(counter)

def count_degree(path):
	counter = {}
	index = 0
	for data in read(path):
		left = int(data['nodeId0'])
		right = int(data['nodeId1'])
		counter[left] = counter.get(left, 0) + 1
		counter[right] = counter.get(right, 0) + 1
		index = index_counter(index, 100000)
	print_counter(counter)

def main():
	count("private_data/musicbrainzGraph/musicbrainzNodes.csv", "nodeType")
	count("private_data/musicbrainzGraph/musicbrainzRelations.csv", "lLinkTypeId", lambda key: int(key))
	count("private_data/musicbrainzGraph/musicbrainzRelations.csv", "strShortLinkPhrase")
	count_degree("private_data/musicbrainzGraph/musicbrainzRelations.csv")

if __name__ == '__main__':
	main()
