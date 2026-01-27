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
                pre_merged_df = process_survey_data(pre_values_file, pre_labels_file)
                
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
                post_merged_df = process_survey_data(post_values_file, post_labels_file)
                
                # Generate Output
                post_output = io.BytesIO()
                with pd.ExcelWriter(post_output, engine='openpyxl') as writer:
                    post_merged_df.to_excel(writer, sheet_name='Post-Survey', index=False)
                post_data = post_output.getvalue()
            
            # 5. Success & Downloads
            st.success("✅ Processing complete! Download your files below.")
            
            # Dynamic Columns for Download Buttons
            # If both exist, use 2 columns. If only one, just use st.write/download directly.
            
            if has_pre and has_post:
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📥 Download PRE-Survey Data",
                        data=pre_data,
                        file_name="Pre_Survey_Merged.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                with col2:
                    st.download_button(
                        label="📥 Download POST-Survey Data",
                        data=post_data,
                        file_name="Post_Survey_Merged.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
            elif has_pre:
                st.download_button(
                    label="📥 Download PRE-Survey Data",
                    data=pre_data,
                    file_name="Pre_Survey_Merged.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            elif has_post:
                st.download_button(
                    label="📥 Download POST-Survey Data",
                    data=post_data,
                    file_name="Post_Survey_Merged.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
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

    except Exception as e:
        st.error(f"An error occurred during processing: {str(e)}")
        # Attempt reset
        if pre_labels_file: pre_labels_file.seek(0)
        if pre_values_file: pre_values_file.seek(0)
        if post_labels_file: post_labels_file.seek(0)
        if post_values_file: post_values_file.seek(0)
