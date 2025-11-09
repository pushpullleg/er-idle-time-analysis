import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
import warnings
warnings.filterwarnings('ignore')

# ===== DATA LOADING & PREPROCESSING =====

df = pd.read_excel('CleanedData.xlsx')

# Convert timestamp columns to datetime
time_cols = ['Arrival Time', 'Registration Start', 'Registration End', 'Triage Start', 
             'Triage End', 'Doctor Seen', 'Exit Time']
for col in time_cols:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')

# ===== FEATURE ENGINEERING: WAIT TIME CALCULATIONS =====

# Time between key milestones (in minutes)
df['Wait_Registration'] = (df['Registration Start'] - df['Arrival Time']).dt.total_seconds() / 60
df['Wait_Triage'] = (df['Triage Start'] - df['Registration End']).dt.total_seconds() / 60
df['Wait_Provider'] = (df['Doctor Seen'] - df['Triage End']).dt.total_seconds() / 60
df['Total_Time_ER'] = (df['Exit Time'] - df['Arrival Time']).dt.total_seconds() / 60

# Shift-based features
df['Shift'] = df['Arrival Time'].dt.strftime('%H:%M').astype(str)
df['Hour'] = df['Arrival Time'].dt.hour
df['Day_of_Week'] = df['Arrival Time'].dt.day_name()
df['Date'] = df['Arrival Time'].dt.date

# ===== DESCRIPTIVE ANALYSIS =====

print("=" * 60)
print("MERIDIAN CITY ER - BASELINE METRICS (90-day period)")
print("=" * 60)

print(f"\nTotal Visits: {len(df)}")
print(f"Unique Patients: {df['Patient ID'].nunique()}")
print(f"Date Range: {df['Arrival Time'].min()} to {df['Arrival Time'].max()}")

print("\n--- WAIT TIME STATISTICS (minutes) ---")
print(f"Registration Wait (avg): {df['Wait_Registration'].mean():.1f}")
print(f"Triage Wait (avg): {df['Wait_Triage'].mean():.1f}")
print(f"Provider Wait (avg): {df['Wait_Provider'].mean():.1f}")
print(f"Total ER Time (avg): {df['Total_Time_ER'].mean():.1f}")

print(f"\nTotal ER Time (median): {df['Total_Time_ER'].median():.1f} min")
print(f"Total ER Time (95th %ile): {df['Total_Time_ER'].quantile(0.95):.1f} min")

# Wait times by triage level
print("\n--- WAIT TIMES BY TRIAGE LEVEL ---")
triage_wait = df.groupby('Triage Level Numeric')[['Wait_Provider', 'Total_Time_ER']].mean()
print(triage_wait)

# Wait times by shift
print("\n--- WAIT TIMES BY SHIFT ---")
shift_wait = df.groupby('Shift')[['Wait_Registration', 'Wait_Provider', 'Total_Time_ER']].mean()
print(shift_wait.sort_values('Total_Time_ER', ascending=False))

# ===== REGRESSION ANALYSIS: WHAT DRIVES LONG WAITS? =====

print("\n" + "=" * 60)
print("REGRESSION ANALYSIS: Root Cause Drivers")
print("=" * 60)

# Prepare features for modeling
df['Triage_Numeric'] = df['Triage Level Numeric']
df['Hour_sin'] = np.sin(2 * np.pi * df['Hour'] / 24)
df['Hour_cos'] = np.cos(2 * np.pi * df['Hour'] / 24)
df['Age_Group'] = pd.cut(df['Age'], bins=[0, 18, 35, 50, 65, 100], 
                         labels=['Child', 'Young Adult', 'Middle Age', 'Senior', 'Elderly'])

# Feature matrix
features = ['Triage_Numeric', 'Age', 'Hour_sin', 'Hour_cos']
X = df[features].dropna()
y = df.loc[X.index, 'Total_Time_ER']

# Random Forest for feature importance
rf_model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
rf_model.fit(X, y)

