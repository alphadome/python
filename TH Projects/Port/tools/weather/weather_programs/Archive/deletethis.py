# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 22:51:01 2019

@author: thoma
"""

with open(r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_databases\databases\ghcnd-inventory.txt") as f:
    contents = f.read()

print(contents[:10000])