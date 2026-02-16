#!/usr/bin/env python3
"""
ER System Load Simulation and Analysis
Meridian City Hospital Emergency Department

This script implements a complete analysis of ER hourly system load patterns
over 90 days, including data preparation, simulation, metrics computation,
visualizations, and interpretation.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from scipy import stats
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# 1. DATA PREPARATION
# ============================================================================

def prepare_and_clean_data(input_file, output_file):
    """
    Load, clean, and prepare the dataset for analysis.
    Remove duplicates and unnecessary derived columns.
    """
    print("=" * 80)
    print("STEP 1: DATA PREPARATION AND CLEANING")
    print("=" * 80)
    
    # Load data
    df = pd.read_csv(input_file)
    print(f"\n✓ Loaded {len(df)} records from {input_file}")
    print(f"✓ Initial columns: {len(df.columns)}")
    
    # Remove exact duplicates
    df_clean = df.drop_duplicates()
    print(f"✓ Removed {len(df) - len(df_clean)} exact duplicate rows")
    
    # Identify duplicate derived columns to remove
    # These are columns that are computed from other columns:
    # - Visit Date, Visit Time (derived from Arrival Time)
    # - WaitTime for Reg, Registration process time, Triage process time, 
    #   WaitTime after Triage, DoctorVisit to Exit, TotalTime(Arrival To Exit)
    #   (all derived from timestamp fields)
    # - Staff Date (derived from Arrival Time)
    
    columns_to_drop = [
        'Visit Date',           # Derived from Arrival Time
        'Visit Time',           # Derived from Arrival Time
        'WaitTime for Reg',     # Derived from timestamps
        'Registration process time',  # Derived
        'Triage process time',        # Derived
        'WaitTime after Triage',      # Derived
        'DoctorVisit to Exit',        # Derived
        'TotalTime(Arrival To Exit)', # Derived
        'Staff Date',                 # Derived from Arrival Time
        'ShiftStart',                 # Redundant with Shift
        'ShiftEnd'                    # Redundant with Shift
    ]
    
    df_clean = df_clean.drop(columns=columns_to_drop)
    print(f"✓ Dropped {len(columns_to_drop)} derived/redundant columns")
    
    # Convert timestamp columns to datetime
    timestamp_cols = ['Arrival Time', 'Registration Start', 'Registration End',
                      'Triage Start', 'Triage End', 'Doctor Seen', 'Exit Time']
    
    for col in timestamp_cols:
        df_clean[col] = pd.to_datetime(df_clean[col])
    
    print(f"✓ Converted timestamp columns to datetime")
    
    # Fill any missing values
    missing_before = df_clean.isnull().sum().sum()
    if missing_before > 0:
        print(f"⚠ Found {missing_before} missing values, filling appropriately...")
        df_clean = df_clean.fillna(method='ffill').fillna(method='bfill')
    
    # Sort by Arrival Time
    df_clean = df_clean.sort_values('Arrival Time').reset_index(drop=True)
    
    print(f"✓ Final cleaned dataset: {len(df_clean)} records, {len(df_clean.columns)} columns")
    print(f"\nCleaned columns:")
    for i, col in enumerate(df_clean.columns, 1):
        print(f"  {i:2d}. {col}")
    
    # Save cleaned data
    df_clean.to_csv(output_file, index=False)
    print(f"\n✓ Saved cleaned data to {output_file}")
    
    return df_clean


# ============================================================================
# 2. HOURLY SIMULATION AND LOAD CALCULATION
# ============================================================================

def create_hourly_timeseries(df):
    """
    Create a continuous hourly time series for 90 days.
    Aggregate Arrivals and Exits per hour.
    """
    print("\n" + "=" * 80)
    print("STEP 2: HOURLY TIME SERIES CREATION AND SIMULATION")
    print("=" * 80)
    
    # Get date range (approximately 90 days)
    min_date = df['Arrival Time'].min()
    max_date = df['Exit Time'].max()
    
    print(f"\n✓ Data spans from {min_date} to {max_date}")
    print(f"✓ Duration: {(max_date - min_date).days} days")
    
    # Create hourly bins
    hourly_index = pd.date_range(
        start=min_date.floor('H'),
        end=max_date.ceil('H'),
        freq='H'
    )
    
    print(f"✓ Created {len(hourly_index)} hourly bins")
    
    # Count arrivals per hour
    df['Arrival Hour'] = df['Arrival Time'].dt.floor('H')
    arrivals_hourly = df['Arrival Hour'].value_counts().sort_index()
    
    # Count exits per hour
    df['Exit Hour'] = df['Exit Time'].dt.floor('H')
    exits_hourly = df['Exit Hour'].value_counts().sort_index()
    
    # Create the hourly dataframe
    hourly_df = pd.DataFrame({
        'Hour': hourly_index,
        'Arrivals': 0,
        'Exits': 0
    })
    
    # Fill in arrivals and exits
    for hour, count in arrivals_hourly.items():
        hourly_df.loc[hourly_df['Hour'] == hour, 'Arrivals'] = count
    
    for hour, count in exits_hourly.items():
        hourly_df.loc[hourly_df['Hour'] == hour, 'Exits'] = count
    
    # Set Hour as index
    hourly_df.set_index('Hour', inplace=True)
    
    print(f"\n✓ Hourly aggregation complete:")
    print(f"  - Total Arrivals: {hourly_df['Arrivals'].sum():,}")
    print(f"  - Total Exits: {hourly_df['Exits'].sum():,}")
    print(f"  - Avg Arrivals/hour: {hourly_df['Arrivals'].mean():.2f}")
    print(f"  - Avg Exits/hour: {hourly_df['Exits'].mean():.2f}")
    
    return hourly_df


def simulate_system_load(hourly_df):
    """
    Run the system load simulation using the dynamics formula:
    Backlog[t] = max(0, Backlog[t-1] + Arrivals[t] - Exits[t])
    System_Load[t] = Backlog[t]
    """
    print("\n" + "=" * 80)
    print("STEP 3: SYSTEM LOAD SIMULATION")
    print("=" * 80)
    
    # Initialize backlog
    backlog = np.zeros(len(hourly_df))
    system_load = np.zeros(len(hourly_df))
    
    arrivals = hourly_df['Arrivals'].values
    exits = hourly_df['Exits'].values
    
    # Run simulation
    for t in range(len(hourly_df)):
        if t == 0:
            backlog[t] = max(0, arrivals[t] - exits[t])
        else:
            backlog[t] = max(0, backlog[t-1] + arrivals[t] - exits[t])
        
        system_load[t] = backlog[t]
    
    # Add to dataframe
    hourly_df['Backlog'] = backlog
    hourly_df['System_Load'] = system_load
    
    print(f"\n✓ Simulation complete for {len(hourly_df)} hourly periods")
    print(f"\nSystem Load Statistics:")
    print(f"  - Min Load: {system_load.min():.2f} patients")
    print(f"  - Max Load: {system_load.max():.2f} patients")
    print(f"  - Mean Load: {system_load.mean():.2f} patients")
    print(f"  - Median Load: {np.median(system_load):.2f} patients")
    print(f"  - Std Dev: {system_load.std():.2f} patients")
    
    return hourly_df


# ============================================================================
# 3. METRICS AND ANALYSIS
# ============================================================================

def compute_analysis_metrics(hourly_df):
    """
    Compute all required metrics: descriptive stats, percentiles, 
    lag correlations, volatility, throughput.
    """
    print("\n" + "=" * 80)
    print("STEP 4: METRICS AND ANALYSIS COMPUTATION")
    print("=" * 80)
    
    arrivals = hourly_df['Arrivals'].values
    exits = hourly_df['Exits'].values
    system_load = hourly_df['System_Load'].values
    
    metrics = {}
    
    # --- Descriptive Stats ---
    metrics['min_load'] = float(system_load.min())
    metrics['max_load'] = float(system_load.max())
    metrics['mean_load'] = float(system_load.mean())
    metrics['median_load'] = float(np.median(system_load))
    metrics['std_load'] = float(system_load.std())
    metrics['q75_load'] = float(np.percentile(system_load, 75))
    metrics['q90_load'] = float(np.percentile(system_load, 90))
    metrics['q95_load'] = float(np.percentile(system_load, 95))
    
    # --- Temporal Stats ---
    max_idx = np.argmax(system_load)
    min_idx = np.argmin(system_load)
    metrics['max_load_time'] = hourly_df.index[max_idx]
    metrics['min_load_time'] = hourly_df.index[min_idx]
    
    # --- Peak Duration ---
    threshold = metrics['mean_load'] + metrics['std_load']
    above_threshold = system_load > threshold
    if np.any(above_threshold):
        # Count consecutive hours above threshold
        peaks = np.diff(np.concatenate(([0], above_threshold, [0])).astype(int))
        peak_starts = np.where(peaks == 1)[0]
        peak_ends = np.where(peaks == -1)[0]
        peak_durations = peak_ends - peak_starts
        metrics['max_peak_duration'] = int(peak_durations.max()) if len(peak_durations) > 0 else 0
        metrics['avg_peak_duration'] = float(peak_durations.mean()) if len(peak_durations) > 0 else 0
    else:
        metrics['max_peak_duration'] = 0
        metrics['avg_peak_duration'] = 0.0
    
    # --- Lag Correlation ---
    lag_correlations = {}
    for lag in range(1, 7):
        if lag < len(arrivals):
            # Lag exits to compare with arrivals
            corr = np.corrcoef(arrivals[:-lag], exits[lag:])[0, 1]
            lag_correlations[f'lag_{lag}_hours'] = float(corr) if not np.isnan(corr) else 0.0
    metrics['lag_correlations'] = lag_correlations
    
    # --- Volatility Index (24-hour rolling std dev) ---
    window = min(24, len(system_load))
    rolling_std = pd.Series(system_load).rolling(window=window).std()
    metrics['avg_volatility'] = float(rolling_std.mean())
    metrics['max_volatility'] = float(rolling_std.max())
    
    # --- Throughput Ratio ---
    metrics['total_arrivals'] = int(arrivals.sum())
    metrics['total_exits'] = int(exits.sum())
    metrics['overall_throughput_ratio'] = float(exits.sum() / arrivals.sum()) if arrivals.sum() > 0 else 0.0
    
    # Daily throughput
    hourly_df['Date'] = hourly_df.index.date
    daily_arrivals = hourly_df.groupby('Date')['Arrivals'].sum()
    daily_exits = hourly_df.groupby('Date')['Exits'].sum()
    daily_throughput = (daily_exits / daily_arrivals).replace([np.inf, -np.inf], np.nan)
    metrics['daily_avg_throughput_ratio'] = float(daily_throughput.mean())
    metrics['daily_min_throughput_ratio'] = float(daily_throughput.min())
    metrics['daily_max_throughput_ratio'] = float(daily_throughput.max())
    
    print(f"\n✓ Metrics computed successfully")
    print(f"\n--- DESCRIPTIVE STATISTICS ---")
    print(f"  Min Load: {metrics['min_load']:.2f}")
    print(f"  Max Load: {metrics['max_load']:.2f}")
    print(f"  Mean Load: {metrics['mean_load']:.2f}")
    print(f"  Median Load: {metrics['median_load']:.2f}")
    print(f"  Std Dev: {metrics['std_load']:.2f}")
    
    print(f"\n--- PERCENTILES ---")
    print(f"  75th: {metrics['q75_load']:.2f}")
    print(f"  90th: {metrics['q90_load']:.2f}")
    print(f"  95th: {metrics['q95_load']:.2f}")
    
    print(f"\n--- TEMPORAL ---")
    print(f"  Max Load: {metrics['max_load']:.2f} at {metrics['max_load_time']}")
    print(f"  Min Load: {metrics['min_load']:.2f} at {metrics['min_load_time']}")
    
    print(f"\n--- PEAK ANALYSIS ---")
    print(f"  Max Peak Duration: {metrics['max_peak_duration']} hours")
    print(f"  Avg Peak Duration: {metrics['avg_peak_duration']:.2f} hours")
    
    print(f"\n--- LAG CORRELATIONS ---")
    for lag, corr in lag_correlations.items():
        print(f"  {lag}: {corr:.4f}")
    
    print(f"\n--- VOLATILITY ---")
    print(f"  Avg Volatility (24-hr rolling): {metrics['avg_volatility']:.2f}")
    print(f"  Max Volatility: {metrics['max_volatility']:.2f}")
    
    print(f"\n--- THROUGHPUT ---")
    print(f"  Overall Ratio (Exits/Arrivals): {metrics['overall_throughput_ratio']:.4f}")
    print(f"  Daily Avg Ratio: {metrics['daily_avg_throughput_ratio']:.4f}")
    
    return metrics


# ============================================================================
# 4. VISUALIZATIONS
# ============================================================================

def create_visualizations(hourly_df, output_dir):
    """
    Generate all required visualizations:
    - Time series plot
    - Arrivals/Exits overlay
    - Heatmap by hour/day
    - Annotated peaks and recovery
    """
    print("\n" + "=" * 80)
    print("STEP 5: GENERATING VISUALIZATIONS")
    print("=" * 80)
    
    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (16, 10)
    
    # --- Plot 1: System Load Over Time ---
    fig, ax = plt.subplots(figsize=(18, 6))
    ax.plot(hourly_df.index, hourly_df['System_Load'], linewidth=2, color='#2E86AB', label='System Load')
    ax.fill_between(hourly_df.index, hourly_df['System_Load'], alpha=0.3, color='#2E86AB')
    
    # Annotate max load
    max_idx = hourly_df['System_Load'].idxmax()
    max_load = hourly_df.loc[max_idx, 'System_Load']
    ax.scatter([max_idx], [max_load], color='red', s=200, zorder=5, marker='X')
    ax.annotate(f'Max: {max_load:.0f}', xy=(max_idx, max_load),
                xytext=(10, 10), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    
    ax.set_xlabel('Time', fontsize=12, fontweight='bold')
    ax.set_ylabel('System Load (Patients in Queue)', fontsize=12, fontweight='bold')
    ax.set_title('ER System Load - Hourly Simulation (90 Days)', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/er_hourly_load_trend.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: er_hourly_load_trend.png")
    plt.close()
    
    # --- Plot 2: Arrivals vs Exits Overlay ---
    fig, ax = plt.subplots(figsize=(18, 7))
    ax.plot(hourly_df.index, hourly_df['Arrivals'], linewidth=2, label='Arrivals', color='#06A77D', alpha=0.8)
    ax.plot(hourly_df.index, hourly_df['Exits'], linewidth=2, label='Exits', color='#D62828', alpha=0.8)
    ax.fill_between(hourly_df.index, hourly_df['Arrivals'], alpha=0.2, color='#06A77D')
    ax.fill_between(hourly_df.index, hourly_df['Exits'], alpha=0.2, color='#D62828')
    
    ax.set_xlabel('Time', fontsize=12, fontweight='bold')
    ax.set_ylabel('Count (Patients/Hour)', fontsize=12, fontweight='bold')
    ax.set_title('ER Arrivals vs Exits - Hourly Pattern', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11, loc='upper right')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/er_arrivals_exits_comparison.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: er_arrivals_exits_comparison.png")
    plt.close()
    
    # --- Plot 3: Heatmap - Hour of Day vs Day of Week ---
    hourly_df_copy = hourly_df.copy()
    hourly_df_copy['Hour_of_Day'] = hourly_df_copy.index.hour
    hourly_df_copy['Day_of_Week'] = hourly_df_copy.index.day_name()
    
    # Create pivot table for heatmap
    heatmap_data = hourly_df_copy.pivot_table(
        values='System_Load',
        index='Hour_of_Day',
        columns='Day_of_Week',
        aggfunc='mean'
    )
    
    # Reorder columns to start with Monday
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_data = heatmap_data[[d for d in day_order if d in heatmap_data.columns]]
    
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='YlOrRd', cbar_kws={'label': 'Avg Load'},
                linewidths=0.5, ax=ax)
    ax.set_xlabel('Day of Week', fontsize=12, fontweight='bold')
    ax.set_ylabel('Hour of Day', fontsize=12, fontweight='bold')
    ax.set_title('Average ER System Load - Hour of Day × Day of Week', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/er_heatmap.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: er_heatmap.png")
    plt.close()
    
    # --- Plot 4: Daily Load Distribution ---
    hourly_df_copy['Date'] = hourly_df_copy.index.date
    daily_max = hourly_df_copy.groupby('Date')['System_Load'].max()
    daily_mean = hourly_df_copy.groupby('Date')['System_Load'].mean()
    
    fig, ax = plt.subplots(figsize=(16, 6))
    ax.plot(daily_max.index, daily_max.values, marker='o', linewidth=2, 
            label='Daily Max Load', color='#D62828')
    ax.plot(daily_mean.index, daily_mean.values, marker='s', linewidth=2, 
            label='Daily Mean Load', color='#2E86AB')
    ax.fill_between(daily_max.index, daily_max.values, alpha=0.2, color='#D62828')
    ax.fill_between(daily_mean.index, daily_mean.values, alpha=0.2, color='#2E86AB')
    
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('System Load (Patients)', fontsize=12, fontweight='bold')
    ax.set_title('Daily Maximum and Average ER System Load', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/er_daily_load_distribution.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: er_daily_load_distribution.png")
    plt.close()
    
    print(f"\n✓ All visualizations created successfully")


# ============================================================================
# 5. ANALYTICAL REPORT
# ============================================================================

def generate_analytical_report(metrics, hourly_df, output_file):
    """
    Generate a comprehensive analytical report following the Interpretation Guide.
    """
    print("\n" + "=" * 80)
    print("STEP 6: GENERATING ANALYTICAL REPORT")
    print("=" * 80)
    
    report = []
    report.append("=" * 80)
    report.append("ER SYSTEM LOAD ANALYSIS - COMPREHENSIVE REPORT")
    report.append("Meridian City Hospital Emergency Department")
    report.append("=" * 80)
    report.append("")
    report.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Analysis Period: {hourly_df.index[0]} to {hourly_df.index[-1]}")
    report.append(f"Duration: {(hourly_df.index[-1] - hourly_df.index[0]).days} days")
    report.append("")
    
    # --- EXECUTIVE SUMMARY ---
    report.append("\n" + "=" * 80)
    report.append("EXECUTIVE SUMMARY")
    report.append("=" * 80)
    report.append(f"""
