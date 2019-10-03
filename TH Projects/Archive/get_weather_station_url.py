# -*- coding: utf-8 -*-
"""
Created on Wed May  1 17:58:46 2019

@author: thoma
"""

# Import libraries
import urllib
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from selenium import webdriver

def get_weather_station_url(address):
    """returns weather url of the input address"""
    #get address 
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    location = geolocator.geocode(address)
    
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
    return weather_station_url

   
def get_station_identifier(url):
    station_identifier = str(url[len(url)-19:len(url)-4])
    return station_identifier


