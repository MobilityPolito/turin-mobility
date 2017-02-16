import datetime

import numpy as np
import pandas as pd
#import geopandas as gpd

from scipy import ndimage
from scipy.spatial import ConvexHull

import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

from pandas.tools.plotting import scatter_matrix

from DataBaseProxy import haversine

# from ParksAnalysis import car2go_parks
# from ParksAnalysis import enjoy_parks

# fig, ax = plt.subplots(1, 1)
# ax = scatter_matrix(car2go_parks[
#                                     [
#                                      "lat", 
#                                      "lon", 
#                                      "duration", 
#                                     ]
#                                 ].astype("float64"), 
#                                 figsize=(10, 10), diagonal='kde')

# fig, ax = plt.subplots(1, 1)
# ax = scatter_matrix(enjoy_parks[
#                                     [
#                                      "lat", 
#                                      "lon", 
#                                      "duration", 
#                                     ]
#                                 ].astype("float64"), 
#                                 figsize=(10, 10), diagonal='kde')

# from ParksAnalysis import car2go_parks_stats
# from ParksAnalysis import enjoy_parks_stats

# def heatmap(d, bins=(100,100), smoothing=1.3, cmap='jet'):

#     x = d["lon"].astype(np.float).values
#     y = d["lat"].astype(np.float).values
#     heatmap, xedges, yedges = np.histogram2d(y, x, bins=bins)
#     extent = [yedges[0], yedges[-1], xedges[-1], xedges[0]]

#     logheatmap = np.log(heatmap)
#     logheatmap[np.isneginf(logheatmap)] = 0
#     logheatmap = ndimage.filters.gaussian_filter(logheatmap, smoothing, mode='nearest')
    
#     plt.imshow(heatmap, cmap=cmap, extent=extent)
#     plt.colorbar()
#     plt.gca().invert_yaxis()
#     plt.show()
# #    plt.savefig("car2go_logheatmap.png")    

#     return

# heatmap(car2go_parks_hour.groupby("hour").get_group(0), bins=20, smoothing=10)
# plt.show()

def color(df):
    if df['provider'][2] == 'enjoy':
        return 'red'
    else:
        return 'blue'

