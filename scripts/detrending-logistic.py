import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

# 1. Load Data
df = pd.read_csv('../data/final/daily_ridership.csv')  
df['date'] = pd.to_datetime(df['date'])
df = df[df['date'] >= '2021-01-01'].copy()
df = df.sort_values('date').reset_index(drop=True)

# 2. Pre-policy subset (2021–2024)
df_pre_policy = df.loc[df['date'] < '2025-01-01'].copy()
df_pre_policy = df_pre_policy.sort_values('date').reset_index(drop=True)

start_date = pd.to_datetime('2021-01-01')
df_pre_policy['time_index'] = (df_pre_policy['date'] - start_date).dt.days

# 3. Define the logistic function
def logistic(t, K, b, t0):
    """A 3-parameter logistic curve."""
    return K / (1 + np.exp(-b * (t - t0)))

# 4. Initial Guesses
#    - K: set near the max ridership from the pre-policy period (plus some buffer).
#    - b: small positive value as a starting guess for the growth rate.
#    - t0: near the midpoint of the pre-policy range in 'time_index'.
y_data = df_pre_policy['total_ridership'].values
x_data = df_pre_policy['time_index'].values

K_init = y_data.max() * 1.2  # add ~20% buffer above observed max
b_init = 0.01               # tune if needed
t0_init = (x_data.min() + x_data.max()) / 2

initial_guesses = [K_init, b_init, t0_init]

# 5. Curve Fit on the pre-policy data
popt, pcov = curve_fit(logistic, x_data, y_data, p0=initial_guesses, maxfev=10000)
K_hat, b_hat, t0_hat = popt

# 6. Apply the logistic model to the entire dataset
df['time_index'] = (df['date'] - start_date).dt.days
df['fitted_logistic'] = logistic(df['time_index'], K_hat, b_hat, t0_hat)

# 7. Detrend: actual minus fitted logistic
df['detrended_logistic'] = df['total_ridership'] - df['fitted_logistic']

# 8. Evaluate R^2 on the 2021–2024 subset
y_pred_pre = logistic(x_data, K_hat, b_hat, t0_hat)
r2_logistic = r2_score(y_data, y_pred_pre)

print("Logistic Curve Fit (2021–2024) Parameters:")
print(f"  K      (capacity): {K_hat:,.2f}")
print(f"  b      (growth rate): {b_hat:,.5f}")
print(f"  t0     (inflection day): {t0_hat:,.2f}")
print(f"  R^2 on 2021–2024 subset: {r2_logistic:.4f}\n")

# 9. Create plots folder if needed
if not os.path.exists('plots'):
    os.makedirs('plots')

# 10. Plot: Original ridership vs. logistic trend
plt.figure(figsize=(10, 5))

split_date = pd.to_datetime('2025-01-05')  # for color separation
df_pre2025 = df[df['date'] <= split_date]
df_post2025 = df[df['date'] > split_date]

# Plot daily ridership in gray/orange
plt.plot(df_pre2025['date'], df_pre2025['total_ridership'],
         color='gray', linewidth=1, label='Daily Ridership (pre-2025)')
plt.plot(df_post2025['date'], df_post2025['total_ridership'],
         color='orange', linewidth=1, label='Daily Ridership (post-2025)')

# Plot logistic curve in dark orange
plt.plot(df['date'], df['fitted_logistic'],
         color='darkorange', linewidth=2, label='Logistic Trend (2021–2024)')

plt.axvline(pd.to_datetime('2025-01-01'), linestyle='--', color='black', label='Policy Start')

plt.title('Daily Ridership with Logistic Growth Curve Fit (2021–2024)')
plt.xlabel('Date')
plt.ylabel('Total Ridership')
plt.legend()
plt.savefig('plots/original_vs_logistic.png', dpi=150)
plt.close()

# 11. Plot: Detrended logistic
plt.figure(figsize=(10, 5))
plt.plot(df_pre2025['date'], df_pre2025['detrended_logistic'],
         color='gray', linewidth=1, label='Detrended Ridership (pre-2025)')
plt.plot(df_post2025['date'], df_post2025['detrended_logistic'],
         color='orange', linewidth=1, label='Detrended Ridership (post-2025)')

plt.axvline(pd.to_datetime('2025-01-01'), linestyle='--', color='black', label='Policy Start')
plt.title('Detrended Ridership (Logistic Baseline)')
plt.xlabel('Date')
plt.ylabel('Detrended Ridership')
plt.legend()
plt.savefig('plots/detrended_logistic.png', dpi=150)
plt.close()
