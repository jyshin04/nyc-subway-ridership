import pandas as pd
from pathlib import Path

# Define the list of station complexes inside the CRZ
stations_inside_crz = {
    "Astor Pl (6)", "Spring St (6)", "Wall St (4,5)", "Broadway (N,W)", "23 St (6)", "28 St (6)", "33 St (6)",
    "7 Av (B,Q)", "Houston St (1)", "Canal St (J,N,Q,R,W,Z,6)", "Bowery (J,Z)", "Grand St (B,D)",
    "Lexington Av-53 St (E,M)/51 St (6)", "Times Sq-42 St (N,Q,R,W,S,1,2,3,7)/42 St (A,C,E)",
    "34 St-Penn Station (1,2,3)", "47-50 Sts-Rockefeller Ctr (B,D,F,M)", "49 St (N,R,W)",
    "Broadway-Lafayette St (B,D,F,M)/Bleecker St (6)", "WTC Cortlandt (1)",
    "Chambers St (A,C)/WTC (E)/Park Pl (2,3)/Cortlandt (R,W)", "Delancey St (F)/Essex St (J,M,Z)",
    "14 St (A,C,E)/8 Av (L)", "Union St (R)", "Clark St (2,3)", "High St (A,C)", "Franklin St (1)",
    "Bowling Green (4,5)", "Court St (R)/Borough Hall (2,3,4,5)", "Wall St (2,3)", "Rector St (1)",
    "Canarsie-Rockaway Pkwy (L)", "Franklin Av (2,3,4,5)/Botanic Garden (S)", "Hoyt St (2,3)",
    "Sutter Av (L)", "Atlantic Av-Barclays Ctr (B,D,N,Q,R,2,3,4,5)", "New Lots Av (L)", "Wilson Av (L)",
    "Nostrand Av (A,C)", "Kingston-Throop Avs (C)", "Franklin Av (C,S)", "Lafayette Av (C)",
    "Clinton-Washington Avs (G)", "Broadway (G)", "Greenpoint Av (G)", "Nassau Av (G)", "Flushing Av (G)",
    "21 St (G)"
}

# Initialize dictionaries to store daily aggregates
inside_crz_daily = {}
outside_crz_daily = {}

# Process each year file
for year in range(2021, 2026):
    file_path = f"../data/raw/{year}.CSV"
    print(f"Loading {file_path}...")
    df = pd.read_csv(file_path, parse_dates=['transit_timestamp'])
    print(f"  → {len(df):,} records loaded.")

    # Extract just the date from timestamp
    df['date'] = df['transit_timestamp'].dt.date

    print(f"Processing station complexes for {year}...")
    for location, group in df.groupby('station_complex'):
        # Aggregate ridership per date
        daily = group.groupby('date')['ridership'].sum()

        # Add to the appropriate dictionary
        target_dict = inside_crz_daily if location in stations_inside_crz else outside_crz_daily
        for day, count in daily.items():
            target_dict[day] = target_dict.get(day, 0) + count

    print(f"Finished processing {year}.\n")

# Convert dictionaries to DataFrames
print("Converting aggregated data to DataFrames...")
inside_df = pd.DataFrame(sorted(inside_crz_daily.items()), columns=['date', 'total_ridership'])
outside_df = pd.DataFrame(sorted(outside_crz_daily.items()), columns=['date', 'total_ridership'])

# Save to CSV
print("Saving Inside_CRZ_Daily.CSV...")
inside_df.to_csv("Inside_CRZ_Daily.CSV", index=False)
print("Saving Outside_CRZ_Daily.CSV...")
outside_df.to_csv("Outside_CRZ_Daily.CSV", index=False)