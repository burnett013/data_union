import pandas as pd
import os

def check_original_pre():
    # Attempt to locate the file mentioned by user
    path = "artifacts/original_pre_values.csv" 
    
    if not os.path.exists(path):
        print(f"File {path} not found. Searching artifacts...")
        for root, dirs, files in os.walk("artifacts"):
            if "original_pre_values.csv" in files:
                path = os.path.join(root, "original_pre_values.csv")
                print(f"Found at: {path}")
                break
    
    if os.path.exists(path):
        print(f"Reading {path}...")
        try:
            df = pd.read_csv(path, header=None)
            print(f"Shape: {df.shape}")
            
            # Check Column R (Index 17)
            if df.shape[1] > 17:
                col_r = df.iloc[:, 17]
                print("Column R (Index 17) Head (Raw):")
                print(col_r.head(10).tolist())
                
                # Check for ID-like values
                print("Sample of values starting row 3:")
                print(col_r.iloc[3:10].tolist())
            else:
                print("File has fewer than 18 columns!")
        except Exception as e:
            print(f"Error reading file: {e}")
    else:
        print("original_pre_values.csv NOT FOUND.")

if __name__ == "__main__":
    check_original_pre()
