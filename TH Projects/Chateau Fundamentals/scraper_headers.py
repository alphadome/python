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

#user_agent = get_random_ua()

#headers = {'user-agent': user_agent}

#for downloading data
#r = requests.get(url,headers=headers,proxies={'https': proxy_url})

#print(get_random_ua())
#url = 'https://www.google.com/'

#user_agent = get_random_ua()

#headers = {'user-agent': user_agent}

#for downloading data
#r = requests.get(url,headers=headers,proxies={'https': proxy_url})

#for selenium
#service_args = [
    #'--proxy={0}'.format(proxy),
    #'--proxy-type=http',
    #'--proxy-auth=user:password'
#]
#print('Processing..' + url)

#driver = webdriver.Chrome(service_args=service_args)
