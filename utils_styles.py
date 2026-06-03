"""
utils_styles.py — ZAMI Premium UI Styling
Professional glassmorphism design with animations and responsive layout
"""

import streamlit as st

def inject_premium_styles():
    """Injects professional CSS styling for ZAMI platform"""
    
    st.markdown("""
    <style>
    /* ─────────────────────────────────────────────
       IMPORT FONTS
    ───────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700;14..32,800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    /* ─────────────────────────────────────────────
       GLOBAL RESET
    ───────────────────────────────────────────── */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, .stApp {
        background: #020306 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display: none;}
    [data-testid="stToolbar"] {display: none;}
    [data-testid="stDecoration"] {display: none;}
    [data-testid="stStatusWidget"] {display: none;}
    
    /* Subtle grid pattern background */
    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image: 
            linear-gradient(rgba(34, 197, 94, 0.008) 1px, transparent 1px),
            linear-gradient(90deg, rgba(34, 197, 94, 0.008) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
        z-index: 0;
    }
    
    /* ─────────────────────────────────────────────
       PREMIUM CARDS (Glassmorphism)
    ───────────────────────────────────────────── */
    .card {
        background: linear-gradient(135deg, rgba(13, 18, 33, 0.95) 0%, rgba(7, 10, 19, 0.98) 100%);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 28px;
        padding: 2rem 2rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(34, 197, 94, 0.3), transparent);
    }
    
    .card:hover {
        border-color: rgba(34, 197, 94, 0.2);
        transform: translateY(-2px);
        box-shadow: 0 25px 40px -12px rgba(0, 0, 0, 0.6);
    }
    
    /* Scenario card active state with animated border */
    .scenario-card-active {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.12) 0%, rgba(8, 12, 24, 0.98) 100%);
        border: 1px solid rgba(34, 197, 94, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .scenario-card-active::after {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #22c55e, #16a34a, #22c55e);
        border-radius: 26px;
        z-index: -1;
        animation: borderPulse 2s ease infinite;
    }
    
    @keyframes borderPulse {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 0.8; }
    }
    
    /* ─────────────────────────────────────────────
       TYPOGRAPHY
    ───────────────────────────────────────────── */
    h1, h2, h3, h4, .section-title {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.03em !important;
    }
    
    .section-label {
        font-size: 0.7rem;
        font-weight: 800;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #22c55e;
        margin-bottom: 0.5rem;
        display: inline-block;
    }
    
    .section-title {
        font-size: 1.8rem;
        color: #ffffff;
        margin-bottom: 1rem;
    }
    
    .owner-exclusive-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 1rem;
        line-height: 1.2;
        background: linear-gradient(135deg, #ffffff 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* ─────────────────────────────────────────────
       DPE BADGE
    ───────────────────────────────────────────── */
    .dpe-badge-big {
        display: inline-block;
        padding: 20px 50px;
        font-size: 4rem;
        font-weight: 900;
        border-radius: 28px;
        color: white;
        text-align: center;
        box-shadow: 0 20px 35px -10px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    
    .dpe-badge-big:hover {
        transform: scale(1.02);
        box-shadow: 0 25px 40px -12px rgba(0, 0, 0, 0.5);
    }
    
    /* ─────────────────────────────────────────────
       METRICS & STATS
    ───────────────────────────────────────────── */
    .metric-value-huge {
        font-size: 2.8rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.03em;
        line-height: 1;
    }
    
    .metric-label-sub {
        font-size: 0.7rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
        margin-top: 0.3rem;
        display: inline-block;
    }
    
    /* ─────────────────────────────────────────────
       BUTTONS
    ───────────────────────────────────────────── */
    .stButton button {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 12px 24px !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
        width: 100%;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 20px -5px rgba(34, 197, 94, 0.3) !important;
    }
    
    .stButton button:active {
        transform: translateY(0px) !important;
    }
    
    /* Secondary button */
    .stButton button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .stButton button[kind="secondary"]:hover {
        background: rgba(34, 197, 94, 0.1) !important;
        border-color: rgba(34, 197, 94, 0.3) !important;
        box-shadow: none !important;
        transform: translateY(-1px) !important;
    }
    
    /* ─────────────────────────────────────────────
       FORM INPUTS
    ───────────────────────────────────────────── */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stTextArea > div > textarea {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 14px !important;
        padding: 12px 16px !important;
        color: #ffffff !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div:focus-within,
    .stTextArea > div > textarea:focus {
        border-color: #22c55e !important;
        box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.15) !important;
        outline: none !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #475569 !important;
    }
    
    /* Radio buttons */
    .stRadio > div {
        gap: 20px;
        flex-wrap: wrap;
    }
    
    .stRadio label {
        background: rgba(15, 23, 42, 0.6);
        padding: 8px 20px;
        border-radius: 40px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .stRadio label:hover {
        background: rgba(34, 197, 94, 0.1);
        border-color: rgba(34, 197, 94, 0.3);
    }
    
    .stRadio label[data-baseweb="radio"] {
        background: transparent;
    }
    
    /* ─────────────────────────────────────────────
       SLIDER / PROGRESS BAR
    ───────────────────────────────────────────── */
    .stSlider div[data-baseweb="slider"] {
        margin-top: 10px;
    }
    
    .stSlider div[role="slider"] {
        background: #22c55e !important;
    }
    
    .stSlider div[data-testid="stThumbValue"] {
        color: #22c55e !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #22c55e, #16a34a) !important;
        border-radius: 10px;
    }
    
    /* ─────────────────────────────────────────────
       DATA FRAME / TABLES
    ───────────────────────────────────────────── */
    .stDataFrame {
        background: rgba(15, 23, 42, 0.4);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .stDataFrame table {
        color: #f8fafc;
    }
    
    /* ─────────────────────────────────────────────
       EXPANDER
    ───────────────────────────────────────────── */
    .streamlit-expanderHeader {
        background: rgba(15, 23, 42, 0.6);
        border-radius: 12px;
        font-weight: 600;
        color: #f8fafc;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(34, 197, 94, 0.1);
    }
    
    /* ─────────────────────────────────────────────
       ALERTS / TOASTS
    ───────────────────────────────────────────── */
    .stAlert {
        border-radius: 14px;
        border-left: 4px solid;
        animation: slideIn 0.3s ease-out;
    }
    
    .stAlert[data-testid="stAlertSuccess"] {
        background: rgba(34, 197, 94, 0.1);
        border-left-color: #22c55e;
    }
    
    .stAlert[data-testid="stAlertError"] {
        background: rgba(239, 68, 68, 0.1);
        border-left-color: #ef4444;
    }
    
    .stAlert[data-testid="stAlertWarning"] {
        background: rgba(245, 158, 11, 0.1);
        border-left-color: #f59e0b;
    }
    
    .stAlert[data-testid="stAlertInfo"] {
        background: rgba(59, 130, 246, 0.1);
        border-left-color: #3b82f6;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* ─────────────────────────────────────────────
       TABS
    ───────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 23, 42, 0.4);
        border-radius: 16px;
        padding: 6px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 8px 24px;
        font-weight: 600;
        transition: all 0.2s;
        color: #94a3b8;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #22c55e, #16a34a);
        color: white;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #22c55e;
    }
    
    /* ─────────────────────────────────────────────
       SELECT BOX DROPDOWN
    ───────────────────────────────────────────── */
    div[data-baseweb="select"] > div {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
    }
    
    div[data-baseweb="select"] ul {
        background: #0f172a;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
    }
    
    div[data-baseweb="select"] li {
        color: #f8fafc;
    }
    
    div[data-baseweb="select"] li:hover {
        background: rgba(34, 197, 94, 0.1);
    }
    
    /* ─────────────────────────────────────────────
       CHECKBOX
    ───────────────────────────────────────────── */
    .stCheckbox label {
        color: #94a3b8;
    }
    
    .stCheckbox label:hover {
        color: #22c55e;
    }
    
    /* ─────────────────────────────────────────────
       SCROLLBAR
    ───────────────────────────────────────────── */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(34, 197, 94, 0.3);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(34, 197, 94, 0.5);
    }
    
    /* ─────────────────────────────────────────────
       FOOTER
    ───────────────────────────────────────────── */
    .footer {
        text-align: center;
        color: #334155;
        padding: 3rem 0 2rem 0;
        font-size: 0.7rem;
        font-weight: 600;
        border-top: 1px solid rgba(255, 255, 255, 0.03);
        margin-top: 4rem;
    }
    
    /* ─────────────────────────────────────────────
       FLOATING ACTION BUTTON
    ───────────────────────────────────────────── */
    .fab {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: linear-gradient(135deg, #22c55e, #16a34a);
        width: 50px;
        height: 50px;
        border-radius: 25px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 24px;
        cursor: pointer;
        box-shadow: 0 10px 25px rgba(34, 197, 94, 0.3);
        transition: all 0.3s ease;
        z-index: 1000;
        border: none;
    }
    
    .fab:hover {
        transform: scale(1.1);
        box-shadow: 0 15px 35px rgba(34, 197, 94, 0.4);
    }
    
    /* ─────────────────────────────────────────────
       CUSTOM LOADING SPINNER
    ───────────────────────────────────────────── */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .custom-spinner {
        width: 40px;
        height: 40px;
        border: 3px solid rgba(34, 197, 94, 0.2);
        border-top: 3px solid #22c55e;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    /* ─────────────────────────────────────────────
       RESPONSIVE DESIGN
    ───────────────────────────────────────────── */
    @media (max-width: 768px) {
        .card {
            padding: 1.2rem;
            border-radius: 20px;
        }
        
        .owner-exclusive-title {
            font-size: 1.5rem;
        }
        
        .section-title {
            font-size: 1.2rem;
        }
        
        .dpe-badge-big {
            font-size: 2.5rem;
            padding: 12px 30px;
        }
        
        .metric-value-huge {
            font-size: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 6px 12px;
            font-size: 0.8rem;
        }
        
        .fab {
            width: 45px;
            height: 45px;
            font-size: 20px;
            bottom: 20px;
            right: 20px;
        }
        
        .stRadio > div {
            gap: 10px;
        }
        
        .stRadio label {
            padding: 6px 12px;
            font-size: 0.8rem;
        }
    }
    
    /* ─────────────────────────────────────────────
       LOADING SHIMMER ANIMATION
    ───────────────────────────────────────────── */
    @keyframes shimmer {
        0% {
            background-position: -1000px 0;
        }
        100% {
            background-position: 1000px 0;
        }
    }
    
    .shimmer {
        background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.05) 50%, rgba(255,255,255,0) 100%);
        background-size: 1000px 100%;
        animation: shimmer 1.5s infinite;
    }
    
    /* ─────────────────────────────────────────────
       TOOLTIP
    ───────────────────────────────────────────── */
    [data-testid="stTooltipHoverTarget"] {
        color: #22c55e;
        cursor: help;
    }
    
    /* ─────────────────────────────────────────────
       NUMBER INPUT
    ───────────────────────────────────────────── */
    .stNumberInput input {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 14px !important;
        color: #ffffff !important;
    }
    
    .stNumberInput input:focus {
        border-color: #22c55e !important;
        box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.15) !important;
    }
    
    /* ─────────────────────────────────────────────
       DATE INPUT
    ───────────────────────────────────────────── */
    .stDateInput input {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 14px !important;
        color: #ffffff !important;
    }
    
    .stDateInput input:focus {
        border-color: #22c55e !important;
        box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.15) !important;
    }
    
    /* ─────────────────────────────────────────────
       MULTISELECT
    ───────────────────────────────────────────── */
    .stMultiSelect div[data-baseweb="select"] {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
    }
    
    /* ─────────────────────────────────────────────
       COLOR PICKER
    ───────────────────────────────────────────── */
    .stColorPicker label {
        color: #94a3b8;
    }
    
    /* ─────────────────────────────────────────────
       SUCCESS / ERROR / WARNING TEXT
    ───────────────────────────────────────────── */
    .stSuccess {
        color: #22c55e;
    }
    
    .stError {
        color: #ef4444;
    }
    
    .stWarning {
        color: #f59e0b;
    }
    
    .stInfo {
        color: #3b82f6;
    }
    
    /* ─────────────────────────────────────────────
       PLOTLY CHART CUSTOMIZATION
    ───────────────────────────────────────────── */
    .js-plotly-plot .plotly .main-svg {
        background: transparent !important;
    }
    
    .js-plotly-plot .plotly .bg {
        fill: transparent !important;
    }
    
    /* ─────────────────────────────────────────────
       FOLIUM MAP CUSTOMIZATION
    ───────────────────────────────────────────── */
    .folium-map {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* ─────────────────────────────────────────────
       HIDE STREAMLIT BRANDING
    ───────────────────────────────────────────── */
    .css-1y0tads {
        display: none;
    }
    
    .st-emotion-cache-1y0tads {
        display: none;
    }
    
    /* ─────────────────────────────────────────────
       CUSTOM CONTAINER FOR RESULTS
    ───────────────────────────────────────────── */
    .result-container {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.05), rgba(34, 197, 94, 0.02));
        border: 1px solid rgba(34, 197, 94, 0.15);
        border-radius: 20px;
        padding: 1.5rem;
        margin-top: 1rem;
    }
    
    /* ─────────────────────────────────────────────
       ENHANCED METRIC CARDS
    ───────────────────────────────────────────── */
    .metric-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 1.2rem;
        text-align: center;
        transition: all 0.2s ease;
    }
    
    .metric-card:hover {
        border-color: rgba(34, 197, 94, 0.3);
        transform: translateY(-2px);
    }
    
    /* ─────────────────────────────────────────────
       STATS GRID
    ───────────────────────────────────────────── */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    /* ─────────────────────────────────────────────
       PRICE TAG
    ───────────────────────────────────────────── */
    .price-tag {
        font-size: 2rem;
        font-weight: 800;
        color: #22c55e;
        display: inline-block;
    }
    
    .price-tag small {
        font-size: 0.8rem;
        font-weight: 400;
        color: #64748b;
    }
    </style>
    
    <!-- Floating Action Button -->
    <div class="fab" onclick="window.scrollTo({top: 0, behavior: 'smooth'})">
        ↑
    </div>
    
    <script>
        // Smooth scroll for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    </script>
    """, unsafe_allow_html=True)