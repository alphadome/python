# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 15:34:31 2019

@author: thoma
"""
import matplotlib.pyplot as plt
from datetime import datetime
from stockclass import Stock

ticker1 = input("Input ticker1:  ")
ticker2 = input("Input ticker2:  ")

ticker_1 = Stock(ticker1)
ticker_2 = Stock(ticker2)

response_dict_1 = ticker_1.get_shareprice_data()
time_series = response_dict_1['Time Series (Daily)']

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

# axis 1
color = 'tab:red'
plt.xlabel("Date", fontsize =12)
fig.autofmt_xdate()
plt.ylabel(str(ticker1), color='black', fontsize =12)
plt.plot(x_values_selected, y_values_selected, color=color)
plt.tick_params(axis='y', labelcolor=color)

ax2 = plt.twinx()  # instantiate a second axes that shares the same x-axis

#axis 2
color = 'tab:blue'
ax2.set_ylabel(str(ticker2), color='black', fontsize=12)  # we already handled the x-label with ax1
ax2.plot(x_values_selected, ticker_2.get_shareprice_data_y(), color=color)
ax2.tick_params(axis='y', labelcolor=color)

#remove borders
plt.gca().spines['top'].set_visible(False)

#Chart title
plt.title(str(ticker1 + " & " + ticker2 + " share price chart"), fontsize = 14)

#Show chart
plt.show()

