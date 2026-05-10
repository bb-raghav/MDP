import sqlite3
import pandas as pd
conn = sqlite3.connect("data/raw/airquality_full.db")

cursor = conn.cursor()

cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table';"
)

tables = cursor.fetchall()

print("Tables:")
print(tables)

query = "SELECT * FROM air_quality_data LIMIT 5"



df = pd.read_sql(query, conn)

print(df.head())