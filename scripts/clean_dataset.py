import pandas as pd
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data", "labels")

print("--- STARTING DATA CLEANING SCRIPT ---")
try:
    df = pd.read_csv(os.path.join(DATA_DIR, 'deep_sea_labeled.csv'))
    print(f"\n[INFO] Successfully loaded 'deep_sea_labeled.csv'. Shape: {df.shape}")
except FileNotFoundError:
    print(f"[ERROR] '{os.path.join(DATA_DIR, 'deep_sea_labeled.csv')}' not found. Exiting.")
    exit()

# Ensure the column names are correct
if 'sequence' not in df.columns or 'taxonomy' not in df.columns:
    print("[ERROR] The CSV file is missing the required 'sequence' or 'taxonomy' column headers.")
    exit()

df['taxonomy'] = df['taxonomy'].str.strip()
print("\n[INFO] Removed leading/trailing whitespace from taxonomy labels.")
print("\n[DIAGNOSTIC] Class distribution in the ORIGINAL file (after stripping whitespace):")
original_counts = df['taxonomy'].value_counts()
print(original_counts)

classes_to_keep = original_counts[original_counts > 1].index
cleaned_df = df[df['taxonomy'].isin(classes_to_keep)]

print(f"\n[INFO] Cleaned dataset shape: {cleaned_df.shape}")
print("\n[DIAGNOSTIC] Class distribution in the NEW CLEAN file:")
cleaned_counts = cleaned_df['taxonomy'].value_counts()
print(cleaned_counts)

if cleaned_df.empty:
    print("\n[ERROR] The cleaned dataset is empty! No class had more than one sample.")
else:
    cleaned_df.to_csv(os.path.join(DATA_DIR, 'deep_sea_labeled_clean.csv'), index=False)
    print(f"\n[SUCCESS] Cleaned dataset saved to '{os.path.join(DATA_DIR, 'deep_sea_labeled_clean.csv')}'")