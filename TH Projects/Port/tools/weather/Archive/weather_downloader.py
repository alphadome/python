# -*- coding: utf-8 -*-
"""
Created on Sun May  5 22:53:54 2019

@author: thoma
"""

import urllib
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from selenium import webdriver
from datetime import date, datetime, timedelta
import json


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
        print(str(url) + +" "+str(err)+" error in analyzing contents - wrong webpage")
            
  

def get_weather_data_precip(address,update=''):
    """returns weather url of the input address"""
    #Check profile to see if we have already
   
    def proceed_with_method():
        #get address 
        geolocator = Nominatim(user_agent="specify_your_app_name_here")
        location = geolocator.geocode(address)
        
        # Set the URL you want to webscrape from
        url = ('http://climexp.knmi.nl/selectdailyseries.cgi?id=idsomeone@somewhere')
        
        driver = webdriver.Chrome(executable_path='C:/Users/thoma/Desktop/Python/TH Projects/Port/tools/chromedriver.exe')
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--test-type")
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)
        
        # select precipitation data
        select_button = driver.find_elements_by_xpath("//input[@name='climate' and @value='gdcnprcp']")[0]
        select_button.click()
        
        #clear keyword box
        select_box3= driver.find_elements_by_xpath('//*[@id="printable"]/div[3]/form/div/table/tbody/tr[10]/td/ul/li/input')[0]
        select_box3.clear()

        # input 10 stations near
        select_box0= driver.find_elements_by_xpath("//input[@name='num' and @class='forminput']")[0]
        select_box0.clear()
        select_box0.send_keys("10")

        # input latitude
        select_box1= driver.find_elements_by_xpath("//input[@name='lat' and @class='forminput']")[0]
        select_box1.clear()
        select_box1.send_keys(str(location.latitude))
        
        # input longitude
        select_box2= driver.find_elements_by_xpath("//input[@name='lon' and @class='forminput']")[0]
        select_box2.clear()
        select_box2.send_keys(str(location.longitude))

        # specify 10y of data min
        select_box2= driver.find_elements_by_xpath("//input[@name='min' and @class='forminput']")[0]
        select_box2.clear()
        select_box2.send_keys("10")
        
        #get stations 
        get_stations = driver.find_elements_by_xpath('//*[@id="printable"]/div[3]/form/div/table/tbody/tr[18]/td/input')[0]
        get_stations.click()
        
        
        #get list of links on page
        station_links = []
        elems = driver.find_elements_by_xpath("//a[@href]")
        for elem in elems:
            if "STATION" in elem.get_attribute("href"):
                station_links.append(elem.get_attribute("href"))
        driver.quit()        
        
        weather_dict_list = []
        position = 0
        end_position = len(station_links)-1
        
        while True:
            if position >= end_position:
                print("No weather station found")
                break
            
            else:
                url = str(station_links[position])
                driver = webdriver.Chrome(executable_path='C:/Users/thoma/Desktop/Python/TH Projects/Port/tools/chromedriver.exe')
                options = webdriver.ChromeOptions()
                options.add_argument('--ignore-certificate-errors')
                options.add_argument("--test-type")
                driver = webdriver.Chrome(chrome_options=options)
                driver.get(url)
        
                # get raw data
                raw_data = driver.find_elements_by_xpath('//*[@id="printable"]/div[3]/div[1]/a[4]')[0]
                raw_data.click()
        
                weather_station_url = driver.current_url
                final_dict = analyse_contents(weather_station_url)
                driver.quit()        

                date_list = []
                for w_date in final_dict.keys():
                    formattedas_date = datetime.strptime(w_date, "%Y-%m-%d")
                    date_list.append(formattedas_date)
                
                if max(date_list) > datetime.today() - timedelta(6*365/12):
                    weather_dict_list.append(final_dict)
                    end_position = position
                    break
                else:
                    position = position + 1

        return weather_dict_list[0]
    
    title = "get_weather_data_precip"
    if weather_profile(address, title) == None or update != '':
        print("/t-Adding/refreshing data...")
        data = proceed_with_method()
        weather_profile(address, title, data)
        return weather_profile(address, title)

    else:
        return weather_profile(address, title)

