"""
Welcome Page - Koteria App

Welcome page with application overview and navigation.
"""

import streamlit as st
from app.utils.airtable import AirtableManager
from app.config import get_app_config

def welcome():
    """Display the welcome page with application overview."""
    
    # CSS to move title to top - maximum positioning
    st.markdown("""
    <style>
    /* Move main content title to top - aggressive positioning */
    .main .block-container {
        padding-top: 0rem !important;
        margin-top: 0rem !important;
    }
    
    /* Target the first element (title) in main content */
    .main .block-container > div:first-child {
        margin-top: -4rem !important;
        padding-top: 0 !important;
    }
    
    /* Alternative selectors for main content */
    .css-1d391kg {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Force title to top - maximum negative margin */
    h1 {
        margin-top: -4rem !important;
        padding-top: 0 !important;
    }
    
    /* Target main content area - maximum positioning */
    .main .block-container h1 {
        margin-top: -4rem !important;
        position: relative !important;
        top: -4rem !important;
    }
    
    /* Additional aggressive selectors */
    .main h1 {
        margin-top: -4rem !important;
        position: relative !important;
        top: -4rem !important;
    }
    
    /* Target any h1 in main content */
    .main .block-container > div:first-child h1 {
        margin-top: -4rem !important;
        padding-top: 0 !important;
        position: relative !important;
        top: -4rem !important;
    }
    
    /* Force main content to start at very top */
    .main {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Target the main content area directly */
    .main .block-container > div:first-child {
        margin-top: -4rem !important;
        padding-top: 0 !important;
        position: relative !important;
        top: -4rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    config = get_app_config("koteria")
    col1, col2 = st.columns(2)
    with col1:
        st.title("Dashboard")
        # Add horizontal line below title - full width
        st.markdown("""
        <div style="
            height: 1px;
            background-color: #e0e0e0;
            margin-top: 10px;
            margin-bottom: 20px;
            margin-left: -2rem;
            margin-right: -2rem;
            width: calc(100vw - 2rem);
            position: relative;
            left: 2rem;
        "></div>
        """, unsafe_allow_html=True)
    # with col2:
    #     if st.button("Refresh Page", use_container_width=True):
    #         st.rerun()
    
    st.markdown("")
    st.markdown("Overview")
    
    # Initialize Airtable manager
    airtable_manager = AirtableManager()
    
    if airtable_manager.is_configured():
        # Fetch and display wizyty table data
        with st.spinner("Loading data from Airtable..."):
            df = airtable_manager.get_table_data("visits")
        
        if not df.empty:
            # Calculate counts for the cards
            total_records = len(df)
            badania_count = len(df[df['typ'] == 'Badanie'])
            wizyty_count = len(df[df['typ'] == 'Wizyta'])
            
            # Display cards with actual counts
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div style="
                    background-color: white;
                    border: 1px solid #e0e0e0;
                    border-radius: 12px;
                    padding: 20px;
                    text-align: center;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    <div style="font-size: 28px; font-weight: bold; color: #000000;">{total_records}</div>
                    <div style="font-size: 14px; font-weight: normal; color: #7f8c8d; margin-bottom: 4px;">Przyjęcia</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="
                    background-color: white;
                    border: 1px solid #e0e0e0;
                    border-radius: 12px;
                    padding: 20px;
                    text-align: center;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    <div style="font-size: 28px; font-weight: bold; color: #000000;">{wizyty_count}</div>
                    <div style="font-size: 14px; font-weight: normal; color: #7f8c8d; margin-bottom: 4px;">Wizyty</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div style="
                    background-color: white;
                    border: 1px solid #e0e0e0;
                    border-radius: 12px;
                    padding: 20px;
                    text-align: center;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    <div style="font-size: 28px; font-weight: bold; color: #000000;">{badania_count}</div>
                    <div style="font-size: 14px; font-weight: normal; color: #7f8c8d; margin-bottom: 4px;">Badania</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Airtable Data Section
            st.markdown("")
            st.markdown("Wizyty")
            
            # Display dataframe without index column and with padding
            st.dataframe(df, use_container_width=True, height=400, hide_index=True)
        else:
            st.info("No data found in the 'visits' table.")
    else:
        st.error("Airtable is not properly configured. Please check your secrets.toml file.")
