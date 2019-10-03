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
import statistics
from datetime import date, datetime, timedelta
import re
from weather_downloader import get_weather
from weather_tools import rolling_day, dict_unpacker, join_dicts
import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
#df = pd.read_excel(io=file_name, sheet_name=sheet)
#print(df.head(15))  # print first 5 rows of the dataframe

# Reading an excel file using Python 
import xlrd 
  
def xldate_to_datetime(xldate):
	temp = datetime(1899, 12, 30)
	delta = timedelta(days=xldate)
	return temp+delta

def date_to_datetime(p_date):
    #print(p_date)
    final = datetime.strptime(str(p_date).replace(" 00:00:00",""), '%Y-%m-%d')#.strftime('%Y-%m-%d %H:%M:%S')
    #print(final)
    #print("and year:")
    #print(str(final.year))
    return final

def date_from_isoweek(iso_year, iso_weeknumber, iso_weekday):
    return datetime.strptime(
        '{:04d} {:02d} {:d}'.format(iso_year, iso_weeknumber, iso_weekday),
        '%G %V %u')

#print(xldate_to_datetime(43415))
# Give the location of the file 
loc = (r"C:\Users\thoma\Desktop\Python\TH Projects\Port\alpha\corn\CORN-CropProgress-2019-08-09.xlsx") 
dest = (r"C:\Users\thoma\Desktop\Python\TH Projects\Port\alpha\corn\corn_crop_progress_dict.txt")
progress_dest = (r"C:\Users\thoma\Desktop\Python\TH Projects\Port\alpha\corn\corn_crop_progress_time_series_dict.txt")
progress_dest_detail = (r"C:\Users\thoma\Desktop\Python\TH Projects\Port\alpha\corn\corn_crop_progress_detail_time_series_dict.txt")


def get_from_xls():
      
    # To open Workbook 
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0)
      
    #for i in range(sheet.ncols): 
    #    print(i, sheet.cell_value(0,i))
    
    progress_dict = {}
    for i in range(sheet.nrows): 
        item_list = []
        for j in range(5,sheet.ncols):
            if j != 6 and j != 7:
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
    
    #print(progress_dict)
    return progress_dict


def detail_analyse_progress(wasde_dict):
    
    titles = wasde_dict['WEEK ENDING']
    for i in range(len(titles)):
        #print(i, titles[i])
        None
        
    plant_dict, em_dict, silk_dict, dough_dict, dent_dict, mature_dict, harvest_dict = {}, {}, {}, {}, {}, {}, {}
    category_list = [plant_dict, em_dict, silk_dict, dough_dict, dent_dict, mature_dict, harvest_dict]
    
    for key, title in wasde_dict.items():
        if key != 'WEEK ENDING':
            week =  float(re.findall(r'\d+',title[0])[0])
            plant = title[1]
            plant_5y = title[2]
            em = title[4]
            em_5y = title[5]
            silk = title[7]
            silk_5y = title[8]
            dough = title[10]
            dough_5y = title[11]    
            dent = title[13]
            dent_5y = title[14]    
            mature = title[16]
            mature_5y = title[17]
            harvest = title[19]
            harvest_5y = title[20]
            
            item_list = [plant, em, silk, dough, mature, harvest]
            for i in range(len(item_list)):
                if item_list[i] != ' ':
                    try:
                        category_list[i][key] = [week, item_list[i]]
                    except Exception:
                        None
    adj_plant_dict, adj_em_dict, adj_silk_dict, adj_dough_dict, adj_dent_dict, adj_mature_dict, adj_harvest_dict = {}, {}, {}, {}, {}, {}, {}
    adj_category_list = [adj_plant_dict, adj_em_dict, adj_silk_dict, adj_dough_dict, adj_dent_dict, adj_mature_dict, adj_harvest_dict]
            
    for i in range(len(category_list)):
        key_list = []   
        for key in category_list[i].keys():        
            key_list.append(key)
        
        key_list = sorted(key_list)
        for j in range(len(key_list)):
            def date_key(key):
                return datetime.strptime(key, "%Y-%m-%d")
            
            items1 = category_list[i][key_list[j]]
            
            if date_key(key_list[j]).year == date_key(key_list[j-1]).year:
                try:
                    items0 = category_list[i][key_list[j-1]]
                    change = (float(items1[1]) - float(items0[1]))/100
                    
                    adj_category_list[i][date_key(key_list[j])] = [items1[0], items1[1]/100, change]
                except Exception:
                    adj_category_list[i][date_key(key_list[j])] = [items1[0], items1[1]/100, items1[1]/100]
            
            try:
                if int(date_key(key_list[j]).year + 1) == int(date_key(key_list[j+1]).year):
                    items0 = category_list[i][key_list[j]]
                    change = (100 - float(items0[1]))/100
                    adj_category_list[i][date_key(key_list[j])+timedelta(days=7)] = [items0[0]+1, 1, change]
            except Exception:
                None
    
    adj_category_list.remove({})
    return adj_category_list

