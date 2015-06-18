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

'''This class has support methods for read dataset model and
other stuffs.
'''

# -- coding: utf-8 --
import os
import sys
import json
import datetime
import pprint
import math
import numpy as np

default_filename = '/Users/jordansilva/Documents/Jordan/Mestrado/Lorien/code/output/vector.rbm'

class reader:
	
	def __init__(self, dataset = default_filename):
		self.filename = dataset

	def parser(self, line):
		aux_array = []
		
		#removing break lines
		line = line.replace('\n', '')
		
		#removing brackets
		line = line.replace('[','').replace(']','')

		#parsing string to int and append to array
		for x in line.split(','):
			aux_array.append(int(x))
		
		return aux_array

	def load(self, size=sys.maxsize, progress=True):  	
		obj = { }
		data = []
		data_full = []
		labels = []
		
		f = open(self.filename)
		i = 0
		for line in f:
			#parsing string vector to array
			aux = self.parser(line)
			data_full.append(aux)
			data.append(aux[1:])
			
			#creating labels
			labels.extend('g' if int(aux[0]) == 1 else 'r')				
			#counting iterations
			i += 1
			if i % 10000 == 0:
				if progress:
					print datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S') + ' ' + str(i)
			
			if i >= size: #break condition
				break

		f.close()
		obj['data-full'] = data_full
		obj['data'] = data
		obj['labels'] = labels
		
		return obj