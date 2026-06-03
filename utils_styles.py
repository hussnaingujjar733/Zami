import streamlit as st

def inject_premium_styles():
    """Injects the ultra-luxury carbon-tech dark theme design language configuration"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600;700&display=swap');
    *, *::before, *::after { box-sizing: border-box; }
    #MainMenu, footer, header { visibility: hidden; }
    html, body, .stApp { background: #04060a; color: #e2e8f0; font-family: 'DM Sans', sans-serif; }
    .brand-header-flex { display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(255, 255, 255, 0.05); padding-bottom: 1.2rem; margin-bottom: 2rem; width: 100%; }
    .logo-img-container img { height: auto; width: 140px; }
    .brand-status-tag { background: rgba(34,197,94,0.05); border: 1px solid rgba(34,197,94,0.2); padding: 7px 15px; border-radius: 30px; font-size: 0.75rem; font-weight: 600; color: #86efac; letter-spacing: 0.05em; }
    h1, h2, h3, h4 { font-family: 'DM Serif Display', serif; }
    .card { background: linear-gradient(145deg, rgba(10,13,22,0.98), rgba(15,19,32,0.92)); border: 1px solid rgba(148,163,184,0.07); border-radius: 20px; padding: 2rem 2.2rem; box-shadow: 0 25px 60px rgba(0,0,0,0.45); margin-bottom: 1.5rem; }
    .scenario-card-active { background: linear-gradient(135deg, rgba(34,197,94,0.1) 0%, rgba(10,13,22,0.98) 100%); border: 1px solid rgba(34,197,94,0.35) !important; box-shadow: 0 15px 35px rgba(34,197,94,0.05); }
    .owner-exclusive-title { font-family: 'DM Serif Display', serif; font-size: 2.5rem; color: #f8fafc; margin-bottom: 0.5rem; letter-spacing: -0.01em; }
    .dpe-badge-big { display: inline-block; padding: 12px 32px; font-size: 3.5rem; font-weight: 900; border-radius: 16px; color: #fff; text-align: center; box-shadow: 0 15px 35px rgba(0,0,0,0.4); }
    .section-label { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: #22c55e; margin-bottom: 0.3rem; }
    .section-title { font-family: 'DM Serif Display', serif; font-size: 1.7rem; color: #f8fafc; margin: 0 0 0.5rem 0; }
    .metric-value-huge { font-size: 2.8rem; font-weight: 700; color: #ffffff; letter-spacing: -0.02em; line-height: 1.1; }
    .metric-label-sub { font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.08em; display: inline-block; }
    .footer { text-align: center; color: #475569; padding: 3rem 0; font-size: 0.82rem; border-top: 1px solid rgba(255,255,255,0.04); margin-top: 4rem; }
    </style>
    """, unsafe_allow_html=True)