The analysis covers a {(hourly_df.index[-1] - hourly_df.index[0]).days}-day period of ER operations,
simulating hourly system load based on patient arrivals and exits. The ER system
demonstrates cyclical load patterns with significant variability across hours and days.

Key Findings:
- The ER operates with highly dynamic patient flow
- Load ranges from {metrics['min_load']:.0f} to {metrics['max_load']:.0f} patients in queue
- Average operational load: {metrics['mean_load']:.1f} patients
- The system experiences peak pressures lasting up to {metrics['max_peak_duration']} continuous hours
""")
    
    # --- 1. LOAD BEHAVIOR ---
    report.append("\n" + "=" * 80)
    report.append("1. LOAD BEHAVIOR ANALYSIS")
    report.append("=" * 80)
    
    hourly_df_copy = hourly_df.copy()
    hourly_df_copy['Hour_of_Day'] = hourly_df_copy.index.hour
    hourly_by_hour = hourly_df_copy.groupby('Hour_of_Day')['System_Load'].agg(['mean', 'std', 'max'])
    
    peak_hour = hourly_by_hour['mean'].idxmax()
    trough_hour = hourly_by_hour['mean'].idxmin()
    
    report.append(f"""
Load Pattern Classification: CYCLICAL with significant variability

Peak Activity:
  - Hour of Day: {peak_hour}:00-{peak_hour}:59 (avg {hourly_by_hour.loc[peak_hour, 'mean']:.1f} patients)
  - Maximum recorded: {hourly_by_hour.loc[peak_hour, 'max']:.0f} patients
  - Std Dev: {hourly_by_hour.loc[peak_hour, 'std']:.2f}

