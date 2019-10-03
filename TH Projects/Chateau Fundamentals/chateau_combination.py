# -*- coding: utf-8 -*-
"""
Created on Sat May 18 10:01:49 2019

@author: thoma
"""

from chateau_weather import Chateau
from chateau_data import Chateau_data
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib.lines as mlines
from datetime import datetime, date, timedelta
import json
import statistics
import math

class Chateau_comb():
    
    def __init__(self, address):
        """initialize attributes to define a stock"""
        self.address = address
    
    def chateau_profile(self, name, data=''):
        """Store a profile in the file so we do not repeat every action"""
        filename = (str(self.address) + "_px_weather_profile.txt")
        #open as write - this takes care of the initial instance of the file
        # if we can read the profile read it, otherwise create an empty dict

        try:
            with open(filename) as f:
                contents = json.load(f)
            chateau_profile_dict = contents

        except FileNotFoundError:
            chateau_profile_dict = {}

        except ValueError:
            print("dictionary has a value error")
            chateau_profile_dict = {}
                 
        # if there is an existing entry:     
        if name in chateau_profile_dict.keys():
            if data:
                del chateau_profile_dict[name]
                chateau_profile_dict[name] = data
                # store the amended profile          
                with open(filename, 'w') as f:
                    json.dump(chateau_profile_dict,f)
                return chateau_profile_dict[name]
            else:
                return chateau_profile_dict[name]
        
        # if there isn't an existing entry
        else:
            if data:
                # create a new one if there is data
                chateau_profile_dict[name] = data
                # store the amended profile          
                with open(filename, 'w') as f:
                    json.dump(chateau_profile_dict,f)
                return chateau_profile_dict[name]

            else:
                # return nothing if there isn't
                return None
    
    def annual_price_weather_chart(self, category, given_month, update=''):
        """returns wine price/date data of the given month"""
       
        def proceed_with_method():
           
            price_dict = Chateau_data(self.address).get_price_data()
            weather_dict = Chateau(self.address).weather_dict(category)
            
            #turn weather_dict into annual rainfall
            monthly_weather_dict = {}
            
            def eomonth(y, m):
                year = y
                if m == 12:
                    month = 1
                else:
                    month = int(m)+1
                given_day = datetime(year, month, 1)
                required_day = given_day - timedelta(days=1)
                return required_day
                        
            for p_date, precip in weather_dict.items():
                formattedas_date = datetime.strptime(p_date, "%Y-%m-%d")
                y = formattedas_date.year
                m = formattedas_date.month
                needed_day = eomonth(y, m)
                if needed_day in monthly_weather_dict.keys():
                    monthly_weather_dict[needed_day] = monthly_weather_dict[needed_day] + float(precip)
                else:
                    monthly_weather_dict[needed_day] = float(precip)
            
            monthly_weather_dict_final = {}
            for p_date, precip in monthly_weather_dict.items():
                da = p_date
                if da.month == given_month:
                    monthly_weather_dict_final[da] = precip
            
            # start chart
            x_values, y_values, z_values = [], [], []
        
            for key in price_dict.keys():
                x_date = datetime.strptime(key, '%Y-%m-%d')
                if x_date > datetime(1980, 12, 31):
                    x_values.append(key)
                    y_values.append(float(str(price_dict[key])))
                    z_date = eomonth(x_date.year, given_month)
                    z_values.append(annual_weather_dict_final[z_date])
            
                        
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
            color = 'tab:red'
            plt.xlabel("Date", fontsize =12)
            plt.ylabel("Price", color='black', fontsize =12)
            plt.bar(x_values, y_values, color=color)
            plt.tick_params(axis='y', labelcolor=color)
            
            ax2 = plt.twinx()  # instantiate a second axes that shares the same x-axis
            
            #axis 2
            color = 'tab:blue'
            ax2.set_ylabel("Precip", color='black', fontsize=12)  # we already handled the x-label with ax1
            ax2.plot(x_values, z_values, color=color)
            ax2.tick_params(axis='y', labelcolor=color)
            
            #remove borders
            plt.gca().spines['top'].set_visible(False)
            
            #Chart title
            plt.title("Weather/Price correlation "+str(given_month), fontsize = 14)
            
            #Show chart
            plt.show()

        proceed_with_method()    

    def vintage_patterns(self, vintage, update=''):
        """returns the weather profile of the vintage"""
       
        def proceed_with_method():
           
            weather_dict_p = Chateau(self.address).weather_dict('p')
            weather_dict_v = Chateau(self.address).weather_dict('v')
            
            #turn weather_dict into annual rainfall
            
            def eomonth(y, m):
                year = y
                if m == 12:
                    month = 1
                else:
                    month = int(m)+1
                given_day = datetime(year, month, 1)
                required_day = given_day - timedelta(days=1)
                return required_day
                        
            def seasonal_weather_dict(dict_sample):
                """returns dict of average daily weather data aggregated by month"""
                monthly_weather_dict = {}
                for p_date, precip in dict_sample.items():
                    formattedas_date = datetime.strptime(p_date, "%Y-%m-%d")
                    y = formattedas_date.year
                    m = formattedas_date.month
                    needed_day = eomonth(y, m)
                    if needed_day in monthly_weather_dict.keys():
                        x = monthly_weather_dict[needed_day][0] + float(precip)
                        y = monthly_weather_dict[needed_day][1] + 1
                        monthly_weather_dict[needed_day]  = [x, y]
                    else:
                        monthly_weather_dict[needed_day] = [float(precip), 1]
                
                monthly_weather_dict_av = {}
                for needed_day in monthly_weather_dict.keys():
                    d = monthly_weather_dict[needed_day][0] / monthly_weather_dict[needed_day][1]
                    monthly_weather_dict_av[needed_day] = d
                return monthly_weather_dict_av
                
            
            def average_seasonal_weather_dict(dict_sample):
                """returns average seasonal weather dictionary"""
                monthly_weather_dict = seasonal_weather_dict(dict_sample)
                average_seasonal_weather_dict = {}
                for p_date, precip in monthly_weather_dict.items():
                    if p_date.month in average_seasonal_weather_dict.keys():
                        x = average_seasonal_weather_dict[p_date.month][0] + float(precip)
                        y = average_seasonal_weather_dict[p_date.month][1] + 1
                        average_seasonal_weather_dict[p_date.month] = [x, y]
                    else:
                        average_seasonal_weather_dict[p_date.month] = [float(precip), 1]
                
                average_seasonal_weather_dict_final = {}
                for month, list_element in average_seasonal_weather_dict.items():
                    d = (list_element[0] / list_element[1])
                    average_seasonal_weather_dict_final[month] = d

                return average_seasonal_weather_dict_final
            
          
            def vintage_monthly_weather_dict(dict_sample, vintage):
                """returns dict of weather data aggregated by month for vintage year"""
                monthly_weather_dict = seasonal_weather_dict(dict_sample)    
                vintage_monthly_weather_dict_final = {}
                for p_date, precip in monthly_weather_dict.items():
                    if p_date.year == vintage:
                        vintage_monthly_weather_dict_final[p_date] = precip
                return vintage_monthly_weather_dict_final
            
            monthly_weather_dict_p = vintage_monthly_weather_dict(weather_dict_p, vintage)
            monthly_weather_dict_v = vintage_monthly_weather_dict(weather_dict_v, vintage)
            seasonal_weather_dict_p = average_seasonal_weather_dict(weather_dict_p)
            seasonal_weather_dict_v = average_seasonal_weather_dict(weather_dict_v)
            
            # start chart
            x_values, y_values, z_values, sy_values, sz_values = [], [], [], [], []
        
            for key in monthly_weather_dict_p.keys():
                x_date = key
                #datetime.strptime(key, '%Y-%m-%d')
                if x_date > datetime(1980, 12, 31):
                    x_values.append(key)
                    y_values.append(float(str(monthly_weather_dict_p[key])))
                    z_values.append(monthly_weather_dict_v[x_date])
                    #y_values.append(float(str(monthly_weather_dict_p[key]))-float(str(seasonal_weather_dict_p[key.month])))
                    #z_values.append(monthly_weather_dict_v[x_date]-seasonal_weather_dict_v[x_date.month])
                    sy_values.append(float(str(seasonal_weather_dict_p[key.month])))
                    sz_values.append(seasonal_weather_dict_v[x_date.month])
            
                        
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
            plt.xlabel("Date", fontsize =12)
            #plt.xticks(np.arange(x_values[11], x_values[0], 2))
            plt.ylabel("Precip", color='black', fontsize =12)
            plt.plot(x_values, y_values, color=color)
            plt.plot(x_values, sy_values, color=color, linestyle ='dashed')
            plt.tick_params(axis='y', labelcolor=color)
            
            ax2 = plt.twinx()  # instantiate a second axes that shares the same x-axis
            
            #axis 2
            color = 'tab:red'
            ax2.set_ylabel("Temp", color='black', fontsize=12)  # we already handled the x-label with ax1
            ax2.plot(x_values, z_values, color=color)
            ax2.plot(x_values, sz_values, color=color, linestyle='dashed')
            ax2.tick_params(axis='y', labelcolor=color)
            
            #remove borders
            plt.gca().spines['top'].set_visible(False)
            
            #Chart title
            plt.title(str(self.address)+ " Weather Pattern for Vintage:  "+str(vintage), fontsize = 14)
            
            #Show chart
            plt.show()

        proceed_with_method()  

    def scatter_analysis(self, category, chosen_month):
        """return the scatter plot across years of the month"""
       
        def proceed_with_method():
           
            weather_dict = Chateau(self.address).weather_dict(category)
            
           
            def eomonth(y, m):
                year = y
                if m == 12:
                    month = 1
                else:
                    month = int(m)+1
                given_day = datetime(year, month, 1)
                required_day = given_day - timedelta(days=1)
                return required_day
                        
            def seasonal_weather_dict(dict_sample):
                """returns dict of average daily weather data aggregated by month"""
                monthly_weather_dict = {}
                for p_date, precip in dict_sample.items():
                    formattedas_date = datetime.strptime(p_date, "%Y-%m-%d")
                    y = formattedas_date.year
                    m = formattedas_date.month
                    needed_day = eomonth(y, m)
                    if needed_day in monthly_weather_dict.keys():
                        x = monthly_weather_dict[needed_day][0] + float(precip)
                        y = monthly_weather_dict[needed_day][1] + 1
                        monthly_weather_dict[needed_day]  = [x, y]
                    else:
                        monthly_weather_dict[needed_day] = [float(precip), 1]
                
                monthly_weather_dict_av = {}
                for needed_day in monthly_weather_dict.keys():
                    d = monthly_weather_dict[needed_day][0] / monthly_weather_dict[needed_day][1]
                    monthly_weather_dict_av[needed_day] = d
                return monthly_weather_dict_av
     
            def all_monthly_weather_dict(dict_sample, chosen_month):
                """returns dict of weather data aggregated by month for vintage year"""
                monthly_weather_dict = seasonal_weather_dict(dict_sample)    
                all_monthly_weather_dict_final = {}
                for p_date, precip in monthly_weather_dict.items():
                    if p_date.month == int(chosen_month):
                        all_monthly_weather_dict_final[p_date] = precip
                return all_monthly_weather_dict_final
            
            monthly_weather_dict = all_monthly_weather_dict(weather_dict, chosen_month)
            price_dict = Chateau_data(self.address).get_price_data()

            
            # start chart
            x_values, y_values = [], []
        
            for key in monthly_weather_dict.keys():
                x_date = key
                #datetime.strptime(key, '%Y-%m-%d')
                if x_date > datetime(1970, 12, 31):
                    try:
                        y = int(x_date.year)
                        x_date_eoy = date(y, 12, 31)
                        y_values.append(price_dict[str(x_date_eoy)])
                        x_values.append(float(str(monthly_weather_dict[key])))
                    except KeyError:
                        None
                    else:
                        None
                   
                        
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
            plt.xlabel(str(category) + " avg daily", fontsize =12)
            #plt.xticks(np.arange(x_values[11], x_values[0], 2))
            plt.ylabel("Price", color='black', fontsize =12)
            plt.scatter(x_values, y_values, color=color)
            plt.tick_params(axis='y', labelcolor=color)
            
                       
            #remove borders
            plt.gca().spines['top'].set_visible(False)
            
            #Chart title
            plt.title(str(self.address)+ " Weather Pattern for Month:  "+str(chosen_month), fontsize = 14)
            
            #Show chart
            plt.show()

        proceed_with_method()  
    

    def correl_analysis(self, category, chosen_month):
        """return the scatter plot across years of the month"""
       
        def proceed_with_method():
           
            weather_dict_raw = Chateau(self.address).weather_dict(category)
            price_dict_raw = Chateau_data(self.address).get_price_data()

            #unpack the dictionaries so the dates have the correct format
            def dict_unpacker(sample_dict):
                dict_unpacked = {}
                for p_date, price in sample_dict.items():
                     formattedas_date = datetime.strptime(p_date, "%Y-%m-%d")
                     dict_unpacked[formattedas_date] = float(price)
                return dict_unpacked
            
            weather_dict = dict_unpacker(weather_dict_raw)
            price_dict = dict_unpacker(price_dict_raw)
                   
           
            def eomonth(y, m):
                """returns eomonth for a year and month"""
                year = y
                if m == 12:
                    month = 1
                else:
                    month = int(m)+1
                given_day = datetime(year, month, 1)
                required_day = given_day - timedelta(days=1)
                return required_day
                        
            def seasonal_weather_dict(dict_sample):
                """returns dict of average daily weather data aggregated by month"""
                monthly_weather_dict = {}
                for p_date, precip in dict_sample.items():
                    formattedas_date = p_date
                    y = formattedas_date.year
                    m = formattedas_date.month
                    needed_day = eomonth(y, m)
                    if needed_day in monthly_weather_dict.keys():
                        x = monthly_weather_dict[needed_day][0] + float(precip)
                        y = monthly_weather_dict[needed_day][1] + 1
                        monthly_weather_dict[needed_day]  = [x, y]
                    else:
                        monthly_weather_dict[needed_day] = [float(precip), 1]
                
                monthly_weather_dict_av = {}
                for needed_day in monthly_weather_dict.keys():
                    d = monthly_weather_dict[needed_day][0] / monthly_weather_dict[needed_day][1]
                    monthly_weather_dict_av[needed_day] = d
                return monthly_weather_dict_av
     
            def all_monthly_weather_dict(dict_sample, chosen_month):
                """returns dict of weather data aggregated by month for all years"""
                monthly_weather_dict = seasonal_weather_dict(dict_sample)    
                all_monthly_weather_dict_final = {}
                for p_date, precip in monthly_weather_dict.items():
                    if p_date.month == int(chosen_month):
                        all_monthly_weather_dict_final[p_date] = precip
                return all_monthly_weather_dict_final
            
            monthly_weather_dict = all_monthly_weather_dict(weather_dict, chosen_month)
            
            #find the average price
            px_list = []
            for px_date, price in price_dict.items():
                if px_date > datetime(1960, 12, 31):
                    px_list.append(price)
            
            av = statistics.mean(px_list)
            sd = statistics.stdev(px_list)
                                          
            print(str(av) + " is the average price for " + str(self.address))
            
            #add prices above average to the selected list
            selected_price_dict = {}
            y_values = []
            for px_date, price in price_dict.items():
                if price > av + 0.5*sd and px_date > datetime(1960, 12, 31):
                    selected_price_dict[px_date] = price
                    y_values.append(price)

            #find weather data for price year
            x_values = []
            for px_date, price in selected_price_dict.items():
                y = px_date.year
                m = chosen_month
                relevant_date = eomonth(y, m)
                addition = monthly_weather_dict[relevant_date]
                x_values.append(addition)
      
            #calculate best fit line
            x = x_values
            y = y_values
            z = np.polyfit(x, y, 2)
            p = np.poly1d(z)
            xp = np.linspace(min(x_values), max(x_values), 100) 
            
            #calculate correlation coefficient
            correl_y = p(x)
            #A = np.vstack([x, np.ones(len(x))]).T
            #m, c = np.linalg.lstsq(A, correl_y, rcond=None)[0]
            #print(m, c)
            R = np.corrcoef(y, correl_y)
            cor = R.item(1) #R is a 2x2 matrix so take the correct entry
            print("\nCorrelation coefficient: " + str(cor))
                       
            print("\nSuggested polynomial a*x^2 + bx + c has [a, b, c]: " + str(z))
              
    
                        
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
            plt.xlabel(str(category) + " avg daily", fontsize =12)
            #plt.xticks(np.arange(x_values[11], x_values[0], 2))
            plt.ylabel("Price", color='black', fontsize =12)
            plt.scatter(x_values, y_values, color=color)
            plt.plot(xp, p(xp), color = 'red')
            plt.tick_params(axis='y', labelcolor=color)
            
                       
            #remove borders
            plt.gca().spines['top'].set_visible(False)
            
            #Chart title
            plt.title(str(self.address)+ " Weather Pattern for Month:  "+str(chosen_month), fontsize = 14)
            
            #Show chart
            plt.show()

        proceed_with_method()  

    def vintage_rule_finder(self, category):
        """Take the standard vintages and record anomalies. 
        Then take the great ones and exclude anomalies occurring in the standard set.
        Now we have list of anomalies that ruin a great vintage.
        
        Take the great vintages and record anomalies.
        Take the standard ones and exclude them from the great set.
        Now have a list of anomalies that make a great vintage.
        
        This won't work if the great vintages are great because they are standard 
        i.e. no anomalies
        """
       
        def proceed_with_method():
           
            weather_dict_raw = Chateau(self.address).weather_dict(category)
            price_dict_raw = Chateau_data(self.address).get_price_data()

            #unpack the dictionaries so the dates have the correct format
            def dict_unpacker(sample_dict):
                dict_unpacked = {}
                for p_date, price in sample_dict.items():
                     formattedas_date = datetime.strptime(p_date, "%Y-%m-%d")
                     dict_unpacked[formattedas_date] = float(price)
                return dict_unpacked
            
            weather_dict = dict_unpacker(weather_dict_raw)
            price_dict = dict_unpacker(price_dict_raw)
                   
           
            def eomonth(y, m):
                """returns eomonth for a year and month"""
                year = y
                if m == 12:
                    month = 1
                else:
                    month = int(m)+1
                given_day = datetime(year, month, 1)
                required_day = given_day - timedelta(days=1)
                return required_day
                        
            def seasonal_weather_dict(dict_sample):
                """returns dict of average daily weather data aggregated by month"""
                monthly_weather_dict = {}
                for p_date, precip in dict_sample.items():
                    formattedas_date = p_date
                    y = formattedas_date.year
                    m = formattedas_date.month
                    needed_day = eomonth(y, m)
                    if needed_day in monthly_weather_dict.keys():
                        x = monthly_weather_dict[needed_day][0] + float(precip)
                        y = monthly_weather_dict[needed_day][1] + 1
                        monthly_weather_dict[needed_day]  = [x, y]
                    else:
                        monthly_weather_dict[needed_day] = [float(precip), 1]
                
                monthly_weather_dict_av = {}
                for needed_day in monthly_weather_dict.keys():
                    d = monthly_weather_dict[needed_day][0] / monthly_weather_dict[needed_day][1]
                    monthly_weather_dict_av[needed_day] = d
                return monthly_weather_dict_av
            
            
            def all_monthly_weather_dict(dict_sample):
                """returns dict of mean, stdev for every month"""
                monthly_weather_dict = seasonal_weather_dict(dict_sample)    
                all_monthly_weather_dict = {}
                for chosen_month in range(1,13):
                    new_list = []
                    for p_date, precip in monthly_weather_dict.items():
                        if p_date.month == int(chosen_month) and p_date > datetime(1970, 12, 31):
                            new_list.append(precip)
                    av = statistics.mean(new_list)
                    sd = statistics.stdev(new_list)
                    all_monthly_weather_dict[chosen_month] = [av, sd]
                return all_monthly_weather_dict
            
           # monthly_weather_dict = all_monthly_weather_dict(weather_dict, chosen_month)
            
            #find the list of top prices
            prices, prices_dates, top_prices, lower_prices, top_prices_dates, lower_prices_dates = [], [], [], [], [], []
            for px_date, price in price_dict.items():
                if px_date > datetime(1980, 12, 31):
                   prices.append(price)
                   prices_dates.append(px_date)

            av = statistics.mean(prices)
            sd = statistics.stdev(prices)
        
            print("\nAverage/Stdev price is: " + str(av) + "/ " + str(sd) + "\n")

            for i in range(0, len(prices)-1):
                if prices[i] > av + 0.5 * sd:
                    top_prices.append(prices[i])
                    top_prices_dates.append(prices_dates[i])
                elif prices[i] < av - 0.5 * sd:
                    lower_prices.append(prices[i])
                    lower_prices_dates.append(prices_dates[i])
            
            poor_criteria_dict = {}
            
            for i in range(1,13):
                poor_criteria_dict[i] = []
                
           
            weather_stats = all_monthly_weather_dict(weather_dict)
            print(weather_stats)
            specific_weather_dict = seasonal_weather_dict(weather_dict)
            #find poor price criteria
            for lower_price_date in lower_prices_dates:
                y = lower_price_date.year
                for i in range(1,13):
                    m = i
                    weather_date = eomonth(y, m)
                    weather_stat = specific_weather_dict[weather_date]
                    av = weather_stats[i][0]
                    sd = weather_stats[i][1]
                    
                    if weather_stat > av + 1*sd:
                        title = "sig over av"
                        if title not in poor_criteria_dict[i]:
                            poor_criteria_dict[i].append(title)
                    
                    elif weather_stat > av + 0.5*sd:
                        title = "slight over av"
                        if title not in poor_criteria_dict[i]:
                            poor_criteria_dict[i].append(title)
                    
                    elif weather_stat < av - 1*sd:
                        title = "slight under av"
                        if title not in poor_criteria_dict[i]:
                            poor_criteria_dict[i].append(title)
                    
                    elif weather_stat < av - 0.5*sd:
                        title = "sig under av"
                        if title not in poor_criteria_dict[i]:
                            poor_criteria_dict[i].append(title)
            
            #find top price criteria
          
            top_criteria_dict = {}
            
            for i in range(1,13):
                top_criteria_dict[i] = []
                
            for top_price_date in top_prices_dates:
                y = top_price_date.year
                for i in range(1,13):
                    m = i
                    weather_date = eomonth(y, m)
                    weather_stat = specific_weather_dict[weather_date]
                    av = weather_stats[i][0]
                    sd = weather_stats[i][1]
                    
                    if weather_stat > av + 1*sd:
                        title = "sig over av"
                        if title not in top_criteria_dict[i]:
                            top_criteria_dict[i].append(title)
                    
                    elif weather_stat > av + 0.5*sd:
                        title = "slight over av"
                        if title not in top_criteria_dict[i]:
                            top_criteria_dict[i].append(title)
                    
                    elif weather_stat < av - 1*sd:
                        title = "sig under av"
                        if title not in top_criteria_dict[i]:
                            top_criteria_dict[i].append(title)
                    
                    elif weather_stat < av - 0.5*sd:
                        title = "slight under av"
                        if title not in top_criteria_dict[i]:
                            top_criteria_dict[i].append(title)
            
            bad_criteria_dict = {}
            
            for i in range(1,13):
                bad_criteria_dict[i] = []
                
            for i in range(1, 13):
                y = [x for x in poor_criteria_dict[i] if x not in top_criteria_dict[i]]
                bad_criteria_dict[i] = y
            
            good_criteria_dict = {}
            
            for i in range(1,13):
                good_criteria_dict[i] = []
                
            for i in range(1, 13):
                y = [x for x in top_criteria_dict[i] if x not in poor_criteria_dict[i]]
                good_criteria_dict[i] = y
            
            print("\n" + str(self.address) + " great vintages have had these seasonal weather anomalies: " + str(top_criteria_dict))
            print("\n" + str(self.address) + " standard vintages have had these seasonal weather anomalies: " + str(poor_criteria_dict))
            print("\n" + str(self.address) + " we will use the following criteria as bad vintage indicators: " + str(bad_criteria_dict))
            print("\n" + str(self.address) + " we will use the following criteria as good vintage indicators: " + str(good_criteria_dict))
            

        proceed_with_method() 

    def vintage_distance(self, vintage, start_month='3', end_month='8'):
        """returns the weather profile of the vintage"""
       
           
        weather_dict_p = Chateau(self.address).weather_dict('p')
        weather_dict_v = Chateau(self.address).weather_dict('v')
        
        #turn weather_dict into annual rainfall
        
        def eomonth(y, m):
            year = y
            if m == 12:
                month = 1
            else:
                month = int(m)+1
            given_day = datetime(year, month, 1)
            required_day = given_day - timedelta(days=1)
            return required_day
                    
        def seasonal_weather_dict(dict_sample):
            """returns dict of average daily weather data aggregated by month"""
            monthly_weather_dict = {}
            for p_date, precip in dict_sample.items():
                formattedas_date = datetime.strptime(p_date, "%Y-%m-%d")
                y = formattedas_date.year
                m = formattedas_date.month
                needed_day = eomonth(y, m)
                if needed_day in monthly_weather_dict.keys():
                    x = monthly_weather_dict[needed_day][0] + float(precip)
                    y = monthly_weather_dict[needed_day][1] + 1
                    monthly_weather_dict[needed_day]  = [x, y]
                else:
                    monthly_weather_dict[needed_day] = [float(precip), 1]
            
            monthly_weather_dict_av = {}
            for needed_day in monthly_weather_dict.keys():
                d = monthly_weather_dict[needed_day][0] / monthly_weather_dict[needed_day][1]
                monthly_weather_dict_av[needed_day] = d
            return monthly_weather_dict_av
            
        
        def average_seasonal_weather_dict(dict_sample):
            """returns average seasonal weather dictionary"""
            monthly_weather_dict = seasonal_weather_dict(dict_sample)
            average_seasonal_weather_dict = {}
            for p_date, precip in monthly_weather_dict.items():
                if p_date.month in average_seasonal_weather_dict.keys():
                    x = average_seasonal_weather_dict[p_date.month][0] + float(precip)
                    y = average_seasonal_weather_dict[p_date.month][1] + 1
                    average_seasonal_weather_dict[p_date.month] = [x, y]
                else:
                    average_seasonal_weather_dict[p_date.month] = [float(precip), 1]
            
            average_seasonal_weather_dict_final = {}
            for month, list_element in average_seasonal_weather_dict.items():
                d = (list_element[0] / list_element[1])
                average_seasonal_weather_dict_final[month] = d

            return average_seasonal_weather_dict_final
        
      
        def vintage_monthly_weather_dict(dict_sample, vintage):
            """returns dict of weather data aggregated by month for vintage year"""
            monthly_weather_dict = seasonal_weather_dict(dict_sample)    
            vintage_monthly_weather_dict_final = {}
            for p_date, precip in monthly_weather_dict.items():
                if p_date.year == vintage:
                    vintage_monthly_weather_dict_final[p_date] = precip
            return vintage_monthly_weather_dict_final
        
        monthly_weather_dict_p = vintage_monthly_weather_dict(weather_dict_p, vintage)
        monthly_weather_dict_v = vintage_monthly_weather_dict(weather_dict_v, vintage)
        seasonal_weather_dict_p = average_seasonal_weather_dict(weather_dict_p)
        seasonal_weather_dict_v = average_seasonal_weather_dict(weather_dict_v)
        
        # start chart
        x_values, y_values, z_values, sy_values, sz_values = [], [], [], [], []
    
        for key in monthly_weather_dict_p.keys():
            x_date = key
            #datetime.strptime(key, '%Y-%m-%d')
            if x_date > datetime(1980, 12, 31):
                x_values.append(key)
                y_values.append(float(str(monthly_weather_dict_p[key])))
                z_values.append(monthly_weather_dict_v[x_date])
                sy_values.append(float(str(seasonal_weather_dict_p[key.month])))
                sz_values.append(seasonal_weather_dict_v[x_date.month])
        
        msq2 = 0
        
        for i in range(int(start_month)-1, int(end_month)-1):
            pd = y_values[i] - sy_values[i]
            vd = z_values[i] - sz_values[i]
            add = pd*pd*0 + vd*vd
            msq2 = msq2 + add
        
        msq = math.sqrt(msq2)
        #print(vintage)
        #print(msq)
        
        return msq

    def price_forecaster(self):
        """returns the weather profile of the vintage"""
        def proceed_with_method():
            
            price_dict_raw = Chateau_data(self.address).get_price_data()
    
            #unpack the dictionaries so the dates have the correct format
            def dict_unpacker(sample_dict):
                dict_unpacked = {}
                for p_date, price in sample_dict.items():
                     formattedas_date = datetime.strptime(p_date, "%Y-%m-%d")
                     dict_unpacked[formattedas_date] = float(price)
                return dict_unpacked
            
            price_dict = dict_unpacker(price_dict_raw)
            
            
            x_values, y_values = [], []
            
            for p_date in price_dict.keys():
                if p_date > datetime(1980, 12, 31):
                    print(p_date.year)
                    y_values.append(price_dict[p_date])
                    d = Chateau_comb(self.address).vintage_distance(p_date.year,'2','8')
                    x_values.append(d)
            
            print(x_values)
            print(y_values)
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
            plt.xlabel("Distance from average seasonality", fontsize =12)
            #plt.xticks(np.arange(x_values[11], x_values[0], 2))
            plt.ylabel("Price", color='black', fontsize =12)
            plt.scatter(x_values, y_values, color=color)
            plt.tick_params(axis='y', labelcolor=color)
            
                       
            #remove borders
            plt.gca().spines['top'].set_visible(False)
            
            #Chart title
            plt.title("Price forecaster", fontsize = 14)
            
            #Show chart
            plt.show()

        proceed_with_method()  

#for i in range(1,13):
    #Chateau_comb("Chateau Margaux").annual_price_weather_chart('p', i)
Chateau_data("Chateau Margaux").print_wine_price(1960)   
#Chateau_comb("Chateau Margaux").vintage_patterns(2015)
#Chateau_comb("Chateau Margaux").vintage_patterns(2010)
#Chateau_comb("Chateau Margaux").vintage_patterns(2009)
#Chateau_comb("Chateau Margaux").vintage_patterns(2005)
#Chateau_comb("Chateau Margaux").vintage_patterns(2000)
#Chateau_comb("Chateau Margaux").vintage_patterns(1996)
#Chateau_comb("Chateau Margaux").vintage_patterns(2006)
#Chateau_comb("Chateau Margaux").vintage_patterns(2007)
#Chateau_comb("Chateau Margaux").correl_analysis('v','7')
Chateau_comb("Chateau Margaux").vintage_rule_finder('v')
#Chateau_comb("Chateau Margaux").vintage_distance(2015)
#Chateau_comb("Chateau Margaux").price_forecaster()




