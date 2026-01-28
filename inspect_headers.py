import pandas as pd
import sys

def inspect(file_path):
    print(f"--- Inspecting {file_path} ---")
    try:
        # Read first 3 rows without header to see raw structure
        df = pd.read_csv(file_path, header=None, nrows=3)
        print(df.head())
        
        # Check specific Q columns if possible (around index 17 based on processing.py)
        if df.shape[1] > 20:
            print("\nColumns around index 17 (QIDs):")
            print(df.iloc[:, 17:25])
    except Exception as e:
        print(f"Error: {e}")
    print("\n")

if __name__ == "__main__":
    inspect("pre_set/pre_labels.csv")
    inspect("pre_set/pre_values.csv")
