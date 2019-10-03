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

from scraper import set_up
import json
import multiprocessing
import time
from random import randint


scrape_location =  r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\general\scraper\bulk_scrape"

def code_url(url):
    reserved_list = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', '.', '%', ' ']
    raw_named_list = ['lt', 'gt', 'co', 'qu', 'bs', 'fs', 'sl', 'qm', 'as', 'pb', 'pc', 'sp']
    named_list = []
    for name in raw_named_list:
        named_list.append(str("TH-")+str(name))
    
    coded_url = url
    for i in range(len(reserved_list)-1):
        symbol = reserved_list[i]
        if symbol in url:
            coded_url = coded_url.replace(symbol, named_list[i])
    
    return coded_url
    
def decode_url(url):
    reserved_list = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', '.', '%', ' ']
    raw_named_list = ['lt', 'gt', 'co', 'qu', 'bs', 'fs', 'sl', 'qm', 'as', 'pb', 'pc', 'sp']
    named_list = []
    for name in raw_named_list:
        named_list.append(str("THC-")+str(name))
    
    decoded_url = url
    for i in range(len(named_list)-1):
        code = named_list[i]
        if code in url:
            decoded_url = decoded_url.replace(code, reserved_list[i])
    
    return decoded_url
    
#print(code_url('https://www.yahoo.com/'))
#print(decode_url('httpsTHC-coTHC-bsTHC-bswwwTHC-pbyahooTHC-pbcomTHC-bs'))

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
    def __init__(self, url, proxy_ip, attempt_no):
        self.url = url
        self.proxy_ip = proxy_ip
        self.attempt_no = attempt_no
    def __call__(self):
        try:
            print("attempting r")
            r = set_up(self.url, self.proxy_ip)
            print("r attempted")
            print(r.status_code)
            if r.status_code == 200:
                filename = scrape_location + str('\\') + str(code_url(self.url)) +str('.txt')
                with open(filename, 'w') as f:
                    json.dump(r.text, f)
                attempts = self.attempt_no + 1
                answer = [self.url, self.url, attempts]
            else:
                attempts = self.attempt_no + 1
                answer = ['fail', self.url, attempts]
        except Exception:
            print("Error in attempted scrape")
            attempts = self.attempt_no + 1
            answer = ['fail', self.url, attempts]
        return answer
    def __str__(self):
        return self.url


def bulk_scrape(url_list, proxy_list):

    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    
    # Enqueue jobs

    local_proxy_list = []
    for proxy in proxy_list:
        local_proxy_list.append(proxy)
    job_limit = min([len(url_list), len(proxy_list)])
    
    for i in range(job_limit):
        choice = randint(0,len(local_proxy_list)-1)
        random_proxy = local_proxy_list[choice]
        local_proxy_list.remove(random_proxy)
        #put the tasks in the queue
        tasks.put(Task(url_list[i], random_proxy, 0))
    
    
    # Start consumers
    num_consumers = multiprocessing.cpu_count() * 3
    print('Creating %d consumers' % num_consumers)
    consumers = [ Consumer(tasks, results)
                  for i in range(num_consumers) ]
    for w in consumers:
        w.start()
        
    task_no = len(url_list)
    # Start printing results
    results_record = []
    while task_no:
        result = results.get()
        answer = result[0]
        url = result[1]
        attempt_no = result[2]
        if answer == 'fail' and attempt_no < 15:
            choice = randint(0,len(local_proxy_list)-1)
            random_proxy = local_proxy_list[choice]
            tasks.put(Task(url, random_proxy, attempt_no))
        if answer == 'fail' and attempt_no >= 15:
            task_no -= 1
        if answer != 'fail':
            results_record.append(url)
            url_list.remove(url)
            print('Result:', url)
            task_no -= 1


    # Add a poison pill for each consumer
    for i in range(num_consumers):
        tasks.put(None)

    
    time.sleep(60)    
    for w in consumers:
        w.terminate()

    print("These urls were successes: " + str(results_record))
    print("These urls were failures: " + str(url_list))    
    
    # Wait for all of the tasks to finish
    tasks.join()
    return url_list

def bulk_scraper(url_list):
        
    tested_proxy_file = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\general\scraper\tested_proxy_file.txt'
    
    with open(tested_proxy_file) as f:
        proxy_list = json.load(f)
    
    bulk_scrape(url_list, proxy_list)
    
    print("Scrape completed")
    return 'Done'
        
if __name__ == '__main__':
    url_list = ["https://www.yahoo.com/", "https://www.apple.com/"]
    
    #with open(r'C:\Users\thoma\Desktop\Python\TH Projects\Port\alpha\corn\corn_download_list.txt') as f:
    #    url_list = json.load(f)

    bulk_scraper(url_list)
    


    
