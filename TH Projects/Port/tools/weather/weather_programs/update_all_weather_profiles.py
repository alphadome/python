# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 14:47:17 2019

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
from datetime import date, datetime
from weather_tools import somonth, text_between
from bulk_scrape import bulk_scraper
from weather_forecast_downloader import get_weather_forecast, find_closest_forecast_location
from weather_history_downloader import historic_weather_data
from weather_downloader import get_weather
import os
import json
from time_restriction import time_restricted_0_var

def get_locations_in_weather_profiles():
    path = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_profiles'
    
    files = []
    locations = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if 'weather_profile_forecast.txt' in file:
                files.append(os.path.join(r, file))
                locations.append(text_between(str(os.path.join(r, file)), 'weather_profiles\\', '_weather_profile_forecast.txt'))
    print(locations)

def user_input():
    def ask():
        answer = input("Update all / just forecast / just history? (a/f/h):  ")
        return answer.strip()

    while True:
        answer = ask()
        if answer == 'a':
            print("Updating all")
            break            
        elif answer == 'h':
            print("Only updating history")
            break
        elif answer == 'f':
            print("Only updating forecasts")
            break
        else:
            print("Please use (a/f/h) to answer the question.")
    return answer

#if name == main needs to encapsulate time_restricted and bulk scrape, i.e. all multiprocesses
if __name__ == '__main__':
    
    #this is a swtich so if user input is a it will update everything and if not default is forecasts
    job = str(time_restricted_0_var(2, user_input))
    print(job)
    if job == 'a':
        switch = 'a'
        print("Updating all")
    elif job == 'h':
        switch = 'h'
        print("Only updating history")
    else:
        switch = 'f'
        print("Only updating forecasts")
    
    filename = r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_profile_inventory.txt"
    with open(filename) as f:
        locations = json.load(f)
        print("Weather profile inventory loaded...")
    
    if switch != 'h':
        #then switch is update all or update forecast
        url_base_list = []
        for location in locations:
            url = find_closest_forecast_location(location)
            url_base_list.append(url)
            print(location, ': ', url)
        
        url_list = []
        basedate = datetime.now()
        basemonth = basedate.strftime("%B").lower()
        
        today = date.today()
        date_last1 = somonth(today.year, today.month - 2)
        date_last = somonth(today.year, today.month - 1)
        date_current = somonth(today.year, today.month)
        date_next = somonth(today.year, today.month+1)
        
        for url_stem in url_base_list:
            url_base = str(url_stem).replace("weather-forecast", str(basemonth) + "-weather")
            url_last1 = str(str(url_base) +"?monyr="+str(date_last1.month)+"/1/"+str(date_last1.year)+"&view=table")
            url_last = str(str(url_base) +"?monyr="+str(date_last.month)+"/1/"+str(date_last.year)+"&view=table")
            url_current = str(str(url_base)+"?monyr="+str(date_current.month)+"/1/"+str(date_current.year)+"&view=table")
            url_next = str(str(url_base) +"?monyr="+str(date_next.month)+"/1/"+str(date_next.year)+"&view=table")
        
            generated_urls = [url_current, url_last, url_next, url_last1] #will give priority to first in this list
            for url in generated_urls:
                url_list.append(url)
        
        bulk_scraper(url_list)
    
    for location in locations:
        print(location)
        #print('updating weather forecasts')
        #get_weather_forecast(location,"update")
        #print('updating weather temp historic')
        #historic_weather_data(location, "T", 'update')    
        #print('updating weather precip historic')
        #historic_weather_data(location, "P", 'update')
        if switch == 'a':
            get_weather(location, 'update')
        elif switch == 'h':
            get_weather(location, 'history')
        else:
            get_weather(location, 'forecast')
        