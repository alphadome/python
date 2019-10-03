# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 17:45:32 2019

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

from weather_downloader import get_weather
from weather_tools import seasonal_patterns


#import sys
#for p in sys.path:
#    print(p)
#weather = get_weather("corn")
weather = get_weather(["Corsham","","","UK"])
precip_dict = weather[0]
temp_dict = weather[1]
for i in range(2009,2020):
    seasonal_patterns(precip_dict, temp_dict, i)


