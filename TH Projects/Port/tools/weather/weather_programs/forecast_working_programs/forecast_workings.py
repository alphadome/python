# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 15:14:18 2019

@author: thoma
"""
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


from weather_tools import text_between, coordinate_distance, find_lat_lon
from scraper import scraper
import json
from bs4 import BeautifulSoup
import time
from geolocation import geolocation

def process_list(url, name_list):
    print("starting process")
    soup = scraper(url)
    local_dict = {}
    links = soup.findAll("div", {"class": "info"})
    for link in links:
        local_list = []
        for item in name_list:
            local_list.append(item)
        if "https://www.accuweather.com/en/browse-locations" in str(link):
            href = text_between(str(link),'href="', '"><em>')
            name = text_between(str(link),'<em>', '</em>')
            local_list.append(name)
            local_dict[href] = local_list
        elif "/weather-forecast/" in str(link):
            href = text_between(str(link),'href="', '"><em>')
            name = text_between(str(link),'<em>', '</em>')
            local_list.append(name)
            local_dict[href] = local_list

    if local_dict == {}:
        print("Nothing found")
        Exception
    return local_dict

#active_list = [['World'], "https://www.accuweather.com/en/browse-locations"]
def create_dict(source_dict, end_dict):
    "Starting new dict"
    local_dict = {}
    for key, name_list in source_dict.items():
        url = key
        new_name = []
        for item in name_list:
            new_name.append(item)
        try:
            local_dict[url] = process_list(url, new_name)
            with open(str(end_dict)+'.txt', 'w') as f:
                json.dump(local_dict, f)
        except Exception:
         None  
    return local_dict

#continent_dict = process_list("https://www.accuweather.com/en/browse-locations", ['World'])

#with open('continent_dict.txt', 'w') as f:
#    json.dump(continent_dict, f)

#with open('continent_dict.txt') as f:
#    continent_dict = json.load(f)
#print(continent_dict)

#country_dict = create_dict(continent_dict, 'country_dict')

def state_dict():

    with open(r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs\forecast_working_files\country_dict.txt') as f:
        country_dict = json.load(f)
    print(country_dict)
    
    state_dict = {}
    for continent_key, dict_item in country_dict.items():
        local_dict = create_dict(dict_item, 'local_dict')
        for key, item in local_dict.items():
            state_dict[key] = item
        with open(r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs\forecast_working_files\state_dict.txt', 'w') as f:
            json.dump(state_dict, f)
    
def region_dict1():

    with open(r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs\forecast_working_files\state_dict.txt') as f:
        state_dict = json.load(f)
    
    region_dict = {}
    for country_key, dict_item in state_dict.items():
        local_dict = create_dict(dict_item, 'local_dict')
        for key, item in local_dict.items():
            region_dict[key] = item
        with open(r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs\forecast_working_files\region_dict.txt', 'w') as f:
            json.dump(region_dict, f)    

#region_dict()
#state_dict = create_dict(country_dict, 'state_dict')
#region_dict = create_dict(state_dict, 'region_dict')
#subregion_dict = create_dict(region_dict, 'subregion_dict')
def process_region_dict():
    region_dict_location = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs\forecast_working_files\region_dict.txt'
    with open(region_dict_location) as f:
        region_dict = json.load(f)
    
    processed_region_dict = {}
    
    count = 0
    for key, items in region_dict.items():
        for subkey, subitems in items.items():
            processed_region_dict[subkey] = subitems
    
    
    processed_region_dict_location = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs\forecast_working_files\processed_region_dict.txt'
    
    with open(processed_region_dict_location, 'w') as f:
        json.dump(processed_region_dict, f)

def sort_list():
    processed_region_dict_location = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs\forecast_working_files\processed_region_dict.txt'
    
    with open(processed_region_dict_location) as f:
        processed_region_dict = json.load(f)
        print(" dict loaded")
    
    region_dict = {}
    total_no = 0
    for key, items in processed_region_dict.items():
        region_dict[key] = items
        total_no += 1
        
    print("dict shortened")
    
    processed_forecast_location = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs\forecast_working_files\processed_forecast_location.txt'
    unfinished_locations = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs\forecast_working_files\unfinished_locations.txt'
    
    forecast_dict = {}
    unfinished_dict = {}
    
    count = 0
    for key, items in region_dict.items():
        print("new item")
        if 'weather-forecast' in str(key):
            print("doing the procedure: " + str(count) +"//" + str(total_no))
            location = ''
            for i in range(len(items)):
                location = location + str(items[len(items)-1 - i]) + ', '
            adj_location = location.replace(", World,",'')
            forecast_dict[key] = adj_location
        else:
            unfinished_dict[key] = items
        count = count + 1
    
    with open(processed_forecast_location, 'w') as f:
        json.dump(forecast_dict, f)
    
    with open(unfinished_locations, 'w') as f:
        json.dump(unfinished_dict, f)

    print("FORECAST-----------------")
    
    forecast_count = 0
    for key, items in forecast_dict.items():
        while forecast_count < 10:
            print(str(key) + str(": ") + str(items))
            forecast_count += 1
    print("UNFINISHED-----------------")
    unfinished_count = 0
    for key, items in unfinished_dict.items():
        while unfinished_count < 10:
            print(str(key) + str(": ") + str(items))
            unfinished_count += 1

filename = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\geo\cities500.txt'
citycode = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\geo\countrycode_processed.txt'

with open(filename, encoding="utf-8") as f:
    contents = f.readlines()

with open(citycode) as f:
    code_list = json.load(f)
        
def search_location(town, region, state, word_country):
    """input address Canary Wharf, London, UK etc"""
            
    for item in code_list:
        if word_country in item[2] or word_country in item[1]:
            country = item[0]
   
    country_pool = []
    count = 0
    for line in contents:
        new_line = line.split('\t')
        if str(country) == str(new_line[8]):
            country_pool.append(line)
            
    ranked_dict = {}
    ranking = []
    for subpool in country_pool:
        count = 0
        if str(town) in subpool and str(town) != '':
            count = count + 10
        if str(region) in subpool and str(region) != '':
            count = count + 5
        if str(state) in subpool and str(state) != '':
            count = count + 1
        ranked_dict[count] = subpool
        ranking.append(count)
        
    #print(ranked_dict)
    sorted_ranking = sorted(ranking)
    best_answer = ranked_dict[sorted_ranking[len(sorted_ranking)-1]]

    new_line = best_answer.split('\t')
    answer = []
    for i in [1,2,4,5,8,10,17,14]:
        answer.append(new_line[i])
  
    return [answer[2], answer[3], answer[0]]


def main():
    t0 = time.perf_counter()
    
    processed_forecast_location = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs\forecast_working_files\processed_forecast_location.txt'
    with open(processed_forecast_location) as f:
        processed_dict = json.load(f)
        print(" dict loaded")   
    
    local_dict = {}
    for key, items in processed_dict.items():
        local_dict[key] = items
    #print(local_dict)
    
    total_no = 0
    for key in local_dict.keys():
        total_no += 1
    
    done_no = 0
    location_dict = {}
    reject_dict = {}
    for key, items in local_dict.items():
        t2 = time.perf_counter()

        try:
            raw_address = items.split(",")
            address = []
            for location in raw_address:
                address.append(location.strip())
            print(address)
            
            country = address[len(address)-2]
            town = address[0]
            region = address[1]
            state = address[2]

            answer = geolocation(town, region, state, country) #[lat, lon, #of entries - above 1 bad]
            lat = answer[0]
            lon = answer[1]
        except Exception:
            lat = "Not found"
            lon = "Not found"
        
        if lat != "Not found":
            location_dict[key] = [lat, lon, items]
            print([lat, lon, items])
         
        else:
            reject_dict[key] = items          
            print('Not found')
        
        done_no += 1
        t1 = time.perf_counter()
        time_taken = t1 - t0
        time_prediction = ((time_taken) * (total_no / done_no) - t1)/3600
        print("On #" +str(done_no) + "/" + str(total_no) +" - estimated time to completion in hours is " +str(time_prediction) + "and the last opeation took " + str(t1 - t2))

    file1 = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs\forecast_working_files\forecast_location.txt'
    file2 = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs\forecast_working_files\reject_location.txt'
    
        
    with open(file1, 'w') as f:
        json.dump(location_dict, f)
    
    with open(file2, 'w') as f:
        json.dump(reject_dict, f)

main()        


    
