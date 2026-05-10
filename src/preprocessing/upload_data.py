import pandas as pd
from src.utils.db import engine

# Load CSV
df = pd.read_csv("data/raw/air_quality.csv")
df.to_sql("air_quality_data",engine,if_exists="replace",index=False)
print("Data uploaded successfully!")