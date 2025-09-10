"""
Koteria - HTML File Processing Application

Main entry point for the Koteria application with proper authentication flow.
"""

import streamlit as st
from app.config import get_app_config, get_credentials, get_user_app
from app.utils import initialize_session_state
from app.pages.welcome import welcome
from app.pages.file_converter import convert_file

def show_login_page():
    """Display the login page."""
    st.title("Koteria Login")
    st.markdown("Welcome to the HTML File Processing Application")
    st.markdown("---")
    
    with st.form("login_form"):
        st.subheader("Enter your credentials")
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        submit_button = st.form_submit_button("Login", use_container_width=True)
        
        if submit_button:
            credentials = get_credentials()
            if username in credentials and credentials[username] == password:
                st.session_state.authenticated = True
                st.session_state.current_user = username
                st.session_state.current_app = get_user_app(username)
                st.session_state.koteria_current_page = "Welcome"
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password. Please try again.")

def show_sidebar_navigation():
    """Display custom navigation in sidebar."""
    with st.sidebar:  
        st.markdown( 
            """ 
            <style> 
                .main-header { 
                    font-size:32px !important; 
                    font-weight:600; padding-bottom:10px; 
                    border-bottom: 1px solid #eee; 
                } 
            </style> 
            """, unsafe_allow_html=True 
        ) 
        st.markdown('<p class="main-header">Koteria App</p>', unsafe_allow_html=True)
        if 'current_user' in st.session_state:
            st.markdown(f"**User:** {st.session_state.current_user}")

        
        # Show navigation panel
        st.markdown("### Navigation")
        
        # Page selection
        pages = ["Welcome", "File Converter"]
        current_page = st.session_state.get('koteria_current_page', 'Welcome')
        
        try:
            page_index = pages.index(current_page)
        except ValueError:
            page_index = 0
        
        selected_page = st.radio(
            "Select Page:",
            pages,
            index=page_index,
            key="page_selector"
        )
        
        if selected_page != current_page:
            st.session_state.koteria_current_page = selected_page
            st.rerun()
        
        st.markdown("---")
        
        # Show current data info
        if st.session_state.get('current_dataframe') is not None:
            df = st.session_state.current_dataframe
            filename = st.session_state.get('current_filename', 'Unknown')
            
            st.markdown("### Current Data")
            st.write(f"**File:** {filename}")
            st.write(f"**Shape:** {df.shape[0]} × {df.shape[1]}")
            st.write(f"**Memory:** {df.memory_usage(deep=True).sum() / 1024:.1f} KB")
            
            if st.button("Clear Data", use_container_width=True):
                st.session_state.current_dataframe = None
                st.session_state.current_filename = None
                st.session_state.file_processed = False
                st.rerun()
        else:
            st.markdown("### Current Data")
            st.info("No data loaded")
        
        st.markdown("---")
        
        # Logout button
        if st.button("Logout", use_container_width=True):
            # Clear all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

def show_koteria_app():
    """Display the main Koteria application."""
    # Initialize app-specific session state
    initialize_session_state()
    
    # Show sidebar navigation
    show_sidebar_navigation()
    
    # Get current page
    current_page = st.session_state.get('koteria_current_page', 'Welcome')
    
    # Display the selected page
    if current_page == "Welcome":
        welcome()
    elif current_page == "File Converter":
        convert_file()
    else:
        st.error(f"Unknown page: {current_page}")

def main():
    """Main function to run the application."""
    # Configure page
    st.set_page_config(
        page_title="Koteria - HTML File Processor",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if st.session_state.authenticated:
        # User is authenticated, show the app
        show_koteria_app()
    else:
        # User is not authenticated, show login page
        show_login_page()

if __name__ == "__main__":
    main()
