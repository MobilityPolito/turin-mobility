import sys
import datetime
sys.path.append('../Architecture')

from ParksAnalysis import get_parks_hours_stats, group_parks_by_hour
from BooksAnalysis import get_books_hours_stats, group_books_by_hour
from DataBaseProxy import DataBaseProxy

dbp = DataBaseProxy()

start = datetime.datetime(2016, 12, 5, 0, 0, 0)
end = datetime.datetime(2016, 12, 8, 23, 59, 59)
#end = datetime.datetime.now()

car2go_parks = dbp.query_parks_df_filtered_v2('car2go', 'torino', start, end, 'business')
car2go_books = dbp.query_books_df_filtered_v2('car2go', 'torino', start, end, 'business')

#car2go_parks = dbp.query_books_df("car2go", "torino", start, end)
#car2go_books = dbp.query_books_df("car2go", "torino", start, end)

car2go_parks_modified, car2go_parks_stats = get_parks_hours_stats(car2go_parks)
car2go_books_modified, car2go_books_stats = get_books_hours_stats(car2go_books)

#car2go_parks_hour = group_parks_by_hour(car2go_parks)
#car2go_books_hour = group_books_by_hour(car2go_books)