# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 22:05:01 2019

@author: thoma
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime
from alphavantage_stockprice_call import get_shareprice
import json

class Stock():
  
    def __init__(self, ticker):
        """initialize attributes to define a stock"""
        self.ticker = ticker

    def get_shareprice_data(self):
        """find share price data or download it if it does not exist"""
        #Open dictionary and store data
        filename = (str(self.ticker) + '_share_price_data.txt')
        try:
            with open(filename) as f:
                #convert the string format from the .txt file to a python dictionary
                response_dict = json.load(f)
                return response_dict
        except FileNotFoundError:
            #if there is no existing file download it from alphavantage
            get_shareprice(self.ticker)
            with open(filename) as f:
                #convert the string format from the .txt file to a python dictionary
                response_dict = json.load(f)
                return response_dict
     
    def update_shareprice_data(self):
        """update share price data"""
        #Open dictionary and store data
        filename = (str(self.ticker) + '_share_price_data.txt')
        try:
            #if there is no existing file download it from alphavantage
            get_shareprice(self.ticker)
            with open(filename) as f:
                #convert the string format from the .txt file to a python dictionary
                response_dict = json.load(f)
                return response_dict
        except Exception:
            None
        else:
            print("There has been an error updating " + str(self.ticker))
    
    def get_shareprice_data_y(self):
        """return a list of historic share price values"""
        #Open dictionary and store data
        response_dict = Stock(self.ticker).get_shareprice_data()
        time_series = response_dict['Time Series (Daily)']
        
        #create the chart list
        x_values, y_values = [], []
        
        for time_series_date, time_series_data in time_series.items():
            formattedas_date = datetime.strptime(time_series_date, "%Y-%m-%d")
            x_values.append(formattedas_date)
            # y_values are strings and need to be floats to work in a chart
            y_values.append(float(time_series_data['4. close']))
        
        #chart breaks with too many values so choose 1y
        y_values_selected = y_values[0:500]
        return y_values_selected 
       
    def print_shareprice_chart(self):
        """print the share price data in a chart"""
        # Split up the dictionary into the useful bits
        response_dict = Stock(self.ticker).get_shareprice_data()
        time_series = response_dict['Time Series (Daily)']
        
        #create the chart list
        x_values, y_values = [], []
        
        for time_series_date, time_series_data in time_series.items():
            formattedas_date = datetime.strptime(time_series_date, "%Y-%m-%d")
            x_values.append(formattedas_date)
            # y_values are strings and need to be floats to work in a chart
            y_values.append(float(time_series_data['4. close']))
        
        #chart breaks with too many values so choose 1y
        x_values_selected = x_values[0:500]
        y_values_selected = y_values[0:500]
                  
        #Size the output
        fig = plt.figure(dpi=128, figsize=(10,6))
        
        #remove borders
        fig.gca().spines['top'].set_visible(False)
        fig.gca().spines['right'].set_visible(False)
        
        #Chart gridlines
        plt.grid(None, 'major', 'both')
        
        #Axis tick formats
        for tick in plt.gca().get_xticklabels():
            tick.set_fontname("Calibri")
            tick.set_fontsize(12)
        for tick in plt.gca().get_yticklabels():
            tick.set_fontname("Calibri")
            tick.set_fontsize(12)
        
        #Axis labels and formats
        plt.xlabel("Date", fontsize =12)
        fig.autofmt_xdate()
        plt.ylabel("Share price", fontsize =12)
        
        #Chart title
        plt.title(str(self.ticker + " share price chart"), fontsize = 14)
        
        #Create the chart
        plt.plot(x_values_selected, y_values_selected)
        
        #Show chart
        plt.show()


#ticker1 = input("Input ticker1:  ")
#ticker_1 = Stock(ticker1)
#ticker_1.print_shareprice_chart()


        
        
