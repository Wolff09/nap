#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from process_data import process_data

def main(cmd_args):
	if len(cmd_args) < 3:
		print "Usage: processing path/to/nodes/file path/to/edge/file path/to/output/file [deletion_names...]"
	elif not os.path.isfile(cmd_args[0]):
		print "Node file is no file"
	elif not os.path.isfile(cmd_args[1]):
		print "Edge file is no file"
	else:
		process_data(*cmd_args)
		sys.exit(0)

if __name__ == '__main__':
	main(sys.argv[1:])