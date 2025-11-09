# ML Implementation Guide: Code Templates & Workflows
## Ready-to-use Python code for each model

---

## MODEL 1: COMPLEXITY PREDICTOR (ESI Level Prediction)

### Quick Start Code

```python
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================================
# STEP 1: LOAD & EXPLORE DATA
# ============================================================================

df = pd.read_csv('final_data.csv')
print(f"Dataset shape: {df.shape}")
print(f"\nColumns: {df.columns.tolist()}")

# ============================================================================
# STEP 2: FEATURE ENGINEERING
# ============================================================================

# Create features from timestamps
df['Arrival Time'] = pd.to_datetime(df['Arrival Time'])
df['Hour'] = df['Arrival Time'].dt.hour
df['DayOfWeek'] = df['Arrival Time'].dt.dayofweek
df['IsWeekend'] = (df['DayOfWeek'] >= 5).astype(int)
df['IsMorningRush'] = ((df['Hour'] >= 6) & (df['Hour'] <= 9)).astype(int)

# Create complexity features
df['VitalSign_Abnormality_Score'] = (
    (df['WaitTime for Reg'] > df['WaitTime for Reg'].quantile(0.75)).astype(int) +
    (df['Triage process time'] > df['Triage process time'].median()).astype(int)
)

# Feature set for complexity prediction
feature_cols = [
    'Age',
    'Hour',
    'DayOfWeek',
    'IsWeekend',
    'IsMorningRush',
    'VitalSign_Abnormality_Score',
    'Nurses On Duty',
    'Doctors On Duty',
    'Specialists On Call',
    'WaitTime for Reg',
    'Triage process time',
]

# Handle missing values
df[feature_cols] = df[feature_cols].fillna(df[feature_cols].median())

# Target variable: Triage Level (as proxy for complexity)
y = df['Triage Level']  # 1-5
X = df[feature_cols]

print(f"\nFeature matrix shape: {X.shape}")
print(f"Class distribution:\n{y.value_counts().sort_index()}")

# ============================================================================
# STEP 3: TRAIN-TEST SPLIT
# ============================================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\nTrain set size: {len(X_train)}")
print(f"Test set size: {len(X_test)}")

# ============================================================================
# STEP 4: TRAIN MODEL
# ============================================================================

model = RandomForestClassifier(
    n_estimators=150,
    max_depth=15,
    min_samples_split=10,
    min_samples_leaf=5,
    class_weight='balanced',  # Handle class imbalance
    random_state=42,
    n_jobs=-1  # Use all CPU cores
)

model.fit(X_train, y_train)
print("\n✓ Model trained")

# ============================================================================
# STEP 5: EVALUATE MODEL
# ============================================================================

# Predictions
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {accuracy:.4f}")

# Detailed report
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['ESI 1', 'ESI 2', 'ESI 3', 'ESI 4', 'ESI 5']))

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.title('Confusion Matrix: Triage Level Prediction')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.tight_layout()
plt.savefig('complexity_confusion_matrix.png')
plt.close()

# ============================================================================
# STEP 6: FEATURE IMPORTANCE
# ============================================================================

importance_df = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=False)

print("\nFeature Importance:")
print(importance_df)

plt.figure(figsize=(10, 6))
sns.barplot(data=importance_df, x='Importance', y='Feature')
plt.title('Feature Importance: Complexity Prediction')
plt.xlabel('Importance Score')
plt.tight_layout()
plt.savefig('complexity_feature_importance.png')
plt.close()

# ============================================================================
# STEP 7: CROSS-VALIDATION
# ============================================================================

cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
print(f"\nCross-validation scores: {cv_scores}")
print(f"Mean CV accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

# ============================================================================
# STEP 8: SAVE MODEL FOR DEPLOYMENT
# ============================================================================

import pickle
with open('complexity_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("\n✓ Model saved to: complexity_model.pkl")

# ============================================================================
# STEP 9: MAKE PREDICTIONS ON NEW DATA
# ============================================================================

# Example: New patient arrives
new_patient = pd.DataFrame({
    'Age': [75],
    'Hour': [8],  # 8 AM (morning rush)
    'DayOfWeek': [2],  # Wednesday
    'IsWeekend': [0],
    'IsMorningRush': [1],
    'VitalSign_Abnormality_Score': [2],
    'Nurses On Duty': [8],
    'Doctors On Duty': [4],
    'Specialists On Call': [2],
    'WaitTime for Reg': [3],
    'Triage process time': [15],
})

predicted_esi = model.predict(new_patient)[0]
predicted_esi_proba = model.predict_proba(new_patient)[0]

print("\n" + "="*60)
print("PREDICTION FOR NEW PATIENT:")
print("="*60)
print(f"Predicted ESI Level: {predicted_esi}")
print(f"\nProbability Distribution:")
for esi in range(1, 6):
    prob = predicted_esi_proba[esi-1]
    bar = "█" * int(prob * 50)
    print(f"  ESI {esi}: {prob:5.1%} {bar}")

print("="*60)
```

