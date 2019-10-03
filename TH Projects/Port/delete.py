# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 23:07:00 2019

@author: thoma
"""
import json

filename = r"C:\Users\thoma\Downloads\qs.crops_20190808.txt\qs.crops_20190808.txt"

with open(filename) as f:
    contents = json.load(f)

print(contents[:1000])