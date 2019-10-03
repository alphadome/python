# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 10:34:40 2019

@author: thoma
"""
import sys
import_list = [
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools",
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\general\scraper",
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs",
        r"C:\Users\thoma\AppData\Local\Programs\Python\Python37-32\Lib\site-packages"        
        ]
for import_location in import_list:
    if import_location not in sys.path:
        sys.path.append(import_location)
import json
import statistics
from fuzzywuzzy import fuzz




cities500 = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\geo\cities500.txt'
admincode1 = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\geo\admincode1.txt'
admincode2 = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\geo\admincode2.txt'
cities500_processed = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\geo\cities500_processed.txt'
admincode1_processed = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\geo\admincode1_processed.txt'
admincode2_processed = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\geo\admincode2_processed.txt'
countrycode_processed = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\geo\countrycode_processed.txt'

def geolocation(address):
    """input address = [location, area, state, country], requires a country, returns [lat,lon]"""
    location = address[0]
    area = address[1]
    state = address[2]
    country = address[3]
    
    
    def country_search(country):
        if country != '':
            with open(countrycode_processed) as f:
                local_list = json.load(f)
            
            code_list, abbrv_list, name_list = [], [], []
            for i in range(len(local_list)):
                code_list.append(local_list[i][0])
                abbrv_list.append(local_list[i][1])
                name_list.append(local_list[i][2])
            
            adj_country_list = []
            for i in range(len(local_list)):
                if country in str(code_list[i]) or country in str(abbrv_list[i]) or country in str(name_list[i]):
                    if code_list[i] not in adj_country_list:
                        adj_country_list.append(code_list[i])
            
            if len(adj_country_list) > 1:
                fuzz_list = []
                for i in range(len(local_list)):
                    if country in str(code_list[i]) or country in str(abbrv_list[i]) or country in str(name_list[i]):
                        #print(name_list[i], code_list[i])
                        name_fuzz = fuzz.ratio(str(country), str(name_list[i]))
                        abbrv_fuzz = fuzz.ratio(country, abbrv_list[i])
                        code_fuzz = fuzz.ratio(country, code_list[i])
                        #print(name_fuzz, abbrv_fuzz, code_fuzz)
                        fuzz_max = max([name_fuzz, abbrv_fuzz, code_fuzz])
                        fuzz_list.append(fuzz_max)
                
                best_match = []
                for i in range(len(fuzz_list)):
                    if fuzz_list[i] == max(fuzz_list):
                        best_match.append(adj_country_list[i])
                
                adj_country_list = best_match
    
        else:
            adj_country_list = ['']
        
        #print(adj_country_list)
        return adj_country_list
    
    def state_search(state):
        if state != '':
            with open(admincode1_processed) as f:
                local_list = json.load(f)
            
            code_list, name_list1, name_list2 = [], [], []
            for i in range(len(local_list)):
                code_list.append(local_list[i][0])
                name_list1.append(local_list[i][1])
                name_list2.append(local_list[i][2])
            
            adj_state_list = []
            for i in range(len(local_list)):
                if state in str(code_list[i]) or state in str(name_list1[i]) or state in str(name_list2[i]):
                    if code_list[i] not in adj_state_list:
                        adj_state_list.append(code_list[i])
        else:
            adj_state_list = ['']
            
        #print(adj_state_list)
        return adj_state_list    
    
    def area_search(area):
        if area != '':
            with open(admincode2_processed) as f:
                local_list = json.load(f)
            
            code_list, name_list1, name_list2 = [], [], []
            for i in range(len(local_list)):
                code_list.append(local_list[i][0])
                name_list1.append(local_list[i][1])
                name_list2.append(local_list[i][2])
            
            adj_area_list = []
            for i in range(len(local_list)):
                if area in str(code_list[i]) or area in str(name_list1[i]) or area in str(name_list2[i]):
                    if code_list[i] not in adj_area_list:
                        adj_area_list.append(code_list[i])
        else:
            adj_area_list = ['']
            
        #print(adj_area_list)
        return adj_area_list   

    def location_search(location):
        if location != '':
            with open(cities500_processed) as f:
                local_list = json.load(f)
            
            possible_list = []
            for i in range(len(local_list)):
                if location in str(local_list[i][1]) or location in str(local_list[i][3]) or location in str(local_list[i][2]):
                    possible_list.append(local_list[i])
            
            if possible_list == []:
                possible_list = ['']
        
        else:
            possible_list = ['']
            
        #print(possible_list)
        return possible_list   

    
    #==============================start logic here
    country_list = country_search(country)
    if len(country_list) > 1:
        print("More than one country found return error.")
        Exception
    
    possible_list = []

    if area == '' and state == '':
        possible_list.append(country_list[0])

    trial_list = [location, area, state]
    for item in trial_list:
        state_list = state_search(item)
        area_list = area_search(item)
        
        for item1 in state_list:
            if str(item1)[:2] == country_list[0]:
                possible_list.append(item1)

        for item2 in area_list:
            if str(item2)[:2] == country_list[0]:
                possible_list.append(item2)    

    if possible_list == []:
        possible_list.append(country_list[0])
    
    with open(cities500_processed) as f:
        cities_list = json.load(f)
    
    #print(possible_list)
    positive_ids = []
    if location == '':
        for item in possible_list:
            code_list = item.split('.')
            criteria = len(code_list)
            for i in range(3-criteria):
                code_list.append('')
            
            
            for all_detail in cities_list:
                count = 0
                if all_detail[8] == code_list[0]:
                    count += 1
                if all_detail[10] == code_list[1]:
                    count += 1
                if all_detail[11] == code_list[2]:
                    count += 1
                if count >= criteria:
                    positive_ids.append(all_detail)
    
    else:
        location_list = location_search(location)
        if location_list == ['']:
            location_list = cities_list

        for item in possible_list:
            code_list = item.split('.')
            criteria = len(code_list)
            for i in range(3-criteria):
                code_list.append('')
            
            
            for all_detail in location_list:
                count = 0
                if all_detail[8] == code_list[0]:
                    count += 1
                if all_detail[10] == code_list[1]:
                    count += 1
                if all_detail[11] == code_list[2]:
                    count += 1
                if count >= criteria:
                    positive_ids.append(all_detail)
        
    lat_list, lon_list = [], []
    for all_detail in positive_ids:
        lat_list.append(float(all_detail[4]))
        lon_list.append(float(all_detail[5]))
    
    #print(positive_ids)         
    lat = statistics.mean(lat_list)
    lon = statistics.mean(lon_list)
    
    return [lat, lon]


if __name__ == '__main__':
    #address = geolocation(['Acucareira', '', 'Bengo', 'Angola']) 
    address = geolocation(['Santa Monica', '', 'California', 'US']) 
    print(address)

        
        
        

        