print("\nFeature Importance (What drives total ER wait time):")
importance_df = pd.DataFrame({
    'Feature': features,
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=False)
print(importance_df)

# Linear regression for coefficient interpretation
lr_model = LinearRegression()
lr_model.fit(X, y)
print("\nLinear Regression Coefficients:")
for feat, coef in zip(features, lr_model.coef_):
    print(f"  {feat}: {coef:.2f} min per unit")

# ===== CLUSTERING ANALYSIS: PATIENT COHORTS =====

print("\n" + "=" * 60)
print("CLUSTERING ANALYSIS: Patient Behavior Segments")
print("=" * 60)

cluster_features = ['Total_Time_ER', 'Triage_Numeric', 'Age']
X_cluster = df[cluster_features].dropna()

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df.loc[X_cluster.index, 'Cluster'] = kmeans.fit_predict(X_cluster)

print("\nCluster Profiles:")
for cluster in sorted(df['Cluster'].dropna().unique()):
    cluster_data = df[df['Cluster'] == cluster]
    print(f"\n  Cluster {int(cluster)}:")
    print(f"    Size: {len(cluster_data)} patients")
    print(f"    Avg Total Time: {cluster_data['Total_Time_ER'].mean():.1f} min")
    print(f"    Avg Triage Level: {cluster_data['Triage_Numeric'].mean():.1f}")
    print(f"    Avg Age: {cluster_data['Age'].mean():.1f}")

# ===== ANOMALY DETECTION: OPERATIONAL BREAKDOWNS =====

print("\n" + "=" * 60)
print("ANOMALY DETECTION: Outlier Days & Shifts")
print("=" * 60)

iso_forest = IsolationForest(contamination=0.1, random_state=42)
df['Anomaly'] = iso_forest.fit_predict(X_cluster)

anomalies = df[df['Anomaly'] == -1]
print(f"\nAnomalous visits detected: {len(anomalies)} ({100*len(anomalies)/len(df):.1f}%)")

print("\nTop 5 Anomalous Visit Characteristics:")
print(anomalies[['Date', 'Triage_Numeric', 'Total_Time_ER', 'Age']].head())

# ===== TIME SERIES: DAILY ARRIVAL PATTERN =====

print("\n" + "=" * 60)
print("DAILY PATTERNS & STAFFING ALIGNMENT")
print("=" * 60)

daily_stats = df.groupby('Date').agg({
    'Visit ID': 'count',
    'Total_Time_ER': 'mean',
    'Triage_Numeric': 'mean'
}).rename(columns={'Visit ID': 'Daily_Arrivals'})

print("\nAverage Daily Arrivals:", daily_stats['Daily_Arrivals'].mean())
print("Max Daily Arrivals:", daily_stats['Daily_Arrivals'].max())
print("Min Daily Arrivals:", daily_stats['Daily_Arrivals'].min())

print("\nHourly Arrival Distribution:")
hourly = df.groupby('Hour').size()
print(hourly)

# ===== KEY INSIGHTS & RECOMMENDATIONS =====

print("\n" + "=" * 60)
print("KEY INSIGHTS FOR HOSPITAL MANAGEMENT")
print("=" * 60)

slow_shift = shift_wait.sort_values('Total_Time_ER', ascending=False).index[0]
print(f"\n1. BOTTLENECK SHIFT: {slow_shift} has longest total ER time")
print(f"   Action: Review staffing levels during this shift")

high_triage_wait = triage_wait.sort_values('Wait_Provider', ascending=False)
print(f"\n2. HIGH-ACUITY PRIORITY: Triage {int(high_triage_wait.index[0])} waits longest for provider")
print(f"   Action: Dedicate senior physician during peak hours")

anomaly_pct = 100 * len(anomalies) / len(df)
print(f"\n3. OPERATIONAL VARIABILITY: {anomaly_pct:.1f}% visits are anomalous")
print(f"   Action: Investigate root causes of extreme outlier days")

print("\n" + "=" * 60)