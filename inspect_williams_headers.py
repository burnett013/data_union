import pandas as pd

def list_headers():
    print("--- Williams Data Headers ---")
    df = pd.read_csv("artifacts/williams_data/pre_labels.csv", header=None, nrows=2)
    
    qids = df.iloc[0, 17:].values
    texts = df.iloc[1, 17:].values
    
    print("Index | QID | Text")
    print("-" * 50)
    for i, (q, t) in enumerate(zip(qids, texts)):
        print(f"{i} | {q} | {t}")

if __name__ == "__main__":
    list_headers()
