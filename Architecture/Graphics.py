import datetime

import numpy as np
import pandas as pd
import geopandas as gpd

from scipy import ndimage
from scipy.spatial import ConvexHull
from sklearn import linear_model

import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

from pandas.tools.plotting import scatter_matrix

from DataBaseProxy import *
dbp = DataBaseProxy()

import sys, os

def color(df):
    if df['provider'][2] == 'enjoy':
        return 'red'
    else:
        return 'blue'
        
def heatmap(lats, lons, hour, path, bins=(100,100), smoothing=1.3, cmap='jet'):
    
    heatmap, xedges, yedges = np.histogram2d(lats, lons, bins=bins)
    
    logheatmap = np.log(heatmap)
    logheatmap[np.isneginf(logheatmap)] = 0
    logheatmap = ndimage.filters.gaussian_filter(logheatmap, smoothing, mode='nearest')
    
    plt.imshow(heatmap, cmap=cmap, extent=[yedges[0], yedges[-1], xedges[-1], xedges[0]], 
               aspect='auto')
    plt.colorbar()
    plt.gca().invert_yaxis()
    plt.savefig(path+"/"+str(hour), dpi=250)
    plt.show()

    return

class Graphics():

    def __init__(self):
        pass

    def plot_samples(self, 
                     df, 
                     col, 
                     filter_col, 
                     provider,
                     quantile=0.0,
                     figsize=(13,6)):
        plt.ylabel(col)
        plt.xlabel("Samples")
        plt.title(provider + " - " + col + " samples")
        s = df.loc[df[filter_col] == True, col].dropna()
        s = s[(s >= s.quantile(q=quantile)) & (s <= s.quantile(q=1.0-quantile))]
        s.plot(marker='o', figsize=figsize, label=provider, color=color(df))

    def plot_samples_vs(self, 
                        enjoy_df, 
                        car2go_df, 
                        col, 
                        filter_col, 
                        quantile=0.0,
                        figsize=(13,6)):
        plt.figure()
        self.plot_samples(enjoy_df, col, filter_col, "Enjoy", quantile, figsize=figsize)
        self.plot_samples(car2go_df, col, filter_col, "Car2Go", quantile, figsize=figsize)
        plt.title("Enjoy vs car2go " + "- " + col + " - samples")
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
        
        plt.figure()
        plt.xlabel(col)
        plt.ylabel("Probability")
        if cumulative:
            plt.title("CDF")
        else:
            plt.title("PDF")
        s = df.loc[df[filter_col] == True, col].dropna()
        s = s[(s >= s.quantile(q=quantile)) & (s <= s.quantile(q=1.0-quantile))]
        s.hist(figsize=figsize, label=provider, color=color, cumulative=cumulative, normed = True, bins=bins)        

    def plot_system_utilization(self, 
                                df, 
                                col, 
                                filter_col, 
                                provider, 
                                color,
                                fleet,
                                freq="30Min",
                                quantile=0.0,
                                figsize=(13,6)):
        
        plt.title("System utilization")
        df_ = df.loc[df[filter_col] == True].set_index("start")
        s = df_[col].dropna()
        s = s[(s >= s.quantile(q=quantile)) & (s <= s.quantile(q=1.0-quantile))]
        s = s.resample(freq).count()/float(len(fleet))
        s.plot(marker='o', figsize=figsize, label=provider, color=color)

    def plot_system_utilization_vs(self,
                                enjoy_df, 
                                car2go_df, 
                                col, 
                                filter_col,
                                fleet,
                                freq="30Min",
                                quantile=0.0,
                                figsize=(13,6)):

        plt.figure()
        self.plot_system_utilization(enjoy_df, col, filter_col, "Enjoy", "red", fleet=fleet, freq=freq, quantile=quantile)
        self.plot_system_utilization(car2go_df, col, filter_col, "Car2Go", "blue", fleet=fleet, freq=freq, quantile=quantile)
        plt.legend()

    def plot_aggregated_count(self, 
                                df, 
                                col, 
                                filter_col, 
                                provider, 
                                color,
                                freq="30Min",
                                quantile=0.0,
                                figsize=(13,6)):
        
        plt.title("Number of bookings aggregated " + freq)
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
        
        plt.ylabel(col)
        plt.title("Aggregated " + col + " - " + provider)
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
        plt.title("Aggregated " + col + " - Enjoy vs car2go" )
        plt.legend()        

    def plot_aggregated_sum(self, 
                        df, 
                        col, 
                        filter_col, 
                        provider, 
                        color,
                        freq="1440Min",
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
                            freq="1440Min",
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
        
        plt.title("Number of daily bookings - " + provider)
        plt.xlabel("Daily hours")
        df_ = df.loc[df[filter_col] == True].set_index("start")
        s = df_[col].dropna()
        s = s[(s >= s.quantile(q=quantile)) & (s <= s.quantile(q=1.0-quantile))]
        div = float(len(s.groupby(s.index.map(lambda t: t.date))))
        print "GIORNI + " + str(div)
        s = s.groupby(s.index.map(lambda t: t.hour)).count()
        s_ = s/div
        s_.plot(marker='o', figsize=figsize, label=provider, color=color)
        
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
        
        plt.xlabel("Daily hours")
        plt.title(provider + " - " +  col + " - daily mean" )
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
        
        plt.title(provider + " - " + col + " - daily sum")
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
        
        plt.figure(figsize = (13,6))
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
        plt.axis([0, 50, 0, 1.1])
        plt.legend(loc=4)

    def cdf_weeks_distance(self, df1, df2):

        plt.figure(figsize = (13,6))
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
        ax.set_ylabel("Measured Duration [m]")
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
        bis_y = bis_x = range(1,int(df_.duration.max()))
        if color(df) == "blue":
            ax.plot(bis_x, bis_y, color="white", linestyle = '--', label = 'time bisector')
        elif color(df) == "red":
            ax.plot(bis_x, bis_y, color="black", linestyle = '--', label = 'time bisector')
        # Create linear regression object
        x = df_.tot_duration_google_transit.values
        y = df_.duration.values
        x = x.reshape(len(x), 1)
        y = y.reshape(len(y), 1)
        regr = linear_model.LinearRegression()
        regr.fit(x, y)
        # Train the model using the training sets
        ax.plot(x, regr.predict(x), color='black', linewidth=1, linestyle='-', label = 'linear regression')

        plt.show()
                   
    def car_vs_transit_resampled(self, df_):
        plt.figure()
        df = self.slotted_df(df_)
        fig, ax = plt.subplots(figsize=(13, 6))       
        plt.axis([0, 80,0,40])
        df_ = df.set_index("start").resample("5Min").mean()
        ax.scatter(df_.tot_duration_google_transit, df_.duration, color=color(df),s=0.5, label = 'resampled')
        bis_y = bis_x = range(1,int(df_.duration.max()))
        ax.plot(bis_x, bis_y, color="black", linestyle='--' ) 

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
        plt.ylabel('Booking Probability') 
        plt.show()
        
    def slotted_df(self, df_):
        df = df_[(df_['ride'] == True) & \
                 (df_['short_trips'] == True) & \
                 (df_['tot_duration_google_transit'].isnull() == False) &\
                 (df_['tot_duration_google_transit']< 100)] 
        df["slot"] = pd.Series()
        delta = 5.0
        df.loc[np.floor(df.tot_duration_google_transit/delta)*delta]
        df.loc[df.tot_duration_google_transit < 5, "slot"] = 5
        df.loc[(df.tot_duration_google_transit < 10) & (df.tot_duration_google_transit > 5), "slot"] = 10
        df.loc[(df.tot_duration_google_transit < 15) & (df.tot_duration_google_transit > 10), "slot"] = 15
        df.loc[(df.tot_duration_google_transit < 20) & (df.tot_duration_google_transit > 15), "slot"] = 20
        df.loc[(df.tot_duration_google_transit < 25) & (df.tot_duration_google_transit > 20), "slot"] = 25
        df.loc[(df.tot_duration_google_transit < 30) & (df.tot_duration_google_transit > 25), "slot"] = 30
        df.loc[(df.tot_duration_google_transit < 35) & (df.tot_duration_google_transit > 30), "slot"] = 35
        df.loc[(df.tot_duration_google_transit < 40) & (df.tot_duration_google_transit > 35), "slot"] = 40
        df.loc[(df.tot_duration_google_transit < 45) & (df.tot_duration_google_transit > 40), "slot"] = 45
        df.loc[(df.tot_duration_google_transit < 50) & (df.tot_duration_google_transit > 45), "slot"] = 50
        df.loc[df.tot_duration_google_transit > 50, "slot"] = 50.1
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
                    .plot(figsize=(13, 6), marker='o', color=color(df), label = 'mean CS time when CS faster than PT')
        plt.xticks(np.arange(0,23+1, 1.0))
        plt.xlabel('Hours of a day')
        plt.legend()
                
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
        
    def car_pt(self, df1):
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

    def car_pt_vs(self, df1, df2):
        plt.figure()
        df = df1[(df1['ride'] == True) & \
                 (df1['short_trips'] == True) & \
                 (df1['duration_driving'].isnull() == False) & \
                 (df1['tot_duration_google_transit'].isnull() == False)]   
        df_ = df.set_index("start")
        df_.groupby(df_.index.map(lambda t: t.hour)).duration.mean().plot(figsize=(13, 6), marker='o', color=color(df1), label = 'avg CS duration')
        _df = df2[(df2['ride'] == True) & \
                 (df2['short_trips'] == True) & \
                 (df1['duration_driving'].isnull() == False) & \
                 (df2['tot_duration_google_transit'].isnull() == False)]   
        __df = _df.set_index("start")
        __df.groupby(__df.index.map(lambda t: t.hour)).duration.mean().plot(figsize=(13, 6), marker='o', color=color(df2), label = 'avg CS duration')
                
        dur_pt = (df_.groupby(df_.index.map(lambda t: t.hour)).tot_duration_google_transit.mean()\
         + __df.groupby(__df.index.map(lambda t: t.hour)).tot_duration_google_transit.mean())/2.0
        dur_pt.plot(figsize=(13, 6), marker='o', color='orange', label = 'avg PT duration')

        dur_pt = (df_.groupby(df_.index.map(lambda t: t.hour)).duration_driving.mean()\
         + __df.groupby(__df.index.map(lambda t: t.hour)).duration_driving.mean())/2.0
        dur_pt.plot(figsize=(13, 6), marker='o', color='purple', label = 'avg car duration')
        
        plt.xticks(np.arange(0,23+1, 1.0))
        plt.xlabel('Hours of a day')
        plt.legend()   

    def isocrono(self, df, pos):

       lat_s = pos[0]
       lon_s = pos[1]

       df_isoc = df[(df["ride"] == True) &\
                               (df["short_trips"] == True)]
       
       df_isoc['eucl_dist'] = df_isoc[['start_lat', 'start_lon', 'end_lat', 'end_lon']].apply\
       (lambda x : haversine(x['start_lat'],x['start_lon'], lat_s, lon_s),axis=1)
       
       df_isoc = df_isoc[(df_isoc["eucl_dist"] <= 0.5)]
       
       zones = gpd.read_file("../../SHAPE/Zonizzazione.dbf")\
              .to_crs({"init": "epsg:4326"})
       zones_geo = zones["geometry"]
       
       fig, ax = plt.subplots(1,1,figsize=(10,10))
       
       zones_geo.plot(color="white",ax=ax)
       ##del df_isoc["start_lat"]
       ##del df_isoc["start_lon"]
       ##-car2go
       ax.set_xlim([7.6, 7.74])
       ax.set_ylim([45.0, 45.11])
       ##-enjoy
       ##ax.set_xlim([7.6, 7.8])
       ##ax.set_ylim([44.95,45.12])
       colors=['red','green','orange', 'blue', 'yellow', 'gray']
       #
       hull= ConvexHull(df_isoc[['start_lon','start_lat']])
       for simplex in hull.simplices:
          plt.plot(df_isoc['start_lon'].iloc[simplex], df_isoc['start_lat'].iloc[simplex], color='red', linewidth=3, label='_nolegend_' )
       #
       for t in range(10,100,10):
          df_isoc_time = df_isoc[(df_isoc['riding_time'] <= t)& (df_isoc['riding_time']>(t-10))]
          if(len(df_isoc_time) > 0):
              print 'in {} minuti : {}'.format(t, len(df_isoc_time))
              if len(df_isoc_time) >=3:
                  hull= ConvexHull(df_isoc_time[['end_lon','end_lat']])
                  for simplex in hull.simplices:
                      plt.plot(df_isoc_time['end_lon'].iloc[simplex], df_isoc_time['end_lat'].iloc[simplex],color=colors[t/10], linewidth=3, label='_nolegend_' )
              df_isoc_time.plot.scatter(x="end_lon", y='end_lat', label=t, s=100, ax=ax, color=colors[t/10])
       plt.legend()

    def isocost(self, df, pos):

        lat_s = pos[0]
        lon_s = pos[1]
        
        df_isoc = df[(df["ride"] == True) &\
                                (df["short_trips"] == True)]

        df_isoc['eucl_dist'] = df_isoc[['start_lat', 'start_lon', 'end_lat', 'end_lon']].apply\
        (lambda x : haversine(x['start_lat'],x['start_lon'], lat_s, lon_s),axis=1)
        
        df_isoc = df_isoc[(df_isoc["eucl_dist"] <= 0.5)]
        
        zones = gpd.read_file("../../SHAPE/Zonizzazione.dbf")\
               .to_crs({"init": "epsg:4326"})
        zones_geo = zones["geometry"]

        fig, ax = plt.subplots(1,1,figsize=(10,10))
        zones_geo.plot(color="white",ax=ax)
        ax.set_xlim([7.6, 7.74])
        ax.set_ylim([45.0, 45.11])

        colors=['red','green','orange', 'blue', 'yellow', 'gray']

        hull= ConvexHull(df_isoc[['start_lon','start_lat']])
        for simplex in hull.simplices:
           plt.plot(df_isoc['start_lon'].iloc[simplex], df_isoc['start_lat'].iloc[simplex], color='red', linewidth=3, label='_nolegend_' )

        for t in range(2,8,2):
           df_isoc_time = df_isoc[(df_isoc['max_bill'] <= t) & (df_isoc['max_bill']>(t-2))]
           if(len(df_isoc_time) > 0):
               print 'in {} minuti : {}'.format(t, len(df_isoc_time))
               if len(df_isoc_time) >=3:
                   hull= ConvexHull(df_isoc_time[['end_lon','end_lat']])
                   for simplex in hull.simplices:
                       plt.plot(df_isoc_time['end_lon'].iloc[simplex], df_isoc_time['end_lat'].iloc[simplex],color=colors[t/2], linewidth=3, label='_nolegend_' )
               df_isoc_time.plot.scatter(x="end_lon", y='end_lat', label=str(t)+' euro', s=100, ax=ax, color=colors[t/2])
               
    def heatmaps_per_hour(self, df):
            
            df_ = df[(df['start_lon'] >= 7.60) &\
                     (df['end_lon'] <= 7.80) &\
                     (df['start_lat'] >= 45) &\
                     (df['end_lat'] <= 45.25)]
            df_["hour"] = df_["start"].apply(lambda d: d.hour)
            
            path = "../Images/"
            if os.path.isdir(path) == False:
                os.makedirs(path)
                
            provider = df_["provider"].iloc[0]
            path += "../Images/"+provider
            if os.path.isdir(path) == False:
                os.makedirs(path)
                
            if os.path.isdir(path + "/initial_destination") == False:
                os.makedirs(path + "/initial_destination")
            i_path = path + "/initial_destination"
                
            if os.path.isdir(path + "/final_destination") == False:
                os.makedirs(path + "/final_destination")
            f_path = path + "/final_destination"
                
            grouped = df_.groupby("hour")
            for hour in range(24):
                zones = gpd.read_file("../../SHAPE/Zonizzazione.dbf").to_crs({"init": "epsg:4326"})
                zones_geo = zones["geometry"]
                zones_geo.plot(color="white").set_title(provider+" - Initial book position - "+str(hour) + ":00")
                path = "/../Images/"
                #heatmap defined at top
                heatmap(grouped.get_group(hour).end_lat.values, 
                        grouped.get_group(hour).end_lon.values,            
                        hour, i_path, bins=20)
                
            for hour in range(24):
                zones = gpd.read_file("../../SHAPE/Zonizzazione.dbf").to_crs({"init": "epsg:4326"})
                zones_geo = zones["geometry"]
                zones_geo.plot(color="white").set_title(provider+" - Final book position - "+str(hour) + ":00")
                path = "/../Images/"
                #heatmap defined at top
                heatmap(grouped.get_group(hour).end_lat.values, 
                        grouped.get_group(hour).end_lon.values,            
                        hour, f_path, bins=20)
            return