---

## MODEL 2: INTELLIGENT DISPATCHER (Queue Assignment Optimization)

### Quick Start Code

```python
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import lightgbm as lgb
import matplotlib.pyplot as plt

# ============================================================================
# STEP 1: PREPARE DATA FOR DISPATCHER MODEL
# ============================================================================

df = pd.read_csv('final_data.csv')

# Target: Post-triage wait time (Doctor Seen - Triage End)
df['Triage End'] = pd.to_datetime(df['Triage End'])
df['Doctor Seen'] = pd.to_datetime(df['Doctor Seen'])
df['Post_Triage_Wait'] = (df['Doctor Seen'] - df['Triage End']).dt.total_seconds() / 60

# Remove extreme outliers
df = df[(df['Post_Triage_Wait'] >= 0) & (df['Post_Triage_Wait'] <= 300)]

print(f"Post-triage wait time distribution:")
print(df['Post_Triage_Wait'].describe())

# ============================================================================
# STEP 2: FEATURE ENGINEERING
# ============================================================================

# Temporal features
df['Triage End Time'] = pd.to_datetime(df['Triage End'])
df['Hour'] = df['Triage End Time'].dt.hour
df['DayOfWeek'] = df['Triage End Time'].dt.dayofweek
df['IsWeekend'] = (df['DayOfWeek'] >= 5).astype(int)
df['IsMorningRush'] = ((df['Hour'] >= 6) & (df['Hour'] <= 9)).astype(int)

# Encode categorical variables
le_disposition = LabelEncoder()
df['Disposition_Encoded'] = le_disposition.fit_transform(df['Disposition'])

# Feature set
dispatcher_features = [
    'Triage Level',
    'Age',
    'Hour',
    'DayOfWeek',
    'IsWeekend',
    'IsMorningRush',
    'Doctors On Duty',
    'Nurses On Duty',
    'Specialists On Call',
    'Registration process time',
    'Triage process time',
    'Disposition_Encoded',
]

# Handle missing values
for col in dispatcher_features:
    if df[col].dtype in ['int64', 'float64']:
        df[col] = df[col].fillna(df[col].median())

X = df[dispatcher_features]
y = df['Post_Triage_Wait']

print(f"\nFeatures: {dispatcher_features}")
print(f"Target (Post-Triage Wait) statistics:")
print(f"  Mean: {y.mean():.1f} min")
print(f"  Median: {y.median():.1f} min")
print(f"  Std: {y.std():.1f} min")

# ============================================================================
# STEP 3: TRAIN-TEST SPLIT & SCALING
# ============================================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"\nTrain size: {len(X_train)}, Test size: {len(X_test)}")

# ============================================================================
# STEP 4: TRAIN LIGHTGBM MODEL
# ============================================================================

train_data = lgb.Dataset(X_train_scaled, label=y_train, feature_name=dispatcher_features)

params = {
    'objective': 'regression',
    'metric': 'mae',
    'num_leaves': 31,
    'learning_rate': 0.05,
    'feature_fraction': 0.8,
    'bagging_fraction': 0.8,
    'bagging_freq': 5,
    'verbose': -1,
}

model = lgb.train(
    params,
    train_data,
    num_boost_round=200,
)

print("✓ Model trained")

# ============================================================================
# STEP 5: EVALUATE
# ============================================================================

y_pred_train = model.predict(X_train_scaled)
y_pred_test = model.predict(X_test_scaled)

mae_test = mean_absolute_error(y_test, y_pred_test)
rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
r2_test = r2_score(y_test, y_pred_test)

print(f"\nModel Performance (Test Set):")
print(f"  MAE:  {mae_test:.2f} minutes")
print(f"  RMSE: {rmse_test:.2f} minutes")
print(f"  R²:   {r2_test:.4f}")

# ============================================================================
# STEP 6: FEATURE IMPORTANCE
# ============================================================================

importance = model.feature_importance(importance_type='gain')
importance_df = pd.DataFrame({
    'Feature': dispatcher_features,
    'Importance': importance,
}).sort_values('Importance', ascending=False)

print(f"\nTop Features:")
print(importance_df.head(10))

plt.figure(figsize=(10, 6))
top_features = importance_df.head(10)
plt.barh(top_features['Feature'], top_features['Importance'])
plt.xlabel('Importance Score')
plt.title('Dispatcher Model: Feature Importance')
plt.tight_layout()
plt.savefig('dispatcher_feature_importance.png')
plt.close()

# ============================================================================
# STEP 7: EXAMPLE PREDICTION
# ============================================================================

# New patient in queue
new_case = pd.DataFrame({
    'Triage Level': [3],  # Moderate
    'Age': [45],
    'Hour': [9],  # 9 AM (rush)
    'DayOfWeek': [2],  # Wed
    'IsWeekend': [0],
    'IsMorningRush': [1],
    'Doctors On Duty': [4],
    'Nurses On Duty': [8],
    'Specialists On Call': [2],
    'Registration process time': [8],
    'Triage process time': [12],
    'Disposition_Encoded': [1],  # Discharge
})

new_case_scaled = scaler.transform(new_case)
predicted_wait = model.predict(new_case_scaled)[0]

print(f"\n{'='*60}")
print(f"DISPATCH PREDICTION:")
print(f"{'='*60}")
print(f"Patient: ESI 3, Age 45, Morning rush (9 AM)")
print(f"Predicted wait time: {predicted_wait:.1f} minutes")
print(f"Confidence interval: {predicted_wait-10:.1f} - {predicted_wait+10:.1f} min")
print(f"\nRecommendation: Assign to available doctor")
print(f"{'='*60}")

# ============================================================================
# STEP 8: SAVE MODEL
# ============================================================================

model.save_model('dispatcher_model.txt')
print("\n✓ Model saved")
```

