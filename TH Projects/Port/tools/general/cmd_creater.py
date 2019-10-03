# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 23:04:48 2019

@author: thoma
"""
from datetime import datetime

program_name = 'update_custom_weather_profiles'
location_address = r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_programs"
location = location_address + '\\'+ program_name
print(location)
cmd_location = str(location) + ".cmd"
cmd_log_location = str(location)+'log' + ".cmd"

program_location = str(location) + ".py"
python_location = r"C:\Users\thoma\AppData\Local\Programs\Python\Python37-32"

atm = datetime.now()
char_list = ['-',':','.', ' ']
for char in char_list:
    atm = str(atm).replace(char,'')
atm = atm[:14]
log_name = str(" >> " + '"' + location_address +"\\log\\"+program_name + 'log' + str(atm) + '.txt"')


line1 = 'cd ' + str(python_location)
line2 = 'python '+ '"' + str(program_location)+'"' + str(log_name)
line3 = 'python '+ '"' + str(program_location)+'"'


with open(cmd_log_location, 'w') as f:
    f.write(line1 + str('\n') + line2 + str('\nPAUSE'))

with open(cmd_location, 'w') as f:
    f.write(line1 + str('\n') + line3 + str('\nPAUSE'))
