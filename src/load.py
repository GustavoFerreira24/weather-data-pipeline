from pathlib import Path

import pandas as pd

from transform import transform_weather_data


def main():
    # Get transformed data
    df = transform_weather_data()

    # Define output path
    project_root = Path(__file__).resolve().parent.parent
    processed_dir = project_root / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)

    output_path = processed_dir / "weather.parquet"

    # Write Parquet
    df.to_parquet(
        output_path,
        engine="pyarrow",
        index=False
    )

    # Validate saved data
    df_loaded = pd.read_parquet(output_path)
    pd.testing.assert_frame_equal(df, df_loaded)

    print("Load completed successfully!")
    print("Shape:", df_loaded.shape)
    print("File size:", output_path.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