---

## MODEL 3: LENGTH-OF-STAY PREDICTOR (Quantile Regression)

### Quick Start Code

```python
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
import matplotlib.pyplot as plt

# ============================================================================
# STEP 1: PREPARE DATA
# ============================================================================

df = pd.read_csv('final_data.csv')

# Target: Doctor cycle time (Doctor Seen to Exit)
df['Doctor Seen'] = pd.to_datetime(df['Doctor Seen'])
df['Exit Time'] = pd.to_datetime(df['Exit Time'])
df['Doctor_Cycle_Time'] = (df['Exit Time'] - df['Doctor Seen']).dt.total_seconds() / 60

# Filter outliers
df = df[(df['Doctor_Cycle_Time'] >= 20) & (df['Doctor_Cycle_Time'] <= 350)]

print(f"Doctor cycle time (LOS) distribution:")
print(df['Doctor_Cycle_Time'].describe())

# Quantile information
quantiles = [0.1, 0.25, 0.5, 0.75, 0.9]
print(f"\nQuantiles:")
for q in quantiles:
    val = df['Doctor_Cycle_Time'].quantile(q)
    print(f"  {q:.0%}: {val:.0f} min")

# ============================================================================
# STEP 2: FEATURE ENGINEERING
# ============================================================================

# Create features
df['Triage End'] = pd.to_datetime(df['Triage End'])
df['Hour'] = df['Triage End'].dt.hour
df['DayOfWeek'] = df['Triage End'].dt.dayofweek

# Encode
le_disp = LabelEncoder()
df['Disposition_Code'] = le_disp.fit_transform(df['Disposition'])

los_features = [
    'Triage Level',
    'Age',
    'Hour',
    'DayOfWeek',
    'Doctors On Duty',
    'Nurses On Duty',
    'Registration process time',
    'Triage process time',
    'WaitTime after Triage',
    'Disposition_Code',
]

# Handle missing
for col in los_features:
    if df[col].dtype in ['int64', 'float64']:
        df[col] = df[col].fillna(df[col].median())

X = df[los_features]
y = df['Doctor_Cycle_Time']

print(f"\nFeatures: {len(los_features)}")

# ============================================================================
# STEP 3: SPLIT & SCALE
# ============================================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"Train: {len(X_train)}, Test: {len(X_test)}")

# ============================================================================
# STEP 4: TRAIN QUANTILE MODELS
# ============================================================================

# We'll train 3 models for 25th, 50th, 90th percentiles
quantile_models = {}

for q in [0.25, 0.50, 0.90]:
    print(f"\nTraining model for {q:.0%} quantile...")
    
    train_data = lgb.Dataset(
        X_train_scaled,
        label=y_train,
        feature_name=los_features
    )
    
    params = {
        'objective': 'quantile',
        'alpha': q,  # Quantile level
        'metric': 'quantile',
        'num_leaves': 31,
        'learning_rate': 0.05,
        'verbose': -1,
    }
    
    model = lgb.train(params, train_data, num_boost_round=150)
    quantile_models[q] = model
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"  MAE: {mae:.2f} minutes")

print("\n✓ All quantile models trained")

# ============================================================================
# STEP 5: PREDICT WITH CONFIDENCE INTERVALS
# ============================================================================

# Median (50%) prediction
y_pred_median = quantile_models[0.50].predict(X_test_scaled)
y_pred_q25 = quantile_models[0.25].predict(X_test_scaled)
y_pred_q90 = quantile_models[0.90].predict(X_test_scaled)

mae_median = mean_absolute_error(y_test, y_pred_median)
mape_median = mean_absolute_percentage_error(y_test, y_pred_median)

print(f"\nTest Set Performance (Median Model):")
print(f"  MAE:  {mae_median:.2f} minutes")
print(f"  MAPE: {mape_median:.2%}")

# Coverage: % of actual values within predicted intervals
coverage = ((y_test >= y_pred_q25) & (y_test <= y_pred_q90)).sum() / len(y_test)
print(f"  Coverage (25%-90%): {coverage:.1%}")

# ============================================================================
# STEP 6: EXAMPLE PREDICTION WITH RANGE
# ============================================================================

new_patient = pd.DataFrame({
    'Triage Level': [2],  # Emergent
    'Age': [65],
    'Hour': [10],
    'DayOfWeek': [1],
    'Doctors On Duty': [4],
    'Nurses On Duty': [8],
    'Registration process time': [8],
    'Triage process time': [15],
    'WaitTime after Triage': [30],
    'Disposition_Code': [1],
})

new_patient_scaled = scaler.transform(new_patient)

pred_q25 = quantile_models[0.25].predict(new_patient_scaled)[0]
pred_q50 = quantile_models[0.50].predict(new_patient_scaled)[0]
pred_q90 = quantile_models[0.90].predict(new_patient_scaled)[0]

print(f"\n{'='*60}")
print(f"LENGTH-OF-STAY PREDICTION:")
print(f"{'='*60}")
print(f"Patient: ESI 2, Age 65, Emergent")
print(f"\nPredicted Doctor Cycle Time:")
print(f"  25th percentile (fast):    {pred_q25:6.0f} minutes")
print(f"  Median (most likely):      {pred_q50:6.0f} minutes")
print(f"  90th percentile (slow):    {pred_q90:6.0f} minutes")
print(f"\nInterpretation:")
print(f"  25% chance patient done in < {pred_q25:.0f} min")
print(f"  50% chance done in {pred_q50:.0f} min")
print(f"  90% chance done by {pred_q90:.0f} min")
print(f"{'='*60}")
```

