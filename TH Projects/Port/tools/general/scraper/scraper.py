# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 18:38:41 2019

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

import requests
from bs4 import BeautifulSoup
from random import randint, choice
import re
import json
import time
from time_restriction import time_restricted
#can't import this from bulk scrape for some reason
def code_url(url):
    reserved_list = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', '.', '%', ' ']
    raw_named_list = ['lt', 'gt', 'co', 'qu', 'bs', 'fs', 'sl', 'qm', 'as', 'pb', 'pc', 'sp']
    named_list = []
    for name in raw_named_list:
        named_list.append(str("TH-")+str(name))
    
    coded_url = url
    for i in range(len(reserved_list)-1):
        symbol = reserved_list[i]
        if symbol in url:
            coded_url = coded_url.replace(symbol, named_list[i])
    
    return coded_url
    
untested_proxy_file = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\general\scraper\untested_proxy_file.txt'
tested_proxy_file = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\general\scraper\tested_proxy_file.txt'

def get_random_ua():
    random_ua = ''
    ua_file = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\general\scraper\ua_file.txt'

    ua_list = []

    with open(ua_file) as f:
        lines = f.readlines()
    for line in lines:
        if len(lines) > 0:
            ua_list.append(line)
    
    choice = randint(0,len(ua_list)-1)
    random_ua = ua_list[choice]
    return random_ua


def generate_https_proxy_list1():
    url = "https://free-proxy-list.net/anonymous-proxy.html"
    while True:
        try:
            with open(tested_proxy_file) as f:
                proxy_list = json.load(f)
            
            if proxy_list == '':
                Exception
            
            choice = randint(0,len(proxy_list)-1)
            random_proxy = proxy_list[choice]
            
            user_agent = get_random_ua()
            
            headers = {'user-agent': user_agent}
            proxy_ip = random_proxy
            
            https_proxy = "https://"+str(proxy_ip)
            
            proxyDict = {
                          "https" : https_proxy, 
                        }
            
            r = requests.get(url,headers=headers,proxies=proxyDict)
    
            soup = BeautifulSoup(r.text, 'html.parser', features="lxml")        
            proxy_list_https = []
            for item in soup.find_all('tr'):
                ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", str(item))
                port = re.findall(r"\d{4,5}", str(item))
                ip_address_raw = str(ip).replace("[",'').replace("]",'')+":"+str(port).replace("[",'').replace("]",'')
                ip_address = ip_address_raw.replace("'",'')
                if ip_address != ':':
                    proxy_list_https.append(str(ip_address))
            
            print("New elite proxy list downloaded (best anonymity)")
            
            with open(untested_proxy_file, 'w') as f:
                json.dump(proxy_list_https, f)
            break
    
        except Exception:
            try:
                r = requests.get("https://free-proxy-list.net/anonymous-proxy.html")
                soup = BeautifulSoup(r.text, 'html.parser')
                proxy_list_https = []
                for item in soup.find_all('tr'):
                    ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", str(item))
                    port = re.findall(r"\d{4,5}", str(item))
                    ip_address_raw = str(ip).replace("[",'').replace("]",'')+":"+str(port).replace("[",'').replace("]",'')
                    ip_address = ip_address_raw.replace("'",'')
                    if ip_address != ':':
                        #only use elite proxies - completely anonymous
                        if "elite proxy" in str(item):
                            proxy_list_https.append(str(ip_address))
                
                print("New elite proxy list downloaded (best anonymity)")
                
                with open(untested_proxy_file, 'w') as f:
                    json.dump(proxy_list_https, f)
                break
            except Exception:
                None
        
    return proxy_list_https

