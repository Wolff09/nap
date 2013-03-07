#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from process_data import process_data

if __name__ == '__main__':
	cmd_args = sys.argv[1:]
	if len(cmd_args) < 3:
		print "Usage: nodes_file edges_file output_file"
	if not os.path.isfile(cmd_args[0]):
		print "Node file is no file"
	if not os.path.isfile(cmd_args[1]):
		print "Edge file is no file"
	process_data(*cmd_args)