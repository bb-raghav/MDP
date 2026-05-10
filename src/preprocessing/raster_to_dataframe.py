import rasterio
import pandas as pd
import numpy as np

file_path = "data/raw/SO2_Bengaluru.tif"

with rasterio.open(file_path) as src:

    data = src.read(1)

rows, cols = data.shape

records = []

for row in range(rows):
    for col in range(cols):

        value = data[row, col]

        records.append({
            "row": row,
            "col": col,
            "so2": float(value)
        })

df = pd.DataFrame(records)

print(df.head())

df.to_csv(
    "outputs/so2_dataframe.csv",
    index=False
)

print("Conversion successful!")