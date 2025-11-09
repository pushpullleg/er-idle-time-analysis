# Multi-Dataset EDA Workflow Guide

## Overview
You have 5 related datasets from Meridian City Hospital ER:
1. **Hospital_Facility.csv** - Facility information
2. **Hospital_Outcomes.csv** - Patient outcomes
3. **Hospital_Patients.csv** - Patient information
4. **Hospital_Staffing_EAST_LOCATION.csv** - Staffing data
5. **Hospital_Visits.csv** - Visit records

## Recommended EDA Strategy

### Step 1: Load All Datasets (Section 1)
- ✅ All 5 datasets are automatically loaded
- Review the overview of all datasets
- Understand the size and structure of each

### Step 2: Understand Relationships (Section 1.5)
- Identify common columns (join keys)
- Understand how datasets relate to each other
- Determine which datasets to analyze together vs. separately

### Step 3: Choose Your Analysis Approach

#### Option A: Analyze Each Dataset Individually (Recommended for Initial EDA)
1. **Start with the most important dataset** (likely `visits` or `outcomes`)
2. In Section 1.5, set `current_dataset_name = 'visits'`
3. Run Sections 2-5 for that dataset
4. Document findings
5. Repeat for other datasets

#### Option B: Create Merged Datasets (For Deeper Analysis)
1. Identify join keys (Patient ID, Visit ID, Facility ID, etc.)
2. Merge related datasets (e.g., Patients + Visits + Outcomes)
3. Analyze the merged dataset
4. This gives you a complete picture but can be complex

#### Option C: Quick Comparison Across All Datasets
1. Run Section 2-5 for each dataset separately
2. Compare findings across datasets
3. Look for patterns and relationships

### Step 4: Team Workflow with Multiple Datasets

**Member 1:** Data Quality & Univariate Analysis
- Analyze 2-3 datasets in parallel
- Focus on: missing values, outliers, distributions
- Compare data quality issues across datasets

**Member 2:** Bivariate Analysis
- Analyze relationships within each dataset
- Focus on correlations and feature relationships
- Identify key relationships between datasets

**Member 3:** Multivariate Analysis & Relationships
- Analyze patterns across datasets
- Create merged datasets if needed
- Identify cross-dataset insights

## Quick Reference: Dataset Selection

To analyze a specific dataset, in Section 1.5, change:

```python
current_dataset_name = 'visits'  # Options: 'facility', 'outcomes', 'patients', 'staffing', 'visits'
```

Or create a merged dataset:

```python
# Example: Merge patients and visits
merged_df = datasets['patients'].merge(
    datasets['visits'], 
    on='PatientID',  # Replace with actual column name
    how='inner'
)
current_dataset = merged_df
df = merged_df.copy()
```

## Common Hospital Data Relationships

Based on typical hospital data structures:

```
Patients (1) ──< (Many) Visits
Visits (1) ──< (Many) Outcomes
Visits (Many) >── (1) Facility
Facility (1) ──< (Many) Staffing
```

## Questions to Answer

1. **Which dataset is the primary focus?** (Usually Visits or Outcomes)
2. **What are the join keys?** (Patient ID, Visit ID, Facility ID, etc.)
3. **Do you need merged data?** (For some analyses, yes)
4. **What's the time period?** (Check date columns across datasets)
5. **Are there duplicates?** (Same patient, multiple visits?)

## Time Management

- **15 min:** Load all datasets, understand relationships
- **20 min:** Quick EDA on primary dataset (likely Visits)
- **15 min:** EDA on secondary datasets (Outcomes, Patients)
- **10 min:** Cross-dataset analysis and merging

## Tips

1. **Start with Visits dataset** - Usually contains the most comprehensive information
2. **Check the Data Dictionary** - Review `Meridian_City_Hospital_Data_Dictionary.xlsx` for field definitions
3. **Identify the target variable early** - Is it in Outcomes? Visits?
4. **Look for date columns** - Time-based analysis might be important
5. **Check for missing join keys** - Some datasets might not have direct relationships

## Example Workflow

```python
# 1. Load all datasets (done in Section 1)
# 2. Understand relationships (Section 1.5)

# 3. Analyze Visits dataset first
current_dataset_name = 'visits'
df = datasets['visits'].copy()
# Run Sections 2-5

# 4. Analyze Outcomes dataset
current_dataset_name = 'outcomes'
df = datasets['outcomes'].copy()
# Run Sections 2-5

# 5. Merge and analyze combined data
merged = datasets['visits'].merge(datasets['outcomes'], on='VisitID')
df = merged.copy()
# Run Sections 2-5 on merged data
```

Good luck with your datathon! 🏥📊

