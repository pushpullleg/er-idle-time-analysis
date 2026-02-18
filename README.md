# er-idle-time-analysis

Analysis of 15,000+ ER patient records from a hospital where wait times didn't correlate with staffing levels. The goal was to find out why.

We built a 4-condition idle detection model to identify moments when a patient was waiting despite a doctor, bed, and treatment area all being available. Out of 15,000 patients, 116 cases of measurable idle time were found — 0.77% of visits.

**The finding:** Night shift (avg 1.5 doctors) served patients faster than Day shift (avg 3.5 doctors). The bottleneck is process-driven, not staffing-driven.

## Approach

1. Joined 5 hospital datasets (patients, visits, staffing, facility, outcomes) and resolved inconsistencies
2. Identified a recurring 5–7 AM surge pattern across shifts
3. Built correlation analysis between staffing levels and wait times
4. Applied the 4-condition idle detection model to isolate provable idle time
5. Used scikit-learn regression to identify which features drive wait time (process variables outweigh staffing variables)

## Stack

Python (Pandas, NumPy, Matplotlib, Seaborn) · Jupyter Notebooks · Alteryx · Scikit-learn

## Structure

```
data/
├── raw/          # original hospital CSVs + data dictionary
└── cleaned/      # processed and joined datasets
analysis/
├── eda/
├── surge_analysis/
├── bottleneck/
├── doctor_idle_time/
├── er_operations/
└── ml/
docs/             # case study materials and final presentation
```

## License

MIT
