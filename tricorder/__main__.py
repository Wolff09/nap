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
	if not args:
		print ">>> You have to provide the path to the input data."
	elif len(args) > 1:
		print ">>> Invalid usage. This command takes exactly one argument, namely the path to the input data."
	else:
		path = args[0]
		if os.path.exists(path) and os.path.isfile(path):
			print ">>> Starting data analysis..."
			calculator.calculate(path)
		else:
			print ">>> You did not provide a valid input file path."

if __name__ == '__main__':
	main(*sys.argv[1:])
