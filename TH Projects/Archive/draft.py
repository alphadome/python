# -*- coding: utf-8 -*-
"""
Created on Tue May  7 22:11:47 2019

@author: thoma
"""
import ast

filename = "1186 Route de Castres, 33650 Saint-Morillon, France_profile.txt"


with open(filename) as file_object:
    contents = file_object.read()
print(contents)
chateau_profile_dict = ast.literal_eval(contents)
chateau_profile_dict["popo"] = "123"
print(chateau_profile_dict)
#with open(filename,'w') as f:
    #f.write(str(chateau_profile_dict))  