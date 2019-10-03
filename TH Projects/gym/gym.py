# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 17:22:39 2019

@author: thoma
"""

import json
import re

filename = r'C:\Users\thoma\Desktop\Python\TH Projects\gym\gym.txt'
with open(filename) as f:
    contents = f.readlines()

days = ['Mon', 'Tues', 'Weds', 'Thurs', 'Sat', 'Sun']

for line in contents:
    print(line)
    for day in days:
        if day in line:
            date = line
            print(date)

    exercise = re.findall(r"\w+", str(line))
    print(exercise)
    #/^(.*?)abc/
    #ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", str(item))

    
    
    
    #print(line)
    print('\n')