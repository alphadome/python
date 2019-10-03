# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 14:57:31 2019

@author: thoma
"""

from weather_history_downloader import historic_weather_data
from weather_forecast_downloader import get_weather_forecast
import statistics
import json

def weather_profile(address, name, data='', update=''):
    """Store a profile in the file so we do not repeat every action"""
    filename = str(r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_profiles/" + str(address) + "_weather_profile.txt")
    filename_temp = str(r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_profiles/" + str(address) + "_weather_profile_backup.txt")

    #open as write - this takes care of the initial instance of the file
    # if we can read the profile read it, otherwise create an empty dict

    try:
        with open(filename) as f:
            contents = json.load(f)
        
        weather_profile_dict = contents
        
        #create backup file in case something goes wrong
        with open(filename_temp, 'w') as f:
            contents = weather_profile_dict
            json.dump(weather_profile_dict, f)

    except FileNotFoundError:
        weather_profile_dict = {}

    except ValueError:
        print("dictionary has a value error")
        weather_profile_dict = {}
             
    # if there is an existing entry:     
    if name in weather_profile_dict.keys():
        if update:
            del weather_profile_dict[name]
            weather_profile_dict[name] = data
            # store the amended profile          
            with open(filename, 'w') as f:
                json.dump(weather_profile_dict,f)
            return weather_profile_dict[name]
        else:
            return weather_profile_dict[name]
    
    # if there isn't an existing entry
    else:
        if data:
            # create a new one if there is data
            weather_profile_dict[name] = data
            # store the amended profile          
            with open(filename, 'w') as f:
                json.dump(weather_profile_dict,f)
            return weather_profile_dict[name]

        else:
            # return nothing if there isn't
            print("t/-There is no existing data for " + str(name) + " - add data...")
            return None


def join_historic_forecast(historic_dict, forecast_dict):
    """Tie up forecast and historic dicts and offer discrepancy amount for checking purposes"""
    combined_dict = historic_dict
    discrepancy_list = []
    for key, item in forecast_dict.items():
        if key in combined_dict.keys():
            discrepancy = float(combined_dict[key]) - float(forecast_dict[key])
            discrepancy_list.append(discrepancy)
        else:
            combined_dict[key] = float(item)
    try:
        error = statistics.mean(discrepancy_list)
    except Exception:
        error = "better check"

    print("History and forecast tied up with error: " + str(error))
    return combined_dict

def adj_join_historic_forecast(historic_dict, forecast_dict):
    """Tie up forecast and historic dicts and offer discrepancy amount for checking purposes"""
    combined_dict = historic_dict
    discrepancy_list = []
    for key, item in forecast_dict.items():
        if key in combined_dict.keys():
            discrepancy = float(combined_dict[key]) - float(forecast_dict[key])
            discrepancy_list.append(discrepancy)
        else:
            None
    try:
        if discrepancy_list == []:
            error = 0
        else:
            error = statistics.mean(discrepancy_list)
    except Exception:
        error = "better check"
        #print(discrepancy_list, historic_dict, forecast_dict)
   
    for key, item in forecast_dict.items():
        if key in combined_dict.keys():
            None
        else:
            combined_dict[key] = float(item) + float(error)


    print("History and forecast tied up with error: " + str(error))    
    return combined_dict

def get_weather(address, update = ''):
    """get joint forecast and historic data, update = forecast or update"""
    
    def proceed_with_method():
        if update == 'forecast':
            precip_hist_dict = historic_weather_data(address, "P")
            temp_hist_dict = historic_weather_data(address, "T")       
        else:
            precip_hist_dict = historic_weather_data(address, "P", update)
            temp_hist_dict = historic_weather_data(address, "T", update)         
        
        if update == 'history':
            forecast_dict = get_weather_forecast(address)
        else:
            forecast_dict = get_weather_forecast(address, update)

        
        precip_forecast_dict = {}
        temp_forecast_dict = {}
        for key, item in forecast_dict.items():
            precip_forecast_dict[key] = item[1]
            temp_forecast_dict[key] = item[0]
        
        precip_dict = join_historic_forecast(precip_hist_dict, precip_forecast_dict)
        #use adj join for temp, forecast is not accurate, this at least gives a shape
        temp_dict = adj_join_historic_forecast(temp_hist_dict, temp_forecast_dict)
        return [precip_dict, temp_dict]
        
    title = "weather_dict_temp"
    if weather_profile(address, title) == None or update != '':
        print("/t-Adding/refreshing data...")
        data = proceed_with_method()
        weather_profile(address, title, data[1], update)
    else:
        print("There is existing data for: " + str(title))
        
    title = "weather_dict_precip"
    if weather_profile(address, title) == None or update != '':
        print("/t-Adding/refreshing data...")
        data = proceed_with_method()
        weather_profile(address, title, data[0], update)
        return [weather_profile(address, title),weather_profile(address, "weather_dict_temp")]
    else:
        return [weather_profile(address, title),weather_profile(address, "weather_dict_temp")]
        print("There is existing data for: " + str(title))            
            
#get_weather("Iowa")