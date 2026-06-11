import streamlit as st
from utils import high_class_ui

# Import views
import views.estimation_view as estimation_view
import views.homeowner_view as homeowner_view
import views.artisan_view as artisan_view
import views.admin_view as admin_view

# ── ⚡ MUST BE FIRST COMMAND ──
st.set_page_config(
    page_title="ZAMI - Luxury Energy Renovation", 
    page_icon="✨", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# ── ⚡ HIDE STREAMLIT DEFAULT UI ──
st.markdown("""
<style>
    header {display: none !important;}
    .stAppDeployButton {display: none !important;}
    button[kind="header"] {display: none !important;}
    div[data-testid="stToolbar"] {display: none !important;}
    [data-testid="collapsedControl"] {display: none !important;}
    section[data-testid="stSidebar"] {display: none !important;}
    .main .block-container {padding-top: 0rem !important;}
    footer {display: none !important;}
    #MainMenu {display: none !important;}
</style>
""", unsafe_allow_html=True)

# ── ⚡ INJECT LUXURY STYLES ──
high_class_ui.inject_high_class_styles()

# ── ⚡ LUXURY HEADER ──
high_class_ui.luxury_header()

# ── ⚡ SESSION STATE ──
if "property_data" not in st.session_state:
    st.session_state.property_data = None
if "step" not in st.session_state:
    st.session_state.step = "address"
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "pdf_generated" not in st.session_state:
    st.session_state.pdf_generated = False
if "client_user" not in st.session_state:
    st.session_state.client_user = None
if "artisan_user" not in st.session_state:
    st.session_state.artisan_user = None
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# ── ⚡ LUXURY NAVIGATION ──
col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    selected_page = st.radio(
        "",
        ["✨ ESTIMATION", "👑 MON ESPACE", "🔧 ESPACE ARTISAN", "⚜️ ADMIN"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # Map back to original names
    page_map = {
        "✨ ESTIMATION": "🔍 Nouvelle Estimation",
        "👑 MON ESPACE": "🏠 Mon Espace Client",
        "🔧 ESPACE ARTISAN": "👷 Espace Artisan",
        "⚜️ ADMIN": "🔐 Admin"
    }
    selected_page = page_map.get(selected_page, "🔍 Nouvelle Estimation")

# ── ⚡ ROUTING ──
if selected_page == "🔍 Nouvelle Estimation":
    estimation_view.show()
elif selected_page == "🏠 Mon Espace Client":
    homeowner_view.show()
elif selected_page == "👷 Espace Artisan":
    artisan_view.show()
elif selected_page == "🔐 Admin":
    admin_view.show()

# ── ⚡ LUXURY FOOTER ──
high_class_ui.luxury_divider()
st.markdown("""
<div style="text-align: center; padding: 1rem;">
    <p style="color: #555; font-size: 0.7rem; letter-spacing: 1px;">
        ZAMI — L'EXCELLENCE DE LA RÉNOVATION ÉNERGÉTIQUE
    </p>
    <p style="color: #333; font-size: 0.6rem;">
        SOURCES OFFICIELLES · ADEME · DVF · BAN · MAPRIMERÉNOV'
    </p>
</div>
""", unsafe_allow_html=True)
