import pandas as pd
import os
import io
from processing import process_survey_data

def verify_robust():
    print("--- Verifying Fix with Original Pre Values & Dummy Labels ---")
    
    val_path = "artifacts/original_pre_values.csv"
    if not os.path.exists(val_path):
        print(f"FAILED: {val_path} not found.")
        return

    # Create a dummy labels file that matches the width of values
    # Read values to get shade
    df_val = pd.read_csv(val_path, header=None)
    ncols = df_val.shape[1]
    print(f"Values shape: {df_val.shape} (Cols: {ncols})")
    
    # Create header rows for labels
    # Row 0: QIDs (Q1, Q2... QIndex)
    # Row 1: Texts
    qids = ["Meta"] * 17 + [f"Q{i}" for i in range(ncols-17)]
    # Ensure Q22 is NOT explicitly used to prove index logic works
    # Wait, col 17 (0-based) IS the 18th column.
    # In my logic, I force the 1st iteration of loop (which is index 0 of the sliced list) to be RecordID.
    # The slice is col 17 onwards.
    # So if I make dummy labels, I just need enough columns.
    
    texts = ["MetaText"] * 17 + [f"Question Text {i}" for i in range(ncols-17)]
    
    # Dummy data rows (just 0s)
    # processing.py reads df_labels then expects rows 0,1 for header and 3+ for data (which are ignored effectively for value merge?)
    # Actually processing.py merges col_lab too. So we need data rows.
    # We can just duplicate the header rows a few times to have valid length
    
    # Create dataframe
    df_lab = pd.DataFrame([qids, texts] + [texts] * (len(df_val)-2))
    
    # Save to String IO is not supported by process_survey_data file path logic if it does .read_csv(path)
    # pass file object or path?
    # buffer
    lab_buf = io.BytesIO()
    df_lab.to_csv(lab_buf, index=False, header=False)
    lab_buf.seek(0)
    
    # Run processing
    try:
        # process_survey_data handles file-like objects
        df = process_survey_data(val_path, lab_buf, dataset_name='pre')
        
        if "RecordID (Value)" in df.columns:
            print("SUCCESS: 'RecordID (Value)' column found.")
            
            # Check for 1046
            print("Checking for ID 1046...")
            d1046 = df[df["RecordID (Value)"] == "1046"]
            print(f"Occurrences of '1046': {len(d1046)}")
            
            if len(d1046) > 0:
                print("Confirmed '1046' is present.")
                if len(d1046) > 1:
                    print(f"VERIFIED: '1046' is marked as duplicate (count {len(d1046)}).")
                else:
                    print("Partial: '1046' found but not duplicated (maybe raw file only has 1?)")
                    
                 # Check strict string
                val_type = type(d1046["RecordID (Value)"].iloc[0])
                print(f"Type of ID: {val_type}")
            else:
                print("FAILED: '1046' NOT FOUND.")
        else:
            print("FAILED: RecordID column missing.")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_robust()
