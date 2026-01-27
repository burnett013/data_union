import pandas as pd
import io

def process_survey_data(values_file, labels_file):
    """
    Merges Qualtrics values and labels datasets into a single DataFrame.
    
    Args:
        values_file: File-like object or path for the Values CSV.
        labels_file: File-like object or path for the Labels CSV.
        
    Returns:
        pd.DataFrame: The cleaned and merged DataFrame.
    """
    # 1. Ingest
    # We read without header initially to handle the 3-row header structure of Qualtrics
    df_values = pd.read_csv(values_file, header=None)
    df_labels = pd.read_csv(labels_file, header=None)
    
    # 2. Extract Header Info (Row 1 -> QID, Row 2 -> Question Text)
    # 0-based index: Row 0 is QID (e.g. Q1), Row 1 is Text
    # We only care about columns R (index 17) onwards for the merge
    
    # Verify we have enough columns
    if df_values.shape[1] < 18:
        raise ValueError("Dataset has fewer than 18 columns. Expected Qualtrics format starting data at column R.")

    # Slice the relevant parts (Metadata columns A-Q are index 0-16)
    # The user wants to KEEP leading zeros in data, so we treat as string later.
    # But for now, let's just focus on the structure.
    
    # Extract QIDs and Texts from the Labels file (usually safer, though Values should match)
    qids = df_labels.iloc[0, 17:]
    questions = df_labels.iloc[1, 17:]
    
    # 3. Build new Composite Header
    # Format: "Qx. Question Text"
    new_headers = []
    for qid, question in zip(qids, questions):
        # Clean up potential NaNs or non-strings if any
        q = str(qid).strip()
        t = str(question).strip()
        new_headers.append(f"{q}. {t}")
    
    # 4. Filter Data Rows
    # Rows 0, 1, 2 are headers/metadata. Data starts at row 3.
    data_values = df_values.iloc[3:, 17:].reset_index(drop=True)
    data_labels = df_labels.iloc[3:, 17:].reset_index(drop=True)
    
    # 5. Merge Value and Label Columns
    # We want: Col 1 Value, Col 1 Label, Col 2 Value, Col 2 Label...
    merged_data = pd.DataFrame()
    
    # Ensure they have same number of columns/rows
    # We'll use the headers count to iterate
    for i, header in enumerate(new_headers):
        # Column from Values
        # Note: We need to ensure we are preserving leading zeros. 
        # Pandas read_csv defaulting to infer types might loose them if we aren't careful.
        # However, since we read with header=None, everything is initially object/mixed.
        # Later we will apply whitespace stripping.
        
        col_val = data_values.iloc[:, i].astype(str).str.strip()
        col_lab = data_labels.iloc[:, i].astype(str).str.strip()
        
        # Replace 'nan' string with empty if it occurred due to conversion
        col_val = col_val.replace('nan', '')
        col_lab = col_lab.replace('nan', '')
        
        # Add to new DF
        # We can use the header for both, or differentiate. 
        # Typically "Value" and "Label" suffixes help, but user asked for:
        # "Record the number form values in one column, then record the label... in the adjacent column"
        # "You'll be left with two columns for each question"
        
        merged_data[f"{header} (Value)"] = col_val
        merged_data[f"{header} (Label)"] = col_lab

    return merged_data
