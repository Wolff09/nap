from read_csv import read_csv as read

def main():
	counter = {} # nodeId: degree
	for data in read(path):
		left = int(data['nodeId0'])
		right = int(data['nodeId1'])
		counter[left] = counter.get(left, 0) + 1
		counter[right] = counter.get(right, 0) + 1
	
	distribution = {}
	for val in counter.values():
		distribution[val] = distribution.get(val, 0) + 1

	# distribution contains val: number of occurrence

if __name__ == '__main__':
	main()