import pandas as pd

FILE_PATH = (
    "data/external/"
    "final_merged_dataset_fixed.xlsx"
)


def inspect_dataset():

    print("\nLoading dataset...\n")

    df = pd.read_excel(FILE_PATH)

    print("=" * 60)
    print("DATASET SHAPE")
    print("=" * 60)

    print(df.shape)

    print("\n")

    print("=" * 60)
    print("COLUMN NAMES")
    print("=" * 60)

    print(df.columns.tolist())

    print("\n")

    print("=" * 60)
    print("DATA TYPES")
    print("=" * 60)

    print(df.dtypes)

    print("\n")

    print("=" * 60)
    print("MISSING VALUES")
    print("=" * 60)

    print(df.isnull().sum())

    print("\n")

    print("=" * 60)
    print("DUPLICATE ROWS")
    print("=" * 60)

    print(df.duplicated().sum())

    print("\n")

    print("=" * 60)
    print("FIRST 5 ROWS")
    print("=" * 60)

    print(df.head())

    print("\n")

    print("=" * 60)
    print("NUMERICAL SUMMARY")
    print("=" * 60)

    print(df.describe())


if __name__ == "__main__":

    inspect_dataset()