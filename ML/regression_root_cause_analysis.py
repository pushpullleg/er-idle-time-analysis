"""
REGRESSION ANALYSIS: ROOT CAUSE QUANTIFICATION OF ER WAIT TIMES
================================================================================
Purpose: Determine which operational variables most strongly predict wait times
Methods: Multiple Linear Regression, Random Forest, Gradient Boosting (XGBoost)
Deliverable: Quantify which operational levers to pull for maximum ROI
================================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

# Try to import XGBoost (optional)
try:
    from xgboost import XGBRegressor
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("⚠ XGBoost not installed. Install with: pip install xgboost")

# Set styling
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

print("=" * 80)
print("REGRESSION ANALYSIS: ROOT CAUSE QUANTIFICATION OF ER WAIT TIMES")
print("=" * 80)

# ============================================================================
# 1. DATA LOADING & PREPROCESSING
# ============================================================================

print("\n[1] LOADING DATA...")
df = pd.read_excel('CleanedData.xlsx')

# Convert timestamp columns to datetime
time_cols = ['Arrival Time', 'Registration Start', 'Registration End', 
             'Triage Start', 'Triage End', 'Doctor Seen', 'Exit Time']
for col in time_cols:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')

print(f"✓ Loaded {len(df):,} patient visits")

# ============================================================================
# 2. FEATURE ENGINEERING: OPERATIONAL VARIABLES
# ============================================================================

print("\n[2] ENGINEERING OPERATIONAL FEATURES...")

# Target variable: Total ER wait time
df['Total_Wait_Time'] = (df['Exit Time'] - df['Arrival Time']).dt.total_seconds() / 60

# Wait time components
df['Registration_Wait'] = (df['Registration Start'] - df['Arrival Time']).dt.total_seconds() / 60
df['Triage_Wait'] = (df['Triage Start'] - df['Registration End']).dt.total_seconds() / 60
df['Provider_Wait'] = (df['Doctor Seen'] - df['Triage End']).dt.total_seconds() / 60
df['Discharge_Wait'] = (df['Exit Time'] - df['Doctor Seen']).dt.total_seconds() / 60

# Temporal features
df['Hour'] = df['Arrival Time'].dt.hour
df['Day_of_Week'] = df['Arrival Time'].dt.dayofweek  # 0=Monday, 6=Sunday
df['Is_Weekend'] = (df['Day_of_Week'] >= 5).astype(int)
df['Is_Night_Shift'] = ((df['Hour'] >= 23) | (df['Hour'] < 7)).astype(int)
df['Is_Peak_Hours'] = ((df['Hour'] >= 8) & (df['Hour'] <= 12)).astype(int)

# Patient volume proxy: arrivals in same hour
df['Hourly_Volume'] = df.groupby([df['Arrival Time'].dt.date, 'Hour'])['Visit ID'].transform('count')

# Daily volume
df['Daily_Volume'] = df.groupby(df['Arrival Time'].dt.date)['Visit ID'].transform('count')

# Acuity level
df['Acuity_Level'] = df['Triage Level Numeric']

# Patient demographics
df['Age_Group'] = pd.cut(df['Age'], bins=[0, 18, 35, 50, 65, 100], 
                         labels=['Pediatric', 'Young_Adult', 'Middle_Age', 'Senior', 'Elderly'])

# Encode categorical variables
le_insurance = LabelEncoder()
df['Insurance_Encoded'] = le_insurance.fit_transform(df['Insurance'].fillna('Unknown'))

le_gender = LabelEncoder()
df['Gender_Encoded'] = le_gender.fit_transform(df['Gender'].fillna('Unknown'))

# Staffing proxy: inverse of hourly volume (lower staff-to-patient ratio = higher volume)
df['Staffing_Pressure'] = df['Hourly_Volume'] / df['Hourly_Volume'].mean()

# Bed availability proxy: cumulative patients in ER at any time
# Simplified: assume patients in ER = arrivals - exits up to that point in the day
df_sorted = df.sort_values('Arrival Time')
df_sorted['Cumulative_Arrivals'] = df_sorted.groupby(df_sorted['Arrival Time'].dt.date).cumcount() + 1
# Estimate exits (patients who have left by this time on same day)
df_sorted['Estimated_Current_Load'] = df_sorted['Cumulative_Arrivals']  # Simplified proxy

# Merge back
df['ER_Load'] = df_sorted['Estimated_Current_Load']

print("✓ Created operational features:")
print("  - Wait time components (Registration, Triage, Provider, Discharge)")
print("  - Temporal features (Hour, Day, Weekend, Night shift, Peak hours)")
print("  - Volume features (Hourly volume, Daily volume)")
print("  - Staffing pressure proxy")
print("  - ER load/bed availability proxy")
print("  - Patient acuity and demographics")

# ============================================================================
# 3. PREPARE MODELING DATASET
# ============================================================================

print("\n[3] PREPARING MODELING DATASET...")

# Select features for modeling
feature_cols = [
    'Acuity_Level',           # Clinical complexity
    'Age',                    # Patient demographics
    'Gender_Encoded',
    'Insurance_Encoded',
    'Hourly_Volume',          # Patient volume
    'Daily_Volume',
    'Staffing_Pressure',      # Staffing adequacy proxy
    'ER_Load',                # Bed availability proxy
    'Registration_Wait',      # Process bottlenecks
    'Triage_Wait',
    'Provider_Wait',
    'Hour',                   # Temporal patterns
    'Day_of_Week',
    'Is_Weekend',
    'Is_Night_Shift',
    'Is_Peak_Hours'
]

# Create clean dataset
df_model = df[feature_cols + ['Total_Wait_Time']].dropna()

X = df_model[feature_cols]
y = df_model['Total_Wait_Time']

print(f"✓ Final dataset: {len(X):,} complete records")
print(f"✓ Features: {len(feature_cols)}")
print(f"✓ Target: Total Wait Time (mean={y.mean():.1f} min, median={y.median():.1f} min)")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"✓ Train set: {len(X_train):,} | Test set: {len(X_test):,}")

# ============================================================================
# 4. MULTIPLE LINEAR REGRESSION - INTERPRETABILITY
# ============================================================================

print("\n" + "=" * 80)
print("[4] MULTIPLE LINEAR REGRESSION - Simple Interpretability")
print("=" * 80)

# Standardize features for coefficient comparison
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Fit linear regression
lr_model = LinearRegression()
lr_model.fit(X_train_scaled, y_train)

# Predictions
y_pred_lr = lr_model.predict(X_test_scaled)

# Evaluation metrics
r2_lr = r2_score(y_test, y_pred_lr)
rmse_lr = np.sqrt(mean_squared_error(y_test, y_pred_lr))
mae_lr = mean_absolute_error(y_test, y_pred_lr)

print(f"\n📊 Linear Regression Performance:")
print(f"  R² Score: {r2_lr:.4f} ({r2_lr*100:.1f}% of variance explained)")
print(f"  RMSE: {rmse_lr:.2f} minutes")
print(f"  MAE: {mae_lr:.2f} minutes")

# Feature importance (standardized coefficients)
lr_importance = pd.DataFrame({
    'Feature': feature_cols,
    'Coefficient': lr_model.coef_,
    'Abs_Coefficient': np.abs(lr_model.coef_)
}).sort_values('Abs_Coefficient', ascending=False)

print("\n🔍 Top 10 Drivers (Standardized Coefficients):")
print("   Higher absolute coefficient = stronger impact on wait time")
print("\n" + lr_importance.head(10).to_string(index=False))

# Calculate percentage contribution to variance
# Using relative importance based on coefficient magnitude
total_coef = lr_importance['Abs_Coefficient'].sum()
lr_importance['Pct_Contribution'] = (lr_importance['Abs_Coefficient'] / total_coef * 100)

print("\n💡 Key Findings (Linear Regression):")
top_5 = lr_importance.head(5)
for idx, row in top_5.iterrows():
    direction = "increases" if row['Coefficient'] > 0 else "decreases"
    print(f"  • {row['Feature']}: {direction} wait time by {abs(row['Coefficient']):.2f} min/unit (standardized)")
    print(f"    Contributes {row['Pct_Contribution']:.1f}% of total coefficient weight")

# ============================================================================
# 5. RANDOM FOREST REGRESSION - NON-LINEAR RELATIONSHIPS
# ============================================================================

print("\n" + "=" * 80)
print("[5] RANDOM FOREST REGRESSION - Capture Non-Linear Relationships")
print("=" * 80)

# Fit Random Forest (no need for scaling)
rf_model = RandomForestRegressor(
    n_estimators=200,
    max_depth=20,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1
)
rf_model.fit(X_train, y_train)

# Predictions
y_pred_rf = rf_model.predict(X_test)

# Evaluation
r2_rf = r2_score(y_test, y_pred_rf)
rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))
mae_rf = mean_absolute_error(y_test, y_pred_rf)

print(f"\n📊 Random Forest Performance:")
print(f"  R² Score: {r2_rf:.4f} ({r2_rf*100:.1f}% of variance explained)")
print(f"  RMSE: {rmse_rf:.2f} minutes")
print(f"  MAE: {mae_rf:.2f} minutes")
print(f"  Improvement over Linear: {(r2_rf - r2_lr)*100:.1f}% more variance explained")

# Feature importance
rf_importance = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=False)

rf_importance['Pct_Contribution'] = (rf_importance['Importance'] / rf_importance['Importance'].sum() * 100)

print("\n🔍 Top 10 Drivers (Feature Importance):")
print("   Percentage shows contribution to prediction accuracy")
print("\n" + rf_importance.head(10).to_string(index=False))

print("\n💡 Key Findings (Random Forest):")
top_5_rf = rf_importance.head(5)
cumulative = 0
for idx, row in top_5_rf.iterrows():
    cumulative += row['Pct_Contribution']
    print(f"  • {row['Feature']}: {row['Pct_Contribution']:.1f}% importance (cumulative: {cumulative:.1f}%)")

# ============================================================================
# 6. GRADIENT BOOSTING - STATE-OF-THE-ART ACCURACY
# ============================================================================

print("\n" + "=" * 80)
print("[6] GRADIENT BOOSTING - State-of-the-Art Prediction")
print("=" * 80)

# Fit Gradient Boosting
gb_model = GradientBoostingRegressor(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.1,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42
)
gb_model.fit(X_train, y_train)

# Predictions
y_pred_gb = gb_model.predict(X_test)

# Evaluation
r2_gb = r2_score(y_test, y_pred_gb)
rmse_gb = np.sqrt(mean_squared_error(y_test, y_pred_gb))
mae_gb = mean_absolute_error(y_test, y_pred_gb)

print(f"\n📊 Gradient Boosting Performance:")
print(f"  R² Score: {r2_gb:.4f} ({r2_gb*100:.1f}% of variance explained)")
print(f"  RMSE: {rmse_gb:.2f} minutes")
print(f"  MAE: {mae_gb:.2f} minutes")
print(f"  Improvement over Linear: {(r2_gb - r2_lr)*100:.1f}% more variance explained")
print(f"  Improvement over Random Forest: {(r2_gb - r2_rf)*100:.1f}% more variance explained")

# Feature importance
gb_importance = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': gb_model.feature_importances_
}).sort_values('Importance', ascending=False)

gb_importance['Pct_Contribution'] = (gb_importance['Importance'] / gb_importance['Importance'].sum() * 100)

print("\n🔍 Top 10 Drivers (Feature Importance):")
print("\n" + gb_importance.head(10).to_string(index=False))

# ============================================================================
# 7. XGBOOST (if available)
# ============================================================================

if XGBOOST_AVAILABLE:
    print("\n" + "=" * 80)
    print("[7] XGBoost - Advanced Gradient Boosting")
    print("=" * 80)
    
    xgb_model = XGBRegressor(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.1,
        random_state=42,
        n_jobs=-1
    )
    xgb_model.fit(X_train, y_train)
    
    y_pred_xgb = xgb_model.predict(X_test)
    
    r2_xgb = r2_score(y_test, y_pred_xgb)
    rmse_xgb = np.sqrt(mean_squared_error(y_test, y_pred_xgb))
    mae_xgb = mean_absolute_error(y_test, y_pred_xgb)
    
    print(f"\n📊 XGBoost Performance:")
    print(f"  R² Score: {r2_xgb:.4f} ({r2_xgb*100:.1f}% of variance explained)")
    print(f"  RMSE: {rmse_xgb:.2f} minutes")
    print(f"  MAE: {mae_xgb:.2f} minutes")
    
    xgb_importance = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': xgb_model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    xgb_importance['Pct_Contribution'] = (xgb_importance['Importance'] / xgb_importance['Importance'].sum() * 100)

# ============================================================================
# 8. MODEL COMPARISON & VISUALIZATION
# ============================================================================

print("\n" + "=" * 80)
print("[8] MODEL COMPARISON")
print("=" * 80)

comparison = pd.DataFrame({
    'Model': ['Linear Regression', 'Random Forest', 'Gradient Boosting'],
    'R²': [r2_lr, r2_rf, r2_gb],
    'RMSE': [rmse_lr, rmse_rf, rmse_gb],
    'MAE': [mae_lr, mae_rf, mae_gb]
})

if XGBOOST_AVAILABLE:
    comparison = pd.concat([comparison, pd.DataFrame({
        'Model': ['XGBoost'],
        'R²': [r2_xgb],
        'RMSE': [rmse_xgb],
        'MAE': [mae_xgb]
    })], ignore_index=True)

print("\n📈 Model Performance Summary:")
print(comparison.to_string(index=False))

# Visualizations
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Model comparison - R² scores
axes[0, 0].bar(comparison['Model'], comparison['R²'], color=['steelblue', 'coral', 'lightgreen', 'gold'][:len(comparison)])
axes[0, 0].set_title('Model Comparison: R² Score (Variance Explained)', fontsize=14, fontweight='bold')
axes[0, 0].set_ylabel('R² Score', fontsize=12)
axes[0, 0].set_ylim(0, 1)
axes[0, 0].grid(True, alpha=0.3, axis='y')
for i, v in enumerate(comparison['R²']):
    axes[0, 0].text(i, v + 0.02, f'{v:.3f}', ha='center', fontweight='bold')

# 2. Feature importance - Gradient Boosting (top 15)
top_features = gb_importance.head(15)
axes[0, 1].barh(range(len(top_features)), top_features['Pct_Contribution'], color='coral', alpha=0.7)
axes[0, 1].set_yticks(range(len(top_features)))
axes[0, 1].set_yticklabels(top_features['Feature'])
axes[0, 1].set_xlabel('Contribution to Wait Time Variance (%)', fontsize=12)
axes[0, 1].set_title('Top 15 Root Cause Drivers (Gradient Boosting)', fontsize=14, fontweight='bold')
axes[0, 1].invert_yaxis()
axes[0, 1].grid(True, alpha=0.3, axis='x')

# 3. Actual vs Predicted - Best model (Gradient Boosting)
axes[1, 0].scatter(y_test, y_pred_gb, alpha=0.3, s=10)
axes[1, 0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2, label='Perfect Prediction')
axes[1, 0].set_xlabel('Actual Wait Time (minutes)', fontsize=12)
axes[1, 0].set_ylabel('Predicted Wait Time (minutes)', fontsize=12)
axes[1, 0].set_title(f'Actual vs Predicted Wait Times (GB Model, R²={r2_gb:.3f})', fontsize=14, fontweight='bold')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# 4. Residual plot
residuals = y_test - y_pred_gb
axes[1, 1].scatter(y_pred_gb, residuals, alpha=0.3, s=10)
axes[1, 1].axhline(y=0, color='r', linestyle='--', lw=2)
axes[1, 1].set_xlabel('Predicted Wait Time (minutes)', fontsize=12)
axes[1, 1].set_ylabel('Residual (Actual - Predicted)', fontsize=12)
axes[1, 1].set_title('Residual Plot (Gradient Boosting)', fontsize=14, fontweight='bold')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('regression_root_cause_analysis.png', dpi=300, bbox_inches='tight')
print("\n✓ Saved visualization: regression_root_cause_analysis.png")

# ============================================================================
# 9. EXECUTIVE SUMMARY - QUANTIFIED ROI INSIGHTS
# ============================================================================

print("\n" + "=" * 80)
print("[9] EXECUTIVE SUMMARY - QUANTIFIED ROOT CAUSES")
print("=" * 80)

print("\n🎯 VARIANCE DECOMPOSITION (What Drives Wait Times):")
print(f"\n  Best Model: Gradient Boosting (R² = {r2_gb:.3f})")
print(f"  Explained {r2_gb*100:.1f}% of wait time variance")
print(f"  Unexplained variance: {(1-r2_gb)*100:.1f}% (random variation, unmeasured factors)")

print("\n📊 TOP ROOT CAUSES (Gradient Boosting Feature Importance):")
top_10 = gb_importance.head(10)
cumulative = 0
for i, row in top_10.iterrows():
    cumulative += row['Pct_Contribution']
    print(f"\n  {int(i)+1}. {row['Feature']}")
    print(f"     • Accounts for {row['Pct_Contribution']:.1f}% of wait time variance")
    print(f"     • Cumulative: {cumulative:.1f}% of total variance explained")

print(f"\n  → Top 5 factors account for {top_10.head(5)['Pct_Contribution'].sum():.1f}% of variance")

print("\n💡 ACTIONABLE INSIGHTS FOR MAXIMUM ROI:")

# Extract top drivers
top_1 = gb_importance.iloc[0]
top_2 = gb_importance.iloc[1]
top_3 = gb_importance.iloc[2]

print(f"\n  1️⃣  PRIORITY #1: {top_1['Feature']}")
print(f"     Impact: {top_1['Pct_Contribution']:.1f}% of wait time variance")
if 'Provider_Wait' in top_1['Feature']:
    print(f"     Action: Optimize physician staffing and patient-to-provider ratios")
elif 'Staffing' in top_1['Feature']:
    print(f"     Action: Increase staffing during high-pressure periods")
elif 'Volume' in top_1['Feature']:
    print(f"     Action: Implement surge protocols and capacity flex strategies")
elif 'Load' in top_1['Feature']:
    print(f"     Action: Improve bed turnover and discharge processes")

print(f"\n  2️⃣  PRIORITY #2: {top_2['Feature']}")
print(f"     Impact: {top_2['Pct_Contribution']:.1f}% of wait time variance")

print(f"\n  3️⃣  PRIORITY #3: {top_3['Feature']}")
print(f"     Impact: {top_3['Pct_Contribution']:.1f}% of wait time variance")

print("\n🎯 RECOMMENDED INTERVENTION STRATEGY:")
print(f"  • Focus on top 3 drivers = {gb_importance.head(3)['Pct_Contribution'].sum():.1f}% potential improvement")
print(f"  • Expected wait time reduction: {gb_importance.head(3)['Pct_Contribution'].sum():.1f}% × current variance")
print(f"  • Predicted impact: Reduce average wait from {y.mean():.0f} min by {y.mean() * gb_importance.head(3)['Pct_Contribution'].sum()/100:.0f} min")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
