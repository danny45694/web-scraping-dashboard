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
        EC.presence_of_element_located((By.CSS_SELECTOR, ".zebra.fw.tb-theme"))
    )
    tbody = table.find_element (By.TAG_NAME, 'tbody')
    rows = tbody.find_elements(By.CSS_SELECTOR, 'tr')
    results = []

    for row in rows: #For each row in rows
        for j in range(1): #for j = num in range of 2
            city_links = row.find_elements(By.CSS_SELECTOR, 'td a')
            date_times = row.find_elements(By.CLASS_NAME, 'r')
            temps = row.find_elements(By.CLASS_NAME, 'rbi')
            
            #for I in range of city links (City links should contain 3 objects)
            for i in range(len(city_links)):

                city = city_links[i].text.strip()
                date_time = date_times[i].text.strip()
                temperature = temps[i].text.strip()
            
            
                city_data = {
                    "City": city,
                    "Date and Time": date_time,
                    "Temperature": temperature
                }
                results.append(city_data)
        break #This break is out of the j for loop but with in the row in rows loop. Should stop the rows from all firing.
    print(results)
    #print(results[0] if results else "No data row found")
#except Exception as e:
    #print("Error:", repr(e))
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
