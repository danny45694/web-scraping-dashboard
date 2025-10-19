from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re


driver = webdriver.Chrome()
driver.get('https://www.timeanddate.com/weather/')

wait = WebDriverWait(driver, 15)

# 1) Wait for any row with at least one city link to appear
table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody")))
rows = table.find_elements(By.TAG_NAME, "tr")

results = []
for row in rows:
    # 2) Every city cell is a <td> that contains an <a>
    city_tds = row.find_elements(By.XPATH, ".//td[a]")

    for city_td in city_tds:
        city = city_td.find_element(By.TAG_NAME, "a").text.strip()

        # 3) The time td: class='r' AND id starts with 'p' (e.g., p0, p47, p94)
        time_td = city_td.find_element(
            By.XPATH, "following-sibling::td[@class='r' and starts-with(@id,'p')][1]"
        )
        date_time = time_td.text.strip()

        # 4) The next temperature td with class='rbi'
        temp_td = city_td.find_element(
            By.XPATH, "following-sibling::td[@class='rbi'][1]"
        )
        temperature = temp_td.text.replace('\xa0', ' ').strip() #Replace non-breaking space with normal space.

        results.append({
            "City": city,
            "Date and Time": date_time,
            "Temperature": temperature
        })

print(results)
driver.quit()

#Export to csv

df = pd.DataFrame(results)

#---------------- Data Cleanup ---------------

#removed leading and trailing whitespace during initial scrape with .strip()
df = df.drop_duplicates()
df = df.dropna()




#-------------- Data Transformations ------------



    #------------ Temp categories --------------
temps_categories = ['very cold','cold','comfortable', 'hot', 'very hot']

def categorize(value):
    if value <= 32:
        return 'very cold'
    elif value <= 60:
        return 'cold'
    elif value <= 79:
        return 'comfortable'
    elif value <= 89:
        return 'hot' 
    else:
        return 'very hot'
    

 #--------- Strip and convert temp to int -------
def stripSTR(value):
    stripped_string = re.sub(r'\s.*', "", value)
    converted_value = int(stripped_string)
    return converted_value
    
df['temp values'] = df['Temperature'].apply(stripSTR)

df['temp category'] = df['temp values'].apply(categorize)


#----------------- grouping ----------------

hottest = df.groupby('City')['temp values'].sort_values(ascending=False)

coldest = df.groupby('City')['temp values'].sort_values(ascending=True)




# -------------- Export to csv ------------------
df.to_csv("weather_data.csv", index=False)