# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 18:15:19 2019

@author: thoma
"""

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="specify_your_app_name_here")
location = geolocator.geocode("Chateau Cheval Blanc")
print(location.address)
print((location.latitude, location.longitude))
print(location.raw)
list = location.address.split(",")
loclist = []
for name in list:
    loclist.append(name)

print(loclist)
print(len(loclist))