import pandas as pd
import os

def find_specific_values():
    cwd = os.getcwd()
    print(f"Current Working Directory: {cwd}")
    
    base_dir = os.path.join(cwd, "artifacts", "williams_data")
    print(f"Target Directory: {base_dir}")
    
    if not os.path.exists(base_dir):
        print(f"ERROR: Directory {base_dir} does not exist!")
        # Fallback to verify structure
        print("Listing root contents:")
        print(os.listdir(cwd))
        if os.path.exists(os.path.join(cwd, "artifacts")):
             print("Listing artifacts:")
             print(os.listdir(os.path.join(cwd, "artifacts")))
        return

    # --- PRE SURVEY ---
    pre_path = os.path.join(base_dir, "pre_values.csv")
    if os.path.exists(pre_path):
        print(f"\n--- Scanning Pre-Survey: {pre_path} ---")
        try:
            df = pd.read_csv(pre_path, header=None)
            targets = ['1046', '1019']
            
            # 1. Search everywhere
            print(f"Searching for {targets} in ENTIRE file...")
            for t in targets:
                found_count = 0
                for col in df.columns:
                    # usage of astype(str) to catch numeric or string types
                    matches = df[col].astype(str).str.strip().eq(t)
                    if matches.any():
                        rows = matches.index[matches].tolist()
                        for r in rows:
                            # Adjust row index for header (data starts at row 3 usually, but we read all)
                            print(f"  FOUND '{t}' at Row {r}, Col {col} (Value: '{df.iloc[r, col]}')")
                            found_count += 1
                if found_count == 0:
                    print(f"  '{t}' NOT FOUND anywhere.")

            # 2. Check "RecordID" column specifically (assuming Q22)
            # We need to find which column is Q22.
            # We can cross-reference pre_labels.csv
            label_path = os.path.join(base_dir, "pre_labels.csv")
            if os.path.exists(label_path):
                 df_lab = pd.read_csv(label_path, header=None)
                 # Row 0 has QIDs
                 qids = df_lab.iloc[0, :].values
                 try:
                     # Find index of Q22
                     # Note: QIDs usually start at col 17 in the supplied data format
                     q22_indices = [i for i, x in enumerate(qids) if str(x).strip() == "Q22"]
                     print(f"  Q22 Column Indices in Labels: {q22_indices}")
                     
                     for idx in q22_indices:
                         print(f"  Checking Column {idx} for duplicates of {targets}...")
                         col_vals = df.iloc[:, idx].astype(str).str.strip()
                         for t in targets:
                             matches = col_vals[col_vals == t]
                             print(f"    '{t}' count in Col {idx}: {len(matches)}")
                 except Exception as e:
                     print(f"  Error checking labels: {e}")
            
        except Exception as e:
             print(f"Error reading Pre CSV: {e}")
    else:
        print(f"Pre-Survey file not found: {pre_path}")

    # --- POST SURVEY ---
    post_path = os.path.join(base_dir, "post_values.csv")
    if os.path.exists(post_path):
        print(f"\n--- Scanning Post-Survey: {post_path} ---")
        try:
            df = pd.read_csv(post_path, header=None)
            targets = ['1023', '1011']
            
            print(f"Searching for {targets} in ENTIRE file...")
            for t in targets:
                found_count = 0
                for col in df.columns:
                    matches = df[col].astype(str).str.strip().eq(t)
                    if matches.any():
                        rows = matches.index[matches].tolist()
                        for r in rows:
                            print(f"  FOUND '{t}' at Row {r}, Col {col} (Value: '{df.iloc[r, col]}')")
                            found_count += 1
                if found_count == 0:
                    print(f"  '{t}' NOT FOUND anywhere.")
                    
        except Exception as e:
            print(f"Error reading Post CSV: {e}")
    else:
        print(f"Post-Survey file not found: {post_path}")

if __name__ == "__main__":
    find_specific_values()