def generate_https_proxy_list2():
    url = 'https://www.proxynova.com/proxy-server-list/elite-proxies/'
    while True:
        try:
            with open(tested_proxy_file) as f:
                proxy_list = json.load(f)
            
            if proxy_list == '':
                Exception
            
            choice = randint(0,len(proxy_list)-1)
            random_proxy = proxy_list[choice]
            
            user_agent = get_random_ua()
            
            headers = {'user-agent': user_agent}
            proxy_ip = random_proxy
            
            https_proxy = "https://"+str(proxy_ip)
            
            proxyDict = {
                          "https" : https_proxy, 
                        }
            
            r = requests.get(url,headers=headers,proxies=proxyDict)
    
            soup = BeautifulSoup(r.text, 'html.parser', features="lxml")        
            proxy_list_https = []
            for item in soup.find_all('tr'):
                ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", str(item))
                port = re.findall(r"\bport-\b\d{1,5}", str(item))
                if ip != [] and port !=[]:
                    proxy_ip = str(ip[0]+':'+str(port[0]).replace("port-",''))
                    proxy_list_https.append(proxy_ip)
            
            print("New elite proxy list downloaded (best anonymity)")
            
            with open(untested_proxy_file, 'w') as f:
                json.dump(proxy_list_https, f)
            break
    
        except Exception:
            try:
                r = requests.get('https://www.proxynova.com/proxy-server-list/elite-proxies/')
                soup = BeautifulSoup(r.text, 'html.parser')
                proxy_list_https = []
                for item in soup.find_all('tr'):
                    ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", str(item))
                    port = re.findall(r"\bport-\b\d{1,5}", str(item))
                    if ip != [] and port !=[]:
                        proxy_ip = str(ip[0]+':'+str(port[0]).replace("port-",''))
                        proxy_list_https.append(proxy_ip)
                
                print("New elite proxy list downloaded (best anonymity)")
                
                with open(untested_proxy_file, 'w') as f:
                    json.dump(proxy_list_https, f)
                break
            except Exception:
                None
        
    return proxy_list_https


def generate_https_proxy_list():
    print("Generating untested proxy list...")
    
    answer = []
    while answer == []:
        switch = choice([True, False])
        if switch == True:
            answer = generate_https_proxy_list1()
            print("1")
        else:
            answer = generate_https_proxy_list2() 
            print("2")

    print("Done")    
    return answer


def test_proxy(proxy_ip, dv=''):
    try:
        url = 'https://www.yahoo.com'
        identity_list = get_random_ua()
        user_agent = identity_list[0]
        headers = {'user-agent': user_agent}
        
        https_proxy = "https://"+str(proxy_ip)
        
        proxyDict = {
                      "https" : https_proxy, 
                    }
        print("\t\t- Sending request to test website and waiting...")
        requests.get(url,headers=headers,proxies=proxyDict)

        print("\t\t- Working proxy found...")
        result = "pass"
    except Exception:
        print("\t\t - Returned error from website")
        result = "fail"
   
    return result

def generate_tested_list(n):
    print("\t - Refreshing/ generating tested proxy list")
    def open_untested_proxy_file(untested_proxy_file):
        try:
            with open(untested_proxy_file) as f:
                untested_proxy_list = json.load(f)
            print("\t\t -Using existing untested proxy list file")
            if untested_proxy_list == '' or untested_proxy_list == []:
                print("\t\t -No existing untested proxy list - generating one")
                generate_https_proxy_list()
                with open(untested_proxy_file) as f:
                    untested_proxy_list = json.load(f)
        except Exception:
            generate_https_proxy_list()
            with open(untested_proxy_file) as f:
                untested_proxy_list = json.load(f)
            print("\t\t -No existing untested proxy list - generating one")
        
        return untested_proxy_list

    def open_tested_proxy_file(tested_proxy_file):

        try:
            with open(tested_proxy_file) as f:
                tested_proxy_list = json.load(f)
            if tested_proxy_list == '':
                tested_proxy_list = []
        
        except Exception:
            tested_proxy_list = []

        return tested_proxy_list
    
    #decide to take a new list every time for the scraper as 1. hopefully done thru a proxy, 2. recently tested by website
    #generate_https_proxy_list()
    
    untested_proxy_list = open_untested_proxy_file(untested_proxy_file)
    tested_proxy_list = open_tested_proxy_file(tested_proxy_file)

    count = 0
    success_count = 0
    while len(tested_proxy_list) < n:
        print("\t\t - " + str(n-len(tested_proxy_list)) + " to go... with " + str(success_count) + " sucessful attempts...")
        untested_proxy_list = open_untested_proxy_file(untested_proxy_file)
        tested_proxy_list = open_tested_proxy_file(tested_proxy_file)        
        choice = randint(0,len(untested_proxy_list)-1)
        proxy_ip = untested_proxy_list[choice]
        print("\t\t -Attempt: " + str(count) )
        untested_proxy_list.remove(proxy_ip)
        
        ##TEST HAPPENS HERE
        print("\t\t - starting test...")
        test_result = time_restricted(10, test_proxy, proxy_ip)
        print("\t\t - ending test...")
        if test_result == "pass":
            print("\t\t - Passed proxy test")
            tested_proxy_list.append(proxy_ip)
            print("\t\t - Adding to tested list proxy: " + str(proxy_ip))
            with open(tested_proxy_file,'w') as f:
                json.dump(tested_proxy_list, f)
            with open(untested_proxy_file,'w') as f:
                json.dump(untested_proxy_list, f)
            success_count = success_count + 1
                        
        if test_result != "pass":
            with open(untested_proxy_file,'w') as f:
                json.dump(untested_proxy_list, f)
            print("\t\t - Fail timer proxy test")
        
        count = count + 1
    

