#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os

def main(*args):
	if not args:
		print ">>> Please specify an operation. Nothing done..."
	elif args[0] == "syncdb":
		syncdb(*args[1:]) # sync db takes at most 2 params
	else:
		print ">>> The operation you specified is invalid. Nothing done..."

def syncdb(*args):
	if len(args) > 2:
		print ">>> Invalid usage. syncdb takes at most 2 arguments. Usage: syncdb [-f] path/to/new/database/file"
		return
	elif len(args) < 1:
		print ">>> Invalid usage. syncdb takes at least 1 argument. Usage: syncdb [-f] path/to/new/database/file"
	elif len(args) == 1:
		if os.path.exists(args[0]):
			print ">>> The specified destination file already exists. Use -f to force overwrite."
		else:
			create_database(args[0])
	else:
		create_database(args[0])

def create_database(path):
	print "Creating new database in: %s" % path
	print "not yet doing anything... not yet implemented"

if __name__ == '__main__':
	main(*sys.argv[1:])