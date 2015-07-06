import os
import json
import datetime
import pprint
import math

API_KEY = "0f60efd9302d38f88380c6a4608bd9be"

dir_weather 	= "../dataset/weather"
file_business 	= "../dataset/yelp_academic_dataset_business.json"
file_users		= "../dataset/yelp_academic_dataset_user.json"
file_reviews 	= "../dataset/yelp_academic_dataset_review.json"
file_users_centroid	= "../dataset/user-centroid.json"
file_users_reviews = "../dataset/user-location.json"

file_feature_name = "feature-climate.data"

_business = {}
_userLocations = {}
_userReviews = {}
_weather = {}

def loadWeather():
	f = os.listdir(dir_weather)
	c = 0
	for l in f:
		if (l == '.DS_Store'):
			continue
		
		folder = dir_weather + '/' + l
		files = os.listdir(folder)
		for f in files:
			if (f == '.DS_Store'):
				continue
			fo = open(folder + '/' + f)
			for i in fo:
				try:
					j = json.loads(i)
				except Exception, e:
					print f
					raise

				data = j['daily']['data'][0]
				d2 = datetime.datetime.utcfromtimestamp(int(data['time']))
				w = l + '-' + d2.strftime('%Y-%m-%d')

				try:
					_weather[w.lower()] = '%s temperatureMin:%f temperatureMax:%f' % (data['icon'], data['temperatureMin'], data['temperatureMax'])
				except Exception, e:
					print 'Local: %s - Data: %s' % (l, d2.strftime('%d/%m/%Y %H:%M:%S %Z'))
					# if (datetime.datetime.now() >= d2):
					# 	print json.dumps(j)
					# 	raise				


def loadUserReviews():
	global _userReviews
	_userReviews = {}

	f = open(file_users_reviews)
	_userReviews = json.load(f)
	xr = {}
	c = 0
	for k in _userReviews.keys():
		c += 1
		u = _userReviews[k]
		b = []
		for r in u['reviews']:
			bid = r['business_id']
			b.append(bid)

		qtd = len(list(set(b)))
		q = 0
		if (qtd in xr):
			q = xr[qtd] + 1
		else:
			q = 1

		xr[qtd] = q
	pprint.pprint(xr)
	print 'total: %d' % c

def generateVW():

	#Reading user reviews
	# print 'loading user reviews locations'
	# loadUserReviews()

	#Generate users attributes
	print 'reading user attributes'
	users = getUserAttributes()

	#Get users locations
	print 'reading user locations'
	getUserLocations()

	#Generate venues attributes
	print 'reading business attributes'
	items = getBusinessAttributes()

	#Loading weather
	print 'loading weather'
	loadWeather()

	
	#getting relevant climate feature
	#fw_feature = open('output/analysis/' + file_feature_name, 'w')

	f = open(file_reviews)	
	fw = open('output/20053-20131.vw', 'w')

	for line in f:
		item = json.loads(line)
		date = datetime.datetime.strptime(item['date'], '%Y-%m-%d')
		if (date.year == 2005 and date.month >= 03) or (date.year > 2005 and date.year < 2013) or (date.year == 2013 and date.month < 02):
			user_id = item['user_id']
			item_id = item['business_id']
			review_id = item['review_id']
			rating = item['stars']#int(item['stars'] >= 4)

			#review namespace
			nReview = 'uid_%s_bid_%s_rid_%s' % (user_id, item_id, review_id)

			#user namespace
			nUser = users[user_id]

			#item attributes namespace
			nItemAttr = items[item_id + '-attr']

			#item categories namespace
			nItemCat = items[item_id + '-cat']

			#contextual namespace		
			#nContextual = getContextAttributes(item)

			#temporal
			temporal = getTemporalAttributes(item)
			temporal = temporal.lower()

			#weather
			weather = getWeatherAttributes(item)
			weather = weather.lower()
			
			#distance
			distance = getDistanceAttributes(item_id, user_id)
			distante = distance.lower()

			result = "%s '%s |user %s |item %s |category %s |weather %s |distance %s |temporal %s" % (rating, nReview, nUser, nItemAttr, nItemCat, weather, distance, temporal)
			#result = '%s |review %s |user %s |item %s |type %s |context %s' % (rating, nReview, nUser, nItemAttr, nItemCat, nContextual)
			fw.write(result + "\n")


			#cli = weather.split(' ')
			#feature = cli[0].replace('nothing', '').replace('not-found', '').strip()

			# feature = temporal
			# #tratamento
			# feature = feature.replace('weekday:0', '').replace('weekend:0', '').replace('weekday:1', 'weekday').replace('weekend:1', 'weekend')
			# #day of week
			# feature = feature.replace('monday','').replace('tuesday','').replace('wednesday','').replace('thursday','').replace('friday','').replace('saturday', '').replace('sunday', '')
			# #seasons
			# feature = feature.replace('summer', '').replace('winter', '').replace('spring', '').replace('fall', '')
			# #weekdays
			# feature = feature.replace('weekday', '').replace('weekend', '')
			# #months
			# feature = feature.replace('september', '').replace('december', '').replace('july', '').replace('march', '').replace('august', '').replace('may', '').replace('june', '').replace('november', '').replace('february', '').replace('october', '').replace('january', '').replace('april', '')

			#gravando arquivo
			# if feature:
			# 	feat = "%s|review %s |item %s |feature %s" % (rating, review_id, item_id, feature)
			# 	fw_feature.write(feat + "\n")

	f.close()
	fw.close()
	# fw_feature.close()
	
	return

