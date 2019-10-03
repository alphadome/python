# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 08:49:33 2019

@author: thoma
"""
import sys
import_list = [
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools",
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\general\scraper",
        ]
for import_location in import_list:
    if import_location not in sys.path:
        sys.path.append(import_location)

from scraper import set_up, generate_https_proxy_list
import json
import multiprocessing
import time
from random import randint
from time_restriction import time_restricted


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
    def __init__(self, url, proxy_ip):
        self.url = url
        self.proxy_ip = proxy_ip
    def __call__(self):
        try:
            r = time_restricted(10,set_up, self.url, self.proxy_ip)
            if r.status_code == 200:
                answer = self.proxy_ip
            else:
                Exception
                answer = 'fail'
        except Exception:
            print("Proxy fails")
            answer = 'fail'
        return answer
    def __str__(self):
        return self.proxy_ip


def bulk_test(proxy_list):

    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    
    # Enqueue jobs
    test_url = "https://www.yahoo.com/"
    
    local_proxy_list = []
    for proxy in proxy_list:
        local_proxy_list.append(proxy)
    
    num_jobs = len(proxy_list)
    for i in range(len(proxy_list)):
        choice = randint(0,len(local_proxy_list)-1)
        random_proxy = local_proxy_list[choice]
        local_proxy_list.remove(random_proxy)
        #put the tasks in the queue
        tasks.put(Task(test_url, random_proxy))
    
    
    # Start consumers
    num_consumers = multiprocessing.cpu_count() * 5
    print('Creating %d consumers' % num_consumers)
    consumers = [ Consumer(tasks, results)
                  for i in range(num_consumers) ]
    for w in consumers:
        w.daemon = True
        
    for w in consumers:
        w.start()
        
    # Add a poison pill for each consumer
    for i in range(num_consumers):
        tasks.put(None)

    # Start printing results
    results_record = []
    
    while num_jobs:
        result = results.get()
        if result != 'fail':
            results_record.append(result)
        num_jobs -= 1
    
#    t0 = time.perf_counter()
#    t1 = t0 + 30*1   # 1 minutes from now

#    while time.perf_counter() < t1:
#        try:
#            result = results.get()
#        except Exception:
#            result = "fail"
#        print('Result:', result)
#        print('stalling line 112')
#        if result != 'fail':
#            print('stalling line 114')
#            results_record.append(result)
#        try:
#            print('stalling line 117')
#            proxy_list.remove(result)
#        except Exception:
#            print('stalling line 121')
#        
#        if time.perf_counter() > t1:
#            break

    
    print("--------------------------------STARTING SLEEP---------------------------------")
    
    while not results.empty():
        results.get()
    
    while not tasks.empty():
        tasks.get()    

    for w in consumers:
        w.join(1)    
    for w in consumers:
        w.terminate()
    for w in consumers:
        w.join(1)
    for w in consumers:
        print('TERMINATED:', w, w.is_alive())

   
    print("These " + str(len(results_record)) + " out of " + str(len(proxy_list)) + " proxy ips were successes: " + str(results_record))
    
    # Wait for all of the tasks to finish

    return results_record



        
if __name__ == '__main__':
    count = 1
    successes = 0
    while True:
        print("STARTING BULK IP TEST: " + str(count))
        new_untested_list = []
        while new_untested_list == []:
            new_untested_list = generate_https_proxy_list()
        
        untested_proxy_file = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\general\scraper\untested_proxy_file.txt'
        with open(untested_proxy_file) as f:
            proxy_list = json.load(f)
        results = bulk_test(proxy_list)
        print("received results")
        tested_proxy_file = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\general\scraper\tested_proxy_file.txt'
        try:
            with open(tested_proxy_file) as f:
                existing_list = json.load(f)
        except Exception:
            existing_list = []
        
        duplicates = []
        for proxy in results:
            if proxy in existing_list:
                duplicates.append(proxy)
            if proxy not in existing_list:
                existing_list.append(proxy)
        
        print("These: " + str(duplicates) + " were duplicates.")
        
    
        with open(tested_proxy_file, 'w') as f:
            json.dump(existing_list, f)    
        successes = len(results) - len(duplicates) + successes
        print("BULK IP TEST: " + str(count) + " COMPLETED")
        print("Total of " + str(successes) + " successes to date")
        count = count + 1

        time.sleep(40*1)


    
