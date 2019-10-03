# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 22:13:59 2019

@author: thoma
"""

from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import pandas as pd

ts = TimeSeries(key='386JT8YPOT81S0X8', output_format='pandas')
data, meta_data = ts.get_intraday(symbol='MSFT',interval='1min', outputsize='full')
data['close'].plot()
plt.title('Intraday Times Series for the MSFT stock (1 min)')
plt.show()
