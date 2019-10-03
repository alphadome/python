# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 13:23:35 2019

@author: thoma
"""

import tarfile
import os

tar = tarfile.open(r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_databases\databases\ghcnd_all.tar.gz", "r:gz")

count = 0
for tarinfo in tar:
    print(tarinfo.name)
    if "US" in str(tarinfo.name):
        print('found')
        f = tar.extractfile(tarinfo)
        content = f.read()
        print(content)
        
tar.close()
