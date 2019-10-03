# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 13:28:55 2019

@author: thoma
"""
from datetime import datetime, date, timedelta
#define our eomonth function
def eomonth(y, m):
    remainder = divmod(m,12)
    y_adj = remainder[0]
    m_adj = remainder[1] + 1
    given_day = datetime(int(y) + y_adj, m_adj, 1)
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