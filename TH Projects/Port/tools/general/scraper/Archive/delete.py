# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 18:19:57 2019

@author: thoma
"""

import sys
import_list = [
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools",
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\general\scraper",
        ]
for import_location in import_list:
    if import_location not in sys.path:
        sys.path.append(import_location)

from bs4 import BeautifulSoup
import json
from scraper import scraper, generate_https_proxy_list
import re

print(generate_https_proxy_list())

def download():
    url = 'https://www.proxynova.com/proxy-server-list/elite-proxies/'
    soup = scraper(url)
    print(soup)
    
    with open('soup_file.txt', 'w') as f:
        json.dump(str(soup.prettify), f)
        
    print('Success')

def hang_on():
    with open('soup_file.txt') as f:
        contents = json.load(f)
    
    soup = BeautifulSoup(contents, features="lxml")
    proxies = soup.findAll("tr")
    proxy_list_https = []
    for item in proxies:
        #print(str("\n")+str(item))
        ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", str(item))
        port = re.findall(r"\bport-\b\d{1,5}", str(item))
        if ip != [] and port !=[]:
            proxy_ip = str(ip[0]+':'+str(port[0]).replace("port-",''))
            proxy_list_https.append(proxy_ip)
        
    print(proxy_list_https)


def generate_https_proxy_list():
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
    
            soup = BeautifulSoup(r.text, 'html.parser')        
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

#print(generate_https_proxy_list())
