# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 12:33:03 2019

@author: thoma
"""
from datetime import date, datetime, timedelta

year = 2018
for m in range(1,13):
    for d in range(1,31):
        f_date = datetime(year,m,d)
        print(f_date)