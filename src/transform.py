
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

print("\nFinal DataFrame:")
print(df_final.head().to_string(index=False))
print("Shape:", df_final.shape)
