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

### Package: `tricorder`

Like the well known [Tricorder](http://readwrite.com/files/styles/800_450sc/public/fields/Mister_Tricorder.jpg),
this package is for analysing data. In this case for the musicbrainz graph.
To analyse a dataset, you need to convert the data to a proper
format via the `processing` package.
The results from the data analysis is written to a sqlite database
named `nap.db`.

The following measures are calculate:

	- size (number of nodes)
	- diameter
	- density
	- degree
	- closeness_centrality
	- betweenness_centrality
	- eccentricity

#### Usage

First of all, you need to create a database to store the results of
the data analysis. Therefore, type
```sh
python tricorder syncdb
```

If your database already exists, your may want to clear it
(remove all entries). You can do this with
```sh
python tricorder cleardb
```

With this setup, you can start your data analysis with
```sh
python tricorder calculate path/to/precessed_data.csv path/to/top_10000_artists.csv
```

This command will take a while and it will consume a lot of memory (over 16GB).
But if you even have spare memory, you may want to speed up the computation
with multithreading. To do so, use the following command
```sh
python tricorder ccalculate path/to/precessed_data.csv path/to/top_10000_artists.csv [number_of_threads]
```

The `number_of_threads` parameter is optional and defaults to `4`.

You can use the tricorder from within your own python script, too.
This is straight forward and thus only depicted in the following.

```python
from tricorder import *
create_tables() # like python tricorder syncdb
clear_tables() # like python tricorder cleardb
print DATABASE_PATH # path to the databased used by this package
calculate("path/to/precessed_data.csv", "path/to/top_10000_artists.csv")
calculate_concurrent("path/to/precessed_data.csv", "path/to/top_10000_artists.csv")
```

Both, `calculate` and `calculate_concurrent`, take an optional parameter `talky`.
This flag defaults to `false`. If `true` status information will be outputted.
Furthermore, `calculate_concurrent` takes the optional parameter `num_threads`
which defines the number of thread to be used for the computation of the metrics
mentioned above. The number of threads defaults to `4` and at least one thread is
used.

#### Dependencies
You need the [PeeWee ORM](https://github.com/coleifer/peewee) and SQLite.

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
```python
from procssing import process_data
process_data("path/to/nodes.csv", "path/to/edges.csv", "path/to/output.csv")
process_data("path/to/nodes.csv", "path/to/edges.csv", "path/to/output.csv", "Various Artists", "Even More Various Artists")
```
You can process without any deletion of nodes and edges - just keeping the original data and transforming it into another format.
However, you may want to delete some nodes from the graph, like `Various Artists`. To do so, you can specify an arbitrary number
of artist names (as strings) and pass them to the method call. The processing removes any node of type `artist` whichs name
matches one of the given names (exact case insensitive match) and all adjacent edges.

Alternatively, you can use this package from the command line by invoking
```sh
python path/to/nodes.csv path/to/edges.csv path/to/output.csv ["Various Artists"...]
```
Again, you can specify an arbitrary number artist names which shall be deleted.

#### Dependencies

If you have [python-progressbar](https://pypi.python.org/pypi/progressbar/2.2) installed you will see
a progress bar. Otherwise no status information is printed. This dependency is **optional**.
