# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 23:07:00 2019

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
import time
from datetime import date, datetime, timedelta
import statistics

import pandas as pd
#df = pd.read_excel(io=file_name, sheet_name=sheet)
#print(df.head(15))  # print first 5 rows of the dataframe

# Reading an excel file using Python 
import xlrd 
  
def xldate_to_datetime(xldate):
	temp = datetime(1900, 1, 1)
	delta = timedelta(days=xldate)
	return temp+delta

#print(xldate_to_datetime(43415))
# Give the location of the file 
loc = (r"C:\Users\thoma\Desktop\Python\TH Projects\Port\alpha\corn\CORN-CropProgress-2019-08-09.xlsx") 
dest = (r"C:\Users\thoma\Desktop\Python\TH Projects\Port\alpha\corn\corn_crop_progress_dict.txt")
progress_dest = (r"C:\Users\thoma\Desktop\Python\TH Projects\Port\alpha\corn\corn_crop_progress_time_series_dict.txt")


def get_from_xls():
      
    # To open Workbook 
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0)
      
    for i in range(sheet.ncols): 
        print(i, sheet.cell_value(0,i))
    
    progress_dict = {}
    for i in range(sheet.nrows): 
        item_list = []
        for j in range(8,sheet.ncols):
            try:
                item_list.append(float(sheet.cell_value(i, j)))
            except Exception:
                item_list.append(str(sheet.cell_value(i, j)))
        
        try:
            c_date_raw = xldate_to_datetime(float(sheet.cell_value(i, 7)))
            c_date = str(c_date_raw).replace(' 00:00:00','')
        except Exception:
            c_date = sheet.cell_value(i,7)                
        progress_dict[c_date] = item_list
    
    with open(dest, 'w') as f:
        json.dump(progress_dict, f)

def analyse_progress():
    with open(dest) as f:
        wasde_dict = json.load(f)
    
    progress_dict = {}
    
    titles = wasde_dict['WEEK ENDING']
    for i in range(len(titles)):
        print(i, titles[i])
    
    for key, title in wasde_dict.items():
        if key != 'WEEK ENDING':
            rating_list = []
            
            plant = title[0]
            plant_5y = title[1]
            em = title[3]
            em_5y = title[4]
            silk = title[6]
            silk_5y = title[7]
            dough = title[9]
            dough_5y = title[10]    
            dent = title[12]
            dent_5y = title[13]    
            mature = title[15]
            mature_5y = title[16]
            harvest = title[18]
            harvest_5y = title[19]
            
            stage_list = [
                             [plant, plant_5y],
                             [em, em_5y],
                             [silk, silk_5y],
                             [dough, dough_5y],
                             [dent, dent_5y],
                             [mature, mature_5y],
                             [harvest, harvest_5y]]
            
            
            for i in [0,6]:
                subitem = stage_list[i]
                if (subitem[0] != ' ' and subitem[1] != ' '):
                    rating_list.append((subitem[0] - subitem[1])*1*subitem[1]/100)
            
            for i in range(1,len(stage_list)-1):
                subitem = stage_list[i]
                if (subitem[0] != ' ' and subitem[1] != ' '):
                    rating_list.append((subitem[0] - subitem[1])*subitem[1]/100)
            
            try:
                progress = statistics.mean(rating_list)
                progress_dict[key] = float(progress)
            except Exception:
                None
    
    print(progress_dict)
    with open(progress_dest, 'w') as f:
        json.dump(progress_dict,f)
        
           

if __name__ == '__main__':
    get_from_xls()
    analyse_progress()