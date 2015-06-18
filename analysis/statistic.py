# Copyright (c) 2015 Jordan Silva <jordan@dcc.ufmg.br>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''I need describe here what this class do and how
'''

# -- coding: utf-8 --

import os
import json
import datetime
import pprint
import math
import operator
import numpy as np

import parser

directory = '/Users/jordansilva/Documents/Jordan/Mestrado/Lorien/code/output'
default_dataset = '/Users/jordansilva/Documents/Jordan/Mestrado/Lorien/code/output/data 2013-2014.vw'
default_output = '/Users/jordansilva/Documents/Jordan/Mestrado/Lorien/code/output/vector.stats'

class statistic:
	
	def __init__(self, filename = default_dataset):
		self.filename = filename
		return

	def run(self):
		stats = {}

		f = open(self.filename)
		#fw = open(output, 'w')
		
		for line in f:
			line_split = line.split('|')

			ident = line_split[0][1:]
			#user data
			uid = ident[ident.index('uid_') + 4:ident.index('_bid')]
			if uid not in stats:
				stats[uid] = 0
			stats[uid] = stats[uid] + 1
			
		#fw.close()
		f.close()

		summarize = {}
		for x in stats:
			if stats[x] not in summarize:
				summarize[stats[x]] = 1
			else:
				summarize[stats[x]] = summarize[stats[x]] + 1			
		
		print summarize

		return

	def split(self, output, sizeReviews = 4):
		items = {}
		f = open(self.filename)
		
		for line in f:
			line_split = line.split('|')

			ident = line_split[0][1:]
			#user data
			uid = ident[ident.index('uid_') + 4:ident.index('_bid')]
			if uid not in items:
				items[uid] = {}
				items[uid]['items'] = []
				items[uid]['count'] = 0

			items[uid]['count'] = items[uid]['count'] + 1
			items[uid]['items'].append(line)
			
		f.close()

		items_bydata = {}		
		for k in items:
			if items[k]['count'] >= sizeReviews:
				for x in items[k]['items']:
					d = x.replace('\n', '').strip()[-10:]
					date = datetime.datetime.strptime(d, '%Y-%m-%d')
					if date not in items_bydata:
						items_bydata[date] = []
					items_bydata[date].append(x)
		
		sorted_x = sorted(items_bydata.items(), key=operator.itemgetter(0))

		fw = open(output, 'w')
		for x in sorted_x:
			fw.write(''.join(x[1]))
		fw.close()

		return
	
if __name__ == '__main__':
	s = statistic()
	s.split(directory + '/2013-2014-4.vw', 4)
