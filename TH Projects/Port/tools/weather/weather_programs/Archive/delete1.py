# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 17:20:02 2019

@author: thoma
"""
import json

filename = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_profile_inventory.txt'

location_list = [['','','Colorado','US'], ['','','Illinois','US'], ['','','Indiana','US'], ['','','Iowa','US'], ['','','Kansas','US'], ['','','Kentucky','US'], ['','','Michigan','US'], ['','','Minnesota','US'], ['','','Missouri','US'], ['','','Nebraska','US'], ['','','North Carolina','US'], ['','','North Dakota','US'], ['','','Ohio','US'], ['','','Pennsylvania','US'], ['','','South Dakota','US'], ['','','Texas','US'], ['','','Wisconsin','US'], ['','','London','UK'], ['','Los Angeles','','UK']]


with open(filename, 'w') as f:
    json.dump(location_list,f)



with open(filename) as f:
    locations = json.load(f)

print(locations)

foldername = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\\'
fname = foldername + str(locations[0]) + '.txt'
with open(fname, 'w') as f:
    json.dump('done',f)