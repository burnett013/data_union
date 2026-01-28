import pandas as pd
import os

def analyze_merged():
    # Use relative path since we are in the root
    path = "artifacts/williams_data/Pre_Survey_Merged.xlsx"
    print(f"Analyzing {path}...")
    
    try:
        df = pd.read_excel(path)
        print("Columns:", df.columns.tolist())
        
        # Identify RecordID column
        # In merged file, it should be "RecordID (Value)" or just "RecordID" depending on clean step
        # The app output has "RecordID (Value)" and "RecordID (Label)"
        
        target_col = "RecordID (Value)"
        if target_col not in df.columns:
            print(f"'{target_col}' not found. Searching for 'RecordID'...")
            cols = [c for c in df.columns if "RecordID" in c]
            print(f"Found related columns: {cols}")
            if cols: target_col = cols[0]
            else: return

        print(f"Using column: {target_col}")
        vals = df[target_col]
        print(f"Values top 20: {vals.head(20).tolist()}")
        
        # Check specific IDs
        targets = [1046, '1046', 1019, '1019'] # Check int and str variants
        print(f"\nChecking for {targets}...")
        
        for t in targets:
            # We check for exact match in the series
            matches = vals[vals == t]
            print(f"  Matches for '{t}' (type {type(t)}): {len(matches)}")
            if len(matches) > 0:
                 print(f"    Indices: {matches.index.tolist()}")
                 print(f"    Actual values types: {matches.map(type).unique()}")

        # Check duplicated() behavior
        print(f"\nPandas duplicated() count: {df.duplicated(subset=[target_col]).sum()}")
        
        # Check strict string duplicated
        str_vals = vals.astype(str).str.strip()
        print(f"Strict string duplicated count: {str_vals.duplicated().sum()}")
        
        if str_vals.duplicated().sum() > 0:
            print("Duplicates found via strict string comparison!")
            print(str_vals[str_vals.duplicated(keep=False)])
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_merged()
