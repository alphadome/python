# -*- coding: utf-8 -*-
"""
Created on Sun May  5 22:53:54 2019

@author: thoma
"""

import urllib
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from selenium import webdriver
from datetime import date
import matplotlib.pyplot as plt
import json

class Chateau():
    
    def __init__(self, address):
        """initialize attributes to define a stock"""
        self.address = address
    
    def chateau_profile(self, name, data=''):
        """Store a profile in the file so we do not repeat every action"""
        filename = (str(self.address) + "_weather_profile.txt")
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
    
    
    def get_weather_station_url(self):
        """returns weather url of the input address"""
        #Check profile to see if we have already
       
        def proceed_with_method():
            #get address 
            geolocator = Nominatim(user_agent="specify_your_app_name_here")
            location = geolocator.geocode(self.address)
            
            # Set the URL you want to webscrape from
            url = ('http://climexp.knmi.nl/selectdailyseries.cgi?id=idsomeone@somewhere')
            
            driver = webdriver.Chrome(executable_path='C:/Users/thoma/Desktop/Python/TH Projects/chromedriver.exe')
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

            # input latitude
            select_box1= driver.find_elements_by_xpath("//input[@name='lat' and @class='forminput']")[0]
            select_box1.clear()
            select_box1.send_keys(str(location.latitude))
            
            # input longitude
            select_box2= driver.find_elements_by_xpath("//input[@name='lon' and @class='forminput']")[0]
            select_box2.clear()
            select_box2.send_keys(str(location.longitude))
            
            #get stations 
            get_stations = driver.find_elements_by_xpath('//*[@id="printable"]/div[3]/form/div/table/tbody/tr[18]/td/input')[0]
            get_stations.click()
            
            # get station data
            station = driver.find_elements_by_xpath('//*[@id="printable"]/div[3]/a[1]')[0]
            station.click()
            
            # get raw data
            raw_data = driver.find_elements_by_xpath('//*[@id="printable"]/div[3]/div[1]/a[4]')[0]
            raw_data.click()
            
            weather_station_url = driver.current_url
            driver.quit()
            #Chateau(self.address).chateau_profile("get_weather_station_url", weather_station_url)
            return weather_station_url
        
        title = "get_weather_station_url"
        if Chateau(self.address).chateau_profile(title) == None:
            data = proceed_with_method()
            Chateau(self.address).chateau_profile(title, data)
        else:
            return Chateau(self.address).chateau_profile(title)
    
    
    def get_station_identifier(self):
        
        def proceed_with_method():
            print("run station identifier method")
            url = str(Chateau(self.address).get_weather_station_url())
            station_identifier = str(url[len(url)-19:len(url)-4])
            return station_identifier
            
        title = "get_station_identifier"
        if Chateau(self.address).chateau_profile(title) == None:
            data = proceed_with_method()
            Chateau(self.address).chateau_profile(title, data)
        else:
            return Chateau(self.address).chateau_profile(title)
    
    def station_downloader(self, category, update = ''):
        """download weather data into txt files and cleans it"""
        #category p = precip, v = avg temp
        def proceed_with_method():
            station_identifier = Chateau(self.address).get_station_identifier()
            url = 'http://climexp.knmi.nl/data/' +str(category) +str(station_identifier) +'.dat'
            
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
                
                return date_list
         
            #needs an error in case there is a wrong url        
            except urllib.error.HTTPError as err:
                print(str(station_identifier) + " " + str(url) + " " + str(err.code))
        
        title = "station_downloader_" + str(category)
        if update:
            data = proceed_with_method()
            Chateau(self.address).chateau_profile(title, data)
            print(str(title) + " updated")
            return Chateau(self.address).chateau_profile(title)

        elif Chateau(self.address).chateau_profile(title) == None:
            data = proceed_with_method()
            Chateau(self.address).chateau_profile(title, data)
            return Chateau(self.address).chateau_profile(title)

        else:
            return Chateau(self.address).chateau_profile(title)
                
    def weather_dict(self, category, update =''):
        """creates a list of dates and weather data and saves it"""
        def proceed_with_method():
            date_list = Chateau(self.address).station_downloader(category, update)
             
            #for some reason this next bit takes a lot of processing power - this bit removes duplicates in the list, for some reason there are 3
            final_dict = {}
            print("1")
            for item in date_list:
                year = item[0]
                month = item[1]
                day = item[2]
                item_date = str(date(int(year), int(month), int(day)))
                item_value = item[len(item)-1]
                
                if item_date not in final_dict.keys():
                    final_dict[item_date] = item_value
            print("2")        
                
            return final_dict
    
        title = "weather_dict_" + str(category)
        if update:
            data = proceed_with_method()
            Chateau(self.address).chateau_profile(title, data)
            print(str(title) + " updated")
            return Chateau(self.address).chateau_profile(title)

        elif Chateau(self.address).chateau_profile(title) == None:
            data = proceed_with_method()
            print("3")
            Chateau(self.address).chateau_profile(title, data)
            return Chateau(self.address).chateau_profile(title)

        else:
            return Chateau(self.address).chateau_profile(title)
        
        
    def print_weather_dict(self, category):
        """print the share price data in a chart"""
        # Split up the dictionary into the useful bits
        final_dict = Chateau(self.address).weather_dict(category)
        #create the chart list
        x_values, y_values = [], []
        
        for key in final_dict.keys():
           x_values.append(key)
           y_values.append(float(final_dict[key]))
        
        #chart breaks with too many values so choose 1y
        x_values_selected = x_values[len(x_values)-500:len(x_values)-1]
        y_values_selected = y_values[len(y_values)-500:len(y_values)-1]
                  
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
        plt.ylabel(str(category), fontsize =12)
        
        #Chart title
        plt.title(str(self.address) + " " + str(category), fontsize = 14)
        
        #Create the chart
        plt.scatter(x_values_selected, y_values_selected)
        
        #Show chart
        plt.show()

#"1186 Route de Castres, 33650 Saint-Morillon, France"
#bordeaux = Chateau("Chateau Cheval Blanc St Emilion")
#bordeaux.get_weather_station_url()
#bordeaux.get_station_identifier()
#bordeaux.station_downloader('v')
#bordeaux.station_downloader('p')
#bordeaux.weather_dict('p', 'update')
#bordeaux.weather_dict('v', 'update')
#bordeaux.print_weather_dict('v')
#bordeaux.print_weather_dict('p')