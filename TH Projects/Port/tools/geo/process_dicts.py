# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 10:23:01 2019

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

cities500 = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\geo\cities500.txt'
admincode1 = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\geo\admincode1.txt'
admincode2 = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\geo\admincode2.txt'
cities500_processed = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\geo\cities500_processed.txt'
admincode1_processed = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\geo\admincode1_processed.txt'
admincode2_processed = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\geo\admincode2_processed.txt'


def process_file(filename, processed_file):
    with open(filename, encoding="utf-8") as f:
        contents = f.readlines()
    
    content_list = []
    for line in contents:
        new_line = line.split('\t')
        content_list.append(new_line)
    
    with open(processed_file, 'w') as f:
        json.dump(content_list, f)

if __name__ == '__main__':
    process_file(cities500, cities500_processed)
    process_file(admincode1, admincode1_processed)
    process_file(admincode2, admincode2_processed)