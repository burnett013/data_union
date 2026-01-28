import pandas as pd
import sys

# Force output
pd.set_option('display.max_rows', None)

def diagnose_all():
    print("--- Checking All Columns for Duplicates (Pre-Survey) ---")
    
    # Read Labels to get QID and Text
    df_labels = pd.read_csv("pre_set/pre_labels.csv", header=None)
    qids = df_labels.iloc[0, 17:].values
    texts = df_labels.iloc[1, 17:].values
    
    print(f"Total Columns inspected: {len(qids)}")
    
    # Read Values
    df_values = pd.read_csv("pre_set/pre_values.csv", header=None)
    data = df_values.iloc[3:, 17:]
    
    # Iterate and check duplicates
    found_dupes = []
    potential_record_ids = []
    
    for idx, (qid, text) in enumerate(zip(qids, texts)):
        col = data.iloc[:, idx]
        # Clean
        col = col.astype(str).str.strip().replace('nan', '')
        
        # Check unique
        n_unique = col.nunique()
        n_total = len(col)
        
        if n_unique < n_total:
            # We have duplicates (or empty strings repeated)
            # Check non-empty duplicates
            dupes = col[col.duplicated(keep=False)]
            non_empty_dupes = dupes[dupes != '']
            
            if not non_empty_dupes.empty:
                found_dupes.append((qid, text, non_empty_dupes.unique()))
        
        # Check if it looks like RecordID
        qid_str = str(qid).upper()
        if "Q22" in qid_str or "RECORD" in str(text).upper() or "ID" in str(text).upper():
            potential_record_ids.append((qid, text, idx))

    print("\n--- Potential RecordID Columns ---")
    for q in potential_record_ids:
        print(f"QID: {q[0]}, Text: {q[1]}, Index: {q[2]}")
        
    print("\n--- Columns with Non-Empty Duplicates ---")
    if not found_dupes:
        print("NONE Found!")
    for qid, text, dupe_vals in found_dupes:
        print(f"[{qid}] {text}: {dupe_vals}")

if __name__ == "__main__":
    diagnose_all()
