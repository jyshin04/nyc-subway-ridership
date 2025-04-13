import pandas as pd
import glob

# Define years to process
years = range(2020, 2026)  # 2020 to 2025

for year in years:
    file_path = f"../data/{year}.csv"
    output_file = f"../processed_data/{year}_processed.csv"

    try:
        print(f"Processing {file_path}...")

        # Load CSV, handling tab separators if necessary
        with open(file_path, "r") as f:
            first_line = f.readline()
            delimiter = "\t" if "\t" in first_line else ","

        df = pd.read_csv(file_path, sep=delimiter, quotechar='"', encoding="utf-8")

        # Ensure column names match expected format
        expected_columns = [
            "transit_timestamp", "transit_mode", "station_complex_id", "station_complex",
            "borough", "payment_method", "fare_class_category", "ridership",
            "transfers", "latitude", "longitude", "Georeference"
        ]
        df = df[expected_columns]  # Drop unexpected columns if any exist

        # Convert timestamp to BigQuery-compatible format
        df["transit_timestamp"] = pd.to_datetime(df["transit_timestamp"], format="%m/%d/%Y %I:%M:%S %p", errors="coerce")

        # Convert numeric columns to proper types
        df["ridership"] = pd.to_numeric(df["ridership"], errors="coerce").fillna(0).astype(int)
        df["transfers"] = pd.to_numeric(df["transfers"], errors="coerce").fillna(0).astype(int)

        # Drop Georeference column 
        df.drop(columns=["Georeference"], inplace=True)

        # Remove rows with missing timestamps
        df = df.dropna(subset=["transit_timestamp"])

        # Save the cleaned CSV
        df.to_csv(output_file, index=False, encoding="utf-8")

        print(f"Successfully processed and saved: {output_file}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
