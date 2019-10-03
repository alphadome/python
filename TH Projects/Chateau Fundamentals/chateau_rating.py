# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 11:08:28 2019

@author: thoma
"""

# -*- coding: utf-8 -*-
"""
Created on Fri May 10 01:16:14 2019

@author: thoma
"""

import requests
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from selenium import webdriver
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt
import json
from scraper_headers import get_random_ua
import time
from chateau_tools import eomonth, dict_unpacker, vintage_monthly_weather_dict, average_seasonal_weather_dict



class Chateau_rating():

    def __init__(self, address):
        """initialize attributes to define a stock"""
        self.address = address
        
    def chateau_profile(self, name, data=''):
            """Store a profile in the file so we do not repeat every action"""
            filename = (str(self.address) + "_rating_profile.txt")
            #open as write - this takes care of the initial instance of the file
            # if we can read the profile read it, otherwise create an empty dict
    
            try:
                with open(filename) as f:
                    contents = json.load(f)
                chateau_profile_dict = contents
    
            except FileNotFoundError:
                chateau_profile_dict = {}
    
            except ValueError:
                print("dictionary has a value error")
                chateau_profile_dict = {}
                     
            # if there is an existing entry:     
            if name in chateau_profile_dict.keys():
                if data:
                    del chateau_profile_dict[name]
                    chateau_profile_dict[name] = data
                    # store the amended profile          
                    with open(filename, 'w') as f:
                        json.dump(chateau_profile_dict,f)
                    return chateau_profile_dict[name]
                else:
                    return chateau_profile_dict[name]
            
            # if there isn't an existing entry
            else:
                if data:
                    # create a new one if there is data
                    chateau_profile_dict[name] = data
                    # store the amended profile          
                    with open(filename, 'w') as f:
                        json.dump(chateau_profile_dict,f)
                    return chateau_profile_dict[name]
    
                else:
                    # return nothing if there isn't
                    return None
        
        
    def get_rating_data_url(self, update=''):
        """returns globalwinescore rating of the target chateau"""
        #Check profile to see if we have already
       
        def proceed_with_method():
            #start the webdriver to find the url to the chateaux on wine-searcher through google
            url = ('https://www.globalwinescore.com/')
            
            driver = webdriver.Chrome(executable_path='C:/Users/thoma/Desktop/Python/TH Projects/chromedriver.exe')
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument("--test-type")
            driver = webdriver.Chrome(chrome_options=options)
            driver.get(url)
            
            select_box1 = driver.find_elements_by_xpath("//input[@id='gws-search' and @name='wine']")[0]
            select_box1.clear()
            select_box1.send_keys(str(self.address))
            time.sleep(5)

            select_box1.send_keys(u'\ue007')
            
            #wait 5s so the page has time to load
            time.sleep(5)
            
            url_found = driver.current_url
            driver.quit()
            
            return url_found
            
            
        title = "get_rating_data_url"
        if update:
            data = proceed_with_method()
            Chateau_rating(self.address).chateau_profile(title, data)
            print(str(title) + " updated")
            return Chateau_rating(self.address).chateau_profile(title)

        elif Chateau_rating(self.address).chateau_profile(title) == None:
            data = proceed_with_method()
            Chateau_rating(self.address).chateau_profile(title, data)
            return Chateau_rating(self.address).chateau_profile(title)

        else:
            return Chateau_rating(self.address).chateau_profile(title)

    def get_rating_data(self, update=''):
        """returns wine price/date data of the input address"""
        #Check profile to see if we have already
       
        def proceed_with_method():
           
            url_wine = Chateau_rating(self.address).get_rating_data_url()
            #use requests to beautiful soup the page and then download the pricing data
            user_agent = get_random_ua()
            #print(user_agent)
            headers = {'user-agent': user_agent}
            r_wine = requests.get(url_wine,headers=headers)
            wine_soup = BeautifulSoup(r_wine.text, 'html.parser')
                
            item_list = []
            for item in wine_soup.find_all('p'):
                item_raw = str(item).replace('<','').replace('>','').replace('p','').replace('b','').replace('/','')
                try:
                    if float(item_raw) > 0:
                        item_list.append(item_raw)
                except Exception:
                    None
            
            item_dict_raw = {}
            for i in range(0, len(item_list)-1):
                if float(item_list[i]) > 101 and float(item_list[i+1]) < 101:
                    item_dict_raw[item_list[i]] = item_list[i+1]
            
            item_dict = {}
            for key, rating in item_dict_raw.items():
                y = int(key)
                m = 12
                item_date = eomonth(y, m)
                item_dict[str(item_date).replace(' 00:00:00','')] = rating
            
           
            return item_dict
        
        #store result in chateau profile
        title = "get_rating_data"
        if update:
            data = proceed_with_method()
            Chateau_rating(self.address).chateau_profile(title, data)
            print(str(title) + " updated")
            return Chateau_rating(self.address).chateau_profile(title)

        elif Chateau_rating(self.address).chateau_profile(title) == None:
            data = proceed_with_method()
            Chateau_rating(self.address).chateau_profile(title, data)
            return Chateau_rating(self.address).chateau_profile(title)

        else:
            return Chateau_rating(self.address).chateau_profile(title)


    def print_wine_rating(self, beg_year):
        """print the share price data in a chart"""
        # Split up the dictionary into the useful bits
        price_dict_raw = Chateau_rating(self.address).get_rating_data()
        price_dict = dict_unpacker(price_dict_raw)
        #create the chart list
        x_values, y_values = [], []
        
        for key in price_dict.keys():
            x_date = key
            if int(x_date.year) > int(beg_year):
                x_values.append(key)
                y_values.append(float(str(price_dict[key])))
       
        print(len(x_values))
        print(len(y_values))
        #Size the output
        fig = plt.figure(dpi=128, figsize=(10,6))
        
        #remove borders
        fig.gca().spines['top'].set_visible(False)
        fig.gca().spines['right'].set_visible(False)
        
        #Chart gridlines
        plt.grid(None, 'major', 'both')
        
        #Axis tick formats
        for tick in plt.gca().get_xticklabels():
            tick.set_fontname("Calibri")
            tick.set_fontsize(12)
            tick.set_rotation('vertical')
        for tick in plt.gca().get_yticklabels():
            tick.set_fontname("Calibri")
            tick.set_fontsize(12)
        
        #Axis labels and formats
        plt.xlabel("Date", fontsize =12)
        #fig.autofmt_xdate()
        plt.ylabel('Rating', fontsize =12)
        #Chart title
        plt.title(str(self.address), fontsize = 14)
        
        #Create the chart
        plt.bar(x_values, y_values)
        
        #Show chart
        plt.show()
    
#Chateau_rating("Chateau Cheval Blanc").get_rating_data('update')
#Chateau_rating("Chateau Margaux").print_wine_rating(1970)   
#Chateau_data("Ridge Monte Bello Santa Cruz Mountains ").print_wine_price(1970) 