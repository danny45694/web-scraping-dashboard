import sqlite3
import pandas as pd

# ---- File paths ----
CSV_FILE = "weather_data.csv"
DB_FILE = "weather.db"

# ---- Connect and create table ----
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS weather (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    City TEXT,
    DateAndTime TEXT,
    TemperatureText TEXT,
    TempValues INTEGER,
    TempCategory TEXT
)
""")

# ---- Read CSV and clean ----
df = pd.read_csv(CSV_FILE)

# Rename columns from Program 1 to match DB
df = df.rename(columns={
    "Date and Time": "DateAndTime",
    "Temperature": "TemperatureText",
    "temp values": "TempValues",
    "temp category": "TempCategory"
})

# Keep only the needed columns
cols = ["City", "DateAndTime", "TemperatureText", "TempValues", "TempCategory"]
df = df[cols]

# ---- Write to database ----
df.to_sql("weather", conn, if_exists="append", index=False)

conn.commit()
conn.close()
print(f"Imported {len(df)} rows into {DB_FILE}")
