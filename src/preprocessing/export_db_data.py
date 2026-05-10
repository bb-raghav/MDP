import sqlite3
import pandas as pd

conn = sqlite3.connect(
    "data/raw/airquality_full.db"
)

query = "SELECT * FROM air_quality_data"

df = pd.read_sql(query, conn)

print(df.head())

df.to_csv(
    "outputs/air_quality_labels.csv",
    index=False
)

print("Export successful!")