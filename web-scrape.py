import pandas as pd
import time
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()


driver.get("https://www.timeanddate.com/weather/")



'''Purpose of this python script is pull data, clean it and prep it for CSV export. Steps needed:
1. Pull data
2. Check over the data and begin cleaning/standarization process
3. Push data into structures that will enable easy export to csv. 
    What structure do I need for my end goal?
        A.
          
        
'''



#Extract website

try:
    wait = WebDriverWait(driver, 10)
    body = driver.find_element(By.CSS_SELECTOR, 'body')
    
    
    # table class ="zebra fw tb-theme"

    locations = body.find_elements(By.CSS_SELECTOR, "table.zebra.fw.tb-theme")
    results = []
    for location in locations:
        tbHeader = location.find_element(By.CSS_SELECTOR, '.tb-header')
        place = location.find_element (By.TAG_NAME, 'tbody')
        data = {
            "location": place
        }
        results.append(data)
except:
    driver.quit()


driver.quit()





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
