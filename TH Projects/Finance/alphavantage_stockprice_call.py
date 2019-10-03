# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 14:34:31 2019

@author: thoma
"""

import requests

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
    with open(filename,'w') as file_object:
        file_object.write(str(response_dict))


    


