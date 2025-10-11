import pandas as pd
import time
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

url = "https://www.baseball-almanac.com/yearmenu.shtml"
driver.get(url)
time.sleep(4)


'''Purpose of this python script is pull data, clean it and prep it for CSV export. Steps needed:
1. Pull data
2. Check over the data and begin cleaning/standarization process
3. Push data into structures that will enable easy export to csv. 
    What structure do I need for my end goal?
        A.
          
        
'''

#Extract relevant details (Year, event names, stats)

#Find year, pull data

    #Put data into a dict


#Find Event names, pull data

    #Put data into a dict


#Find stats, pull data

    #put data into a dict


#Save raw data into CSV for each dataset
# Base syntax code for writing to csv

#with open('output.csv', 'w', newline='') as csvfile:
    #writer = csv.writer(csvfile)
    #write.writerows(data) -----> data being from the datasets

