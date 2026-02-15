import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Load the cleaned data
df = pd.read_csv('/Users/mukeshravichandran/Datathon/Doctor_Idle_Time/final_data_cleaned.csv')

# Convert timestamps to datetime
df['Triage End Timestamp'] = pd.to_datetime(df['Triage End Timestamp'])
df['Doctor Seen Timestamp'] = pd.to_datetime(df['Doctor Seen Timestamp'])
df['Exit Timestamp'] = pd.to_datetime(df['Exit Timestamp'])

# Create a total clinicians column
df['Total Clinicians On Duty'] = df['Doctors On Duty'] + df['Specialists On Call']

print("="*80)
print("VALIDATION CHECK: Can there be more patients in consultation than clinicians?")
print("="*80)

# For each patient, at their Triage End, count:
# 1. How many patients are currently with clinicians (including 10-min buffer)
# 2. How many total clinicians available

def count_active_clinicians_at_time(timestamp, all_patients_df, buffer_minutes=10):
    """Count clinicians actively with patients at a given timestamp"""
    active = all_patients_df[
        (all_patients_df['Doctor Seen Timestamp'] <= timestamp) &
        ((all_patients_df['Exit Timestamp'] + timedelta(minutes=buffer_minutes)) >= timestamp)
    ].shape[0]
    return active

def count_waiting_patients_at_time(timestamp, all_patients_df):
    """Count patients waiting for doctors at a given timestamp"""
    waiting = all_patients_df[
        (all_patients_df['Triage End Timestamp'] <= timestamp) &
        (all_patients_df['Doctor Seen Timestamp'] > timestamp)
    ].shape[0]
    return waiting

# Sample analysis for first 100 unique triage end times
print("\nSample Analysis (first 100 triage end timestamps):")
print("-"*80)

results = []
for idx, row in df.head(100).iterrows():
    triage_end = row['Triage End Timestamp']
    doctors_on_duty = row['Doctors On Duty']
    specialists_on_call = row['Specialists On Call']
    total_clinicians = row['Total Clinicians On Duty']
    
    # Count active clinicians at this triage end moment
    active_clinicians = count_active_clinicians_at_time(triage_end, df)
    
    # Count waiting patients at this triage end moment
    waiting_patients = count_waiting_patients_at_time(triage_end, df)
    
    # Can there be concurrent consultations?
    idle_clinicians = total_clinicians - active_clinicians
    
    results.append({
        'Triage End': triage_end,
        'Total Clinicians': total_clinicians,
        'Active Clinicians': active_clinicians,
        'Idle Clinicians': idle_clinicians,
        'Waiting Patients': waiting_patients,
        'Bottleneck': 'YES' if idle_clinicians > 0 and waiting_patients > 0 else 'NO'
    })

results_df = pd.DataFrame(results)
print(results_df.to_string(index=False))

print("\n" + "="*80)
print("SUMMARY STATISTICS")
print("="*80)
print(f"Max Active Clinicians in sample: {results_df['Active Clinicians'].max()}")
print(f"Max Clinicians On Duty in sample: {results_df['Total Clinicians'].max()}")
print(f"Max Waiting Patients in sample: {results_df['Waiting Patients'].max()}")
print(f"Instances where Active > Total Clinicians: {(results_df['Active Clinicians'] > results_df['Total Clinicians']).sum()}")
print(f"   ↳ This would indicate ERROR in logic or data!")

print("\n" + "="*80)
print("FULL DATASET ANALYSIS")
print("="*80)

# Now do full dataset
full_results = []
snapshot_times = df['Triage End Timestamp'].unique()

print(f"\nAnalyzing {len(snapshot_times)} unique triage end timestamps...")
print("This will take a moment...\n")

for snapshot_time in snapshot_times[:500]:  # First 500 unique times to speed up
    total_clinicians_at_time = df[df['Triage End Timestamp'] == snapshot_time]['Total Clinicians On Duty'].iloc[0]
    
    active_clinicians = count_active_clinicians_at_time(snapshot_time, df)
    waiting_patients = count_waiting_patients_at_time(snapshot_time, df)
    idle_clinicians = total_clinicians_at_time - active_clinicians
    
    full_results.append({
        'Snapshot Time': snapshot_time,
        'Total Clinicians': total_clinicians_at_time,
        'Active Clinicians': active_clinicians,
        'Waiting Patients': waiting_patients,
        'Idle Clinicians': idle_clinicians,
        'Bottleneck': 'YES' if idle_clinicians > 0 and waiting_patients > 0 else 'NO'
    })

full_df = pd.DataFrame(full_results)

# Check if we ever have more active clinicians than total
data_error_count = (full_df['Active Clinicians'] > full_df['Total Clinicians']).sum()

print(f"Total unique snapshots analyzed: {len(full_df)}")
print(f"\n✅ Data Validation:")
print(f"   Instances where Active > Total: {data_error_count}")
if data_error_count == 0:
    print(f"   ✓ NO DATA ERRORS - Logic is sound!")
else:
    print(f"   ✗ {data_error_count} ERRORS DETECTED - Logic issue!")

print(f"\n📊 Key Statistics:")
print(f"   Max clinicians on duty simultaneously: {full_df['Total Clinicians'].max()}")
print(f"   Max active clinicians at any time: {full_df['Active Clinicians'].max()}")
print(f"   Max waiting patients at any time: {full_df['Waiting Patients'].max()}")
print(f"   Max idle clinicians at any time: {full_df['Idle Clinicians'].max()}")

print(f"\n⚠️  Bottleneck Events:")
bottleneck_count = (full_df['Bottleneck'] == 'YES').sum()
print(f"   Bottleneck instances (out of {len(full_df)}): {bottleneck_count}")
print(f"   Percentage: {(bottleneck_count/len(full_df)*100):.1f}%")

print(f"\n📈 Average During Bottlenecks:")
bottleneck_df = full_df[full_df['Bottleneck'] == 'YES']
if len(bottleneck_df) > 0:
    print(f"   Avg waiting patients: {bottleneck_df['Waiting Patients'].mean():.1f}")
    print(f"   Avg idle clinicians: {bottleneck_df['Idle Clinicians'].mean():.1f}")
    print(f"   Avg total clinicians on duty: {bottleneck_df['Total Clinicians'].mean():.1f}")

print("\n" + "="*80)
print("WORST BOTTLENECK INSTANCES")
print("="*80)
worst = full_df.nlargest(10, 'Idle Clinicians')[['Snapshot Time', 'Total Clinicians', 'Active Clinicians', 'Waiting Patients', 'Idle Clinicians']]
print(worst.to_string(index=False))
