import csv

def read_csv(path, delimiter="\t"):
	"""
	Reads a CSV file with given path (may be relative).
	Yields every row as a dictionary.
	The keys for the dictionary are read from the head of the CSV file.

	If a row contains more fields than the header indicates the last
	field of the head consumes the remaining fields of the row.
	"""
	file = open(path, "r")
	reader = csv.reader(file, delimiter=delimiter)
	head = reader.next() # pop head
	len_head = len(head)
	len_head_sub = len_head - 1
	for row in reader:
		data = {head[i]: row[i] for i in range(0, len_head_sub)}
		data[head[-1]] = " ".join(row[i] for i in range(len_head, len(row))) # last field greedily takes the remain
		yield data