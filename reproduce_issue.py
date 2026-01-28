import pandas as pd
import io
import sys
from processing import process_survey_data

def check_duplicates(df, name):
    print(f"\n--- Checking Duplicates for {name} ---")
    if df is None:
        print("DataFrame is None")
        return

    record_id_col = "RecordID (Value)"
    if record_id_col not in df.columns:
        print(f"Column '{record_id_col}' NOT FOUND.")
        print("Available columns:", df.columns.tolist())
        
        # Check if Q22 exists maybe?
        possible_matches = [c for c in df.columns if "Q22" in c or "RecordID" in c]
        print("Possible RecordID columns:", possible_matches)
        return

    print(f"Found '{record_id_col}' column.")
    duplicates = df[df.duplicated(subset=[record_id_col], keep=False)]
    
    if not duplicates.empty:
        print(f"Found {len(duplicates)} duplicates:")
        print(duplicates[record_id_col].value_counts())
        print(duplicates[[record_id_col]])
    else:
        print("No duplicates found.")

    # Check for duplicates using different logic (ignoring case, whitespace, types)
    print("\nDeep inspection of values (first 20 unique):")
    vals = df[record_id_col].astype(str).str.strip()
    print(vals.unique()[:20])
    
    dupes_strict = vals[vals.duplicated(keep=False)]
    print(f"\nStrict duplicates count after strip/str: {len(dupes_strict)}")
    if not dupes_strict.empty:
        print(dupes_strict)


def reproduce():
    try:
        # Pre Survey
        print("Processing Pre Survey...")
        with open("pre_set/pre_values.csv", "rb") as pv, open("pre_set/pre_labels.csv", "rb") as pl:
            # We need to simulate file objects that can be read by pd.read_csv
            # process_survey_data expects file paths or file-like objects.
            # passing paths directly might be safer since we are in same dir.
            df_pre = process_survey_data("pre_set/pre_values.csv", "pre_set/pre_labels.csv", dataset_name='pre')
            check_duplicates(df_pre, "Pre-Survey")

        # Post Survey
        print("\nProcessing Post Survey...")
        df_post = process_survey_data("post_set/post_values.csv", "post_set/post_labels.csv", dataset_name='post')
        check_duplicates(df_post, "Post-Survey")

    except Exception as e:
        print(f"Error during reproduction: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    reproduce()
