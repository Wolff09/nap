#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from models import DATABASE_PATH, create_tables, clear_tables
import calculator


OPERATIONS = ("syncdb", "cleardb", "calculate")

def main(*args):
	if not args:
		print ">>> Please specify an operation. Nothing done... Available operations: %s" % ", ".join(OPERATIONS)
	else:
		operation_name = args[0]
		if operation_name in OPERATIONS:
			globals()[operation_name](*args[1:])
		else:
			print ">>> The operation you specified is invalid. Nothing done... Available operations: %s" % ", ".join(OPERATIONS)

def syncdb(*args):
	if len(args) > 1:
		print ">>> Invalid usage. syncdb takes at most 1 argument. Usage: syncdb [-f]"
	elif len(args) == 1:
		if os.path.exists(DATABASE_PATH):
			os.remove(DATABASE_PATH)
			create_database()
		else:
			create_database()
	elif len(args) == 0:
		if os.path.exists(DATABASE_PATH):
			print ">>> The database already exists. Use -f to force overwrite or use cleardb."
		else:
			create_database()

def create_database():
	print ">>> Creating database at: %s" % DATABASE_PATH
	create_tables()

def cleardb(*args):
	if os.path.exists(DATABASE_PATH):
		print ">>> Clearing database at: %s" % DATABASE_PATH
		res = clear_tables()
		print ">>> %s Partitions deleted, %s Nodes deleted" % res
	else:
		print "There is no database that could be cleared. Use syncdb to create one."

def calculate(*args):
	if not args or len(args) < 2:
		print ">>> You have to provide the path to the input data and the path to the top artists."
	elif len(args) > 2:
		print ">>> Invalid usage. This command takes exactly two arguments: path to the input data and path to top artists."
	else:
		path_data = args[0]
		path_artists = args[1]
		if not os.path.exists(path_data) or not os.path.isfile(path_data):
			print ">>> You did not provide a valid data input file path."
		elif not os.path.exists(path_artists) or not os.path.isfile(path_artists):
			print ">>> You did not provide a valid artists input file path."
		else:
			print ">>> Starting data analysis..."
			calculator.calculate(path_data)

if __name__ == '__main__':
	main(*sys.argv[1:])
