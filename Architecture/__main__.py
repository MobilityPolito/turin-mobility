import datetime
from DataBaseProxy import DataBaseProxy
from Car2GoProvider import Car2Go
from EnjoyProvider import Enjoy

dbp = DataBaseProxy()
dbp.compress()

car2go = Car2Go()
enjoy = Enjoy()

end = datetime.datetime(2016, 12, 10, 0, 0, 0)
start = end - datetime.timedelta(days = 1)

car2go.select_data("torino","timestamp", start, end)    
print car2go.get_fields()
print car2go.get_fleet()
car2go_status, car2go_cars = car2go.get_parks_and_books_v2()

enjoy.select_data("torino","timestamp", start, end)    
print enjoy.get_fields()
print enjoy.get_fleet()
enjoy_status, enjoy_cars = enjoy.get_parks_and_books_v2()
