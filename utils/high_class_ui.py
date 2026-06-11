"""
ZAMI - High-Class Professional UI
Luxury, premium, enterprise-grade design
"""

import streamlit as st
import base64
import os

def get_logo_base64():
    logo_paths = ["assets/zami_logo.png", "assets/logo2.png"]
    for path in logo_paths:
        if os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return None

def inject_high_class_styles():
    """Inject luxury, professional, high-end styles"""
    
    st.markdown("""
    <style>
    /* ========== LUXURY COLOR PALETTE ========== */
    :root {
        --gold: #D4AF37;
        --gold-light: #F3E5AB;
        --gold-dark: #996515;
        --black: #0A0A0A;
        --black-light: #1A1A1A;
        --gray: #2A2A2A;
        --gray-light: #3A3A3A;
        --white: #FFFFFF;
        --white-dim: #F5F5F5;
    }
    
    /* ========== PREMIUM BACKGROUND ========== */
    .stApp {
        background: linear-gradient(135deg, #0A0A0A 0%, #1A1A1A 50%, #0A0A0A 100%);
    }
    
    /* ========== LUXURY HEADER ========== */
    .luxury-header {
        background: linear-gradient(135deg, rgba(10,10,10,0.95), rgba(26,26,26,0.9));
        backdrop-filter: blur(20px);
        border-radius: 0 0 30px 30px;
        padding: 2rem;
        margin: -1rem -1rem 2rem -1rem;
        border-bottom: 2px solid var(--gold);
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        position: relative;
        overflow: hidden;
    }
    
    .luxury-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -50%;
        width: 200%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(212,175,55,0.1), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .logo-gold {
        width: 60px;
        height: 60px;
        object-fit: contain;
        filter: drop-shadow(0 0 15px rgba(212,175,55,0.5));
    }
    
    .gold-text {
        font-size: 3rem;
        font-weight: 300;
        letter-spacing: 8px;
        background: linear-gradient(135deg, var(--gold), var(--gold-light), var(--gold));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        font-family: 'Playfair Display', serif;
    }
    
    .gold-subtitle {
        color: var(--gold-light);
        font-size: 0.8rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        font-weight: 300;
    }
    
    /* ========== PREMIUM NAVIGATION ========== */
    .luxury-nav {
        background: rgba(26,26,26,0.8);
        backdrop-filter: blur(10px);
        border-radius: 60px;
        padding: 0.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(212,175,55,0.3);
    }
    
    .luxury-nav-item {
        display: inline-block;
        padding: 0.7rem 1.8rem;
        margin: 0 0.2rem;
        border-radius: 50px;
        color: #888;
        font-weight: 500;
        transition: all 0.3s ease;
        cursor: pointer;
        font-size: 0.9rem;
    }
    
    .luxury-nav-item.active {
        background: linear-gradient(135deg, var(--gold-dark), var(--gold));
        color: var(--black);
        box-shadow: 0 5px 15px rgba(212,175,55,0.3);
    }
    
    /* ========== LUXURY CARDS ========== */
    .luxury-card {
        background: linear-gradient(135deg, rgba(26,26,26,0.9), rgba(10,10,10,0.8));
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(212,175,55,0.2);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .luxury-card::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--gold), transparent);
        transform: scaleX(0);
        transition: transform 0.4s ease;
    }
    
    .luxury-card:hover::after {
        transform: scaleX(1);
    }
    
    .luxury-card:hover {
        transform: translateY(-5px);
        border-color: rgba(212,175,55,0.5);
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }
    
    /* ========== PREMIUM METRICS ========== */
    .metric-luxury {
        background: rgba(26,26,26,0.6);
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid rgba(212,175,55,0.2);
        transition: all 0.3s ease;
        position: relative;
    }
    
    .metric-luxury:hover {
        transform: translateY(-3px);
        border-color: var(--gold);
        box-shadow: 0 10px 25px rgba(212,175,55,0.2);
    }
    
    .metric-gold-value {
        font-size: 2rem;
        font-weight: 600;
        color: var(--gold);
        font-family: 'Playfair Display', serif;
    }
    
    .metric-label-luxury {
        font-size: 0.7rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 0.5rem;
    }
    
    /* ========== LUXURY BUTTONS ========== */
    .stButton > button {
        background: linear-gradient(135deg, var(--gold-dark), var(--gold));
        color: var(--black);
        border: none;
        border-radius: 50px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        width: 100%;
        text-transform: uppercase;
        font-size: 0.8rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(212,175,55,0.4);
        background: linear-gradient(135deg, var(--gold), var(--gold-light));
    }
    
    /* ========== LUXURY INPUTS ========== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: rgba(26,26,26,0.8);
        border: 1px solid rgba(212,175,55,0.3);
        border-radius: 50px;
        padding: 0.8rem 1.5rem;
        color: var(--white);
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--gold);
        box-shadow: 0 0 0 3px rgba(212,175,55,0.2);
        transform: scale(1.01);
    }
    
    /* ========== LUXURY DIVIDER ========== */
    .luxury-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--gold), var(--gold-light), var(--gold), transparent);
        margin: 2rem 0;
    }
    
    /* ========== CUSTOM SCROLLBAR ========== */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: var(--black-light);
    }
    ::-webkit-scrollbar-thumb {
        background: var(--gold);
        border-radius: 3px;
    }
    
    /* ========== RESPONSIVE ========== */
    @media (max-width: 768px) {
        .gold-text {
            font-size: 1.8rem;
            letter-spacing: 4px;
        }
        .logo-gold {
            width: 40px;
            height: 40px;
        }
        .luxury-card {
            padding: 1rem;
        }
        .metric-gold-value {
            font-size: 1.4rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def luxury_header():
    """Display luxury gold-themed header"""
    
    logo_base64 = get_logo_base64()
    
    if logo_base64:
        st.markdown(f'''
        <div class="luxury-header">
            <div style="text-align: center;">
                <img src="data:image/png;base64,{logo_base64}" class="logo-gold">
                <h1 class="gold-text">ZAMI</h1>
                <p class="gold-subtitle">INTELLIGENCE ARTIFICIELLE POUR LA RÉNOVATION ÉNERGÉTIQUE</p>
                <div style="margin-top: 1rem;">
                    <span style="color: var(--gold); font-size: 0.7rem;">✦</span>
                    <span style="color: #666; margin: 0 0.5rem;">ADEME</span>
                    <span style="color: var(--gold); font-size: 0.7rem;">✦</span>
                    <span style="color: #666; margin: 0 0.5rem;">DVF</span>
                    <span style="color: var(--gold); font-size: 0.7rem;">✦</span>
                    <span style="color: #666; margin: 0 0.5rem;">MaPrimeRénov'</span>
                    <span style="color: var(--gold); font-size: 0.7rem;">✦</span>
                    <span style="color: #666; margin: 0 0.5rem;">IA</span>
                    <span style="color: var(--gold); font-size: 0.7rem;">✦</span>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="luxury-header">
            <div style="text-align: center;">
                <h1 class="gold-text">ZAMI</h1>
                <p class="gold-subtitle">INTELLIGENCE ARTIFICIELLE POUR LA RÉNOVATION ÉNERGÉTIQUE</p>
            </div>
        </div>
        ''', unsafe_allow_html=True)


def luxury_metric(label, value, delta=None, icon=None):
    """Display luxury metric card"""
    
    delta_html = f'<p style="color: var(--gold); font-size: 0.7rem;">{delta}</p>' if delta else ''
    
    st.markdown(f'''
    <div class="metric-luxury">
        <div class="metric-gold-value">{value}</div>
        <div class="metric-label-luxury">{label}</div>
        {delta_html}
    </div>
    ''', unsafe_allow_html=True)


def luxury_card(content, title=None):
    """Display luxury card"""
    
    title_html = f'<h3 style="color: var(--gold); margin-bottom: 1rem; font-weight: 300;">{title}</h3>' if title else ''
    
    st.markdown(f'''
    <div class="luxury-card">
        {title_html}
        {content}
    </div>
    ''', unsafe_allow_html=True)


def luxury_divider():
    """Display luxury gold divider"""
    st.markdown('<div class="luxury-divider"></div>', unsafe_allow_html=True)
