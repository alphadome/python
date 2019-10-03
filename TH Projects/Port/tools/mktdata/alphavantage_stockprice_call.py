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


def get_quandl(dataset, ticker):
    api_key = "fLWzoTtv7FAScXoPzk8L"
    url = ('https://www.quandl.com/api/v3/datasets/' + str(dataset) +'/' + str(ticker) + '/data.json?api_key=' + str(api_key))
    r = requests.get(url)
    print("Status code:", r.status_code)
    print(str(r.text))    
    download_dict = eval(str(r.text).replace('null','"null"'))
    dataset_dict = download_dict['dataset_data']
    data_list = dataset_dict['data']
    
    desired_dict = {}
    for item in data_list:
        date = item[0]
        price = item[1]
        desired_dict[date] = price

    filename = (str(route) + str(ticker) + '_quandl_price_data.txt')
    with open(filename,'w') as f:
        json.dump(desired_dict, f)

get_quandl('TFGRAIN', 'CORN')