Trough Activity:
  - Hour of Day: {trough_hour}:00-{trough_hour}:59 (avg {hourly_by_hour.loc[trough_hour, 'mean']:.1f} patients)
  - Std Dev: {hourly_by_hour.loc[trough_hour, 'std']:.2f}

Interpretation:
The ER shows a predictable cyclical pattern with peak loads during {peak_hour}:00-{peak_hour}:59 hours,
indicating consistent surge periods that likely correspond to business hours. The load is relatively
stable with a coefficient of variation of {(metrics['std_load']/metrics['mean_load']):.2%}, suggesting
moderate operational predictability.
""")
    
    # --- 2. PEAKS AND RECOVERY ---
    report.append("\n" + "=" * 80)
    report.append("2. PEAKS AND RECOVERY ANALYSIS")
    report.append("=" * 80)
    
    threshold = metrics['mean_load'] + metrics['std_load']
    above_threshold = hourly_df['System_Load'] > threshold
    
    if np.any(above_threshold):
        peaks = np.diff(np.concatenate(([0], above_threshold.values, [0])).astype(int))
        peak_starts_idx = np.where(peaks == 1)[0]
        peak_ends_idx = np.where(peaks == -1)[0]
        peak_count = len(peak_starts_idx)
    else:
        peak_count = 0
    
    report.append(f"""
