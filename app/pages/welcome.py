"""
Welcome Page - Koteria App

Welcome page with application overview and navigation.
"""

import streamlit as st
import pandas as pd
from app.config import get_app_config

def welcome():
    """Display the welcome page with application overview."""
    config = get_app_config("koteria")
    
    st.markdown("### Welcome to Koteria")
    
    # Application overview
    st.markdown("---")
    st.markdown("### What you can do:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **File Processing**
        - Upload HTML files
        - Extract structured data
        - Process veterinary records
        - Export to CSV format
        """)
    
    with col2:
        st.markdown("""
        **Data Analysis**
        - View processed data
        - Analyze data quality
        - Download results
        - Multi-page navigation
        """)
    
    # Current data status
    st.markdown("---")
    st.markdown("### Current Session Status")
    
    if st.session_state.get('current_dataframe') is not None:
        df = st.session_state.current_dataframe
        filename = st.session_state.get('current_filename', 'Unknown')
        
        st.success(f"**Data Loaded**: {filename}")
        st.info(f"**Data Shape**: {df.shape[0]} rows × {df.shape[1]} columns")
        
        # Quick preview
        with st.expander("Quick Data Preview"):
            st.dataframe(df.head(), use_container_width=True)
            
        # Navigation suggestion
        st.markdown("**Next Step**: Go to **File Converter** to analyze your data or upload a new file.")
    else:
        st.info("**No Data Loaded**")
        st.markdown("**Get Started**: Go to **File Converter** to upload and process an HTML file.")
    
    # Features overview
    st.markdown("---")
    st.markdown("### Key Features")
    
    from st_aggrid import AgGrid, GridOptionsBuilder 
    data = pd.DataFrame({ "User": ["Alice", "Bob", "Charlie"], "Plan": ["Free", "Pro", "Enterprise"], "Status": ["Active", "Inactive", "Active"] }) 
    gb = GridOptionsBuilder.from_dataframe(data) 
    gb.configure_pagination(paginationAutoPageSize=True) 
    gb.configure_default_column(editable=True, groupable=True) 
    grid_options = gb.build() 
    AgGrid(data, gridOptions=grid_options, theme="streamlit")
    
    # Quick actions
    st.markdown("---")
    st.markdown("### Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Go to File Converter", use_container_width=True):
            st.session_state.koteria_current_page = "File Converter"
            st.rerun()
    
    with col2:
        if st.session_state.get('current_dataframe') is not None:
            if st.button("View Data", use_container_width=True):
                st.session_state.koteria_current_page = "File Converter"
                st.rerun()
        else:
            st.button("View Data", disabled=True, use_container_width=True)
    
    with col3:
        if st.button("Refresh Page", use_container_width=True):
            st.rerun()
