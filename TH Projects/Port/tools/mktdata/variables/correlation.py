# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 14:23:11 2019

@author: thoma
"""

import json
import os
import math
import statistics
import numpy as np
import matplotlib.pyplot as plt


def average(x):
    assert len(x) > 0
    return float(sum(x)) / len(x)

def pearson_def(x, y):
    """pearson_def([1,2,3], [1,5,7])"""
    assert len(x) == len(y)
    n = len(x)
    assert n > 0
    avg_x = statistics.mean(x)
    avg_y = statistics.mean(y)
    diffprod = 0
    xdiff2 = 0
    ydiff2 = 0
    for idx in range(n):
        xdiff = x[idx] - avg_x
        ydiff = y[idx] - avg_y
        diffprod += xdiff * ydiff
        xdiff2 += xdiff * xdiff
        ydiff2 += ydiff * ydiff
    return diffprod / math.sqrt(xdiff2 * ydiff2)



def day_correl():
    
    with open("ORB_quandl_price_data.txt") as f:
        indep_var_dict = json.load(f)

    correl_dict = {}
    for file in os.listdir(r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata\shareprices\processed\close_price_1dchg"):
        if file.endswith(".txt"):
            filename = (os.path.join(r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata\shareprices\processed\close_price_1dchg", file))
            with open(filename) as f:
                dep_var_dict = json.load(f)
            
            x_list, y_list = [], []
            
            for key, items in indep_var_dict.items():
                try:
                    y_list.append(dep_var_dict[key])
                    x_list.append(indep_var_dict[key])
                except Exception:
                    None
            
            correl_dict[pearson_def(x_list, y_list)] = [str(file).replace(".txt",''), len(x_list)]
    
    key_list = []
    for key in correl_dict.keys():
        key_list.append(key)
    
    key_list = sorted(key_list)
    
    adj_correl_dict = {}
    for key in key_list:
        adj_correl_dict[key] = correl_dict[key]
    
    
    with open("1dcorrel.txt", 'w') as f:
        json.dump(adj_correl_dict, f)
        
def movement_correl(destination, d=5):
    """ d is sampling frequency"""
    
    price_path = r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata\commodity\processed\close_price\ORB_quandl_price_data.txt"

    with open(price_path) as f:
        indep_var_dict = json.load(f)    
    
    date_list = []
    for key in indep_var_dict.keys():
        date_list.append(key)
    
    date_list = sorted(date_list)
    
    trimmed_dict = {}
    for i in range(len(date_list)):
        if i % d == 0:
            trimmed_dict[date_list[i]] = indep_var_dict[date_list[i]]
    
      
   
    correl_dict = {}
    for file in os.listdir(r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata\shareprices\processed\close_price"):
        if file.endswith(".txt"):
            filename = (os.path.join(r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata\shareprices\processed\close_price", file))
            with open(filename) as f:
                dep_var_dict = json.load(f)
            
            x_list, y_list = [], []
            
            for key, items in trimmed_dict.items():
                try:
                    y_list.append(dep_var_dict[key])
                    x_list.append(indep_var_dict[key])
                except Exception:
                    None
            
            def one_deriv(sample_list):
                
                pct_list = []
                for i in range(1, len(sample_list)):
                    try:
                        pct = (sample_list[i] / sample_list[i-1]) - 1
                        pct_list.append(pct)
                    except Exception:
                        None
                        
                return pct_list
            
            x_list = one_deriv(x_list)
            y_list = one_deriv(y_list)
            
            if len(x_list) != len(y_list):
                print(filename)
            
            adj_x_list, adj_y_list = [], []
            try:
                mean = statistics.mean(x_list)
                stdev = statistics.stdev(x_list)
                print(mean, stdev)
            except Exception:
                stdev=0
            
            for i in range(0,len(x_list)):
                if abs(x_list[i]) > mean + stdev:
                    try:
                        adj_y_list.append(y_list[i])
                        adj_x_list.append(x_list[i])
                    except Exception:
                        None
            
            try:
                correl_dict[pearson_def(adj_x_list, adj_y_list)] = [str(file).replace(".txt",''), len(x_list)]
            except Exception:
                None
            
    key_list = []
    for key in correl_dict.keys():
        key_list.append(key)
    
    key_list = sorted(key_list)
    
    adj_correl_dict = {}
    for key in key_list:
        adj_correl_dict[key] = correl_dict[key]
            
    
    with open(destination, 'w') as f:
        json.dump(adj_correl_dict, f)   

def correl_graph():

    with open("y1correl.txt") as f:
        dcorrel_dict = json.load(f)    

    with open("y5correl.txt") as f:
        ycorrel_dict = json.load(f)    
    
    dcorrel_ticker_dict = {}    
    for key, items in dcorrel_dict.items():
        dcorrel_ticker_dict[items[0]] = [float(key), items[1]]

    ycorrel_ticker_dict = {}    
    for key, items in ycorrel_dict.items():
        ycorrel_ticker_dict[items[0]] = [float(key), items[1]]
        
    #graph stuff
    x_values, y_values, n_values = [], [], []

    for key in ycorrel_ticker_dict.keys():
        try:
            x_values.append(ycorrel_ticker_dict[key][0])
            y_values.append(dcorrel_ticker_dict[key][0])
            n_values.append([str(key), ycorrel_ticker_dict[key][1], dcorrel_ticker_dict[key][1]])
        except Exception:
            None
    
    #calculate best fit line
    x = x_values
    y = y_values
    z = np.polyfit(x, y, 1)
    z_formatted = np.ndarray.tolist(z)
    p = np.poly1d(z)
    xp = np.linspace(min(x_values), max(x_values), 100) 
    
    #calculate correlation coefficient
    correl_y = p(x)
    #A = np.vstack([x, np.ones(len(x))]).T
    #m, c = np.linalg.lstsq(A, correl_y, rcond=None)[0]
    #print(m, c)
    R = np.corrcoef(y, correl_y)
    cor = R.item(1) #R is a 2x2 matrix so take the correct entry
    print("\nCorrelation coefficient: " + str('%0.2f' % cor))
               
    print("\nSuggested polynomial a*x + b has [a, b]: "
    #      + str('%0.2f' % z_formatted[0]) +", "
    #      + str('%0.2f' % z_formatted[1]) +", "
          + str('%0.2f' % z_formatted[0]) +", "
          + str('%0.2f' % z_formatted[1]))

                
    #Size the output
    fig = plt.figure(dpi=128, figsize=(25,15)) #10,6
    
    #Chart gridlines
    plt.grid(None, 'major', 'both')
    
    #Axis tick formats
    for tick in plt.gca().get_xticklabels():
        tick.set_fontname("Calibri")
        tick.set_fontsize(12)
        tick.set_rotation('vertical')
    for tick in plt.gca().get_yticklabels():
        tick.set_fontname("Calibri")
        tick.set_fontsize(12)
    
    #Axis labels and formats
    
    # axis 1
    color = 'tab:blue'
    plt.xlabel("y_correl", fontsize =12)
    #plt.xticks(np.arange(x_values[11], x_values[0], 2))
    plt.ylabel("1d_correl", color='black', fontsize =12)
    plt.scatter(x_values, y_values, color=color)
    plt.plot(xp, p(xp), color = 'red')
    plt.tick_params(axis='y', labelcolor=color)
    
    for i, txt in enumerate(n_values):
        plt.annotate(txt, (x[i], y[i]))
    
               
    #remove borders
    plt.gca().spines['top'].set_visible(False)
    
    #Chart title
    plt.title("5% move correlvs 1d correl", fontsize = 14)
    
    #Show chart
    plt.savefig('figure1.pdf')
    #plt.show()
            
#day_correl()
movement_correl("y5correl.txt", 5)
movement_correl("y1correl.txt", 1)
correl_graph()