# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 13:13:15 2019

@author: thoma
"""

import os
import json


def process_sp_download(filename, destination1, destination2):
    with open(filename) as f:
        download_dict = json.load(f)

    close_price_dict = {}
    for key, items in download_dict.items():
        if key != 'Date':
            try:
                close_price_dict[key] = float(items['Adj Close'])
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
    
    spdirectory = r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata\shareprices"
    for file in os.listdir(spdirectory):
        if file.endswith(".txt"):
            filename = (os.path.join(spdirectory, file))
            destination1 = (os.path.join(spdirectory, "processed\close_price", file))
            destination2 = (os.path.join(spdirectory, "processed\close_price_1dchg", file))
            destination3 = (os.path.join(spdirectory, "beta_adj_close_price", file))
            process_sp_download(filename, destination1, destination2)
    
    indexdirectory = r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata\index"
    for file in os.listdir(indexdirectory):
        if file.endswith(".txt"):
            filename = (os.path.join(indexdirectory, file))
            destination1 = (os.path.join(indexdirectory, "processed\close_price", file))
            destination2 = (os.path.join(indexdirectory, "processed\close_price_1dchg", file))
            process_sp_download(filename, destination1, destination2)