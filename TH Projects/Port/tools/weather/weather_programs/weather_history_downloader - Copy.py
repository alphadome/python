# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 22:24:46 2019

@author: thoma
"""
import sys
import_list = [
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools",
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs",        
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\geo"
        ]
for import_location in import_list:
    if import_location not in sys.path:
        sys.path.append(import_location)

from datetime import date, datetime, timedelta
import json
from math import sin, cos, sqrt, atan2, radians
from geopy.geocoders import Nominatim
from geolocation import geolocation
from weather_tools import join_dicts
import tarfile
import re
       

def weather_profile(address, name, data='', update=''):
    """Store a profile in the file so we do not repeat every action"""
    filename = str(r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_profiles/" + str(address) + "_weather_profile_history.txt")
    filename_temp = str(r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_profiles/" + str(address) + "_weather_profile_history_backup.txt")

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

def coordinate_distance(lat1,lon1,lat2,lon2):
    # approximate radius of earth in km
    R = 6373.0
    
    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))
    lat2 = radians(float(lat2))
    lon2 = radians(float(lon2))
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance = R * c
    return float(distance)


def coordinate_distance_test():
    print(coordinate_distance("52.2296756", "21.0122287", "52.406374", "16.9251681"))
    print("Should be:", 278.546, "km")


def process_noaa_list():
    filename = r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_databases\databases\ghcnd-inventory.txt"
    
    station_list = []
    with open(filename) as f:
        contents = f.read()
    
    for i in range(round(len(contents)/46)):
        line = contents[i*46:i*46+46]
        station_code = str(contents[i*46:i*46+11])

        latitude = float(str(contents[i*46+11:i*46+20]).replace(" ",""))
        longitude = float(str(contents[i*46+20:i*46+30]).replace(" ",""))
        weather_type = str(str(contents[i*46+30:i*46+35]).replace(" ",""))[0:4] 
        start_date = float(str(contents[i*46+35:i*46+40]).replace(" ",""))    
        end_date = float(str(contents[i*46+40:i*46+46]).replace(" ",""))
#        if station_code == "USC00134101":
#            print(station_code, weather_type, start_date, end_date, date.today().year)
#            if float(end_date) > float(date.today().year) -1 and float(start_date) < float(date.today().year) -7:
#                print("confirm")
        if float(end_date) > float(date.today().year) -1 and float(start_date) < float(date.today().year) -7:
            if weather_type == "PRCP" or weather_type == "TAVG":
                station = []    
                station.append(station_code)
                station.append(latitude)
                station.append(longitude)
                station.append(weather_type)
                station.append(start_date)
                station.append(end_date)
                station_list.append(station)
#                if station_code == "USC00134101":
#                    print(station)
    
   
    new_filename = r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_databases\ghcnd-inventory_processed.txt"
    with open(new_filename,'w') as f:
        json.dump(station_list, f)
    print("NOAA raw contents processed")

def find_nearest_noaa_station(address, weather_type):
    location = geolocation(address)
    lat1 = location[0]
    lon1 = location[1]
    
    if weather_type == "T":
        weather_type = "TAVG"
    elif weather_type == "P":
        weather_type = "PRCP"
    else:
        print("weather type argument spelt wrong - P or T")

    filename = r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_databases\ghcnd-inventory_processed.txt"
    with open(filename) as f:
        station_list = json.load(f)
    adj_station_list = []
    for i in range(len(station_list)):
        if str(station_list[i][3]) == str(weather_type):
            adj_station_list.append(station_list[i])
        else:
            None
    
    if len(adj_station_list) == 0:
        print("weather type argument spelt wrong - P or T")

    distance_dict = {}
    for i in range(len(adj_station_list)):
        station = adj_station_list[i]
        station_code = station[0]
        lat2 = station[1]
        lon2 = station[2]
        key = coordinate_distance(lat1,lon1,lat2,lon2)
        distance_dict[key] = station_code
    
    sorted_locations = []
    for key in distance_dict.keys():
        sorted_locations.append(float(key))
    sorted_locations = sorted(sorted_locations)
    
    eligible_dict = {}
    for key in sorted_locations[:30]:
        eligible_dict[key] = distance_dict[key]
    
    return eligible_dict


def get_noaa_dict(station_code, weather_type):
    #tar = tarfile.open(r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_databases\databases\ghcnd_all.tar.gz")
    
    #found = False
    #for tarinfo in tar:
    #    if found == False:
    #        if str(station_code) in str(tarinfo.name):
    #            print('Found')
    #            found = True
    #            f = tar.extractfile(tarinfo)
    #            content = f.read()
    #    else:
    #        break
                
    #tar.close()
    
    filename = r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_databases\databases\ghcnd_all\\" + str(station_code) + ".dly"
    with open(filename) as f:
        content = f.read()
    
    lines = str(content).split("\n")
    data = []
    for line in lines:
        item = []
        new = str(line).split(" ")
        date_type = str(new[0]).replace(str(station_code),'')
        weather_date = date_type[:6]
        weather_id = date_type[6:10]
        item.append(weather_date)
        item.append(weather_id)
        for i in range(1,len(new)):
            nos = re.findall(r'-?\d+', new[i])
            for no in nos:
                item.append(no)
        data.append(item)
    
    print(data)
    weather_dict = {}
    
    if weather_type == "T":
        record = "TAVG"
    elif weather_type == "P":
        record = "PRCP"
    else:
        record = ''
    
    for line in data:
        if line[1] == record:
            year = str(line[0])[0:4]
            month = str(line[0])[4:6]
            for i in range(2,len(line)):
                item = float(line[i]) * 0.1

                day = i-1
                try:
                    weather_date = str(date(int(year), int(month), int(day)))
                    if int(item) != int(-999.9):
                        weather_dict[weather_date] = float("%0.1f" % item)
                except Exception:
                    None
                    #print(line)
                
    return weather_dict

get_noaa_dict("USR0000INEA", "T")
#print(get_noaa_dict("USC00139750", "P"))


def process_ecad_list(filename, processed_filename):
    with open(filename) as f:
        contents = f.read()
    
    start_no = int(contents.index(",PARNAME"))
    #print(contents[start_no + 8:10000])
    if contents[start_no+1:start_no+8] == "PARNAME":
        None
    else:
        print("Reanalyse where the data starts in process_ecad_list")
    
    station_list = []
    data_list = contents[start_no + 8:len(contents)].replace(" ","").replace("\n\n","\n").split('\n')
    
    data = []
    for item in data_list:
        if item == '':
            data_list.remove(item)
        else:
            line = item.split(',')
            data.append(line)

    for i in range(len(data)):
        try:
            line = data[i]
            station_code = line[0]
            location_name = line[2]
            country_code = line[3]
            lat_raw = str(line[4])
            lon_raw = str(line[5])
            weather_type = line[7]
            weather_type = weather_type[0:2] #keep first letter as there are many subcategories
            #https://www.ecad.eu//dailydata/datadictionaryelement.php for weather type
            start_date_raw = line[8]
            end_date_raw = line[9]
            
            lat_list = lat_raw[0:len(lat_raw)].split(':')
            lat = float(lat_list[0]) + float(lat_list[1])/60 + float(lat_list[2])/3600
    
            lon_list = lon_raw[0:len(lon_raw)].split(':')
            lon = float(lon_list[0]) + float(lon_list[1])/60 + float(lon_list[2])/3600
            
            start_date = float(start_date_raw[:4])
            end_date = float(end_date_raw[:4])
            station = [station_code, location_name, country_code, lat, lon, weather_type, start_date, end_date]
            year = date.today().year
            if float(end_date) > float(year-1) and float(start_date) < float(year-7):
                #print(station)
                station_list.append(station)

        except Exception:
            None

    new_filename = str(processed_filename)
    with open(new_filename,'w') as f:
        json.dump(station_list, f)


def find_nearest_ecad_station(address, weather_type):
    location = geolocation(address)
    lat1 = location[0]
    lon1 = location[1]
    
    if weather_type == "T":
        filename = r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_databases\ECA_blend_tg_processed.txt"
        weather_type = "TG"
    elif weather_type =="P":
        filename = r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_databases\ECA_blend_rr_processed.txt"
        weather_type = "RR"
    with open(filename) as f:
        station_list = json.load(f)
    
    adj_station_list = []
    for i in range(len(station_list)):
        if str(station_list[i][5]) == str(weather_type):
            adj_station_list.append(station_list[i])
        else:
            None
    if len(adj_station_list) == 0:
        print("weather type argument spelt wrong - TG or RR")

    distance_dict = {}
    for i in range(len(adj_station_list)):
        station = adj_station_list[i]
        station_code = station[0]
        location_name = station[1]
        lat2 = station[3]
        lon2 = station[4]
        key = coordinate_distance(lat1,lon1,lat2,lon2)
        distance_dict[key] = [station_code, location_name]
    
    sorted_locations = []
    for key in distance_dict.keys():
        sorted_locations.append(float(key))
    sorted_locations = sorted(sorted_locations)
    
    eligible_dict = {}
    for key in sorted_locations[:30]:
        eligible_dict[key] = distance_dict[key]
    
    return eligible_dict   
#print(find_nearest_ecad_station(["", "", "London", "UK"],"T"))
#print(find_nearest_noaa_station(["","","London","UK"],"T"))

def update_stations():
    """only do this occasionally"""
    process_noaa_list()
    #ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/
    process_ecad_list(r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_databases\databases\ECA_blend_tg\sources.txt", r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_databases\ECA_blend_tg_processed.txt")
    process_ecad_list(r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_databases\databases\ECA_blend_rr\sources.txt", r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_databases\ECA_blend_rr_processed.txt")


def get_ecad_file_location(station_info, weather_type):

    station_code = station_info[0] 
    station_distance = station_info[1]
    database = station_info[2]
    
    zeros_needed = 6 - len(station_code)
    zeros_string = ""
    for i in range(zeros_needed):
        zeros_string = zeros_string + str("0")
    
    code = str(zeros_string) + str(station_code)
    
    if weather_type == "T":
        filename = str(r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_databases\databases\ECA_blend_tg\TG_STAID" + str(code) + ".txt")
    elif weather_type =="P":
        filename = str(r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_databases\databases\ECA_blend_rr\RR_STAID" + str(code) + ".txt")
    
    return [str(filename), float(station_distance), station_code]
    
#get_ecad_file_location("London","T")

def get_ecad_dict(station_info, weather_type):
    
    station = get_ecad_file_location(station_info, weather_type)
    filename = station[0]
    station_code = station[2]
    
    with open(filename) as f:
        contents = f.read()
    lines = contents.split("\n")
    weather_dict = {}
    for line in lines:
        data = line.replace(" ","").split(",")
        if data[0] == station_code:
            try:
                date_code = data[2]
                year = date_code[0:4]
                month = date_code[4:6]
                day = date_code[6:8]
                weather_date = str(date(int(year), int(month), int(day)))
                weather_data = float("%0.1f" % (float(data[3]) * 0.1))
    
                if int(weather_data) == int(-999.9):
                    None
                else:                     
                    weather_dict[weather_date] = weather_data
            
            except Exception:
                None

    return weather_dict


def find_nearest_station(address, weather_type, update=''):
    """returns station code and best location"""

    def proceed_with_method():    
        noaa_dict = find_nearest_noaa_station(address, weather_type)
        ecad_dict = find_nearest_ecad_station(address, weather_type) 
        
        total_dict = join_dicts(noaa_dict, ecad_dict)
        location_list = []
        for key in total_dict.keys():
            location_list.append(key)
        location_list = sorted(location_list)
        station_info = 'Error in finding nearest station'
        for i in range(len(location_list)):
            best_location = location_list[i]
            try:
                try:
                    station_code = noaa_dict[best_location]
                    database = "NOAA"
                    station_info = [station_code, best_location, database, weather_type]
                    weather_dict = get_noaa_dict(station_code, weather_type)
                    weather_dates = []
                    for key in weather_dict.keys():
                        formattedas_date = datetime.strptime(str(key), "%Y-%m-%d")
                        weather_dates.append(formattedas_date)
                    
                    #this is to wean out weather stations that return non consistent data
                    today = date.today()
                    for i in range(int(today.year - 15), int(today.year)):
                        date_list = []
                        for weather_date in weather_dates:
                            if int(weather_date.year) == int(i) and weather_date not in date_list:
                                date_list.append(weather_date)
                        if len(date_list) < 330:
                            station_info = 'Error in finding nearest station'
                            break
               
                except Exception:
                    code = ecad_dict[best_location]
                    code = code[0]
                    database = "ECAD"
                    station_info = [code, best_location, database, weather_type]
                    station_code = station_info[0]
                    weather_dict = get_ecad_dict(station_info, weather_type)
        
                    weather_dates = []
                    for key in weather_dict.keys():
                        formattedas_date = datetime.strptime(key, "%Y-%m-%d")
                        weather_dates.append(formattedas_date)
                    #print(weather_dates)
                    #this is to wean out weather stations that return non consistent data
                    today = date.today()
                    for i in range(int(today.year - 15), int(today.year)):
                        date_list = []
                        for weather_date in weather_dates:
                            if int(weather_date.year) == int(i) and weather_date not in date_list:
                                date_list.append(weather_date)
                        if len(date_list) < 330:
                            station_info = 'Error in finding nearest station'
                            break
                
            except Exception:
                print('Error')
            
                                  
            finally:
                if station_info != 'Error in finding nearest station':
                    break

        return station_info

    title = "nearest_station_" + str(weather_type)
    if weather_profile(address, title) == None or update:
        print("/t-Adding/refreshing data...")
        data = proceed_with_method()
        weather_profile(address, title, data, update)
        return weather_profile(address, title)

    else:
        return weather_profile(address, title)

#print(find_nearest_station(["", "", "Iowa", "US"], "P", 'update'))
#print(find_nearest_station("Iowa","T"))        

def historic_weather_data(address, weather_type, update=''):
    """returns weather dict, weather_type can be either T or P"""
    def proceed_with_method():
        station_info = find_nearest_station(address, weather_type, update)
        station_code = station_info[0]
        database = station_info[2]
        
        if database == "NOAA":
            weather_dict = get_noaa_dict(station_code, weather_type)
        elif database == "ECAD":
            weather_dict = get_ecad_dict(station_info, weather_type)
        
        return weather_dict
        
    title = "weather_dict_" + str(weather_type)
    if weather_profile(address, title) == None or update != '':
        print("/t-Adding/refreshing data...")
        data = proceed_with_method()
        weather_profile(address, title, data, update)
        return weather_profile(address, title)

    else:
        return weather_profile(address, title) 
    
#print(historic_weather_data("London", "T"))    
#print(historic_weather_data("London", "P"))    

   
