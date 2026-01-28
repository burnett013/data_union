import os
import pandas as pd

def locate_and_search():
    print(f"Propagating from: {os.getcwd()}")
    target_file = "pre_values.csv"
    found_path = None
    
    # 1. Walk to find the file
    for root, dirs, files in os.walk("."):
        if target_file in files:
            found_path = os.path.abspath(os.path.join(root, target_file))
            print(f"FOUND FILE AT: {found_path}")
            break
            
    if not found_path:
        print(f"Could not find {target_file} in current or sub directories.")
        # Try listing artifacts explicitly
        if os.path.exists("artifacts"):
            print("Listing 'artifacts' dir:")
            print(os.listdir("artifacts"))
        return

    # 2. Search for Duplicates in Found File (Pre)
    print(f"\nScanning found file for ['1046', '1019']...")
    try:
        df = pd.read_csv(found_path, header=None)
        targets = ['1046', '1019']
        
        for t in targets:
            matches = df.applymap(lambda x: str(x).strip() == t)
            found = matches.stack()
            found = found[found]
            if not found.empty:
                print(f"  FOUND '{t}' at:")
                for idx in found.index:
                    print(f"    Row: {idx[0]}, Col: {idx[1]}")
            else:
                print(f"  '{t}' NOT FOUND.")
                
        # 3. Search POST if possible (assume sibling)
        parent = os.path.dirname(found_path)
        post_path = os.path.join(parent, "post_values.csv")
        if os.path.exists(post_path):
             print(f"\nScanning Post file at {post_path} for ['1023', '1011']...")
             df_post = pd.read_csv(post_path, header=None)
             targets_post = ['1023', '1011']
             for t in targets_post:
                matches = df_post.applymap(lambda x: str(x).strip() == t)
                found = matches.stack()
                found = found[found]
                if not found.empty:
                    print(f"  FOUND '{t}' at:")
                    for idx in found.index:
                         print(f"    Row: {idx[0]}, Col: {idx[1]}")
                else:
                    print(f"  '{t}' NOT FOUND.")

    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    locate_and_search()
