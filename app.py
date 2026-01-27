import streamlit as st
import pandas as pd
import io
from processing import process_survey_data

# --- Page Configuration ---
st.set_page_config(
    page_title="Qualtrics Data Merger",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Styling (Color Palette) ---
# Primary: #CB6015 (Orange), #002F6C (Navy)
# Secondary: #333F48 (Dark Grey), #B9D9EB (Light Blue)
# Others: #C1C5C8 (Grey), #B6ADA5 (Warm Gray)

st.markdown("""
<style>
    /* Main Background & Text */
    .stApp {
        background-color: #FFFFFF;
        color: #333F48;
    }
    
    /* Primary Button (Navy) */
    div.stButton > button {
        background-color: #002F6C;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #CB6015; /* Orange on hover */
        border: none;
        color: white;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #F0F2F6;
        border-right: 1px solid #C1C5C8;
    }
    
    /* Headers (Orange) */
    h1, h2, h3 {
        color: #CB6015;
        font-family: 'Gotham', 'Arial', sans-serif;
    }
    
    /* Uploaders */
    .stFileUploader label {
        color: #002F6C;
        font-weight: bold;
    }
    
    /* Success Message */
    .stSuccess {
        background-color: #B9D9EB;
        color: #002F6C;
    }
</style>
""", unsafe_allow_html=True)

# --- Main App ---

st.title("Qualtrics Data Merger 📊")
st.markdown("""
Refine and merge your Pre-Survey and Post-Survey Qualtrics datasets. 
This tool combines **Values** and **Labels** into a single readable format.
""")

st.write("---")

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("1. Upload Pre-Survey Data")
    pre_labels_file = st.file_uploader("Pre-Set Labels CSV", type=['csv'], key="pre_labels")
    pre_values_file = st.file_uploader("Pre-Set Values CSV", type=['csv'], key="pre_values")
    
    st.markdown("---")
    
    st.header("2. Upload Post-Survey Data")
    post_labels_file = st.file_uploader("Post-Set Labels CSV", type=['csv'], key="post_labels")
    post_values_file = st.file_uploader("Post-Set Values CSV", type=['csv'], key="post_values")

    st.markdown("---")
    process_btn = st.button("🚀 Process & Merge Data")

# --- Processing Logic ---
if process_btn:
    # 1. Validation
    if not (pre_labels_file and pre_values_file and post_labels_file and post_values_file):
        st.error("Please upload all four files (Pre-Set and Post-Set) to proceed.")
        st.stop()
        
    try:
        with st.spinner("Processing datasets..."):
            # 2. Process Pre-Set
            st.info("Merging Pre-Survey Data...")
            # Reset file pointers just in case
            pre_values_file.seek(0)
            pre_labels_file.seek(0)
            pre_merged_df = process_survey_data(pre_values_file, pre_labels_file)
            
            # 3. Process Post-Set
            st.info("Merging Post-Survey Data...")
            post_values_file.seek(0)
            post_labels_file.seek(0)
            post_merged_df = process_survey_data(post_values_file, post_labels_file)
            
            # 4. Generate Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                pre_merged_df.to_excel(writer, sheet_name='Pre-Survey', index=False)
                post_merged_df.to_excel(writer, sheet_name='Post-Survey', index=False)
            
            output_data = output.getvalue()
            
            # 5. Success & Download
            st.success("✅ Data processed successfully!")
            
            st.download_button(
                label="📥 Download Combined XLSX",
                data=output_data,
                file_name="Qualtrics_Merged_Data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            # Previews
            with st.expander("Preview: Pre-Survey Data (First 5 Rows)"):
                st.dataframe(pre_merged_df.head())
                
            with st.expander("Preview: Post-Survey Data (First 5 Rows)"):
                st.dataframe(post_merged_df.head())

    except Exception as e:
        st.error(f"An error occurred during processing: {str(e)}")
        st.error("Please check that your input files are raw Qualtrics CSV exports.")
