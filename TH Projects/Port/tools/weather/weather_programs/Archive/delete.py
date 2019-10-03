# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 15:59:57 2019

@author: thoma
"""
import json

filename = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs\forecast_working_files\forecast_location.txt'
with open(filename) as f:
    local_dict = json.load(f)
    

count = 0
key_list = []
for key in local_dict.keys():
    count += 1
    if count < 10:
        key_list.append(key)
    else:
        break

for key in key_list:
    print(key, local_dict[key])


loc_fname = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\geo\cities500.txt'