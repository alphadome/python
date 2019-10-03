# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 15:14:18 2019

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
import statistics

filename = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\geo\cities500.txt'
citycode = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\geo\citycode_processed.txt'

with open(filename, encoding="utf-8") as f:
    contents = f.readlines()

with open(citycode) as f:
    code_list = json.load(f)
        
def search_location_alt(town, region, state, word_country):
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
    print(sorted_ranking)
    best_answer = ranked_dict[sorted_ranking[len(sorted_ranking)-1]]

    new_line = best_answer.split('\t')
    answer = []
    for i in [1,2,4,5,8,10,17,14]:
        answer.append(new_line[i])
  
    return [answer[2], answer[3], answer[0]]

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
    lat = []
    lon = []
    place = []
    for subpool in country_pool:
        count = 0
        if str(town) in subpool and str(town) != '':
            count = count + 10
            print(subpool)
        if str(region) in subpool and str(region) != '':
            count = count + 5
        if str(state) in subpool and str(state) != '':
            count = count + 1
        ranked_dict[count] = subpool
        ranking.append(count)
        
        new_line = subpool.split('\t')

        lat.append(float(new_line[4]))
        lon.append(float(new_line[5]))
        place.append(new_line[1])
    
    adj_ranking, adj_lat, adj_lon = [], [], []
    if town == '':
        for i in range(len(ranking)-1):
            if ranking[i] == max(ranking):
                adj_ranking.append(ranking[i])
                adj_lat.append(lat[i])
                adj_lon.append(lon[i])
    
        if region != "":
            place = region
        elif state != "":
            place = state
        else:
            place = word_country
    
        avg_lat = statistics.mean(adj_lat)
        avg_lon = statistics.mean(adj_lon)
        
    
    else:
        for i in range(len(ranking)-1):
            if ranking[i] == max(ranking):
                adj_ranking.append(ranking[i])
                adj_lat.append(lat[i])
                adj_lon.append(lon[i])
        
        place = town
        avg_lat = statistics.mean(adj_lat)
        avg_lon = statistics.mean(adj_lon)        
    
  
    return [avg_lat, avg_lon, place]    
if __name__ == '__main__':    
    #print(search_location('Santa Monica', 'LA', 'CA', 'US'))
    #print(search_location('Corsham', '', '', 'UK'))
    #print(search_location('Ulua', 'Bengo', '', 'Angola'))
    'print(search_location('Iowa City', '', 'IA', 'US'))
    #print(search_location_new('', 'Penang', '', 'MY'))
    #print(search_location_new('', 'London', '', 'UK'))