---

## MODEL 4: WORKLOAD FORECASTER (Time Series)

### Quick Start Code

```python
import pandas as pd
import numpy as np
from fbprophet import Prophet
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_percentage_error, mean_absolute_error

# ============================================================================
# STEP 1: PREPARE TIME SERIES DATA
# ============================================================================

df = pd.read_csv('final_data.csv')

# Calculate hourly wait times
df['Triage End'] = pd.to_datetime(df['Triage End'])
df['Doctor Seen'] = pd.to_datetime(df['Doctor Seen'])
df['Wait_Minutes'] = (df['Doctor Seen'] - df['Triage End']).dt.total_seconds() / 60

# Aggregate by hour
df['Hour_Floor'] = df['Triage End'].dt.floor('H')
hourly_wait = df.groupby('Hour_Floor')['Wait_Minutes'].agg(['mean', 'count']).reset_index()
hourly_wait.columns = ['ds', 'y_wait', 'patient_count']

# Filter: only hours with multiple patients
hourly_wait = hourly_wait[hourly_wait['patient_count'] >= 2]

# Also calculate queue length (patients waiting for doctor)
df['Time'] = df['Triage End'].dt.floor('H')
queue_length = df.groupby('Time').size().reset_index(name='queue_size')
queue_length.columns = ['ds', 'queue_size']

# Merge
timeseries = hourly_wait.merge(queue_length, how='left', left_on='ds', right_on='ds')
timeseries['y'] = timeseries['y_wait']  # Target for Prophet

print(f"Time series data: {len(timeseries)} hours")
print(f"Date range: {timeseries['ds'].min()} to {timeseries['ds'].max()}")
print(f"\nWait time statistics:")
print(timeseries['y'].describe())

# ============================================================================
# STEP 2: PROPHET MODEL
# ============================================================================

# Prepare data for Prophet
prophet_df = timeseries[['ds', 'y']].dropna()

# Create model
model = Prophet(
    yearly_seasonality=False,
    weekly_seasonality=True,
    daily_seasonality=True,
    interval_width=0.80,  # 80% confidence intervals
)

# Fit
print("\nTraining Prophet model...")
model.fit(prophet_df)
print("✓ Model trained")

# ============================================================================
# STEP 3: MAKE PREDICTIONS
# ============================================================================

# Forecast next 14 days (336 hours)
future = model.make_future_dataframe(periods=14*24, freq='H')
forecast = model.predict(future)

# Evaluation: Compare forecast to actual (first 336 hours)
actuals = prophet_df['y'].values[:336]
forecasts = forecast['yhat'].values[:336]

mae = mean_absolute_error(actuals, forecasts)
mape = mean_absolute_percentage_error(actuals, forecasts)

print(f"\nForecast Performance:")
print(f"  MAE:  {mae:.2f} minutes")
print(f"  MAPE: {mape:.2%}")

# ============================================================================
# STEP 4: IDENTIFY HIGH-DEMAND PERIODS
# ============================================================================

# Find times when wait time predicted > 45 min
high_wait_mask = forecast['yhat'] > 45
high_wait_periods = forecast[high_wait_mask][['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

print(f"\nHigh wait time periods (forecast > 45 min):")
print(high_wait_periods.head(10))

# ============================================================================
# STEP 5: STAFFING RECOMMENDATIONS
# ============================================================================

print(f"\n{'='*60}")
print(f"STAFFING RECOMMENDATIONS (Based on forecast):")
print(f"{'='*60}")

for idx, row in high_wait_periods.head(5).iterrows():
    hour = row['ds']
    predicted_wait = row['yhat']
    confidence_lower = row['yhat_lower']
    confidence_upper = row['yhat_upper']
    
    if predicted_wait > 60:
        recommendation = "CALL ON-CALL DOCTOR"
        color = "🔴"
    else:
        recommendation = "Monitor closely"
        color = "🟡"
    
    print(f"\n{color} {hour}")
    print(f"   Predicted wait: {predicted_wait:.0f} min (range: {confidence_lower:.0f}-{confidence_upper:.0f})")
    print(f"   → {recommendation}")

# ============================================================================
# STEP 6: VISUALIZE FORECAST
# ============================================================================

fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Wait time forecast
ax1 = axes[0]
ax1.plot(timeseries['ds'], timeseries['y'], 'b.', label='Actual', markersize=4)
ax1.plot(forecast['ds'], forecast['yhat'], 'r-', label='Forecast', linewidth=2)
ax1.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], 
                  alpha=0.3, color='red', label='80% CI')
ax1.axhline(y=45, color='orange', linestyle='--', label='Alert threshold (45 min)')
ax1.set_ylabel('Wait Time (minutes)')
ax1.set_title('Prophet Forecast: ED Wait Times')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Seasonality components
model.plot_components(forecast, ax=axes[1])
plt.suptitle('')  # Remove default title
plt.tight_layout()
plt.savefig('workload_forecast.png', dpi=150)
plt.close()

print(f"\n✓ Forecast visualization saved: workload_forecast.png")

# ============================================================================
# STEP 7: SAVE MODEL
# ============================================================================

with open('workload_forecast_model.pkl', 'wb') as f:
    import pickle
    pickle.dump(model, f)

print(f"✓ Model saved: workload_forecast_model.pkl")
```

