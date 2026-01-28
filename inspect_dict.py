import pandas as pd
import os

filepath = "/Users/andyburnett/Library/Mobile Documents/com~apple~CloudDocs/Desktop/X03.27.25/UT_Tyler/qualtrics_union/bowen_j_project/qualtrics_union/artifacts/bowen_dict.xlsx"

try:
    df = pd.read_excel(filepath, sheet_name='labels_range')
    print("Columns:", df.columns.tolist())
    print("\nFirst 5 Rows:")
    print(df.head().to_string())
except Exception as e:
    print(f"Error: {e}")
