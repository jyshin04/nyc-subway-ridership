import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.linear_model import LinearRegression
import numpy as np

# Load hourly ridership data
df = pd.read_csv("../data/final/hourly_ridership.csv") 
df['hour'] = pd.to_datetime(df['hour'])
df = df[df['hour'] >= '2021-01-01'].copy()
df.sort_values('hour', inplace=True)

# Create time-based features
df['hour_of_day'] = df['hour'].dt.hour
df['day_of_week'] = df['hour'].dt.dayofweek

# One-hot encode cyclic features
df_encoded = pd.get_dummies(df, columns=['hour_of_day', 'day_of_week'], drop_first=True)

# Features just for cyclic patterns
cyclic_features = [col for col in df_encoded.columns if col.startswith('hour_of_day_') or col.startswith('day_of_week_')]

# Fit linear model to capture cyclic trends only
model = LinearRegression()
model.fit(df_encoded[cyclic_features], df_encoded['total_ridership'])

# Predict cyclic component
df['cyclic_component'] = model.predict(df_encoded[cyclic_features])

# Remove cyclic component from actual ridership
df['residual_ridership'] = df['total_ridership'] - df['cyclic_component']

# Save plots
os.makedirs('plots', exist_ok=True)
df.set_index('hour', inplace=True)
df.index = df.index.tz_localize(None)  # Remove tz info if any

# Split for plotting
split_date = pd.to_datetime('2025-01-05')
df_pre2025 = df.loc[df.index <= split_date]
df_post2025 = df.loc[df.index > split_date]

# Plot: Cyclic component
plt.figure(figsize=(14, 5))
plt.plot(df.index, df['cyclic_component'], color='purple', label='Estimated Cyclic Component', linewidth=1)
plt.title('Estimated Hourly + Weekly Cyclic Trend')
plt.xlabel('Date')
plt.ylabel('Ridership (Cyclic Component)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("plots/hourly_cyclic_component.png", dpi=150)
plt.close()

# Plot: Residual ridership (no cycles)
plt.figure(figsize=(14, 5))
plt.plot(df_pre2025.index, df_pre2025['residual_ridership'], color='gray', linewidth=1, label='Residual (pre-2025)')
plt.plot(df_post2025.index, df_post2025['residual_ridership'], color='orange', linewidth=1, label='Residual (post-2025)')
plt.axvline(split_date, linestyle='--', color='black', label='Policy Start')
plt.title('Hourly Ridership (Cyclic-Adjusted / Detrended)')
plt.xlabel('Date')
plt.ylabel('Ridership without Cyclic Trend')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("plots/hourly_cyclic_detrended.png", dpi=150)
plt.close()