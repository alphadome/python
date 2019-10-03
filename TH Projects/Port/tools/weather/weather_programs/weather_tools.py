# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 13:28:55 2019

@author: thoma
"""
from datetime import datetime, date, timedelta
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta
import json
import statistics
from geopy.geocoders import Nominatim
from math import sin, cos, sqrt, atan2, radians


#define our eomonth function

def text_between(text, left, right):
    between = text[text.index(left)+len(left):text.index(right)]
    return between

def eomonth(y, m):
    remainder = divmod(m,12)
    y_adj = remainder[0]
    m_adj = remainder[1] + 1
    given_day = datetime(int(y) + y_adj, m_adj, 1)
    required_day = given_day - timedelta(days=1)
    return required_day

def somonth(y, m):
    remainder = divmod(m,12)
    y_adj = remainder[0]
    m_adj = remainder[1] + 1
    given_day = datetime(int(y) + y_adj, m_adj - 1, 1)
    required_day = given_day
    return required_day

def join_dicts(dict1, dict2):
    dict_combined = {}
    for key, item in dict1.items():
        dict_combined[key] = item
        
    for key2, item2 in dict2.items():
        if key2 in dict1.keys():
            None
        else:
           dict_combined[key2] = item2
    return dict_combined

def coordinate_distance(lat1,lon1,lat2,lon2):
    # approximate radius of earth in km
    R = 6373.0
    
    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))
    lat2 = radians(float(lat2))
    lon2 = radians(float(lon2))
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance = R * c
    return float(distance)

def find_lat_lon(address):
    try:
        geolocator = Nominatim(user_agent="my-application", timeout=30)
        location = geolocator.geocode(address)
        lat1 = location.latitude
        lon1 = location.longitude
        return(lat1, lon1)
        
    except Exception:
        return str("Not found")
    
    
    
#unpack the dictionaries so the dates have the correct format
def dict_unpacker(sample_dict):
    dict_unpacked = {}
    for p_date, price in sample_dict.items():
        formattedas_date = datetime.strptime(str(p_date), "%Y-%m-%d")
        try:
            dict_unpacked[formattedas_date] = float(price) #consider floating price
        except Exception:
            dict_unpacked[formattedas_date] = price #consider floating price
             
    return dict_unpacked


def rolling_day(x, sample_dict):
    """gives the rolling dict but only with dates already in the dict"""
    rolling_dict = {}
        
    for p_date, precip in sample_dict.items():
        f_date = p_date #datetime.strptime(p_date, "%Y-%m-%d")
        avg_precip_list = []
        for i in range(0,x):
            test_date = f_date - timedelta(days=i)
            if test_date in sample_dict.keys():
                avg_precip_list.append(sample_dict[test_date])
        
        try:
            rolling_dict[p_date] = float("{0:.2f}".format(statistics.mean(avg_precip_list)))
        except Exception:
            None
    return rolling_dict
            
def rolling_day_all_days(x, sample_dict):
    """give the rolling dict where possible with all dates"""

    #find all years in the dict
    year_list = []
    for key in sample_dict.keys():
        if key.year not in year_list:
            year_list.append(key.year)
    
    #create a list of all dates in a year
    date_list = []
    for year in year_list:
        for m in range(1,13):
            for d in range(1,31):
                try:
                    f_date = datetime(year,m,d)
                    date_list.append(f_date)
                except Exception:
                    None
    
    #matches rolling_dict dates with sample dict dates                
    rolling_dict = {}
    for f_date in date_list:
        rolling_list = []
        for i in range(0,x):
            test_date = f_date - timedelta(days=i)
            try:
                rolling_list.append(sample_dict[test_date])
            except Exception:
                None
        #try adding - if it doesnt add its empty, which is ok
        try:
            rolling_dict[f_date] = float("{0:.2f}".format(statistics.mean(rolling_list)))
        except Exception:
            None        
           
    return rolling_dict
            


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

#returns average daily seasonal weather dict
def avg_daily_seasonal_weather_dict(dict_sample, vintage):
    """returns average seasonal weather dictionary"""
    desired_dict = {}
    
    for p_date, data in dict_sample.items():
        try:
            desired_date = datetime(date.today().year, p_date.month, p_date.day)
            if desired_date in desired_dict.keys():
                None
            else:
                desired_dict[str(desired_date).replace(" 00:00:00",'')] = []
        except Exception:
            None

    desired_dict = dict_unpacker(desired_dict)
    for p_date, data in dict_sample.items():
        for d_date, d_list in desired_dict.items():
            if d_date.month == p_date.month and d_date.day == p_date.day and int(vintage) > p_date.year:
                d_list.append(data)
                desired_dict[d_date] = d_list
                
    for d_date, d_list in desired_dict.items():
        try:
            desired_dict[d_date] = float("{0:.2f}".format(float(statistics.mean(d_list))))
        except Exception:
            None
            
    return desired_dict

#returns dict of weather data aggregated by month for vintage year  
def vintage_monthly_weather_dict(dict_sample, vintage):
    """returns dict of weather data aggregated by month for vintage year"""
    monthly_weather_dict = seasonal_weather_dict(dict_sample)
    vintage_monthly_weather_dict_final = {}
    for p_date, precip in monthly_weather_dict.items():
        if float(p_date.year) == float(vintage):
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

def seasonal(sample_dict, x):
    """returns seasonality dict over x years"""
    sample_dict = rolling_day_all_days(7,dict_unpacker(sample_dict))
    
    year_list = []
    for key in sample_dict.keys():
        if key.year not in year_list:
            year_list.append(key.year)
    
    seasonal_dict = {}
    diff_dict = {}
    for key, items in sample_dict.items():
        s_list = []       
        for year in year_list:
            if year < key.year and year > key.year - x:
                try:
                    s_date = datetime(int(year), key.month, key.day)
                    s_list.append(sample_dict[s_date])
                except Exception:
                    None
        try:
            seasonal_dict[str(key).replace(" 00:00:00",'')] = statistics.mean(s_list)
            diff_dict[str(key).replace(" 00:00:00",'')] = sample_dict[key] - statistics.mean(s_list)
        except Exception:
            None
    
    return seasonal_dict

def diff_from_seasonal(sample_dict, x):
    """returns seasonality dict over x years"""
    sample_dict = rolling_day_all_days(7,dict_unpacker(sample_dict))
    
    year_list = []
    for key in sample_dict.keys():
        if key.year not in year_list:
            year_list.append(key.year)
    
    seasonal_dict = {}
    diff_dict = {}
    for key, items in sample_dict.items():
        s_list = []       
        for year in year_list:
            if year < key.year and year > key.year - x:
                try:
                    s_date = datetime(int(year), key.month, key.day)
                    s_list.append(sample_dict[s_date])
                except Exception:
                    None
        try:
            seasonal_dict[str(key).replace(" 00:00:00",'')] = statistics.mean(s_list)
            
            diff = sample_dict[key] - statistics.mean(s_list)
            if key.month == 1 or key.month == 12: #this gets skewed by continutity at year edges
                diff = 0
            
            diff_dict[str(key).replace(" 00:00:00",'')] = diff
        except Exception:
            None
    
    return diff_dict
    
    

def seasonal_patterns(weather_dict_p_raw, weather_dict_v_raw, vintage):
    """returns the weather profile of the vintage vs average seasonality"""
       
    weather_dict_p = dict_unpacker(weather_dict_p_raw)
    weather_dict_v = dict_unpacker(weather_dict_v_raw)
    
    monthly_weather_dict_p = vintage_monthly_weather_dict(weather_dict_p, vintage)
    monthly_weather_dict_v = vintage_monthly_weather_dict(weather_dict_v, vintage)
    seasonal_weather_dict_p = average_seasonal_weather_dict(weather_dict_p)
    seasonal_weather_dict_v = average_seasonal_weather_dict(weather_dict_v)
    
    # start chart
    x_values, y_values, z_values, sy_values, sz_values = [], [], [], [], []
    
    datelist = []
    if eomonth(vintage,12) > datetime(date.today().year,date.today().month,date.today().day):
        for i in range(1,13):
            datelist.append(eomonth(date.today().year,i))
    else:
        for i in range(1,13):
            datelist.append(eomonth(vintage,i))

    for key in datelist:#monthly_weather_dict_p.keys():
        x_date = key
        #datetime.strptime(key, '%Y-%m-%d')
        if x_date > datetime(1970, 12, 31):
            x_values.append(key)
            #y_values.append(float(str(monthly_weather_dict_p[key]))-float(str(seasonal_weather_dict_p[key.month])))
            #z_values.append(monthly_weather_dict_v[x_date]-seasonal_weather_dict_v[x_date.month])
            sy_values.append(float(str(seasonal_weather_dict_p[key.month])))
            sz_values.append(seasonal_weather_dict_v[x_date.month])
            try:
                y_values.append(float(str(monthly_weather_dict_p[key])))
            except Exception:
                y_values.append(float(str(seasonal_weather_dict_p[key.month])))
                
            try:
                z_values.append(monthly_weather_dict_v[x_date])
            except Exception:
                z_values.append(seasonal_weather_dict_v[x_date.month])
                    
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
    plt.title("Weather Pattern for Year:  "+str(vintage), fontsize = 14)
    
    #Show chart
    plt.show()



def seasonal_patterns_w_price(weather_dict_p_raw, weather_dict_v_raw, price_dict, vintage):
    """returns the weather profile of the vintage vs average seasonality"""
       
    weather_dict_p = rolling_day_all_days(7,dict_unpacker(weather_dict_p_raw))
    weather_dict_v = rolling_day_all_days(7,dict_unpacker(weather_dict_v_raw))
    price_dict = rolling_day_all_days(7,dict_unpacker(price_dict))
    
    seasonal_weather_dict_p = rolling_day(7,avg_daily_seasonal_weather_dict(weather_dict_p, vintage))
    seasonal_weather_dict_v = rolling_day(7,avg_daily_seasonal_weather_dict(weather_dict_v, vintage))
    seasonal_price_dict = rolling_day(7,avg_daily_seasonal_weather_dict(price_dict, vintage))
    
    print()
    
    # start chart
    x_values, y_values, z_values, sy_values, sz_values = [], [], [], [], []
    a_values, sa_values = [], []
    #print(sorted(weather_dict_p.keys()))
    datelist = []
    if eomonth(vintage,12) > datetime(date.today().year,date.today().month,date.today().day):
        for key in weather_dict_p.keys():
            if int(key.year) == float(vintage) - 1:
                try:
                    datelist.append(datetime(key.year+1, key.month, key.day))
                except Exception:
                    None
    else:
        for key in weather_dict_p.keys():
            if key.year == int(vintage):
                datelist.append(key)
    
    datelist = sorted(datelist) #need this otherwise dates come jumbled up and messes up graph
    for i in range(len(datelist)):#monthly_weather_dict_p.keys():
        
        key = datelist[i]
        x_date = key
        #datetime.strptime(key, '%Y-%m-%d')
        if x_date > datetime(1970, 12, 31):
            x_values.append(key)
            #y_values.append(float(str(monthly_weather_dict_p[key]))-float(str(seasonal_weather_dict_p[key.month])))
            #z_values.append(monthly_weather_dict_v[x_date]-seasonal_weather_dict_v[x_date.month])
            
            try:
                sy_values.append(float(str(seasonal_weather_dict_p[datetime(date.today().year, key.month, key.day)])))
            except Exception:
                try:
                    sy_values.append(sy_values[len(sy_values)-1])
                except Exception:
                    sy_values.append('exception')            
            try:
                sz_values.append(float(str(seasonal_weather_dict_v[datetime(date.today().year, key.month, key.day)])))
            except Exception:
                try:
                    sz_values.append(sz_values[len(sz_values)-1])           
                except Exception:
                    sz_values.append('exception')            
            try:
                y_values.append(float(str(weather_dict_p[key])))
            except Exception:
                #y_values.append(float(str(seasonal_weather_dict_p[datetime(date.today().year, key.month, key.day)])))
                try:
                    y_values.append(y_values[len(y_values)-1])
                except Exception:
                    y_values.append('exception')            
            try:
                z_values.append(weather_dict_v[key])
            except Exception:
                #z_values.append(float(str(seasonal_weather_dict_v[datetime(date.today().year, key.month, key.day)])))
                try:
                    z_values.append(z_values[len(z_values)-1])
                except Exception:
                    z_values.append('exception')  
            try:
                a_values.append(price_dict[key])
            except Exception:
                try:
                    a_values.append(a_values[len(a_values)-1])
                except Exception:
                    a_values.append('exception')

            try:
                sa_values.append(float(str(seasonal_price_dict[datetime(date.today().year, key.month, key.day)])))
            except Exception:
                try:
                    sa_values.append(sa_values[len(sa_values)-1])  
                except Exception:
                    sa_values.append('exception')
    
    #print(x_values)
    #print(a_values)
    #print("OK")
    for i in range(len(datelist)):
        for current_list in [x_values, y_values, z_values, sy_values, sz_values, a_values, sa_values]:
            if current_list[i] == 'exception':
                try:
                    for t in range(len(datelist)-i):
                        if current_list[i+t] != 'exception':
                            current_list[i] = current_list[i+t]
                            break
                        else:
                            None
                                
                except Exception:
                    current_list[i] = 0
                    
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
    
    ax3 = plt.twinx()  # instantiate a second axes that shares the same x-axis
    
    #axis 3
    color = 'tab:black'
    ax3.set_ylabel("Price", color='black', fontsize=12)  # we already handled the x-label with ax1
    ax3.plot(x_values, a_values, color='black')
    #ax3.plot(x_values, sa_values, color='black', linestyle ='dashed')
    ax3.tick_params(axis='y', labelcolor='black')
    #ax3.invert_yaxis()

    #remove borders
    plt.gca().spines['top'].set_visible(False)
    
    #Chart title
    plt.title("Weather Pattern for Year:  "+str(vintage), fontsize = 14)
    
    #Show chart
    plt.show()

if __name__ == '__main__':
    None