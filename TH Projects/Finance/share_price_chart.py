# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 15:34:31 2019

@author: thoma
"""
import ast
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime
from alphavantage_stockprice_call import get_shareprice

ticker = input("Input ticker:  ")

#Open dictionary and store data
filename = (str(ticker) + '_share_price_data.txt')
try:
    with open(filename) as file_object:
        #convert the string format from the .txt file to a python dictionary
        response_dict = ast.literal_eval(file_object.read())

except FileNotFoundError:
    #if there is no existing file download it from alphavantage
    get_shareprice(ticker)
    with open(filename) as file_object:
        #convert the string format from the .txt file to a python dictionary
        response_dict = ast.literal_eval(file_object.read())

# Split up the dictionary into the useful bits
meta_data = response_dict['Meta Data']
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
plt.title(str(ticker + " share price chart"), fontsize = 14)

#Create the chart
plt.plot(x_values_selected, y_values_selected)

#Show chart
plt.show()
