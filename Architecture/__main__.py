import json
import datetime
from DataBaseProxy import DataBaseProxy
from Car2GoProvider import Car2Go
from EnjoyProvider import Enjoy

from Analysis import day_analysis, getODmatrix

dbp = DataBaseProxy()
#dbp.compress()

##################################################
################BOOK&PARK CREATION################
##################################################

#car2go = Car2Go()
#enjoy = Enjoy()

#end = datetime.datetime(2016, 12, 10, 0, 0, 0)
#start = end - datetime.timedelta(days = 1)
#car2go.select_data("torino","timestamp", start, end)
#enjoy.select_data("torino","timestamp", start, end)

#car2go.end = datetime.datetime(2017, 01, 10, 0, 0, 0)
#car2go.start = datetime.datetime(2016, 12, 04, 0, 0, 0)
#car2go.select_data("torino", "full")    
#enjoy.end = datetime.datetime(2017, 01, 10, 0, 0, 0)
#enjoy.start = datetime.datetime(2016, 12, 04, 0, 0, 0)
#enjoy.select_data("torino", "full")    

#print car2go.get_fields()
#print car2go.get_fleet()
#print car2go.get_fleet_from_db()

#car2go_status, car2go_cars = car2go.get_parks_and_books_v2()

#print enjoy.get_fields()
#print enjoy.get_fleet()
#print enjoy.get_fleet_from_db()

#enjoy_status, enjoy_cars = enjoy.get_parks_and_books_v2()


##################################################
##################DATA ANALYSIS###################
##################################################


provider = 'enjoy'
city = 'torino'
fleet_size = 403

year = 2016
month = 12

for day in range(9, 10, 1):

	print ('day:'+str(day))

	books_df_car2go, parks_d_car2go, day_stats_car2go = \
	    day_analysis(city, provider, year, month, day, fleet_size)
	zones, origins, destinations, od = getODmatrix(city, provider, year, month, day)

	day_db = datetime.datetime(year, month, day, 23, 59)
	dbp.insert_day_analysis(day_db, city, provider, list(day_stats_car2go.T.to_dict().values()), json.loads(od.T.to_json()).values())