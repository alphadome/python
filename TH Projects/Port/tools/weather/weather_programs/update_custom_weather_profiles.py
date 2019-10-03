# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 20:17:28 2019

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

import json
from weather_downloader import get_weather
from datetime import date, datetime, timedelta
import os


path = r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_custom_profile_mix\\"
destination_path = r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_profiles\\"
files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.txt' in file:
            files.append(os.path.join(r, file))

#for f in files:
    #print(f)
    #print(str(f).replace(path,''))
    #actual_name = str(f).replace(path,'')    
    #filename_mix = destination_path + str(actual_name).replace('.txt', '_weather_profile.txt')
    #print(filename_mix)
    
def main(filename):
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
        
        state = str(key)
        print(state)
        pct = float(items.strip('%'))/100
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
        state = str(key)
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
            date_adj_weather_dict_temp[key] = float("{0:.2f}".format(items / total_pct))
    
            
    for key, items in weather_dict_precip.items():
        if key in temp_keys:
            date_adj_weather_dict_precip[key] = float("{0:.2f}".format(items / total_pct))
    
        
    corn_weather_dict["weather_dict_temp"] = date_adj_weather_dict_temp
    corn_weather_dict["weather_dict_precip"] = date_adj_weather_dict_precip

    actual_name = str(filename).replace(path,'')    
    filename_mix = (destination_path + str(actual_name).replace('.txt', '_weather_profile.txt'))
    with open(filename_mix, 'w') as f:
        json.dump(corn_weather_dict, f)

if __name__ == '__main__':
    for filename in files:
        print("calculating custom weather for...")
        print(filename)
        main(filename)