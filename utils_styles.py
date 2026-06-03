"""
utils_styles.py — ZAMI Premium UI Styling
Apple/Stripe level glass morphism with 3D particles
"""

import streamlit as st

def inject_premium_styles():
    st.markdown("""
    <style>
    /* ─────────────────────────────────────────────
       FONTS
    ───────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
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
    
    /* Fade In Animation */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .card, .stButton, .stTextInput, .stSelectbox, .stRadio, .stTabs {
        animation: fadeInUp 0.6s ease-out forwards;
    }
    
    .card:nth-child(1) { animation-delay: 0s; }
    .card:nth-child(2) { animation-delay: 0.1s; }
    .card:nth-child(3) { animation-delay: 0.2s; }
    .card:nth-child(4) { animation-delay: 0.3s; }
    
    /* ─────────────────────────────────────────────
       PREMIUM GLASS CARD
    ───────────────────────────────────────────── */
    .card {
        background: rgba(15, 25, 45, 0.65) !important;
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
    }
    
    .card::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(34, 197, 94, 0.15), transparent) !important;
        transition: left 0.6s ease !important;
    }
    
    .card:hover::before {
        left: 100% !important;
    }
    
    .card:hover {
        transform: translateY(-6px) !important;
        border-color: rgba(34, 197, 94, 0.4) !important;
        box-shadow: 0 20px 40px -15px rgba(34, 197, 94, 0.2), 0 8px 32px rgba(0, 0, 0, 0.3) !important;
    }
    
    .card::after {
        content: '' !important;
        position: absolute !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, #22c55e, transparent) !important;
        opacity: 0 !important;
        transition: opacity 0.3s ease !important;
    }
    
    .card:hover::after {
        opacity: 1 !important;
    }
    
    /* Scenario Active Card */
    .scenario-card-active {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.15), rgba(15, 25, 45, 0.8)) !important;
        border: 1px solid rgba(34, 197, 94, 0.5) !important;
        box-shadow: 0 0 20px rgba(34, 197, 94, 0.2) !important;
    }
    
    /* ─────────────────────────────────────────────
       TYPOGRAPHY
    ───────────────────────────────────────────── */
    .owner-exclusive-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    .section-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #fff;
        margin-bottom: 0.5rem;
    }
    
    .section-label {
        font-size: 0.7rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #22c55e;
        font-weight: 800;
        margin-bottom: 0.5rem;
        display: inline-block;
    }
    
    /* ─────────────────────────────────────────────
       PREMIUM BUTTONS
    ───────────────────────────────────────────── */
    .stButton button {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.9) 0%, rgba(22, 163, 74, 0.95) 100%) !important;
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
    
    /* Secondary Button */
    .stButton button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.05) !important;
        box-shadow: none !important;
    }
    
    .stButton button[kind="secondary"]:hover {
        background: rgba(34, 197, 94, 0.15) !important;
        border: 1px solid rgba(34, 197, 94, 0.3) !important;
    }
    
    /* ─────────────────────────────────────────────
       PREMIUM INPUTS
    ───────────────────────────────────────────── */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stTextArea > div > textarea,
    .stNumberInput input {
        background: rgba(15, 25, 45, 0.5) !important;
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
        background: rgba(15, 25, 45, 0.7) !important;
    }
    
    /* ─────────────────────────────────────────────
       PREMIUM RADIO BUTTONS
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
    }
    
    .stRadio label:hover {
        background: rgba(34, 197, 94, 0.15) !important;
        border-color: rgba(34, 197, 94, 0.4) !important;
        transform: translateY(-2px) !important;
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
        transform: scale(1.05) translateY(-5px);
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
       PREMIUM TABS
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
       FLOATING ACTION BUTTON
    ───────────────────────────────────────────── */
    .fab {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: linear-gradient(135deg, #22c55e, #16a34a);
        width: 52px;
        height: 52px;
        border-radius: 26px;
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
       SCROLLBAR
    ───────────────────────────────────────────── */
    ::-webkit-scrollbar {
        width: 6px;
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
        padding: 3rem 0;
        font-size: 0.7rem;
        border-top: 1px solid rgba(255, 255, 255, 0.03);
        margin-top: 4rem;
    }
    
    /* ─────────────────────────────────────────────
       RESPONSIVE
    ───────────────────────────────────────────── */
    @media (max-width: 768px) {
        .card {
            padding: 1rem !important;
        }
        .owner-exclusive-title {
            font-size: 1.6rem;
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
            right: 20px;
        }
        .stRadio label {
            padding: 6px 16px;
            font-size: 0.8rem;
        }
    }
    </style>
    
    <div class="fab" onclick="window.scrollTo({top: 0, behavior: 'smooth'})">
        ↑
    </div>
    
    <div id="tsparticles"></div>
    
    <script src="https://cdn.jsdelivr.net/npm/tsparticles@2.12.0/tsparticles.bundle.min.js"></script>
    <script>
    (function() {
        function loadParticles() {
            if (typeof tsParticles === 'undefined') {
                setTimeout(loadParticles, 100);
                return;
            }
            tsParticles.load("tsparticles", {
                fpsLimit: 60,
                particles: {
                    number: { value: 60, density: { enable: true, area: 800 } },
                    color: { value: ["#22c55e", "#3b82f6", "#a855f7", "#f59e0b"] },
                    shape: { type: "circle" },
                    opacity: { value: 0.3, random: true, animation: { enable: true, speed: 1, minimumValue: 0.1, sync: false } },
                    size: { value: 3, random: true, animation: { enable: true, speed: 2, minimumValue: 0.5, sync: false } },
                    links: { enable: true, color: "#22c55e", opacity: 0.15, distance: 150, width: 1 },
                    move: { enable: true, speed: 1, direction: "none", random: true, straight: false, outModes: { default: "out" } }
                },
                interactivity: { events: { onHover: { enable: true, mode: "grab" }, resize: true }, modes: { grab: { distance: 140, links: { opacity: 0.3 } } } },
                background: { color: "transparent" },
                detectRetina: true
            });
        }
        loadParticles();
    })();
    </script>
    """, unsafe_allow_html=True)