"""
ZAMI - Premium UI Package
"""

import streamlit as st
import base64
import os

def get_logo_base64():
    """Load and convert logo to base64"""
    logo_paths = ["assets/zami_logo.png", "assets/logo2.png"]
    for path in logo_paths:
        if os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return None

def inject_premium_styles():
    """Inject premium CSS styles"""
    
    st.markdown("""
    <style>
    /* Global */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    }
    
    /* Header */
    .premium-header {
        background: linear-gradient(135deg, rgba(15,23,42,0.8), rgba(30,41,59,0.6));
        backdrop-filter: blur(20px);
        border-radius: 30px;
        padding: 1.5rem;
        margin: 1rem 0 2rem 0;
        border: 1px solid rgba(52,211,153,0.2);
        text-align: center;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
    }
    
    .logo-img {
        width: 55px;
        height: 55px;
        object-fit: contain;
        animation: float 4s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }
    
    .glowing-text {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #34d399, #10b981, #059669);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.9; text-shadow: 0 0 15px #34d399; }
    }
    
    .premium-badge {
        display: inline-block;
        background: rgba(52,211,153,0.15);
        backdrop-filter: blur(5px);
        padding: 0.3rem 0.8rem;
        border-radius: 50px;
        font-size: 0.7rem;
        margin: 0.2rem;
        border: 1px solid rgba(52,211,153,0.3);
    }
    
    /* Cards */
    .premium-card {
        background: rgba(30,41,59,0.6);
        backdrop-filter: blur(12px);
        border-radius: 24px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(52,211,153,0.2);
        transition: all 0.3s ease;
    }
    
    .premium-card:hover {
        transform: translateY(-5px);
        border-color: rgba(52,211,153,0.5);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    /* Metrics */
    .metric-premium {
        background: linear-gradient(135deg, rgba(30,41,59,0.8), rgba(15,23,42,0.9));
        border-radius: 20px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid rgba(52,211,153,0.3);
        transition: all 0.3s ease;
    }
    
    .metric-premium:hover {
        transform: translateY(-3px);
        border-color: #34d399;
    }
    
    .metric-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        background: linear-gradient(135deg, #34d399, #10b981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        font-size: 0.8rem;
        color: #94a3b8;
        margin-top: 0.5rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #2E7D32, #1B5E20);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(46,125,50,0.4);
    }
    
    /* Inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: rgba(30,41,59,0.8);
        border: 1px solid rgba(52,211,153,0.3);
        border-radius: 50px;
        padding: 0.7rem 1.2rem;
        color: white;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #34d399;
        box-shadow: 0 0 0 2px rgba(52,211,153,0.2);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(30,41,59,0.6);
        padding: 0.5rem;
        border-radius: 60px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 40px;
        padding: 0.5rem 1.2rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2E7D32, #1B5E20);
    }
    
    /* Scrollbar */
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
    
    /* Responsive */
    @media (max-width: 768px) {
        .glowing-text { font-size: 1.8rem; }
        .logo-img { width: 40px; height: 40px; }
        .metric-value { font-size: 1.4rem; }
        .premium-card { padding: 1rem; }
    }
    </style>
    """, unsafe_allow_html=True)


def premium_header():
    """Display premium animated header"""
    
    logo_base64 = get_logo_base64()
    
    if logo_base64:
        st.markdown(f'''
        <div class="premium-header">
            <div class="logo-container">
                <img src="data:image/png;base64,{logo_base64}" class="logo-img">
                <h1 class="glowing-text">ZAMI</h1>
                <img src="data:image/png;base64,{logo_base64}" class="logo-img">
            </div>
            <p style="color: #94a3b8; margin-top: 0.5rem;">INTELLIGENCE ARTIFICIELLE POUR LA RÉNOVATION ÉNERGÉTIQUE</p>
            <div style="display: flex; justify-content: center; gap: 0.5rem; margin-top: 1rem; flex-wrap: wrap;">
                <span class="premium-badge">ADEME</span>
                <span class="premium-badge">DVF</span>
                <span class="premium-badge">MaPrimeRénov</span>
                <span class="premium-badge">IA</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="premium-header">
            <h1 class="glowing-text">🏠 ZAMI</h1>
            <p style="color: #94a3b8;">INTELLIGENCE ARTIFICIELLE POUR LA RÉNOVATION ÉNERGÉTIQUE</p>
        </div>
        ''', unsafe_allow_html=True)


def premium_metric(label, value, delta=None, icon="📊"):
    """Display premium metric card"""
    
    delta_html = f'<p style="color: #10b981; font-size: 0.7rem;">{delta}</p>' if delta else ''
    
    st.markdown(f'''
    <div class="metric-premium">
        <div class="metric-icon">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {delta_html}
    </div>
    ''', unsafe_allow_html=True)


def premium_card(content, title=None, icon=None):
    """Display premium glass card"""
    
    title_html = f'<h3 style="color: #34d399; margin-bottom: 0.75rem;">{icon} {title}</h3>' if title else ''
    
    st.markdown(f'''
    <div class="premium-card">
        {title_html}
        {content}
    </div>
    ''', unsafe_allow_html=True)


def premium_progress(value, max_value=100):
    """Display premium progress bar"""
    percentage = (value / max_value) * 100
    st.markdown(f'''
    <div style="background: #1e293b; border-radius: 10px; height: 8px; overflow: hidden;">
        <div style="background: linear-gradient(90deg, #34d399, #10b981); border-radius: 10px; height: 100%; width: {percentage}%;"></div>
    </div>
    ''', unsafe_allow_html=True)


def show_toast(message, type="success"):
    """Display toast notification"""
    colors = {"success": "#2E7D32", "error": "#dc2626", "info": "#3b82f6"}
    color = colors.get(type, "#2E7D32")
    st.success(message)


def show_confetti():
    """Show confetti effect"""
    st.components.v1.html('''
    <script>
        for(let i=0;i<80;i++){
            const c=document.createElement('div');
            c.style.position='fixed';
            c.style.left=Math.random()*100+'%';
            c.style.top='-10px';
            c.style.width=Math.random()*8+4+'px';
            c.style.height=c.style.width;
            c.style.backgroundColor=['#34d399','#10b981','#2E7D32','#f59e0b'][Math.floor(Math.random()*4)];
            c.style.borderRadius='50%';
            c.style.pointerEvents='none';
            c.style.zIndex='9999';
            c.style.animation='fall 2s linear forwards';
            document.body.appendChild(c);
            setTimeout(()=>c.remove(),2000);
        }
    </script>
    <style>
        @keyframes fall{
            0%{transform:translateY(0) rotate(0deg);opacity:1;}
            100%{transform:translateY(100vh) rotate(360deg);opacity:0;}
        }
    </style>
    ''', height=0)
