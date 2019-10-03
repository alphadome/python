# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 22:25:18 2019

@author: thoma
"""
import time
timeout = time.time() + 0.01*1   # 1 minutes from now

while time.time() < timeout:
    print("test")
    
print("Ended")