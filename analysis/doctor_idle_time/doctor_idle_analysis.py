"""
Doctor Idle Time Analysis - First Principles Approach

Question: Are doctors sitting idle while patients wait in queue after triage?

Approach:
1. For each time window, calculate how many doctors are actively seeing patients
2. Compare active doctors vs. doctors on duty
3. Identify if patients are waiting while doctors are available
4. Calculate potential idle time and its impact

IMPORTANT REALISTIC ASSUMPTIONS:
- Doctors need TRANSITION TIME between patients (default: 10 minutes)
- This accounts for:
  * Post-patient documentation/charting
  * Hand washing and sanitization
  * Room turnover and cleanup
  * Brief mental reset/break
  * Reviewing next patient's chart
- We do NOT expect zero-downtime patient-to-patient transitions
- Only flag as "idle" if doctor is available AFTER this reasonable buffer

This prevents unrealistic expectations and focuses on genuine flow bottlenecks.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Load data
print("Loading data...")
df = pd.read_csv(DATA_DIR / "cleaned" / "final_data.csv")

# Convert time columns to datetime
time_cols = ['Arrival Time', 'Registration Start', 'Registration End', 
             'Triage Start', 'Triage End', 'Doctor Seen', 'Exit Time']
for col in time_cols:
    df[col] = pd.to_datetime(df[col])

print(f"Total visits: {len(df)}")
print(f"Date range: {df['Arrival Time'].min()} to {df['Arrival Time'].max()}")
print(f"Hospitals: {df['Hospital ID'].unique()}")
print("\n" + "="*80)

# ============================================================================
# ANALYSIS 1: PATIENT WAITING WHILE DOCTORS ARE IDLE
# ============================================================================
print("\n ANALYSIS 1: IDLE DOCTOR DETECTION")
print("="*80)

def count_active_doctors_at_time(all_visits, check_time, transition_buffer_minutes=10):
    """
    Count how many doctors are actively seeing patients at a given time.
    A doctor is "active" if a patient has been seen but hasn't exited yet.
    
    IMPORTANT: We add a transition buffer (default 10 min) after patient exit
    to account for:
    - Documentation/charting time
    - Hand washing/sanitization
    - Room turnover
    - Quick break/mental reset
    - Reviewing next patient chart
    
    This prevents unrealistic assumption that doctors jump immediately 
    from one patient to the next with zero downtime.
    """
    # Doctor is considered busy from when they start seeing patient
    # until EXIT TIME + BUFFER (to allow for post-patient tasks)
    active = all_visits[
        (all_visits['Doctor Seen'] <= check_time) & 
        (all_visits['Exit Time'] + pd.Timedelta(minutes=transition_buffer_minutes) > check_time)
    ]
    return len(active)

def count_waiting_patients_at_time(all_visits, check_time):
    """
    Count how many patients have finished triage but haven't seen doctor yet.
    """
    waiting = all_visits[
        (all_visits['Triage End'] <= check_time) & 
        (all_visits['Doctor Seen'] > check_time)
    ]
    return len(waiting)

# Analyze by hospital and shift
idle_scenarios = []

for hospital in df['Hospital ID'].unique():
    hospital_df = df[df['Hospital ID'] == hospital].copy()
    
    for shift in hospital_df['Shift'].unique():
        shift_df = hospital_df[hospital_df['Shift'] == shift].copy()
        
        if len(shift_df) == 0:
            continue
            
        # Get number of doctors on duty for this shift
        doctors_on_duty = shift_df['Doctors On Duty'].iloc[0]
        
        # For each patient who waited after triage
        for idx, patient in shift_df.iterrows():
            triage_end = patient['Triage End']
            doctor_seen = patient['Doctor Seen']
            wait_time = (doctor_seen - triage_end).total_seconds() / 60
            
            if wait_time > 10:  # Only consider waits > 10 minutes
                # Check at the moment triage ended
                # Use 10-minute buffer: doctor needs time after patient exits for 
                # documentation, handwashing, room turnover, chart review
                active_doctors = count_active_doctors_at_time(shift_df, triage_end, transition_buffer_minutes=10)
                waiting_patients = count_waiting_patients_at_time(shift_df, triage_end)
                idle_doctors = doctors_on_duty - active_doctors
                
                if idle_doctors > 0 and waiting_patients > 0:
                    idle_scenarios.append({
                        'Hospital': hospital,
                        'Shift': shift,
                        'Visit ID': patient['Visit ID'],
                        'Triage End': triage_end,
                        'Doctor Seen': doctor_seen,
                        'Wait Time (min)': wait_time,
                        'Doctors On Duty': doctors_on_duty,
                        'Active Doctors': active_doctors,
                        'Idle Doctors': idle_doctors,
                        'Patients Waiting': waiting_patients,
                        'Triage Level': patient['Triage Level']
                    })

idle_df = pd.DataFrame(idle_scenarios)

if len(idle_df) > 0:
    print(f"\n✓ Found {len(idle_df)} instances where patients waited while doctors appeared idle\n")
    
    print("Summary Statistics:")
    print(f"  Average wait time: {idle_df['Wait Time (min)'].mean():.1f} minutes")
    print(f"  Median wait time: {idle_df['Wait Time (min)'].median():.1f} minutes")
    print(f"  Max wait time: {idle_df['Wait Time (min)'].max():.1f} minutes")
    print(f"  Total patient-hours wasted: {idle_df['Wait Time (min)'].sum()/60:.1f} hours")
    
    print("\n" + "-"*80)
    print("By Hospital:")
    hospital_summary = idle_df.groupby('Hospital').agg({
        'Visit ID': 'count',
        'Wait Time (min)': ['mean', 'median', 'max'],
        'Idle Doctors': 'mean',
        'Patients Waiting': 'mean'
    }).round(1)
    hospital_summary.columns = ['Count', 'Avg Wait', 'Med Wait', 'Max Wait', 'Avg Idle Docs', 'Avg Waiting']
    print(hospital_summary)
    
    print("\n" + "-"*80)
    print("By Shift:")
    shift_summary = idle_df.groupby('Shift').agg({
        'Visit ID': 'count',
        'Wait Time (min)': ['mean', 'median', 'max'],
        'Idle Doctors': 'mean'
    }).round(1)
    shift_summary.columns = ['Count', 'Avg Wait', 'Med Wait', 'Max Wait', 'Avg Idle Docs']
    print(shift_summary)
    
    print("\n" + "-"*80)
    print("Sample Cases (worst 10):")
    sample = idle_df.nlargest(10, 'Wait Time (min)')[
        ['Hospital', 'Shift', 'Wait Time (min)', 'Idle Doctors', 'Patients Waiting', 'Triage Level']
    ]
    print(sample.to_string(index=False))
    
else:
    print("No clear idle doctor scenarios detected.")

# ============================================================================
# ANALYSIS 2: DOCTOR UTILIZATION OVER TIME
# ============================================================================
print("\n\n ANALYSIS 2: DOCTOR UTILIZATION TIMELINE")
print("="*80)

def analyze_utilization_for_date(hospital_df, date_str):
    """
    Analyze doctor utilization for a specific date by creating a minute-by-minute timeline.
    """
    day_df = hospital_df[hospital_df['Visit Date'] == date_str].copy()
    
    if len(day_df) == 0:
        return None
    
    # Get the full day range
    start_time = day_df['Arrival Time'].min().floor('H')
    end_time = day_df['Exit Time'].max().ceil('H')
    
    # Create minute-by-minute timeline
    timeline = []
    current_time = start_time
    
    while current_time <= end_time:
        # Determine which shift this time belongs to
        hour = current_time.hour
        if 7 <= hour < 15:
            shift = 'DAY'
            shift_df = day_df[day_df['Shift'] == 'DAY']
        elif 15 <= hour < 23:
            shift = 'EVENING'
            shift_df = day_df[day_df['Shift'] == 'EVENING']
        else:
            shift = 'NIGHT'
            shift_df = day_df[day_df['Shift'] == 'NIGHT']
        
        if len(shift_df) > 0:
            doctors_on_duty = shift_df['Doctors On Duty'].iloc[0]
            active = count_active_doctors_at_time(day_df, current_time)
            waiting = count_waiting_patients_at_time(day_df, current_time)
            idle = max(0, doctors_on_duty - active)
            utilization = (active / doctors_on_duty * 100) if doctors_on_duty > 0 else 0
            
            timeline.append({
                'Time': current_time,
                'Shift': shift,
                'Doctors On Duty': doctors_on_duty,
                'Active Doctors': active,
                'Idle Doctors': idle,
                'Patients Waiting': waiting,
                'Utilization %': utilization,
                'Inefficiency': 1 if (idle > 0 and waiting > 0) else 0
            })
        
        current_time += timedelta(minutes=5)  # 5-minute intervals
    
    return pd.DataFrame(timeline)

# Analyze a sample date for each hospital
for hospital in df['Hospital ID'].unique():
    hospital_df = df[df['Hospital ID'] == hospital].copy()
    
    # Pick the date with most visits
    date_counts = hospital_df['Visit Date'].value_counts()
    if len(date_counts) > 0:
        busiest_date = date_counts.index[0]
        
        print(f"\n{hospital} - Busiest Date: {busiest_date}")
        print("-"*80)
        
        timeline_df = analyze_utilization_for_date(hospital_df, busiest_date)
        
        if timeline_df is not None and len(timeline_df) > 0:
            avg_util = timeline_df['Utilization %'].mean()
            inefficient_periods = timeline_df['Inefficiency'].sum()
            total_periods = len(timeline_df)
            
            print(f"  Average Doctor Utilization: {avg_util:.1f}%")
            print(f"  Inefficient Time Periods: {inefficient_periods}/{total_periods} ({inefficient_periods/total_periods*100:.1f}%)")
            print(f"  Peak Active Doctors: {timeline_df['Active Doctors'].max()}")
            print(f"  Peak Waiting Patients: {timeline_df['Patients Waiting'].max()}")
            
            # Find periods with highest inefficiency
            inefficient = timeline_df[timeline_df['Inefficiency'] == 1]
            if len(inefficient) > 0:
                print(f"\n  Example Inefficient Periods:")
                sample_periods = inefficient.head(3)[['Time', 'Shift', 'Doctors On Duty', 
                                                       'Active Doctors', 'Idle Doctors', 'Patients Waiting']]
                print(sample_periods.to_string(index=False))

# ============================================================================
# ANALYSIS 3: GAP ANALYSIS BETWEEN CONSECUTIVE DOCTOR VISITS
# ============================================================================
print("\n\n ANALYSIS 3: DOCTOR APPOINTMENT GAPS")
print("="*80)

gap_analysis = []

for hospital in df['Hospital ID'].unique():
    hospital_df = df[df['Hospital ID'] == hospital].copy()
    hospital_df = hospital_df.sort_values('Doctor Seen').reset_index(drop=True)
    
    for i in range(len(hospital_df) - 1):
        current_patient = hospital_df.iloc[i]
        next_patient = hospital_df.iloc[i + 1]
        
        # Calculate gap between when current patient saw doctor and next patient saw doctor
        gap_minutes = (next_patient['Doctor Seen'] - current_patient['Doctor Seen']).total_seconds() / 60
        
        # Check if this gap is during business hours and significant
        hour = current_patient['Doctor Seen'].hour
        if gap_minutes > 30 and 6 <= hour <= 22:  # 30+ minute gaps during reasonable hours
            # Check if patients were waiting during this gap
            patients_waiting = count_waiting_patients_at_time(
                hospital_df, 
                current_patient['Doctor Seen'] + timedelta(minutes=15)  # Check midpoint of gap
            )
            
            if patients_waiting > 0:
                gap_analysis.append({
                    'Hospital': hospital,
                    'Time': current_patient['Doctor Seen'],
                    'Gap (min)': gap_minutes,
                    'Patients Waiting': patients_waiting,
                    'Shift': current_patient['Shift']
                })

gap_df = pd.DataFrame(gap_analysis)

if len(gap_df) > 0:
    print(f"\nFound {len(gap_df)} significant gaps (>30 min) with waiting patients\n")
    
    print("By Hospital:")
    print(gap_df.groupby('Hospital').agg({
        'Gap (min)': ['count', 'mean', 'max'],
        'Patients Waiting': 'mean'
    }).round(1))
    
    print("\nTop 10 Longest Gaps:")
    print(gap_df.nlargest(10, 'Gap (min)')[['Hospital', 'Time', 'Gap (min)', 'Patients Waiting', 'Shift']])
else:
    print("No significant gaps detected.")

# ============================================================================
# SUMMARY AND RECOMMENDATIONS
# ============================================================================
print("\n\n" + "="*80)
print(" SUMMARY & KEY INSIGHTS")
print("="*80)

if len(idle_df) > 0:
    total_wasted_hours = idle_df['Wait Time (min)'].sum() / 60
    avg_idle_doctors = idle_df['Idle Doctors'].mean()
    
    print(f"""
