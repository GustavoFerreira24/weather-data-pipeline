import json
from pathlib import Path

import pandas as pd

project_root = Path(__file__).resolve().parent.parent
raw_dir = project_root / "data" / "raw"

dataframes = []

for file_path in sorted(raw_dir.glob("*.json")):
    city = file_path.stem

    # Read raw JSON
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Convert to DataFrame
    df = pd.DataFrame(data["hourly"])

    # Convert timestamps
    df["time"] = pd.to_datetime(df["time"], utc=True)

    # Rename columns
    df = df.rename(columns={
        "time": "timestamp",
        "temperature_2m": "temperature",
        "relative_humidity_2m": "humidity",
        "wind_speed_10m": "wind_speed"
    })

    # Add city
    df["city"] = city

    # Store DataFrame
    dataframes.append(df)

    print(f"{city}: {len(df)} rows")

# Combine all cities
df_final = pd.concat(dataframes, ignore_index=True)

# Data Quality

required_columns = {
    "city", "timestamp", "temperature",
    "humidity", "precipitation", "wind_speed"
}

# Validate schema
if set(df_final.columns) != required_columns:
    raise ValueError("Unexpected DataFrame schema")

# Validate numeric data types
numeric_columns = [
    "temperature", "humidity",
    "precipitation", "wind_speed"
]

for column in numeric_columns:
    df_final[column] = pd.to_numeric(
        df_final[column], errors="raise"
    )

# Validate required fields
if df_final[["city", "timestamp"]].isna().any().any():
    raise ValueError("Missing city or timestamp")

# Validate measurement ranges
invalid_values = (
    (df_final["humidity"].notna() &
     ~df_final["humidity"].between(0, 100))
    | (df_final["precipitation"] < 0)
    | (df_final["wind_speed"] < 0)
)

if invalid_values.any():
    raise ValueError("Invalid weather measurements")

# Remove identical rows
original_count = len(df_final)
df_final = df_final.drop_duplicates()

print(f"Exact duplicates removed: {original_count - len(df_final)}")

# Detect conflicting observations
conflicts = df_final.duplicated(
    subset=["city", "timestamp"],
    keep=False
)

if conflicts.any():
    raise ValueError("Conflicting observations for the same city and timestamp")

# Report missing values
print("\nMissing values:")
print(df_final.isna().sum())

print("\nFinal shape:", df_final.shape)
print("Data Quality checks passed!")
