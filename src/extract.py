
import json
from pathlib import Path

import requests


# Cities and their coordinates
cities = {
    "porto": {"latitude": 41.15, "longitude": -8.61},
    "lisboa": {"latitude": 38.72, "longitude": -9.14},
    "madrid": {"latitude": 40.42, "longitude": -3.70}
}

# API configuration
url = "https://archive-api.open-meteo.com/v1/archive"

# Raw data directory
project_root = Path(__file__).resolve().parent.parent
raw_dir = project_root / "data" / "raw"
raw_dir.mkdir(parents=True, exist_ok=True)

# Extract weather data for each city
for city, coordinates in cities.items():

    params = {
        "latitude": coordinates["latitude"],
        "longitude": coordinates["longitude"],
        "start_date": "2026-09-01",
        "end_date": "2026-09-02",
        "hourly": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
        "timezone": "UTC"
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()  #detect errors in the request

    data = response.json()

    # Save raw JSON
    output_path = raw_dir / f"{city}.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    print(f"Data saved to {output_path}")

print("Extraction completed successfully!")
