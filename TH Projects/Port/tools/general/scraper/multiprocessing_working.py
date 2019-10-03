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

from scraper import set_up as bulk_scrape
import json
import multiprocessing
import time
from random import randint


scrape_location =  r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\general\scraper\bulk_scrape"

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
            r = bulk_scrape(self.url, self.proxy_ip)
            filename = scrape_location + str('\\') + str(self.url).replace('/','_').replace('.','-').replace(':','&') +str('.txt')
            with open(filename, 'w') as f:
                json.dump(r.text, f)
            answer = self.url
        except Exception:
            print("Error in desired txt filename")
            answer = 'fail'
        return answer
    def __str__(self):
        return self.url


if __name__ == '__main__':
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    
    # Enqueue jobs
    url_list = ["https://www.yahoo.com/", "https://www.apple.com/"]
    proxy_list = ["36.90.104.220:8080", "129.157.226.237:3128"]
    local_proxy_list = []
    for proxy in proxy_list:
        local_proxy_list.append(proxy)
    job_limit = min([len(url_list), len(proxy_list)])
    
    for i in range(job_limit):
        choice = randint(0,len(local_proxy_list)-1)
        random_proxy = local_proxy_list[choice]
        local_proxy_list.remove(random_proxy)
        #put the tasks in the queue
        tasks.put(Task(url_list[i], random_proxy))
    
    
    # Start consumers
    num_consumers = multiprocessing.cpu_count() * 2
    print('Creating %d consumers' % num_consumers)
    consumers = [ Consumer(tasks, results)
                  for i in range(num_consumers) ]
    for w in consumers:
        w.start()
        
    # Add a poison pill for each consumer
    for i in range(num_consumers):
        tasks.put(None)

    # Start printing results
    results_record = []
    while url_list:
        result = results.get()
        results_record.append(result)
        print('Result:', result)
        try:
            url_list.remove(result)
        except Exception:
            None
    
    time.sleep(60)    
    for w in consumers:
        w.terminate()

    print("These urls were successes: " + str(results_record))
    print("These urls were failures: " + str(url_list))    
    
    # Wait for all of the tasks to finish
    tasks.join()

    
