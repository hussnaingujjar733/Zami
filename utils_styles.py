import streamlit as st

def inject_premium_styles():
    """
    Injects an adaptive trillion-dollar grade UI/UX framework.
    Includes automated CSS Media Queries for fluid layout scaling between Desktop & Mobile.
    """
    st.markdown("""
    <style>
    /* ── 🪐 GLOBAL LUXURY FONTS & RESET CORE ── */
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    *, *::before, *::after { 
        box-sizing: border-box; 
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    #MainMenu, footer, header { visibility: hidden; }
    
    /* ── 🛰️ MATTE BLACK SPACE CANVAS BACKGROUND ── */
    html, body, .stApp { 
        background: #020306 !important; 
        color: #f8fafc !important; 
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        letter-spacing: -0.01em;
    }
    
    .stApp::before {
        content: ''; position: fixed; inset: 0;
        background-image: 
            linear-gradient(rgba(34, 197, 94, 0.01) 1px, transparent 1px),
            linear-gradient(90deg, rgba(34, 197, 94, 0.01) 1px, transparent 1px);
        background-size: 40px 40px;
        pointer-events: none; z-index: 0; opacity: 0.7;
    }
    
    /* ── 🏔️ PREMIUM FLOATING NAVBAR ── */
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
    }
    
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
    }
    
    .section-title { 
        font-family: 'SF Pro Display', sans-serif; 
        font-size: 1.9rem; 
        color: #f8fafc; 
        font-weight: 700;
        margin: 0 0 0.8rem 0; 
    }
    
    .dpe-badge-big { 
        display: inline-block; 
        padding: 16px 40px; 
        font-size: 4rem; 
        font-weight: 900; 
        border-radius: 22px; 
        color: #ffffff !important; 
        text-align: center; 
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
    }
    
    .metric-value-huge { 
        font-size: 3.2rem; 
        font-weight: 900; 
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
    
    /* Input & Button UI elements defaults */
    .stTextInput div div input { background: rgba(15, 23, 42, 0.6) !important; border: 1px solid rgba(255, 255, 255, 0.08) !important; border-radius: 14px !important; padding: 12px 18px !important; color: #fff !important; }
    .stButton button { background: linear-gradient(135deg, #16a34a 0%, #15803d 100%) !important; border: none !important; border-radius: 14px !important; padding: 14px 28px !important; color: white !important; font-weight: 700 !important; box-shadow: 0 10px 25px rgba(22, 163, 74, 0.25) !important; width: 100%; }
    .stSelectbox div div div { background: rgba(15, 23, 42, 0.6) !important; border-radius: 14px !important; color: white !important; }
    .stSlider div div div div { background-color: #22c55e !important; }
    
    .footer { text-align: center; color: #334155; padding: 4rem 0 2rem 0; font-size: 0.8rem; font-weight: 600; border-top: 1px solid rgba(255, 255, 255, 0.03); margin-top: 5rem; }

    /* ─────────────────────────────────────────────
    /* 📱 🚨 AUTOMATED DYNAMIC CSS MEDIA QUERIES (MOBILE OPTIMIZATION LAYER)
    /* ───────────────────────────────────────────── */
    @media (max-width: 768px) {
        /* Adjusting Global Navigation Padding spacing */
        .brand-header-flex {
            flex-direction: column !important;
            gap: 15px !important;
            padding: 1rem 1.5rem !important;
            text-align: center !important;
            align-items: center !important;
        }
        
        /* Balancing Floating elements inside layouts */
        div[data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            gap: 15px !important;
        }
        
        /* Scaling Cards Padding for compact mobile space grids */
        .card {
            padding: 1.5rem 1.5rem !important;
            border-radius: 18px !important;
        }
        
        /* Fluid Responsive Text Down-Scaling */
        .owner-exclusive-title {
            font-size: 1.75rem !important;
            letter-spacing: -0.02em !important;
            line-height: 1.2 !important;
        }
        
        .section-title {
            font-size: 1.35rem !important;
        }
        
        /* Dynamic resizing of huge numeric metric data values */
        .metric-value-huge {
            font-size: 2rem !important;
        }
        
        /* Resizing the Big DPE official rating badge */
        .dpe-badge-big {
            font-size: 2.5rem !important;
            padding: 10px 25px !important;
            border-radius: 14px !important;
        }
        
        /* Folium maps resizing layout safety bounds */
        iframe {
            height: 280px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)