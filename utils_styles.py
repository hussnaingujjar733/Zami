import streamlit as st

def inject_premium_styles():
    st.markdown("""
    <style>
    /* 1. Import Premium Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Apply Font Everywhere */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* 2. Main Background & Text Colors */
    .stApp {
        background-color: #0B1120; /* Deep premium blue-black */
        color: #F8FAFC;
    }

    /* Hide standard header, footer and main menu */
    header { visibility: hidden !important; }
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* 3. Streamlit Default Inputs Styling (Text Input, Selectbox) */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(30, 41, 59, 0.5) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 12px 16px !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput input:focus, .stSelectbox div[data-baseweb="select"]:focus-within {
        border-color: #38BDF8 !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2) !important;
        background-color: rgba(30, 41, 59, 0.8) !important;
    }

    /* 4. Super Premium Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0284C7, #2563EB) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 14px 0 rgba(37, 99, 235, 0.39) !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5) !important;
        background: linear-gradient(135deg, #0369A1, #1D4ED8) !important;
    }

    /* 5. Radio Buttons Modernization */
    div[role="radiogroup"] > label {
        background: rgba(30, 41, 59, 0.4);
        padding: 15px 20px;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.05);
        margin-bottom: 8px;
        transition: all 0.2s;
        cursor: pointer;
    }
    div[role="radiogroup"] > label:hover {
        background: rgba(30, 41, 59, 0.8);
        border-color: #38BDF8;
    }

    /* 6. Custom Glass Card & Headers */
    .premium-card {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        margin-bottom: 25px;
    }
    
    .step-header {
        color: #38bdf8;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 20px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)