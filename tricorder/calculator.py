from models import Partition, Node
import component_iterator as iterator
import shortcuts as sc
import networkx as nx

def get_top_artists(path):
	with open(path, "r") as file:
		return set([a for a in file.read().split("\r")])

def calculate_concurrent(path_data, path_artists, num_threads=4, talky=False):
	"""
	Same as `calculate`, but uses multiple threads to accelerate the computation
	process. Threading is only applied the calculation of the measures - the
	input data is still read sequentially.

	Note: this is even more memory consuming than `calculate`.
	Further note: the real bottleneck seems to be reading the data from disk.
	"""
	from threading import Thread
	from Queue import Queue
	from sys import stdout
	import time
	def worker(id):
		while True:
			index, graph = queue.get()
			# filling the queue might take longer than processing (due to file reads)
			# thus we tell the queue that we are done; queue is not involved later on so it should be ok
			queue.task_done()
			do_work(index, graph)
			status[id] += 1
	def do_work(index, graph):
		calculate_connected_component(index, graph, top_artists)
	def print_stati():
		# fancy output looks ugly...
		if talky:
			# print table head
			stdout.write('Progress:' + 'all'.rjust(11) + '  || ' + ' | '.join([("T%s" % (i+1)).rjust(5) for i in range(num_threads)]) + '\n')
			while do_the_print:
				# reprint table body
				stdout.write('\r' + str(sum(status)).rjust(20) + '  || ' + ' | '.join([str(i).rjust(5) for i in status]))
				stdout.flush()
				time.sleep(.75)
			stdout.write('\n')

	num_threads = max(num_threads, 1) # stupid user might be stupid
	queue = Queue(maxsize=num_threads*2)
	top_artists = get_top_artists(path_artists)
	status = [0 for i in range(num_threads)]
	do_the_print = True

	# create workers
	for i in range(num_threads):
		t = Thread(target=worker, args=(i,))
		t.daemon = True
		t.start()

	# for status information
	status_thread = Thread(target=print_stati)
	status_thread.start()

	# load data
	for tupel in enumerate(iterator.components(path_data)):
		if tupel[0] > 500: break
		queue.put(tupel)

	# wait until all threads are finished
	queue.join()
	do_the_print = False

def calculate(path_data, path_artists, talky=False):
	"""
	Reads all connected components from the given dataset and computes
	measures for this graph. For each connected component
	'calculate_connected_component' is called - see this method for
	documentation.
	"""
	top_artists = get_top_artists(path_artists)
	for i, graph in enumerate(iterator.components(path_data)):
		calculate_connected_component(i, graph, top_artists, talky)

def calculate_connected_component(index, graph, top_artists, talky=False):
	"""
	Takes the given graph and computes the following measures:
		- size (number of nodes)
		- diameter
		- density
		- degree
		- closeness_centrality
		- betweenness_centrality
		- eccentricity

	The first three measures are computed for each connected component.
	The remaining ones are computed for each node.

	The result is written to a database (see tricorder.models).
	"""
	is_real_graph = graph.number_of_edges() > 0
	num_artists = 0
	num_top_artists = 0

	# calculate measures (only if we have edges!)
	density = nx.density(graph) if is_real_graph else 0
	diameter = nx.diameter(graph) if is_real_graph else 0
	degree = sc.degree_centrality(graph) if is_real_graph else {}
	closeness = sc.closeness_centrality(graph) if is_real_graph else {}
	betweenness = sc.betweenness_centrality(graph) if is_real_graph else {}
	eccentricity = sc.eccentricity(graph) if is_real_graph else {}

	# create Node DB entries
	for id, attrs in graph.node.items():
		if attrs['type'] == 'artist':
			num_artists += 1
			if attrs['name'] in top_artists:
				num_top_artists += 1
		ecc = 1/eccentricity[id] if id in eccentricity else 0 # need an extra variable here since division by zero is evil
		Node.create(nid=int(id), pid=graph.graph['pid'], node_type=attrs["type"],
			name=attrs["name"], degree=degree.get(id, 0), closeness=closeness.get(id, 0),
			eccentricity=ecc, betweenness=betweenness.get(id, 0))

	# create Partition DB entry
	Partition.create(pid=graph.graph['pid'], diameter=diameter,
		num_nodes=graph.number_of_nodes(), num_edges=graph.number_of_edges(),
		num_artists=num_artists, num_top_artists=num_top_artists, density=density)

	if talky and index % 500 == 0: print index
