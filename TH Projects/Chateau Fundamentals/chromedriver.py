# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 17:34:08 2019

@author: thoma
"""



from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location = r"C:/Users/thoma/Desktop/Python/TH Projects/chromedriver.exe"
# This line defines your Chromium exe file location.

driver = webdriver.Chrome(chrome_options=options)
driver.get('https://www.google.com/')