def get_weather_data_temp(address,update=''):
    """returns weather url of the input address"""
    #Check profile to see if we have already
   
    def proceed_with_method():
        #get address 
        geolocator = Nominatim(user_agent="specify_your_app_name_here")
        location = geolocator.geocode(address)
        
        # Set the URL you want to webscrape from
        url = ('http://climexp.knmi.nl/selectdailyseries.cgi?id=idsomeone@somewhere')
        
        driver = webdriver.Chrome(executable_path='C:/Users/thoma/Desktop/Python/TH Projects/Port/tools/chromedriver.exe')
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--test-type")
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)
        
        # select precipitation data
        select_button = driver.find_elements_by_xpath("//input[@name='climate' and @value='gdcntave']")[0]
        select_button.click()
        
        #clear keyword box
        select_box3= driver.find_elements_by_xpath('//*[@id="printable"]/div[3]/form/div/table/tbody/tr[10]/td/ul/li/input')[0]
        select_box3.clear()

        # input 10 stations near
        select_box0= driver.find_elements_by_xpath("//input[@name='num' and @class='forminput']")[0]
        select_box0.clear()
        select_box0.send_keys("10")

        # input latitude
        select_box1= driver.find_elements_by_xpath("//input[@name='lat' and @class='forminput']")[0]
        select_box1.clear()
        select_box1.send_keys(str(location.latitude))
        
        # input longitude
        select_box2= driver.find_elements_by_xpath("//input[@name='lon' and @class='forminput']")[0]
        select_box2.clear()
        select_box2.send_keys(str(location.longitude))

        # specify 10y of data min
        select_box2= driver.find_elements_by_xpath("//input[@name='min' and @class='forminput']")[0]
        select_box2.clear()
        select_box2.send_keys("10")
        
        #get stations 
        get_stations = driver.find_elements_by_xpath('//*[@id="printable"]/div[3]/form/div/table/tbody/tr[18]/td/input')[0]
        get_stations.click()
        
        
        #get list of links on page
        station_links = []
        elems = driver.find_elements_by_xpath("//a[@href]")
        for elem in elems:
            if "STATION" in elem.get_attribute("href"):
                station_links.append(elem.get_attribute("href"))
        driver.quit()        
        
        weather_dict_list = []
        position = 0
        end_position = len(station_links)-1
        
        while True:
            if position >= end_position:
                print("No weather station found")
                break
            
            else:
                url = str(station_links[position])
                driver = webdriver.Chrome(executable_path='C:/Users/thoma/Desktop/Python/TH Projects/Port/tools/chromedriver.exe')
                options = webdriver.ChromeOptions()
                options.add_argument('--ignore-certificate-errors')
                options.add_argument("--test-type")
                driver = webdriver.Chrome(chrome_options=options)
                driver.get(url)
        
                # get raw data
                raw_data = driver.find_elements_by_xpath('//*[@id="printable"]/div[3]/div[1]/a[4]')[0]
                raw_data.click()
        
                weather_station_url = driver.current_url
                final_dict = analyse_contents(weather_station_url)
                driver.quit()        

                date_list = []
                for w_date in final_dict.keys():
                    formattedas_date = datetime.strptime(w_date, "%Y-%m-%d")
                    date_list.append(formattedas_date)
                
                if max(date_list) > datetime.today() - timedelta(6*365/12):
                    weather_dict_list.append(final_dict)
                    end_position = position
                    break
                else:
                    position = position + 1

        return weather_dict_list[0]
    
    title = "get_weather_data_temp"
    if weather_profile(address, title) == None or update != '':
        print("/t-Adding/refreshing data...")
        data = proceed_with_method()
        weather_profile(address, title, data)
        return weather_profile(address, title)
    else:
        return weather_profile(address, title)

get_weather_data_precip("Iowa",'update')
get_weather_data_temp("Iowa",'update')


