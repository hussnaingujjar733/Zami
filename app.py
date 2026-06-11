import streamlit as st
from utils import premium_ui

# Import views
import views.estimation_view as estimation_view
import views.homeowner_view as homeowner_view
import views.artisan_view as artisan_view
import views.admin_view as admin_view

# ── ⚡ MUST BE FIRST COMMAND ──
st.set_page_config(
    page_title="ZAMI - Rénov' Marketplace", 
    page_icon="🏠", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# ── ⚡ INJECT PREMIUM 3D STYLES ──
premium_ui.inject_premium_3d_styles()

# ── ⚡ PREMIUM HEADER WITH LOGO ──
premium_ui.premium_header()

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
if "selected_project" not in st.session_state:
    st.session_state.selected_project = None
if "quote_submitted" not in st.session_state:
    st.session_state.quote_submitted = False

# ── ⚡ NAVIGATION ──
col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    selected_page = st.radio(
        "Menu Principal",
        ["🔍 Nouvelle Estimation", "🏠 Mon Espace Client", "👷 Espace Artisan", "🔐 Admin"],
        horizontal=True,
        label_visibility="collapsed"
    )

# ── ⚡ ROUTING ──
if selected_page == "🔍 Nouvelle Estimation":
    estimation_view.show()
elif selected_page == "🏠 Mon Espace Client":
    homeowner_view.show()
elif selected_page == "👷 Espace Artisan":
    artisan_view.show()
elif selected_page == "🔐 Admin":
    admin_view.show()

# ── ⚡ FOOTER ──
st.markdown("""
<div style="text-align: center; padding: 2rem; margin-top: 2rem; border-top: 1px solid rgba(52, 211, 153, 0.2);">
    <p style="color: #64748b; font-size: 0.7rem;">
        © 2026 ZAMI - Données officielles ADEME | DVF | MaPrimeRénov'
    </p>
</div>
""", unsafe_allow_html=True)