KEY FINDINGS:

1. IDLE DOCTOR INSTANCES: {len(idle_df):,} cases detected
   - Total patient wait time: {total_wasted_hours:,.1f} hours
   - Average idle doctors per incident: {avg_idle_doctors:.1f}
   - Most affected shift: {idle_df['Shift'].value_counts().index[0]}
   - Most affected hospital: {idle_df['Hospital'].value_counts().index[0]}

2. ROOT CAUSES (Hypotheses):
   - Scheduling gaps between patient handoffs
   - Doctors finishing with one patient but not immediately getting next
   - Possible lack of real-time queue visibility
   - Triage-to-doctor assignment delays
   - Shift change inefficiencies

3. POTENTIAL IMPACT:
   - If idle time was used efficiently: ~{total_wasted_hours:.0f} additional patient hours
   - Average wait reduction possible: {idle_df['Wait Time (min)'].mean():.1f} minutes per affected patient
   - Patient satisfaction improvement opportunity: High (wait time is key driver)

RECOMMENDATIONS:

1. Real-time Queue Dashboard: Give doctors visibility into waiting patients
2. Automated Assignment: Auto-assign next patient when doctor becomes available  
3. Shift Overlap: Have incoming shift start seeing patients before outgoing shift ends
4. Fast Track Utilization: Better use of fast track for lower acuity patients
5. Monitor Utilization: Track doctor utilization % as KPI (target: >75-80%)
""")
else:
    print("\nNo significant idle doctor patterns detected in current analysis.")
    print("This could mean:")
    print("  - Efficient patient flow and doctor utilization")
    print("  - Wait times are due to other factors (labs, imaging, specialty consults)")
    print("  - All doctors are consistently busy")

print("="*80)
print("\nAnalysis complete!")
