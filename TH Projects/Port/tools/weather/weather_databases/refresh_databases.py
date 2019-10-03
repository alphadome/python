# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 21:17:55 2019

@author: thoma
"""
import sys
import_list = [
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools",
        r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\general\scraper",
        r"C:\Users\thoma\AppData\Local\Programs\Python\Python37-32\Lib\site-packages"
        ]
for import_location in import_list:
    if import_location not in sys.path:
        sys.path.append(import_location)

import requests
from ftplib import FTP
import tarfile
import zipfile
from clint.textui import progress


def extract_tar_gz(fname,extractedpath):
    if (fname.endswith("tar.gz")):
        print("extracting tar.gz")
        tar = tarfile.open(fname, "r:gz")
        tar.extractall(path=extractedpath)
        tar.close()
    elif (fname.endswith("tar")):
        print("extracting tar")
        tar = tarfile.open(fname, "r:")
        tar.extractall(path=extractedpath)
        tar.close()

def refresh_noaa():
    
    ftp = FTP('ftp.ncdc.noaa.gov')     # connect to host, default port
    ftp.login()                     # user anonymous, passwd anonymous@
    ftp.cwd('pub/data/ghcn/daily/')               # change into "debian" directory
    ftp.retrlines('LIST')           # list directory contents
    
    ftp_stem = "/pub/data/ghcn/daily/"
    ftp_file = ["readme.txt", "ghcnd-inventory.txt", "ghcnd_all.tar.gz"]
    
    noaa_folder = r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_databases\databases\\"    
    
    for file in ftp_file:
        ftp.retrbinary('RETR ' + ftp_stem + file, open(str(noaa_folder + str(file)), 'wb').write)
    
    ftp.quit()
    
def refresh_ecad():
    
    download_base = 'https://www.ecad.eu/utils/downloadfile.php?file=download/'
    download_extension = ['ECA_blend_tg.zip',
                          'ECA_blend_rr.zip'
                          ]

    ecad_folder = r"C:\Users\thoma\Desktop\Python\TH Projects\Port\tools\weather\weather_databases\databases\\"    
   
    for extension in download_extension:
        url = download_base + extension
        print("downloading " + str(url))
        r = requests.get(url, stream=True)  
        
        path = str(str(ecad_folder)+extension)
        with open(path, 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                if chunk:
                    f.write(chunk)
                    f.flush()        
        
        with open(str(ecad_folder)+extension, 'wb') as f:
            f.write(r.content)
        
        print("extracting " + str(extension))
        with zipfile.ZipFile(str(ecad_folder)+extension, 'r') as zip_ref:
            zip_ref.extractall(str(ecad_folder)+str(extension).replace('.zip',''))



if __name__ == '__main__':
    refresh_ecad()
    refresh_noaa()

