import pandas as pd


def inspect_dataset():

    print("\nLoading dataset...\n")


    FILE_PATH = (
        "data/external/"
        "data_1055_rows.csv"
    )


    # =========================
    # LOAD CSV
    # =========================

    df = pd.read_csv(FILE_PATH)


    # =========================
    # SHAPE
    # =========================

    print("=" * 60)
    print("DATASET SHAPE")
    print("=" * 60)

    print(df.shape)


    # =========================
    # COLUMNS
    # =========================

    print("\n" + "=" * 60)
    print("COLUMNS")
    print("=" * 60)

    print(df.columns.tolist())


    # =========================
    # FIRST 5 ROWS
    # =========================

    print("\n" + "=" * 60)
    print("FIRST 5 ROWS")
    print("=" * 60)

    print(df.head())


    # =========================
    # DATA TYPES
    # =========================

    print("\n" + "=" * 60)
    print("DATA TYPES")
    print("=" * 60)

    print(df.dtypes)


    # =========================
    # MISSING VALUES
    # =========================

    print("\n" + "=" * 60)
    print("MISSING VALUES")
    print("=" * 60)

    print(df.isnull().sum())


    # =========================
    # DUPLICATES
    # =========================

    print("\n" + "=" * 60)
    print("DUPLICATE ROWS")
    print("=" * 60)

    print(df.duplicated().sum())


    # =========================
    # NUMERIC SUMMARY
    # =========================

    print("\n" + "=" * 60)
    print("NUMERIC SUMMARY")
    print("=" * 60)

    print(df.describe())


if __name__ == "__main__":

    inspect_dataset()