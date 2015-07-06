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

directory = '/Users/jordansilva/Documents/Jordan/Mestrado/Lorien/code/output/theano'
default_dataset = '/Users/jordansilva/Documents/Jordan/Mestrado/Lorien/code/output/2013-2014-4 ordered.vw'
default_output 	= '/Users/jordansilva/Documents/Jordan/Mestrado/Lorien/code/output/theano/reviews.data'
file_categories = '/Users/jordansilva/Documents/Jordan/Mestrado/Lorien/code/output/categories.data'

''' Dataset model:
input
		rating 'id |user avegare_stars:<1-5> review_counts:<int>
							 |item stars:<1-5> [features]
							 |category [categories]
							 |weather <clear-day|cloudy|fog|partly-cloudy|rain|snow|wind> temperaturemin:<double> temperaturemax:<double>
							 |distance <near|medium|far>
							 |temporal <dayOfWeek> weekday:<bool> weekend:<bool> <month> <season> <date>

output
				 1 					22 				7 				3 		 7+1+1+12+4
		[ relevant, categories, weather, distance, temporal ] 1 #58
'''


class parser:

	weatherVector 		= ['clear-day','cloudy','fog','partly-cloudy','rain','snow','wind']
	distanceVector 		= ['near', 'medium', 'far']
	daysOfWeeksVector = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
	isWeekendVector		= ['weekday', 'weekend']
	monthsVector 			= ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
	seasonVector 			= ['spring', 'summer', 'fall', 'winter']
	
	def constructVectorBase(self):
		self.baseVector.append('user_id')
		self.baseVector.append('business_id')

		#categories
		f = open(file_categories)
		for line in f:
			category = line.split('|')
			self.categoriesVector.append(category[0])
		f.close()		
		self.baseVector.extend(self.categoriesVector)

		self.baseVector.append('weather')
		self.baseVector.append('distance')
		self.baseVector.append('daysOfWeek')
		self.baseVector.append('isWeekend')
		self.baseVector.append('month')
		self.baseVector.append('season')
		
		return

	def parse(self, filename = default_dataset, output = default_output):
		self.users = []
		self.business = []

		f = open(filename)
		fw = open(output, 'w')

		for line in f:
			line_split = line.split('|')
			ident = line_split[0][1:]

			#rating
			rating = int(line_split[0][:1])

			#user data
			uid = ident[ident.index('uid_') + 4:ident.index('_bid_')]

			#item data
			bid = ident[ident.index('bid_') + 4:ident.index('_rid_')]

			if uid not in self.users:
				self.users.append(uid)

			if bid not in self.business:
				self.business.append(bid)

			#categories info
			categories = line_split[3].strip().split(" ")
			categories = categories[1:]

			#weather
			weather = line_split[4].strip().split(" ")		
			weather = weather[1].replace('partly-cloudy-day', 'partly-cloudy').replace('partly-cloudy-night', 'partly-cloudy')
			
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

			uid_n = self.users.index(uid) + 1
			bid_n = self.business.index(bid) + 1
			
			item = self.constructVector(uid_n, bid_n, categories, weather, distance, dayOfWeek, isWeekday, isWeekend, month, season, line)
			#print line_split

			fw.write('%d %s \n' % (rating, str(item)))

		fw.close()
		f.close()

		fw = open(directory + '/users.data', 'w')
		for ind, x in enumerate(self.users):
			fw.write(('%d %s\n' % (ind + 1, x)))
		fw.close()

		fw = open(directory + '/business.data', 'w')
		for ind, x in enumerate(self.business):
			fw.write(('%d %s\n' % (ind + 1, x)))
		fw.close()
		
		print 'places without any categories: %d' % self.statistical['no_categories']		
		print 'file generated: %s' % output
		print 'statistical data'
		print self.statistical

		return

	def constructVector(self, uid, bid, categories, weather, distance, dayOfWeek, isWeekday, isWeekend, month, season, line):
		itemVector = [0] * len(self.baseVector)
		
		itemVector[0] = uid
		itemVector[1] = bid

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
			#self.statistical['categories_not_found'].append(line)
			
		#weather
		try:
			indexWeather = self.baseVector.index('weather')
			index = self.weatherVector.index(weather)
			itemVector[indexWeather] = index + 1
		except Exception as e:
			itemVector[indexWeather] = 0

		#distance
		indexDistance = self.baseVector.index('distance')
		index = self.distanceVector.index(distance)
		itemVector[indexDistance] = index + 1

		#temporal
		#dayOfWeek
		indexDayOfWeek = self.baseVector.index('daysOfWeek')
		index = self.daysOfWeeksVector.index(dayOfWeek)
		itemVector[indexDayOfWeek] = index + 1	

		#isWeekend
		indexIsWeekend = self.baseVector.index('isWeekend')
		itemVector[indexIsWeekend] = 0 if isWeekday else 1
		
		#month
		indexMonth = self.baseVector.index('month')
		index = self.monthsVector.index(month)
		itemVector[indexMonth] = index + 1

		#season
		indexSeason = self.baseVector.index('season')
		index = self.seasonVector.index(season)
		itemVector[indexSeason] = index + 1
		
		return itemVector

	# def parserToTheano(self):
	# 	vCategories = []
	# 	vBusiness = []
	# 	vUsers = []

	# 	f = open(default_output)
	# 	#fw = open(directory + '/reviews.lstm', 'w')
	# 	for line in f:
	# 		line_split = line.split(' ')
	# 		rel = line_split[0]
	# 		user = line_split[1]
	# 		business = line_split[2]
	# 		feat = line[line.index('['):]
	# 		break
	# 	#fw.write(''.join(self.statistical))
	# 	#fw.close()

	def __init__(self):
		self.baseVector = []
		self.categoriesVector = []
		self.statistical = {}
		self.statistical['no_categories'] = 0
		self.statistical['categories_not_found'] = []
		self.constructVectorBase()

if __name__ == '__main__':
	p = parser()
	p.parse()
	# p.parserToTheano()