High-Load Period Definition: System Load > Mean + 1 Std Dev ({threshold:.2f} patients)

Peak Statistics:
  - Number of high-load events: {peak_count}
  - Maximum peak duration: {metrics['max_peak_duration']} consecutive hours
  - Average peak duration: {metrics['avg_peak_duration']:.1f} hours

Recovery Dynamics:
The system exhibits {['strong', 'moderate', 'weak'][min(2, int(metrics['avg_peak_duration']/5))]} recovery capability,
with peaks lasting an average of {metrics['avg_peak_duration']:.1f} hours.
This indicates {'efficient' if metrics['avg_peak_duration'] < 4 else 'moderate' if metrics['avg_peak_duration'] < 8 else 'slow'} throughput
and {'good' if metrics['avg_peak_duration'] < 4 else 'acceptable' if metrics['avg_peak_duration'] < 8 else 'concerning'} operational management.

Critical Insight:
Periods exceeding {metrics['max_peak_duration']} hours of sustained high load represent critical
operational stress points requiring immediate intervention or resource augmentation.
""")
    
    # --- 3. RESPONSE DYNAMICS ---
    report.append("\n" + "=" * 80)
    report.append("3. RESPONSE DYNAMICS - LAG CORRELATION ANALYSIS")
    report.append("=" * 80)
    
    report.append(f"""