def linear_correl(x_values, y_values):
        #calculate generic best fit line
        x = x_values
        y = y_values
        z = np.polyfit(x, y, 1)
        z_formatted = np.ndarray.tolist(z)
        p = np.poly1d(z)
        xp = np.linspace(min(x_values), max(x_values), 100) 
        
        #calculate correlation coefficient
        correl_y = p(x)
        #A = np.vstack([x, np.ones(len(x))]).T
        #m, c = np.linalg.lstsq(A, correl_y, rcond=None)[0]
        #print(m, c)
        R = np.corrcoef(y, correl_y)
        cor = R.item(1) #R is a 2x2 matrix so take the correct entry
        #print("\n For:" + str(identifier))

        #print("\nCorrelation coefficient: " + str('%0.2f' % cor))
                   
        #print("\nSuggested polynomial a*x + b has [a, b]: "
        #      + str('%0.2f' % z_formatted[0]) +", "
        #      + str('%0.2f' % z_formatted[1]))# +", "
              #+ str('%0.2f' % z_formatted[2]))                  #+ str('%0.2f' % z_formatted[3]))
        
        #return [correl coeff, ax, b]
       
        return [cor, z_formatted[0], z_formatted[1]]
    
def scatter_graph_correl(x_values, y_values, n_values, identifier):
        #calculate and print best fit line
        x = x_values
        y = y_values
        z = np.polyfit(x, y, 1)
        z_formatted = np.ndarray.tolist(z)
        p = np.poly1d(z)
        xp = np.linspace(min(x_values), max(x_values), 100) 
        
        #calculate correlation coefficient
        correl_y = p(x)
        #A = np.vstack([x, np.ones(len(x))]).T
        #m, c = np.linalg.lstsq(A, correl_y, rcond=None)[0]
        #print(m, c)
        R = np.corrcoef(y, correl_y)
        cor = R.item(1) #R is a 2x2 matrix so take the correct entry
        print("\n For:" + str(identifier))

        print("\nCorrelation coefficient: " + str('%0.2f' % cor))
                   
        print("\nSuggested polynomial a*x + b has [a, b]: "
              + str('%0.2f' % z_formatted[0]) +", "
              + str('%0.2f' % z_formatted[1]))# +", "
              #+ str('%0.2f' % z_formatted[2]))                  #+ str('%0.2f' % z_formatted[3]))

                    
        #Size the output
        fig = plt.figure(dpi=128, figsize=(10,6))
        
        #Chart gridlines
        plt.grid(None, 'major', 'both')
        
        #Axis tick formats
        for tick in plt.gca().get_xticklabels():
            tick.set_fontname("Calibri")
            tick.set_fontsize(12)
            tick.set_rotation('vertical')
        for tick in plt.gca().get_yticklabels():
            tick.set_fontname("Calibri")
            tick.set_fontsize(12)
        
        #Axis labels and formats
        
        # axis 1
        color = 'tab:blue'
        plt.xlabel("Input", fontsize =12)
        #plt.xticks(np.arange(x_values[11], x_values[0], 2))
        plt.ylabel("Output", color='black', fontsize =12)
        plt.scatter(x_values, y_values, color=color)
        plt.plot(xp, p(xp), color = 'red')
        plt.tick_params(axis='y', labelcolor=color)
        
        for i, txt in enumerate(n_values):
            plt.annotate(txt, (x[i], y[i]))
        
                   
        #remove borders
        plt.gca().spines['top'].set_visible(False)
        
        #Chart title
        plt.title(str(identifier), fontsize = 14)
        
        #Show chart
        plt.show()

