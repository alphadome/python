# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 08:54:25 2019

@author: thoma
"""
import re
from bs4 import BeautifulSoup

with open('scraper_file.txt') as f:
    r = json.load(f)

soup = BeautifulSoup(r, 'html.parser')
proxy_list_https = []
for item in soup.find_all('tr'):
    print(item)
    ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", str(item))
    port = re.findall(r"\d{4,5}", str(item))
    print(ip, port)
    ip_address_raw = str(ip).replace("[",'').replace("]",'')+":"+str(port).replace("[",'').replace("]",'')
    ip_address = ip_address_raw.replace("'",'')
    if ip_address != ':':
        if "elite proxy" in str(item):
            proxy_list_https.append(str(ip_address))
    
