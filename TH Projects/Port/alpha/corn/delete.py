# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 19:42:57 2019

@author: thoma
"""
from datetime import datetime

def date_from_isoweek(iso_year, iso_weeknumber, iso_weekday):
    return datetime.strptime(
        '{:04d} {:02d} {:d}'.format(iso_year, iso_weeknumber, iso_weekday),
        '%G %V %u').date()
    

print(date_from_isoweek(2016,15,7))