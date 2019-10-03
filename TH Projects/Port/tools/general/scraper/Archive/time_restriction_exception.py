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

def time_restricted(t, f, v1, v2=''):
    test_list = []
    class thread_with_exception(threading.Thread): 
        def __init__(self, name): 
            threading.Thread.__init__(self) 
            self.name = name 
                  
        def run(self): 
      
            # target function of the thread class 
            try: 
                while True: 
                    answer = f(v1, v2)
                    test_list.append(answer)
                    print('\t\t - Success:' + str(v1) + str(v2)) 
                    return 1
            finally: 
                print('\t\t - End timer test process') 
               
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
                print('\t\t - Exception raise failure') 
           
    t1 = thread_with_exception('Thread 1') 
    t1.start() 
    time.sleep(t) 
    t1.raise_exception() 
    t1.join() 
    
    if test_list == []:
        print("\t\t - Fail timer test for proxy: " + str(v1) +" "+ str(v2))
        return "Fail"
    else:
        print("\t\t - Pass timer test for proxy: " + str(v1) +" "+ str(v2))
        print(test_list[0])
        return test_list[0]



def trial1(v1, v2=''):
    time.sleep(1)
    return (float(v1))* 2

def trial2(v1, v2='0'):
    time.sleep(1)
    return (float(v1) + float(v2))* 2

#time_restricted(2, trial2, 2, 2)
def time_restricted1(t, f, v1, v2=''):
    test_list = []
    def run(): 
        while True: 
            answer = f(v1, v2)
            test_list.append(answer)
            print('\t\t - Success:' + str(v1) + str(v2)) 
            return 1
            
            global stop_threads 
            if stop_threads: 
                break
      
    stop_threads = False
    t1 = threading.Thread(target = run) 
    t1.start() 
    time.sleep(1) 
    stop_threads = True
    t1.join() 
    
    if test_list == []:
        print("\t\t - Fail timer test for proxy: " + str(v1) +" "+ str(v2))
        return "Fail"
    else:
        print("\t\t - Pass timer test for proxy: " + str(v1) +" "+ str(v2))
        print(test_list[0])
        return test_list[0]

time_restricted1(2, trial1, 2)