Lag Correlation Results (Exits vs Arrivals):
""")
    for lag, corr in metrics['lag_correlations'].items():
        report.append(f"  {lag}: {corr:+.4f}")
    
    max_lag = max(metrics['lag_correlations'].items(), key=lambda x: abs(x[1]))
    report.append(f"""
Interpretation:
The maximum correlation ({max_lag[1]:+.4f}) occurs at {max_lag[0]}, indicating that
exit patterns best align with arrival patterns from {max_lag[0].split('_')[1]} hours prior.

Operational Meaning:
- High positive correlation: Exits respond quickly to arrivals (efficient throughput)
- Time lag indicates: Average patient processing time from arrival to exit
- Implication: Staff capacity appears {'well-matched' if max_lag[1] > 0.5 else 'moderately aligned' if max_lag[1] > 0.3 else 'misaligned'} with patient flow

Recommendations:
The exit lag of approximately {max_lag[0].split('_')[1]} hours suggests that patients take
this long to progress through the ER. Consider analyzing:
- Triage efficiency
- Doctor availability bottlenecks
- Bed turnover times
- Discharge processing delays
""")
    
    # --- 4. SYSTEM EFFICIENCY ---
    report.append("\n" + "=" * 80)
    report.append("4. SYSTEM EFFICIENCY - THROUGHPUT ANALYSIS")
    report.append("=" * 80)
    
    report.append(f"""