def get_random_proxy_tested():

    with open(tested_proxy_file) as f:
        proxy_list = json.load(f)
    
    if proxy_list == [] or proxy_list == '':
        generate_tested_list(20)
       
    choice = randint(0,len(proxy_list)-1)
    random_proxy = proxy_list[choice]
    return random_proxy    


def set_up(url, proxy_ip):
    user_agent = get_random_ua()
    
    headers = {'user-agent': user_agent}
    
    https_proxy = "https://"+str(proxy_ip)
    
    proxyDict = {
                  "https" : https_proxy, 
                }

    print("\t - Requesting site info with proxy: " + str(proxy_ip))
    r = requests.get(url,headers=headers,proxies=proxyDict, timeout=10)
    print("\t - Scrape was a success")
    return r


def scraper_new(url):        
    #starts off generating a new proxy list from the website, through a proxy
    
    loop = True
    count = 0
    while loop:    
        #sleep a bit - google got suspicious when scraping niche things
        print("-Attempt: " + str(count))
        
        with open(tested_proxy_file) as f:
            tested_proxy_list = json.load(f)
        
        if len(tested_proxy_list) < 1:
            generate_tested_list(1)
            
        def remove_proxy_from_tested_file(proxy_ip):
            print("\t - Removing proxy " + str(proxy_ip) + " from tested list")
            tested_proxy_list.remove(proxy_ip)
            with open(tested_proxy_file,'w') as f:
                json.dump(tested_proxy_list, f)   
        
        if count > 20:
            print("\t - Scraper tool failed after 20 attempts - breaking process.")
            soup = 'Too many attempts error'
            break
        
        proxy_ip = get_random_proxy_tested()
            
        try:
            #set a loose time restriction as theoretically we have tested already
            r = time_restricted(15, set_up, url, proxy_ip)
        
        except Exception: #requests.exceptions.ConnectionError - suggest for specific proxy error
            print("\t - Proxy Connection Error")
            remove_proxy_from_tested_file(proxy_ip)
            count = count + 1
            soup = '\t - Request Error'
        
        if r == "fail":
            remove_proxy_from_tested_file(proxy_ip)
            count = count + 1
            soup = '\t - Request Error'
            count = count + 1
        else:
            try:
                soup = BeautifulSoup(r.text, 'html.parser') #for json will need different parser
                break
   
            except Exception:
                remove_proxy_from_tested_file(proxy_ip)
                soup = '\t - Soup Error'
                count = count + 1
                
    return soup


def scraper(url):
    try:
        filename = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\general\scraper\bulk_scrape\\' + str(code_url(url)) +'.txt'
        print(filename)
        with open(filename) as f:
            print("Found in bulk scrape file: " + str(url))
            rtext = json.load(f)
        
        soup = BeautifulSoup(rtext, features="lxml")
        
    except FileNotFoundError:
        print("Not found in bulk scrape file: " + str(url))
        soup = scraper_new(url)

    return soup


if __name__ == "__main__":
    url = 'https://www.yahoo.com/'
#   url = 'https://free-proxy-list.net/anonymous-proxy.html'
#    url = 'https://www.proxynova.com/proxy-server-list/elite-proxies/'
#   url = 'https://www.accuweather.com/en/us/lincoln-il/62656/weather-forecast/332738'
    soup = scraper(url)
    print(soup)
    
    with open('scraper_file.txt', 'w') as f:
        json.dump(str(soup.prettify), f)
        
    print('Success')
