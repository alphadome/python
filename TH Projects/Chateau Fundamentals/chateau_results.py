# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 13:07:55 2019

@author: thoma
"""

from chateau_weather import Chateau
from chateau_data import Chateau_data
from chateau_comb_new import Chateau_comb
from chateau_rating import Chateau_rating
import numpy as np
import ast
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta
import json
import statistics
from geopy.geocoders import Nominatim
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier 
from sklearn.neural_network import MLPRegressor
from chateau_tools import eomonth, dict_unpacker, vintage_monthly_weather_dict, average_seasonal_weather_dict, seasonal_weather_dict
from scipy.optimize import curve_fit


class Chateau_results():

    def __init__(self, address):
        """initialize attributes to define a stock"""
        self.address = address
        
    def price_vs_rating_cubic(self):
        """return the scatter plot across years of the month"""
       
        def proceed_with_method():
            rating_dict_raw = Chateau_rating(self.address).get_rating_data()
            price_dict_raw = Chateau_data(self.address).get_price_data()
            
            rating_dict = dict_unpacker(rating_dict_raw)
            price_dict = dict_unpacker(price_dict_raw)
            
            x_values, y_values, n_values = [], [], []
            
            for key, price in price_dict.items():
                if key in rating_dict.keys() and key > datetime(1970,12,31):
                    y_values.append(price)
                    x_values.append(rating_dict[key])
                    n_values.append(key.year)
                    
      
            #calculate best fit line
            x = x_values
            y = y_values
            z = np.polyfit(x, y, 3)
            z_formatted = np.ndarray.tolist(z)
            p = np.poly1d(z)
            xp = np.linspace(min(x_values), max(x_values), 100) 
            
            #calculate correlation coefficient
            correl_y = p(x)
            #A = np.vstack([x, np.ones(len(x))]).T
            #m, c = np.linalg.lstsq(A, correl_y, rcond=None)[0]
            #print(m, c)
            R = np.corrcoef(y, correl_y)
            cor = R.item(1) #R is a 2x2 matrix so take the correct entry
            print("\nCorrelation coefficient: " + str('%0.2f' % cor))
                       
            print("\nSuggested polynomial a*x^3 + bx^2 + cx + d has [a, b, c, d]: "
                  + str('%0.2f' % z_formatted[0]) +", "
                  + str('%0.2f' % z_formatted[1]) +", "
                  + str('%0.2f' % z_formatted[2]) +", "
                  + str('%0.2f' % z_formatted[3]))
    
                        
            #Size the output
            fig = plt.figure(dpi=128, figsize=(10,6))
            
            #Chart gridlines
            plt.grid(None, 'major', 'both')
            
            #Axis tick formats
            for tick in plt.gca().get_xticklabels():
                tick.set_fontname("Calibri")
                tick.set_fontsize(12)
                tick.set_rotation('vertical')
            for tick in plt.gca().get_yticklabels():
                tick.set_fontname("Calibri")
                tick.set_fontsize(12)
            
            #Axis labels and formats
            
            # axis 1
            color = 'tab:blue'
            plt.xlabel("Global wine rating", fontsize =12)
            #plt.xticks(np.arange(x_values[11], x_values[0], 2))
            plt.ylabel("Price", color='black', fontsize =12)
            plt.scatter(x_values, y_values, color=color)
            plt.plot(xp, p(xp), color = 'red')
            plt.tick_params(axis='y', labelcolor=color)
            
            for i, txt in enumerate(n_values):
                plt.annotate(txt, (x[i], y[i]))
            
                       
            #remove borders
            plt.gca().spines['top'].set_visible(False)
            
            #Chart title
            plt.title(str(self.address)+ " Rating vs Price", fontsize = 14)
            
            #Show chart
            plt.show()

        proceed_with_method() 


    def price_vs_rating_exp(self):
        """return the scatter plot across years of the month"""
       
        def proceed_with_method():
            rating_dict_raw = Chateau_rating(self.address).get_rating_data()
            price_dict_raw = Chateau_data(self.address).get_price_data()
            
            rating_dict = dict_unpacker(rating_dict_raw)
            price_dict = dict_unpacker(price_dict_raw)
            
            x_values, y_values, n_values = [], [], []
            
            for key, price in price_dict.items():
                if key in rating_dict.keys() and key > datetime(1970,12,31):
                    y_values.append(price)
                    x_values.append(rating_dict[key])
                    n_values.append(key.year)           
            
            x = x_values
            y = y_values
            #A = curve_fit(lambda t,a,b: a*np.exp(b*t),  x,  y)
            B = curve_fit(lambda t,a,b: a*np.exp(b*t),  x,  y,  p0=(300, 0.1))
            
            
            def func(x):
                a = np.ndarray.tolist(B[0])[0]
                b = np.ndarray.tolist(B[0])[1]
                f = a * np.exp(b*x)
                return f
            
            #calculate best fit line
            xp = np.linspace(min(x_values), max(x_values), 100) 
            
            #calculate correlation coefficient
            correl_y = []
            for item in x_values:
                correl_y.append(func(item))
            
            #A = np.vstack([x, np.ones(len(x))]).T
            #m, c = np.linalg.lstsq(A, correl_y, rcond=None)[0]
            #print(m, c)
            R = np.corrcoef(y, correl_y)
            cor = R.item(1) #R is a 2x2 matrix so take the correct entry
            print("\nCorrelation coefficient: " + str('%0.2f' % cor))
                       
            print("\nSuggested exponential a * exp (bx) has [a, b]: " + str('%0.2f' %np.ndarray.tolist(B[0])[0]) + ", " + str('%0.2f' % np.ndarray.tolist(B[0])[1]))
    
                        
            #Size the output
            fig = plt.figure(dpi=128, figsize=(10,6))
            
            #Chart gridlines
            plt.grid(None, 'major', 'both')
            
            #Axis tick formats
            for tick in plt.gca().get_xticklabels():
                tick.set_fontname("Calibri")
                tick.set_fontsize(12)
                tick.set_rotation('vertical')
            for tick in plt.gca().get_yticklabels():
                tick.set_fontname("Calibri")
                tick.set_fontsize(12)
            
            #Axis labels and formats
            
            # axis 1
            color = 'tab:blue'
            plt.xlabel("Global wine rating", fontsize =12)
            #plt.xticks(np.arange(x_values[11], x_values[0], 2))
            plt.ylabel("Price", color='black', fontsize =12)
            plt.scatter(x_values, y_values, color=color)
            plt.plot(xp, func(xp), color = 'red')
            plt.tick_params(axis='y', labelcolor=color)
            
            for i, txt in enumerate(n_values):
                plt.annotate(txt, (x[i], y[i]))
            
                       
            #remove borders
            plt.gca().spines['top'].set_visible(False)
            
            #Chart title
            plt.title(str(self.address)+ " Rating vs Price", fontsize = 14)
            
            #Show chart
            plt.show()

        proceed_with_method()

    
    def rainfall_correlation(self, start_month, end_month, update=''):
        """returns the weather profile of the vintage vs average seasonality"""
       
        def proceed_with_method():
           
            weather_dict_p_raw = Chateau(self.address).weather_dict('p')
            weather_dict_v_raw = Chateau(self.address).weather_dict('v')

           
            weather_dict_p = dict_unpacker(weather_dict_p_raw)
            weather_dict_v = dict_unpacker(weather_dict_v_raw)
            
            rating_dict_raw = Chateau_rating(self.address).get_rating_data()
            rating_dict = dict_unpacker(rating_dict_raw)
            
            seasonal_weather_dict_p = average_seasonal_weather_dict(weather_dict_p)
            seasonal_weather_dict_v = average_seasonal_weather_dict(weather_dict_v)

            price_dict_raw = Chateau_data(self.address).get_price_data()
            
            price_dict = dict_unpacker(price_dict_raw)
            
            x_values, y_values, n_values = [], [], []
            
            for key, rating in rating_dict.items():
                if key in rating_dict.keys() and key > datetime(1970,12,31)  and rating > 96:
                    
                    p_values, v_values = [], []

                    for w_date, data in weather_dict_p.items():
                        if w_date < eomonth(key.year, end_month-1) and w_date > eomonth(key.year, start_month-1):
                            p_values.append(float(data))
                    
                    if p_values == []:
                        None
                    else:
                        av = statistics.mean(p_values)
                        x_values.append(av)
                        y_values.append(rating)
                        n_values.append(key.year) 

      
            #calculate best fit line
            x = x_values
            y = y_values
            z = np.polyfit(x, y, 2)
            z_formatted = np.ndarray.tolist(z)
            p = np.poly1d(z)
            xp = np.linspace(min(x_values), max(x_values), 100) 
            
            #calculate correlation coefficient
            correl_y = p(x)
            #A = np.vstack([x, np.ones(len(x))]).T
            #m, c = np.linalg.lstsq(A, correl_y, rcond=None)[0]
            #print(m, c)
            R = np.corrcoef(y, correl_y)
            cor = R.item(1) #R is a 2x2 matrix so take the correct entry
            print("\n For month:" + str(start_month))

            print("\nCorrelation coefficient: " + str('%0.2f' % cor))
                       
            print("\nSuggested polynomial a*x^2 + bx + c has [a, b, c]: "
                  + str('%0.2f' % z_formatted[0]) +", "
                  + str('%0.2f' % z_formatted[1]) +", "
                  + str('%0.2f' % z_formatted[2]))                  #+ str('%0.2f' % z_formatted[3]))
    
                        
            #Size the output
            fig = plt.figure(dpi=128, figsize=(10,6))
            
            #Chart gridlines
            plt.grid(None, 'major', 'both')
            
            #Axis tick formats
            for tick in plt.gca().get_xticklabels():
                tick.set_fontname("Calibri")
                tick.set_fontsize(12)
                tick.set_rotation('vertical')
            for tick in plt.gca().get_yticklabels():
                tick.set_fontname("Calibri")
                tick.set_fontsize(12)
            
            #Axis labels and formats
            
            # axis 1
            color = 'tab:blue'
            plt.xlabel("Rainfall", fontsize =12)
            #plt.xticks(np.arange(x_values[11], x_values[0], 2))
            plt.ylabel("Rating", color='black', fontsize =12)
            plt.scatter(x_values, y_values, color=color)
            plt.plot(xp, p(xp), color = 'red')
            plt.tick_params(axis='y', labelcolor=color)
            
            for i, txt in enumerate(n_values):
                plt.annotate(txt, (x[i], y[i]))
            
                       
            #remove borders
            plt.gca().spines['top'].set_visible(False)
            
            #Chart title
            plt.title(str(self.address)+ " Rating vs Price", fontsize = 14)
            
            #Show chart
            plt.show()

        proceed_with_method()  

    def temp_correlation(self, start_month, end_month, update=''):
        """returns the weather profile of the vintage vs average seasonality"""
       
        def proceed_with_method():
           
            weather_dict_p_raw = Chateau(self.address).weather_dict('p')
            weather_dict_v_raw = Chateau(self.address).weather_dict('v')

           
            weather_dict_p = dict_unpacker(weather_dict_p_raw)
            weather_dict_v = dict_unpacker(weather_dict_v_raw)
            
            rating_dict_raw = Chateau_rating(self.address).get_rating_data()
            rating_dict = dict_unpacker(rating_dict_raw)
            
            seasonal_weather_dict_p = average_seasonal_weather_dict(weather_dict_p)
            seasonal_weather_dict_v = average_seasonal_weather_dict(weather_dict_v)

            price_dict_raw = Chateau_data(self.address).get_price_data()
            
            price_dict = dict_unpacker(price_dict_raw)
            
            x_values, y_values, n_values = [], [], []
            
            for key, rating in rating_dict.items():
                if key in rating_dict.keys() and key > datetime(1970,12,31) and rating > 96:
                    
                    p_values, v_values = [], []

                    for w_date, data in weather_dict_v.items():
                        if w_date < eomonth(key.year, end_month-1) and w_date > eomonth(key.year, start_month-1):
                            v_values.append(float(data))
                    
                    if v_values == []:
                        None
                    else:
                        av = statistics.mean(v_values)
                        x_values.append(av)
                        y_values.append(rating)
                        n_values.append(key.year)                    
      
            #calculate best fit line
            x = x_values
            y = y_values
            z = np.polyfit(x, y, 2)
            z_formatted = np.ndarray.tolist(z)
            p = np.poly1d(z)
            xp = np.linspace(min(x_values), max(x_values), 100) 
            
            #calculate correlation coefficient
            correl_y = p(x)
            #A = np.vstack([x, np.ones(len(x))]).T
            #m, c = np.linalg.lstsq(A, correl_y, rcond=None)[0]
            #print(m, c)
            R = np.corrcoef(y, correl_y)
            cor = R.item(1) #R is a 2x2 matrix so take the correct entry
            print("\n For month:" + str(start_month))
            print("\nCorrelation coefficient: " + str('%0.2f' % cor))
                       
            print("\nSuggested polynomial a*x^2 + bx + c has [a, b, c]: "
                  + str('%0.2f' % z_formatted[0]) +", "
                  + str('%0.2f' % z_formatted[1]) +", "
                  + str('%0.2f' % z_formatted[2]))                  #+ str('%0.2f' % z_formatted[3]))
    
                        
            #Size the output
            fig = plt.figure(dpi=128, figsize=(10,6))
            
            #Chart gridlines
            plt.grid(None, 'major', 'both')
            
            #Axis tick formats
            for tick in plt.gca().get_xticklabels():
                tick.set_fontname("Calibri")
                tick.set_fontsize(12)
                tick.set_rotation('vertical')
            for tick in plt.gca().get_yticklabels():
                tick.set_fontname("Calibri")
                tick.set_fontsize(12)
            
            #Axis labels and formats
            
            # axis 1
            color = 'tab:blue'
            plt.xlabel("Temp", fontsize =12)
            #plt.xticks(np.arange(x_values[11], x_values[0], 2))
            plt.ylabel("Rating", color='black', fontsize =12)
            plt.scatter(x_values, y_values, color=color)
            plt.plot(xp, p(xp), color = 'red')
            plt.tick_params(axis='y', labelcolor=color)
            
            for i, txt in enumerate(n_values):
                plt.annotate(txt, (x[i], y[i]))
            
                       
            #remove borders
            plt.gca().spines['top'].set_visible(False)
            
            #Chart title
            plt.title(str(self.address)+ " Rating vs Price", fontsize = 14)
            
            #Show chart
            plt.show()

        proceed_with_method()  



    def ranking_correlation(self, update=''):
        """returns the weather profile of the vintage vs average seasonality"""
       
        def proceed_with_method():
           
            weather_dict_p_raw = Chateau(self.address).weather_dict('p')
            weather_dict_v_raw = Chateau(self.address).weather_dict('v')
           
            weather_dict_p = dict_unpacker(weather_dict_p_raw)
            weather_dict_v = dict_unpacker(weather_dict_v_raw)
            
            rating_dict_raw = Chateau_rating(self.address).get_rating_data()
            rating_dict = dict_unpacker(rating_dict_raw)
            
            seasonal_weather_dict_p = seasonal_weather_dict(weather_dict_p)
            seasonal_weather_dict_v = seasonal_weather_dict(weather_dict_v)
            
            av_seasonal_weather_dict_p = average_seasonal_weather_dict(weather_dict_p)
            av_seasonal_weather_dict_v = average_seasonal_weather_dict(weather_dict_v)
            

            x_values, y_values, n_values = [], [], []
            
            for key, rating in rating_dict.items():
                if key > datetime(1970,12,31) and int(key.year) > 1970:
                    
                    strike_v = 0
                    strike_p = 0

                    for i in range(4,10):
                        try:
                            if seasonal_weather_dict_v[eomonth(key.year, i)] < av_seasonal_weather_dict_v[i]:
                                
                                if i in range(7,10):
                                    a = 0.5
                                else:
                                    a = 1
                                
                                strike_v = strike_v + (av_seasonal_weather_dict_v[i]-seasonal_weather_dict_v[eomonth(key.year, i)])
                        
                        except Exception:
                            None
                            
                    for i in range(5,10):
                        try:
                            if seasonal_weather_dict_p[eomonth(key.year, i)] > 1.5 * av_seasonal_weather_dict_p[i]:
                                strike_p = strike_p + (seasonal_weather_dict_p[eomonth(key.year, i)] - av_seasonal_weather_dict_p[i])                        
                        except Exception:
                            None
        
                x_values.append(strike_v + strike_p)
                y_values.append(rating)
                n_values.append(key.year)                         


               
                


            #calculate best fit line
            x = x_values
            y = y_values
            z = np.polyfit(x, y, 1)
            z_formatted = np.ndarray.tolist(z)
            p = np.poly1d(z)
            xp = np.linspace(min(x_values), max(x_values), 100) 
            
            #calculate correlation coefficient
            correl_y = p(x)
            #A = np.vstack([x, np.ones(len(x))]).T
            #m, c = np.linalg.lstsq(A, correl_y, rcond=None)[0]
            #print(m, c)
            R = np.corrcoef(y, correl_y)
            cor = R.item(1) #R is a 2x2 matrix so take the correct entry
            print("\nCorrelation coefficient: " + str('%0.2f' % cor))
                       
            print("\nSuggested polynomial a*x + b has [a, b]: "
                  + str('%0.2f' % z_formatted[0]) +", "
                  + str('%0.2f' % z_formatted[1]))                  #+ str('%0.2f' % z_formatted[3]))
    
                        
            #Size the output
            fig = plt.figure(dpi=128, figsize=(10,6))
            
            #Chart gridlines
            plt.grid(None, 'major', 'both')
            
            #Axis tick formats
            for tick in plt.gca().get_xticklabels():
                tick.set_fontname("Calibri")
                tick.set_fontsize(12)
                tick.set_rotation('vertical')
            for tick in plt.gca().get_yticklabels():
                tick.set_fontname("Calibri")
                tick.set_fontsize(12)
            
            #Axis labels and formats
            
            # axis 1
            color = 'tab:blue'
            plt.xlabel("Temp", fontsize =12)
            #plt.xticks(np.arange(x_values[11], x_values[0], 2))
            plt.ylabel("Rating", color='black', fontsize =12)
            plt.scatter(x_values, y_values, color=color)
            plt.plot(xp, p(xp), color = 'red')
            plt.tick_params(axis='y', labelcolor=color)
            
            for i, txt in enumerate(n_values):
                plt.annotate(txt, (x[i], y[i]))
            
                       
            #remove borders
            plt.gca().spines['top'].set_visible(False)
            
            #Chart title
            plt.title(str(self.address)+ " Rating vs Price", fontsize = 14)
            
            #Show chart
            plt.show()

        proceed_with_method()  



    def multi_regression(self):
        """analysis of vintage rule strikes vs price"""
        def proceed_with_method():

          
            weather_dict_p_raw = Chateau(self.address).weather_dict('p')
            weather_dict_v_raw = Chateau(self.address).weather_dict('v')

           
            weather_dict_p = dict_unpacker(weather_dict_p_raw)
            weather_dict_v = dict_unpacker(weather_dict_v_raw)
            
            rating_dict_raw = Chateau_rating(self.address).get_rating_data()
            rating_dict = dict_unpacker(rating_dict_raw)
            
            seasonal_weather_dict_p = seasonal_weather_dict(weather_dict_p)
            seasonal_weather_dict_v = seasonal_weather_dict(weather_dict_v)

           
            av_seasonal_weather_dict_p = average_seasonal_weather_dict(weather_dict_p)
            av_seasonal_weather_dict_v = average_seasonal_weather_dict(weather_dict_v)
 
            
            x_values_train, y_values_train, n_values_train = [], [], []
            x_values_test, y_values_test, n_values_test = [], [], []
            
            s_values_train, r_values_train, d_values_train = [], [], []
            s_values_test, r_values_test, d_values_test = [], [], []
            
            def func_p(x):
                f = -0.57 *x*x + 2.23 * x + 92.78
                return f
            
            def func_v(x):
                f = -0.29*x*x + 12.85*x -43.96
                return f
            
            
            for key, rating in rating_dict.items():
                if key > datetime(1970,12,31) and key < datetime(2000,12,31) and int(key.year) > 1970:
                    for i in range(6,7):
                        try:
                            av_v = seasonal_weather_dict_v[eomonth(key.year, i)]
                            av_p = seasonal_weather_dict_p[eomonth(key.year, i)]

                            x_values_train.append([func_v(av_v), func_p(av_p)])
                            y_values_train.append(rating)
                            n_values_train.append(key.year)                              
                        
                        except Exception:
                            None
                
                if key >= datetime(2000,12,31) and int(key.year) > 1970:
                    for i in range(6,7):
                        try:
                            av_v = seasonal_weather_dict_v[eomonth(key.year, i)]
                            av_p = seasonal_weather_dict_p[eomonth(key.year, i)]

                            x_values_test.append([func_v(av_v), func_p(av_p)])
                            y_values_test.append(rating)
                            n_values_test.append(key.year)                              
                        
                        except Exception:
                            None


                if key > datetime(1970,12,31) and key < datetime(2000,12,31) and int(key.year) > 1970:
                    
                    strike_v = 0
                    strike_p = 0

                    for i in range(4,10):
                        try:
                            if seasonal_weather_dict_v[eomonth(key.year, i)] < av_seasonal_weather_dict_v[i]:
                                
                                if i in range(7,10):
                                    a = 0.5
                                else:
                                    a = 1
                                
                                strike_v = strike_v + 1
                        
                        except Exception:
                            None
                            
                    for i in range(5,10):
                        try:
                            if seasonal_weather_dict_p[eomonth(key.year, i)] > 1.5 * av_seasonal_weather_dict_p[i]:
                                strike_p = strike_p + 1                       
                        except Exception:
                            None
        
                    s_values_train.append(strike_v + strike_p)
                    r_values_train.append(rating)
                    d_values_train.append(key.year)             

                if key >= datetime(2000,12,31) and int(key.year) > 1970:
                    
                    strike_v = 0
                    strike_p = 0

                    for i in range(4,10):
                        try:
                            if seasonal_weather_dict_v[eomonth(key.year, i)] < av_seasonal_weather_dict_v[i]:
                                
                                if i in range(7,10):
                                    a = 0.5
                                else:
                                    a = 1
                                
                                strike_v = strike_v + 1
                        
                        except Exception:
                            None
                            
                    for i in range(5,10):
                        try:
                            if seasonal_weather_dict_p[eomonth(key.year, i)] > 1.5 * av_seasonal_weather_dict_p[i]:
                                strike_p = strike_p + 1                       
                        except Exception:
                            None
        
                    s_values_test.append(strike_v + strike_p)
                    r_values_test.append(rating)
                    d_values_test.append(key.year)             
                        
                    
            j_dict_train = {}
            for i in range(0, len(n_values_train)-1):
                j_dict_train[n_values_train[i]] = [x_values_train[i], y_values_train[i]]

            j_dict_test = {}
            for i in range(0, len(n_values_test)-1):
                j_dict_test[n_values_test[i]] = [x_values_test[i], y_values_test[i]]

            s_dict_train = {}
            for i in range(0, len(d_values_train)-1):
                s_dict_train[d_values_train[i]] = [s_values_train[i], r_values_train[i]]

            s_dict_test = {}
            for i in range(0, len(d_values_test)-1):
                s_dict_test[d_values_test[i]] = [s_values_test[i], r_values_test[i]]
            
            
            train_dict = {}
            for key in j_dict_train.keys():
                if key in s_dict_train.keys():
                    new_list = j_dict_train[key][0]
                    strike = s_dict_train[key][0]
                    new_list.append(int(strike))
                    rating = j_dict_train[key][1]
                    train_dict[key] = [new_list, rating]

            test_dict = {}
            for key in j_dict_test.keys():
                if key in s_dict_test.keys():
                    new_list = j_dict_test[key][0]
                    strike = s_dict_test[key][0]
                    new_list.append(int(strike))
                    rating = j_dict_test[key][1]
                    test_dict[key] = [new_list, rating]            
            
            x_values_train, y_values_train, n_values_train = [], [], []
            x_values_test, y_values_test, n_values_test = [], [], []
            
            
            
            for key in train_dict.keys():
                x_values_train.append(train_dict[key][0])
                y_values_train.append(train_dict[key][1])
                n_values_train.append(key)
    
            for key in test_dict.keys():
                x_values_test.append(test_dict[key][0])
                y_values_test.append(test_dict[key][1])
                n_values_test.append(key)
            
            
            X_values_train = np.array(x_values_train)
            X_values_test = np.array(x_values_test)
            X_values_all = np.array(x_values_train + x_values_test)
            y_values_all = y_values_train + y_values_test
            n_values_all = n_values_train + n_values_test
            

            
            #Create linear regression object
            regr = linear_model.LinearRegression()
            
            #Train the model using the training sets
            regr.fit(X_values_train, y_values_train)
            
            #Make predictions using the testing set
            y_values_pred = regr.predict(X_values_test)
            y_values_pred_all = regr.predict(X_values_all)

            
            #The coefficients
            print('Coefficients: \n', regr.coef_)
            #The mean squared error
            print("Mean squared error: %.2f"
                  % mean_squared_error(y_values_test, y_values_pred))
            #Explained variance score: 1 is perfect prediction
            print('R2 score: %.2f' % r2_score(y_values_test, y_values_pred))
            
            x = y_values_pred_all
            y = y_values_all
            z = np.polyfit(x, y, 1)
            z_formatted = np.ndarray.tolist(z)
            p = np.poly1d(z)
            xp = np.linspace(min(y_values_pred_all), max(y_values_pred_all), 100) 
            
            #calculate correlation coefficient
            correl_y = p(x)
            R = np.corrcoef(y_values_all, y_values_pred_all)
            cor = R.item(1) #R is a 2x2 matrix so take the correct entry
            print("\nCorrelation coefficient: " + str('%0.2f' % cor))
                       
            print("\nSuggested polynomial a*x + b has [a, b]: "
                  + str('%0.2f' % z_formatted[0]) +", "
                  + str('%0.2f' % z_formatted[1]))                  #+ str('%0.2f' % z_formatted[3]))
    
                        
            #Size the output
            fig = plt.figure(dpi=128, figsize=(10,6))
            
            #Chart gridlines
            plt.grid(None, 'major', 'both')
            
            #Axis tick formats
            for tick in plt.gca().get_xticklabels():
                tick.set_fontname("Calibri")
                tick.set_fontsize(12)
                tick.set_rotation('vertical')
            for tick in plt.gca().get_yticklabels():
                tick.set_fontname("Calibri")
                tick.set_fontsize(12)
            
            #Axis labels and formats
            
            # axis 1
            color = 'tab:blue'
            plt.xlabel("Rating Estimate (weather fundamentals)", fontsize =12)
            #plt.xticks(np.arange(x_values[11], x_values[0], 2))
            plt.ylabel("Rating", color='black', fontsize =12)
            plt.scatter(y_values_pred_all, y_values_all, color=color)
            plt.plot(xp, p(xp), color = 'red')
            plt.tick_params(axis='y', labelcolor=color)
            
            for i, txt in enumerate(n_values_all):
                plt.annotate(txt, (y_values_pred_all[i], y_values_all[i]))
            
                       
            #remove borders
            plt.gca().spines['top'].set_visible(False)
            
            #Chart title
            plt.title(str(self.address)+ " Rating vs Estimate", fontsize = 14)
            
            #Show chart
            plt.show()
            



        proceed_with_method()


    def top_vintage_multi_regression(self):
        """analysis of vintage rule strikes vs price"""
        def proceed_with_method():

          
            weather_dict_p_raw = Chateau(self.address).weather_dict('p')
            weather_dict_v_raw = Chateau(self.address).weather_dict('v')

           
            weather_dict_p = dict_unpacker(weather_dict_p_raw)
            weather_dict_v = dict_unpacker(weather_dict_v_raw)
            
            rating_dict_raw = Chateau_rating(self.address).get_rating_data()
            rating_dict = dict_unpacker(rating_dict_raw)
            
            seasonal_weather_dict_p = seasonal_weather_dict(weather_dict_p)
            seasonal_weather_dict_v = seasonal_weather_dict(weather_dict_v)

           
            av_seasonal_weather_dict_p = average_seasonal_weather_dict(weather_dict_p)
            av_seasonal_weather_dict_v = average_seasonal_weather_dict(weather_dict_v)
 
            
            x_values_train, y_values_train, n_values_train = [], [], []
            x_values_test, y_values_test, n_values_test = [], [], []
            
            s_values_train, r_values_train, d_values_train = [], [], []
            s_values_test, r_values_test, d_values_test = [], [], []
            
            def func_p(x):
                func_list =[]
                for i in range(0,10):
                    
                    if i in [12]: #[2, 7, 9]
                        if i ==2:
                            f = 0.02 *x*x + -0.47 * x + 99.08
                        if i ==7:
                            f = -1.17*x*x + 2.69*x + 96.88
                        if i ==9:
                            f = -0.28*x*x + 0.46*x +98.08
                    
                    else:
                        f = 0
                    
                    func_list.append(f)
                
                return func_list
            
            def func_v(x):
                func_list =[]
                for i in range(0,10):
                    
                    if i in [4,5]: #[3,4,5,6,8]

                        if i ==3:
                            f = -1.17*x*x + 27.42*x + -38.69
                        if i ==4:
                            f = -0.29*x*x + 8.03*x + 42.72
                        if i ==5:
                            f = -0.24*x*x + 8.05*x +31.77                     
                        if i ==6:
                            f = -0.21*x*x + 8.90*x +3.81                 
                        if i ==8:
                            f = -0.22*x*x + 9.64*x -7.21
                    else:
                        f = 0
                    
                    func_list.append(f)
                
                return func_list
            
            
            for key, rating in rating_dict.items():
                if key > datetime(1970,12,31) and key < datetime(2000,12,31) and int(key.year) > 1970 and rating > 96:
                    x_list = []
                    for i in range(2,10):
                        try:
                            av_v = seasonal_weather_dict_v[eomonth(key.year, i)]
                            av_p = seasonal_weather_dict_p[eomonth(key.year, i)]
                            
                            v_adj = func_v(av_v)
                            p_adj = func_p(av_p)
                            
                            v_used = v_adj[i]
                            p_used = p_adj[i]
                            
                            if v_used != 0:
                                x_list.append(v_used)
                            if p_used !=0:
                                x_list.append(p_used)
                        
                        except Exception:
                            None
                            
                    if x_list != []:
                        x_values_train.append(x_list)
                        y_values_train.append(rating)
                        n_values_train.append(key.year) 
                
                if key >= datetime(2000,12,31) and int(key.year) > 1970  and rating > 96:
                    x_list = []
                    for i in range(2,10):
                        try:
                            av_v = seasonal_weather_dict_v[eomonth(key.year, i)]
                            av_p = seasonal_weather_dict_p[eomonth(key.year, i)]
                            
                            v_adj = func_v(av_v)
                            p_adj = func_p(av_p)
                            
                            v_used = v_adj[i]
                            p_used = p_adj[i]
                            
                            if v_used != 0:
                                x_list.append(v_used)
                            if p_used !=0:
                                x_list.append(p_used)
                        
                        except Exception:
                            None
                    
                    if x_list != []:
                        x_values_test.append(x_list)
                        y_values_test.append(rating)
                        n_values_test.append(key.year) 
                        
                        
            X_values_train = np.array(x_values_train)
            X_values_test = np.array(x_values_test)
            X_values_all = np.array(x_values_train + x_values_test)
            y_values_all = y_values_train + y_values_test
            n_values_all = n_values_train + n_values_test
            

            
            #Create linear regression object
            regr = linear_model.LinearRegression()
            
            #Train the model using the training sets
            regr.fit(X_values_train, y_values_train)
            
            #Make predictions using the testing set
            y_values_pred = regr.predict(X_values_test)
            y_values_pred_all = regr.predict(X_values_all)

            
            #The coefficients
            print('Coefficients: \n', regr.coef_)
            #The mean squared error
            print("Mean squared error: %.2f"
                  % mean_squared_error(y_values_test, y_values_pred))
            #Explained variance score: 1 is perfect prediction
            print('R2 score: %.2f' % r2_score(y_values_test, y_values_pred))
            
            x = y_values_pred_all
            y = y_values_all
            z = np.polyfit(x, y, 1)
            z_formatted = np.ndarray.tolist(z)
            p = np.poly1d(z)
            xp = np.linspace(min(y_values_pred_all), max(y_values_pred_all), 100) 
            
            #calculate correlation coefficient
            correl_y = p(x)
            R = np.corrcoef(y_values_all, y_values_pred_all)
            cor = R.item(1) #R is a 2x2 matrix so take the correct entry
            print("\nCorrelation coefficient: " + str('%0.2f' % cor))
                       
            print("\nSuggested polynomial a*x + b has [a, b]: "
                  + str('%0.2f' % z_formatted[0]) +", "
                  + str('%0.2f' % z_formatted[1]))                  #+ str('%0.2f' % z_formatted[3]))
    
                        
            #Size the output
            fig = plt.figure(dpi=128, figsize=(10,6))
            
            #Chart gridlines
            plt.grid(None, 'major', 'both')
            
            #Axis tick formats
            for tick in plt.gca().get_xticklabels():
                tick.set_fontname("Calibri")
                tick.set_fontsize(12)
                tick.set_rotation('vertical')
            for tick in plt.gca().get_yticklabels():
                tick.set_fontname("Calibri")
                tick.set_fontsize(12)
            
            #Axis labels and formats
            
            # axis 1
            color = 'tab:blue'
            plt.xlabel("Rating Estimate (weather fundamentals)", fontsize =12)
            #plt.xticks(np.arange(x_values[11], x_values[0], 2))
            plt.ylabel("Rating", color='black', fontsize =12)
            plt.scatter(y_values_pred_all, y_values_all, color=color)
            plt.plot(xp, p(xp), color = 'red')
            plt.tick_params(axis='y', labelcolor=color)
            
            for i, txt in enumerate(n_values_all):
                plt.annotate(txt, (y_values_pred_all[i], y_values_all[i]))
            
                       
            #remove borders
            plt.gca().spines['top'].set_visible(False)
            
            #Chart title
            plt.title(str(self.address)+ " Rating vs Estimate", fontsize = 14)
            
            #Show chart
            plt.show()
            



        proceed_with_method()

    def top_vintage_multi_regression_applied_all(self):
        """analysis of vintage rule strikes vs price"""
        def proceed_with_method():

          
            weather_dict_p_raw = Chateau(self.address).weather_dict('p')
            weather_dict_v_raw = Chateau(self.address).weather_dict('v')

           
            weather_dict_p = dict_unpacker(weather_dict_p_raw)
            weather_dict_v = dict_unpacker(weather_dict_v_raw)
            
            rating_dict_raw = Chateau_rating(self.address).get_rating_data()
            rating_dict = dict_unpacker(rating_dict_raw)
            
            seasonal_weather_dict_p = seasonal_weather_dict(weather_dict_p)
            seasonal_weather_dict_v = seasonal_weather_dict(weather_dict_v)

           
            av_seasonal_weather_dict_p = average_seasonal_weather_dict(weather_dict_p)
            av_seasonal_weather_dict_v = average_seasonal_weather_dict(weather_dict_v)
 
            
            x_values_train, y_values_train, n_values_train = [], [], []
            x_values_test, y_values_test, n_values_test = [], [], []
            
            s_values_train, r_values_train, d_values_train = [], [], []
            s_values_test, r_values_test, d_values_test = [], [], []
            
            def func_p(x):
                func_list =[]
                for i in range(0,10):
                    
                    if i in [12]: #[2, 7, 9]
                        if i ==2:
                            f = 0.02 *x*x + -0.47 * x + 99.08
                        if i ==7:
                            f = -1.17*x*x + 2.69*x + 96.88
                        if i ==9:
                            f = -0.28*x*x + 0.46*x +98.08
                    
                    else:
                        f = 0
                    
                    func_list.append(f)
                
                return func_list
            
            def func_v(x):
                func_list =[]
                for i in range(0,10):
                    
                    if i in [4,5]: #[3,4,5,6,8]

                        if i ==3:
                            f = -1.17*x*x + 27.42*x + -38.69
                        if i ==4:
                            f = -0.29*x*x + 8.03*x + 42.72
                        if i ==5:
                            f = -0.24*x*x + 8.05*x +31.77                     
                        if i ==6:
                            f = -0.21*x*x + 8.90*x +3.81                 
                        if i ==8:
                            f = -0.22*x*x + 9.64*x -7.21
                    else:
                        f = 0
                    
                    func_list.append(f)
                
                return func_list
            
            def est_function(x_list):
                a = float(x_list[0])
                b = float(x_list[1])
                f = (a * 0.39965315 + b * 0.11562814)*2.67 - 160.99
                return f

            
            for key, rating in rating_dict.items():
                if key > datetime(1970,12,31) and key < datetime(2000,12,31) and int(key.year) > 1970 and rating > 95:
                    x_list = []
                    for i in range(2,10):
                        try:
                            av_v = seasonal_weather_dict_v[eomonth(key.year, i)]
                            av_p = seasonal_weather_dict_p[eomonth(key.year, i)]
                            
                            v_adj = func_v(av_v)
                            p_adj = func_p(av_p)
                            
                            v_used = v_adj[i]
                            p_used = p_adj[i]
                            
                            if v_used != 0:
                                x_list.append(v_used)
                            if p_used !=0:
                                x_list.append(p_used)
                        
                        except Exception:
                            None
                            
                    if x_list != []:
                        x_values_train.append(est_function(x_list))
                        y_values_train.append(rating)
                        n_values_train.append(key.year) 
                
                if key >= datetime(2000,12,31) and int(key.year) > 1970  and rating > 95:
                    x_list = []
                    for i in range(2,10):
                        try:
                            av_v = seasonal_weather_dict_v[eomonth(key.year, i)]
                            av_p = seasonal_weather_dict_p[eomonth(key.year, i)]
                            
                            v_adj = func_v(av_v)
                            p_adj = func_p(av_p)
                            
                            v_used = v_adj[i]
                            p_used = p_adj[i]
                            
                            if v_used != 0:
                                x_list.append(v_used)
                            if p_used !=0:
                                x_list.append(p_used)
                        
                        except Exception:
                            None
                    
                    if x_list != []:
                        x_values_test.append(est_function(x_list))
                        y_values_test.append(rating)
                        n_values_test.append(key.year) 
            


            
            #X_values_train = np.array(x_values_train)
            #X_values_test = np.array(x_values_test)
            x_values_all = x_values_train + x_values_test
            y_values_all = y_values_train + y_values_test
            n_values_all = n_values_train + n_values_test
            

            
            #Create linear regression object
            #regr = linear_model.LinearRegression()
            
            #Train the model using the training sets
            #regr.fit(X_values_train, y_values_train)
            
            #Make predictions using the testing set
            #y_values_pred = regr.predict(X_values_test)
            #y_values_pred_all = regr.predict(X_values_all)

            
            #The coefficients
            #print('Coefficients: \n', regr.coef_)
            #The mean squared error
            #print("Mean squared error: %.2f"
                  #% mean_squared_error(y_values_test, y_values_pred))
            #Explained variance score: 1 is perfect prediction
            #print('R2 score: %.2f' % r2_score(y_values_test, y_values_pred))
            
            x = x_values_all
            y = y_values_all
            z = np.polyfit(x, y, 1)
            z_formatted = np.ndarray.tolist(z)
            p = np.poly1d(z)
            xp = np.linspace(min(x_values_all), max(x_values_all), 100) 
            
            #calculate correlation coefficient
            correl_y = p(x)
            R = np.corrcoef(y_values_all, correl_y)
            cor = R.item(1) #R is a 2x2 matrix so take the correct entry
            print("\nCorrelation coefficient: " + str('%0.2f' % cor))
                       
            print("\nSuggested polynomial a*x + b has [a, b]: "
                  + str('%0.2f' % z_formatted[0]) +", "
                  + str('%0.2f' % z_formatted[1]))                  #+ str('%0.2f' % z_formatted[3]))
    
                        
            #Size the output
            fig = plt.figure(dpi=128, figsize=(10,6))
            
            #Chart gridlines
            plt.grid(None, 'major', 'both')
            
            #Axis tick formats
            for tick in plt.gca().get_xticklabels():
                tick.set_fontname("Calibri")
                tick.set_fontsize(12)
                tick.set_rotation('vertical')
            for tick in plt.gca().get_yticklabels():
                tick.set_fontname("Calibri")
                tick.set_fontsize(12)
            
            #Axis labels and formats
            
            # axis 1
            color = 'tab:blue'
            plt.xlabel("Rating Estimate (weather fundamentals)", fontsize =12)
            #plt.xticks(np.arange(x_values[11], x_values[0], 2))
            plt.ylabel("Rating", color='black', fontsize =12)
            plt.scatter(x_values_all, y_values_all, color=color)
            plt.plot(xp, p(xp), color = 'red')
            plt.tick_params(axis='y', labelcolor=color)
            
            for i, txt in enumerate(n_values_all):
                plt.annotate(txt, (x_values_all[i], y_values_all[i]))
            
                       
            #remove borders
            plt.gca().spines['top'].set_visible(False)
            
            #Chart title
            plt.title(str(self.address)+ " Rating vs Estimate", fontsize = 14)
            
            #Show chart
            plt.show()
            



        proceed_with_method()

#Chateau_results("Chateau Cheval Blanc").price_vs_rating_cubic()
#Chateau_results("Chateau Margaux").rainfall_correlation(3, 9)
#Chateau_results("Chateau Margaux").temp_correlation(3, 9)
#for i in range(1,12):
    #Chateau_results("Chateau Margaux").rainfall_correlation(i, i+1)
    #Chateau_results("Chateau Margaux").temp_correlation(i, i+1)
#Chateau_results("Chateau Margaux").rainfall_correlation(6, 7)
#Chateau_results("Chateau Margaux").temp_correlation(6, 7)    
#Chateau_results("Chateau Margaux").temp_times_rainfall_correlation()
#Chateau_results("Chateau Margaux").ranking_correlation()
#Chateau_results("Chateau Margaux").pricing_forecast()
Chateau_results("Chateau Margaux").multi_regression()
Chateau_results("Chateau Margaux").price_vs_rating_cubic()
#Chateau_results("Chateau Margaux").top_vintage_multi_regression()
Chateau_results("Chateau Margaux").top_vintage_multi_regression_applied_all()
