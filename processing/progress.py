#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
	from progressbar import ProgressBar
	class StatusBar:
		def __init__(self, maxval):
			self.bar = ProgressBar(maxval).start()
		def update(self, val):
			self.bar.update(val if val <= self.bar.maxval else self.bar.maxval)
		def close(self):
			self.bar.finish()
except:
	print ">>> Note: If you install 'progressbar' from 'https://pypi.python.org/pypi/progressbar/2.2' a progress bar is displayed."
	class StatusBar:
		def __init__(*args, **kwargs):
			pass
		def update(*args, **kwargs):
			pass
		def close(*args, **kwargs):
			pass