import os
import pandas as pd
import numpy as np

from backend.preprocessing.pipeline.raster_utils import (
    load_raster,
    resample_raster,
    clean_array,
)

BASE_FOLDER = "data/raw/india"

TARGET_FILE = "NO2_India.tif"

FEATURE_FILES = {
    "DEM": "DEM_India.tif",
    "NDVI": "NDVI_India.tif",
    "LULC": "LULC_India.tif",
    "POP": "POP_India.tif",
    "NL": "NightLights_India.tif",
}


def build_india_dataset():

    target_path = os.path.join(
        BASE_FOLDER,
        TARGET_FILE
    )

    target_data, metadata = load_raster(
        target_path
    )

    target_height, target_width = target_data.shape

    features = {}

    for feature_name, filename in FEATURE_FILES.items():

        path = os.path.join(
            BASE_FOLDER,
            filename
        )

        data = resample_raster(
            path,
            target_height,
            target_width
        )

        data = clean_array(data)

        features[feature_name] = data

    rows = []

    for row in range(target_height):

        for col in range(target_width):

            record = {
                "row": row,
                "col": col,
                "NO2": target_data[row, col],
            }

            for feature_name in features:

                record[feature_name] = (
                    features[feature_name][row, col]
                )

            rows.append(record)

    df = pd.DataFrame(rows)

    df.replace(
        [np.inf, -np.inf],
        np.nan,
        inplace=True
    )

    df.dropna(inplace=True)

    output_path = (
        "outputs/datasets/"
        "india_feature_dataset.csv"
    )

    df.to_csv(
        output_path,
        index=False
    )

    print(df.head())

    print(
        f"\nDataset shape: {df.shape}"
    )

    print(
        f"\nSaved to: {output_path}"
    )