import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = "../data/final/inside_outside_CRZ.csv"
df = pd.read_csv(file_path)

# Convert hour column to datetime
df['hour'] = pd.to_datetime(df['hour'])
df['year'] = df['hour'].dt.year
df['date'] = df['hour'].dt.date
df['hour_of_day'] = df['hour'].dt.hour

# Group by year, hour_of_day, and zone to compute average ridership
hourly_avg = df.groupby(['year', 'hour_of_day', 'zone'])['total_ridership'].mean().reset_index()

# Split into inside and outside
inside = hourly_avg[hourly_avg['zone'] == 'Inside']
outside = hourly_avg[hourly_avg['zone'] == 'Outside']

# --- Plot average hourly pattern for Inside CRZ ---
plt.figure(figsize=(12, 6))
for year in sorted(inside['year'].unique()):
    plt.plot(
        inside[inside['year'] == year]['hour_of_day'],
        inside[inside['year'] == year]['total_ridership'],
        label=f'Inside - {year}'
    )
plt.title("Average Hourly Subway Ridership (Inside CRZ) - Jan & Feb")
plt.xlabel("Hour of Day")
plt.ylabel("Avg Ridership")
plt.xticks(range(0, 24))
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("../visualizations/inside_crz_hourly_avg.png")
plt.close()

# --- Plot average hourly pattern for Outside CRZ ---
plt.figure(figsize=(12, 6))
for year in sorted(outside['year'].unique()):
    plt.plot(
        outside[outside['year'] == year]['hour_of_day'],
        outside[outside['year'] == year]['total_ridership'],
        label=f'Outside - {year}'
    )
plt.title("Average Hourly Subway Ridership (Outside CRZ) - Jan & Feb")
plt.xlabel("Hour of Day")
plt.ylabel("Avg Ridership")
plt.xticks(range(0, 24))
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("../visualizations/outside_crz_hourly_avg.png")
plt.close()

# --- Compare specific single days ---
comparison_days = ['2024-01-29', '2025-01-27']
single_day_df = df[df['date'].astype(str).isin(comparison_days)]

# Group by date, hour, zone
single_day_grouped = single_day_df.groupby(['date', 'hour_of_day', 'zone'])['total_ridership'].sum().reset_index()

# Plot for inside CRZ
inside_single = single_day_grouped[single_day_grouped['zone'] == 'Inside']
plt.figure(figsize=(12, 6))
for day in comparison_days:
    day_data = inside_single[inside_single['date'] == pd.to_datetime(day).date()]
    plt.plot(day_data['hour_of_day'], day_data['total_ridership'], label=f'Inside - {day}')
plt.title("Single Day Ridership Comparison (Inside CRZ)")
plt.xlabel("Hour of Day")
plt.ylabel("Ridership")
plt.xticks(range(0, 24))
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("../visualizations/single_day_inside_comparison.png")
plt.close()

# Plot for outside CRZ
outside_single = single_day_grouped[single_day_grouped['zone'] == 'Outside']
plt.figure(figsize=(12, 6))
for day in comparison_days:
    day_data = outside_single[outside_single['date'] == pd.to_datetime(day).date()]
    plt.plot(day_data['hour_of_day'], day_data['total_ridership'], label=f'Outside - {day}')
plt.title("Single Day Ridership Comparison (Outside CRZ)")
plt.xlabel("Hour of Day")
plt.ylabel("Ridership")
plt.xticks(range(0, 24))
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("../visualizations/single_day_outside_comparison.png")
plt.close()