def generateUserItemVW():

	#Reading user reviews
	# print 'loading user reviews locations'
	# loadUserReviews()
	
	f = open(file_reviews)
	fw = open('output/data-user.vw', 'w')

	for line in f:
		item = json.loads(line)
		user_id = item['user_id']
		item_id = item['business_id']
		rating = item['stars']

		result = "%s |user %s |item %s" % (rating, user_id, item_id)
		#result = '%s |review %s |user %s |item %s |type %s |context %s' % (rating, nReview, nUser, nItemAttr, nItemCat, nContextual)
		fw.write(result + "\n")

	f.close()
	fw.close()
	
	return	

def getUserLocations():
	global _userLocations
	_userLocations = {}

	f = open(file_users_centroid)
	for line in f:
		j = json.loads(line)	
		u = {}
		u['lat'] = j['lat']
		u['lng'] = j['lng']
		_userLocations[j['user_id']] = u	

def getUserAttributes():
	f = open(file_users)
	xr = {}
	for line in f:
		j = json.loads(line)
		#xr[j['user_id']] = 'user_id__%s average_stars:%s review_counts:%s' % (j['user_id'], str(j['average_stars']), str(j['review_count']))
		xr[j['user_id']] = 'average_stars:%s review_counts:%s' % (str(j['average_stars']), str(j['review_count']))

	f.close()

	return xr

#Item attributes
def getBusinessAttributes():
	global _business
	_business = {}

	f = open(file_business)
	xr = {}
	for line in f:
		j = json.loads(line)
		_business[j['business_id']] = j

		cat = ' '.join(getCategories(j['categories']))
		attr = ' '.join(getAttributes(j['attributes'], None))
		#xr[j['business_id']] = 'business_id__%s open:%d stars:%d %s %s' % (j['business_id'], int(j['open']), j['stars'], cat.lower(), attr.lower())
		xr[j['business_id'] + '-attr'] = 'stars:%d %s' % (j['stars'], attr.lower())
		xr[j['business_id'] + '-cat'] = cat.lower()		
	
	f.close()

	return xr

#Item categories
def getCategories(attr):
	result = []
	for k in attr:
		result.append(k.replace(" ", "-"))
	
	return result

#Item attributes
def getAttributes(attrs, attr): 
	result = []
	for a in attrs:
		key = a
		value = attrs[a]
		if (type(value) is dict):
			result.extend(getAttributes(value, key))
		else:
			if (attr is not None):
				key = attr + '_' + key

			v = value
			if (type(value) is unicode):
				value = key + '__' + v
			elif(type(value) is bool):
				v = str(int(attrs[a]))
				value = key + ':' + v
			else:
				value = key + ':' + str(v)
			
			value = value.replace(" ", "-")
			result.append(value)
	return result


