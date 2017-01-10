import random

import datetime
import time

import requests
from pymongo import MongoClient
import json

import logging

LOG_FILENAME = 'data_collection.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

MONGO_HOME = 'mongodb://localhost:27017/'
DB_NAME = 'CSMS'
db_user = 'csms'
db_pwd 	= '1234'
db_city = 'torino'

client = MongoClient(MONGO_HOME)
db = client[DB_NAME]
db.authenticate(db_user, db_pwd)
collection = db[db_city]

def DBinsert (current_state):

	record = {
				"timestamp": datetime.datetime.now(),
				"provider": 'enjoy',
				"state": current_state
			 }

	try:
		collection.insert_one(record)
		message = 'SUCCESS! time: {}'.format(datetime.datetime.now())
		logging.debug(message)
	except:
		message = 'FAIL! time: {}'.format(datetime.datetime.now())
		logging.debug(message)

class EnjoyClass():

	def __init__(self, city):
		self.city = city
		self.last_state = None
		self.url_home = 'https://enjoy.eni.com/it/' + city + '/map/'
		self.url_cars = 'https://enjoy.eni.com/ajax/retrieve_vehicles'

	def start_session(self):
		self.session = requests.Session()
		self.session.get(self.url_home)
		self.start_time = datetime.datetime.now()

	def stop_session(self):
		self.session = self.session.close()

	def get_state (self):
		request = self.session.get(self.url_cars)
		current_state = json.loads(request.text)
		self.last_state = current_state
		DBinsert(self.last_state)

def main():

	try:
		print('Initializing...')
		enjoy = EnjoyClass('torino')
		enjoy.start_session()
		print ('enjoy class and session: ok!')

		while(True):

			try:
				if (datetime.datetime.now() - enjoy.start_time).total_seconds() < 3000:
					enjoy.get_state()

				else:
					try:
						enjoy.stop_session()
					except:
						logging.debug('FAIL in stop_session(), time: {}').format(datetime.datetime.now())

					try:
						enjoy.start_session()
					except:
						logging.debug('FAIL in start_session() after stop, time: {}').format(datetime.datetime.now())

					try:
						enjoy.get_state()
					except:
						logging.debug('FAIL in get_state(), time: {}').format(datetime.datetime.now())
			except:
				logging.debug('FAIL in first control after IF STATEMENT, time: {}').format(datetime.datetime.now())

			try:
				time.sleep(60 + random.randint(-30,30))
			except:
				logging.debug('FAIL, error in time.sleep(), time: {}').format(datetime.datetime.now())

	except:
		print('Error in initializing enjoy class or session')

if __name__ == "__main__":
	main()