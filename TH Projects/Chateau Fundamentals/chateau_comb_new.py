# -*- coding: utf-8 -*-
"""
Created on Mon May 27 22:52:18 2019

@author: thoma
"""


from chateau_weather import Chateau
from chateau_data import Chateau_data
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta
import json
import statistics


#define our eomonth function
def eomonth(y, m):
    year = y
    if int(m) + 1 > 12:
        month = 1
        y = y+1
    else:
        month = int(m)+1
    given_day = datetime(year, month, 1)
    required_day = given_day - timedelta(days=1)
    return required_day

#unpack the dictionaries so the dates have the correct format
def dict_unpacker(sample_dict):
    dict_unpacked = {}
    for p_date, price in sample_dict.items():
         formattedas_date = datetime.strptime(p_date, "%Y-%m-%d")
         dict_unpacked[formattedas_date] = float(price)
    return dict_unpacked

# returns dict of average daily weather data aggregated by month
def seasonal_weather_dict(dict_sample):
    """returns dict of average daily weather data aggregated by month"""
    monthly_weather_dict = {}
    for p_date, precip in dict_sample.items():
        formattedas_date = p_date
        #datetime.strptime(p_date, "%Y-%m-%d")
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

#returns average seasonal weather dict
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

#returns dict of weather data aggregated by month for vintage year  
def vintage_monthly_weather_dict(dict_sample, vintage):
    """returns dict of weather data aggregated by month for vintage year"""
    monthly_weather_dict = seasonal_weather_dict(dict_sample)    
    vintage_monthly_weather_dict_final = {}
    for p_date, precip in monthly_weather_dict.items():
        if p_date.year == vintage:
            vintage_monthly_weather_dict_final[p_date] = precip
    return vintage_monthly_weather_dict_final

def all_monthly_weather_dict(dict_sample, chosen_month):
    """returns dict of weather data for chosen month for all years"""
    monthly_weather_dict = seasonal_weather_dict(dict_sample)    
    all_monthly_weather_dict_final = {}
    for p_date, precip in monthly_weather_dict.items():
        if p_date.month == int(chosen_month):
            all_monthly_weather_dict_final[p_date] = precip
    return all_monthly_weather_dict_final

def all_monthly_weather_dict_detail(dict_sample):
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

#class defn begins
#--------------------------------------------------------------------------------