def weather_correlation(train_date_year, sample_dict, graph_y_or_n):
    """for progress dict returns weekly correlation list of progress vs precip, temp and last week progress [correl coeff, ax, b]"""
   
    category_dict = sample_dict
    
    weather = get_weather("corn")
    precip_dict = dict_unpacker(weather[0])
    temp_dict = dict_unpacker(weather[1])
    
    rolling_precip = rolling_day(7, precip_dict)
    rolling_temp = rolling_day(7, temp_dict)
    
    unique_week_list = []
    week_list = []
    change_list = []
    progress_list = []
    date_list = []
    precip_list = []
    temp_list = []
    
    exception_list = []
    for key, items in category_dict.items():
        try:
            precip_list.append(rolling_precip[key])
            temp_list.append(rolling_temp[key])
            week_list.append(items[0])
            change_list.append(items[2])
            date_list.append(key)
            progress_list.append(items[1])
        except Exception:
            exception_list.append(key)
                    
        if items[0] not in unique_week_list:
            unique_week_list.append(items[0])
    
    print("These dates not found in the weather dictionary: ", exception_list)

    unique_week_list = sorted(unique_week_list)
    correl_dict = {}
    for i in range(len(unique_week_list)):
        p_values, t_values, r_values, y_values, n_values = [], [], [], [], []
        for j in range(len(week_list)):
            #TRAIN DATE LIMIT HAPPENS HERE
            if unique_week_list[i] == week_list[j] and date_list[j].year <= train_date_year:
                y_values.append(change_list[j])
                p_values.append(precip_list[j])
                t_values.append(temp_list[j])
                n_values.append(str(date_list[j]).replace(" 00:00:00",""))
                r_values.append(1 - float(progress_list[j]) + float(change_list[j]))

        if n_values != []:
            #if you want graphs == y
            if graph_y_or_n == 'y':
                identifier1 = "Week "+ str(unique_week_list[i]) + ", precip"
                identifier2 = "Week "+ str(unique_week_list[i]) + ", temp"
                identifier3 = "Week "+ str(unique_week_list[i]) + ", amount left"
                
                scatter_graph_correl(p_values, y_values, n_values, identifier1)
                scatter_graph_correl(t_values, y_values, n_values, identifier2)
                scatter_graph_correl(r_values, y_values, n_values, identifier3)
            #otherwise make the correl dict
            else:
                correl_list = [linear_correl(p_values, y_values),
                               linear_correl(t_values, y_values),
                               linear_correl(r_values, y_values)]
                correl_dict[int(unique_week_list[i])] = correl_list
    
    return correl_dict


