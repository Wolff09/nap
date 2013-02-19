import networkx as nx
import csv


def main():
	G = nx.Graph()

	print "-- reading nodes --"
	attrs_file = open("musicbrainzGraph/musicbrainzNodes.csv", "r")
	my_reader = csv.reader(attrs_file, delimiter="\t")
	my_reader.next() # pop head
	for row in my_reader:
		id = int(row[0])
		G.add_node(id, globalMusicBrainzId=row[1], musicBrainzTableId=row[2], nodeType=row[3], name=row[4])
		if id % 100000 == 0:
			print id

	print "-- reading edges --"
	attrs_file = open("musicbrainzGraph/musicbrainzRelations.csv", "r")
	my_reader = csv.reader(attrs_file, delimiter="\t")
	my_reader.next() # pop head
	index = 0
	for row in my_reader:
		G.add_edge(int(row[0]), int(row[1]), lLinkTypeId=row[2], strShortLinkPhrase=row[3])
		if index % 100000 == 0:
			print index
		index += 1

	print "-- writing graph --"
	nx.write_gexf(G, 'musicbrainz.gexf')

	print "-- finished --"
	return

if __name__ == '__main__':
	main()
