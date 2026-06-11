"""
ZAMI - Mobile-Responsive UI Styles
Optimized for all screen sizes
"""

import streamlit as st

def inject_mobile_styles():
    """Inject responsive CSS for mobile, tablet, and desktop"""
    
    st.markdown("""
    <style>
    /* ========== VARIABLES ========== */
    :root {
        --primary: #2E7D32;
        --primary-dark: #1B5E20;
        --primary-light: #34d399;
        --background: #0f172a;
        --surface: #1e293b;
        --text: #f8fafc;
        --text-secondary: #94a3b8;
        --border: #334155;
    }
    
    /* ========== GLOBAL ========== */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .stApp {
        background: linear-gradient(135deg, var(--background) 0%, var(--surface) 100%);
    }
    
    /* ========== MOBILE FIRST (Default) ========== */
    
    /* Header */
    .mobile-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        border-radius: 16px;
        margin-bottom: 1rem;
    }
    
    .mobile-header h1 {
        font-size: 1.8rem;
        color: white;
        margin: 0;
    }
    
    .mobile-header p {
        font-size: 0.8rem;
        color: #E8F5E9;
        margin-top: 0.25rem;
    }
    
    /* Cards */
    .card {
        background: rgba(30, 41, 59, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1rem;
        margin: 0.75rem 0;
        border: 1px solid rgba(52, 211, 153, 0.2);
        transition: all 0.2s ease;
    }
    
    .card:active {
        transform: scale(0.98);
    }
    
    /* Metrics */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.75rem;
        margin: 1rem 0;
    }
    
    .metric-item {
        background: var(--surface);
        border-radius: 12px;
        padding: 0.75rem;
        text-align: center;
        border: 1px solid var(--border);
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, var(--primary-light), #10b981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        font-size: 0.7rem;
        color: var(--text-secondary);
        margin-top: 0.25rem;
    }
    
    /* Buttons */
    .btn-primary, .stButton > button {
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .btn-primary:active, .stButton > button:active {
        transform: scale(0.96);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 50px;
        padding: 0.6rem 1rem;
        color: var(--text);
        font-size: 0.9rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-light);
        box-shadow: 0 0 0 2px rgba(52, 211, 153, 0.2);
    }
    
    /* Tabs for Mobile */
    .stTabs [data-baseweb="tab-list"] {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        background: var(--surface);
        padding: 0.5rem;
        border-radius: 50px;
        margin-bottom: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        flex: 1;
        text-align: center;
        padding: 0.5rem;
        font-size: 0.8rem;
        border-radius: 40px;
        white-space: nowrap;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        color: white;
    }
    
    /* Progress Bar */
    .progress-container {
        background: var(--border);
        border-radius: 10px;
        height: 6px;
        margin: 0.5rem 0;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, var(--primary-light), #10b981);
        border-radius: 10px;
        height: 100%;
        transition: width 0.3s ease;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1.5rem;
        margin-top: 2rem;
        border-top: 1px solid var(--border);
        font-size: 0.7rem;
        color: var(--text-secondary);
    }
    
    /* ========== TABLET (min-width: 768px) ========== */
    @media (min-width: 768px) {
        .mobile-header h1 {
            font-size: 2.2rem;
        }
        
        .metric-grid {
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
        }
        
        .metric-value {
            font-size: 1.8rem;
        }
        
        .card {
            padding: 1.25rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            font-size: 0.9rem;
            padding: 0.6rem 1rem;
        }
    }
    
    /* ========== DESKTOP (min-width: 1024px) ========== */
    @media (min-width: 1024px) {
        .mobile-header h1 {
            font-size: 2.8rem;
        }
        
        .metric-grid {
            grid-template-columns: repeat(4, 1fr);
            gap: 1.25rem;
        }
        
        .metric-value {
            font-size: 2rem;
        }
        
        .card {
            padding: 1.5rem;
        }
    }
    
    /* ========== TOUCH FRIENDLY ========== */
    button, 
    .stButton > button,
    [data-baseweb="tab"],
    .stSelectbox > div,
    input {
        min-height: 44px;
        min-width: 44px;
    }
    
    /* ========== SMOOTH SCROLLING ========== */
    html {
        scroll-behavior: smooth;
    }
    
    /* ========== BOTTOM NAVIGATION FOR MOBILE ========== */
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: var(--surface);
        display: flex;
        justify-content: space-around;
        padding: 0.5rem;
        border-top: 1px solid var(--border);
        z-index: 1000;
    }
    
    .bottom-nav-item {
        text-align: center;
        padding: 0.5rem;
        flex: 1;
        cursor: pointer;
        border-radius: 12px;
        transition: all 0.2s ease;
    }
    
    .bottom-nav-item:active {
        background: rgba(52, 211, 153, 0.1);
    }
    
    .bottom-nav-icon {
        font-size: 1.5rem;
    }
    
    .bottom-nav-label {
        font-size: 0.7rem;
        margin-top: 0.25rem;
        color: var(--text-secondary);
    }
    
    .bottom-nav-item.active .bottom-nav-label {
        color: var(--primary-light);
    }
    
    /* Hide default radio on mobile (use bottom nav instead) */
    @media (max-width: 768px) {
        div[role="radiogroup"] {
            display: none !important;
        }
    }
    
    /* Show bottom nav only on mobile */
    @media (min-width: 769px) {
        .bottom-nav {
            display: none;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def mobile_bottom_nav(selected):
    """Display bottom navigation bar for mobile"""
    
    items = [
        {"icon": "🔍", "label": "Estimation", "key": "🔍 Nouvelle Estimation"},
        {"icon": "🏠", "label": "Espace Client", "key": "🏠 Mon Espace Client"},
        {"icon": "👷", "label": "Artisan", "key": "👷 Espace Artisan"},
        {"icon": "🔐", "label": "Admin", "key": "🔐 Admin"}
    ]
    
    st.markdown('<div class="bottom-nav">', unsafe_allow_html=True)
    
    cols = st.columns(4)
    for i, item in enumerate(items):
        with cols[i]:
            active_class = 'active' if selected == item['key'] else ''
            st.markdown(f"""
            <div class="bottom-nav-item {active_class}" onclick="window.location.href='?page={item['key']}'">
                <div class="bottom-nav-icon">{item['icon']}</div>
                <div class="bottom-nav-label">{item['label']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def responsive_metric(label, value, delta=None, columns=2):
    """Display a responsive metric card"""
    
    delta_html = f'<p style="color: #10b981; font-size: 0.7rem;">{delta}</p>' if delta else ''
    
    st.markdown(f"""
    <div class="metric-item">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def responsive_card(content, title=None):
    """Display a responsive card"""
    
    title_html = f'<h3 style="color: #34d399; margin-bottom: 0.5rem;">{title}</h3>' if title else ''
    
    st.markdown(f"""
    <div class="card">
        {title_html}
        {content}
    </div>
    """, unsafe_allow_html=True)


def show_loading_animation():
    """Show mobile-optimized loading animation"""
    
    st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; padding: 2rem;">
        <div class="custom-spinner"></div>
        <p style="margin-left: 1rem; color: #94a3b8;">Chargement...</p>
    </div>
    <style>
        .custom-spinner {
            width: 30px;
            height: 30px;
            border: 3px solid rgba(52, 211, 153, 0.3);
            border-radius: 50%;
            border-top-color: #34d399;
            animation: spin 0.8s linear infinite;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
    """, unsafe_allow_html=True)

def touch_button(label, key=None, type="primary"):
    """Display a touch-friendly button (min 44px height)"""
    
    button_class = "btn-primary" if type == "primary" else "btn-secondary"
    
    return st.button(
        label, 
        key=key, 
        use_container_width=True,
        help="Tap to continue"
    )
