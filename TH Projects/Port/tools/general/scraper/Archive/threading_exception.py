# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 21:20:12 2019

@author: thoma
"""

# Python program raising 
# exceptions in a python 
# thread 
  
import threading 
import ctypes 
import time 
import requests

def get_random_ua():
    random_ua = ''
    ua_file = r'C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\general_programs\scraper\ua_file.txt'

    ua_list = []

    with open(ua_file) as f:
        lines = f.readlines()
    for line in lines:
        if len(lines) > 0:
            ua_list.append(line)
    
    choice = randint(0,len(ua_list)-1)
    random_ua = ua_list[choice]
    return random_ua

def test_proxy_function(proxy_ip):
    try:
        url = 'https://www.yahoo.com'
        identity_list = get_random_ua()
        user_agent = identity_list[0]
        headers = {'user-agent': user_agent}
        
        https_proxy = "https://"+str(proxy_ip)
        
        proxyDict = {
                      "https" : https_proxy, 
                    }
        r = requests.get(url,headers=headers,proxies=proxyDict)

        result = "pass"
    except Exception:
        result = "fail"
    return result


def trial(proxy_ip):
    time.sleep(4)
    return float(proxy_ip) * 2

# Python program raising 
# exceptions in a python 
# thread 

def time_restricted_test(f, proxy_ip, t):
    test_list = []
    class thread_with_exception(threading.Thread): 
        def __init__(self, name): 
            threading.Thread.__init__(self) 
            self.name = name 
                  
        def run(self): 
      
            # target function of the thread class 
            try: 
                while True: 
                    answer = f(proxy_ip)
                    test_list.append(answer)
                    print('Success:' + str(proxy_ip)) 
                    return 1
            finally: 
                print('End process') 
               
        def get_id(self): 
      
            # returns id of the respective thread 
            if hasattr(self, '_thread_id'): 
                return self._thread_id 
            for id, thread in threading._active.items(): 
                if thread is self: 
                    return id
       
        def raise_exception(self): 
            thread_id = self.get_id() 
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
                  ctypes.py_object(SystemExit)) 
            if res > 1: 
                ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
                print('Exception raise failure') 
           
    t1 = thread_with_exception('Thread 1') 
    t1.start() 
    time.sleep(t) 
    t1.raise_exception() 
    t1.join() 
    
    if test_list == []:
        print("Fail for proxy: " + str(proxy_ip))
        return "Fail"
    else:
        print("Pass for proxy: " + str(proxy_ip))
        return "Pass"

time_restricted_test(trial, 2, 2)

#mythread = MyThread(name = "Thread-{}".format(x + 1))  # ...Instantiate a thread and pass a unique ID to it


