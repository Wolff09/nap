import csv

def read_csv(path, delimiter="\t"):
	"""
	Reads a CSV file with given path (may be relative).
	Yields every row as a dictionary.
	The keys for the dictionary are read from the head of the CSV file.
	"""
	file = open(path, "r")
	reader = csv.reader(file, delimiter=delimiter)
	head = reader.next() # pop head
	for row in reader:
		data = {head[i]: row[i] for i in range(0, len(row))}
		yield data