import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Load the data
df = pd.read_csv('/Users/mukeshravichandran/Datathon/final_data.csv')

print("="*80)
print("SYSTEMATIC DATA EXPLORATION - CHAIN OF THOUGHT")
print("="*80)

# 1. First, understand what we have
print("\n1️⃣  WHAT DATA DO WE HAVE?")
print("-"*80)
print(f"Total visits: {len(df):,}")
print(f"Date range: {df['Visit Date'].min()} to {df['Visit Date'].max()}")
print(f"\nColumns related to our analysis:")
print(df[['Visit ID', 'Triage Level', 'Triage End', 'Doctor Seen', 'Exit Time', 
          'Doctors On Duty', 'Nurses On Duty', 'Specialists On Call',
          'Facility Size (Beds)', 'ICU Beds', 'Regular Beds', 'Fast Track Beds',
          'Shift', 'DoctorVisit to Exit', 'WaitTime after Triage']].head(10).to_string())

# 2. Understand the wait time
print("\n\n2️⃣  WHAT IS 'WAIT TIME AFTER TRIAGE'?")
print("-"*80)
df['Triage End'] = pd.to_datetime(df['Triage End'])
df['Doctor Seen'] = pd.to_datetime(df['Doctor Seen'])
df['Exit Time'] = pd.to_datetime(df['Exit Time'])

# Calculate wait time ourselves
df['Calculated Wait'] = (df['Doctor Seen'] - df['Triage End']).dt.total_seconds() / 60

print(f"Given 'WaitTime after Triage': min={df['WaitTime after Triage'].min()}, max={df['WaitTime after Triage'].max()}, mean={df['WaitTime after Triage'].mean():.1f}")
print(f"Our calculated (Doctor Seen - Triage End): min={df['Calculated Wait'].min():.1f}, max={df['Calculated Wait'].max():.1f}, mean={df['Calculated Wait'].mean():.1f}")
print(f"Match? {np.allclose(df['WaitTime after Triage'], df['Calculated Wait'])}")

# 3. Distribution of wait times
print("\n\n3️⃣  DISTRIBUTION OF WAIT TIMES (after triage)")
print("-"*80)
print(df['WaitTime after Triage'].describe())
print(f"\nWait time percentiles:")
print(f"  10th: {df['WaitTime after Triage'].quantile(0.10):.1f} min")
print(f"  25th: {df['WaitTime after Triage'].quantile(0.25):.1f} min")
print(f"  50th (median): {df['WaitTime after Triage'].quantile(0.50):.1f} min")
print(f"  75th: {df['WaitTime after Triage'].quantile(0.75):.1f} min")
print(f"  90th: {df['WaitTime after Triage'].quantile(0.90):.1f} min")

# 4. By Severity
print("\n\n4️⃣  WAIT TIME BY SEVERITY LEVEL")
print("-"*80)
severity_stats = df.groupby('Triage Level')['WaitTime after Triage'].agg([
    'count', 'mean', 'median', 'std', 'min', 'max'
]).round(2)
print(severity_stats)

# 5. Staff on duty
print("\n\n5️⃣  STAFF PATTERNS")
print("-"*80)
print("Doctors on duty:")
print(df['Doctors On Duty'].value_counts().sort_index())
print("\nSpecialists on call:")
print(df['Specialists On Call'].value_counts().sort_index())
print("\nNurses on duty:")
print(df['Nurses On Duty'].value_counts().sort_index())

# 6. Beds on duty
print("\n\n6️⃣  BED AVAILABILITY")
print("-"*80)
print("Regular Beds available:")
print(df['Regular Beds'].value_counts().sort_index())
print("\nFast Track Beds on shift:")
print(df['Fast Tracks Beds on shift'].value_counts().sort_index())
print("\nICU Beds:")
print(df['ICU Beds'].value_counts().sort_index())

