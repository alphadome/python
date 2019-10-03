# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 17:41:55 2019

@author: thoma
"""

# Import libraries
import urllib
from bs4 import BeautifulSoup
from get_weather_station_url import get_weather_station_url, get_station_identifier
from datetime import date

currenturl = get_weather_station_url("1186 Route de Castres, 33650 Saint-Morillon, France")

#'http://climexp.knmi.nl/data/pgdcnFR000007510.dat'


station_identifier = get_station_identifier(currenturl)
print(station_identifier)
#station_index = str(currenturl[len(currenturl)-19:len(currenturl)-4])

    
def station_downloader(url,category):
    """download weather data into txt files and format it"""
    try:
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        
        filename = (str(category) + str(station_identifier) + ".txt")
        with open(filename, 'w') as file_object:
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
            
            #for some reason this next bit takes a lot of processing power - this bit removes duplicates in the list, for some reason there are 3
            final_dict = []
            for item in date_list:
                year = item[0]
                month = item[1]
                day = item [2]
                item_date = date(int(year), int(month), int(day))
                item_value = item[len(item)-1]
                final_item = {'date': item_date, str(category): item_value}
                
                if final_item not in final_dict:
                    final_dict.append(final_item)
                    
            #data now saved in a useful format
            file_object.write(str(final_dict))
            
    #needs an error in case there is a wrong url        
    except urllib.error.HTTPError as err:
        print(str(station_identifier) + " " + str(url) + " " + str(err.code))
    
# we have precipitation
# precipitation http://climexp.knmi.nl/data/pgdcnFR000007510.dat
p_url = 'http://climexp.knmi.nl/data/' + 'p' +str(station_identifier) +'.dat'
station_downloader(p_url, 'p')
print(str('p' +str(station_identifier)) + " done")
# average temp http://climexp.knmi.nl/data/vgdcnFR000007510.dat
av_url = 'http://climexp.knmi.nl/data/' + 'v' +str(station_identifier) +'.dat'
station_downloader(av_url, 'v')
print(str('v' +str(station_identifier)) + " done")

# min temp http://climexp.knmi.nl/data/ngdcnFR000007510.dat
min_url = 'http://climexp.knmi.nl/data/' + 'n' +str(station_identifier) +'.dat'
station_downloader(min_url, 'n')
print(str('n' +str(station_identifier)) + " done")

# max temp http://climexp.knmi.nl/data/xgdcnFR000007510.dat
max_url = 'http://climexp.knmi.nl/data/' + 'x' +str(station_identifier) +'.dat'
station_downloader(max_url, 'x')
print(str('x' +str(station_identifier)) + " done")
