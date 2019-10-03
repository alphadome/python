# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 14:34:31 2019

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
import time
from datetime import date, datetime, timedelta


route = r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata\data\\"
# Make an API and store the response.
def get_shareprice(ticker):
    """download share price data from alphavantage"""
    url = ('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + str(ticker) + '&outputsize=full&apikey=386JT8YPOT81S0X8')
    r = requests.get(url)
    print("Status code:", r.status_code)
    
    # Store API response in a variable.
    response_dict = r.json()
    meta_data = response_dict['Meta Data']
    time_series = response_dict['Time Series (Daily)']
    
    #Create a file called ticker share price data and save the dictionary there
    filename = (str(ticker) + '_share_price_data.txt')
    with open(filename,'w') as f:
        json.dump(response_dict, f)

def get_fx(fx):
    """from fx1 to fx2"""
    [fx1, fx2] = fx
    url = ('https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=' + str(fx1) +'&to_symbol=' +str(fx2) +'&outputsize=full&apikey=386JT8YPOT81S0X8')
    r = requests.get(url)
    print("Status code:", r.status_code)
    
    # Store API response in a variable.
    response_dict = r.json()
    
    #Create a file called ticker share price data and save the dictionary there
    foldername = r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata\currency\\"
    filename = (foldername + str(fx1) +str(fx2) + '_price_data.txt')
    with open(filename,'w') as f:
        json.dump(response_dict, f)

def search_ticker_alphavantage(name):
    url = ('https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=' + str(name) + '&apikey=386JT8YPOT81S0X8')
    r = requests.get(url)
    print("Status code:", r.status_code)
    
    # Store API response in a variable.
    response_dict = r.json()
    #meta_data = response_dict['Meta Data']
    #time_series = response_dict['Time Series (Daily)']
    try:
        return_list = response_dict['bestMatches']
        print(return_list)
    except Exception:
        print(r.status_code)
        return_list = []
    #print(return_list)
    return [return_list, r.status_code]
    #Create a file called ticker share price data and save the dictionary there
    #filename = (str(ticker) + '_share_price_data.txt')
    #with open(filename,'w') as f:
    #    json.dump(response_dict, f)

def download_quandl(dataset, ticker):
    api_key = "fLWzoTtv7FAScXoPzk8L"
    url = ('https://www.quandl.com/api/v3/datasets/' + str(dataset) +'/' + str(ticker) + '/data.json?api_key=' + str(api_key))
    r = requests.get(url)
    print("Status code:", r.status_code)
    #print(str(r.text))    
    download_dict = eval(str(r.text).replace('null','"null"'))
    desired_dict = {}
   
    dataset_dict = download_dict['dataset_data']

    def add_key_to_desired_dict(key):
        desired_dict[key] = dataset_dict[key]
    
    for key in ['start_date', 'end_date']:
        add_key_to_desired_dict(key)
        
    data_list = dataset_dict['data']
    
    data_dict = {}
    for item in data_list:
        p_date = item[0]
        price = item[1]
        data_dict[p_date] = price
    
    desired_dict['dataset_data'] = data_dict
    update_date = str(date(int(datetime.today().year), int(datetime.today().month), int(datetime.today().day)))

    desired_dict['last_update'] = str(update_date)
    
    foldername = r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata\commodity\\"
    filename = (foldername + str(ticker) + '_quandl_price_data.txt')
    with open(filename,'w') as f:
        json.dump(desired_dict, f)
    
    return data_dict

def get_quandl(dataset, ticker):
    foldername = r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\mktdata\commodity\\"
    filename = (foldername + str(ticker) + '_quandl_price_data.txt')
    try:
        with open(filename) as f:
            local_dict = json.load(f)
        
        def unpack_date(p_date):
            formattedas_date = datetime.strptime(p_date, "%Y-%m-%d")
            return formattedas_date
        
        call_date = str(date(int(datetime.today().year), int(datetime.today().month), int(datetime.today().day)))

        if unpack_date(local_dict['last_update']) >= unpack_date(call_date):
            data_dict =  local_dict['dataset_data']
            print('Existing ' +str(ticker)+' data used')
        
        else:
            data_dict = 'Error'
            #Exception
        
    except Exception:
        data_dict = download_quandl(dataset, ticker)
        print('Fresh ' +str(ticker)+' data downloaded')

    
    return data_dict

def quandl_dict_unpacker(data_dict):
    price_dict = data_dict['dataset_data']
    return price_dict
        
    
if __name__ == '__main__':
    #download_quandl('TFGRAIN', 'CORN')
    #get_quandl('TFGRAIN', 'CORN')
    #search_ticker_alphavantage('Total')
    get_fx('EUR', 'USD')