Overall Throughput Metrics:
  - Total Arrivals (90 days): {metrics['total_arrivals']:,} patients
  - Total Exits (90 days): {metrics['total_exits']:,} patients
  - Throughput Ratio: {metrics['overall_throughput_ratio']:.2%}
  - Backlog: {metrics['total_arrivals'] - metrics['total_exits']:,} patients remaining

Daily Throughput Analysis:
  - Average daily ratio: {metrics['daily_avg_throughput_ratio']:.2%}
  - Range: {metrics['daily_min_throughput_ratio']:.2%} to {metrics['daily_max_throughput_ratio']:.2%}

Efficiency Assessment:
A throughput ratio of {metrics['overall_throughput_ratio']:.2%} indicates that approximately
{metrics['overall_throughput_ratio']*100:.1f}% of arriving patients exit daily. 
The {'low' if metrics['overall_throughput_ratio'] < 0.5 else 'moderate' if metrics['overall_throughput_ratio'] < 0.8 else 'high'} ratio
suggests {'significant capacity constraints' if metrics['overall_throughput_ratio'] < 0.5 else 'balanced operations' if metrics['overall_throughput_ratio'] < 0.8 else 'efficient throughput'}.

Daily variability of {(metrics['daily_max_throughput_ratio']-metrics['daily_min_throughput_ratio']):.2%} indicates
operational inconsistency, possibly due to staffing variations or admission patterns.
""")
    
    # --- 5. STRATEGIC INSIGHTS AND RECOMMENDATIONS ---
    report.append("\n" + "=" * 80)
    report.append("5. STRATEGIC INSIGHTS AND RECOMMENDATIONS")
    report.append("=" * 80)
    
    volatility_level = 'high' if metrics['max_volatility'] > 10 else 'moderate' if metrics['max_volatility'] > 5 else 'low'
    
    report.append(f"""
