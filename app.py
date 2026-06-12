import streamlit as st
import warnings
import sqlite3
import os

warnings.filterwarnings('ignore')

# ========== FORCE DATABASE INITIALIZATION ==========
# This MUST run before any other imports
from utils import utils_db_marketplace

# Initialize database - create all tables if not exist
try:
    utils_db_marketplace.init_db()
    print("✅ Database initialized successfully")
except Exception as e:
    print(f"Database init error: {e}")

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
    st.markdown("""
    <div class="luxury-card" style="text-align:center;">
        <h2 style="color:#D4AF37;">Estimez vos travaux de rénovation énergétique en quelques minutes</h2>
        <p style="color:#ccc; font-size:1.05rem;">
            ZAMI analyse votre adresse, votre DPE et votre projet pour vous donner une estimation claire,
            une fourchette de coût et un rapport PDF téléchargeable.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        high_class_ui.luxury_metric("Adresse", "BAN", delta="Recherche officielle")
    with col_b:
        high_class_ui.luxury_metric("DPE", "ADEME", delta="Lorsque disponible")
    with col_c:
        high_class_ui.luxury_metric("Estimation", "Fourchette", delta="Pas de fausse précision")
    with col_d:
        high_class_ui.luxury_metric("Rapport", "PDF", delta="Téléchargeable")

    st.markdown("""
    <div class="luxury-card">
        <h3 style="color:#D4AF37;">Comment ça marche ?</h3>
        <p style="color:#ccc;">
            1. Entrez votre adresse<br>
            2. Vérifiez les informations du logement<br>
            3. Obtenez une estimation avec niveau de confiance<br>
            4. Téléchargez votre rapport ou demandez des devis d'artisans
        </p>
        <p style="color:#888; font-size:0.85rem;">
            Estimation indicative. Un devis final nécessite une visite technique par un professionnel qualifié.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("❓ Questions fréquentes"):
        st.markdown("""
        **Cette estimation est-elle un devis final ?**  
        Non. ZAMI fournit une estimation indicative. Le devis final nécessite une visite technique par un artisan.

        **D'où viennent les données ?**  
        Nous utilisons la Base Adresse Nationale et les données ADEME lorsque disponibles. Certaines valeurs sont estimées si les données officielles ne sont pas trouvées.

        **Pourquoi une fourchette de prix ?**  
        Les travaux dépendent de l'état réel du logement, des matériaux et de la visite technique. Une fourchette est plus honnête qu'un prix exact.

        **Puis-je recevoir des devis ?**  
        Oui. Après l'estimation, vous pouvez demander à être contacté par des artisans.

        **Le service est-il gratuit ?**  
        L'estimation initiale est gratuite et sans engagement.
        """)

    estimation_view.show()
elif selected_page == "🏠 Mon Espace Client":
    homeowner_view.show()
elif selected_page == "👷 Espace Artisan":
    artisan_view.show()
elif selected_page == "🔐 Admin":
    admin_view.show()

# ── ⚡ LUXURY FOOTER ──
st.markdown("""
<div style="text-align: center; padding: 1rem; margin-top: 2rem; border-top: 1px solid rgba(212,175,55,0.2);">
    <p style="color: #555; font-size: 0.7rem; letter-spacing: 1px;">
        ZAMI — L'EXCELLENCE DE LA RÉNOVATION ÉNERGÉTIQUE
    </p>
</div>
""", unsafe_allow_html=True)
