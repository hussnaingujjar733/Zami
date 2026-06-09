import streamlit as st

def inject_premium_styles():
    st.markdown("""
    <style>
    /* ==========================================================
       ZAMI - PREMIUM DESIGN SYSTEM
       ========================================================== */
    
    /* 1. Global Font Setup */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* 2. Page & Background Layout */
    .stApp {
        background-color: #0B1120 !important;
        color: #F8FAFC !important;
    }

    /* 3. SIDEBAR REMOVAL & LAYOUT FIX */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stSidebarCollapseControl"] { display: none !important; }
    
    /* Center container and maximize space */
    [data-testid="stMainBlockContainer"] {
        max-width: 1200px !important;
        padding-top: 2rem !important;
    }

    /* 4. Hide Streamlit Defaults */
    header { visibility: hidden !important; }
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* 5. Modern Inputs & Selects */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(30, 41, 59, 0.5) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 12px 16px !important;
        transition: all 0.3s ease !important;
    }

    /* 6. Premium Button System */
    .stButton > button {
        background: linear-gradient(135deg, #0284C7, #2563EB) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 14px 0 rgba(37, 99, 235, 0.39) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5) !important;
        background: linear-gradient(135deg, #0369A1, #1D4ED8) !important;
    }

    /* 7. Glassmorphism Card System */
    .premium-card {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        margin-bottom: 25px;
    }

    /* 8. Modern Radio Group */
    div[role="radiogroup"] > label {
        background: rgba(30, 41, 59, 0.4) !important;
        padding: 15px 20px !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
        margin-bottom: 8px !important;
        transition: all 0.2s !important;
    }
    
    div[role="radiogroup"] > label:hover {
        background: rgba(30, 41, 59, 0.8) !important;
        border-color: #38BDF8 !important;
    }

    /* 9. Success & Error Alert Modernization */
    .stAlert {
        background-color: rgba(30, 58, 138, 0.2) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)