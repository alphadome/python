# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 17:15:48 2019

@author: thoma
"""


def everything_between(text, begin, end):
    idx1=text.find(begin)
    idx2=text.find(end,idx1)
    return text[idx1+len(begin):idx2].strip()

