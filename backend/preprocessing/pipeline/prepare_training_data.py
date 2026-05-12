import pandas as pd


INPUT_FILE = (
    "data/external/"
    "final_merged_dataset_fixed.xlsx"
)

OUTPUT_FILE = (
    "data/processed/"
    "training_dataset.csv"
)


def create_aqi_category(aqi):

    if aqi <= 50:
        return "Good"

    elif aqi <= 100:
        return "Moderate"

    elif aqi <= 150:
        return "Poor"

    else:
        return "Severe"


def prepare_training_data():

    print("\nLoading dataset...\n")

    # =========================
    # Load Dataset
    # =========================

    df = pd.read_excel(INPUT_FILE)

    print("Original shape:", df.shape)

    # =========================
    # Clean Column Names
    # =========================

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    print("\nCleaned Columns:\n")
    print(df.columns.tolist())

    # =========================
    # Convert Numeric Columns
    # =========================

    df["aqi"] = pd.to_numeric(
        df["aqi"],
        errors="coerce"
    )

    df["pm2.5"] = pd.to_numeric(
        df["pm2.5"],
        errors="coerce"
    )

    df["pm10"] = pd.to_numeric(
        df["pm10"],
        errors="coerce"
    )

    # =========================
    # Remove Invalid Rows
    # =========================

    df = df.dropna()

    print("\nShape after cleaning:", df.shape)

    # =========================
    # Timestamp Processing
    # =========================

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    df["year"] = df["timestamp"].dt.year
    df["month"] = df["timestamp"].dt.month
    df["day"] = df["timestamp"].dt.day

    # =========================
    # AQI Category
    # =========================

    df["aqi_category"] = df["aqi"].apply(
        create_aqi_category
    )

    # =========================
    # Feature Selection
    # =========================

    selected_columns = [

        # location
        "city",
        "latitude",
        "longitude",

        # weather
        "temperature",
        "humidity",
        "pressure",
        "wind_speed",

        # satellite
        "aer",
        "co",
        "dem",
        "lulc",
        "ndvi",
        "nightlights",
        "no2",
        "pop",
        "so2",

        # time
        "year",
        "month",
        "day",

        # targets
        "aqi",
        "aqi_category",
        "pm2.5",
        "pm10",
    ]

    df = df[selected_columns]

    # =========================
    # Dataset Summary
    # =========================

    print("\nFinal shape:", df.shape)

    print("\nAQI Category Counts:\n")
    print(df["aqi_category"].value_counts())

    print("\nFirst 5 Rows:\n")
    print(df.head())

    # =========================
    # Save Processed Dataset
    # =========================

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nTraining dataset saved!")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":

    prepare_training_data()