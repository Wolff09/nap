
from read_csv import read_csv as read

def print_counter(counter):
	print str(counter).replace(",", ",\n")

def count(path, key_name, converter=None, printer=100000):
	counter = {}
	index = 0
	for data in read(path):
		key = data[key_name] if not converter else converter(data[key_name])
		counter[key] = counter.get(key, 0) + 1
		if index % printer == 0:
			print index
		index += 1
	print_counter(counter)

def main():
	count("private_data/musicbrainzGraph/musicbrainzNodes.csv", "nodeType")
	count("private_data/musicbrainzGraph/musicbrainzRelations.csv", "lLinkTypeId", lambda key: int(key))
	count("private_data/musicbrainzGraph/musicbrainzRelations.csv", "strShortLinkPhrase")

if __name__ == '__main__':
	main()
