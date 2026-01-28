import pandas as pd
import os
from processing import process_survey_data

def verify():
    print("--- Verifying Fix with Original Pre Values ---")
    
    # Use the file we know exists and has duplicates
    val_path = "artifacts/original_pre_values.csv"
    # Use generic labels as proxy (we just need valid structure for processing to run)
    lab_path = "pre_set/pre_labels.csv" 
    
    if os.path.exists(val_path) and os.path.exists(lab_path):
        print(f"Processing {val_path}...")
        try:
            # We must use 'pre' or 'post' to trigger any named logic, though we removed specific named logic
            # for Q22, we kept the arg.
            df = process_survey_data(val_path, lab_path, dataset_name='pre')
            
            # Check for RecordID (Value) column existence
            if "RecordID (Value)" in df.columns:
                 print("SUCCESS: 'RecordID (Value)' column created.")
                 
                 # Check top values
                 print("Head of RecordID (Value):")
                 print(df["RecordID (Value)"].head(10).tolist())
                 
                 # Check for 1046
                 dupes = df[df.duplicated(subset=["RecordID (Value)"], keep=False)]
                 print(f"Total Duplicates Detected: {len(dupes)}")
                 if not dupes.empty:
                     print("Duplicate IDs found:")
                     print(dupes["RecordID (Value)"].unique().tolist())
                     
                 if "1046" in df["RecordID (Value)"].values:
                     # Check if it is actually flagged as duplicate
                     d1046 = df[df["RecordID (Value)"] == "1046"]
                     if len(d1046) > 1:
                         print("VERIFIED: ID '1046' is present AND flagged as duplicate (count > 1).")
                     else:
                         print("WARNING: ID '1046' is present but valid/unique (count 1).")
                 else:
                     print("FAILED: 1046 NOT FOUND in processed data.")
            else:
                 print(f"FAILED: 'RecordID (Value)' not in columns: {df.columns.tolist()}")
                 
        except Exception as e:
            print(f"Processing Error: {e}")
    else:
        print(f"Files missing: {val_path} or {lab_path}")

if __name__ == "__main__":
    verify()
