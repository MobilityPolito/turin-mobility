import random
import logging
import requests
import datetime
import time
import json
import sys

sys.path.append('../../Architecture')

from DataSource_without_Thread import RTDS
from DataBaseProxy import dbp

LOG_FILENAME = 'data_collection.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

class EnjoyRTDS(RTDS):

	def __init__ (self, city):
		self.name = "enjoy"       
		self.city = city
		self.url_home = 'https://enjoy.eni.com/it/' + self.city + '/map/'
		self.url_cars = 'https://enjoy.eni.com/ajax/retrieve_vehicles'
		self.last_state = None

	def start_session(self):
		self.session = requests.Session()
		self.session.get(self.url_home)
		self.start_time = datetime.datetime.now()

	def stop_session(self):
		self.session = self.session.close()

	def to_DB (self):
		dbp.insert(self.name, self.city, self.last_state)

	def get_state (self):
		request = self.session.get(self.url_cars)
		current_state = json.loads(request.text)
		self.last_state = current_state
		self.to_DB()

def main():

	try:
		print('Initializing...')
		enjoy = EnjoyRTDS('torino')
		enjoy.start_session()
		print enjoy.session
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