import pandas as pd
import sys

# Force output
pd.set_option('display.max_rows', None)

def diagnose_williams_pre():
    print("--- Diagnosing Williams Data (Pre-Survey) ---")
    
    label_path = "artifacts/williams_data/pre_labels.csv"
    value_path = "artifacts/williams_data/pre_values.csv"
    
    try:
        # Read Labels
        df_labels = pd.read_csv(label_path, header=None)
        qids = df_labels.iloc[0, 17:].values
        texts = df_labels.iloc[1, 17:].values # Row 1 is text
        
        # Find RecordID (Q22)
        q22_indices = [i for i, x in enumerate(qids) if str(x).strip() == "Q22"]
        print(f"Q22 found at indices (relative to data start): {q22_indices}")
        
        if not q22_indices:
            print("Q22 NOT FOUND in labels!")
            return

        col_idx = q22_indices[0] + 17 # actual column index in CSV
        
        # Read Values
        df_values = pd.read_csv(value_path, header=None)
        raw_values = df_values.iloc[3:, col_idx].astype(str).str.strip()
        
        print(f"Total Rows: {len(raw_values)}")
        print(f"Unique Values: {raw_values.nunique()}")
        
        # Check Duplicates
        dupes = raw_values[raw_values.duplicated(keep=False)]
        if not dupes.empty:
            print(f"FOUND {len(dupes)} duplicates:")
            print(dupes.value_counts())
            print(dupes.sort_values())
        else:
            print("No duplicates found in Q22.")
            
        # Check adjacent columns just in case
        print("\nChecking adjacent columns for ID-like patterns...")
        for offset in range(-2, 3):
            check_idx = col_idx + offset
            if check_idx < 0 or check_idx >= df_values.shape[1]: continue
            
            sample = df_values.iloc[3:8, check_idx].tolist()
            print(f"Col {check_idx} ({qids[col_idx+offset-17] if 0 <= col_idx+offset-17 < len(qids) else '?'}) Sample: {sample}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    diagnose_williams_pre()
