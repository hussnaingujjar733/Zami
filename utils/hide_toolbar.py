import streamlit as st

def hide_streamlit_toolbar():
    """Hide the top black bar and 3 dots menu"""
    
    st.markdown("""
    <style>
        /* Hide main header/toolbar */
        header[data-testid="stHeader"] {
            display: none !important;
        }
        
        /* Hide deploy button */
        .stAppDeployButton {
            display: none !important;
        }
        
        /* Hide top-right menu */
        button[kind="header"] {
            display: none !important;
        }
        
        /* Hide the toolbar container */
        div[data-testid="stToolbar"] {
            display: none !important;
        }
        
        /* Hide the decoration element */
        div[data-testid="stDecoration"] {
            display: none !important;
        }
        
        /* Remove the top padding since header is hidden */
        .main .block-container {
            padding-top: 0.5rem !important;
        }
        
        /* Hide the "Manage app" button */
        .stAppDeployButton + div {
            display: none !important;
        }
        
        /* Hide the Streamlit branding */
        #MainMenu {
            visibility: hidden;
            display: none;
        }
        
        footer {
            visibility: hidden;
            display: none;
        }
        
        /* Hide the view fullscreen button */
        button[title="View fullscreen"] {
            display: none !important;
        }
    </style>
    
    <script>
        // Additional JavaScript to hide elements
        setTimeout(function() {
            const headers = document.querySelectorAll('header');
            headers.forEach(header => header.style.display = 'none');
            
            const toolbars = document.querySelectorAll('[data-testid="stToolbar"]');
            toolbars.forEach(toolbar => toolbar.style.display = 'none');
        }, 100);
    </script>
    """, unsafe_allow_html=True)

def hide_sidebar():
    """Hide the sidebar completely"""
    st.markdown("""
    <style>
        [data-testid="collapsedControl"] {
            display: none !important;
        }
        section[data-testid="stSidebar"] {
            display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

def clean_ui():
    """Apply all UI cleanups"""
    hide_streamlit_toolbar()
    hide_sidebar()
