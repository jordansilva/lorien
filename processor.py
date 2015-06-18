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

'''This is a class for test deep learning models for represent and predict
POI recommendations
'''

# -- coding: utf-8 --
import os
import sys
import json
import datetime
import pprint
import math
import numpy as np
import ast
from analysis.parser import parser #parser
from util.reader import reader #loaddata
from algorithms.rbm import RBM #rbm
import matplotlib.pyplot as plt #mathplotlib

#tsne
from tsne import bh_sne

dataset3 = '/Users/jordansilva/Documents/Jordan/Mestrado/Lorien/code/output/vector-3.rbm'
dataset4 = '/Users/jordansilva/Documents/Jordan/Mestrado/Lorien/code/output/vector-4.rbm'

def run(training_size = sys.maxsize):
	
	print 'size of training sample: %d' % training_size 

	#load data
	r = reader(dataset3)
	obj = r.load(size=training_size, progress=False)

	#parser
	p = parser()
	data_categories = {}
	label_categories = {}
	
	for d in obj['data-full']:
		for c in p.categories_item(d):
			if c not in data_categories:
				data_categories[c] = []
				label_categories[c] = []
			
			data_categories[c].append(d[1:])
			label_categories[c].append('g' if d[0] == 1 else 'r')			
	
	print len(data_categories)
	for c in data_categories:
		print '------------------------'
		print '%s (%d)' % (c, len(data_categories[c]))
		print '------------------------'
		if len(data_categories[c]) > 100:
			t_sne(data_categories[c], label_categories[c])
		else:
			print 'small dimensionality'
	#echen_rbm(obj)

	return

#http://lvdmaaten.github.io/tsne/
#t-Distributed Stochastic Neighbor Embedding (t-SNE) is a (prize-winning) technique for dimensionality reduction that is particularly well suited for the visualization of high-dimensional datasets.
def t_sne(data, labels):
	arr = np.array(data, dtype=np.float64)
	x2 = bh_sne(arr)
	plt.scatter(x2[:, 0], x2[:, 1], c=labels)
	plt.show()

def echen_rbm(data):
	visible_units = 57
	hidden_units = 10
	epochs_size = 5000
	
	print '> running rbm'
	print 'visible units: %d' % visible_units
	print 'hidden units: %d' % hidden_units
	print 'epochs size: %d' % epochs_size
	print '-------------'
	
	rbm = RBM(num_visible = visible_units, num_hidden = hidden_units, learning_rate=0.1)
	training_data = np.array(data)
	rbm.train(training_data, epochs_size, True)

	#print(rbm.weights)
	# np.savetxt('test.out', r.weights)
	# user = np.array([[0,0,0,1,1,0]])
	#print rbm.run_visible(user)
	
	# hidden_data = np.array([[0,1]]) # A matrix with a single row that contains the states of the hidden units. (We can also include more rows.)
	# print(r.run_hidden(hidden_data)) # See what visible units are activated

if __name__ == '__main__':
	print 'running processor...'

	training_size = sys.maxsize# 10000
	
	run(training_size)

	print 'processor executed'
	
