# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 13:13:15 2019

@author: thoma
"""

import os
import json
import statistics

SXXP = r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata\index\processed\close_price_1dchg\^STOXX.txt"
with open(SXXP) as f:
    SXXP_dict = json.load(f)

SXXP_list = []
for key, items in SXXP_dict.items():
    SXXP_list.append(items)

mean = statistics.mean(SXXP_list)
stdev = statistics.stdev(SXXP_list)

#print(mean, stdev)

complete_beta_dict = {}


def beta(path, file):
    filename = (os.path.join(path, "processed\close_price_1dchg", file))

    with open(filename) as f:
        sp_dict = json.load(f)
    
    beta_dict = {}
    beta_list = []
    count = 0
    for key, items in SXXP_dict.items():
        if abs(items) > mean + stdev:
            try:
                calc = float(sp_dict[key]) / float(items)
                beta_list.append(calc)
                count += 1
                beta = statistics.mean(beta_list)
                betasd = statistics.stdev(beta_list)
                beta_dict[key] = [beta, betasd, count]
            except Exception:
                None
    
    destination = (os.path.join(path, "processed\\beta", file)) #needed a double slash for some reason
    
    with open(destination, 'w') as f:
        json.dump(beta_dict, f)
    
    try:
        complete_beta_dict[file] = [beta, betasd, count]
    except Exception:
        complete_beta_dict[file] = ["Error", "Error", "Error"]
        
    
    return beta_dict


if __name__ == '__main__':
   
    path = r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata\shareprices"
    chg_path = (os.path.join(path, "processed\\close_price_1dchg"))
    for file in os.listdir(chg_path):
        if file.endswith(".txt"):
            beta(path, file)
    
        with open(r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata\shareprices\processed\beta_summary.txt", 'w') as f:
            json.dump(complete_beta_dict, f)