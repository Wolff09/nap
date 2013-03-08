NAP - Network Analysis Project
==============================

Goals and Tasks
---------------

Write something useful here...

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
	- sort files

Note: the conversion is not done in memory, but with multiple
temporary files.

- data analysis (per connected component)
	- calculate metrics
	- count interesting stuff
		- number of artists per component
		- number of TOP10000 artists per component
		- number of node types per component
		- number of edge types per component
	- write stuff to db
- ...