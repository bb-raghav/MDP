import pandas as pd
import os
import joblib

ROOT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)

INPUT_FILE = os.path.join(
    ROOT_DIR,
    "data",
    "external",
    "data_1055_rows.csv"
)

OUTPUT_FILE = os.path.join(
    ROOT_DIR,
    "data",
    "processed",
    "aqi_training_data.csv"
)

CITY_ENCODER_FILE = os.path.join(
    ROOT_DIR,
    "backend",
    "models",
    "saved",
    "city_encoder.pkl"
)


def prepare_training_data():

    print("\nLoading dataset...\n")

    df = pd.read_csv(INPUT_FILE)


    # =========================
    # CLEAN COLUMN NAMES
    # =========================

    df.columns = [

        col.strip()
        .lower()
        .replace(".", "_")
        .replace(" ", "_")

        for col in df.columns
    ]


    print("=" * 60)
    print("COLUMNS AFTER CLEANING")
    print("=" * 60)

    print(df.columns.tolist())


    # =========================
    # DATE FEATURES
    # =========================

    print("\nExtracting date features...\n")

    df["date"] = pd.to_datetime(
        df["date"]
    )

    df["year"] = (
        df["date"].dt.year
    )

    df["month"] = (
        df["date"].dt.month
    )

    df["day"] = (
        df["date"].dt.day
    )

    df["weekday"] = (
        df["date"].dt.weekday
    )


    # =========================
    # REMOVE UNUSED COLUMNS
    # =========================

    print("Dropping unused columns...\n")

    df = df.drop(
        columns=["date"]
    )


    # =========================
    # CITY ENCODING
    # =========================

    print("Encoding cities...\n")

    city_categories = (
        df["city"]
        .astype(str)
        .str.strip()
        .str.lower()
        .astype("category")
    )

    df["city_encoded"] = city_categories.cat.codes

    city_encoder = {
        "mapping": {
            city: int(index)
            for index, city in enumerate(city_categories.cat.categories)
        },
        "default_code": 0,
    }


    # =========================
    # FINAL FEATURE SET
    # =========================

    selected_columns = [

        "pm2_5",
        "pm10",
        "no2",
        "so2",
        "co",

        "temperature",
        "humidity",
        "pressure",
        "wind_speed",
        "apparent_temperature",

        "year",
        "month",
        "day",
        "weekday",

        "city_encoded",

        "aqi"
    ]


    df = df[selected_columns]


    # =========================
    # CHECK FINAL DATASET
    # =========================

    print("\n" + "=" * 60)
    print("FINAL DATASET SHAPE")
    print("=" * 60)

    print(df.shape)


    print("\n" + "=" * 60)
    print("FIRST 5 ROWS")
    print("=" * 60)

    print(df.head())


    # =========================
    # SAVE
    # =========================

    df.to_csv(

        OUTPUT_FILE,

        index=False
    )

    os.makedirs(os.path.dirname(CITY_ENCODER_FILE), exist_ok=True)
    joblib.dump(city_encoder, CITY_ENCODER_FILE)


    print("\nTraining dataset saved!")
    print(f"Saved to: {OUTPUT_FILE}")
    print(f"City encoder saved to: {CITY_ENCODER_FILE}")


if __name__ == "__main__":

    prepare_training_data()
