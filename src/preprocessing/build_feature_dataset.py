import os
import rasterio
import pandas as pd

folder = "data/raw"

merged_df = None

for file in os.listdir(folder):

    if file.endswith(".tif"):

        layer_name = file.split("_")[0].lower()

        path = os.path.join(folder, file)

        with rasterio.open(path) as src:

            data = src.read(1)

        rows, cols = data.shape

        records = []

        for row in range(rows):
            for col in range(cols):

                records.append({
                    "row": row,
                    "col": col,
                    layer_name: float(data[row, col])
                })

        df = pd.DataFrame(records)

        if merged_df is None:
            merged_df = df
        else:
            merged_df = pd.merge(
                merged_df,
                df,
                on=["row", "col"]
            )

print(merged_df.head())

merged_df.to_csv(
    "outputs/full_feature_dataset.csv",
    index=False
)

print("Feature dataset created successfully!")