---

## MODEL 5: OUTCOME PREDICTOR (Neural Network)

### Quick Start Code

```python
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential, layers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
import matplotlib.pyplot as plt

# ============================================================================
# STEP 1: PREPARE DATA (Assuming we have outcome labels)
# ============================================================================

df = pd.read_csv('final_data.csv')

# Create target: High risk patients (those with complications, re-admission, etc.)
# For this demo, we'll use a proxy: patients with long LOS + high ESI
df['Doctor Seen'] = pd.to_datetime(df['Doctor Seen'])
df['Exit Time'] = pd.to_datetime(df['Exit Time'])
df['LOS_Minutes'] = (df['Exit Time'] - df['Doctor Seen']).dt.total_seconds() / 60

# Binary target: High risk = ESI 1-2 OR LOS > 3 hours OR Satisfaction < 3
df['High_Risk'] = (
    (df['Triage Level'] <= 2) |
    (df['LOS_Minutes'] > 180) |
    (df['Satisfaction'] < 3)
).astype(int)

print(f"Target distribution:")
print(df['High_Risk'].value_counts())
print(f"High-risk rate: {df['High_Risk'].mean():.2%}")

# ============================================================================
# STEP 2: FEATURE ENGINEERING
# ============================================================================

df['Arrival Time'] = pd.to_datetime(df['Arrival Time'])
df['Hour'] = df['Arrival Time'].dt.hour
df['DayOfWeek'] = df['Arrival Time'].dt.dayofweek

# Encode categorical
le_disp = LabelEncoder()
df['Disposition_Code'] = le_disp.fit_transform(df['Disposition'])

le_gender = LabelEncoder()
df['Gender_Code'] = le_gender.fit_transform(df['Gender'])

le_insurance = LabelEncoder()
df['Insurance_Code'] = le_insurance.fit_transform(df['Insurance'])

outcome_features = [
    'Triage Level',
    'Age',
    'Hour',
    'DayOfWeek',
    'Doctors On Duty',
    'Nurses On Duty',
    'Registration process time',
    'Triage process time',
    'WaitTime after Triage',
    'Gender_Code',
    'Insurance_Code',
]

# Handle missing
for col in outcome_features:
    if df[col].dtype in ['int64', 'float64']:
        df[col] = df[col].fillna(df[col].median())

X = df[outcome_features]
y = df['High_Risk']

print(f"\nFeatures: {len(outcome_features)}")

# ============================================================================
# STEP 3: SPLIT & SCALE
# ============================================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Compute class weights (for imbalanced data)
class_weight = {
    0: 1.0,
    1: (1 - y_train.mean()) / y_train.mean()  # Up-weight minority class
}

print(f"\nClass weights: {class_weight}")

# ============================================================================
# STEP 4: BUILD NEURAL NETWORK
# ============================================================================

model = Sequential([
    layers.Input(shape=(len(outcome_features),)),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(16, activation='relu'),
    layers.Dense(1, activation='sigmoid'),  # Binary classification
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy', tf.keras.metrics.AUC()],
)

print(f"\n{'='*60}")
print(f"Model Architecture:")
print(f"{'='*60}")
model.summary()

# ============================================================================
# STEP 5: TRAIN MODEL
# ============================================================================

print(f"\nTraining neural network...")
history = model.fit(
    X_train_scaled, y_train,
    validation_data=(X_test_scaled, y_test),
    epochs=150,
    batch_size=32,
    class_weight=class_weight,
    verbose=0,
)

print(f"✓ Training complete")

# ============================================================================
# STEP 6: EVALUATE
# ============================================================================

# Predictions
y_pred_proba = model.predict(X_test_scaled, verbose=0)
y_pred = (y_pred_proba > 0.5).astype(int).flatten()

# Metrics
auc_score = roc_auc_score(y_test, y_pred_proba)
acc = (y_pred == y_test.values).mean()

print(f"\nTest Set Performance:")
print(f"  Accuracy: {acc:.2%}")
print(f"  AUC-ROC:  {auc_score:.4f}")

print(f"\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Low Risk', 'High Risk']))

# ============================================================================
# STEP 7: EXAMPLE PREDICTION
# ============================================================================

new_patient = pd.DataFrame({
    'Triage Level': [2],
    'Age': [72],
    'Hour': [9],
    'DayOfWeek': [1],
    'Doctors On Duty': [4],
    'Nurses On Duty': [8],
    'Registration process time': [8],
    'Triage process time': [14],
    'WaitTime after Triage': [45],
    'Gender_Code': [0],
    'Insurance_Code': [1],
})

new_patient_scaled = scaler.transform(new_patient)
risk_probability = model.predict(new_patient_scaled, verbose=0)[0][0]

print(f"\n{'='*60}")
print(f"ADVERSE OUTCOME RISK PREDICTION:")
print(f"{'='*60}")
print(f"Patient: ESI 2, Age 72")
print(f"\nRisk Score: {risk_probability:.1%}")
print(f"\nRisk Level: ", end="")
if risk_probability < 0.2:
    print("🟢 LOW - Standard care")
elif risk_probability < 0.4:
    print("🟡 MODERATE - Monitor closely")
elif risk_probability < 0.7:
    print("🔴 HIGH - Senior MD review")
else:
    print("🔴🔴 CRITICAL - Immediate intervention")

print(f"\nRecommendation: ", end="")
if risk_probability > 0.6:
    print("Escalate to senior physician")
    print("Consider ICU bed assignment")
    print("Arrange specialist consult")
else:
    print("Continue standard protocol")

print(f"{'='*60}")

# ============================================================================
# STEP 8: SAVE MODEL
# ============================================================================

model.save('outcome_prediction_model.h5')
print(f"\n✓ Model saved: outcome_prediction_model.h5")
```

