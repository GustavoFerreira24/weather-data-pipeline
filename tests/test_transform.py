import pandas as pd
import pytest

from src.transform import validate_weather_data


def test_invalid_humidity():
    df = pd.DataFrame([{
        "city": "porto",
        "timestamp": pd.Timestamp("2026-09-01T12:00:00Z"),
        "temperature": 22.5,
        "humidity": 150,
        "precipitation": 0.0,
        "wind_speed": 10.0
    }])

    with pytest.raises(ValueError, match="Invalid weather measurements"):
        validate_weather_data(df)



def test_conflicting_observations():
    df1 = pd.DataFrame([{
        "city": "porto",
        "timestamp": pd.Timestamp("2026-09-01T12:00:00Z"),
        "temperature": 14.3,
        "humidity": 90,
        "precipitation": 0.6,
        "wind_speed": 10.9
    }])

    df2 = pd.DataFrame([{
        "city": "porto",
        "timestamp": pd.Timestamp("2026-09-01T12:00:00Z"),
        "temperature": 27.3,
        "humidity": 90,
        "precipitation": 0.6,
        "wind_speed": 10.9
    }])

    df_final = pd.concat([df1, df2], ignore_index=True)

    with pytest.raises(ValueError, match="Conflicting weather observations"):
        validate_weather_data(df_final)


def test_identical_duplicates():
    df = pd.DataFrame([{
        "city": "porto",
        "timestamp": pd.Timestamp("2026-09-01T12:00:00Z"),
        "temperature": 14.3,
        "humidity": 90,
        "precipitation": 0.6,
        "wind_speed": 10.9
    }, {
        "city": "porto",
        "timestamp": pd.Timestamp("2026-09-01T12:00:00Z"),
        "temperature": 14.3,
        "humidity": 90,
        "precipitation": 0.6,
        "wind_speed": 10.9
    }])

    df_final = validate_weather_data(df)

    assert len(df_final) == 1