Key Operational Findings:

1. CAPACITY & LOAD MANAGEMENT
   - Peak load of {metrics['max_load']:.0f} patients occurs at {metrics['max_load_time'].strftime('%A %H:%M')}
   - 95th percentile load: {metrics['q95_load']:.0f} patients
   - Volatility is {volatility_level} (rolling 24-hr std dev: {metrics['max_volatility']:.2f})
   
   ACTION ITEMS:
   ✓ Increase staffing during identified peak hours ({peak_hour}:00-{peak_hour}:59)
   ✓ Implement surge protocols when load exceeds {metrics['q95_load']:.0f} patients
   ✓ Cross-train staff to handle surge capacity

2. DISCHARGE & EXIT OPTIMIZATION
   - Current exit lag: approximately {max_lag[0].split('_')[1]} hours after arrival
   - Throughput ratio: {metrics['overall_throughput_ratio']:.2%}
   
   ACTION ITEMS:
   ✓ Streamline discharge processes to reduce patient dwell time
   ✓ Implement bed management protocols
   ✓ Consider fast-track pathways for lower-acuity patients
   ✓ Improve coordination between doctor and exit/admission decisions

3. TRIAGE & FLOW EFFICIENCY
   - Load stability coefficient of variation: {(metrics['std_load']/metrics['mean_load']):.2%}
   - Predictable patterns enable proactive scheduling
   
   ACTION ITEMS:
   ✓ Align triage staff capacity with predictable hourly patterns
   ✓ Pre-position resources before known peak hours
   ✓ Implement dynamic triage to prioritize faster-resolution cases

