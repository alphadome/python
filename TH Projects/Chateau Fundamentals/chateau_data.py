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
from datetime import datetime, date
import matplotlib.pyplot as plt
import json
from scraper_headers import get_random_ua

class Chateau_data():

    def __init__(self, address):
        """initialize attributes to define a stock"""
        self.address = address
        
    def chateau_profile(self, name, data=''):
            """Store a profile in the file so we do not repeat every action"""
            filename = (str(self.address) + "_data_profile.txt")
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
        
        
    def get_price_data_url(self, update=''):
        """returns wine-searcher url of the target chateau"""
        #Check profile to see if we have already
       
        def proceed_with_method():
            #start the webdriver to find the url to the chateaux on wine-searcher through google
            url = ('https://www.google.com/')
            
            driver = webdriver.Chrome(executable_path='C:/Users/thoma/Desktop/Python/TH Projects/chromedriver.exe')
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument("--test-type")
            driver = webdriver.Chrome(chrome_options=options)
            driver.get(url)
            
            select_box1 = driver.find_elements_by_xpath("//input[@type='text' and @role='combobox']")[0]
            select_box1.clear()
            select_box1.send_keys(str(self.address + " wine data market searcher"))
            select_box1.send_keys(u'\ue007')
            url_found = driver.current_url
            
            #find the wine-searcher url in the google search
            r = requests.get(url_found)
            google_soup = BeautifulSoup(r.text, 'html.parser')
            
            relevant_link = []
            
            for link in google_soup.find_all('a', href=True):
                if "https://www.wine-searcher.com/find/" in str(link):
                    relevant_link.append(link)

           
            google_list = str(relevant_link[2]).split("/")
            
            for i in range(0, len(google_list)-1):
                if "find" in google_list[i]:
                    url_wine = "https://www.wine-searcher.com/find/" + str(google_list[i+1]) + "/#t3"
                    break
            driver.quit()
            
            return url_wine
            
            
        title = "get_price_data_url"
        if update:
            data = proceed_with_method()
            Chateau_data(self.address).chateau_profile(title, data)
            print(str(title) + " updated")
            return Chateau_data(self.address).chateau_profile(title)

        elif Chateau_data(self.address).chateau_profile(title) == None:
            data = proceed_with_method()
            Chateau_data(self.address).chateau_profile(title, data)
            return Chateau_data(self.address).chateau_profile(title)

        else:
            return Chateau_data(self.address).chateau_profile(title)

    def get_price_data(self, update=''):
        """returns wine price/date data of the input address"""
        #Check profile to see if we have already
       
        def proceed_with_method():
           
            url_wine = Chateau_data(self.address).get_price_data_url()
            #use requests to beautiful soup the page and then download the pricing data
            user_agent = get_random_ua()
            #print(user_agent)
            headers = {'user-agent': user_agent}
            r_wine = requests.get(url_wine,headers=headers)
            wine_soup = BeautifulSoup(r_wine.text, 'html.parser')
            price_dict ={}
            
            def everything_between(text, begin, end):
                idx1=text.find(begin)
                idx2=text.find(end,idx1)
                return text[idx1+len(begin):idx2].strip()
                
            
            for item in wine_soup.find_all('a'):
                if "title=\"Avg:" in str(item):
                    line = everything_between(str(item),"title=\"Avg:",  "</span></a>") 
                    element = line.split(">")
                    wine_price = float((element[0].strip('\u20b4\"').strip("£")).replace(",", ""))
                    year = element[len(element)-1].strip("\n")
                    wine_date = str(date(int(year), int(12), int(31)))
                    price_dict[wine_date] = wine_price
            
            sorted_price_dict = {}
            for i in sorted(price_dict.keys()):
                sorted_price_dict[i] = price_dict[i]
            
            return sorted_price_dict
            
        #store result in chateau profile
        title = "get_price_data"
        if update:
            data = proceed_with_method()
            Chateau_data(self.address).chateau_profile(title, data)
            print(str(title) + " updated")
            return Chateau_data(self.address).chateau_profile(title)

        elif Chateau_data(self.address).chateau_profile(title) == None:
            data = proceed_with_method()
            Chateau_data(self.address).chateau_profile(title, data)
            return Chateau_data(self.address).chateau_profile(title)

        else:
            return Chateau_data(self.address).chateau_profile(title)


    def print_wine_price(self, beg_year):
        """print the share price data in a chart"""
        # Split up the dictionary into the useful bits
        price_dict = Chateau_data(self.address).get_price_data()
        #create the chart list
        x_values, y_values = [], []
        
        for key in price_dict.keys():
            x_date = datetime.strptime(key, '%Y-%m-%d')
            if int(x_date.year) > int(beg_year):
                x_values.append(key)
                y_values.append(float(str(price_dict[key])))
       
                
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
        plt.ylabel('Price', fontsize =12)
        
        #Chart title
        plt.title(str(self.address), fontsize = 14)
        
        #Create the chart
        plt.bar(x_values, y_values)
        
        #Show chart
        plt.show()
    
#Chateau_data("Chateau Cheval Blanc St Emilion").get_price_data('update')
#Chateau_data("Chateau Margaux").print_wine_price()   
#Chateau_data("Ridge Monte Bello Santa Cruz Mountains ").print_wine_price(1970) 