# 7. Time doctor spends with patient
print("\n\n7️⃣  HOW LONG DOES DOCTOR SPEND WITH PATIENT?")
print("-"*80)
print(df['DoctorVisit to Exit'].describe())
print(f"\nDoctor visit duration percentiles:")
print(f"  10th: {df['DoctorVisit to Exit'].quantile(0.10):.1f} min")
print(f"  25th: {df['DoctorVisit to Exit'].quantile(0.25):.1f} min")
print(f"  50th (median): {df['DoctorVisit to Exit'].quantile(0.50):.1f} min")
print(f"  75th: {df['DoctorVisit to Exit'].quantile(0.75):.1f} min")
print(f"  90th: {df['DoctorVisit to Exit'].quantile(0.90):.1f} min")

# 8. By shift
print("\n\n8️⃣  PATTERNS BY SHIFT")
print("-"*80)
shift_stats = df.groupby('Shift').agg({
    'Doctors On Duty': 'first',
    'Nurses On Duty': 'first',
    'Specialists On Call': 'first',
    'WaitTime after Triage': ['count', 'mean', 'median'],
    'DoctorVisit to Exit': 'mean'
}).round(2)
shift_stats.columns = ['Doctors', 'Nurses', 'Specialists', 'Patient Count', 'Avg Wait', 'Median Wait', 'Avg Doctor Time']
print(shift_stats)

# 9. Simple ratio: patients per doctor per shift
print("\n\n9️⃣  CAPACITY RATIO: Patients per Doctor per Shift")
print("-"*80)
df['Visit Date'] = pd.to_datetime(df['Visit Date'])
ratio_by_shift = df.groupby(['Visit Date', 'Shift']).agg({
    'Doctors On Duty': 'first',
    'Visit ID': 'count',
    'WaitTime after Triage': 'mean'
}).reset_index()
ratio_by_shift.columns = ['Date', 'Shift', 'Doctors', 'Patients', 'Avg Wait']
ratio_by_shift['Patients per Doctor'] = ratio_by_shift['Patients'] / ratio_by_shift['Doctors']

print("\nSample of daily shift data:")
print(ratio_by_shift.head(20).to_string(index=False))

print(f"\nStatistics on 'Patients per Doctor' per shift:")
print(f"  Mean: {ratio_by_shift['Patients per Doctor'].mean():.1f} patients/doctor/shift")
print(f"  Median: {ratio_by_shift['Patients per Doctor'].median():.1f} patients/doctor/shift")
print(f"  Std Dev: {ratio_by_shift['Patients per Doctor'].std():.1f}")
print(f"  Max: {ratio_by_shift['Patients per Doctor'].max():.1f} (on {ratio_by_shift.loc[ratio_by_shift['Patients per Doctor'].idxmax(), 'Date'].date()})")

# 10. Key insight: Does high wait correlate with high patient load?
print("\n\n🔟 KEY INSIGHT: Does Wait Time Correlate with Patient/Doctor Ratio?")
print("-"*80)
correlation = ratio_by_shift['Patients per Doctor'].corr(ratio_by_shift['Avg Wait'])
print(f"Correlation between (Patients per Doctor) and (Avg Wait Time): {correlation:.3f}")
print("  If > 0.7: Strong correlation - more patients = longer waits")
print("  If < 0.3: Weak correlation - something else driving waits")

print("\n" + "="*80)
print("OBSERVATIONS & NEXT QUESTIONS")
print("="*80)
print("""
Based on this data, we need to answer:

1. Is wait time driven by CAPACITY (too many patients for doctors)?
   → Look at patient/doctor ratio vs wait time

2. Is wait time driven by SEVERITY (high-severity cases taking long)?
   → Look at triage level vs doctor visit duration vs wait time

3. Is wait time driven by BED/ROOM AVAILABILITY?
   → Do we have enough beds for waiting patients?

4. Is wait time driven by COORDINATION (process failure)?
   → Can we see instances where doctor available but patient still waiting?

Which ONE should we focus on first?
""")

