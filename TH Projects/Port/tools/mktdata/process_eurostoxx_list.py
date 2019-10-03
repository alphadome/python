# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 14:25:51 2019

@author: thoma
"""

import sys
import_list = [
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools",
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\general\scraper",
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs",
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata"        

        ]
for import_location in import_list:
    if import_location not in sys.path:
        sys.path.append(import_location)

import json
import time
from datetime import date, datetime, timedelta
import statistics
from mktprice_call import search_ticker_alphavantage
from yahoofinance import download_yahoo_sp

import pandas as pd
#df = pd.read_excel(io=file_name, sheet_name=sheet)
#print(df.head(15))  # print first 5 rows of the dataframe

# Reading an excel file using Python 
import xlrd 
  
def xldate_to_datetime(xldate):
	temp = datetime(1900, 1, 1)
	delta = timedelta(days=xldate)
	return temp+delta

loc = (r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata\stoxx800list.xlsx") 
dest = (r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata\stoxx800dict.txt")


def get_from_xls():
      
    # To open Workbook 
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0)
      
    #for i in range(sheet.ncols): 
    #    print(i, sheet.cell_value(2,i))
    count = 0
    progress_dict = {}
    for i in range(sheet.nrows): 
        item_list = []
        for j in [2,5,9,7]:
            try:
                item_list.append(float(sheet.cell_value(i, j)))
            except Exception:
                item_list.append(str(sheet.cell_value(i, j)))
        
        try:
            if float(item_list[2]) > 2: #criteria to only take mkt cap above 1bn
                progress_dict[item_list[0]] = [item_list[1], item_list[2], item_list[3]]
                count += 1
        
        except Exception:
            None
    
    #print(progress_dict)
    #print(count)
    
    
    
    return progress_dict

def old_method():
    #get list from sxxp list
    progress_dict = get_from_xls()
    
    #get list from current analysed tickers
    with open(dest) as f:
        current_progress = json.load(f)
    
    #update ticker and error lists with previous work
    error_list = []
    ticker_list = []
    
    success_list = current_progress[0]
    fail_list = current_progress[1]
    
    for success in success_list:
        ticker_list.append(success)
    
    for fail in fail_list:
        error_list.append(fail)
        
    print(ticker_list, error_list)
    
    #define protocol for breaking
    def break_protocol():
        with open(dest, 'w') as f:
            json.dump([ticker_list, error_list], f)
    
    #start analysig new tickers
    count = 0
    for key, items in progress_dict.items():
        if str(key) not in success_list:
            time.sleep(15)
            result_list = search_ticker_alphavantage(key)
            if str(result_list[1]) != str(200):
                break_protocol()
                print("Server error breaking...")
                break
            
            filtered_list = []
            for result_dict in result_list[0]:
                if result_dict['8. currency'] == items[2]:
                    filtered_list.append(result_dict['1. symbol'])
                    
            if filtered_list == []:
                result_list = search_ticker_alphavantage(items[0])
                if str(result_list[1]) != str(200):
                    break_protocol()
                    print("Server error breaking...")
                    break
                for result_dict in result_list[0]:
                    if result_dict['8. currency'] == items[2]:
                        filtered_list.append(result_dict['1. symbol'])    
            
            print(filtered_list)
            
            if len(filtered_list) == 0:
                error_list.append(key)
                print(count, ': error for', key)
            else: 
                ticker_list.append(filtered_list[0])
                print(count, ': ', filtered_list[0])
        
            count += 1
            break_protocol()

def from_core_list():
    
    #get list from sxxp list
    progress_dict = get_from_xls()

    ticker_dict = {}
   
    def ticker_transformation_one(ticker):
        ticker_parts = ticker.split('.')
        if ticker_parts[1] == 'S':
            ticker = ticker_parts[0] + '.SW'
        if ticker_parts[1] == 'MM':
            ticker = ticker_parts[0] + '.ME'
        if ticker_parts[1] == 'I':
            ticker = ticker_parts[0] + '.IR'
        if 'b' in ticker:
            ticker = ticker.replace('b','-B')
        if 'a' in ticker:
            ticker = ticker.replace('a','-A')
        if 'G.DE' in ticker:
            ticker = ticker.replace('G.DE','.DE')    
        if 'n.' in ticker:
            ticker = ticker.replace('n.','.') 
        return ticker
    

    #start log lists for save protocl    
    success_list, fail_list = [], []
    
    def save_protocol():
        with open("log.txt", 'w') as f:
            json.dump([success_list, fail_list], f)
    
    def run_protocol():
        count = 0
        
        with open("manual1.txt") as f:
            manual_dict = json.load(f)
        
        for key in progress_dict.keys():
            count += 1
    
            try:
                if key in manual_dict.keys():
                    ticker = manual_dict[key]
                
                download_yahoo_sp(str(ticker))
                print(count, ": ", key)
                success_list.append(key)
                ticker_dict[key] = ticker
                
            except Exception:
                
                try:
                    ticker = ticker_transformation_one(key)
                    download_yahoo_sp(str(ticker))
                    print(count, ": ", key)
                    success_list.append(key)
                    ticker_dict[key] = ticker
                
                except Exception:
                    
                    try:
                        ticker = ticker_transformation_one(key)
                        ticker_parts = ticker.split('.')
                        ticker = str(ticker_parts[0])[0:len(ticker_parts[0])-1] + '.' + ticker_parts[1]
                        download_yahoo_sp(str(ticker))
                        print(count, ": ", key)
                        success_list.append(key)
                        ticker_dict[key] = ticker                    
                    
                    except Exception:
                        fail_list.append(key)
                        print("Error")
                    
            
            save_protocol()
    
    run_protocol()

    with open("RIC2Yahoo.txt", 'w') as f:
        json.dump(ticker_dict, f)
    with open("faillist.txt", 'w') as f:
        json.dump(fail_list,f)
            
            
if __name__ == '__main__':
    
    from_core_list()
   
    