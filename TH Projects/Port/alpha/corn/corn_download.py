# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 15:29:41 2019

@author: thoma
"""
import sys
import_list = [
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools",
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\general\scraper",
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs"        

        ]
for import_location in import_list:
    if import_location not in sys.path:
        sys.path.append(import_location)

file_name =  r"C:\Users\thoma\Desktop\Python\TH Projects\Port\alpha\corn\corn_prod_us_state.xlsx"
sheet =  'us_state'
import json
import time
from weather_tools import somonth
from datetime import date, datetime, timedelta
from weather_downloader import get_weather
from weather_tools import seasonal_patterns
from weather_forecast_downloader import get_weather_forecast




import pandas as pd
df = pd.read_excel(io=file_name, sheet_name=sheet)
#print(df.head(15))  # print first 5 rows of the dataframe

# Reading an excel file using Python 
import xlrd 
  
# Give the location of the file 
def get_from_xls():
    loc = (r"C:\Users\thoma\Desktop\Python\TH Projects\Port\alpha\corn\corn_prod_us_state.xlsx") 
      
    # To open Workbook 
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0) 
      
    for i in range(sheet.ncols): 
        if sheet.cell_value(1, i) == 'Pct 2018':
            col_pct = i
    
    for i in range(sheet.ncols): 
        if sheet.cell_value(1, i) == 'URLS':
            col_url = i
    
    corn_dict = {}
    url_list = []
    for i in range(sheet.nrows): 
        state = sheet.cell_value(i, 0)
        pct = sheet.cell_value(i, col_pct)
        url = sheet.cell_value(i, col_url)
        try:
            no = "{0:.1%}".format(float(pct))
        except Exception:
            no = '100.0%'
        try:
            if no != '100.0%':
                corn_dict[state] = [no, url]
        except Exception:
            None
        if url != '' and url != 'URLS':
            url_list.append(url)
    
    
    filename = (r"C:\Users\thoma\Desktop\Python\TH Projects\Port\alpha\corn\corn_dict.txt") 
    with open(filename, 'w') as f:
        json.dump(corn_dict, f)
    
    return url_list

def corn_links(url_list):
    
    complete_url_list = []
    for url_stem in url_list:
        url_stem = str(url_stem).replace("weather-forecast", "july-weather")
        url_base = url_stem
        
        today = date.today()
        date_last = somonth(today.year, today.month - 1)
        date_current = somonth(today.year, today.month)
        date_next = somonth(today.year, today.month+1)
    
        url_last = str(str(url_base) +"?monyr="+str(date_last.month)+"/1/"+str(date_last.year)+"&view=table")
        url_current = str(str(url_base)+"?monyr="+str(date_current.month)+"/1/"+str(date_current.year)+"&view=table")
        url_next = str(str(url_base) +"?monyr="+str(date_next.month)+"/1/"+str(date_next.year)+"&view=table")
    
        urls = [url_current, url_last, url_next]
        for url in urls:
            complete_url_list.append(url)
    
    filename1 = (r"C:\Users\thoma\Desktop\Python\TH Projects\Port\alpha\corn\corn_download_list.txt") 
    
    with open(filename1, 'w') as f:
        json.dump(complete_url_list, f)
    
    print(len(complete_url_list))    
    return complete_url_list
corn_links(get_from_xls())

def alter_weather_profiles():
    filename = (r"C:\Users\thoma\Desktop\Python\TH Projects\Port\alpha\corn\corn_dict.txt") 
    with open(filename) as f:
        corn_dict = json.load(f)
    
    #print(corn_dict)
    
    
    name = "weather_forecast_url"
    for key, items in corn_dict.items():
        if items[1] != '':
            state_dict = {}
            filename = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_profiles\\' + str(key.strip()) +"_weather_profile_forecast.txt"
            url = items[1]
            state_dict[name] = url
            with open(filename, 'w') as f:
                json.dump(state_dict, f)

def get_forecasts():
    filename = (r"C:\Users\thoma\Desktop\Python\TH Projects\Port\alpha\corn\corn_dict.txt") 
    with open(filename) as f:
        corn_dict = json.load(f)    
    
    for key, items in corn_dict.items():
        if items[1] != '':
            get_weather_forecast(key.strip())


def main():
    filename = (r"C:\Users\thoma\Desktop\Python\TH Projects\Port\alpha\corn\corn_dict.txt") 
    with open(filename) as f:
        corn_dict = json.load(f)
    
    print(corn_dict)
    
    corn_weather_dict = {}

    total_pct = 0
    weather_dict_temp = {}
    weather_dict_precip = {}

    for key, items in corn_dict.items():
        try:
            weather_dict_temp = corn_weather_dict["weather_dict_temp"]
            weather_dict_precip = corn_weather_dict["weather_dict_precip"]
        except Exception:
            None
        
        url = items[1]
        if url != '':
            state = key.strip()
            print(state)
            pct = float(items[0].strip('%'))
            weather = get_weather(state)
            precip_dict = weather[0]
            temp_dict = weather[1]
            total_pct = float(total_pct) + float(pct)
            for key1, data in precip_dict.items():
                if key1 in weather_dict_precip.keys():
                    weather_dict_precip[key1] = pct * precip_dict[key1] + weather_dict_precip[key1]
                if key1 not in weather_dict_precip.keys():
                    weather_dict_precip[key1] = pct * precip_dict[key1]
                
                    
            for key1, data in temp_dict.items():
                if key1 in weather_dict_temp.keys():
                    weather_dict_temp[key1] = pct * temp_dict[key1] + weather_dict_temp[key1]
                if key1 not in weather_dict_temp.keys():
                    weather_dict_temp[key1] = pct * temp_dict[key1]
                    
                            
            corn_weather_dict["weather_dict_temp"] = weather_dict_temp
            corn_weather_dict["weather_dict_precip"] = weather_dict_precip
    
    
    weather_dict_temp = corn_weather_dict["weather_dict_temp"]
    weather_dict_precip = corn_weather_dict["weather_dict_precip"]    

    precip_keys = []
    temp_keys = []
    count = 0
    for key, items in corn_dict.items():
        url = items[1]
        if url != '':
            state = key.strip()
            print(state)
            weather = get_weather(state)
            precip_dict = weather[0]
            temp_dict = weather[1]
            
            for subkey in precip_dict.keys():
                if count < 1:
                    precip_keys.append(subkey)
            
            for subkey in temp_dict.keys():
                if count < 1:
                    temp_keys.append(subkey)        
    
            for subkey in precip_keys:
                formattedas_date = datetime.strptime(subkey, "%Y-%m-%d")
                if subkey not in precip_dict.keys() and int(formattedas_date.year) != int(date.today().year):
                    precip_keys.remove(subkey)
                
            for subkey in temp_keys:
                formattedas_date = datetime.strptime(subkey, "%Y-%m-%d")
                if subkey not in temp_dict.keys() and int(formattedas_date.year) != int(date.today().year):
                    temp_keys.remove(subkey)
            
            count += 1


    date_adj_weather_dict_temp = {}
    date_adj_weather_dict_precip = {}
    for key, items in weather_dict_temp.items():
        if key in temp_keys:
            date_adj_weather_dict_temp[key] = items / total_pct

            
    for key, items in weather_dict_precip.items():
        if key in temp_keys:
            date_adj_weather_dict_precip[key] = items / total_pct

        
    corn_weather_dict["weather_dict_temp"] = date_adj_weather_dict_temp
    corn_weather_dict["weather_dict_precip"] = date_adj_weather_dict_precip
    
    filename_c = r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_profiles\corn_weather_profile.txt"
    with open(filename_c, 'w') as f:
        json.dump(corn_weather_dict, f)


main()
