import streamlit as st
import streamlit.components.v1 as components
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
    /* Premium navigation buttons */
    div[role="radiogroup"] {
        display: flex;
        justify-content: center;
        gap: 1rem;
        padding: 0.8rem;
        background: rgba(10,10,10,0.65);
        border: 1px solid rgba(212,175,55,0.25);
        border-radius: 999px;
        margin: 1rem auto 2rem auto;
        max-width: 850px;
        box-shadow: 0 12px 35px rgba(0,0,0,0.35);
    }

    div[role="radiogroup"] label {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(212,175,55,0.18);
        border-radius: 999px;
        padding: 0.75rem 1.4rem !important;
        min-width: 170px;
        text-align: center;
        transition: all 0.25s ease;
        cursor: pointer;
    }

    div[role="radiogroup"] label:hover {
        border-color: rgba(212,175,55,0.7);
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(212,175,55,0.15);
    }

    div[role="radiogroup"] label:has(input:checked) {
        background: linear-gradient(135deg, #996515, #D4AF37);
        color: #0A0A0A !important;
        font-weight: 700;
        box-shadow: 0 10px 25px rgba(212,175,55,0.35);
    }

    div[role="radiogroup"] label p {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
    }

    @media (max-width: 768px) {
        div[role="radiogroup"] {
            flex-direction: column;
            border-radius: 24px;
            gap: 0.6rem;
        }

        div[role="radiogroup"] label {
            width: 100%;
            min-width: unset;
        }
    }
</style>
""", unsafe_allow_html=True)


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


components.html("""
<script type="text/javascript">
(function(c,l,a,r,i,t,y){
    c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
})(window, document, "clarity", "script", "x62g3pef8k");
</script>
""", height=0)

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
        "Navigation principale",
        ["✨ ESTIMATION", "👑 MON ESPACE", "🔧 ESPACE ARTISAN"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # Map back to original names
    page_map = {
        "✨ ESTIMATION": "🔍 Nouvelle Estimation",
        "👑 MON ESPACE": "🏠 Mon Espace Client",
        "🔧 ESPACE ARTISAN": "👷 Espace Artisan"
    }
    selected_page = page_map.get(selected_page, "🔍 Nouvelle Estimation")

    # Hidden admin access:
    # https://thezami.com/?admin=true
    if st.query_params.get("admin") == "true":
        selected_page = "🔐 Admin"

# ── ⚡ ROUTING ──
if selected_page == "🔍 Nouvelle Estimation":
    st.markdown("""
    <div class="luxury-card" style="text-align:center;">
        <h1 style="color:#D4AF37; margin-bottom:0.5rem;">Rénovez mieux. Estimez vos travaux en 2 minutes.</h1>
        <p style="color:#ccc; font-size:1.1rem;">
            Obtenez une fourchette de coût, un niveau de confiance, une estimation des aides
            et un rapport PDF pour votre projet de rénovation énergétique.
        </p>
        <p style="color:#D4AF37; font-weight:600;">
            ✓ Estimation gratuite &nbsp; ✓ Rapport PDF &nbsp; ✓ Devis d'artisans &nbsp; ✓ Sans engagement
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        high_class_ui.luxury_metric("1", "Adresse", delta="Recherche BAN")
    with col_b:
        high_class_ui.luxury_metric("2", "Analyse", delta="DPE / logement")
    with col_c:
        high_class_ui.luxury_metric("3", "Estimation", delta="Coût + aides")
    with col_d:
        high_class_ui.luxury_metric("4", "Devis", delta="Artisans")

    st.markdown("""
    <div class="luxury-card" style="text-align:center; border:1px solid rgba(52,211,153,0.25);">
        <h3 style="color:#34d399;">🔒 Une estimation transparente, pas une promesse commerciale</h3>
        <p style="color:#ccc; line-height:1.8;">
            ZAMI affiche une fourchette de coût, un niveau de fiabilité et les limites de l'estimation.
            Le devis final reste confirmé par un professionnel après visite technique.
        </p>
        <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:1rem; margin-top:1rem;">
            <div><strong style="color:#D4AF37;">Données</strong><br><span style="color:#ccc;">ADEME / BAN</span></div>
            <div><strong style="color:#D4AF37;">Rapport</strong><br><span style="color:#ccc;">PDF instantané</span></div>
            <div><strong style="color:#D4AF37;">Méthode</strong><br><span style="color:#ccc;">Fourchette réaliste</span></div>
            <div><strong style="color:#D4AF37;">Devis</strong><br><span style="color:#ccc;">Sans engagement</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="luxury-card">
        <h3 style="color:#D4AF37;">Pourquoi utiliser ZAMI ?</h3>
        <p style="color:#ccc; line-height:1.8;">
            ✓ Fourchette réaliste au lieu d'un prix unique trompeur<br>
            ✓ Niveau de confiance affiché pour plus de transparence<br>
            ✓ Données ADEME lorsque disponibles et Base Adresse Nationale<br>
            ✓ Rapport PDF téléchargeable pour comparer et discuter avec un artisan<br>
            ✓ Demande de devis gratuite et sans engagement
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="luxury-card">
        <h3 style="color:#D4AF37; text-align:center;">Ils peuvent utiliser ZAMI pour préparer leur projet</h3>
        <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; margin-top:1rem;">
            <div style="background:rgba(255,255,255,0.04); padding:1rem; border-radius:16px;">
                <p style="color:#D4AF37;">★★★★★</p>
                <p style="color:#ccc;">"Une estimation claire avant de contacter un artisan."</p>
                <p style="color:#888; font-size:0.8rem;">Propriétaire - Île-de-France</p>
            </div>
            <div style="background:rgba(255,255,255,0.04); padding:1rem; border-radius:16px;">
                <p style="color:#D4AF37;">★★★★★</p>
                <p style="color:#ccc;">"Le rapport PDF aide à comprendre le budget travaux."</p>
                <p style="color:#888; font-size:0.8rem;">Utilisateur bêta</p>
            </div>
            <div style="background:rgba(255,255,255,0.04); padding:1rem; border-radius:16px;">
                <p style="color:#D4AF37;">★★★★★</p>
                <p style="color:#ccc;">"La fourchette de prix est plus réaliste qu'un prix unique."</p>
                <p style="color:#888; font-size:0.8rem;">Projet rénovation</p>
            </div>
        </div>
        <p style="color:#888; font-size:0.8rem; text-align:center; margin-top:1rem;">
            Exemples de retours bêta utilisés pour améliorer l'expérience ZAMI.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="luxury-card" style="text-align:center;">
        <h3 style="color:#D4AF37;">🤝 Réseau d'artisans en construction</h3>
        <p style="color:#ccc;">
            ZAMI est actuellement en phase bêta en Île-de-France.
            Nous intégrons progressivement des artisans partenaires pour traiter les demandes de rénovation énergétique.
        </p>
        <p style="color:#34d399; font-weight:600;">
            ✓ Artisans locaux &nbsp; ✓ Projets qualifiés &nbsp; ✓ Devis comparables &nbsp; ✓ Lancement progressif
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="luxury-card" style="text-align:center; border: 1px solid rgba(212,175,55,0.35);">
        <h3 style="color:#D4AF37;">Prêt à connaître le potentiel de votre logement ?</h3>
        <p style="color:#ccc;">
            Commencez avec votre adresse ci-dessous. L'estimation prend moins de 2 minutes.
        </p>
        <p style="color:#D4AF37; font-weight:600; font-size:1.05rem;">
            ↓ Recevoir mon estimation gratuite ↓
        </p>
    </div>
    """, unsafe_allow_html=True)

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
    <p style="color: #777; font-size: 0.75rem;">
        📧 thezamifrance@gmail.com | 🌐 www.thezami.com
    </p>
</div>
""", unsafe_allow_html=True)

with st.expander("📄 Mentions légales"):
    try:
        with open("mentions_legales.md", "r", encoding="utf-8") as f:
            st.markdown(f.read())
    except FileNotFoundError:
        st.info("Mentions légales non disponibles pour le moment.")

with st.expander("🔒 Politique de confidentialité"):
    try:
        with open("politique_confidentialite.md", "r", encoding="utf-8") as f:
            st.markdown(f.read())
    except FileNotFoundError:
        st.info("Politique de confidentialité non disponible pour le moment.")
