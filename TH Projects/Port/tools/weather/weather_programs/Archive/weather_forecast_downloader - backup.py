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
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs"        

        ]
for import_location in import_list:
    if import_location not in sys.path:
        sys.path.append(import_location)

from scraper import scraper
from time_restriction import time_restricted
from weather_tools import somonth, join_dicts, text_between, coordinate_distance, find_lat_lon


import json
from bs4 import BeautifulSoup
import statistics
import dateutil.parser
from datetime import date, datetime, timedelta
from geopy.geocoders import Nominatim
import citipy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re
import json
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



def get_city(address):
    """get the nearest city to an address to find the weather forecast (forecast only has cities)"""
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    
    while True:
        try:
            location = geolocator.geocode(address)
            break
        except Exception:
            None
    
    city = citipy.nearest_city(location.latitude, location.longitude)
    return [city.city_name.title(), city.country_code.title()]

def find_closest_forecast_location(soup):
    """ if accuweather is on search-locations page this finds the closest forecast offered"""    

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


def visit_forecast_home(address):
    """return url of weather forecast site"""    
    
    getcity = get_city(address)
    location = str(str(getcity[0]) + ", " + str(getcity[1]))
    city = getcity[0]
    
    url = ('https://www.accuweather.com/en/gb/united-kingdom-weather')
    #url = ('https://www.accuweather.com/#')
        
    #driver = webdriver.Chrome(executable_path='C:/Users/thoma/Desktop/Python/TH Projects/Port/tools/general_programs/chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    driver = webdriver.Chrome(chrome_options=options, executable_path='C:/Users/thoma/Desktop/Python/TH Projects/Port/tools/general/chromedriver.exe')
    driver.get(url)
    
    # say yes to ads or we can't proceed
    driver.find_element_by_css_selector('p.fc-button-label').click()
    
    # input destination and hit enter
    #//*[@id="findcity"]/input[1]
    #//*[@id="s"]
    #//*[@id="findcity"]/input[3]
    #select_box0= driver.find_elements_by_xpath('//*[@id="findcity"]/input[1]')[0]
    #select_box0.click()
    select_box1= driver.find_elements_by_xpath('//*[@id="s"]')[0]
    select_box1.clear()
    select_box1.send_keys(str(location))
    
    time.sleep(10)
    print("GO")
    select_box1.send_keys(Keys.RETURN)
    #select_box1.send_keys(Keys.ENTER)
    #select_box0.submit()

    #select_box0.send_keys(u'\ue007')
    
    if driver.current_url == "https://www.accuweather.com/en/search-locations":
        
        html = driver.page_source
        soup = BeautifulSoup(html)
        desired_url = find_closest_forecast_location(soup)
    
    else:
        desired_url = driver.current_url
    
    driver.quit()
    return desired_url

#print(visit_forecast_home("London"))
#print(visit_forecast_home("Illinois"))


#with open('scraper_file.txt') as f:
#    contents = json.load(f)

def download_forecast_temp_old(contents):
    """input beautiful soup contents, output forecast temp dict"""
    """download temperature forecast temperature from accueilweather"""
    soup = BeautifulSoup(contents)
    datedivs = soup.findAll("h3", {"class": "date"})
    ltempdivs = soup.findAll("span", {"class": "large-temp"})
    stempdivs = soup.findAll("span", {"class": "small-temp"})
    
    datelist, ltemplist, stemplist = [], [], []
    
    for div in datedivs:
        required = text_between(str(div),'<time>', '</time>')
        estimated_date = str(required) + " " + str(datetime.today().year)
        yourdate = dateutil.parser.parse(estimated_date)
        year = yourdate.year
        month = yourdate.month
        day = yourdate.day
        item_date = str(date(int(year), int(month), int(day)))
        datelist.append(item_date)
    
    for div in ltempdivs:
        required = text_between(str(div),'"large-temp">', '°</span>')
        try:
            ltemplist.append(float(required))
        except Exception:
            print("t/- Scraping of the forecast page going wrong")
    
    for div in stempdivs:
        required = text_between(str(div),'"small-temp">/', '°</span>')
        stemplist.append(float(required))
        try:
            stemplist.append(float(required))
        except Exception:
            print("t/- Scraping of the forecast page going wrong")
    
    
    if len(datedivs) == len(ltempdivs) and  len(datedivs) == len(stempdivs):
        None
    else:
        print("t/-error in scraping of weather forecast download")
    
    
    forecast_dict = {}
    for i in range(0,len(datelist)-1):
        forecast_dict[datelist[i]] = statistics.mean([ltemplist[i],stemplist[i]])
    
    return forecast_dict
    

#soup = scraper("https://www.accuweather.com/en/gb/london/ec4a-2/january-weather/328328?monyr=7/1/2019&view=table")
#with open("trial_forecast.txt",'w') as f:
#    json.dump(str(soup), f)
#before = soup.findAll("tr", {"class":"pre"})
#after = soup.findAll("tr", {"class":"lo calendar-list-cl-tr cl hv"})
#souper = soup.findAll("a")
#print(souper)
#print(before)
#print(after)
#nos = re.findall(r'-?\d+\/\d+', "<time>7/1</time></th>")
#print(nos[0])
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
        url_base = visit_forecast_home(address)
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


#get_weather_forecast("London","update")




