# Meridian Hospital ER — Datathon Analysis

**ETAMU Datathon** | Healthcare Operations | Python, Alteryx, Machine Learning

## Problem

Meridian City Hospital's emergency room experiences patient wait times that don't correlate with staffing levels. We analyzed **15,000+ patient records** across five hospital datasets to identify the root causes of ER inefficiency.

## Key Finding

We built a **4-condition idle detection model** that identifies moments when patients wait despite all resources being available:

```
Doctor Available  +  Patient Waiting  +  Bed Available  +  Treatment Area Empty
= Definitive Idle Time Detected
```

Out of 15,000 patients, we found **116 cases of measurable idle time** (0.77%) — proving the bottleneck is **process-driven, not staffing-driven**.

**The paradox:** Night shift (1.5 doctors avg) serves patients faster than Day shift (3.5 doctors avg). Lean operations outperform over-staffing.

## Repository Structure

```
data/
  raw/              Original hospital datasets (5 CSVs + data dictionary)
  cleaned/          Processed and joined datasets
analysis/
  eda/              Exploratory data analysis notebooks
  surge_analysis/   5-7 AM surge pattern investigation
  bottleneck/       Wait time correlation and bottleneck detection
  doctor_idle_time/ Idle time detection model and validation
  er_operations/    Hourly flow and operations analysis
  thermodynamics/   System load simulation and shift optimization
  triage/           Triage-level analysis
ml/                 Regression models and feature importance analysis
workflows/          Alteryx data preparation workflows
scripts/            Python utilities (dataset generation, presentation)
docs/               Case study materials, consulting deliverables
presentation/       Final slides and visualizations
```

## Tech Stack

- **Analysis:** Python (Pandas, NumPy, Matplotlib, Seaborn), Jupyter Notebooks
- **Data Prep:** Alteryx workflows for cleaning and joining 5 datasets
- **ML:** Scikit-learn regression models for root cause analysis
- **Visualization:** Matplotlib, Seaborn, custom charts

## Approach

1. **Data Cleaning** — Joined 5 hospital datasets (patients, visits, staffing, facility, outcomes) and resolved inconsistencies
2. **Exploratory Analysis** — Identified the 5-7 AM surge pattern and shift-level performance differences
3. **Bottleneck Detection** — Built correlation analysis between staffing levels and wait times
4. **Idle Time Model** — Developed a 4-condition logical model to detect provable idle time from raw data
5. **Root Cause Analysis** — ML regression to identify which features drive wait times (process > staffing)

## Team

Datathon competition entry — East Texas A&M University
