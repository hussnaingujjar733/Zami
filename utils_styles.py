"""
utils_styles.py — ZAMI Premium UI Styling
Complete glassmorphism design with animations and responsive layout
"""

import streamlit as st

def inject_premium_styles():
    """Injects professional CSS styling for ZAMI platform"""
    
    st.markdown("""
    <style>
    /* ─────────────────────────────────────────────
       IMPORT FONTS
    ───────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700;14..32,800;14..32,900&display=swap');
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
       ANIMATIONS
    ───────────────────────────────────────────── */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes fadeInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes glowPulse {
        0%, 100% {
            box-shadow: 0 0 5px rgba(34, 197, 94, 0.2);
        }
        50% {
            box-shadow: 0 0 20px rgba(34, 197, 94, 0.4);
        }
    }
    
    @keyframes borderFlow {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }
    
    /* ─────────────────────────────────────────────
       PREMIUM GLASS CARDS
    ───────────────────────────────────────────── */
    .card {
        background: rgba(10, 15, 30, 0.65) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 28px !important;
        padding: 2rem !important;
        margin-bottom: 1.5rem !important;
        transition: all 0.4s cubic-bezier(0.2, 0.8, 0.4, 1) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
        position: relative !important;
        overflow: hidden !important;
        animation: fadeInUp 0.6s ease-out forwards;
        opacity: 0;
    }
    
    .card:nth-child(1) { animation-delay: 0s; }
    .card:nth-child(2) { animation-delay: 0.1s; }
    .card:nth-child(3) { animation-delay: 0.2s; }
    .card:nth-child(4) { animation-delay: 0.3s; }
    .card:nth-child(5) { animation-delay: 0.4s; }
    .card:nth-child(6) { animation-delay: 0.5s; }
    
    .card::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(34, 197, 94, 0.08), transparent) !important;
        transition: left 0.6s ease !important;
    }
    
    .card:hover::before {
        left: 100% !important;
    }
    
    .card:hover {
        transform: translateY(-6px) !important;
        border-color: rgba(34, 197, 94, 0.3) !important;
        box-shadow: 0 20px 40px -15px rgba(34, 197, 94, 0.15), 0 8px 32px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Scenario Card Active */
    .scenario-card-active {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.12), rgba(15, 25, 45, 0.8)) !important;
        border: 1px solid rgba(34, 197, 94, 0.4) !important;
        box-shadow: 0 0 25px rgba(34, 197, 94, 0.15) !important;
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
        padding: 22px 55px;
        font-size: 4.5rem;
        font-weight: 900;
        border-radius: 32px;
        color: white;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 15px 35px -10px rgba(0,0,0,0.4);
        position: relative;
        overflow: hidden;
        animation: glowPulse 2s infinite;
    }
    
    .dpe-badge-big::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .dpe-badge-big:hover::before {
        left: 100%;
    }
    
    .dpe-badge-big:hover {
        transform: scale(1.02) translateY(-5px);
        box-shadow: 0 25px 45px -12px rgba(0,0,0,0.5);
    }
    
    /* ─────────────────────────────────────────────
       METRICS
    ───────────────────────────────────────────── */
    .metric-value-huge {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.03em;
        display: inline-block;
        animation: fadeInRight 0.6s ease-out;
    }
    
    .metric-label-sub {
        font-size: 0.7rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
        display: inline-block;
        margin-top: 0.3rem;
    }
    
    /* ─────────────────────────────────────────────
       BUTTONS
    ───────────────────────────────────────────── */
    .stButton button {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 14px 32px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.3px !important;
        transition: all 0.3s cubic-bezier(0.2, 0.8, 0.4, 1) !important;
        box-shadow: 0 8px 20px rgba(34, 197, 94, 0.25) !important;
        position: relative !important;
        overflow: hidden !important;
        cursor: pointer !important;
        width: 100%;
    }
    
    .stButton button::before {
        content: '' !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        width: 0 !important;
        height: 0 !important;
        border-radius: 50% !important;
        background: rgba(255, 255, 255, 0.3) !important;
        transform: translate(-50%, -50%) !important;
        transition: width 0.4s ease, height 0.4s ease !important;
    }
    
    .stButton button:hover::before {
        width: 200px !important;
        height: 200px !important;
    }
    
    .stButton button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 30px -8px rgba(34, 197, 94, 0.4) !important;
    }
    
    .stButton button:active {
        transform: translateY(0px) !important;
    }
    
    /* Secondary Button */
    .stButton button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.05) !important;
        box-shadow: none !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .stButton button[kind="secondary"]:hover {
        background: rgba(34, 197, 94, 0.15) !important;
        border-color: rgba(34, 197, 94, 0.3) !important;
        transform: translateY(-2px) !important;
    }
    
    /* ─────────────────────────────────────────────
       FORM INPUTS
    ───────────────────────────────────────────── */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stTextArea > div > textarea,
    .stNumberInput input {
        background: rgba(15, 25, 45, 0.6) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 14px 18px !important;
        color: #fff !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div:focus-within,
    .stNumberInput input:focus {
        border-color: #22c55e !important;
        box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.15), 0 0 0 1px #22c55e !important;
        outline: none !important;
        background: rgba(15, 25, 45, 0.8) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #475569 !important;
    }
    
    /* ─────────────────────────────────────────────
       RADIO BUTTONS
    ───────────────────────────────────────────── */
    .stRadio > div {
        gap: 16px;
        flex-wrap: wrap;
    }
    
    .stRadio label {
        background: rgba(15, 25, 45, 0.5) !important;
        backdrop-filter: blur(10px) !important;
        padding: 10px 24px !important;
        border-radius: 50px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        color: #94a3b8 !important;
    }
    
    .stRadio label:hover {
        background: rgba(34, 197, 94, 0.15) !important;
        border-color: rgba(34, 197, 94, 0.4) !important;
        transform: translateY(-2px) !important;
        color: #22c55e !important;
    }
    
    /* Active Radio */
    .stRadio div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(22, 163, 74, 0.1)) !important;
        border-color: #22c55e !important;
        color: #22c55e !important;
        box-shadow: 0 0 15px rgba(34, 197, 94, 0.2) !important;
    }
    
    /* ─────────────────────────────────────────────
       TABS
    ───────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(15, 25, 45, 0.4);
        backdrop-filter: blur(10px);
        border-radius: 60px;
        padding: 6px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 40px;
        padding: 10px 28px;
        font-weight: 600;
        color: #94a3b8;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #22c55e;
        background: rgba(34, 197, 94, 0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #22c55e, #16a34a) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(34, 197, 94, 0.3);
    }
    
    /* ─────────────────────────────────────────────
       EXPANDER
    ───────────────────────────────────────────── */
    .streamlit-expanderHeader {
        background: rgba(15, 23, 42, 0.6);
        border-radius: 12px;
        font-weight: 600;
        color: #f8fafc;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(34, 197, 94, 0.1);
        color: #22c55e;
    }
    
    /* ─────────────────────────────────────────────
       ALERTS / TOASTS
    ───────────────────────────────────────────── */
    .stAlert {
        border-radius: 14px;
        border-left: 4px solid;
        animation: fadeInLeft 0.3s ease-out;
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
    
    /* ─────────────────────────────────────────────
       SELECT BOX
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
        transition: all 0.2s ease;
    }
    
    div[data-baseweb="select"] li:hover {
        background: rgba(34, 197, 94, 0.1);
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
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #22c55e, #16a34a) !important;
        border-radius: 10px;
    }
    
    /* ─────────────────────────────────────────────
       DATA FRAME
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
       CHECKBOX
    ───────────────────────────────────────────── */
    .stCheckbox label {
        color: #94a3b8;
        transition: all 0.2s ease;
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
       FLOATING ACTION BUTTON
    ───────────────────────────────────────────── */
    .fab {
        position: fixed;
        bottom: 30px;
        right: 100px;
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
       FOOTER
    ───────────────────────────────────────────── */
    .footer {
        text-align: center;
        color: #334155;
        padding: 3rem 0;
        font-size: 0.7rem;
        border-top: 1px solid rgba(255, 255, 255, 0.03);
        margin-top: 4rem;
    }
    
    /* ─────────────────────────────────────────────
       RESPONSIVE DESIGN
    ───────────────────────────────────────────── */
    @media (max-width: 768px) {
        .card {
            padding: 1rem !important;
            border-radius: 20px !important;
        }
        
        .owner-exclusive-title {
            font-size: 1.6rem;
        }
        
        .section-title {
            font-size: 1.2rem;
        }
        
        .metric-value-huge {
            font-size: 2rem;
        }
        
        .dpe-badge-big {
            font-size: 2.5rem;
            padding: 12px 30px;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 6px 16px;
            font-size: 0.8rem;
        }
        
        .fab {
            width: 44px;
            height: 44px;
            font-size: 20px;
            bottom: 20px;
            right: 80px;
        }
        
        .stRadio label {
            padding: 6px 16px;
            font-size: 0.8rem;
        }
        
        .stButton button {
            padding: 10px 20px !important;
            font-size: 0.85rem !important;
        }
    }
    
    /* ─────────────────────────────────────────────
       TABLET RESPONSIVE
    ───────────────────────────────────────────── */
    @media (min-width: 769px) and (max-width: 1024px) {
        .card {
            padding: 1.5rem !important;
        }
        
        .owner-exclusive-title {
            font-size: 2rem;
        }
        
        .metric-value-huge {
            font-size: 2.5rem;
        }
    }
    
    /* ─────────────────────────────────────────────
       LOADING SHIMMER
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
       GRADIENT TEXT UTILITY
    ───────────────────────────────────────────── */
    .gradient-text {
        background: linear-gradient(135deg, #22c55e, #16a34a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* ─────────────────────────────────────────────
       GLOW EFFECT
    ───────────────────────────────────────────── */
    .glow {
        animation: glowPulse 2s infinite;
    }
    </style>
    
    <!-- Floating Action Button -->
    <div class="fab" onclick="window.scrollTo({top: 0, behavior: 'smooth'})">
        ↑
    </div>
    """, unsafe_allow_html=True)