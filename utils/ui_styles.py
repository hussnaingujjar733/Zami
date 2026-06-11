import streamlit as st

def inject_premium_styles():
    """Simple working styles"""
    st.markdown("""
    <style>
    /* Header styling */
    .stApp {
        background-color: #0f172a;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #2E7D32;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background-color: #1B5E20;
        transform: scale(1.02);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #34d399;
        background-color: #1e293b;
        color: white;
    }
    
    /* Metric styling */
    .stMetric {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #34d399;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: #1e293b;
        border-radius: 12px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2E7D32;
        color: white;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 2rem;
        border-top: 1px solid #334155;
        color: #64748b;
        font-size: 0.8rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Add simple header
    st.markdown("""
    <div style="text-align: center; padding: 1rem; margin-bottom: 1rem;">
        <h1 style="color: #34d399;">🏠 ZAMI</h1>
        <p style="color: #94a3b8;">Rénovation Énergétique par IA</p>
    </div>
    """, unsafe_allow_html=True)

def show_toast(message, type="success"):
    """Simple toast notification"""
    st.success(message)
