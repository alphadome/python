# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 21:41:26 2019

@author: thoma
"""

file_name =  r"C:\Users\thoma\Desktop\Python\TH Projects\Port\alpha\corn\corn_prod_us_state.xlsx"
sheet =  'us_state'

import pandas as pd
df = pd.read_excel(io=file_name, sheet_name=sheet)
#print(df.head(15))  # print first 5 rows of the dataframe

# Reading an excel file using Python 
import xlrd 
  
# Give the location of the file 
loc = (r"C:\Users\thoma\Desktop\Python\TH Projects\Port\alpha\corn\corn_prod_us_state.xlsx") 
  
import sys
import_list = [
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools",
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata",
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\general\scraper",
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs"        

        ]
for import_location in import_list:
    if import_location not in sys.path:
        sys.path.append(import_location)

from weather_downloader import get_weather
from weather_tools import seasonal_patterns_w_price, seasonal_patterns, seasonal, diff_from_seasonal
from mktprice_call import quandl_dict_unpacker
import json

def state_names():
    filename = (r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_custom_profile_mix\corn.txt") 
    with open(filename) as f:
        corn_dict = json.load(f)
    
    state_list = []
    for key, items in corn_dict.items():
        state_list.append(key)
    
    print(state_list)
    return state_list

#state_list = state_names()

#for state in state_list:
#    print(state)
#    weather = get_weather(state)
#    precip_dict = weather[0]
#    temp_dict = weather[1]
#    seasonal_patterns_w_price(precip_dict, temp_dict, precip_dict, '2019')
    #for i in range(2015,2020):
    #seasonal_patterns_w_price(precip_dict, temp_dict, precip_dict, '2019')


corn_price_location = r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata\data\CORN_quandl_price_data.txt"
with open(corn_price_location) as f:
    metadata_dict = json.load(f)

price_dict = quandl_dict_unpacker(metadata_dict)

progress_dest = (r"C:\Users\thoma\Desktop\Python\TH Projects\Port\alpha\corn\corn_crop_progress_time_series_dict.txt")
with open(progress_dest) as f:
    progress_dict = json.load(f)

forecast_dest = (r"C:\Users\thoma\Desktop\Python\TH Projects\Port\alpha\corn\corn_crop_forecast_time_series_dict.txt")
with open(forecast_dest) as f:
    forecast_dict = json.load(f)
    
forecast_dict = diff_from_seasonal(forecast_dict, 5) #seasonal(forecast_dict, 5)
#print(forecast_dict)

inverted_progress_dict = {}
for key, item in forecast_dict.items():#progress_dict.items():
    inverted_progress_dict[key] = -1 * item

weather = get_weather("corn")
precip_dict = weather[0]
temp_dict = weather[1]  
#seasonal_patterns_w_price(precip_dict, temp_dict, price_dict, '2015')
#below shows that reported corn progress drives the corn price
seasonal_patterns_w_price(price_dict, price_dict, inverted_progress_dict, '2019')
seasonal_patterns_w_price(price_dict, price_dict, inverted_progress_dict, '2018')
seasonal_patterns_w_price(price_dict, price_dict, inverted_progress_dict, '2017')
seasonal_patterns_w_price(price_dict, price_dict, inverted_progress_dict, '2016')
seasonal_patterns_w_price(price_dict, price_dict, inverted_progress_dict, '2015')
seasonal_patterns_w_price(price_dict, price_dict, inverted_progress_dict, '2014')
#investigating weather vs corn progress
#seasonal_patterns_w_price(precip_dict, temp_dict, inverted_progress_dict, '2019')
#take the seasonal progress add to the seaonsal weather dict and map that as progress

