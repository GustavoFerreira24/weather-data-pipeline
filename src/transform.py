import json
from pathlib import Path

import pandas as pd


def transform_weather_data() -> pd.DataFrame:
    project_root = Path(__file__).resolve().parent.parent
    raw_dir = project_root / "data" / "raw"

    dataframes = []

    for file_path in sorted(raw_dir.glob("*.json")):
        city = file_path.stem

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        df = pd.DataFrame(data["hourly"])

        df["time"] = pd.to_datetime(df["time"], utc=True)

        df = df.rename(columns={
            "time": "timestamp",
            "temperature_2m": "temperature",
            "relative_humidity_2m": "humidity",
            "wind_speed_10m": "wind_speed"
        })

        df["city"] = city
        dataframes.append(df)

    if not dataframes:
        raise ValueError("No raw JSON files found")

    df_final = pd.concat(dataframes, ignore_index=True)

    # Data Quality
    required_columns = {
        "city", "timestamp", "temperature",
        "humidity", "precipitation", "wind_speed"
    }

    if set(df_final.columns) != required_columns:
        raise ValueError("Unexpected DataFrame schema")

    numeric_columns = [
        "temperature", "humidity",
        "precipitation", "wind_speed"
    ]

    for column in numeric_columns:
        df_final[column] = pd.to_numeric(
            df_final[column], errors="raise"
        )

    if df_final[["city", "timestamp"]].isna().any().any():
        raise ValueError("Missing city or timestamp")

    invalid_values = (
        (df_final["humidity"].notna() &
         ~df_final["humidity"].between(0, 100))
        | (df_final["precipitation"] < 0)
        | (df_final["wind_speed"] < 0)
    )

    if invalid_values.any():
        raise ValueError("Invalid weather measurements")

    df_final = df_final.drop_duplicates().reset_index(drop=True)

    if df_final.duplicated(
        subset=["city", "timestamp"]
    ).any():
        raise ValueError("Conflicting weather observations")

    return df_final


if __name__ == "__main__":
    df = transform_weather_data()
    print("Transformation completed!")
    print("Shape:", df.shape)
    print(df.head().to_string(index=False))
