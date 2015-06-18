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

'''This is a parser to convert Yelp Dataset Ouput to Vector Model
where will work on deep learning models like Restricted Boltzmann Machines (RBMs) 
and Long Short Term Memory (LSTMs).
'''

# -- coding: utf-8 --

import os
import json
import datetime
import pprint
import math
import operator

directory = '/Users/jordansilva/Documents/Jordan/Mestrado/Lorien/code/output'
default_dataset = '/Users/jordansilva/Documents/Jordan/Mestrado/Lorien/code/output/2013-2014-4 ordered.vw'
default_output 	= '/Users/jordansilva/Documents/Jordan/Mestrado/Lorien/code/output/vector.rbm'
file_categories = '/Users/jordansilva/Documents/Jordan/Mestrado/Lorien/code/output/categories.data'

''' Dataset model:
input
		rating 'id |user avegare_stars:<1-5> review_counts:<int>
							 |item stars:<1-5> [features]
							 |category [categories]
							 |weather <clear-day|cloudy|fog|partly-clear|rain|snow|wind> temperaturemin:<double> temperaturemax:<double>
							 |distance <near|medium|far>
							 |temporal <dayOfWeek> weekday:<bool> weekend:<bool> <month> <season> <date>

output
		[ relevant, categories, weather, distance, temporal ]
'''

weatherVector 		= ['clear-day','cloudy','fog','partly-clear','rain','snow','wind']
distanceVector 		= ['near', 'medium', 'far']
daysOfWeeksVector = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
isWeekendVector		= ['weekday', 'weekend']
monthsVector 			= ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
seasonVector 			= ['spring', 'summer', 'fall', 'winter']

class parser:
	
	def constructVectorBase(self):
		#rating
		self.baseVector.append('relevant')

		#categories
		f = open(file_categories)
		for line in f:
			category = line.split('|')
			self.categoriesVector.append(category[0])
		f.close()		
		self.baseVector.extend(self.categoriesVector)

		#weather
		self.baseVector.extend(weatherVector)

		#distance
		self.baseVector.extend(distanceVector)

		#temporal
		self.baseVector.extend(daysOfWeeksVector)
		self.baseVector.extend(isWeekendVector)
		self.baseVector.extend(monthsVector)
		self.baseVector.extend(seasonVector)
		
		return

	def parse(self, filename = default_dataset, output = default_output):
		f = open(filename)
		fw = open(output, 'w')
		
		for line in f:
			line_split = line.split('|')
			
			#rating
			rating = int(line_split[0][:1])

			#user data
			#line_split[1]

			#item data
			#line_split[2]

			#categories info
			categories = line_split[3].strip().split(" ")
			categories = categories[1:]

			#weather
			weather = line_split[4].strip().split(" ")		
			weather = weather[1].replace('partly-cloudy-day', 'partly-clear').replace('partly-cloudy-night', 'partly-clear')
			
			#distance
			distance = line_split[5].strip().split(" ")
			distance = distance[1].replace("distance-", "")

			#temporal
			temporal = line_split[6].strip().split(" ")
			dayOfWeek = temporal[1]
			isWeekday = '1' in temporal[2]
			isWeekend = '1' in temporal[3]
			month = temporal[4]
			season = temporal[5]

			item = self.constructVector(rating, categories, weather, distance, dayOfWeek, isWeekday, isWeekend, month, season, line)
			#print line_split

			fw.write(str(item) + '\n')
			
		fw.close()
		f.close()
		print 'places without any categories: %d' % self.statistical['no_categories']		
		print 'file generated: %s' % output
		print 'statistical data'
		print self.statistical

		return

	def constructVector(self, rating, categories, weather, distance, dayOfWeek, isWeekday, isWeekend, month, season, line):
		itemVector = [0] * len(self.baseVector)
		
		#relevant
		isRelevant = 0
		if rating > 3:
			isRelevant = 1

		index = self.baseVector.index('relevant')
		itemVector[index] = isRelevant

		categoryFound = 0
		#categories
		for c in categories:
			try:
				index = self.baseVector.index(c)
				itemVector[index] = 1
				categoryFound += 1

				if c in self.statistical:
					self.statistical[c] = self.statistical[c] + 1
				else:
					self.statistical[c] = 1
			except Exception as e:
				pass
				#print 'Category not found'

		if categoryFound == 0:
			self.statistical['no_categories'] = self.statistical['no_categories'] + 1
			
		#weather
		try:
			index = self.baseVector.index(weather)
			itemVector[index] = 1
		except Exception as e:
			pass
			#print 'Weather not found'

		#distance
		index = self.baseVector.index(distance)
		itemVector[index] = 1

		#temporal
		#dayOfWeek
		index = self.baseVector.index(dayOfWeek)
		itemVector[index] = 1	

		#isWeekday
		index = self.baseVector.index('weekday')
		itemVector[index] = 1 if isWeekday else 0

		#isWeekend
		index = self.baseVector.index('weekend')
		itemVector[index] = 1 if isWeekend else 0

		#month
		index = self.baseVector.index(month)
		itemVector[index] = 1	

		#season
		index = self.baseVector.index(season)
		itemVector[index] = 1	
		
		return itemVector

	def translate_item(self, item):
		translated = []

		isRelevant = 'relevant' if item[0] == 1 else 'irrelevant'
		translated.append(isRelevant)

		item = item[1:]
		baseVector2 = self.baseVector[1:]

		for inx, val in enumerate(item):
			if val == 1:
				translated.append(baseVector2[inx])
		
		return translated

	def categories_item(self, item):
		translated = self.translate_item(item)
		categories = []
		for c in translated:
			if c in self.categoriesVector:
				categories.append(c)

		return categories

	def __init__(self):
		self.baseVector = []
		self.categoriesVector = []
		self.statistical = {}
		self.statistical['no_categories'] = 0
		self.constructVectorBase()

if __name__ == '__main__':
	p = parser()
	p.parse()

#result = "%s '%s |user %s |item %s |category %s |weather %s |distance %s |temporal %s" % (rating, nReview, nUser, nItemAttr, nItemCat, weather, distance, temporal)