#Context attributes
def getContextAttributes(review):
	#temporal
	temporal = getTemporalAttributes(review)

	#weather
	weather = getWeatherAttributes(review)
	
	#distance
	distance = getDistanceAttributes(review['business_id'], review['user_id'])

	attributes = '%s %s %s' % (temporal, distance, weather)
	return attributes.lower()

def getTemporalAttributes(review):
	date = datetime.datetime.strptime(review['date'], '%Y-%m-%d')
	dayofweek = date.strftime('%A').lower()
	weekday = int((date.isoweekday() < 6))
	weekend = int((date.isoweekday() >= 6))
	month = date.strftime('%B').lower()
	season = getSeason(date, 'north')
	
	context = '%s weekday:%d weekend:%d %s %s %s' % (dayofweek, weekday, weekend, month, season, review['date'])
	return context

_city = []
def getWeatherAttributes(review):
	b = _business[review['business_id']]
	name = b['city']
	name = name.strip()
	
	weatherName = name + '-' + review['date']
	weatherName = weatherName.replace('"', '').lower()

	v = 'nothing'
	try:
		v = _weather[weatherName]		
	except Exception, e:
		if ('las vegas' in weatherName):
			weatherName = 'las vegas' + '-' + review['date']
			v = _weather[weatherName]
		else:
			print 'error'
			v = 'not-found'
			_city.append(weatherName)
	finally:
		return v

def getSeason(date, hemisphere):
	md = date.month * 100 + date.day

	if ((md > 320) and (md < 621)):
	    s = 0 #spring
	elif ((md > 620) and (md < 923)):
	    s = 1 #summer
	elif ((md > 922) and (md < 1223)):
	    s = 2 #fall
	else:
	    s = 3 #winter

	if not hemisphere == 'north':
	    s = (s + 2) % 3


	if (s == 0):
		return 'spring'
	elif (s == 1):
		return 'summer'
	elif (s == 2):
		return 'fall'
	else:
		return 'winter'

def getDistanceAttributes(business, user):
	
	lat1 = _userLocations[user]['lat']
	lng1 = _userLocations[user]['lng']
	lat2 = _business[business]['latitude']
	lng2 = _business[business]['longitude']
	distance = distance_on_unit_sphere(lat1, lng1, lat2, lng2)
	
	km = distance / 1000	
	if (km <= 5):
		return 'distance-near'
	elif (km > 5 and km <= 20):
		return 'distance-medium'
	else:
		return 'distance-far'
	
	#print 'lat1: %f lng1: %f | lat2: %f lng2: %f == distance %f' % (lat1, lng1, lat2, lng2, distance)		

def feq(a,b):
    if abs(a-b)<0.00000001:
        return 1
    else:
        return 0

def distance_on_unit_sphere(lat1, long1, lat2, long2):
	
    try:		
	    if (feq(lat1, lat2) and feq(long1, long2)):
	    	return 0

	    # Convert latitude and longitude to 
	    # spherical coordinates in radians.
	    degrees_to_radians = math.pi/180.0

	    # phi = 90 - latitude
	    phi1 = (90.0 - lat1)*degrees_to_radians
	    phi2 = (90.0 - lat2)*degrees_to_radians
	        
	    # theta = longitude
	    theta1 = long1*degrees_to_radians
	    theta2 = long2*degrees_to_radians
	        
	    # Compute spherical distance from spherical coordinates.
	        
	    # For two locations in spherical coordinates 
	    # (1, theta, phi) and (1, theta, phi)
	    # cosine( arc length ) = 
	    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
	    # distance = rho * arc length
	    
	    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
	           math.cos(phi1)*math.cos(phi2))

	    arc = math.acos( cos )

	    # Remember to multiply arc by the radius of the earth 
	    # in your favorite set of units to get length.


	    distance  = math.degrees(arc) # in degrees
	    distance  = distance * 60 # 60 nautical miles / lat degree
	    distance = distance * 1852 # conversion to meters
	    distance  = round(distance)
	    return distance

    except:
    	print 'lat1: %f lng1: %f | lat2: %f lng2: %f' % (lat1, long1, lat2, long2)
    	raise

generateVW();

#errors
print _city