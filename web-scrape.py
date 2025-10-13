import pandas as pd
import time
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
    wait = WebDriverWait(driver, 15)

    table = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table.zebra.fw.tb-theme"))
    )
    body = driver.find_element(By.CSS_SELECTOR, 'body')
    tbody = body.find_element (By.TAG_NAME, 'tbody')
    rows = tbody.find_elements(By.CSS_SELECTOR, 'tr')

    results = []

    for row in rows:
        city_links = row.find_elements(By.CSS_SELECTOR, 'td a')
        city = city_links[0].text.strip()
        #date_time = cities.find_elements(By.CLASS_NAME, '.r')
        temp_els = row.find_elements(By.CSS_SELECTOR, 'td > .rbi')
        temperature = temp_els[0].text.strip()
        
        city_data = {
            "City": city,
            "Temperature": temperature
        }
        results.append(city_data)
        break
    print(results[0] if results else "No data row found")
except Exception as e:
    print("Error:", repr(e))
finally:
    driver.quit()


#If I want to see exactly what I am targeting.
    #print(rows[0].get_attribute("outerHTML"))  # first row’s HTML


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