class Graphics():

    def __init__(self):
        pass

    def plot_samples(self, 
                     df, 
                     col, 
                     filter_col, 
                     provider, 
                     color,
                     quantile=0.0,
                     figsize=(13,6)):
        
        plt.title(col)
        s = df.loc[df[filter_col] == True, col].dropna()
        s = s[(s >= s.quantile(q=quantile)) & (s <= s.quantile(q=1.0-quantile))]
        s.plot(marker='o', figsize=figsize, label=provider, color=color)

    def plot_samples_vs(self, 
                        enjoy_df, 
                        car2go_df, 
                        col, 
                        filter_col, 
                        quantile=0.0,
                        figsize=(13,6)):

        plt.figure()
        self.plot_samples(enjoy_df, col, filter_col, "Enjoy", "red", quantile, figsize=figsize)
        self.plot_samples(car2go_df, col, filter_col, "Car2Go", "blue", quantile, figsize=figsize)
        plt.legend()        

    def hist(self, 
             df, 
             col, 
             filter_col, 
             provider, 
             color, 
             quantile=0.00,
             bins=100,
             cumulative=False,
             figsize=(13,6)):
        
        plt.title(col)
        s = df.loc[df[filter_col] == True, col].dropna()
        s = s[(s >= s.quantile(q=quantile)) & (s <= s.quantile(q=1.0-quantile))]
        s.hist(figsize=figsize, label=provider, color=color, cumulative=cumulative, bins=bins)        

    def plot_aggregated_count(self, 
                                df, 
                                col, 
                                filter_col, 
                                provider, 
                                color,
                                freq="30Min",
                                quantile=0.0,
                                figsize=(13,6)):
        
        plt.title("Number of bookings")
        df_ = df.loc[df[filter_col] == True].set_index("start")
        s = df_[col].dropna()
        s = s[(s >= s.quantile(q=quantile)) & (s <= s.quantile(q=1.0-quantile))]
        s = s.resample(freq).count()
        s.plot(marker='o', figsize=figsize, label=provider, color=color)

    def plot_aggregated_count_vs(self, 
                                enjoy_df, 
                                car2go_df, 
                                col, 
                                filter_col,
                                freq="30Min",
                                quantile=0.0,
                                figsize=(13,6)):

        plt.figure()
        self.plot_aggregated_count(enjoy_df, col, filter_col, "Enjoy", "red", freq=freq, quantile=quantile)
        self.plot_aggregated_count(car2go_df, col, filter_col, "Car2Go", "blue", freq=freq, quantile=quantile)
        plt.legend()        
        
    def plot_aggregated_mean(self, 
                        df, 
                        col, 
                        filter_col, 
                        provider, 
                        color,
                        freq="30Min",
                        quantile=0.0,
                        figsize=(13,6)):
        
        plt.title(col)
        df_ = df.loc[df[filter_col] == True].set_index("start")
        s = df_[col].dropna()
        s = s[(s >= s.quantile(q=quantile)) & (s <= s.quantile(q=1.0-quantile))]
        s = s.resample(freq).mean()
        s.plot(marker='o', figsize=figsize, label=provider, color=color)

    def plot_aggregated_mean_vs(self, 
                            enjoy_df, 
                            car2go_df, 
                            col, 
                            filter_col,
                            freq="30Min",
                            quantile=0.0,
                            figsize=(13,6)):

        plt.figure()
        self.plot_aggregated_mean(enjoy_df, col, filter_col, "Enjoy", "red", freq=freq, quantile=quantile)
        self.plot_aggregated_mean(car2go_df, col, filter_col, "Car2Go", "blue", freq=freq, quantile=quantile)
        plt.legend()        

    def plot_aggregated_sum(self, 
                        df, 
                        col, 
                        filter_col, 
                        provider, 
                        color,
                        freq="30Min",
                        quantile=0.0,
                        figsize=(13,6)):
        
        plt.title(col)
        df_ = df.loc[df[filter_col] == True].set_index("start")
        s = df_[col].dropna()
        s = s[(s >= s.quantile(q=quantile)) & (s <= s.quantile(q=1.0-quantile))]
        s = s.resample(freq).sum()
        s.plot(marker='o', figsize=figsize, label=provider, color=color)

    def plot_aggregated_sum_vs(self, 
                            enjoy_df, 
                            car2go_df, 
                            col, 
                            filter_col,
                            freq="30Min",
                            quantile=0.0,
                            figsize=(13,6)):

        plt.figure()
        self.plot_aggregated_sum(enjoy_df, col, filter_col, "Enjoy", "red", freq=freq, quantile=quantile)
        self.plot_aggregated_sum(car2go_df, col, filter_col, "Car2Go", "blue", freq=freq, quantile=quantile)
        plt.legend()        
        
    def plot_daily_count(self, 
                        df, 
                        col, 
                        filter_col, 
                        provider, 
                        color,
                        quantile=0.0,
                        figsize=(13,6)):
        
        plt.title("Number of bookings")
        df_ = df.loc[df[filter_col] == True].set_index("start")
        s = df_[col].dropna()
        s = s[(s >= s.quantile(q=quantile)) & (s <= s.quantile(q=1.0-quantile))]
        s = s.groupby(s.index.map(lambda t: t.hour)).count()
        s.plot(marker='o', figsize=figsize, label=provider, color=color)
        
    def plot_daily_count_vs(self, 
                            enjoy_df, 
                            car2go_df, 
                            col, 
                            filter_col,
                            quantile=0.0,
                            figsize=(13,6)):

        plt.figure()
        self.plot_daily_count(enjoy_df, col, filter_col, "Enjoy", "red", quantile=quantile)
        self.plot_daily_count(car2go_df, col, filter_col, "Car2Go", "blue", quantile=quantile)
        plt.legend()        
        
    def plot_daily_mean(self, 
                        df, 
                        col, 
                        filter_col, 
                        provider, 
                        color,
                        freq="30Min",
                        quantile=0.0,
                        figsize=(13,6)):
        
        plt.title(col)
        df_ = df.loc[df[filter_col] == True].set_index("start")
        s = df_[col].dropna()
        s = s[(s >= s.quantile(q=quantile)) & (s <= s.quantile(q=1.0-quantile))]
        s = s.groupby(s.index.map(lambda t: t.hour)).mean()
        s.plot(marker='o', figsize=figsize, label=provider, color=color)
        
    def plot_daily_mean_vs(self, 
                            enjoy_df, 
                            car2go_df, 
                            col, 
                            filter_col,
                            freq="30Min",
                            quantile=0.0,
                            figsize=(13,6)):

        plt.figure()
        self.plot_daily_mean(enjoy_df, col, filter_col, "Enjoy", "red", freq=freq, quantile=quantile)
        self.plot_daily_mean(car2go_df, col, filter_col, "Car2Go", "blue", freq=freq, quantile=quantile)
        plt.legend()        

    def plot_daily_sum(self, 
                        df, 
                        col, 
                        filter_col, 
                        provider, 
                        color,
                        freq="30Min",
                        quantile=0.0,
                        figsize=(13,6)):
        
        plt.title(col)
        df_ = df.loc[df[filter_col] == True].set_index("start")
        s = df_[col].dropna()
        s = s[(s >= s.quantile(q=quantile)) & (s <= s.quantile(q=1.0-quantile))]
        s = s.groupby(s.index.map(lambda t: t.hour)).sum()
        s.plot(marker='o', figsize=figsize, label=provider, color=color)
        
    def plot_daily_sum_vs(self, 
                            enjoy_df, 
                            car2go_df, 
                            col, 
                            filter_col,
                            freq="30Min",
                            quantile=0.0,
                            figsize=(13,6)):

        plt.figure()
        self.plot_daily_sum(enjoy_df, col, filter_col, "Enjoy", "red", freq=freq, quantile=quantile)
        self.plot_daily_sum(car2go_df, col, filter_col, "Car2Go", "blue", freq=freq, quantile=quantile)
        plt.legend()        
        
    def cdf_weeks_duration(self, df1, df2):
        
        plt.figure()
        plt.title('CDF by weeks duration')
        weeks_number = df1['week'].unique()

        for week in weeks_number:
            df1[(df1['ride'] == True)\
                             & (df1['short_trips'] == True)\
                             & (df1['week']==week)].duration.hist(bins=10000, normed=1, cumulative=True, histtype='step')

        for week in weeks_number:
            df2[(df2['ride'] == True)\
                             & (df2['short_trips'] == True)\
                             & (df2['week']==week)].duration.hist(bins=10000, normed=1, cumulative=True, histtype='step')
        plt.ylabel('p')
        plt.xlabel('duration [m]')
        plt.axis([0, 120, 0, 1.1])
        plt.legend(loc=4)

    def cdf_weeks_distance(self, df1, df2):

        plt.figure()
        plt.title('CDF : weeks distance')
        weeks_number = df1['week'].unique()

        for week in weeks_number:
            df1[(df1['ride'] == True)\
                             & (df1['short_trips'] == True)\
                             & (df1['week']==week)].distance_driving\
                             .hist(bins=100, normed=1, label='enjoy '+str(week), cumulative=True, histtype='step')

        for week in weeks_number:
           df2[(df2['ride'] == True)\
                            & (df2['short_trips'] == True)\
                            & (df2['week']==week)].distance_driving\
                            .hist(bins=100, normed=1, label='car2go '+str(week), cumulative=True, histtype='step')
                            
        plt.ylabel('p')
        plt.xlabel('distance [km]')
        plt.axis([0, 20, 0, 1.1])
        plt.legend(loc=4)

    def cdf_business_weekend(self, df):

        df_ = df[(df.duration >= df.duration.quantile(q=0.01))\
                 & (df.duration <= df.duration.quantile(q=1.0-0.02))]        
        
        fig, ax = plt.subplots(figsize=(13, 6))
        plt.title(str(df['provider'][0]) + " - Business days vs Weekend days duration CDF")

        bd_df = df_[(df_['business'] == True) & (df_['ride'] == True)]
        n, bins, patches = ax.hist(bd_df.duration, 1000, histtype='step',
                                   cumulative=True, label="Business day",
                                   rwidth=2.0, color=color(df), normed=1)

        we_df = df_[(df_['weekend'] == True) & (df_['ride'] == True)]
        n, bins, patches = ax.hist(we_df.duration, 1000, histtype='step',
                                   cumulative=True, label="Week end", linestyle="--",
                                   rwidth=2.0, color=color(df), normed=1)
        ax.legend(loc=4)
        ax.set_xlabel('Durations')
        ax.set_ylabel('CDF probability')
        plt.show()

    def car_vs_google(self, df):
        
        enj = df[(df['ride'] == True) &\
                     (df['short_trips'] == True) ]

        bis_y = bis_x = range(1,int(enj.duration.max()))

        fig, ax = plt.subplots(figsize=(13, 6))
        plt.title (str(df['provider'][0]) + " - Duration vs Google forecast time")
        ax.set_xlabel('Duration')
        ax.set_ylabel('Google Duration')

        ax.scatter(enj['duration_driving'],enj['duration'],
                   s=0.5, label= "Trips", color= color(df))
        ax.plot(bis_x,bis_y,linewidth=1.0, linestyle='--', 
                label= "Equal time bisector", color= "black")
        ax.set_xlabel("Google Forecast [m]")
        ax.set_ylabel("Measuerd Duration [m]")
        plt.axis([0, 50, 0, 50])
        plt.legend(loc=4)
        plt.show()

    def car_vs_google_comparison(self, df_provider1, df_provider2):
        plt.figure()
        df1 = df_provider1[(df_provider1['ride'] == True) &\
                     (df_provider1['short_trips'] == True) ]

        df2 = df_provider2[(df_provider2['ride'] == True) &\
                     (df_provider2['short_trips'] == True) ]

        bis_y = bis_x = range(1,int(df1.duration.max()))
        fig, ax = plt.subplots(figsize=(13, 6))
        plt.title ("Duration vs Google forecast time")
        ax.set_xlabel('Duration')
        ax.set_ylabel('Google Duration')
        ax.scatter(df1['duration_driving'],df1['duration'],
                   s=1, label= "Trips", color= color(df1))
        ax.scatter(df2['duration_driving'],df2['duration'],
                   s=1, label= "Trips", color= color(df2))
        ax.plot(bis_x,bis_y,linewidth=1.0, linestyle='--', 
                label= "Equal time bisector", color= "black")
        ax.set_xlabel("Google Forecast [m]")
        ax.set_ylabel("Measuerd Duration [m]")
        plt.axis([0, 50, 0, 50])
        plt.legend(loc=4)
        plt.show()
        
    def car_vs_transit(self, df):
        plt.figure()
        df_ = df[(df['ride'] == True) & \
                (df['short_trips'] == True) & \
                (df['tot_duration_google_transit'].isnull() == False) ]           
        fig, ax = plt.subplots(figsize=(13, 6))
        plt.title ("Duration vs Google Transit")
        ax.set_xlabel('Tbus [m]')
        ax.set_ylabel('Tcar [m]')
        ax.axis([0,100,0,45])                                       
        ax.scatter(df_.tot_duration_google_transit, df_.duration, color=color(df),s=0.5)
        ax.plot(df_.duration, df_.duration, color="green")
        plt.show()
                   
    def car_vs_transit_resampled(self, df_):
        plt.figure()
        df = self.slotted_df(df_)
        fig, ax = plt.subplots(figsize=(13, 6))       
        plt.axis([0, 80,0,40])
        df_ = df.set_index("start").resample("5Min").mean()
        ax.scatter(df_.tot_duration_google_transit, df_.duration, color=color(df),s=0.5)
        bis_y = bis_x = range(1,int(df_.duration.max()))
        ax.plot(bis_x, bis_y, color="green", linestyle='--', ) 
        plt.xlabel('Tbus [m]')
        plt.ylabel('Tcar [m]') 
        plt.show()        
        
    def car_vs_transit_bar(self, df_):
        plt.figure()
        df = self.slotted_df(df_)
        fig, ax = plt.subplots(figsize=(13, 6))       
        ax = df.groupby('slot')._id.count().apply(lambda x : x/float(len(df)))
        ax.plot.bar(color=color(df_))
        plt.xlabel('Google transit durations slots [m]')
        plt.ylabel('Booking Frequencies') 
        plt.show()
        
    def slotted_df(self, df_):
        df = df_[(df_['ride'] == True) & \
                 (df_['short_trips'] == True) & \
                 (df_['tot_duration_google_transit'].isnull() == False) &\
                 (df_['tot_duration_google_transit']< 100)] 
        df["slot"] = pd.Series()
        df.loc[df.tot_duration_google_transit < 10, "slot"] = 10
        df.loc[(df.tot_duration_google_transit < 20) & (df.tot_duration_google_transit > 10), "slot"] = 20
        df.loc[(df.tot_duration_google_transit < 30) & (df.tot_duration_google_transit > 20), "slot"] = 30
        df.loc[(df.tot_duration_google_transit < 40) & (df.tot_duration_google_transit > 30), "slot"] = 40
        df.loc[(df.tot_duration_google_transit < 50) & (df.tot_duration_google_transit > 40), "slot"] = 50
        df.loc[(df.tot_duration_google_transit < 60) & (df.tot_duration_google_transit > 50), "slot"] = 60
        df.loc[(df.tot_duration_google_transit < 70) & (df.tot_duration_google_transit > 60), "slot"] = 70
        df.loc[(df.tot_duration_google_transit < 80) & (df.tot_duration_google_transit > 70), "slot"] = 80
        df.loc[(df.tot_duration_google_transit < 90) & (df.tot_duration_google_transit > 80), "slot"] = 90
        df.loc[df.tot_duration_google_transit > 90, "slot"] = 100
        return df

    def faster_PT_hours(self, df1):
        plt.figure()

        df = df1[(df1['ride'] == True) & \
                (df1['short_trips'] == True) & \
                (df1['tot_duration_google_transit'].isnull() == False) ] 
        df3= df[(df.tot_duration_google_transit >= df.tot_duration_google_transit.quantile(q=0.01))\
                         & (df.tot_duration_google_transit <= df.tot_duration_google_transit.quantile(q=1.0-0.02))]      
        df2= df3[(df3.duration >= df3.duration.quantile(q=0.01))\
                         & (df3.duration <= df3.duration.quantile(q=1.0-0.02))]  
        df_ = df2[df2.tot_duration_google_transit < df2.duration].set_index("start")
        df_.groupby(df_.index.map(lambda t: t.hour)).tot_duration_google_transit.mean()\
                    .plot(figsize=(13, 6), marker='o', color=color(df), label = 'mean PT time when PT faster than CS')
        plt.xticks(np.arange(0,23+1, 1.0))
        plt.xlabel('Hours of a day')
        plt.legend()
        
    def faster_car_hours(self, df1):
        plt.figure()
        df = df1[(df1['ride'] == True) & \
                (df1['short_trips'] == True) & \
                (df1['tot_duration_google_transit'].isnull() == False) ] 
        df3= df[(df.tot_duration_google_transit >= df.tot_duration_google_transit.quantile(q=0.01))\
                         & (df.tot_duration_google_transit <= df.tot_duration_google_transit.quantile(q=1.0-0.02))]      
        df2= df3[(df3.duration >= df3.duration.quantile(q=0.01))\
                         & (df3.duration <= df3.duration.quantile(q=1.0-0.02))]  
        df_ = df2[df2.tot_duration_google_transit > df2.duration].set_index("start")
        df_.groupby(df_.index.map(lambda t: t.hour)).duration.mean()\
                    .plot(figsize=(13, 6), marker='o', color=color(df), label = 'mean CS when CS faster than PT')
        plt.xticks(np.arange(0,23+1, 1.0))
        plt.xlabel('Hours of a day')
        plt.legend()

