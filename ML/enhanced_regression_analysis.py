"""
ENHANCED REGRESSION ANALYSIS: ROOT CAUSE QUANTIFICATION WITH REAL OPERATIONAL DATA
====================================================================================
Purpose: Determine which operational variables most strongly predict ER wait times
Data Sources: Merges Visits, Staffing, Facility, Outcome, and Patient data
Methods: Multiple Linear Regression, Random Forest, Gradient Boosting (XGBoost)
Deliverable: "Staffing shortfall accounts for X% of wait time variance"
====================================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

# Try to import XGBoost
try:
    import xgboost as xgb
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False
    print("⚠ XGBoost not installed. Install with: pip install xgboost")

# Set styling
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

print("=" * 80)
print("ENHANCED REGRESSION ANALYSIS: ROOT CAUSE QUANTIFICATION")
print("=" * 80)

# ============================================================================
# 1. DATA LOADING & MERGING
# ============================================================================

print("\n[1] LOADING AND MERGING OPERATIONAL DATA...")

# Load all datasets
visits_df = pd.read_csv('Cleaned/Hospital_visits_out.csv')
staffing_df = pd.read_csv('Cleaned/Hospital_Staffing_out.csv')
facility_df = pd.read_csv('Cleaned/Hospital_facility_out.csv')
outcome_df = pd.read_csv('Cleaned/Hospital_outcome_out.csv')
patients_df = pd.read_csv('Cleaned/Hospital_patients_out.csv')

print(f"✓ Loaded {len(visits_df):,} visits")
print(f"✓ Loaded {len(staffing_df):,} staffing records")
print(f"✓ Loaded {len(facility_df):,} facility records")
print(f"✓ Loaded {len(outcome_df):,} outcome records")
print(f"✓ Loaded {len(patients_df):,} patient records")

# Convert timestamps
time_cols = ['Arrival Time', 'Registration Start', 'Registration End', 
             'Triage Start', 'Triage End', 'Doctor Seen', 'Exit Time']
for col in time_cols:
    if col in visits_df.columns:
        visits_df[col] = pd.to_datetime(visits_df[col], errors='coerce')

# Convert staffing date
staffing_df['Staff Date'] = pd.to_datetime(staffing_df['Staff Date'])

# Merge datasets
print("\n[2] MERGING DATASETS...")

# Start with visits
df = visits_df.copy()

# Merge with patients
df = df.merge(patients_df, on='Patient ID', how='left')
print(f"✓ Merged patient demographics ({len(df):,} records)")

# Merge with outcomes
df = df.merge(outcome_df, on='Visit ID', how='left')
print(f"✓ Merged outcomes ({len(df):,} records)")

# Merge with facility
df = df.merge(facility_df, on='Hospital ID', how='left')
print(f"✓ Merged facility data ({len(df):,} records)")

# Merge with staffing (by date and shift)
df['Visit_Date'] = df['Arrival Time'].dt.date
df['Visit_Date'] = pd.to_datetime(df['Visit_Date'])
staffing_df['Staff Date'] = pd.to_datetime(staffing_df['Staff Date'])

# Rename staffing columns to avoid conflicts with facility
staffing_df = staffing_df.rename(columns={'Fast Track Beds': 'Fast_Track_Staffed'})

df = df.merge(
    staffing_df, 
    left_on=['Visit_Date', 'Arrived At Shift'], 
    right_on=['Staff Date', 'Shift'],
    how='left',
    suffixes=('', '_staffing')
)
print(f"✓ Merged staffing data ({len(df):,} records)")

# ============================================================================
# 3. FEATURE ENGINEERING: OPERATIONAL VARIABLES
# ============================================================================

print("\n[3] ENGINEERING OPERATIONAL FEATURES...")

# TARGET VARIABLE: Total ER wait time (minutes)
df['Total_Wait_Time'] = (df['Exit Time'] - df['Arrival Time']).dt.total_seconds() / 60

# Wait time components
df['Registration_Wait'] = (df['Registration Start'] - df['Arrival Time']).dt.total_seconds() / 60
df['Triage_Wait'] = (df['Triage Start'] - df['Registration End']).dt.total_seconds() / 60
df['Provider_Wait'] = (df['Doctor Seen'] - df['Triage End']).dt.total_seconds() / 60
df['Discharge_Wait'] = (df['Exit Time'] - df['Doctor Seen']).dt.total_seconds() / 60

# REAL OPERATIONAL VARIABLES FROM STAFFING DATA
print("\n✓ Using REAL operational variables:")
print(f"  - Nurses On Duty: {df['Nurses On Duty'].notna().sum():,} records")
print(f"  - Doctors On Duty: {df['Doctors On Duty'].notna().sum():,} records")
print(f"  - Specialists On Call: {df['Specialists On Call'].notna().sum():,} records")
print(f"  - Fast Track Beds (Facility): {df['Fast Track Beds'].notna().sum():,} records")
print(f"  - Fast Track Staffed: {df['Fast_Track_Staffed'].notna().sum():,} records")

# Staffing ratios (key operational metrics)
df['Patients_Per_Nurse'] = df.groupby(['Visit_Date', 'Arrived At Shift'])['Visit ID'].transform('count') / df['Nurses On Duty']
df['Patients_Per_Doctor'] = df.groupby(['Visit_Date', 'Arrived At Shift'])['Visit ID'].transform('count') / df['Doctors On Duty']

# Temporal features
df['Hour'] = df['Arrival Time'].dt.hour
df['Day_of_Week'] = df['Arrival Time'].dt.dayofweek
df['Is_Weekend'] = (df['Day_of_Week'] >= 5).astype(int)
df['Is_Night_Shift'] = (df['Arrived At Shift'] == 'NIGHT').astype(int)
df['Is_Evening_Shift'] = (df['Arrived At Shift'] == 'EVENING').astype(int)

# Peak hour indicators
df['Is_Peak_Hours'] = ((df['Hour'] >= 8) & (df['Hour'] <= 11)).astype(int)
df['Is_Off_Peak'] = ((df['Hour'] >= 22) | (df['Hour'] <= 5)).astype(int)

# Volume/Load features
df['Hourly_Volume'] = df.groupby([df['Arrival Time'].dt.date, df['Hour']])['Visit ID'].transform('count')
df['Daily_Volume'] = df.groupby(df['Arrival Time'].dt.date)['Visit ID'].transform('count')

# ER Capacity utilization
df['Bed_Utilization_Rate'] = df['Hourly_Volume'] / df['Facility Size (Beds)']

# Encode categorical variables
le_triage = LabelEncoder()
le_disposition = LabelEncoder()
le_gender = LabelEncoder()
le_insurance = LabelEncoder()
le_hospital = LabelEncoder()

df['Triage_Numeric'] = le_triage.fit_transform(df['Triage Level'].fillna('unknown'))
df['Disposition_Numeric'] = le_disposition.fit_transform(df['Disposition'].fillna('unknown'))
df['Gender_Numeric'] = le_gender.fit_transform(df['Gender'].fillna('unknown'))
df['Insurance_Numeric'] = le_insurance.fit_transform(df['Insurance'].fillna('unknown'))
df['Hospital_Numeric'] = le_hospital.fit_transform(df['Hospital ID'].fillna('unknown'))

print(f"\n✓ Total features engineered: {len(df.columns)}")

# ============================================================================
# 4. PREPARE DATA FOR MODELING
# ============================================================================

print("\n[4] PREPARING DATA FOR REGRESSION MODELS...")

# Select features for modeling
operational_features = [
    # REAL STAFFING VARIABLES
    'Nurses On Duty',
    'Doctors On Duty',
    'Specialists On Call',
    'Fast_Track_Staffed',
    'Patients_Per_Nurse',
    'Patients_Per_Doctor',
    
    # FACILITY VARIABLES
    'Facility Size (Beds)',
    'ICU Beds',
    'Regular Beds',
    'Fast Track Beds',
    'Bed_Utilization_Rate',
    
    # PATIENT/CLINICAL VARIABLES
    'Age',
    'Triage_Numeric',
    'Gender_Numeric',
    'Insurance_Numeric',
    
    # VOLUME/DEMAND VARIABLES
    'Hourly_Volume',
    'Daily_Volume',
    
    # TEMPORAL VARIABLES
    'Hour',
    'Day_of_Week',
    'Is_Weekend',
    'Is_Night_Shift',
    'Is_Evening_Shift',
    'Is_Peak_Hours',
    'Is_Off_Peak',
    
    # HOSPITAL
    'Hospital_Numeric'
]

# Create feature matrix
X = df[operational_features].copy()
y = df['Total_Wait_Time'].copy()

# Remove rows with missing values
valid_idx = X.notna().all(axis=1) & y.notna()
X = X[valid_idx]
y = y[valid_idx]

print(f"✓ Feature matrix: {X.shape[0]:,} samples × {X.shape[1]} features")
print(f"✓ Target variable: {len(y):,} wait times")
print(f"\nTarget Statistics:")
print(f"  Mean wait time: {y.mean():.1f} minutes")
print(f"  Median wait time: {y.median():.1f} minutes")
print(f"  Std dev: {y.std():.1f} minutes")
print(f"  Min: {y.min():.1f} minutes")
print(f"  Max: {y.max():.1f} minutes")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\n✓ Train set: {len(X_train):,} samples")
print(f"✓ Test set: {len(X_test):,} samples")

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ============================================================================
# 5. MODEL 1: MULTIPLE LINEAR REGRESSION
# ============================================================================

print("\n" + "=" * 80)
print("[5] MODEL 1: MULTIPLE LINEAR REGRESSION")
print("=" * 80)

lr_model = LinearRegression()
lr_model.fit(X_train_scaled, y_train)

y_pred_lr = lr_model.predict(X_test_scaled)

lr_r2 = r2_score(y_test, y_pred_lr)
lr_rmse = np.sqrt(mean_squared_error(y_test, y_pred_lr))
lr_mae = mean_absolute_error(y_test, y_pred_lr)

print(f"\nPerformance Metrics:")
print(f"  R² Score: {lr_r2:.4f} ({lr_r2*100:.2f}% variance explained)")
print(f"  RMSE: {lr_rmse:.2f} minutes")
print(f"  MAE: {lr_mae:.2f} minutes")

# Feature coefficients
coef_df = pd.DataFrame({
    'Feature': operational_features,
    'Coefficient': lr_model.coef_,
    'Abs_Coefficient': np.abs(lr_model.coef_)
}).sort_values('Abs_Coefficient', ascending=False)

print("\nTop 10 Most Impactful Features (Linear Model):")
print("=" * 80)
for idx, row in coef_df.head(10).iterrows():
    impact = "increases" if row['Coefficient'] > 0 else "decreases"
    print(f"  {row['Feature']:.<40} {impact} wait by {abs(row['Coefficient']):>6.2f} min/unit")

# ============================================================================
# 6. MODEL 2: RANDOM FOREST REGRESSION
# ============================================================================

print("\n" + "=" * 80)
print("[6] MODEL 2: RANDOM FOREST REGRESSION")
print("=" * 80)

rf_model = RandomForestRegressor(
    n_estimators=100,
    max_depth=15,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1
)

print("\nTraining Random Forest...")
rf_model.fit(X_train, y_train)

y_pred_rf = rf_model.predict(X_test)

rf_r2 = r2_score(y_test, y_pred_rf)
rf_rmse = np.sqrt(mean_squared_error(y_test, y_pred_rf))
rf_mae = mean_absolute_error(y_test, y_pred_rf)

print(f"\nPerformance Metrics:")
print(f"  R² Score: {rf_r2:.4f} ({rf_r2*100:.2f}% variance explained)")
print(f"  RMSE: {rf_rmse:.2f} minutes")
print(f"  MAE: {rf_mae:.2f} minutes")

# Feature importances
importance_df = pd.DataFrame({
    'Feature': operational_features,
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=False)

print("\nTop 10 Most Important Features (Random Forest):")
print("=" * 80)
for idx, row in importance_df.head(10).iterrows():
    print(f"  {row['Feature']:.<40} {row['Importance']*100:>6.2f}%")

# ============================================================================
# 7. MODEL 3: GRADIENT BOOSTING REGRESSION
# ============================================================================

print("\n" + "=" * 80)
print("[7] MODEL 3: GRADIENT BOOSTING (Sklearn)")
print("=" * 80)

gb_model = GradientBoostingRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42
)

print("\nTraining Gradient Boosting...")
gb_model.fit(X_train, y_train)

y_pred_gb = gb_model.predict(X_test)

gb_r2 = r2_score(y_test, y_pred_gb)
gb_rmse = np.sqrt(mean_squared_error(y_test, y_pred_gb))
gb_mae = mean_absolute_error(y_test, y_pred_gb)

print(f"\nPerformance Metrics:")
print(f"  R² Score: {gb_r2:.4f} ({gb_r2*100:.2f}% variance explained)")
print(f"  RMSE: {gb_rmse:.2f} minutes")
print(f"  MAE: {gb_mae:.2f} minutes")

# Feature importances
gb_importance_df = pd.DataFrame({
    'Feature': operational_features,
    'Importance': gb_model.feature_importances_
}).sort_values('Importance', ascending=False)

print("\nTop 10 Most Important Features (Gradient Boosting):")
print("=" * 80)
for idx, row in gb_importance_df.head(10).iterrows():
    print(f"  {row['Feature']:.<40} {row['Importance']*100:>6.2f}%")

# ============================================================================
# 8. XGBOOST (if available)
# ============================================================================

if HAS_XGBOOST:
    print("\n" + "=" * 80)
    print("[8] MODEL 4: XGBOOST REGRESSION")
    print("=" * 80)
    
    xgb_model = xgb.XGBRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42,
        n_jobs=-1
    )
    
    print("\nTraining XGBoost...")
    xgb_model.fit(X_train, y_train)
    
    y_pred_xgb = xgb_model.predict(X_test)
    
    xgb_r2 = r2_score(y_test, y_pred_xgb)
    xgb_rmse = np.sqrt(mean_squared_error(y_test, y_pred_xgb))
    xgb_mae = mean_absolute_error(y_test, y_pred_xgb)
    
    print(f"\nPerformance Metrics:")
    print(f"  R² Score: {xgb_r2:.4f} ({xgb_r2*100:.2f}% variance explained)")
    print(f"  RMSE: {xgb_rmse:.2f} minutes")
    print(f"  MAE: {xgb_mae:.2f} minutes")
    
    # Feature importances
    xgb_importance_df = pd.DataFrame({
        'Feature': operational_features,
        'Importance': xgb_model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    print("\nTop 10 Most Important Features (XGBoost):")
    print("=" * 80)
    for idx, row in xgb_importance_df.head(10).iterrows():
        print(f"  {row['Feature']:.<40} {row['Importance']*100:>6.2f}%")

# ============================================================================
# 9. MODEL COMPARISON
# ============================================================================

print("\n" + "=" * 80)
print("[9] MODEL COMPARISON SUMMARY")
print("=" * 80)

comparison_data = {
    'Model': ['Linear Regression', 'Random Forest', 'Gradient Boosting'],
    'R² Score': [lr_r2, rf_r2, gb_r2],
    'RMSE (min)': [lr_rmse, rf_rmse, gb_rmse],
    'MAE (min)': [lr_mae, rf_mae, gb_mae]
}

if HAS_XGBOOST:
    comparison_data['Model'].append('XGBoost')
    comparison_data['R² Score'].append(xgb_r2)
    comparison_data['RMSE (min)'].append(xgb_rmse)
    comparison_data['MAE (min)'].append(xgb_mae)

comparison_df = pd.DataFrame(comparison_data)
comparison_df = comparison_df.sort_values('R² Score', ascending=False)

print("\n" + comparison_df.to_string(index=False))

best_model = comparison_df.iloc[0]['Model']
best_r2 = comparison_df.iloc[0]['R² Score']

print(f"\n🏆 BEST MODEL: {best_model}")
print(f"   Explains {best_r2*100:.2f}% of wait time variance")

# ============================================================================
# 10. KEY INSIGHTS & VARIANCE DECOMPOSITION
# ============================================================================

print("\n" + "=" * 80)
print("[10] ROOT CAUSE ANALYSIS: VARIANCE DECOMPOSITION")
print("=" * 80)

# Use best performing model's feature importances
if best_model == 'Random Forest':
    top_features = importance_df.head(10)
elif best_model == 'Gradient Boosting':
    top_features = gb_importance_df.head(10)
elif best_model == 'XGBoost' and HAS_XGBOOST:
    top_features = xgb_importance_df.head(10)
else:
    top_features = coef_df.head(10)

# Categorize features
staffing_features = ['Nurses On Duty', 'Doctors On Duty', 'Specialists On Call', 
                     'Patients_Per_Nurse', 'Patients_Per_Doctor', 'Fast_Track_Staffed']
facility_features = ['Facility Size (Beds)', 'ICU Beds', 'Regular Beds', 
                    'Fast Track Beds', 'Bed_Utilization_Rate']
volume_features = ['Hourly_Volume', 'Daily_Volume']
clinical_features = ['Age', 'Triage_Numeric', 'Gender_Numeric', 'Insurance_Numeric']
temporal_features = ['Hour', 'Day_of_Week', 'Is_Weekend', 'Is_Night_Shift', 
                    'Is_Evening_Shift', 'Is_Peak_Hours', 'Is_Off_Peak']

# Calculate category contributions
staffing_importance = importance_df[importance_df['Feature'].isin(staffing_features)]['Importance'].sum()
facility_importance = importance_df[importance_df['Feature'].isin(facility_features)]['Importance'].sum()
volume_importance = importance_df[importance_df['Feature'].isin(volume_features)]['Importance'].sum()
clinical_importance = importance_df[importance_df['Feature'].isin(clinical_features)]['Importance'].sum()
temporal_importance = importance_df[importance_df['Feature'].isin(temporal_features)]['Importance'].sum()

print("\n📊 VARIANCE DECOMPOSITION BY CATEGORY:")
print("=" * 80)
print(f"  Staffing Variables........... {staffing_importance*100:>6.2f}%")
print(f"  Facility/Bed Availability.... {facility_importance*100:>6.2f}%")
print(f"  Patient Volume/Demand........ {volume_importance*100:>6.2f}%")
print(f"  Clinical Factors............. {clinical_importance*100:>6.2f}%")
print(f"  Temporal Patterns............ {temporal_importance*100:>6.2f}%")

# ============================================================================
# 11. ACTIONABLE RECOMMENDATIONS
# ============================================================================

print("\n" + "=" * 80)
print("[11] ACTIONABLE RECOMMENDATIONS (ROI PRIORITIZATION)")
print("=" * 80)

print("\n🎯 TOP 3 OPERATIONAL LEVERS TO PULL:")
print("-" * 80)

recommendations = []

# Analyze top features
for idx, row in importance_df.head(3).iterrows():
    feature = row['Feature']
    importance = row['Importance']
    
    if feature in staffing_features:
        if 'Nurse' in feature:
            print(f"\n1. STAFFING OPTIMIZATION - NURSES ({importance*100:.1f}% impact)")
            print(f"   Current avg: {df['Nurses On Duty'].mean():.1f} nurses per shift")
            print(f"   Current patient/nurse ratio: {df['Patients_Per_Nurse'].mean():.1f}:1")
            print(f"   💡 Action: Increase nurse staffing during peak hours (8-11 AM)")
            print(f"   💰 Expected ROI: {importance*100:.1f}% reduction in wait times")
        elif 'Doctor' in feature:
            print(f"\n2. PHYSICIAN CAPACITY ({importance*100:.1f}% impact)")
            print(f"   Current avg: {df['Doctors On Duty'].mean():.1f} doctors per shift")
            print(f"   Current patient/doctor ratio: {df['Patients_Per_Doctor'].mean():.1f}:1")
            print(f"   💡 Action: Add 1-2 physicians during EVENING/NIGHT shifts")
            print(f"   💰 Expected ROI: {importance*100:.1f}% reduction in wait times")
    
    elif feature in facility_features:
        if 'Bed' in feature:
            print(f"\n3. BED AVAILABILITY/TURNOVER ({importance*100:.1f}% impact)")
            print(f"   Current bed utilization: {df['Bed_Utilization_Rate'].mean()*100:.1f}%")
            print(f"   💡 Action: Improve discharge processes to increase bed turnover")
            print(f"   💰 Expected ROI: {importance*100:.1f}% reduction in wait times")
    
    elif feature in volume_features:
        print(f"\n{len(recommendations)+1}. DEMAND MANAGEMENT ({importance*100:.1f}% impact)")
        print(f"   💡 Action: Implement patient scheduling/diversion during peak hours")
        print(f"   💰 Expected ROI: {importance*100:.1f}% reduction in wait times")

# ============================================================================
# 12. VISUALIZATIONS
# ============================================================================

print("\n[12] Generating visualizations...")

# Create figure with subplots
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Plot 1: Feature Importance
top_10 = importance_df.head(10)
axes[0, 0].barh(range(len(top_10)), top_10['Importance'], color='steelblue')
axes[0, 0].set_yticks(range(len(top_10)))
axes[0, 0].set_yticklabels(top_10['Feature'])
axes[0, 0].set_xlabel('Importance')
axes[0, 0].set_title(f'Top 10 Features Driving ER Wait Times ({best_model})', fontweight='bold')
axes[0, 0].invert_yaxis()

# Plot 2: Model Comparison
axes[0, 1].bar(comparison_df['Model'], comparison_df['R² Score'], color=['coral', 'steelblue', 'lightgreen', 'orange'][:len(comparison_df)])
axes[0, 1].set_ylabel('R² Score')
axes[0, 1].set_title('Model Performance Comparison', fontweight='bold')
axes[0, 1].set_ylim([0, 1])
for i, (model, r2) in enumerate(zip(comparison_df['Model'], comparison_df['R² Score'])):
    axes[0, 1].text(i, r2 + 0.02, f'{r2:.3f}', ha='center', fontweight='bold')

# Plot 3: Variance Decomposition
categories = ['Staffing', 'Facility/Beds', 'Volume', 'Clinical', 'Temporal']
values = [staffing_importance, facility_importance, volume_importance, 
          clinical_importance, temporal_importance]
colors_pie = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
axes[1, 0].pie(values, labels=categories, autopct='%1.1f%%', startangle=90, colors=colors_pie)
axes[1, 0].set_title('Wait Time Variance by Category', fontweight='bold')

# Plot 4: Actual vs Predicted (best model)
if best_model == 'Random Forest':
    y_pred_best = y_pred_rf
elif best_model == 'Gradient Boosting':
    y_pred_best = y_pred_gb
elif best_model == 'XGBoost':
    y_pred_best = y_pred_xgb
else:
    y_pred_best = y_pred_lr

axes[1, 1].scatter(y_test, y_pred_best, alpha=0.3, s=10)
axes[1, 1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
axes[1, 1].set_xlabel('Actual Wait Time (minutes)')
axes[1, 1].set_ylabel('Predicted Wait Time (minutes)')
axes[1, 1].set_title(f'Actual vs Predicted Wait Times ({best_model})', fontweight='bold')
axes[1, 1].text(0.05, 0.95, f'R² = {best_r2:.3f}', transform=axes[1, 1].transAxes, 
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('regression_analysis_results.png', dpi=300, bbox_inches='tight')
print("✓ Saved visualization to 'regression_analysis_results.png'")

plt.show()

# ============================================================================
# 13. EXPORT RESULTS
# ============================================================================

print("\n[13] Exporting results...")

# Save feature importance
importance_df.to_csv('feature_importance.csv', index=False)
print("✓ Saved feature importance to 'feature_importance.csv'")

# Save model comparison
comparison_df.to_csv('model_comparison.csv', index=False)
print("✓ Saved model comparison to 'model_comparison.csv'")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE!")
print("=" * 80)
