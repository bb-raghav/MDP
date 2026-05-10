import pandas as pd

df = pd.read_csv(
    "outputs/full_feature_dataset.csv"
)

print(df.info())
print(df.isnull().sum())

# Remove NaNs
df = df.dropna()

# Remove duplicate rows
df = df.drop_duplicates()

# Save cleaned dataset
df.to_csv(
    "outputs/clean_feature_dataset.csv",
    index=False
)

print("Cleaning successful!")