def corn_weather_correls(train_date_year, category_dict):
    season_list = []
    season_type = weather_correlation(train_date_year, category_dict, 'n') #'n'no graphs
    season_list.append(season_type)
    
    #saving as a list meerley son json.dump will work
    with open('season_correlation.txt','w') as f:
        json.dump(season_list,f)
    
   
    correl_dict = season_list[0]

    weather = get_weather("corn")
    precip_dict = dict_unpacker(weather[0])
    temp_dict = dict_unpacker(weather[1])
    
    rolling_precip = rolling_day(7, precip_dict)
    rolling_temp = rolling_day(7, temp_dict)

    #category_dict = detail_analyse_progress(progress_dict)
    remaining_dict = {}
    exception_list = []
    
    #category dict is date : [week, progress, progress chg]
    #this gets the remaining_dict i.e. for the week before how much planting was left
    for key, items in category_dict.items():
        try:
            key = date_to_datetime(key)
            remaining_dict[key] = (1 - float(items[1]) + float(items[2]))

        except Exception:
            exception_list.append(key)
    
    #-------------- START get forecast definition START----------------
    #need input item = [week, date, precip, temp, remaining, forecast progress_chg]
    def get_item(year, week):
        item_date = date_from_isoweek(year,week,7)
        item_date_next = date_from_isoweek(year,week+1,7)
        
        try:
            item_precip = rolling_precip[item_date]
        except Exception:
            item_precip = 'precip_error'
        
        try:
            item_temp = rolling_temp[item_date]
        except Exception:
            item_temp = 'temp_error'
            
        #need to fix item remaining to tie in with forecast
        try:
            item_remaining = remaining_dict[item_date]
        except Exception:
            item_remaining = 'remaining_error'

        
        input_list = [item_precip, item_temp, item_remaining]
        
        key_list = []
        for key in correl_dict.keys():
            key_list.append(key)
        max_correl_no = str(max(key_list))
        used_correl_week = min([str(week),max_correl_no])

        correl_list = correl_dict[int(used_correl_week)]#need the int
        #for reference this is the correl list, linear_correl = [coeff, ax, b]
        #correl_list = [linear_correl(p_values, y_values),
        #       linear_correl(t_values, y_values),
        #       linear_correl(r_values, y_values)]

        coeff_sum = 0
        total_weighted_forecast = 0
        for i in range(len(input_list)):
            #print(input_list, correl_list)
            forecast = correl_list[i][1] * input_list[i] + correl_list[i][2]
            coeff = correl_list[i][0]
            try:
                coeff_sum = coeff_sum + coeff
                weighted_forecast = forecast * coeff
                total_weighted_forecast += weighted_forecast
            except Exception:
                coeff_sum = 3
                weighted_forecast = forecast
                total_weighted_forecast += weighted_forecast
        
        forecast_progress_chg = total_weighted_forecast / coeff_sum
       
        #for when the forecast has no remaining already
        try:
            next_remaining_check = remaining_dict[item_date_next] #testing for error in next remaining amount
        except Exception:
            remaining_dict[item_date_next] = item_remaining + forecast_progress_chg
        
        return [week, item_date, item_precip, item_temp, item_remaining, forecast_progress_chg]
        #--------------END get forecast definition END ----------------
    
    year_list = []
    week_list = []
    
    #find the weeks and years in the category dict and the max/mins
    for key in category_dict:
        #formattedas_date = datetime.strptime(str(key), "%Y-%m-%d")
        formattedas_date = key
        week = formattedas_date.strftime("%V")
        if formattedas_date.year not in year_list:
            year_list.append(int(formattedas_date.year))
        if week not in week_list:
            week_list.append(int(week))
    
    #to ensure this year is in the list
    this_year = datetime.today().year
    if this_year not in year_list:
        year_list.append(this_year) 
    
    max_year = max(year_list)
    min_year = min(year_list)
    max_week = max(week_list)
    min_week = min(week_list)
    
    #find the forecast chg for those weeks and years in the category dict and add cum forecast
    forecast_dict = {}
    for i in range(min_year,max_year+1):
        cum_forecast = 0
        for j in range(min_week, max_week+1):
            try:
                item = get_item(i,j)
                add = abs(float(item[5])) #abs because later readings provide big -ves as it uses the correlation all the way
                if str(add) == 'nan':
                    add = 0
                cum_forecast += add
                item.append(min([cum_forecast,1])) #this is needed to cap forecast progress at 100%
                forecast_dict[item[1]] = item
            except Exception:
                None
   
   
    output_dict = {}
    for key, items in forecast_dict.items():
        output_dict[key] = items[6]
    
    
    forecast_key_list = []
    for key in forecast_dict.keys():
        forecast_key_list.append(key)
    
    for i in range(min_year,max_year+1):
        for j in range(1,53):
            output_key = date_from_isoweek(i,j,7)  #- timedelta(days=1)
            if output_key not in forecast_key_list and j < min_week:
                output_dict[output_key] = 0
            elif output_key not in forecast_key_list and j > max_week:
                output_dict[output_key] = 1
            elif output_key not in forecast_key_list:
                output_dict[output_key] = 0 # this fills any errors with zeros, consider removing
    
    #sort output dict for convenience
    sorted_output_dict = {}
    sorted_list = []
    for key in output_dict.keys():
        sorted_list.append(key)

    sorted_list = sorted(sorted_list)
    for key in sorted_list:        
        sorted_output_dict[key] = output_dict[key]
    #print(output_dict)
    return sorted_output_dict
         

