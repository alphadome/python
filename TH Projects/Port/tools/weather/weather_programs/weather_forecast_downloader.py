# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 14:44:31 2019

@author: thoma
"""


#import importlib.util
#spec = importlib.util.spec_from_file_location("scraper", r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\general_programs\scraper\scraper.py")
#foo = importlib.util.module_from_spec(spec)
#spec.loader.exec_module(foo)
#scraper = foo.scraper
import sys
import_list = [
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools",
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\general\scraper",
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs",        
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\geo"
        ]
for import_location in import_list:
    if import_location not in sys.path:
        sys.path.append(import_location)

from scraper import scraper
from time_restriction import time_restricted
from weather_tools import somonth, join_dicts, text_between, coordinate_distance, find_lat_lon

import json
import statistics
from datetime import date, datetime, timedelta
import re
from geolocation import geolocation

def weather_profile(address, name, data='', update=''):
    """Store a profile in the file so we do not repeat every action"""
    filename = str(r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_profiles/" + str(address) + "_weather_profile_forecast.txt")
    filename_temp = str(r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_profiles/" + str(address) + "_weather_profile_forecast_backup.txt")


    #open as write - this takes care of the initial instance of the file
    # if we can read the profile read it, otherwise create an empty dict

    try:
        with open(filename) as f:
            contents = json.load(f)
        
        weather_profile_dict = contents
        
        #create backup file in case something goes wrong
        with open(filename_temp, 'w') as f:
            contents = weather_profile_dict
            json.dump(weather_profile_dict, f)

    except FileNotFoundError:
        weather_profile_dict = {}

    except ValueError:
        print("dictionary has a value error")
        weather_profile_dict = {}
             
    # if there is an existing entry:     
    if name in weather_profile_dict.keys():
        if update:
            del weather_profile_dict[name]
            weather_profile_dict[name] = data
            # store the amended profile          
            with open(filename, 'w') as f:
                json.dump(weather_profile_dict,f)
            return weather_profile_dict[name]
        else:
            return weather_profile_dict[name]
    
    # if there isn't an existing entry
    else:
        if data:
            # create a new one if there is data
            weather_profile_dict[name] = data
            # store the amended profile          
            with open(filename, 'w') as f:
                json.dump(weather_profile_dict,f)
            return weather_profile_dict[name]

        else:
            # return nothing if there isn't
            print("t/-There is no existing data for " + str(name) + " - add data...")
            return None


def find_closest_forecast_location(address):
    """address in format['location', 'area', 'state', 'country'], returns closes weather URL"""

    address_location = geolocation(address)
    ############CHANGE OUT OF ARCHIVE WHEN COMPLETE##########
    filename = r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs\forecast_working_files\Archive\forecast_location.txt"
    
    with open(filename) as f:
        forecast_location_dict = json.load(f)
    
    distance_list = []
    url_list = []
    for key, items in forecast_location_dict.items():
        forecast_lat = items[0]
        forecast_lon = items[1]
        distance = coordinate_distance(address_location[0], address_location[1], forecast_lat, forecast_lon)
        distance_list.append(distance)
        url_list.append([distance, key, items])
    
    ranked_list = sorted(distance_list)
    best_ranking = ranked_list[0]
    
    answer_url = []
    for url_entry in url_list:
        if url_entry[0] == best_ranking:
            answer_url.append(url_entry)
    
    print("Found these urls and using the first entry: " + str(answer_url))
    return answer_url[0][1]

#print(find_closest_forecast_location(['', '', 'London', 'UK']))
   

def download_forecast(url):
    soup = scraper(url)
    #soup = BeautifulSoup(str(contents))


    before = soup.findAll("tr", {"class":"pre"})
    after = soup.findAll("tr", {"class":"lo calendar-list-cl-tr cl hv"})
    
    forecast_dict = {}
    
    for div in before:
        raw_div = str(div).replace('<td>','').replace('</td>','')
        raw_div = str(raw_div).split("\n")

        try:
            date_nos = re.findall(r'-?\d+\/\d+', str(raw_div[1]))
            raw_date = str(date_nos[0])
            raw_date_list = raw_date.split("/")
            today = date.today()
            year = today.year
            month = raw_date_list[0]
            day = raw_date_list[1]
            weather_date = str(date(int(year), int(month), int(day)))

        
            temp_list = raw_div[2].replace("°",'').split("/")
            temp_list_adj= []
            for temp in temp_list:
                temp_list_adj.append(float(temp))
            
            temp = statistics.mean(temp_list_adj)
            
            precip_nos = re.findall(r'-?\d+', raw_div[3])
            precip = float(precip_nos[0])
            
            forecast_dict[weather_date] = [temp, precip]
        
        except Exception:
            None
            
    for div in after:
        raw_div = str(div).replace('<td>','').replace('</td>','')
        raw_div = str(raw_div).split("\n")

        try:
            date_nos = re.findall(r'-?\d+\/\d+', str(raw_div[1]))
            raw_date = str(date_nos[0])
            raw_date_list = raw_date.split("/")
            today = date.today()
            year = today.year
            month = raw_date_list[0]
            day = raw_date_list[1]
            weather_date = str(date(int(year), int(month), int(day)))

        
            temp_list = raw_div[2].replace("°",'').split("/")
            temp_list_adj= []
            for temp in temp_list:
                temp_list_adj.append(float(temp))
            
            temp = statistics.mean(temp_list_adj)
            
            precip_nos = re.findall(r'-?\d+', raw_div[3])
            precip = float(precip_nos[0])
            
            forecast_dict[weather_date] = [temp, precip]
        
        except Exception:
            None
    
    return forecast_dict
#"https://www.accuweather.com/en/us/iowa-city-ia/52240/weather-forecast/328802"
##https://www.accuweather.com/en/us/iowa-city-ia/52240/august-weather/328802?monyr=7/1/2019&view=table
#print(download_forecast("https://www.accuweather.com/en/us/iowa-city-ia/52240/january-weather/328802?monyr=8/1/2019&view=table"))
#https://www.accuweather.com/en/us/iowa-city-ia/52240/weather-forecast/328802
#https://www.accuweather.com/en/gb/london/ec4a-2/weather-forecast/328328
#https://www.accuweather.com/en/gb/london/ec4a-2/month/328328?monyr=8/01/2019
#https://www.accuweather.com/en/gb/london/ec4a-2/august-weather/328328?monyr=8/1/2019
#https://www.accuweather.com/en/us/iowa-city-ia/52240/august-weather/328802?monyr=7/1/2019&view=table

#print(download_forecast("https://www.accuweather.com/en/gb/london/ec4a-2/january-weather/328328?monyr=7/1/2019&view=table"))
def get_weather_forecast(address, update=''):
    """input address, output forecast weather_dict"""
    
    def method_url():
        url_base = find_closest_forecast_location(address)
        return url_base
    
    def method_dict():
        basedate = datetime.now()
        basemonth = basedate.strftime("%B").lower()
        
        url_stem = weather_profile(address, "weather_forecast_url")
        url_stem = str(url_stem).replace("weather-forecast", str(basemonth) + "-weather")
        url_base = url_stem
        
        today = date.today()
        date_last1 = somonth(today.year, today.month - 2)
        date_last = somonth(today.year, today.month - 1)
        date_current = somonth(today.year, today.month)
        date_next = somonth(today.year, today.month+1)

        url_last1 = str(str(url_base) +"?monyr="+str(date_last1.month)+"/1/"+str(date_last1.year)+"&view=table")
        url_last = str(str(url_base) +"?monyr="+str(date_last.month)+"/1/"+str(date_last.year)+"&view=table")
        url_current = str(str(url_base)+"?monyr="+str(date_current.month)+"/1/"+str(date_current.year)+"&view=table")
        url_next = str(str(url_base) +"?monyr="+str(date_next.month)+"/1/"+str(date_next.year)+"&view=table")
        
        url_list = [url_current, url_last, url_next, url_last1] #will give priority to first in this list
        #print(url_list)
        combined_dict = {}
        
        for url in url_list:
            forecast_dict = download_forecast(url)
            print(str(url) + " downloaded")
            combined_dict = join_dicts(combined_dict, forecast_dict)
            weather_profile(address, "weather_forecast_dict", combined_dict, update)
            print(str(url) + " added")
            print(combined_dict)
        
        return combined_dict
    
    title = "weather_forecast_url"
    if weather_profile(address, title) == None:
        print("/t-Adding/refreshing data...")
        data = method_url()
        print(data)
        weather_profile(address, title, data, update)
    else:
        print("There is existing data for: " + str(title))


    title = "weather_forecast_dict"
    if weather_profile(address, title) == None or update != '':
        print("/t-Adding/refreshing data...")
        data = method_dict()
        print(data)
        weather_profile(address, title, data, update)
        return weather_profile(address, title)
    else:
        return weather_profile(address, title)


#get_weather_forecast(['', '', 'Colorado', 'US'],"update")




