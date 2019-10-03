# -*- coding: utf-8 -*-
"""
Created on Fri May  3 16:14:53 2019

@author: thoma
"""

# Import libraries
from get_weather_station_url import get_station_identifier
import ast
from transformer import Transformer

def list_to_dict(filename): 
    """find and replace in text file so its of dictionary format"""
    with open(filename) as f:
        newText = f.read()
        while '[' in newText:
            newText = newText.replace('[','{')
        while '[' in newText:
            newText = newText.replace(']','}')
 
    with open(filename, "w") as f:
        f.write(newText)

def dict_merge(address): 
    weather_url = 'http://climexp.knmi.nl/data/pgdcnFR000007510.dat'
    #get_weather_station_url(address)
    station_identifier = get_station_identifier(weather_url)
    
    p_url = 'p' +str(station_identifier) +'.txt'
    av_url = 'v' +str(station_identifier) +'.txt'
    min_url = 'n' +str(station_identifier) +'.txt'
    max_url = 'x' +str(station_identifier) +'.txt'

    weather_files = [p_url, av_url, min_url, max_url]
    print(p_url)   
    
    response_dict = []

    #for i in range(0,len(weather_files)-1):
        #list_to_dict(weather_files[i])
        #with open(weather_files[i]) as file_object:
            #convert the string format from the .txt file to a python dictionary
            #new_dict = ast.literal_eval(file_object.read())
            #print("1")
            #response_dict.append(new_dict)
            #print("2")
    with open(p_url) as file_object:
    
        tree = ast.parse(file_object.read(), mode='eval')
    
    transformer = Transformer()
    
    # raises RuntimeError on invalid code
    transformer.visit(tree)
    
    # compile the ast into a code object
    clause = compile(tree, '<AST>', 'eval')
    
    # make the globals contain only the Decimal class,
    # and eval the compiled object
    result = eval(clause, dict(Decimal=decimal.Decimal))

current_address = "1186 Route de Castres, 33650 Saint-Morillon, France"
dict_merge(current_address)
