# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 22:27:18 2019

@author: thoma
"""

from bbfreeze import Freezer

freezer = Freezer(distdir='dist')
freezer.addScript('helloworld.py', gui_only=True)
freezer()