#    def isocore(self, df, pos):
#
#        lat_s = pos[0]
#        lon_s = pos[1]
#        #'''Trying isocrone'''
#        #
##        lat_s = 45.0650653
##        lon_s = 7.6936148
#        #
#        #
##        lat_s = 45.0620829 #porta nuova coordinate
##        lon_s = 7.6762908
#        #time_lower = 5
#        #time_upper = 20
#        #isocrone = enjoy
#
#
#        df_isoc = df[(df["ride"] == True) &\
#                                (df["short_trips"] == True)]
#        
#        df_isoc['eucl_dist'] = df_isoc[['start_lat', 'start_lon', 'end_lat', 'end_lon']].apply\
#        (lambda x : haversine(x['start_lat'],x['start_lon'], lat_s, lon_s),axis=1)
#        
#        df_isoc = df_isoc[(df_isoc["eucl_dist"] <= 0.5)]
#        
#        zones = gpd.read_file("../../SHAPE/Zonizzazione.dbf")\
#               .to_crs({"init": "epsg:4326"})
#        zones_geo = zones["geometry"]
#        
#        fig, ax = plt.subplots(1,1,figsize=(10,10))
#        
#        zones_geo.plot(color="white",ax=ax)
#        ##del df_isoc["start_lat"]
#        ##del df_isoc["start_lon"]
#        ##-car2go
#        ax.set_xlim([7.6, 7.74])
#        ax.set_ylim([45.0, 45.11])
#        ##-enjoy
#        ##ax.set_xlim([7.6, 7.8])
#        ##ax.set_ylim([44.95,45.12])
#        colors=['red','green','orange', 'blue', 'yellow', 'gray']
#        #
#        hull= ConvexHull(df_isoc[['start_lon','start_lat']])
#        for simplex in hull.simplices:
#           plt.plot(df_isoc['start_lon'].iloc[simplex], df_isoc['start_lat'].iloc[simplex], color='red', linewidth=3, label='_nolegend_' )
#        #
#        for t in range(10,100,10):
#           df_isoc_time = df_isoc[(df_isoc['duration'] <= t)& (df_isoc['duration']>(t-10))]
#           if(len(df_isoc_time) > 0):
#               print 'in {} minuti : {}'.format(t, len(df_isoc_time))
#               if len(df_isoc_time) >=3:
#                   hull= ConvexHull(df_isoc_time[['end_lon','end_lat']])
#                   for simplex in hull.simplices:
#                       plt.plot(df_isoc_time['end_lon'].iloc[simplex], df_isoc_time['end_lat'].iloc[simplex],color=colors[t/10], linewidth=3, label='_nolegend_' )
#               df_isoc_time.plot.scatter(x="end_lon", y='end_lat', label=t, s=100, ax=ax, color=colors[t/10])
#          
#        plt.legend()
#                
    def faster_car_PTtime_hours(self, df1):
        plt.figure()
        df = df1[(df1['ride'] == True) & \
                (df1['short_trips'] == True) & \
                (df1['tot_duration_google_transit'].isnull() == False)] 
        df3= df[(df.tot_duration_google_transit >= df.tot_duration_google_transit.quantile(q=0.01))\
                         & (df.tot_duration_google_transit <= df.tot_duration_google_transit.quantile(q=1.0-0.02))]      
        df2= df3[(df3.duration >= df3.duration.quantile(q=0.01))\
                         & (df3.duration <= df3.duration.quantile(q=1.0-0.02))]  
        df_ = df2[df2.tot_duration_google_transit > df2.duration].set_index("start")
        df_.groupby(df_.index.map(lambda t: t.hour)).tot_duration_google_transit.mean()\
                    .plot(figsize=(13, 6), marker='o', color=color(df), label = 'mean PT time when CS faster')
        plt.xticks(np.arange(0,23+1, 1.0))
        plt.xlabel('Hours of a day')
        plt.legend()        
        
    def car_vs_pt(self, df1):
        plt.figure()
        df = df1[(df1['ride'] == True) & \
                 (df1['short_trips'] == True) & \
                 (df1['tot_duration_google_transit'].isnull() == False)]   
        df_ = df.set_index("start")
        df_.groupby(df_.index.map(lambda t: t.hour)).duration.mean().plot(figsize=(13, 6), marker='o', color=color(df), label = 'avg CS duration')
        df_.groupby(df_.index.map(lambda t: t.hour)).tot_duration_google_transit.mean().plot(figsize=(13, 6), marker='o', color='orange', label = 'avg PT duration')
        plt.xticks(np.arange(0,23+1, 1.0))
        plt.xlabel('Hours of a day')
        plt.legend()

    def cars_vs_pt(self, df1, df2):
        plt.figure()
        df = df1[(df1['ride'] == True) & \
                 (df1['short_trips'] == True) & \
                 (df1['tot_duration_google_transit'].isnull() == False)]   
        df_ = df.set_index("start")
        df_.groupby(df_.index.map(lambda t: t.hour)).duration.mean().plot(figsize=(13, 6), marker='o', color=color(df1), label = 'avg CS duration')
        _df = df2[(df2['ride'] == True) & \
                 (df2['short_trips'] == True) & \
                 (df2['tot_duration_google_transit'].isnull() == False)]   
        __df = _df.set_index("start")
        __df.groupby(__df.index.map(lambda t: t.hour)).duration.mean().plot(figsize=(13, 6), marker='o', color=color(df2), label = 'avg CS duration')
                
        dur_pt = (df_.groupby(df_.index.map(lambda t: t.hour)).tot_duration_google_transit.mean()\
         + __df.groupby(__df.index.map(lambda t: t.hour)).tot_duration_google_transit.mean())/2.0
        dur_pt.plot(figsize=(13, 6), marker='o', color='orange', label = 'avg PT duration')
        
        plt.xticks(np.arange(0,23+1, 1.0))
        plt.xlabel('Hours of a day')
        plt.legend()        