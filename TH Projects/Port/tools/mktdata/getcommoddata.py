# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 22:09:12 2019

@author: thoma
"""

from mktprice_call import download_quandl
import time
import os
import json

commod_list = [['TFGRAIN', 'CORN'], ['OPEC', 'ORB'], ['LBMA', 'GOLD'], ['CHRIS', 'CME_HG2']]

def download_data():
    for commod in commod_list:
        time.sleep(20)
        download_quandl(commod[0], commod[1])

def process_commod_download(filename, destination1, destination2):
    with open(filename) as f:
        download_dict = json.load(f)
        
    time_series_dict = download_dict['dataset_data']
    
    close_price_dict = {}
    for key, items in time_series_dict.items():
        try:
            close_price_dict[key] = float(items)
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
    
    #download_data()
    
    for file in os.listdir(r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata\commodity"):
        if file.endswith("_price_data.txt"):
            filename = (os.path.join(r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata\commodity", file))
            destination1 = (os.path.join(r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata\commodity\processed\close_price", file))
            destination2 = (os.path.join(r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata\commodity\processed\close_price_1dchg", file))
            process_commod_download(filename, destination1, destination2)