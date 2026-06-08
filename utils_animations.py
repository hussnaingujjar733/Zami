import streamlit as st

def ai_analyzing_animation():
    st.markdown("""
    <style>
    .scanning-container {
        text-align: center;
        padding: 40px;
        background: rgba(15, 23, 42, 0.5);
        border-radius: 16px;
        border: 1px solid rgba(56, 189, 248, 0.2);
        margin: 20px 0;
    }
    .scanner-line {
        height: 2px;
        width: 100%;
        background: #38BDF8;
        box-shadow: 0 0 10px #38BDF8, 0 0 20px #38BDF8;
        animation: scan 1.5s infinite ease-in-out;
    }
    @keyframes scan {
        0% { transform: translateY(-20px); opacity: 0; }
        50% { opacity: 1; }
        100% { transform: translateY(20px); opacity: 0; }
    }
    .loading-text {
        color: #38BDF8;
        margin-top: 20px;
        font-size: 1.1rem;
        font-weight: 600;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    </style>
    
    <div class="scanning-container">
        <div class="scanner-line"></div>
        <div class="loading-text">⚡ ZAMI AI croise les données ADEME & DVF... Veuillez patienter.</div>
    </div>
    """, unsafe_allow_html=True)

def display_premium_metrics(dpe, surface, budget, roi):
    st.markdown(f"""
    <style>
    .metric-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 25px 0;
    }}
    .metric-box {{
        background: linear-gradient(145deg, #1E293B, #0F172A);
        border: 1px solid rgba(56, 189, 248, 0.15);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        transition: transform 0.3s ease;
    }}
    .metric-box:hover {{
        transform: translateY(-5px);
        border-color: #34D399;
    }}
    .metric-title {{
        color: #94A3B8;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }}
    .metric-value {{
        color: #F8FAFC;
        font-size: 2rem;
        font-weight: 800;
    }}
    .metric-highlight {{
        color: #34D399;
    }}
    .dpe-badge {{
        background: #3B82F6;
        color: white;
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 1.8rem;
    }}
    </style>

    <div class="metric-grid">
        <div class="metric-box">
            <div class="metric-title">Étiquette DPE</div>
            <div class="metric-value"><span class="dpe-badge">{dpe}</span></div>
        </div>
        <div class="metric-box">
            <div class="metric-title">Surface</div>
            <div class="metric-value">{surface:.0f} m²</div>
        </div>
        <div class="metric-box">
            <div class="metric-title">Budget Estimé</div>
            <div class="metric-value">{budget:,.0f} €</div>
        </div>
        <div class="metric-box" style="border-color: rgba(52, 211, 153, 0.3);">
            <div class="metric-title">Potentiel ROI</div>
            <div class="metric-value metric-highlight">+{roi:.1f} %</div>
        </div>
    </div>
    """, unsafe_allow_html=True)