class Chateau_comb():
    
    def __init__(self, address):
        """initialize attributes to define a stock"""
        self.address = address
    
    def chateau_profile(self, name, data=''):
        """Store a profile in the file so we do not repeat every action"""
        filename = (str(self.address) + "_px_analysis_profile.txt")
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
    

    def vintage_patterns(self, vintage, update=''):
        """returns the weather profile of the vintage vs average seasonality"""
       
        def proceed_with_method():
           
            weather_dict_p_raw = Chateau(self.address).weather_dict('p')
            weather_dict_v_raw = Chateau(self.address).weather_dict('v')

           
            weather_dict_p = dict_unpacker(weather_dict_p_raw)
            weather_dict_v = dict_unpacker(weather_dict_v_raw)
            
            
            monthly_weather_dict_p = vintage_monthly_weather_dict(weather_dict_p, vintage)
            monthly_weather_dict_v = vintage_monthly_weather_dict(weather_dict_v, vintage)
            seasonal_weather_dict_p = average_seasonal_weather_dict(weather_dict_p)
            seasonal_weather_dict_v = average_seasonal_weather_dict(weather_dict_v)
            
            # start chart
            x_values, y_values, z_values, sy_values, sz_values = [], [], [], [], []
        
            for key in monthly_weather_dict_p.keys():
                x_date = key
                #datetime.strptime(key, '%Y-%m-%d')
                if x_date > datetime(1970, 12, 31):
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

            weather_dict_raw = Chateau(self.address).weather_dict(category)
            price_dict_raw = Chateau_data(self.address).get_price_data()
           
            weather_dict = dict_unpacker(weather_dict_raw)
            price_dict = dict_unpacker(price_dict_raw)
            
            monthly_weather_dict = all_monthly_weather_dict(weather_dict, chosen_month)

            
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
    

    def correl_chart(self, category, chosen_month):
        """return the scatter plot across years of the month"""
       
        def proceed_with_method():
           
            weather_dict_raw = Chateau(self.address).weather_dict(category)
            price_dict_raw = Chateau_data(self.address).get_price_data()
           
            weather_dict = dict_unpacker(weather_dict_raw)
            price_dict = dict_unpacker(price_dict_raw)

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
                if price > av + 0.5*sd and px_date > datetime(1970, 12, 31):
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

    def correl_analysis(self, category, update=''):
        """return the scatter plot across years of the month"""
       
        def proceed_with_method():
           
            weather_dict_raw = Chateau(self.address).weather_dict(category)
            price_dict_raw = Chateau_data(self.address).get_price_data()
           
            weather_dict = dict_unpacker(weather_dict_raw)
            price_dict = dict_unpacker(price_dict_raw)
            
            correl_dict = {}
            def correl_calculator(chosen_month):
                monthly_weather_dict = all_monthly_weather_dict(weather_dict, chosen_month)
                
                #find the average price
                px_list = []
                for px_date, price in price_dict.items():
                    if px_date > datetime(1970, 12, 31):
                        px_list.append(price)
                
                av = statistics.mean(px_list)
                sd = statistics.stdev(px_list)
                                              
                
                #add prices above average to the selected list
                selected_price_dict = {}
                y_values = []
                for px_date, price in price_dict.items():
                    if price > av + 0.5*sd and px_date > datetime(1970, 12, 31):
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
                R = np.corrcoef(y, correl_y)
                cor = R.item(1) #R is a 2x2 matrix so take the correct entry
                #print(str(chosen_month) + ": " + str(cor))
                return [cor, z.item(0), z.item(1), z.item(2)]
            
            for i in range(1,13):
                correl_dict[i] = correl_calculator(i)   
            
            return correl_dict
        
        title = "correl_analysis_" + str(category)
        if update:
            data = proceed_with_method()
            Chateau_comb(self.address).chateau_profile(title, data)
            print(str(title) + " updated")
            return Chateau_comb(self.address).chateau_profile(title)

        elif Chateau_comb(self.address).chateau_profile(title) == None:
            data = proceed_with_method()
            Chateau_comb(self.address).chateau_profile(title, data)
            return Chateau_comb(self.address).chateau_profile(title)

        else:
            return Chateau_comb(self.address).chateau_profile(title)
        
    def print_correl_analysis(self, category, update=''):
        """return the scatter plot across years of the month"""
        title = "correl_analysis_" + str(category)
        correl_dict = Chateau_comb(self.address).chateau_profile(title)
        
        print("\nFor category " +str(category) + ":")
        for i in range(1,13):
            print("Month "+ str(i) + " has correlation: " +str('%.2f' % correl_dict[str(i)][0]))

    def used_correl_analysis(self, category, update=''):
        """return the scatter plot across years of the month"""
       
        def proceed_with_method():
            title = "correl_analysis_" + str(category)
            correl_dict = Chateau_comb(self.address).chateau_profile(title)
            new_dict = {}
            for i in range(1,13):
                if correl_dict[str(i)][0] > 0.6:
                    new_dict[i] = correl_dict[str(i)]
            
            return new_dict
        
        title = "used_correl_analysis_" + str(category)
        if update:
            data = proceed_with_method()
            Chateau_comb(self.address).chateau_profile(title, data)
            print(str(title) + " updated")
            return Chateau_comb(self.address).chateau_profile(title)

        elif Chateau_comb(self.address).chateau_profile(title) == None:
            data = proceed_with_method()
            Chateau_comb(self.address).chateau_profile(title, data)
            return Chateau_comb(self.address).chateau_profile(title)

        else:
            return Chateau_comb(self.address).chateau_profile(title)
        
        
    def vintage_rule_finder(self, category, update=''):
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

            weather_dict = dict_unpacker(weather_dict_raw)
            price_dict = dict_unpacker(price_dict_raw)
            
           # monthly_weather_dict = all_monthly_weather_dict(weather_dict, chosen_month)
            
            #find the list of top prices
            prices, prices_dates, top_prices, lower_prices, top_prices_dates, lower_prices_dates = [], [], [], [], [], []
            for px_date, price in price_dict.items():
                if px_date > datetime(1970, 12, 31):
                   prices.append(price)
                   prices_dates.append(px_date)

            av = statistics.mean(prices)
            sd = statistics.stdev(prices)
        
            print("\nAverage/Stdev price is: " + str(av) + "/ " + str(sd) + "\n")

            for i in range(0, len(prices)-1):
                if prices[i] > av + 0.5 * sd:
                    top_prices.append(prices[i])
                    top_prices_dates.append(prices_dates[i])
                elif prices[i] < av - 0 * sd:
                    lower_prices.append(prices[i])
                    lower_prices_dates.append(prices_dates[i])
            
            poor_criteria_dict = {}
            
            for i in range(1,13):
                poor_criteria_dict[i] = []
                
           
            weather_stats = all_monthly_weather_dict_detail(weather_dict)
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
                    
                    if weather_stat > av + 2*sd:
                        title = "sig over av"
                        if title not in poor_criteria_dict[i]:
                            poor_criteria_dict[i].append(title)
                    
                    elif weather_stat > av + 1*sd:
                        title = "slight over av"
                        if title not in poor_criteria_dict[i]:
                            poor_criteria_dict[i].append(title)
                    
                    elif weather_stat < av - 2*sd:
                        title = "slight under av"
                        if title not in poor_criteria_dict[i]:
                            poor_criteria_dict[i].append(title)
                    
                    elif weather_stat < av - 1*sd:
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
                    
                    if weather_stat > av + 2*sd:
                        title = "sig over av"
                        if title not in top_criteria_dict[i]:
                            top_criteria_dict[i].append(title)
                    
                    elif weather_stat > av + 1*sd:
                        title = "slight over av"
                        if title not in top_criteria_dict[i]:
                            top_criteria_dict[i].append(title)
                    
                    elif weather_stat < av - 2*sd:
                        title = "sig under av"
                        if title not in top_criteria_dict[i]:
                            top_criteria_dict[i].append(title)
                    
                    elif weather_stat < av - 1*sd:
                        title = "slight under av"
                        if title not in top_criteria_dict[i]:
                            top_criteria_dict[i].append(title)
            
            bad_criteria_dict = {}
            
            for i in range(1,13):
                bad_criteria_dict[i] = []
                
            for i in range(1, 13):
                y = [x for x in poor_criteria_dict[i] if x not in top_criteria_dict[i]]
                av = weather_stats[i][0]
                sd = weather_stats[i][1]
                bad_criteria_dict[i] = [y, av, sd]
            
            good_criteria_dict = {}
            
            for i in range(1,13):
                good_criteria_dict[i] = []
                
            for i in range(1, 13):
                y = [x for x in top_criteria_dict[i] if x not in poor_criteria_dict[i]]
                av = weather_stats[i][0]
                sd = weather_stats[i][1]
                good_criteria_dict[i] = [y, av, sd]
            
            print("\n" + str(self.address) + " great vintages have had these seasonal " +str(category)+" weather anomalies: " + str(top_criteria_dict))
            print("\n" + str(self.address) + " standard vintages have had these seasonal " +str(category)+" weather anomalies: " + str(poor_criteria_dict))
            print("\n" + str(self.address) + " we will use the following criteria as bad " +str(category)+" vintage indicators: " + str(bad_criteria_dict))
            #print("\n" + str(self.address) + " we will use the following criteria as good vintage indicators: " + str(good_criteria_dict))
            return bad_criteria_dict
            

        title = "vintage_rule_finder_" + str(category)
        if update:
            data = proceed_with_method()
            Chateau_comb(self.address).chateau_profile(title, data)
            print(str(title) + " updated")
            return Chateau_comb(self.address).chateau_profile(title)

        elif Chateau_comb(self.address).chateau_profile(title) == None:
            data = proceed_with_method()
            Chateau_comb(self.address).chateau_profile(title, data)
            return Chateau_comb(self.address).chateau_profile(title)

        else:
            return Chateau_comb(self.address).chateau_profile(title)

    def vintage_rule_finder_analysis(self, update=''):
        """analysis of vintage rule strikes vs price"""
        def proceed_with_method():
            criteria_dict_p = Chateau_comb(self.address).chateau_profile('vintage_rule_finder_p')
            criteria_dict_v = Chateau_comb(self.address).chateau_profile('vintage_rule_finder_v')
            
            weather_dict_raw_p = Chateau(self.address).weather_dict('p')
            weather_dict_raw_v = Chateau(self.address).weather_dict('v')

            price_dict_raw = Chateau_data(self.address).get_price_data()

            weather_dict_p = dict_unpacker(weather_dict_raw_p)
            weather_dict_v = dict_unpacker(weather_dict_raw_v)
            
            seasonal_weather_dict_p = seasonal_weather_dict(weather_dict_p)
            seasonal_weather_dict_v = seasonal_weather_dict(weather_dict_v)

            price_dict = dict_unpacker(price_dict_raw)
            
            strike_dict = {}
            for px_date, price in price_dict.items():
                if px_date > datetime(1970, 12, 31):
                   y = px_date.year
                   strike = 0
                 
                   #exceptions in p
                   for i in range(1,10):
                       m = i
                       required_day = eomonth(y,m)
                       data = seasonal_weather_dict_p[required_day]
                       av = criteria_dict_p[str(i)][1]
                       sd = criteria_dict_p[str(i)][2]
                       for t in range(0,len(criteria_dict_p[str(i)][0])-1):
                           if criteria_dict_p[str(i)][0][t] == 'sig over av':
                               if data > av + 2 * sd:
                                   strike = strike + 1

                           if criteria_dict_p[str(i)][0][t] == 'slight over av':
                               if data > av + 1 * sd and data < av + 2 * sd:
                                   strike = strike + 1                                   
                                   
                           if criteria_dict_p[str(i)][0][t] == 'sig under av':
                               if data < av - 2 * sd:
                                   strike = strike + 1                               
                               
                           if criteria_dict_p[str(i)][0][t] == 'slight under av':
                               if data < av - 1 * sd and data > av - 2 * sd:
                                   strike = strike + 1

                   #exceptions in v
                   for i in range(1,13):
                       m = i
                       required_day = eomonth(y,m)
                       data = seasonal_weather_dict_v[required_day]
                       av = criteria_dict_v[str(i)][1]
                       sd = criteria_dict_v[str(i)][2]
                       for t in range(0,len(criteria_dict_v[str(i)][0])-1):
                           if criteria_dict_v[str(i)][0][t] == 'sig over av':
                               if data > av + 2 * sd:
                                   strike = strike + 1

                           if criteria_dict_v[str(i)][0][t] == 'slight over av':
                               if data > av + 1 * sd and data < av + 2 * sd:
                                   strike = strike + 1                                   
                                   
                           if criteria_dict_v[str(i)][0][t] == 'sig under av':
                               if data < av - 2 * sd:
                                   strike = strike + 1                               
                               
                           if criteria_dict_v[str(i)][0][t] == 'slight under av':
                               if data < av - 1 * sd and data > av - 2 * sd:
                                   strike = strike + 1         
                    
                   strike_dict[str(eomonth(int(px_date.year), 12))] = [price, strike] 

            return strike_dict                  

        title = "vintage_rule_finder_analysis"
        if update:
            data = proceed_with_method()
            Chateau_comb(self.address).chateau_profile(title, data)
            print(str(title) + " updated")
            return Chateau_comb(self.address).chateau_profile(title)

        elif Chateau_comb(self.address).chateau_profile(title) == None:
            data = proceed_with_method()
            Chateau_comb(self.address).chateau_profile(title, data)
            return Chateau_comb(self.address).chateau_profile(title)

        else:
            return Chateau_comb(self.address).chateau_profile(title)        
        

    def vintage_rule_finder_analysis_print(self):
        """analysis of vintage rule strikes vs price"""
        def proceed_with_method():
            criteria_dict_p = Chateau_comb(self.address).chateau_profile('vintage_rule_finder_p')
            criteria_dict_v = Chateau_comb(self.address).chateau_profile('vintage_rule_finder_v')
            
            weather_dict_raw_p = Chateau(self.address).weather_dict('p')
            weather_dict_raw_v = Chateau(self.address).weather_dict('v')

            price_dict_raw = Chateau_data(self.address).get_price_data()

            weather_dict_p = dict_unpacker(weather_dict_raw_p)
            weather_dict_v = dict_unpacker(weather_dict_raw_v)
            
            seasonal_weather_dict_p = seasonal_weather_dict(weather_dict_p)
            seasonal_weather_dict_v = seasonal_weather_dict(weather_dict_v)

            price_dict = dict_unpacker(price_dict_raw)
            
            strike_dict = {}
            for px_date, price in price_dict.items():
                if px_date > datetime(1970, 12, 31):
                   y = px_date.year
                   strike = 0
                 
                   #exceptions in p
                   for i in range(1,10):
                       m = i
                       required_day = eomonth(y,m)
                       data = seasonal_weather_dict_p[required_day]
                       av = criteria_dict_p[str(i)][1]
                       sd = criteria_dict_p[str(i)][2]
                       for t in range(0,len(criteria_dict_p[str(i)][0])-1):
                           if criteria_dict_p[str(i)][0][t] == 'sig over av':
                               if data > av + 2 * sd:
                                   strike = strike + 1

                           if criteria_dict_p[str(i)][0][t] == 'slight over av':
                               if data > av + 1 * sd and data < av + 2 * sd:
                                   strike = strike + 1                                   
                                   
                           if criteria_dict_p[str(i)][0][t] == 'sig under av':
                               if data < av - 2 * sd:
                                   strike = strike + 1                               
                               
                           if criteria_dict_p[str(i)][0][t] == 'slight under av':
                               if data < av - 1 * sd and data > av - 2 * sd:
                                   strike = strike + 1

                   #exceptions in v
                   for i in range(1,13):
                       m = i
                       required_day = eomonth(y,m)
                       data = seasonal_weather_dict_v[required_day]
                       av = criteria_dict_v[str(i)][1]
                       sd = criteria_dict_v[str(i)][2]
                       for t in range(0,len(criteria_dict_v[str(i)][0])-1):
                           if criteria_dict_v[str(i)][0][t] == 'sig over av':
                               if data > av + 2 * sd:
                                   strike = strike + 1

                           if criteria_dict_v[str(i)][0][t] == 'slight over av':
                               if data > av + 1 * sd and data < av + 2 * sd:
                                   strike = strike + 1                                   
                                   
                           if criteria_dict_v[str(i)][0][t] == 'sig under av':
                               if data < av - 2 * sd:
                                   strike = strike + 1                               
                               
                           if criteria_dict_v[str(i)][0][t] == 'slight under av':
                               if data < av - 1 * sd and data > av - 2 * sd:
                                   strike = strike + 1         
                    
                   strike_dict[eomonth(px_date.year, 12)] = [price, strike]             
            
            #calculate best fit line
            x_values, y_values = [], []
            for key in strike_dict.keys():
                y_values.append(strike_dict[key][0])
                x_values.append(strike_dict[key][1])
            
            
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
            plt.xlabel("Strikes", fontsize =12)
            #plt.xticks(np.arange(x_values[11], x_values[0], 2))
            plt.ylabel("Price", color='black', fontsize =12)
            plt.scatter(x_values, y_values, color=color)
            plt.plot(xp, p(xp), color = 'red')
            plt.tick_params(axis='y', labelcolor=color)
            
                       
            #remove borders
            plt.gca().spines['top'].set_visible(False)
            
            #Chart title
            plt.title(str(self.address)+ " Strikes vs Price:  ", fontsize = 14)
            
            #Show chart
            plt.show()
            
        proceed_with_method()


    def price_forecaster(self, vintage, update=''):
        """returns the weather profile of the vintage"""
        def proceed_with_method():
            dict_forecast_v = Chateau_comb(self.address).used_correl_analysis('v', str(update))
            dict_forecast_p = Chateau_comb(self.address).used_correl_analysis('p', str(update))
            weather_dict_raw_p = Chateau(self.address).weather_dict('p')
            weather_dict_p = dict_unpacker(weather_dict_raw_p)

            weather_dict_raw_v = Chateau(self.address).weather_dict('v')
            weather_dict_v = dict_unpacker(weather_dict_raw_v)
            
            
            m_weather_dict_p = seasonal_weather_dict(weather_dict_p)
            m_weather_dict_v = seasonal_weather_dict(weather_dict_v)
            
            price_predictions = []
            
            for i in dict_forecast_v.keys():
                y = vintage
                m = i
                required_date = eomonth(y, m)
                x = m_weather_dict_v[required_date]
                
                a = dict_forecast_v[i][1]
                b = dict_forecast_v[i][2]
                c = dict_forecast_v[i][3]
                
                p = a * x * x + b * x + c
                price_predictions.append(p)
                
            for i in dict_forecast_p.keys():
                y = vintage
                m = i
                required_date = eomonth(y, m)
                x = m_weather_dict_p[required_date]
                
                a = dict_forecast_p[i][1]
                b = dict_forecast_p[i][2]
                c = dict_forecast_p[i][3]
                
                p = a * x * x + b * x + c
                price_predictions.append(p)   
            
            predictions_av = statistics.mean(price_predictions)
            
            
            #apply factor now based on strikes
            #calculate best fit line
            strike_dict = Chateau_comb(self.address).vintage_rule_finder_analysis(update)

            x_values, y_values = [], []
            for key in strike_dict.keys():
                y_values.append(strike_dict[key][0])
                x_values.append(strike_dict[key][1])
                       
            x = x_values
            y = y_values
            z = np.polyfit(x, y, 2)
            p = np.poly1d(z)
            
            vintage_date = eomonth(vintage, 12)
            strikes = strike_dict[str(vintage_date)][1]
            

            #find the list of top prices

            price_dict_raw = Chateau_data(self.address).get_price_data()
            price_dict = dict_unpacker(price_dict_raw)

            prices, top_prices = [], []
            for px_date, price in price_dict.items():
                if px_date > datetime(1970, 12, 31):
                   prices.append(price)

            av = statistics.mean(prices)
            sd = statistics.stdev(prices)

        
            for i in range(0, len(prices)-1):
                if prices[i] > av + 0.5 * sd:
                    top_prices.append(prices[i])
            
            top_price_mean = statistics.mean(top_prices)
            
            if strikes == 0:
                adj_prediction = predictions_av
            
            if strikes > 0 :
                adj_prediction = predictions_av * p(strikes) / top_price_mean
               
            print('%.2f' % adj_prediction)
            return adj_prediction
                   
        r = proceed_with_method()
        return r

    def price_forecaster_tester(self, beg_year, update=''):
        """returns the weather profile of the vintage"""
        def proceed_with_method():
            price_dict_raw = Chateau_data(self.address).get_price_data()
            price_dict = dict_unpacker(price_dict_raw)
            
            #create the chart list
            x_values, y_values, z_values = [], [], []
            
            for key in price_dict.keys():
                x_date = key
                if int(x_date.year) > int(beg_year):
                    x_values.append(key.year)
                    y_values.append(float(str(price_dict[key])))
                    forecast = Chateau_comb(self.address).price_forecaster(x_date.year)
                    print(x_date.year)
                    z_values.append(forecast)
           
            print(y_values)
            print(z_values)
            
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
            plt.ylabel("Price", color='black', fontsize =12)
            plt.bar(x_values, y_values, facecolor='none', edgecolor='blue',)
            plt.scatter(x_values, z_values, color='red', linestyle ='dashed')
            plt.tick_params(axis='y', labelcolor=color)
            
            #ax2 = plt.twinx()  # instantiate a second axes that shares the same x-axis
            
            #axis 2
            #color = 'tab:red'
            #ax2.set_ylabel("Price", color='black', fontsize=12)  # we already handled the x-label with ax1
            #ax2.plot(x_values, y_values, color=color)
            #ax2.scatter(x_values, z_values, color=color, linestyle='dashed')
            #ax2.tick_params(axis='y', labelcolor=color)
            
            #remove borders
            plt.gca().spines['top'].set_visible(False)
            
            #Chart title
            plt.title(str(self.address)+ " actual px vs forecast", fontsize = 14)
            
            #Show chart
            plt.show()

        proceed_with_method()  

