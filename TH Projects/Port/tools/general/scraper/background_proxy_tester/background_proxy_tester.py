# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 19:53:37 2019

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

from scraper import generate_https_proxy_list, generate_tested_list
generate_https_proxy_list()
generate_tested_list(100)
