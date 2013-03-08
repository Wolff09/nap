NAP - Network Analysis Project
==============================

Goals and Tasks
---------------
Write something useful here...


TODO
----
- data analysis (per connected component)
	- calculate metrics
	- count interesting stuff
		- number of artists per component
		- number of TOP10000 artists per component
		- number of node types per component
		- number of edge types per component
	- write stuff to db
- ...


Code Overview
-------------

### Package: `processing`

This package is used to convert the musicbrainz graph into a
format which can be used more easily. That is, we can read the
connected components from the files without loading the complete
graph (which takes more than 16GB of RAM).

Therefore the data undergoes the following steps:
	- read original musicbrainz data
	- delete "various artists" node
	- delete "various artists" edges
	- find connected components
	- merge files
	- annotate connected component id
	- sort according to connected component
	- write

The conversion is done completely in memory. Thus, the performance
is quite well. The memory consumption is somewhere between 3GB to
3.5GB.

#### Usage

You can use this package from within python scripts like so

	from procssing import process_data
	process_data("path/to/nodes.csv", "path/to/edges.csv", "path/to/output.csv", various_artists_id=-1)

The `various_artists_id` is an optional parameter which defaults to `-1`. A value of `-1` means that
no node is deleted. If a positive integer is given the node with that index and all adjacent edges are
deleted.

Alternatively, you can use this package from the command line by invoking

	python path/to/nodes.csv path/to/edges.csv path/to/output.csv

By now, you can not specify the `various_artists_id` like above.

#### Dependencies

If you have [python-progressbar](https://pypi.python.org/pypi/progressbar/2.2) installed you will see
a progress bar. Otherwise no status information is printed. This dependency is **optional**.
