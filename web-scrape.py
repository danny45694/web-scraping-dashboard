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
        # City (skip row if no <a>)
        a_tags = city_td.find_elements(By.TAG_NAME, "a")
        if not a_tags:
            continue
        city = a_tags[0].text.strip()

        # 3) The time td: class='r' AND id starts with 'p' (e.g., p0, p47, p94)
        date_time = None
        time_candidates = city_td.find_elements(
            By.XPATH, "following-sibling::td[@class='r' and starts-with(@id,'p')][1]"
        )
        if time_candidates:
            date_time = time_candidates[0].text.strip()

        # 4) The next temperature td with class='rbi'
        temperature = None
        temp_candidates = city_td.find_elements(
            By.XPATH, "following-sibling::td[@class='rbi'][1]"
        )
        if temp_candidates:
            temperature = temp_candidates[0].text.replace('\xa0', ' ').strip()

        results.append({
            "City": city,
            "Date and Time": date_time,
            "Temperature": temperature
        })

#print(results) #Checking output to ensure it works.
driver.quit()

#Export to csv

df = pd.DataFrame(results)

#---------------- Data Cleanup ---------------
# removed leading and trailing whitespace during initial scrape with .strip()
df = df.drop_duplicates()
df = df.dropna()

#-------------- Data Transformations ------------

#------------ Temp categories --------------
category_order = ['very cold','cold','comfortable','hot','very hot']

def categorize(value):
    if value is None:
        return None
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
    if not isinstance(value, str):
        return None
    m = re.match(r"^(-?\d+)", value.strip())
    return int(m.group(1)) if m else None

df['temp values'] = df['Temperature'].apply(stripSTR)

# Drop rows where temp couldn't be parsed (optional, but avoids errors)
df = df.dropna(subset=['temp values'])
df['temp values'] = df['temp values'].astype(int)

df['temp category'] = df['temp values'].apply(categorize)

#----------------- grouping ----------------

category_counts = (
    df['temp category']
      .value_counts()
      .reindex(category_order, fill_value=0)
      .rename_axis('temp category')
      .reset_index(name='count')
)

hottest = df.sort_values('temp values', ascending=False)
coldest = df.sort_values('temp values', ascending=True)


# Filter for cold, comfortable, and hot etc.
def filter_cities_by_category(df, category, sort_by='City'):
    cols = ['City', 'Temperature', 'temp values', 'temp category', 'Date and Time']
    out = df.loc[df['temp category'].eq(category), cols]
    if sort_by in out.columns:
        out = out.sort_values(sort_by, ascending=True)
    return out

# -------------- Export to csv ------------------
df.to_csv("weather_data.csv", index=False)
print(f"Saved {len(df)} rows to weather_data.csv")
