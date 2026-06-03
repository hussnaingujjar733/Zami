import streamlit as st

def inject_premium_styles():
    """
    Injects a trillion-dollar company grade UI/UX framework into the application workspace.
    Features: Glassmorphism design elements, Neon gradient glowing tracking lines, 
    Premium Apple-inspired typography, and dynamic micro-interactions.
    """
    st.markdown("""
    <style>
    /* ── 🪐 GLOBAL LUXURY FONTS & RESET CORE ── */
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    *, *::before, *::after { 
        box-sizing: border-box; 
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    #MainMenu, footer, header { visibility: hidden; }
    
    /* ── 🛰️ MATTE BLACK SPACE CANVAS BACKGROUND ── */
    html, body, .stApp { 
        background: #020306 !important; 
        color: #f8fafc !important; 
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        letter-spacing: -0.01em;
    }
    
    /* Cybernetic grid ambient layout pattern texture fallback */
    .stApp::before {
        content: ''; position: fixed; inset: 0;
        background-image: 
            linear-gradient(rgba(34, 197, 94, 0.01) 1px, transparent 1px),
            linear-gradient(90deg, rgba(34, 197, 94, 0.01) 1px, transparent 1px);
        background-size: 40px 40px;
        pointer-events: none; z-index: 0; opacity: 0.7;
    }
    
    /* ── 🏔️ APPLE-INSPIRED PREMIUM FLOATING NAVBAR ── */
    .brand-header-flex { 
        display: flex; 
        align-items: center; 
        justify-content: space-between; 
        background: linear-gradient(180deg, rgba(10, 15, 30, 0.7) 0%, rgba(5, 8, 16, 0.4) 100%);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(255, 255, 255, 0.04);
        padding: 1.2rem 2.5rem; 
        border-radius: 24px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
        margin-bottom: 2.5rem; 
        width: 100%; 
    }
    
    .brand-status-tag { 
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.12) 0%, rgba(21, 128, 61, 0.04) 100%); 
        border: 1px solid rgba(34, 197, 94, 0.3); 
        padding: 8px 18px; 
        border-radius: 100px; 
        font-size: 0.72rem; 
        font-weight: 700; 
        color: #4ade80; 
        letter-spacing: 0.08em;
        text-transform: uppercase;
        box-shadow: 0 0 20px rgba(34, 197, 94, 0.15);
    }
    
    /* ── 🔮 HIGH-FIDELITY GLASSMORPHISM CARDS (STRIPE-GRADE) ── */
    .card { 
        background: linear-gradient(135deg, rgba(13, 18, 33, 0.85) 0%, rgba(7, 10, 19, 0.95) 100%); 
        border: 1px solid rgba(255, 255, 255, 0.06); 
        border-radius: 28px; 
        padding: 2.5rem 2.8rem; 
        box-shadow: 0 40px 90px rgba(0, 0, 0, 0.65), inset 0 1px 1px rgba(255, 255, 255, 0.1); 
        margin-bottom: 2rem; 
        position: relative;
        overflow: hidden;
    }
    
    .card::after {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
        background: linear-gradient(90deg, transparent, rgba(34, 197, 94, 0.2), transparent);
    }
    
    .card:hover {
        border-color: rgba(34, 197, 94, 0.25);
        box-shadow: 0 45px 100px rgba(34, 197, 94, 0.05), 0 40px 90px rgba(0, 0, 0, 0.7);
        transform: translateY(-2px);
    }
    
    /* Active selection luxury layout accent override */
    .scenario-card-active { 
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.08) 0%, rgba(8, 12, 24, 0.98) 100%) !important; 
        border: 1px solid rgba(34, 197, 94, 0.45) !important; 
        box-shadow: 0 20px 45px rgba(34, 197, 94, 0.08), inset 0 1px 2px rgba(34, 197, 94, 0.2) !important; 
    }
    
    /* ── 🪐 LUXURY TYPOGRAPHY ENGINE ── */
    h1, h2, h3, h4 { 
        font-family: 'SF Pro Display', -apple-system, sans-serif !important; 
        font-weight: 700 !important;
        letter-spacing: -0.03em !important;
    }
    
    .owner-exclusive-title { 
        font-family: 'SF Pro Display', sans-serif; 
        font-size: 2.8rem; 
        font-weight: 900;
        color: #ffffff; 
        margin-bottom: 0.8rem; 
        letter-spacing: -0.04em;
        background: linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .section-label { 
        font-size: 0.75rem; 
        font-weight: 800; 
        letter-spacing: 0.18em; 
        text-transform: uppercase; 
        color: #22c55e; 
        margin-bottom: 0.4rem; 
        font-family: 'SF Pro Display', sans-serif;
    }
    
    .section-title { 
        font-family: 'SF Pro Display', sans-serif; 
        font-size: 1.9rem; 
        color: #f8fafc; 
        font-weight: 700;
        margin: 0 0 0.8rem 0; 
    }
    
    /* ── 🟢 PREMIUM GLOWING DPE BADGE (OFFICIAL DESIGN MATRICES) ── */
    .dpe-badge-big { 
        display: inline-block; 
        padding: 16px 40px; 
        font-size: 4rem; 
        font-weight: 900; 
        font-family: 'SF Pro Display', sans-serif;
        border-radius: 22px; 
        color: #ffffff !important; 
        text-align: center; 
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
        position: relative;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    /* ── 📊 METRIC VALUE COMPRESSION ── */
    .metric-value-huge { 
        font-size: 3.2rem; 
        font-weight: 900; 
        font-family: 'SF Pro Display', sans-serif;
        color: #ffffff; 
        letter-spacing: -0.04em; 
        line-height: 1; 
    }
    
    .metric-label-sub { 
        font-size: 0.8rem; 
        color: #64748b; 
        text-transform: uppercase; 
        letter-spacing: 0.1em; 
        font-weight: 700;
        margin-top: 0.3rem;
        display: inline-block; 
    }
    
    /* ── 🎛️ SYSTEM COMPONENT OVERRIDES (STREAMLIT NATIVE MODIFICATIONS) ── */
    /* Input field optimization */
    .stTextInput div div input {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 14px !important;
        padding: 12px 18px !important;
        color: #fff !important;
        font-size: 1rem !important;
    }
    .stTextInput div div input:focus {
        border-color: #22c55e !important;
        box-shadow: 0 0 15px rgba(34, 197, 94, 0.2) !important;
    }
    
    /* Premium button parameters configuration */
    .stButton button {
        background: linear-gradient(135deg, #16a34a 0%, #15803d 100%) !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 14px 28px !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: -0.01em !important;
        box-shadow: 0 10px 25px rgba(22, 163, 74, 0.25) !important;
        cursor: pointer;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
        box-shadow: 0 12px 30px rgba(34, 197, 94, 0.4) !important;
        transform: translateY(-1px);
    }
    
    /* Dropdown selection lists optimization */
    .stSelectbox div div div {
        background: rgba(15, 23, 42, 0.6) !important;
        border-radius: 14px !important;
        color: white !important;
    }
    
    /* Slider architecture improvements */
    .stSlider div div div div {
        background-color: #22c55e !important;
    }
    
    /* ── 📝 SYSTEM FOOTER ── */
    .footer { 
        text-align: center; 
        color: #334155; 
        padding: 4rem 0 2rem 0; 
        font-size: 0.8rem; 
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        border-top: 1px solid rgba(255, 255, 255, 0.03); 
        margin-top: 5rem; 
    }
    </style>
    """, unsafe_allow_html=True)