---

## DEPLOYMENT: SIMPLE REST API

### Quick Start Code

```python
from flask import Flask, request, jsonify
import pickle
import json
import numpy as np
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Load models
with open('complexity_model.pkl', 'rb') as f:
    complexity_model = pickle.load(f)

with open('dispatcher_model.txt', 'r') as f:
    import lightgbm as lgb
    dispatcher_model = lgb.Booster(model_file=f)

@app.route('/predict/complexity', methods=['POST'])
def predict_complexity():
    """Predict patient complexity (ESI level)"""
    data = request.json
    
    # Extract features
    features = np.array([[
        data['age'],
        data['hour'],
        data['day_of_week'],
        data['is_weekend'],
        data['is_morning_rush'],
        data['vital_abnormality_score'],
        data['nurses_on_duty'],
        data['doctors_on_duty'],
        data['specialists_on_call'],
        data['wait_time_for_reg'],
        data['triage_process_time'],
    ]])
    
    # Predict
    prediction = complexity_model.predict(features)[0]
    probability = complexity_model.predict_proba(features)[0]
    
    return jsonify({
        'predicted_esi': int(prediction),
        'confidence': float(probability.max()),
        'probability_distribution': {
            f'esi_{i+1}': float(p) for i, p in enumerate(probability)
        }
    })

@app.route('/predict/dispatcher', methods=['POST'])
def predict_dispatcher():
    """Predict post-triage wait time"""
    data = request.json
    
    # Extract features
    features = np.array([[
        data['triage_level'],
        data['age'],
        data['hour'],
        data['day_of_week'],
        data['is_weekend'],
        data['is_morning_rush'],
        data['doctors_on_duty'],
        data['nurses_on_duty'],
        data['specialists_on_call'],
        data['registration_time'],
        data['triage_time'],
        data['disposition_code'],
    ]])
    
    # Predict
    wait_time = dispatcher_model.predict(features)[0]
    
    return jsonify({
        'predicted_wait_minutes': float(wait_time),
        'alert': wait_time > 45,
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'OK'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
```

### How to use the API:

```bash
# Start server
python app.py

# Make prediction
curl -X POST http://localhost:5000/predict/complexity \
  -H "Content-Type: application/json" \
  -d '{
    "age": 75,
    "hour": 8,
    "day_of_week": 2,
    "is_weekend": 0,
    "is_morning_rush": 1,
    "vital_abnormality_score": 2,
    "nurses_on_duty": 8,
    "doctors_on_duty": 4,
    "specialists_on_call": 2,
    "wait_time_for_reg": 3,
    "triage_process_time": 15
  }'
```

---

## KEY TAKEAWAYS

1. **Start Simple:** Begin with Random Forest (easy to understand, fast)
2. **Iterate:** Add LightGBM, then neural networks
3. **Explainability First:** Use SHAP values, show feature importance
4. **Validate Often:** Compare predictions to actual outcomes daily
5. **Deploy Cautiously:** A/B test before full rollout
6. **Monitor Always:** Track model performance continuously

Good luck! 🚀