4. RESOURCE ALLOCATION
   - Highest utilization: {peak_hour}:00-{peak_hour}:59 (mean {hourly_by_hour.loc[peak_hour, 'mean']:.1f} patients)
   - Lowest utilization: {trough_hour}:00-{trough_hour}:59 (mean {hourly_by_hour.loc[trough_hour, 'mean']:.1f} patients)
   - Peak-to-trough ratio: {(hourly_by_hour.loc[peak_hour, 'mean'] / hourly_by_hour.loc[trough_hour, 'mean']):.1f}x
   
   ACTION ITEMS:
   ✓ Implement shift overlaps during transition hours
   ✓ Use part-time/on-call staff for surge periods
   ✓ Consider shift scheduling optimization to match demand patterns

5. PREDICTIVE MONITORING
   - System load is {'highly', 'moderately', 'weakly'}[min(2, int((metrics['overall_throughput_ratio']*100)/50))] predictable
   - Implement real-time load monitoring dashboards
   
   ACTION ITEMS:
   ✓ Set alerts at 75th percentile ({metrics['q75_load']:.0f}) and 90th percentile ({metrics['q90_load']:.0f})
   ✓ Activate surge protocols when 95th percentile exceeded
   ✓ Enable staff to anticipate capacity constraints
""")
    
    report.append("\n" + "=" * 80)
    report.append("END OF REPORT")
    report.append("=" * 80)
    
    report_text = "\n".join(report)
    
    with open(output_file, 'w') as f:
        f.write(report_text)
    
    print(f"✓ Report generated: {output_file}")
    print("\n" + report_text)
    
    return report_text


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("\n" + "=" * 80)
    print("ER SYSTEM LOAD SIMULATION AND ANALYSIS")
    print("Meridian City Hospital Emergency Department")
    print("=" * 80)
    
    # Define paths
    project_root = Path(__file__).resolve().parent.parent.parent
    input_file = str(project_root / "data" / "cleaned" / "final_data.csv")
    output_dir = str(Path(__file__).resolve().parent)
    cleaned_file = f'{output_dir}/improved_final_data.csv'
    simulation_file = f'{output_dir}/er_hourly_load_simulation.csv'
    report_file = f'{output_dir}/er_load_insights.txt'
    
    # Step 1: Data Preparation
    df = prepare_and_clean_data(input_file, cleaned_file)
    
    # Step 2: Create hourly time series
    hourly_df = create_hourly_timeseries(df)
    
    # Step 3: Simulate system load
    hourly_df = simulate_system_load(hourly_df)
    
    # Step 4: Compute metrics
    metrics = compute_analysis_metrics(hourly_df)
    
    # Step 5: Generate visualizations
    create_visualizations(hourly_df, output_dir)
    
    # Step 6: Generate report
    generate_analytical_report(metrics, hourly_df, report_file)
    
    # Export simulation data
    hourly_df.to_csv(simulation_file)
    print(f"\n✓ Saved simulation data: {simulation_file}")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)
    print(f"\nGenerated Files:")
    print(f"  1. {cleaned_file}")
    print(f"  2. {simulation_file}")
    print(f"  3. {output_dir}/er_hourly_load_trend.png")
    print(f"  4. {output_dir}/er_arrivals_exits_comparison.png")
    print(f"  5. {output_dir}/er_heatmap.png")
    print(f"  6. {output_dir}/er_daily_load_distribution.png")
    print(f"  7. {report_file}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
