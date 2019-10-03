# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 18:25:13 2019

@author: thoma
"""

# Python program showing 
# how to kill threads 
# using set/reset stop 
# flag 
  
import threading 
import time 


  
def run(): 
    n = 0
    while n < 1: 
        print('thread running') 
        n = n + 1
        global stop_threads 
        if stop_threads: 
            break
  
stop_threads = False
t1 = threading.Thread(target = run) 
t1.start() 
time.sleep(5) 
stop_threads = True
t1.join() 
print('thread killed') 