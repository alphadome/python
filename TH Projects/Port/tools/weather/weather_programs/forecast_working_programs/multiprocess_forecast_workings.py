# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 15:14:18 2019

@author: thoma
"""
import sys
import_list = [
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools",
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\general\scraper",
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs",        
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\geo"        
        ]
for import_location in import_list:
    if import_location not in sys.path:
        sys.path.append(import_location)


from weather_tools import text_between, coordinate_distance, find_lat_lon
from scraper import scraper
import json
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from random import randint
from geolocation import geolocation

import multiprocessing
import time


class Consumer(multiprocessing.Process):
    
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                print('%s: Exiting' % proc_name)
                self.task_queue.task_done()
                break
            print('%s: %s' % (proc_name, next_task))
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)
        return


class Task(object):
    def __init__(self, url, address):
        self.url = url
        self.address = address
    def __call__(self):
        try:
            location = geolocation(self.address)
            lat = location[0]
            lon = location[1]
            answer = [self.url, lat, lon, self.address]
            print(answer)

        except Exception as error:
            print(error)
            answer = [self.url, 'fail', 'fail', self.address]
            print(answer)

        return answer
    def __str__(self):
        return self.url


if __name__ == '__main__':
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    
    # Start consumers
    num_consumers = multiprocessing.cpu_count() * 1
    print('Creating %d consumers' % num_consumers)

    consumers = [ Consumer(tasks, results)
              for i in range(num_consumers) ]
    
    for w in consumers:
        w.start()
    
    # Enqueue jobs
    processed_forecast_location = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs\forecast_working_files\processed_forecast_location.txt'
    with open(processed_forecast_location) as f:
        local_dict = json.load(f)
        print(" dict loaded")
    #local_dict = {'url':'London, UK'}
    
  
    total_no = 0
    for key in local_dict.keys():
        total_no += 1   
    fixed_total_no = total_no
    t0 = time.perf_counter()


    for key, items in local_dict.items():
        address_raw = items.split(',')
        location = address_raw[0].strip()
        state = address_raw[1].strip()
        country = address_raw[2].strip()
        address = [location, '', state, country]
        url = key
        tasks.put(Task(url, address))
    
    # Add a poison pill for each consumer
    for i in range(num_consumers):
        tasks.put(None)

    # Wait for all of the tasks to finish
    tasks.join()
    
    location_dict = {}
    reject_dict = {}
    success = 0
    failures = 0
    # Start printing results
    while total_no:
        result = results.get()
        t2 = time.perf_counter()
        print(result)
        url = result[0]
        lat = result[1]
        lon = result[2]
        location = result[3]
        
        if lat == 'fail':
            #choice = randint(0,len(proxy_list)-1)
            #random_proxy = proxy_list[choice]
            #tasks.put(Task(url, location, random_proxy))
            reject_dict[url] = location
            failures += 1
        else:
            location_dict[url] = [lat, lon, location]
            success +=1
        
        total_no -= 1
        done_no = fixed_total_no - total_no
        t1 = time.perf_counter()
        time_taken = t1 - t0
        time_prediction = ((time_taken) * (fixed_total_no / done_no) - t1)/3600
        print("On #" +str(done_no) + "/" + str(fixed_total_no) +" - estimated time to completion in hours is " +str(time_prediction) + "and the last opeation took " + str(t1 - t2))


    file1 = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs\forecast_working_files\forecast_location.txt'
    file2 = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs\forecast_working_files\reject_location.txt'
    
        
    with open(file1, 'w') as f:
        json.dump(location_dict, f)
    
    with open(file2, 'w') as f:
        json.dump(reject_dict, f)        

