import pandas as pd
import os

INPUT_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "data",
    "external",
    "data_1055_rows.csv"
)

OUTPUT_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "data",
    "processed",
    "aqi_training_data.csv"
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

    df["city_encoded"] = (

        df["city"]
        .astype("category")
        .cat.codes
    )


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


    print("\nTraining dataset saved!")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":

    prepare_training_data()