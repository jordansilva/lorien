# -- coding: utf-8 --

import os
import json
import datetime
import pprint
import math
import operator

#mathplotlib
import numpy as np
import matplotlib.pyplot as plt

directory = '/Users/jordansilva/Documents/Jordan/Mestrado/Lorien/code/output/analysis'
files = ['feature-climate.data', 'feature-distance.data', 'feature-temporal-dayofweek.data', 'feature-temporal-month.data', 'feature-temporal-season.data', 'feature-temporal-weekday.data', 'feature-categories.data']
representation = {}
features = {}
featuresCount = {}

#loads feature file to dictionary representation
#rating |review id |item id |feature properties[]
def representation(filename):
	f = open(filename)
	for line in f:
		lineData = line.split('|')

		rating = lineData[0].strip()
		#reviewId = lineData[1][7:].strip()
		#itemId = lineData[2][5:].strip()		
		featureProperties = lineData[3][8:].strip().split(' ')
		featureProperties = filter(None, featureProperties)		

		for feat in featureProperties:

			if feat not in featuresCount:
				featuresCount[feat] = 1
			else:
				featuresCount[feat] = featuresCount[feat] + 1

			good = 0
			bad = 0
			if int(rating) > 3:
				good = 1
			else:
				bad = 1

			if feat not in features:
				features[feat] = {}			
				features[feat]['good'] = good
				features[feat]['bad'] = bad
			else:			
				features[feat]['good'] = features[feat]['good'] + good
				features[feat]['bad'] = features[feat]['bad'] + bad

	return


def printFeatures(size):
	sorted_x = sorted(featuresCount.items(), key=operator.itemgetter(1), reverse=True)
	# sorted_x = [x for x in sorted_x if x[1] >= 100]
	# sorted_x = sorted(sorted_x, key=operator.itemgetter(0))
	
	# for x in sorted_x:
	# 	print '%s %s' % (x[0], x[1])
	
	print sorted_x[:size]

def plot():
	N = len(features)
	
	ind = np.arange(N)    # the x locations for the groups
	width = 0.35       # the width of the bars: can also be len(x) sequence
	
	dataRelevant = []
	dataNonRelevant = []
	legend = []

	for item in features:		
		dataRelevant.append(features[item]['good'])
		dataNonRelevant.append(features[item]['bad'])
		legend.append(item)
	
	fig, ax = plt.subplots()
	rects1 = ax.bar(ind, dataRelevant, width, color='g')
	rects2 = ax.bar(ind+width, dataNonRelevant, width, color='r')

	# add some text for labels, title and axes ticks
	ax.set_ylabel('Amount of reviews')
	ax.set_title('Feature Relevance')
	ax.set_xticks(ind+width)
	ax.set_xticklabels( legend )	

	autolabel(rects1, ax)
	autolabel(rects2, ax)

	ax.legend( (rects1[0], rects2[0]), (u'Relevant feedback', u'Irrelevant feedback') )

	plt.show()

def autolabel(rects, ax):
  # attach some text labels
  for rect in rects:
		height = rect.get_height()
		ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height), ha='center', va='bottom')

#main program
def main():
	representation(directory + '/' + files[6])
	printFeatures(200)
	#plot()
	#print features


main()