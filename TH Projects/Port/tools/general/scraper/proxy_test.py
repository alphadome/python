# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 17:41:51 2019

@author: thoma
"""
import sys
import_list = [
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools",
        r"C:\Users\thoma\AppData\Local\Programs\Python\Python37-32\Lib\site-packages",
        ]
for import_location in import_list:
    if import_location not in sys.path:
        sys.path.append(import_location)
from proxylist.base import ProxyList
pl = ProxyList()
pl.load_file('/web/proxy.txt')
pl.random()
pl.random().address()
len(pl)