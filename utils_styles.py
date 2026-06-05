"""
utils_styles.py — ZAMI Premium UI v3.0
Updated color scheme: Blue + Green + Amber
"""

import streamlit as st

def inject_premium_styles():
    st.markdown("""
    <style>
    /* ─────────────────────────────────────────────
       IMPORT FONTS
    ───────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700;14..32,800;14..32,900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Calistoga&display=swap');
    
    /* ─────────────────────────────────────────────
       GLOBAL STYLES
    ───────────────────────────────────────────── */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, .stApp {
        background: radial-gradient(circle at 10% 20%, #0F172A 0%, #020617 100%) !important;
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
    
    /* Animated background gradient */
    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background: radial-gradient(ellipse at 50% 50%, rgba(59,130,246,0.05), transparent 70%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* ─────────────────────────────────────────────
       ANIMATIONS
    ───────────────────────────────────────────── */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes fadeInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* ─────────────────────────────────────────────
       PREMIUM GLASS CARDS
    ───────────────────────────────────────────── */
    .card {
        background: rgba(15, 23, 42, 0.7) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border: 1px solid rgba(59, 130, 246, 0.15) !important;
        border-radius: 28px !important;
        padding: 2rem !important;
        margin-bottom: 1.5rem !important;
        transition: all 0.4s cubic-bezier(0.2, 0.8, 0.4, 1) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(59, 130, 246, 0.05) !important;
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
        background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.08), transparent) !important;
        transition: left 0.6s ease !important;
    }
    
    .card:hover::before {
        left: 100% !important;
    }
    
    .card:hover {
        transform: translateY(-6px) !important;
        border-color: rgba(59, 130, 246, 0.4) !important;
        box-shadow: 0 20px 40px -15px rgba(59, 130, 246, 0.2), 0 8px 32px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Scenario Card Active */
    .scenario-card-active {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.12), rgba(16, 185, 129, 0.08)) !important;
        border: 1px solid rgba(59, 130, 246, 0.5) !important;
        box-shadow: 0 0 25px rgba(59, 130, 246, 0.15) !important;
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
        background: linear-gradient(135deg, #3B82F6, #10B981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        display: inline-block;
    }
    
    .section-title {
        font-size: 1.8rem;
        background: linear-gradient(135deg, #F8FAFC, #94A3B8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    .owner-exclusive-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        line-height: 1.2;
        background: linear-gradient(135deg, #F8FAFC 0%, #3B82F6 50%, #10B981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        background-size: 200% auto;
        animation: gradientShift 3s ease infinite;
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
        animation: float 3s ease-in-out infinite;
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
        background: linear-gradient(135deg, #3B82F6, #10B981);
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
        background: linear-gradient(135deg, #3B82F6 0%, #10B981 100%) !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 14px 32px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.3px !important;
        transition: all 0.3s cubic-bezier(0.2, 0.8, 0.4, 1) !important;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.25) !important;
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
        box-shadow: 0 15px 30px -8px rgba(59, 130, 246, 0.4) !important;
    }
    
    .stButton button:active {
        transform: translateY(0px) !important;
    }
    
    /* Secondary Button */
    .stButton button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.05) !important;
        box-shadow: none !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
    }
    
    .stButton button[kind="secondary"]:hover {
        background: rgba(59, 130, 246, 0.15) !important;
        border-color: rgba(59, 130, 246, 0.6) !important;
        transform: translateY(-2px) !important;
    }
    
    /* ─────────────────────────────────────────────
       FORM INPUTS
    ───────────────────────────────────────────── */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stTextArea > div > textarea,
    .stNumberInput input {
        background: rgba(15, 23, 42, 0.6) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
        border-radius: 16px !important;
        padding: 14px 18px !important;
        color: #F8FAFC !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div:focus-within,
    .stNumberInput input:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15), 0 0 0 1px #3B82F6 !important;
        outline: none !important;
        background: rgba(15, 23, 42, 0.8) !important;
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
        background: rgba(15, 23, 42, 0.5) !important;
        backdrop-filter: blur(10px) !important;
        padding: 10px 24px !important;
        border-radius: 50px !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        color: #94A3B8 !important;
    }
    
    .stRadio label:hover {
        background: rgba(59, 130, 246, 0.15) !important;
        border-color: rgba(59, 130, 246, 0.5) !important;
        transform: translateY(-2px) !important;
        color: #3B82F6 !important;
    }
    
    /* Active Radio */
    .stRadio div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(16, 185, 129, 0.1)) !important;
        border-color: #3B82F6 !important;
        color: #3B82F6 !important;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.2) !important;
    }
    
    /* ─────────────────────────────────────────────
       TABS
    ───────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(10px);
        border-radius: 60px;
        padding: 6px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 40px;
        padding: 10px 28px;
        font-weight: 600;
        color: #94A3B8;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #3B82F6;
        background: rgba(59, 130, 246, 0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3B82F6, #10B981) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    /* ─────────────────────────────────────────────
       EXPANDER
    ───────────────────────────────────────────── */
    .streamlit-expanderHeader {
        background: rgba(15, 23, 42, 0.6);
        border-radius: 12px;
        font-weight: 600;
        color: #F8FAFC;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(59, 130, 246, 0.1);
        color: #3B82F6;
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
        background: rgba(16, 185, 129, 0.1);
        border-left-color: #10B981;
    }
    
    .stAlert[data-testid="stAlertError"] {
        background: rgba(239, 68, 68, 0.1);
        border-left-color: #EF4444;
    }
    
    .stAlert[data-testid="stAlertWarning"] {
        background: rgba(245, 158, 11, 0.1);
        border-left-color: #F59E0B;
    }
    
    .stAlert[data-testid="stAlertInfo"] {
        background: rgba(59, 130, 246, 0.1);
        border-left-color: #3B82F6;
    }
    
    /* ─────────────────────────────────────────────
       SELECT BOX
    ───────────────────────────────────────────── */
    div[data-baseweb="select"] > div {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 14px;
    }
    
    div[data-baseweb="select"] ul {
        background: #0F172A;
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 14px;
    }
    
    div[data-baseweb="select"] li {
        color: #F8FAFC;
        transition: all 0.2s ease;
    }
    
    div[data-baseweb="select"] li:hover {
        background: rgba(59, 130, 246, 0.1);
    }
    
    /* ─────────────────────────────────────────────
       SLIDER / PROGRESS BAR
    ───────────────────────────────────────────── */
    .stSlider div[data-baseweb="slider"] {
        margin-top: 10px;
    }
    
    .stSlider div[role="slider"] {
        background: #3B82F6 !important;
    }
    
    .stSlider div[data-testid="stThumbValue"] {
        color: #3B82F6 !important;
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #3B82F6, #10B981) !important;
        border-radius: 10px;
    }
    
    /* ─────────────────────────────────────────────
       DATA FRAME
    ───────────────────────────────────────────── */
    .stDataFrame {
        background: rgba(15, 23, 42, 0.4);
        border-radius: 16px;
        border: 1px solid rgba(59, 130, 246, 0.15);
    }
    
    .stDataFrame table {
        color: #F8FAFC;
    }
    
    /* ─────────────────────────────────────────────
       CHECKBOX
    ───────────────────────────────────────────── */
    .stCheckbox label {
        color: #94A3B8;
        transition: all 0.2s ease;
    }
    
    .stCheckbox label:hover {
        color: #3B82F6;
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
        background: rgba(59, 130, 246, 0.4);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(59, 130, 246, 0.6);
    }
    
    /* ─────────────────────────────────────────────
       FLOATING ACTION BUTTON
    ───────────────────────────────────────────── */
    .fab {
        position: fixed;
        bottom: 30px;
        right: 100px;
        background: linear-gradient(135deg, #3B82F6, #10B981);
        width: 50px;
        height: 50px;
        border-radius: 25px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 24px;
        cursor: pointer;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
        transition: all 0.3s ease;
        z-index: 1000;
        border: none;
    }
    
    .fab:hover {
        transform: scale(1.1);
        box-shadow: 0 15px 35px rgba(59, 130, 246, 0.4);
    }
    
    /* ─────────────────────────────────────────────
       FOOTER
    ───────────────────────────────────────────── */
    .footer {
        text-align: center;
        color: #475569;
        padding: 3rem 0;
        font-size: 0.7rem;
        border-top: 1px solid rgba(59, 130, 246, 0.1);
        margin-top: 4rem;
    }
    
    /* ─────────────────────────────────────────────
       ACCURACY PROGRESS BAR
    ───────────────────────────────────────────── */
    .accuracy-container {
        background: rgba(15, 23, 42, 0.6);
        border-radius: 16px;
        padding: 15px;
        margin: 20px 0;
        border: 1px solid rgba(59, 130, 246, 0.15);
    }
    
    .accuracy-badge {
        width: 30px;
        height: 30px;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        font-weight: 700;
    }
    
    /* ─────────────────────────────────────────────
       BEFORE/AFTER SECTION
    ───────────────────────────────────────────── */
    .before-after-dynamic {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.05), rgba(16, 185, 129, 0.02));
        border-radius: 32px;
        padding: 40px;
        margin: 30px 0;
        text-align: center;
        border: 1px solid rgba(59, 130, 246, 0.1);
    }
    
    .before-card {
        background: linear-gradient(135deg, #1E293B, #0F172A);
        border-radius: 24px;
        padding: 20px;
        width: 300px;
        text-align: center;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    .after-card {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.05));
        border-radius: 24px;
        padding: 20px;
        width: 300px;
        text-align: center;
        border: 1px solid #10B981;
    }
    
    .value-gain {
        background: rgba(16, 185, 129, 0.1);
        border-radius: 60px;
        padding: 12px 24px;
        display: inline-block;
        margin-top: 30px;
    }
    
    .gain-number {
        font-size: 20px;
        font-weight: 800;
        color: #10B981;
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
        
        .before-card, .after-card {
            width: 260px;
            padding: 15px;
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
       HERO SECTION
    ───────────────────────────────────────────── */
    .hero-premium {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.8), rgba(2, 6, 23, 0.9));
        border-radius: 32px;
        padding: 60px 40px;
        text-align: center;
        position: relative;
        overflow: hidden;
        margin-bottom: 40px;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    .hero-premium::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(59, 130, 246, 0.08) 0%, transparent 70%);
        animation: heroRotate 25s linear infinite;
    }
    
    @keyframes heroRotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .hero-badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(16, 185, 129, 0.1));
        backdrop-filter: blur(10px);
        padding: 8px 20px;
        border-radius: 100px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        color: #3B82F6;
        margin-bottom: 24px;
        border: 1px solid rgba(59, 130, 246, 0.3);
        text-transform: uppercase;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 20px;
        font-family: 'Space Grotesk', sans-serif;
        background: linear-gradient(135deg, #F8FAFC, #3B82F6, #10B981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #94A3B8;
        max-width: 600px;
        margin: 0 auto 32px;
        line-height: 1.6;
    }
    
    .search-box-premium {
        max-width: 650px;
        margin: 0 auto;
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(12px);
        border-radius: 60px;
        padding: 8px;
        display: flex;
        border: 1px solid rgba(59, 130, 246, 0.2);
        transition: all 0.3s cubic-bezier(0.2, 0.8, 0.4, 1);
    }
    
    .search-box-premium:hover {
        border-color: rgba(59, 130, 246, 0.5);
        box-shadow: 0 0 25px rgba(59, 130, 246, 0.12);
        transform: translateY(-2px);
    }
    
    .search-box-premium input {
        flex: 1;
        background: transparent;
        border: none;
        padding: 18px 24px;
        font-size: 1rem;
        color: white;
        outline: none;
    }
    
    .search-box-premium input::placeholder {
        color: #475569;
    }
    
    .search-box-premium button {
        background: linear-gradient(135deg, #3B82F6, #10B981);
        border: none;
        padding: 12px 36px;
        border-radius: 50px;
        color: white;
        font-weight: 600;
        font-size: 0.95rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2);
    }
    
    .search-box-premium button:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.35);
    }
    
    /* ─────────────────────────────────────────────
       TRUST SECTION
    ───────────────────────────────────────────── */
    .trust-section {
        display: flex;
        justify-content: center;
        gap: 40px;
        flex-wrap: wrap;
        margin: 40px 0;
        padding: 20px;
        background: rgba(255,255,255,0.02);
        border-radius: 20px;
    }
    
    .trust-item {
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .trust-item:hover {
        transform: translateY(-5px);
    }
    
    .trust-icon {
        font-size: 28px;
        margin-bottom: 8px;
    }
    
    .trust-text {
        font-size: 12px;
        color: #64748b;
    }
    
    .review-card {
        background: rgba(255,255,255,0.03);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(59, 130, 246, 0.1);
        transition: all 0.3s ease;
    }
    
    .review-card:hover {
        transform: translateY(-5px);
        border-color: rgba(59, 130, 246, 0.3);
    }
    
    .review-stars {
        color: #F59E0B;
        margin-bottom: 12px;
    }
    
    .review-text {
        font-size: 14px;
        color: #CBD5E1;
        margin-bottom: 12px;
        font-style: italic;
    }
    
    .review-author {
        font-size: 12px;
        color: #10B981;
        font-weight: 600;
    }
    
    /* ─────────────────────────────────────────────
       COUNTER SECTION
    ───────────────────────────────────────────── */
    .counter-section {
        display: flex;
        justify-content: center;
        gap: 60px;
        margin: 50px 0;
        text-align: center;
        flex-wrap: wrap;
    }
    
    .counter-item {
        text-align: center;
        padding: 20px 30px;
        background: rgba(255,255,255,0.02);
        border-radius: 20px;
        border: 1px solid rgba(59, 130, 246, 0.1);
        transition: all 0.3s ease;
        min-width: 180px;
    }
    
    .counter-item:hover {
        transform: translateY(-5px);
        border-color: rgba(59, 130, 246, 0.3);
    }
    
    .counter-number {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #3B82F6, #10B981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .counter-label {
        font-size: 0.8rem;
        color: #64748b;
        margin-top: 8px;
    }
    </style>
    
    <!-- Floating Action Button -->
    <div class="fab" onclick="window.scrollTo({top: 0, behavior: 'smooth'})">
        ↑
    </div>
    """, unsafe_allow_html=True)