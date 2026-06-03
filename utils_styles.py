"""
utils_styles.py — ZAMI Premium UI Styling with 3D Particles
"""

import streamlit as st

def inject_premium_styles():
    st.markdown("""
    <style>
    /* ─────────────────────────────────────────────
       IMPORT FONTS
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
    
    /* Premium Glass Card */
    .card {
        background: rgba(10, 15, 30, 0.7) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 32px !important;
        padding: 2rem !important;
        margin-bottom: 1.5rem !important;
        transition: all 0.4s cubic-bezier(0.2, 0.8, 0.4, 1) !important;
        box-shadow: 0 25px 45px -12px rgba(0, 0, 0, 0.4) !important;
    }
    
    .card:hover {
        transform: translateY(-6px) !important;
        border-color: rgba(34, 197, 94, 0.4) !important;
        box-shadow: 0 35px 55px -15px rgba(34, 197, 94, 0.15) !important;
    }
    
    /* Typography */
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
    }
    
    /* DPE Badge */
    .dpe-badge-big {
        display: inline-block;
        padding: 20px 50px;
        font-size: 4rem;
        font-weight: 900;
        border-radius: 28px;
        color: white;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 20px 35px -10px rgba(0,0,0,0.4);
    }
    
    .dpe-badge-big:hover {
        transform: scale(1.02);
        box-shadow: 0 25px 40px -12px rgba(0,0,0,0.5);
    }
    
    /* Metrics */
    .metric-value-huge {
        font-size: 3rem;
        font-weight: 800;
        color: #fff;
        letter-spacing: -0.03em;
    }
    
    .metric-label-sub {
        font-size: 0.7rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
        border: none !important;
        border-radius: 40px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 25px -5px rgba(34, 197, 94, 0.4) !important;
    }
    
    /* Inputs */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stTextArea > div > textarea {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 12px 16px !important;
        color: #fff !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #22c55e !important;
        box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.2) !important;
    }
    
    /* Radio Buttons */
    .stRadio > div {
        gap: 16px;
    }
    
    .stRadio label {
        background: rgba(15, 23, 42, 0.6);
        padding: 8px 20px;
        border-radius: 40px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        transition: all 0.2s;
    }
    
    .stRadio label:hover {
        background: rgba(34, 197, 94, 0.1);
        border-color: rgba(34, 197, 94, 0.3);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 23, 42, 0.4);
        border-radius: 60px;
        padding: 6px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 40px;
        padding: 8px 24px;
        font-weight: 600;
        color: #94a3b8;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #22c55e, #16a34a);
        color: white;
    }
    
    /* Floating Action Button */
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
    }
    
    .fab:hover {
        transform: scale(1.1);
        box-shadow: 0 15px 35px rgba(34, 197, 94, 0.4);
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(34, 197, 94, 0.3);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(34, 197, 94, 0.5);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #334155;
        padding: 3rem 0;
        font-size: 0.7rem;
        border-top: 1px solid rgba(255, 255, 255, 0.03);
        margin-top: 4rem;
    }
    
    /* Responsive */
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
        .fab {
            width: 44px;
            height: 44px;
            font-size: 20px;
            bottom: 20px;
            right: 20px;
        }
    }
    </style>
    
    <!-- Floating Action Button -->
    <div class="fab" onclick="window.scrollTo({top: 0, behavior: 'smooth'})">
        ↑
    </div>
    
    <!-- 3D Particle Background -->
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