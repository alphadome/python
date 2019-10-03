# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 15:14:18 2019

@author: thoma
"""
import sys
import_list = [
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools",
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\general\scraper",
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs"        
        ]
for import_location in import_list:
    if import_location not in sys.path:
        sys.path.append(import_location)


import json

filename = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\geo\citycode.txt'
processed_filename = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\geo\citycode_processed.txt'



if __name__ == '__main__':
    with open(filename, encoding="utf-8") as f:
        contents = f.readlines()
    
    result_list = []
    
    for line in contents:
        #print(line)
        new_line = line.split('\t')
        result = []
        for i in [0,3,4]:
            result.append(new_line[i])
        
        result_list.append(result)
        
    with open(processed_filename, 'w') as f:
        json.dump(result_list, f)
    
    print(result_list)
