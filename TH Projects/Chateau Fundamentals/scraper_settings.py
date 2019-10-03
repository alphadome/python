# -*- coding: utf-8 -*-
"""
Created on Fri May 10 02:48:30 2019

@author: thoma
"""
import requests
import numpy as np
from selenium import webdriver
from random import randint

def get_random_ua():
    random_ua = ''
    ua_file = 'ua_file.txt'
    ua_list = []

    with open(ua_file) as f:
        lines = f.readlines()
    for line in lines:
        if len(lines) > 0:
            ua_list.append(line)
    
    choice = randint(0,len(ua_list)-1)
    random_ua = ua_list[choice]
    return random_ua
        
def get_random_proxy():
    random_proxy = ''
    proxy_file = 'proxy_file.txt'
    proxy_list = []

    with open(proxy_file) as f:
        lines = f.readlines()
    for line in lines:
        if len(lines) > 0:
            proxy_list.append(line)
    
    choice = randint(0,len(proxy_list)-1)
    random_proxy = proxy_list[choice]
    return random_proxy

url = 'https://www.google.com/'

user_agent = get_random_ua()
proxy_url = get_random_proxy()

headers = {'user-agent': user_agent}

#for downloading data
#r = requests.get(url,headers=headers,proxies={'https': proxy_url})

#for selenium
proxy = get_random_proxy()
service_args = [
    '--proxy={0}'.format(proxy),
    '--proxy-type=http',
    '--proxy-auth=user:password'
]
print('Processing..' + url)
browser = webdriver.PhantomJS(executable_path='/Users/thoma/Anaconda3/Lib/site-packages/selenium/webdriver/phantomjs')

driver = webdriver.PhantomJS(service_args=service_args)
