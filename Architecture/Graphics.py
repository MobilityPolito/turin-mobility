import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

from pandas.tools.plotting import scatter_matrix

from Analysis import day_analysis

books_df_car2go, day_stats_car2go = \
    day_analysis("torino", "car2go", 2016, 12, 11, 403.0)
books_df_enjoy, day_stats_enjoy = \
    day_analysis("torino", "enjoy", 2016, 12, 11, 140.0)

#car2go_label = day_stats_car2go["n_parks"].plot(label="Car2Go", legend=True)
#enjoy_label = day_stats_enjoy["n_parks"].plot(label="Enjoy", legend=True)    

fig, ax = plt.subplots(1, 2, figsize=(16, 8))
car2go_handle, = ax[0].plot(day_stats_car2go["n_books"].index, 
                             day_stats_car2go["n_books"], label="Car2Go")
enjoy_handle, = ax[0].plot(day_stats_enjoy["n_books"].index, 
                            day_stats_enjoy["n_books"], label="Enjoy")
plt.legend(handles=[car2go_handle, enjoy_handle])
ax[0].set_title("Absolute number of bookings")
    
car2go_handle, = ax[1].plot(day_stats_car2go["n_books_norm"].index, 
                             day_stats_car2go["n_books_norm"], label="Car2Go")
enjoy_handle, = ax[1].plot(day_stats_enjoy["n_books_norm"].index, 
                            day_stats_enjoy["n_books_norm"], label="Enjoy")
plt.legend(handles=[car2go_handle, enjoy_handle])
ax[1].set_title("System utilization")
plt.savefig("n_books.png")

fig, ax = plt.subplots(1, 2, figsize=(16, 8))
car2go_handle, = ax[0].plot(day_stats_car2go["avg_books_duration"].index, 
                             day_stats_car2go["avg_books_duration"], label="Car2Go")
enjoy_handle, = ax[0].plot(day_stats_enjoy["avg_books_duration"].index, 
                            day_stats_enjoy["avg_books_duration"], label="Enjoy")
plt.legend(handles=[car2go_handle, enjoy_handle])
ax[0].set_title("Average duration")

car2go_handle, = ax[1].plot(day_stats_car2go["med_books_duration"].index, 
                             day_stats_car2go["med_books_duration"], label="Car2Go")
enjoy_handle, = ax[1].plot(day_stats_enjoy["med_books_duration"].index, 
                            day_stats_enjoy["med_books_duration"], label="Enjoy")
plt.legend(handles=[car2go_handle, enjoy_handle])
ax[1].set_title("Median duration")
plt.savefig("duration.png")

#car2go_handle, = ax[1].plot(day_stats_car2go["avg_books_distance"].index, 
#                             day_stats_car2go["avg_books_distance"], label="Car2Go")
#enjoy_handle, = ax[1].plot(day_stats_enjoy["avg_books_distance"].index, 
#                            day_stats_enjoy["avg_books_distance"], label="Enjoy")
#plt.legend(handles=[car2go_handle, enjoy_handle])
#ax[1].set_title("Average distance")

#
#fig, ax = plt.subplots(1, 1, figsize=(8, 8))
#car2go_handle, = ax.plot(day_stats_car2go["avg_books_bill"].index, 
#                         day_stats_car2go["avg_books_bill"], label="Car2Go")
#enjoy_handle, = ax.plot(day_stats_enjoy["avg_books_bill"].index, 
#                        day_stats_enjoy["avg_books_bill"], label="Enjoy")
#plt.legend(handles=[car2go_handle, enjoy_handle])
