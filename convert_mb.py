import networkx as nx
import csv


def main():
	G = nx.Graph()

	print "-- reading nodes --"
	attrs_file = open("private_data/musicbrainzGraph/musicbrainzNodes.csv", "r")
	my_reader = csv.reader(attrs_file, delimiter="\t")
	my_reader.next() # pop head
	# num = {}
	# for row in my_reader:
	#	id = int(row[0])
	#	#G.add_node(id)#, globalMusicBrainzId=row[1], musicBrainzTableId=row[2], nodeType=row[3], name=row[4])
	#	if id % 100000 == 0:
	#		print id
	#	nodeType = row[3]
	#	if nodeType in num:
	#		num[nodeType] += 1
	#	else:
	#		num[nodeType] = 1
	# print str(num).replace(",", ",\n")

	print "-- reading edges --"
	attrs_file = open("private_data/musicbrainzGraph/musicbrainzRelations.csv", "r")
	my_reader = csv.reader(attrs_file, delimiter="\t")
	my_reader.next() # pop head
	index = 0
	num = {}
	for row in my_reader:
		# G.add_edge(int(row[0]), int(row[1]))#, lLinkTypeId=row[2], strShortLinkPhrase=row[3])
		if index % 100000 == 0:
			print index
		index += 1
		edgeType = row[3]
		if edgeType in num:
			num[edgeType] += 1
		else:
			num[edgeType] = 1
	print str(num).replace(",", ",\n")

	print "-- writing graph --"
	nx.write_gexf(G, 'musicbrainz.gexf')

	print "-- finished --"
	return

if __name__ == '__main__':
	main()
