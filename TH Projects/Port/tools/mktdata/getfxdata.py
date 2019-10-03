# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 20:46:00 2019

@author: thoma
"""

from mktprice_call import get_fx
import time
import os
import json

fx_list = ["BRL", "ARS", "SEK", "GBP", "EUR", "USD"] #to be continued

duplicate_list = []
for item in fx_list:
    duplicate_list.append(item)

couples_list = []
for fx in fx_list:
    duplicate_list.remove(fx)
    for item in duplicate_list:
        if fx != item:
            if [fx, item] not in couples_list and [item, fx] not in couples_list:
                couples_list.append([fx, item])

def download_data():    
    for item in couples_list:
        time.sleep(20)
        get_fx(item)

def process_fx_download(filename, destination1, destination2):
    with open(filename) as f:
        download_dict = json.load(f)
        
    time_series_dict = download_dict['Time Series FX (Daily)']
    close_price_dict = {}
    for key, items in time_series_dict.items():
        try:
            close_price_dict[key] = float(items['4. close'])
        except Exception:
            None

    with open(destination1,'w') as f:
        json.dump(close_price_dict, f)
            
    #turn close prices into pct change
    date_list = []
    for key in close_price_dict.keys():
        date_list.append(key)
    
    date_list = sorted(date_list)
    
    pct_dict = {}
    
    for i in range(1, len(date_list)):
        try:
            pct = (close_price_dict[date_list[i]] / close_price_dict[date_list[i-1]]) - 1
            pct_dict[date_list[i]] = pct
        except Exception:
            None
        
    with open(destination2,'w') as f:
        json.dump(pct_dict, f)
    
    return pct_dict

if __name__ == '__main__':
    
    #download_data
    
    for file in os.listdir(r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata\currency"):
        if file.endswith("_price_data.txt"):
            filename = (os.path.join(r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata\currency", file))
            destination1 = (os.path.join(r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata\currency\processed\close_price", file))
            destination2 = (os.path.join(r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata\currency\processed\close_price_1dchg", file))
            process_fx_download(filename, destination1, destination2)


    
    