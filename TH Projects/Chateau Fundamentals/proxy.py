# -*- coding: utf-8 -*-
"""
Created on Sat May 11 22:29:15 2019

@author: thoma
"""

from selenium import webdriver

PROXY = "192.249.53.158" # IP:PORT or HOST:PORT

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)

chrome = webdriver.Chrome(chrome_options=chrome_options)
chrome.get("http://google.com")

ChromeOptions options = new ChromeOptions();
// Add the WebDriver proxy capability.
Proxy proxy = new Proxy();
proxy.setHttpProxy("myhttpproxy:3337");
options.setCapability("proxy", proxy);