if __name__ == '__main__':
    
    def test_one_category():
        progress_dict = get_from_xls()
        category_dict = detail_analyse_progress(progress_dict)
        #gets a list of dicts with each stage's data e.g. harvest [week, absolute progress, change]
        
      
        progress_forecast = corn_weather_correls(2016, category_dict[0])
        
        key_list = []
        for key in progress_forecast.keys():
            key_list.append(key)
        
        adj_key_list = sorted(key_list)
        for key in adj_key_list:
            try:
                None
                print(key, progress_forecast[key])
            except Exception:
                None
    
    #test_one_category()


    def put_it_together():
        progress_dict = get_from_xls()
        category_dict = detail_analyse_progress(progress_dict)
        #gets a list of dicts with each stage's data e.g. harvest [week, absolute progress, change]

        #get max weather date
        weather = get_weather("corn")
        precip_dict = dict_unpacker(weather[0])
        precip_list = []
        for key in precip_dict.keys():
            precip_list.append(key)
        precip_list = sorted(precip_list)
        max_date = precip_list[len(precip_list)-1]
        print(max_date)
        
        progress_list = []
        
        for item in category_dict:
            progress_forecast = corn_weather_correls(2016, item)
            progress_list.append(progress_forecast)
        
        overall_progress_dict = {}
    
        for key in progress_list[0].keys():
            try:
                add_list = []
                for j in range(0,len(progress_list)): #this was 1
                    if key.year > 1980:
                        add_list.append(progress_list[j][key])
                
                season_weighter = [2,1,1,1,1,1,2]
                weighted_avg = 0
                for i in range(0,len(add_list)):
                    plus = season_weighter[i] * add_list[i]
                    weighted_avg += plus
                weighted_avg = weighted_avg / len(add_list)
                
                if key <= max_date:
               
                    overall_progress_dict[str(key).replace(" 00:00:00",'')] = weighted_avg #statistics.mean(add_list)#[statistics.mean(add_list), add_list] #keep for debugging purposes to see all components
            except Exception:
                None
        
        #print(overall_progress_dict)

        key_list = []
        for key in overall_progress_dict.keys():
            key_list.append(key)
        
        adj_key_list = sorted(key_list)
        for key in adj_key_list:
            try:
                None
                print(key, overall_progress_dict[key])
            except Exception:
                None
        
        progress_dest = (r"C:\Users\thoma\Desktop\Python\TH Projects\Port\alpha\corn\corn_crop_forecast_time_series_dict.txt")
        with open(progress_dest, 'w') as f:
            json.dump(overall_progress_dict,f)
        
    
    put_it_together()    
        
        
    
    
    
    
