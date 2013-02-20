import csv

def read_csv(path):
	file = open(path, "r")
	reader = csv.reader(file, delimiter="\t")
	head = reader.next() # pop head
	for row in reader:
		data = {head[i]: row[i] for i in range(0, len(row)-1)}
		yield data