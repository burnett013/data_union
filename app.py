import streamlit as st
import pandas as pd
import io
from processing import process_survey_data, generate_docx_dictionary

# --- Page Configuration ---
st.set_page_config(
    page_title="Qualtrics Data Merger",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Styling (Default Streamlit + Orange Accents) ---
# Keeping headers Orange (#CB6015) as requested.
# Reverting main button/background styles to Streamlit defaults.

st.markdown("""
<style>
    /* Headers (Orange) */
    h1, h2, h3 {
        color: #CB6015 !important;
        font-family: 'Gotham', 'Arial', sans-serif;
    }
    
    /* Sidebar Headers */
    .css-10trblm {
        color: #CB6015;
    }
    
    /* Custom divider */
    hr {
        margin-top: 1rem;
        margin-bottom: 1rem;
        border: 0;
        border-top: 1px solid #CB6015;
    }
</style>
""", unsafe_allow_html=True)

# --- Main App ---

st.title("Qualtrics Data Merger 📊")
st.markdown("""
Refine and merge your Pre-Survey and Post-Survey Qualtrics datasets. 
This tool combines **Values** and **Labels** into clean Excel files.
""")

st.write("---")

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("1. Pre-Survey Data")
    st.warning("Ensure you upload the correct file types below.")
    st.subheader("🅰️ Pre-Survey LABELS")
    pre_labels_file = st.file_uploader("Upload 'Choice Text' CSV", type=['csv'], key="pre_labels")
    
    st.subheader("🔢 Pre-Survey VALUES")
    pre_values_file = st.file_uploader("Upload 'Numeric Values' CSV", type=['csv'], key="pre_values")
    
    st.markdown("---")
    
    st.header("2. Post-Survey Data")
    st.subheader("🅰️ Post-Survey LABELS")
    post_labels_file = st.file_uploader("Upload 'Choice Text' CSV", type=['csv'], key="post_labels")
    
    st.subheader("🔢 Post-Survey VALUES")
    post_values_file = st.file_uploader("Upload 'Numeric Values' CSV", type=['csv'], key="post_values")

    st.markdown("---")
    process_btn = st.button("🚀 Process & Merge Data", type="primary")

# --- Processing Logic ---
if process_btn:
    # 1. Validation Logic
    has_pre = pre_labels_file is not None and pre_values_file is not None
    has_post = post_labels_file is not None and post_values_file is not None
    
    if not (has_pre or has_post):
        st.error("Please upload at least one complete set of data (Labels AND Values) for either Pre-Survey or Post-Survey.")
        st.stop()
        
    try:
        with st.spinner("Processing datasets..."):
            
            # --- PRE-SURVEY PROCESSING ---
            pre_data = None
            pre_merged_df = None
            if has_pre:
                # Reset file pointers just in case
                pre_values_file.seek(0)
                pre_labels_file.seek(0)
                # Pass 'pre' to trigger Q22 -> RecordID (pre) renaming
                pre_merged_df = process_survey_data(pre_values_file, pre_labels_file, dataset_name='pre')
                
                # Generate Output
                pre_output = io.BytesIO()
                with pd.ExcelWriter(pre_output, engine='openpyxl') as writer:
                    pre_merged_df.to_excel(writer, sheet_name='Pre-Survey', index=False)
                pre_data = pre_output.getvalue()

            # --- POST-SURVEY PROCESSING ---
            post_data = None
            post_merged_df = None
            if has_post:
                post_values_file.seek(0)
                post_labels_file.seek(0)
                # Pass 'post' to trigger Q22 -> RecordID (post) renaming
                post_merged_df = process_survey_data(post_values_file, post_labels_file, dataset_name='post')
                
                # Generate Output
                post_output = io.BytesIO()
                with pd.ExcelWriter(post_output, engine='openpyxl') as writer:
                    post_merged_df.to_excel(writer, sheet_name='Post-Survey', index=False)
                post_data = post_output.getvalue()
            
            # 5. Success & Downloads
            st.success("✅ Processing complete! Download your files below.")
            
            # --- Dynamic Download Columns ---
            # We want to offer: Pre Data, Post Data, Pre Dict (DOCX), Post Dict (DOCX)
            # User asked for "a third download button adjacent"
            # It might be cleaner to group Pre downloads together and Post downloads together, 
            # OR have Data Layout and Dict Layout.
            # "I want a third download button adjacent to the pre and post download buttons."
            # Maybe 3 columns: Pre Data | Post Data | Dictionary (if applicable)
            # Actually, dictionary is per dataset. So if we have Pre, we have Pre Dict. 
            # The prompt implies one general desire, but logically we need two dictionaries if we have two datasets, 
            # or maybe the user implies one combined? Usually they are separate.
            # Let's create dictionary for EACH available dataset.
            
            download_cols = st.columns(3)
            
            # Col 1: Pre Survey Downloads
            if has_pre:
                with download_cols[0]:
                    st.write("**Pre-Survey**")
                    st.download_button(
                        label="📥 Excel Data",
                        data=pre_data,
                        file_name="Pre_Survey_Merged.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                        key="dl_pre_data"
                    )
                    # Generate Pre Dict
                    pre_dict_io = generate_docx_dictionary(pre_merged_df)
                    st.download_button(
                        label="📘 Data Dictionary (DOCX)",
                        data=pre_dict_io,
                        file_name="Pre_Survey_Dictionary.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True,
                        key="dl_pre_dict"
                    )

            # Col 2: Post Survey Downloads
            if has_post:
                with download_cols[1]:
                    st.write("**Post-Survey**")
                    st.download_button(
                        label="📥 Excel Data",
                        data=post_data,
                        file_name="Post_Survey_Merged.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                        key="dl_post_data"
                    )
                    # Generate Post Dict
                    post_dict_io = generate_docx_dictionary(post_merged_df)
                    st.download_button(
                        label="📘 Data Dictionary (DOCX)",
                        data=post_dict_io,
                        file_name="Post_Survey_Dictionary.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True,
                        key="dl_post_dict"
                    )
            
            st.divider()
            
            # Previews
            st.subheader("Data Previews")
            
            if has_pre:
                with st.expander("Preview: Pre-Survey Data (First 5 Rows)", expanded=True):
                    st.dataframe(pre_merged_df.head(), use_container_width=True)
            
            if has_post:
                with st.expander("Preview: Post-Survey Data (First 5 Rows)", expanded=True):
                    st.dataframe(post_merged_df.head(), use_container_width=True)
            
            # --- KPIs / Statistics ---
            st.write("---")
            st.subheader("Dataset Statistics")
            
            # Calculate Counts & Duplicates
            # Helper to find ID column for duplicates
            def get_duplicates(df):
                if df is None: return 0, []
                # Look for column starting with RecordID and ending with (Value)
                target_col = "RecordID (Value)"
                if target_col in df.columns:
                    dupes = df[df.duplicated(subset=[target_col], keep=False)]
                    if not dupes.empty:
                        # Return count and list of unique duplicate IDs
                        return len(dupes), dupes[target_col].unique().tolist()
                return 0, []

            num_pre = len(pre_merged_df) if has_pre and pre_merged_df is not None else 0
            num_post = len(post_merged_df) if has_post and post_merged_df is not None else 0
            total_rows = num_pre + num_post
            
            dupe_count_pre, dupes_pre_list = get_duplicates(pre_merged_df)
            dupe_count_post, dupes_post_list = get_duplicates(post_merged_df)
            
            # Row 1: Counts
            kpi1, kpi2, kpi3 = st.columns(3)
            with kpi1:
                st.metric(label="Total Combined Rows", value=total_rows)
            with kpi2:
                st.metric(label="Pre-Survey Rows", value=num_pre)
            with kpi3:
                st.metric(label="Post-Survey Rows", value=num_post)
                
            # Row 2: Duplicates
            st.caption("Duplicate Detection based on 'RecordID' column:")
            d1, d2, d3 = st.columns(3)
            with d2:
                st.metric(label="Pre-Survey Duplicates", value=dupe_count_pre, delta_color="inverse")
                if dupe_count_pre > 0:
                     with st.expander("View Pre-Survey Duplicates"):
                          st.write(dupes_pre_list)
            with d3:
                st.metric(label="Post-Survey Duplicates", value=dupe_count_post, delta_color="inverse")
                if dupe_count_post > 0:
                     with st.expander("View Post-Survey Duplicates"):
                          st.write(dupes_post_list)

    except Exception as e:
        st.error(f"An error occurred during processing: {str(e)}")
        # Attempt reset
        if pre_labels_file: pre_labels_file.seek(0)
        if pre_values_file: pre_values_file.seek(0)
        if post_labels_file: post_labels_file.seek(0)
        if post_values_file: post_values_file.seek(0)

# --- SPSS Preparation Section ---
st.write("---")
st.header("Step 2: Prepare for SPSS (CSV Export)")

st.markdown("""
Upload your **merged Excel files** (generated above) to convert them into SPSS-ready CSVs.
*   Removes duplicate ID columns.
*   Renames columns with `pre_` or `post_` prefixes.
""")

col_spss_pre, col_spss_post = st.columns(2)

with col_spss_pre:
    st.subheader("Process Pre-Survey")
    spss_pre_file = st.file_uploader("Upload Merged Pre-Survey (XLSX)", type=['xlsx'], key="spss_pre")

with col_spss_post:
    st.subheader("Process Post-Survey")
    spss_post_file = st.file_uploader("Upload Merged Post-Survey (XLSX)", type=['xlsx'], key="spss_post")

import re

def clean_for_spss(df, prefix):
    """
    Cleans DataFrame for SPSS:
    1. Removes 'RecordID (Value)' column.
    2. Renames 'RecordID (Label)' -> 'RecordID'.
    3. For all other questions:
       - DROPS the Text Label column (e.g. "Q1 (Label)")
       - KEEPS the Numeric Value column (e.g. "Q1 (Value)")
       - Renames the Value column to "{prefix}_{Qnumber}" (e.g. pre_Q1)
    """
    # 1 & 2. Handle RecordID
    # Drop Value version
    if "RecordID (Value)" in df.columns:
        df = df.drop(columns=["RecordID (Value)"])
    if "RecordID" in df.columns: # Sometimes merged file might have it as just RecordID if saved that way?
         pass # Actually clean_for_spss is typically run on the merged output which has (Value) and (Label)
    
    # Rename Label version
    if "RecordID (Label)" in df.columns:
        df = df.rename(columns={"RecordID (Label)": "RecordID"})
        
    # 3. Rename others
    new_cols = {}
    cols_to_drop = []
    
    for col in df.columns:
        if col == "RecordID":
            continue
            
        # Regex to find Q numbers (e.g. "Q1. Question Text (Value)")
        match = re.match(r"^(Q\d+)", col)
        if match:
            q_part = match.group(1) # e.g. Q1
            
            if "(Label)" in col:
                # DROP text labels for SPSS
                cols_to_drop.append(col)
            
            elif "(Value)" in col:
                # KEEP numerical values and rename
                # e.g. pre_Q1
                new_name = f"{prefix}_{q_part}"
                new_cols[col] = new_name
            
    # Apply changes
    df = df.drop(columns=cols_to_drop)
    df = df.rename(columns=new_cols)
    
    return df

if spss_pre_file:
    try:
        df_pre = pd.read_excel(spss_pre_file)
        df_pre_clean = clean_for_spss(df_pre, "pre")
        
        csv_pre = df_pre_clean.to_csv(index=False).encode('utf-8')
        
        col_spss_pre.download_button(
            label="📥 Download SPSS-Ready CSV (Pre)",
            data=csv_pre,
            file_name="Pre_Survey_SPSS.csv",
            mime="text/csv"
        )
        col_spss_pre.success("Ready for download!")
    except Exception as e:
        col_spss_pre.error(f"Error: {e}")

if spss_post_file:
    try:
        df_post = pd.read_excel(spss_post_file)
        df_post_clean = clean_for_spss(df_post, "post")
        
        csv_post = df_post_clean.to_csv(index=False).encode('utf-8')
        
        col_spss_post.download_button(
            label="📥 Download SPSS-Ready CSV (Post)",
            data=csv_post,
            file_name="Post_Survey_SPSS.csv",
            mime="text/csv"
        )
        col_spss_post.success("Ready for download!")
    except Exception as e:
        col_spss_post.error(f"Error: {e}")

# --- Footer ---
st.write("---")
st.markdown(
    """
    <div style='text-align: center; color: grey; font-size: small;'>
        Version 1.1 | Updated: 2026-01-28 09:10 CST
    </div>
    """,
    unsafe_allow_html=True
)