#for i in range(1,13):
    #Chateau_comb("Chateau Margaux").annual_price_weather_chart('p', i)
#Chateau_data("Chateau Margaux").print_wine_price(1970)   
#Chateau_comb("Chateau Margaux").vintage_patterns(2015)
#Chateau_comb("Chateau Margaux").vintage_patterns(2010)
#Chateau_comb("Chateau Margaux").vintage_patterns(2009)
#Chateau_comb("Chateau Margaux").vintage_patterns(2005)
#Chateau_comb("Chateau Margaux").vintage_patterns(2016)
#Chateau_comb("Chateau Margaux").vintage_patterns(1996)
#Chateau_comb("Chateau Margaux").vintage_patterns(2017)
#Chateau_comb("Chateau Margaux").vintage_patterns(2014)
#Chateau_comb("Chateau Margaux").vintage_patterns(2013)
#Chateau_comb("Chateau Margaux").vintage_patterns(2007)

#Chateau_comb("Chateau Margaux").scatter_analysis('v','7')
#Chateau_comb("Chateau Margaux").correl_chart('v','4')
#Chateau_comb("Chateau Margaux").correl_analysis('p', 'update')
#Chateau_comb("Chateau Margaux").used_correl_analysis('v', 'update')
#Chateau_comb("Chateau Margaux").print_correl_analysis('p', 'update')
#Chateau_comb("Chateau Margaux").vintage_rule_finder('v', 'update')
#Chateau_comb("Chateau Margaux").vintage_rule_finder_analysis()

#Chateau_comb("Chateau Margaux").vintage_rule_finder_analysis_print()

#Chateau_comb("Chateau Margaux").price_forecaster(1993)
#Chateau_comb("Chateau Margaux").price_forecaster_tester(1980)