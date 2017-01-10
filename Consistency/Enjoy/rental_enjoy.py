from pymongo import MongoClient
import datetime
import json
from bson import json_util
import logging

LOG_FILENAME = 'rental.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

MONGO_HOME = 'mongodb://localhost:27017/'

client = MongoClient(MONGO_HOME)
input_db = client.test
#input_db.authenticate('csms', '1234')
collection = input_db['torino']
collection_cars = input_db['enjoy_fleet']

# cursor = collection.find({'provider':'enjoy'}).limit(1)
cursor = collection.find({'provider':'enjoy'}).sort('_id')
cursor_cars = collection_cars.find()

cars = {}

class EnjoyCar():

	def __init__(self, plate):
		self.plate = plate
		self.free = None
		self.lon = float
		self.lat = float
		self.rent = 0
		self.idle = []

	def SetLatLon(self, lat, lon):
		self.lat = lat
		self.lon = lon

	def AddRent(self):
		self.rent += 1

	def ChangeState(self, state):
		self.free = state

	def SetIdleTime(self, time):
		self.idle.append(time)

	def ReserveCar(self, time):
		print 'reserve'
		self.last_presence = time
		self.free = False

	def ReleaseCar(self):
		print 'release'
		self.free = True

	def UpdateParameters(self, car):
		print 'UPDATe PARAM'
		self.SetLatLon(car['lat'], car['lon'])

	def CheckPrecedentState(self, car):
		if self.free == None :
			self.ReleaseCar()
		else:
			self.free == True
			self.UpdateParameters(car)

	def ShowAllInfo(self):
		print "-----"
		print "Car with plate {} is free: {}".format(self.plate, self.free)
		print "In position lon: {} and lat:{}".format(self.lon, self.lat)
		print "#Rent: {}".format(self.rent)
		# print self.idle


for doc in cursor_cars:
	enjoy_car = EnjoyCar(doc['plate'])
	
	#If we want to use a list for all the cars
	# cars.append(enjoy_car)

	#If we want to use a dict with all the cars
	# { ...
	# 'plate' : EnjoyCar object
	#   ... }
	cars[doc['plate']] = enjoy_car 


for doc in cursor:
	for available_car in doc['state']:

		cars[available_car['car_plate']].CheckPrecedentState(available_car)

		if cars[available_car['car_plate']].free == True:
			cars[available_car['car_plate']].SetLatLon(available_car['lat'],available_car['lon'])

		elif cars[available_car['car_plate']].free == False:
			print "----- CHANGE STATE -----"
			print 'car {} was in lat:{} and lon:{} at {}'.format(cars[available_car['car_plate']].plate, cars[available_car['car_plate']].lat, 
																cars[available_car['car_plate']].lon, cars[available_car['car_plate']].last_presence)
			cars[available_car['car_plate']].ReleaseCar()

		else:
			cars[available_car['car_plate']].ReserveCar()
			cars[available_car['car_plate']].ChangeState(False)

for plate in cars:
	cars[plate].ShowAllInfo()

# for doc in cursor:

# 	for available_car in doc['state']:

# 		if cars['EZ500DD']['plate'] in available_car['car_plate']:
			
# 			if cars['EZ500DD']['rent'] == 1:

# 				print 'moved from {} to {}'.format(cars['EZ500DD']['last_lon'], available_car['lon'])
# 				print 'init {} finish {}'.format(cars['EZ500DD']['last_presence'], doc['timestamp'])

# 				cars['EZ500DD'].update({
# 										'last_lon': available_car['lon'],
# 										'last_lat': available_car['lat'],
# 										'last_presence': doc['timestamp'],
# 										'rent': 0
# 									})

# 			else:
# 				cars['EZ500DD'].update({
# 									'last_lon': available_car['lon'],
# 									'last_lat': available_car['lat'],
# 									'last_presence': doc['timestamp'],
# 									'rent': 0
# 									})
# 		else:
# 			if cars['EZ500DD']['rent'] == 0 and found == 1:
# 				cars['EZ500DD'].update({'rent': 1})
# 				found = 0
# 				print 'qui dentro!!!-----------------'
# 			else:
# 				pass


	# try:
	# 	for available_car in doc['state']:
	# 		if available_car['car_plate'] not in cars:
	# 			cars.append(available_car['car_plate'])
	# except:
	# 	count_error += 1
	# 	message = 'ERROR! in entry {}'.format(doc['_id'])
	# 	logging.debug(message)

# print cars
# print cars['EZ500DD']['last_pos']