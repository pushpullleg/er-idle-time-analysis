import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Read the final_data.csv
df = pd.read_csv(DATA_DIR / "cleaned" / "final_data.csv")

# Select only the columns you need
columns_needed = [
    'Patient ID',
    'Visit ID',
    'Triage End',
    'Doctor Seen',
    'Exit Time',
    'Doctors On Duty',
    'Nurses On Duty',
    'Specialists On Call',
    'Shift',
    'Triage Level',
    'Disposition'
]

# Create the cleaned dataset
cleaned_df = df[columns_needed].copy()

# Rename columns for clarity (optional - remove if you prefer current names)
cleaned_df = cleaned_df.rename(columns={
    'Triage End': 'Triage End Timestamp',
    'Doctor Seen': 'Doctor Seen Timestamp',
    'Exit Time': 'Exit Timestamp',
    'Shift': 'Shift Type'
})

# Display info
print(f"Original dataset shape: {df.shape}")
print(f"Cleaned dataset shape: {cleaned_df.shape}")
print(f"\nFirst few rows of cleaned data:")
print(cleaned_df.head(10))
print(f"\nColumn names:")
print(cleaned_df.columns.tolist())
print(f"\nData types:")
print(cleaned_df.dtypes)
print(f"\nMissing values:")
print(cleaned_df.isnull().sum())

# Save the cleaned dataset
output_path = DATA_DIR / "cleaned" / "final_data_cleaned.csv"
cleaned_df.to_csv(output_path, index=False)
print(f"\n✅ Cleaned dataset saved to: {output_path}")
print(f"Total rows: {len(cleaned_df)}")
