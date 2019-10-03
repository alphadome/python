# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 19:00:51 2019

@author: thoma
"""

filename = r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_databases\databases\ghcnd_all\ACW00011604.dly"
with open(filename) as f:
    contents = f.read()

print(contents)