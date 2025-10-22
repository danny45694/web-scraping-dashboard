import sqlite3
import pandas as pd

# File names
CSV_FILE = "weather_data.csv"
DB_FILE = "weather.db"


# Connect to database
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create the table
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

# Read the CSV file
df = pd.read_csv(CSV_FILE)

# Rename columns to match database
df = df.rename(columns={
    "Date and Time": "DateAndTime",
    "Temperature": "TemperatureText",
    "temp values": "TempValues",
    "temp category": "TempCategory"
})

# Keep only needed columns
cols = ["City", "DateAndTime", "TemperatureText", "TempValues", "TempCategory"]
df = df[cols]

#print("Columns after rename:", df.columns.tolist())

# Import into database
print("Importing data")
df.to_sql("weather", conn, if_exists="append", index=False)

# Save changes
conn.commit()


# Close connection
conn.close()
print("Import complete")