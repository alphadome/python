# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 13:57:40 2019

@author: thoma
"""
import json
from bs4 import BeautifulSoup
from weather_tools import text_between
import re
from weather_tools import coordinate_distance, find_lat_lon


def find_closest_forecast_location(soup):
    
    with open('scraper_forecast_file.txt') as f:
        contents = json.load(f)
    
    soup = BeautifulSoup(contents)
    links = soup.findAll("div", {"class": "info"})
    
    location_list = []
    for link in links:
        try:
            href = text_between(str(link),'href="', '"><em>')
            accu_codes =  re.findall(r'\(\d+\)', str(link))
            try:
                code = accu_codes[0]
            except Exception:
                code = '</em>'
        
            location = text_between(str(link),'<em>', code)
            location_list.append([location, href])
        
        except Exception:
            None
    
    if location_list == []:
        print("Forecast scraper needs attention")
    
    home = find_lat_lon("Illinois")
    lat1 = home[0]
    lon1 = home[1]
    
    distance_location_list = []
    distance_list = []
    
    for location in location_list:
        try:
            accu_location = find_lat_lon(str(location[0]))
            lat2 = accu_location[0]
            lon2 = accu_location[1]
            distance = float(coordinate_distance(lat1, lon1, lat2, lon2))
            distance_location_list.append([distance, location[0], location[1]])
            distance_list.append(distance)
            print("Checking distance of forecast location: " + str(location[0]))
    
        except Exception:
            None
    
    closest_location_distance = min(distance_list)
    
    for place in distance_location_list:
        if place[0] == closest_location_distance:
            url = place[2]
            name = place[1]
    
    print(url, name, min(distance_list))
    return url
    
    
    
    
    