# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 18:38:41 2019

@author: thoma
"""
import requests
from bs4 import BeautifulSoup
from random import randint
import re
import json
import time
import multiprocessing as mp


def get_random_ua():
    random_ua = ''
    ua_file = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\general_programs\scraper\ua_file.txt'

    ua_list = []

    with open(ua_file) as f:
        lines = f.readlines()
    for line in lines:
        if len(lines) > 0:
            ua_list.append(line)
    
    choice = randint(0,len(ua_list)-1)
    random_ua = ua_list[choice]
    return random_ua

def generate_https_proxy_list():
    url = "https://free-proxy-list.net/"
    proxy_file = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\general_programs\scraper\proxy_file.txt'
    
    try:
        with open(proxy_file, 'w') as f:
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

        soup = BeautifulSoup(r.text, 'html.parser')        
        proxy_list_https = []
        for item in soup.find_all('tr'):
            ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", str(item))
            port = re.findall(r"\d{4,5}", str(item))
            ip_address_raw = str(ip).replace("[",'').replace("]",'')+":"+str(port).replace("[",'').replace("]",'')
            ip_address = ip_address_raw.replace("'",'')
            if ip_address != ':':
                proxy_list_https.append(str(ip_address))        
    
    except Exception:
        r = requests.get("https://free-proxy-list.net/")
        soup = BeautifulSoup(r.text, 'html.parser')
        proxy_list_https = []
        for item in soup.find_all('tr'):
            ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", str(item))
            port = re.findall(r"\d{4,5}", str(item))
            ip_address_raw = str(ip).replace("[",'').replace("]",'')+":"+str(port).replace("[",'').replace("]",'')
            ip_address = ip_address_raw.replace("'",'')
            if ip_address != ':':
                proxy_list_https.append(str(ip_address))
   
    with open(proxy_file, 'w') as f:
        json.dump(proxy_list_https, f)

def get_random_proxy():
    proxy_file = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\general_programs\scraper\proxy_file.txt'

    with open(proxy_file) as f:
        proxy_list = json.load(f)
    
    choice = randint(0,len(proxy_list)-1)
    random_proxy = proxy_list[choice]
    return random_proxy


def everything_between(text, begin, end):
    idx1=text.find(begin)
    idx2=text.find(end,idx1)
    return text[idx1+len(begin):idx2].strip()

def get_working_identity():
    print("Searching for working proxy address...")
    def get_identity():
        proxy_ip = get_random_proxy()
        user_agent = get_random_ua()
        return [user_agent, proxy_ip]
    
    def test_identity():
        n = 0
        attempt_count = 0
        while n == 0:
            try:
                url = 'https://www.yahoo.com'
                identity_list = get_identity()
                user_agent = identity_list[0]
                proxy_ip = identity_list[1]
                headers = {'user-agent': user_agent}
                
                https_proxy = "https://"+str(proxy_ip)
                
                proxyDict = {
                              "https" : https_proxy, 
                            }
                r = requests.get(url,headers=headers,proxies=proxyDict)
                n = 1
                print("\t- Working proxy found...")
            
            except Exception:
                attempt_count = attempt_count + 1
                print("\t- Attempt " + str(attempt_count) + " to find working proxy...")
                if attempt_count > 10:
                    generate_https_proxy_list()
                    print("\t- Generating a new proxy list...")
                None

        return [user_agent, proxy_ip]
    
    return test_identity()

def get_working_identity_list():
    tested_proxy_file = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\general_programs\scraper\tested_proxy_file.txt'
    
    try:
        with open(tested_proxy_file) as f:
            tested_proxy_list = json.load(f)
            if len(tested_proxy_list) > 10:
                return tested_proxy_list
            else:
                while len(tested_proxy_list) <= 10:
                    count = 10 - len(tested_proxy_list)
                    print("Replenishing working proxy list: " + str(count) + " left...")
                    new_working_proxy = get_working_identity()
                    tested_proxy_list.append(new_working_proxy[1])
                with open(tested_proxy_file, 'w') as f:
                    json.dump(tested_proxy_list, f)                
                print("Working proxy list replenished")
                return tested_proxy_list
    
    except Exception:
        tested_proxy_list = []
        while len(tested_proxy_list) <= 10:
            count = 10 - len(tested_proxy_list)
            print("Replenishing working proxy list: " + str(count) + " left...")
            new_working_proxy = get_working_identity()
            tested_proxy_list.append(new_working_proxy[1])
        with open(tested_proxy_file, 'w') as f:
            json.dump(tested_proxy_list, f)                
        print("Working proxy list replenished")
        return tested_proxy_list

def get_random_working_proxy():
    tested_proxy_file = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\general_programs\scraper\tested_proxy_file.txt'

    with open(proxy_file) as f:
        proxy_list = json.load(f)
    
    choice = randint(0,len(proxy_list)-1)
    random_proxy = proxy_list[choice]
    return random_proxy

def get_tested_identity():
    proxy_ip = get_random_working_proxy()
    user_agent = get_random_ua()
    return [user_agent, proxy_ip]

def set_up(url):
    identity_list = get_working_identity()    
    user_agent = identity_list[0]
    proxy_ip = identity_list[1]
    
    headers = {'user-agent': user_agent}
    
    https_proxy = "https://"+str(proxy_ip)
    
    proxyDict = {
                  "https" : https_proxy, 
                }

    print("Requesting site info...")
    r = requests.get(url,headers=headers,proxies=proxyDict)
    print("Success")
    return r
    #r = foo()
    #pool = mp.Pool(mp.cpu_count())
    #result = pool.map(foo())

    # Wait 10 seconds for foo
#    time.sleep(10)
  #  if result.is_alive():
   #     print ("foo is running... let's kill it...")
    # Terminate foo
    #result.terminate()

    # Cleanup
    #result.join()

def scraper(url):        
    #starts off generating a new proxy list from the website, through a proxy
    generate_https_proxy_list()
    
    loop = True
    count = 0
    attempt_count = 0
    while loop:    
        #sleep a bit - google got suspicious when scraping niche things
        time.sleep(5)
        if attempt_count > 20:
            generate_https_proxy_list()
        
        try:
            r = set_up(url)
            break
        
        except Exception: #requests.exceptions.ConnectionError - suggest for specific proxy error
            count = count + 1
            print("\tScrape attempt: " + str(count)) 
            print("\tProxy Connection Error")
            attempt_count = attempt_count + 1
            if count > 20:
                break
    try:
        soup = BeautifulSoup(r.text, 'html.parser') #for json will need different parser
    
    except Exception:
        soup = 'Soup Error'
    return soup

def test_scraper():
    url = 'https://www.yahoo.com'
    soup = scraper(url)
    print(soup)
    
    with open('scraper_file.txt', 'w') as f:
        json.dump(str(soup.prettify), f)
        
    print('Success')

#test_scraper()
