# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 20:25:49 2019

@author: thoma
"""
import sys
import_list = [
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools",
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\general\scraper",
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs",
        r"C:\Users\thoma\AppData\Local\Programs\Python\Python37-32\Lib\site-packages"        

        ]
for import_location in import_list:
    if import_location not in sys.path:
        sys.path.append(import_location)

import requests
import json
from datetime import datetime
from yahoo_historical import Fetcher
from yahoo_finance import Share, Currency

def text_between(text, left, right):
    between = text[text.index(left)+len(left):text.index(right)]
    return between

def uni_to_datetime(number):
    ts = int(number)

    # if you encounter a "year is out of range" error the timestamp
    # may be in milliseconds, try `ts /= 1000` in that case
    real = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')# %H:%M:%S')
    return real

destination_folder = r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata\shareprices\\"

def download_yahoo_sp_old(ticker):
    """downloads share price dict from yahoo finance api for associated RIC ticker"""
    api_url = "https://query1.finance.yahoo.com/v7/finance/download/%s?period1=%s&period2=%s&interval=%s&events=%s&crumb=%s"
    
    end=None
    interval="1d"
    url = api_url % (ticker, start, end, interval, events, crumb)
    
    #url = 'https://finance.yahoo.com/quote/%s/history' % (ticker)
    r = requests.get(url)
    txt = r.content
    
    price_dict = {}
    for line in txt.splitlines():
        if "HistoricalPriceStore" in str(line):
            between = text_between(str(line), 'HistoricalPriceStore":{"prices":', ',"isPending')
            price_list = eval(between)
            for item in price_list:
                try:
                    pdate = item["date"]
                    local_dict = {}
                    for key in item.keys():
                        if key != "date":
                            local_dict[key] = item[key]
                     
                    pdate = uni_to_datetime(pdate)
                    print(pdate)
                    price_dict[pdate] = local_dict
                
                except Exception:
                    None
            
    #print(price_dict)
            
    new_filename = (destination_folder + ticker + ".txt")
    with open(new_filename, 'w') as f:
        json.dump(price_dict, f)

def download_yahoo_sp(ticker):
    today = datetime.today()
    data = Fetcher(ticker, [2000,1,1], [today.year,today.month,today.day])
    price_dict = data.getPriceDict()
    new_filename = (destination_folder + ticker + ".txt")
    with open(new_filename, 'w') as f:
        json.dump(price_dict, f)
    return price_dict


if __name__ == '__main__':
    ticker = "^STOXX"
    download_yahoo_sp(ticker)

            
