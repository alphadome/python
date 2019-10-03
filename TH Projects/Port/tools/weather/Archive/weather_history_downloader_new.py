# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 22:24:46 2019

@author: thoma
"""
from datetime import date, datetime, timedelta
import json
from math import sin, cos, sqrt, atan2, radians
from geopy.geocoders import Nominatim
import requests
from weather_tools import join_dicts
import urllib
from bs4 import BeautifulSoup
from selenium import webdriver


def weather_profile(address, name, data='', update=''):
    """Store a profile in the file so we do not repeat every action"""
    filename = (str(address) + "_weather_profile_history.txt")
    filename_temp = (str(address) + "_weather_profile_history_temp.txt")
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


def coordinate_distance_test():
    print(coordinate_distance("52.2296756", "21.0122287", "52.406374", "16.9251681"))
    print("Should be:", 278.546, "km")


def process_noaa_list():
    filename = "ghcnd-inventory.txt"
    
    station_list = []
    with open(filename) as f:
        contents = f.read()
    
    for i in range(round(len(contents)/46)):
        line = contents[i*46:i*46+46]
        station_code = str(contents[i*46:i*46+11])

        latitude = float(str(contents[i*46+11:i*46+20]).replace(" ",""))
        longitude = float(str(contents[i*46+20:i*46+30]).replace(" ",""))
        weather_type = str(str(contents[i*46+30:i*46+35]).replace(" ",""))[0] 
        start_date = float(str(contents[i*46+35:i*46+40]).replace(" ",""))    
        end_date = float(str(contents[i*46+40:i*46+46]).replace(" ",""))
#        if station_code == "USC00134101":
#            print(station_code, weather_type, start_date, end_date, date.today().year)
#            if float(end_date) > float(date.today().year) -1 and float(start_date) < float(date.today().year) -7:
#                print("confirm")
        if float(end_date) > float(date.today().year) -1 and float(start_date) < float(date.today().year) -7:
            if weather_type == "P" or weather_type == "T":
                station = []    
                station.append(station_code)
                station.append(latitude)
                station.append(longitude)
                station.append(weather_type)
                station.append(start_date)
                station.append(end_date)
                station_list.append(station)
#                if station_code == "USC00134101":
#                    print(station)
    
   
    new_filename = "ghcnd-inventory_processed.txt"
    with open(new_filename,'w') as f:
        json.dump(station_list, f)




def find_nearest_noaa_station(address, weather_type):
    geolocator = Nominatim(user_agent="my-application", timeout=30)
    location = geolocator.geocode(address)
    lat1 = location.latitude
    lon1 = location.longitude
    
    filename = "ghcnd-inventory_processed.txt"
    with open(filename) as f:
        station_list = json.load(f)
    adj_station_list = []
    for i in range(len(station_list)):
        if str(station_list[i][3]) == str(weather_type):
            adj_station_list.append(station_list[i])
        else:
            None
    
    if len(adj_station_list) == 0:
        print("weather type argument spelt wrong - P or T")

    distance_dict = {}
    for i in range(len(adj_station_list)):
        station = adj_station_list[i]
        station_code = station[0]
        lat2 = station[1]
        lon2 = station[2]
        key = coordinate_distance(lat1,lon1,lat2,lon2)
        distance_dict[key] = station_code
    
    sorted_locations = []
    for key in distance_dict.keys():
        sorted_locations.append(float(key))
    sorted_locations = sorted(sorted_locations)
    
    eligible_dict = {}
    for key in sorted_locations[:10]:
        eligible_dict[key] = distance_dict[key]
    
    return eligible_dict


def get_ecad_list():
    url = "https://www.ecad.eu//download/ECA_blend_source_tg.txt"
    r = requests.get(url)

    new_filename = "ecad_station_list.txt"
    with open(new_filename,'w') as f:
        json.dump(r.text, f)


def process_ecad_list():
    filename = "ecad_station_list.txt"
    with open(filename) as f:
        contents = json.load(f)
    
    if contents[1179:1186] == "PARNAME":
        None
    else:
        print("Reanalyse where the data starts in process_ecad_list")
    
    #print(contents[:1192])
    station_list = []
    #print(str(contents[0:1186]))
    data_list = contents[1186:len(contents)].replace(" ","").split('\r\n')
    data = []
    
    for item in data_list:
        line = item.split(',')
        data.append(line)
    
    for i in range(len(data)):
        try:
            line = data[i]
            station_code = line[0]
            location_name = line[2]
            country_code = line[3]
            lat_raw = str(line[4])
            lon_raw = str(line[5])
            weather_type = line[7]
            weather_type = weather_type[0] #keep first letter as there are many subcategories
            #https://www.ecad.eu//dailydata/datadictionaryelement.php for weather type
            start_date_raw = line[8]
            end_date_raw = line[9]
            
            lat_list = lat_raw[0:len(lat_raw)].split(':')
            lat = float(lat_list[0]) + float(lat_list[1])/60 + float(lat_list[2])/3600
    
            lon_list = lon_raw[0:len(lon_raw)].split(':')
            lon = float(lon_list[0]) + float(lon_list[1])/60 + float(lon_list[2])/3600
            
            start_date = float(start_date_raw[:4])
            end_date = float(end_date_raw[:4])
            station = [station_code, location_name, country_code, lat, lon, weather_type, start_date, end_date]
            year = date.today().year
            if float(end_date) > float(year-1) and float(start_date) < float(year-7):
                #print(station)
                station_list.append(station)

        except Exception:
            None

    new_filename = "ecad_inventory_processed.txt"
    with open(new_filename,'w') as f:
        json.dump(station_list, f)

def find_nearest_ecad_station(address, weather_type):
    geolocator = Nominatim(user_agent="my-application", timeout=30)
    location = geolocator.geocode(address)
    lat1 = location.latitude
    lon1 = location.longitude
    
    filename = "ecad_inventory_processed.txt"
    with open(filename) as f:
        station_list = json.load(f)
    
    adj_station_list = []
    for i in range(len(station_list)):
        if str(station_list[i][5]) == str(weather_type):
            adj_station_list.append(station_list[i])
        else:
            None
    if len(adj_station_list) == 0:
        print("weather type argument spelt wrong - T or R")

    distance_dict = {}
    for i in range(len(adj_station_list)):
        station = adj_station_list[i]
        station_code = station[0]
        location_name = station[1]
        lat2 = station[3]
        lon2 = station[4]
        key = coordinate_distance(lat1,lon1,lat2,lon2)
        distance_dict[key] = [station_code, location_name]
    
    sorted_locations = []
    for key in distance_dict.keys():
        sorted_locations.append(float(key))
    sorted_locations = sorted(sorted_locations)
    
    eligible_dict = {}
    for key in sorted_locations[:30]:
        eligible_dict[key] = distance_dict[key]
    
    return eligible_dict   



def analyse_contents(url):
    
    try:
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        
        contents = list(soup.children)
        #contents are a big text file with \ns
        content_list = list(contents[0].split('\n'))
        #content_list: every line of contents is a member of this list
        
        date_list = []
        
        for line in content_list:
            # turn the lines in the content_list into useable form
            content_list_linelist = list(line.split(' ', -1))
            #contents>
            #content_list: contents are now a list>
            #content_list_line: line in the content list>
            #content_list_line_item: item in the content list line
            for content_list_line_item in content_list_linelist:
                if content_list_line_item == '':
                    content_list_linelist.remove(content_list_line_item)
                elif content_list_line_item == ' ':
                    content_list_linelist.remove(content_list_line_item)
   
            for content_list_line_item in content_list_linelist:
                try:
                    if float(content_list_line_item) == '':
                        content_list_linelist.remove(content_list_line_item)
                        date_list.append(content_list_linelist)
                except ValueError:
                    break
                else:
                    date_list.append(content_list_linelist)
        
        final_dict = {}
        for item in date_list:
            year = item[0]
            month = item[1]
            day = item[2]
            item_date = str(date(int(year), int(month), int(day)))
            item_value = item[len(item)-1]
            
            if item_date not in final_dict.keys():
                final_dict[item_date] = item_value
            
        return final_dict
    
    #needs an error in case there is a wrong url        
    except urllib.error.HTTPError as err:
        print(str(url) + " "+str(err)+" error in analyzing contents - wrong webpage")


def update_stations():
    """only do this occasionally"""
    process_noaa_list()
    #ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/
    get_ecad_list()
    process_ecad_list()

def find_nearest_station(address, weather_type):
    """returns station code and best location"""
    if weather_type == "T":
        noaa_dict = find_nearest_noaa_station(address, weather_type)
        ecad_dict_raw = find_nearest_ecad_station(address, weather_type) 
        
        ecad_dict = {}
        for key, item in ecad_dict_raw.items():
            ecad_dict[key] = str(item[0])
        
        total_dict = join_dicts(noaa_dict, ecad_dict)
        location_list = []
        for key in total_dict.keys():
            location_list.append(key)
        location_list = sorted(location_list)
        
        best_location = location_list[0]

        try:
            code = noaa_dict[best_location]
            database = "NOAA"
        
        except Exception:
            code = ecad_dict[best_location]
            database = "ECAD"

        
    elif weather_type =="P":
        noaa_dict = find_nearest_noaa_station(address, weather_type)
        ecad_dict_raw = find_nearest_ecad_station(address, "T")
        
        ecad_dict = {}
        for key, item in ecad_dict_raw.items():
            url = "http://climexp.knmi.nl/data/bpeca" + str(item[0]) +".dat"
            try:
                r = requests.get(url)
                if r.status_code == "200":
                    ecad_dict[key] = str(item[0])
            except Exception:
                None
            
        
        total_dict = join_dicts(noaa_dict, ecad_dict)
        location_list = []
        for key in total_dict.keys():
            location_list.append(key)
        location_list = sorted(location_list)
        
        best_location = location_list[0]

        try:
            code = noaa_dict[best_location]
            database = "NOAA"
        
        except Exception:
            code = ecad_dict[best_location]
            database = "ECAD"

    else:
        print("Review weather_type specified")         

    
    return [code, best_location, database]

print(find_nearest_station("London","T"))


def get_weather_data_url_precip(address,update=''):
    """returns weather url of the input address"""
    #Check profile to see if we have already
   
    def proceed_with_method():
        station = find_nearest_station(address, "P")
        station_code = station[0] 
        station_distance = station[1]
        database = station[2]
                
        if database == "NOAA":
            weather_station_url = "http://climexp.knmi.nl/data/pgdcn" + str(station_code) + ".dat"
        
        elif database == "ECAD":
            weather_station_url = "http://climexp.knmi.nl/data/bpeca" + str(station_code) + ".dat"
        
        return [str(weather_station_url), float(station_distance)]
    
    title = "get_weather_data_url_precip"
    if weather_profile(address, title) == None or update != '':
        print("/t-Adding/refreshing data...")
        data = proceed_with_method()
        weather_profile(address, title, data)
        return weather_profile(address, title)

    else:
        return weather_profile(address, title)

def get_weather_data_precip(address, update=''):
    
    def proceed_with_method():
        url = get_weather_data_url_precip(address)[0]
        final_dict = analyse_contents(url)
        return final_dict

    title = "get_weather_data_precip"
    if weather_profile(address, title) == None or update != '':
        print("/t-Adding/refreshing data...")
        data = proceed_with_method()
        weather_profile(address, title, data)
        return weather_profile(address, title)

    else:
        return weather_profile(address, title)

def get_weather_data_url_temp(address,update=''):
    """returns weather url of the input address"""
    #Check profile to see if we have already
   
    def proceed_with_method():
        station = find_nearest_station(address, "T")
        station_code = station[0] 
        station_distance = station[1]
        database = station[2]
                
        if database == "NOAA":
            url_avg = "http://climexp.knmi.nl/data/vgdcn" + str(station_code) + ".dat"
            url_max = "http://climexp.knmi.nl/data/xgdcn" + str(station_code) + ".dat"
            url_min = "http://climexp.knmi.nl/data/ngdcn" + str(station_code) + ".dat"
            
            urls = [ url_max, url_min, url_avg]
            for url in urls:
                r = requests.get(url)
                if r.status_code == 200:
                    weather_station_url = url
                else:
                    None
        
        elif database == "ECAD":
            weather_station_url = "http://climexp.knmi.nl/data/bteca" + str(station_code) + ".dat"
        
        return [str(weather_station_url), float(station_distance)]
    
    title = "get_weather_data_url_temp"
    if weather_profile(address, title) == None or update != '':
        print("/t-Adding/refreshing data...")
        data = proceed_with_method()
        weather_profile(address, title, data)
        return weather_profile(address, title)
    else:
        return weather_profile(address, title)

def get_weather_data_temp(address, update=''):
    
    def proceed_with_method():
        url = get_weather_data_url_temp(address)
        final_dict = analyse_contents(url)
        return final_dict

    title = "get_weather_data_temp"
    if weather_profile(address, title) == None or update != '':
        print("/t-Adding/refreshing data...")
        data = proceed_with_method()
        weather_profile(address, title, data)
        return weather_profile(address, title)

    else:
        return weather_profile(address, title)        

#get_weather_data_precip("London",'update')
#get_weather_data_temp("London",'update')
get_weather_data_url_precip("London",'update')
#get_weather_data_url_temp("London",'update')
   
