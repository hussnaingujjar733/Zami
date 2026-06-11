"""
ZAMI - Premium 3D UI with Wow Effects
"""

import streamlit as st
import base64
import os
from PIL import Image

def get_logo_base64():
    """Load logo and convert to base64"""
    
    # Try multiple possible paths
    logo_paths = ["assets/zami_logo.png", "assets/logo2.png", "assets/logo.png"]
    
    for path in logo_paths:
        full_path = os.path.join(os.getcwd(), path)
        if os.path.exists(full_path):
            with open(full_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    
    return None

def inject_premium_3d_styles():
    """Inject premium 3D styles"""
    
    st.markdown("""
    <style>
    /* ========== BACKGROUND ========== */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e293b, #0f172a, #1e1b4b);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    /* ========== LOGO + GLOWING TEXT ========== */
    @keyframes glowPulse {
        0% {
            text-shadow: 0 0 5px #34d399, 0 0 10px #34d399;
            opacity: 0.8;
        }
        50% {
            text-shadow: 0 0 15px #34d399, 0 0 25px #10b981, 0 0 35px #059669;
            opacity: 1;
        }
        100% {
            text-shadow: 0 0 5px #34d399, 0 0 10px #34d399;
            opacity: 0.8;
        }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .logo-img {
        width: 50px;
        height: 50px;
        object-fit: contain;
        animation: float 3s ease-in-out infinite;
        filter: drop-shadow(0 0 10px rgba(52, 211, 153, 0.5));
    }
    
    .glowing-text {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #34d399, #10b981, #059669);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glowPulse 2s ease-in-out infinite;
        display: inline-block;
        margin: 0 0.5rem;
    }
    
    .header-container {
        text-align: center;
        padding: 1rem 0 2rem 0;
    }
    
    .logo-wrapper {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
    }
    
    /* ========== CARDS ========== */
    .glass-3d {
        background: rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(12px);
        border-radius: 24px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(52, 211, 153, 0.3);
        transition: all 0.4s ease;
    }
    
    .glass-3d:hover {
        transform: translateY(-5px);
        border-color: rgba(52, 211, 153, 0.6);
        box-shadow: 0 20px 40px rgba(52, 211, 153, 0.1);
    }
    
    /* ========== METRICS ========== */
    .metric-3d {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9));
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(52, 211, 153, 0.3);
        transition: all 0.3s ease;
    }
    
    .metric-3d:hover {
        transform: translateY(-5px);
        border-color: #34d399;
    }
    
    .metric-value-3d {
        font-size: 1.8rem;
        font-weight: bold;
        background: linear-gradient(135deg, #34d399, #10b981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label-3d {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: 0.5rem;
    }
    
    /* ========== BUTTONS ========== */
    .stButton > button {
        background: linear-gradient(135deg, #2E7D32, #1B5E20);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.7rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(46, 125, 50, 0.3);
    }
    
    /* ========== PARTICLES ========== */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
    }
    
    .particle {
        position: absolute;
        background: rgba(52, 211, 153, 0.3);
        border-radius: 50%;
        pointer-events: none;
        animation: floatParticle linear infinite;
    }
    
    @keyframes floatParticle {
        0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100vh) rotate(360deg); opacity: 0; }
    }
    
    /* ========== RESPONSIVE ========== */
    @media (max-width: 768px) {
        .logo-img {
            width: 40px;
            height: 40px;
        }
        .glowing-text {
            font-size: 2rem;
        }
        .metric-value-3d {
            font-size: 1.4rem;
        }
    }
    
    /* ========== SCROLLBAR ========== */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #1e293b;
    }
    ::-webkit-scrollbar-thumb {
        background: #34d399;
        border-radius: 4px;
    }
    </style>
    
    <div class="particles" id="particles"></div>
    <script>
        (function() {
            const container = document.getElementById('particles');
            if(!container) return;
            for(let i = 0; i < 40; i++) {
                const p = document.createElement('div');
                p.className = 'particle';
                const size = Math.random() * 4 + 2;
                p.style.width = size + 'px';
                p.style.height = size + 'px';
                p.style.left = Math.random() * 100 + '%';
                p.style.animationDuration = Math.random() * 10 + 5 + 's';
                p.style.animationDelay = Math.random() * 10 + 's';
                container.appendChild(p);
            }
        })();
    </script>
    """, unsafe_allow_html=True)


def premium_header():
    """Display header with logo and glowing text"""
    
    logo_base64 = get_logo_base64()
    
    if logo_base64:
        # With logo
        st.markdown(f'''
        <div class="header-container">
            <div class="logo-wrapper">
                <img src="data:image/png;base64,{logo_base64}" class="logo-img" alt="Logo">
                <h1 class="glowing-text">ZAMI</h1>
                <img src="data:image/png;base64,{logo_base64}" class="logo-img" alt="Logo">
            </div>
            <p style="color: #94a3b8; font-size: 0.9rem; margin-top: 0.5rem;">
                INTELLIGENCE ARTIFICIELLE POUR LA RÉNOVATION ÉNERGÉTIQUE
            </p>
            <div style="display: flex; justify-content: center; gap: 0.5rem; margin-top: 1rem; flex-wrap: wrap;">
                <span style="background: rgba(52,211,153,0.15); padding: 0.2rem 0.7rem; border-radius: 20px; font-size: 0.7rem;">ADEME</span>
                <span style="background: rgba(52,211,153,0.15); padding: 0.2rem 0.7rem; border-radius: 20px; font-size: 0.7rem;">DVF</span>
                <span style="background: rgba(52,211,153,0.15); padding: 0.2rem 0.7rem; border-radius: 20px; font-size: 0.7rem;">MaPrimeRénov'</span>
                <span style="background: rgba(52,211,153,0.15); padding: 0.2rem 0.7rem; border-radius: 20px; font-size: 0.7rem;">IA</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        # Without logo (fallback)
        st.markdown('''
        <div class="header-container">
            <h1 class="glowing-text">🏠 ZAMI</h1>
            <p style="color: #94a3b8; font-size: 0.9rem; margin-top: 0.5rem;">
                INTELLIGENCE ARTIFICIELLE POUR LA RÉNOVATION ÉNERGÉTIQUE
            </p>
        </div>
        ''', unsafe_allow_html=True)


def premium_metric(label, value, delta=None, icon="📊"):
    """Display premium metric card"""
    
    delta_html = f'<p style="color: #10b981; font-size: 0.7rem;">{delta}</p>' if delta else ''
    
    st.markdown(f'''
    <div class="metric-3d">
        <div style="font-size: 1.5rem;">{icon}</div>
        <div class="metric-value-3d">{value}</div>
        <div class="metric-label-3d">{label}</div>
        {delta_html}
    </div>
    ''', unsafe_allow_html=True)


def premium_button(label, key=None):
    """Display premium button"""
    return st.button(label, key=key, use_container_width=True)


def premium_card(content, title=None, icon=None):
    """Display premium glass card"""
    
    title_html = f'<h3 style="color: #34d399; margin-bottom: 0.5rem;">{icon} {title}</h3>' if title else ''
    
    st.markdown(f'''
    <div class="glass-3d">
        {title_html}
        {content}
    </div>
    ''', unsafe_allow_html=True)


def show_confetti():
    """Show confetti effect"""
    st.components.v1.html("""
    <script>
        (function() {
            const colors = ['#34d399', '#10b981', '#2E7D32', '#f59e0b'];
            for(let i = 0; i < 80; i++) {
                const c = document.createElement('div');
                c.style.position = 'fixed';
                c.style.left = Math.random() * 100 + '%';
                c.style.top = '-10px';
                c.style.width = Math.random() * 8 + 4 + 'px';
                c.style.height = Math.random() * 8 + 4 + 'px';
                c.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                c.style.borderRadius = '50%';
                c.style.pointerEvents = 'none';
                c.style.zIndex = '9999';
                c.style.animation = 'fall 2s linear forwards';
                document.body.appendChild(c);
                setTimeout(() => c.remove(), 2000);
            }
        })();
    </script>
    <style>
        @keyframes fall {
            0% { transform: translateY(0) rotate(0deg); opacity: 1; }
            100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
        }
    </style>
    """, height=0)
