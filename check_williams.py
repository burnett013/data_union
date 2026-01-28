import os
import pandas as pd

def inspect_and_check():
    print(f"CWD: {os.getcwd()}")
    
    if os.path.exists("artifacts"):
        print("Contents of 'artifacts':")
        try:
            items = os.listdir("artifacts")
            print(items)
            
            for item in items:
                sub = os.path.join("artifacts", item)
                if os.path.isdir(sub):
                    print(f"  Contents of '{item}':")
                    try:
                        print(f"  {os.listdir(sub)}")
                    except Exception as e:
                        print(f"  Error listing {item}: {e}")
        except Exception as e:
            print(f"Error listing artifacts: {e}")
            
    else:
        print("'artifacts' directory NOT FOUND in CWD.")
        return

    # Attempt to read Williams file if found
    target_path = os.path.join("artifacts", "williams_data", "pre_values.csv")
    if os.path.exists(target_path):
        print(f"\nScanning {target_path}...")
        try:
            df = pd.read_csv(target_path, header=None)
            targets = ['1046', '1019']
            for t in targets:
                matches = df.applymap(lambda x: str(x).strip() == t)
                found = matches.stack()
                found = found[found]
                if not found.empty:
                    print(f"FOUND '{t}':")
                    for idx in found.index:
                        print(f"  Row: {idx[0]}, Col: {idx[1]}")
                else:
                    print(f"'{t}' NOT FOUND.")
        except Exception as e:
            print(f"Error reading csv: {e}")
    else:
        print(f"\nTarget file {target_path} still NOT FOUND via os.path.exists().")

if __name__ == "__main__":
    inspect_and_check()
