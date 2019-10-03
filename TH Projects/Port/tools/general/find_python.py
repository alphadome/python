# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 18:25:13 2019

@author: thoma
"""

import sys
import platform
import imp

print("Python EXE     : " + sys.executable)
print("Architecture   : " + platform.architecture()[0])
print("Path to arcpy  : " + imp.find_module("arcpy")[1])

raw_input("\n\nPress ENTER to quit")
