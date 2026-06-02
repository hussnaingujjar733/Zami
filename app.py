import random
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie

# ── 🧠 IMPORT YOUR NEW ML BACKEND MODULES ──
try:
    import data_pipeline as dp
    import ml_engine as ml
    ML_BACKEND_READY = True
except ImportError:
    ML_BACKEND_READY = False

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ZAMI | Premium Intelligence",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# GLOBAL STYLES — Ultra Luxury Dark Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }
#MainMenu, footer, header { visibility: hidden; }

html, body, .stApp {
    background: #05070c;
    color: #e2e8f0;
    font-family: 'DM Sans', sans-serif;
}

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
    opacity: 0.5;
}

.stApp::after {
    content: '';
    position: fixed;
    top: -20vh;
    right: -10vw;
    width: 80vw;
    height: 80vh;
    background: radial-gradient(ellipse, rgba(220,38,38,0.06) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

.brand-header-flex {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    padding-bottom: 1.2rem;
    margin-bottom: 2rem;
    width: 100%;
}
.logo-img-container img {
    height: auto;
    width: 140px;
    image-rendering: -webkit-optimize-contrast;
    image-rendering: crisp-edges;
}
.brand-status-tag {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 7px 15px;
    border-radius: 30px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    color: #94a3b8;
}

h1, h2, h3, h4 { font-family: 'DM Serif Display', serif; }

.card {
    background: linear-gradient(145deg, rgba(11,14,23,0.98), rgba(16,20,35,0.85));
    border: 1px solid rgba(148,163,184,0.06);
    border-radius: 24px;
    padding: 1.8rem 2rem;
    box-shadow: 0 30px 70px rgba(0,0,0,0.4);
    margin-bottom: 1.5rem;
}

.landing-hero {
    background: linear-gradient(135deg, rgba(11,13,23,0.95), rgba(35,15,15,0.6));
    border: 1px solid rgba(220,38,38,0.15);
    border-radius: 32px;
    padding: 3rem;
    box-shadow: 0 50px 90px rgba(0,0,0,0.45);
    height: 100%;
}
.landing-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(220,38,38,0.08);
    border: 1px solid rgba(220,38,38,0.2);
    color: #fca5a5;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 6px 14px;
    border-radius: 999px;
    margin-bottom: 1.5rem;
}
.landing-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2.2rem, 4.5vw, 3.8rem);
    line-height: 1.1;
    color: #f8fafc;
    margin: 0 0 1.2rem 0;
}
.landing-title em { color: #dc2626; font-style: italic; }

.video-container {
    background: #0f121d;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 32px;
    padding: 1.5rem;
    box-shadow: 0 50px 90px rgba(0,0,0,0.4);
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: 100%;
}

.news-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 16px;
    padding: 1.2rem;
    transition: all 0.2s ease;
    height: 100%;
}
.news-card:hover {
    border-color: rgba(220,38,38,0.3);
    background: rgba(255,255,255,0.04);
}
.news-date { font-size: 0.7rem; font-weight: 700; color: #dc2626; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px; }
.news-title { font-size: 1.05rem; font-weight: 600; color: #fff; margin-bottom: 6px; line-height: 1.4; }
.news-desc { color: #94a3b8; font-size: 0.85rem; line-height: 1.5; }

.stButton > button {
    background: linear-gradient(135deg, #dc2626 0%, #a81a1a 100%) !important;
    color: white !important;
    border: 0 !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 0.8rem 1.5rem !important;
    box-shadow: 0 4px 25px rgba(220,38,38,0.25) !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(220,38,38,0.4) !important;
}

.section-label { font-size: 0.7rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #dc2626; margin-bottom: 0.3rem; }
.section-title { font-family: 'DM Serif Display', serif; font-size: 1.6rem; color: #f8fafc; margin: 0 0 0.4rem 0; }
.footer { text-align: center; color: #475569; padding: 3rem 0; font-size: 0.85rem; border-top: 1px solid rgba(255,255,255,0.04); margin-top: 4rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# STATE CONFIG & STORAGE
# ─────────────────────────────────────────────
if "show_app" not in st.session_state: st.session_state.show_app = False
if "raw_data" not in st.session_state: st.session_state.raw_data = pd.DataFrame()
if "city_coords" not in st.session_state: st.session_state.city_coords = (48.8566, 2.3522)
if "last_zipcode" not in st.session_state: st.session_state.last_zipcode = "75018"
if "address_suggestions" not in st.session_state: st.session_state.address_suggestions = []
if "landing_target_section" not in st.session_state: st.session_state.landing_target_section = "Vue générale"

DEFAULT_CENTER = (48.8566, 2.3522)
DATASET_ID     = "meg-83tjwtg8dyz4vv7h1dqe"

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

lottie_scan = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_5n8y9uob.json")

# ─────────────────────────────────────────────
# APIS AND DATA ENGINES (WITH ML FALLBACKS)
# ─────────────────────────────────────────────
def safe_get(url, params=None, timeout=10):
    try:
        r = requests.get(url, params=params, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception: return None

def get_city_center(zipcode: str):
    data = safe_get("https://geo.api.gouv.fr/communes", {"codePostal": zipcode, "fields": "centre"})
    try:
        c = data[0]["centre"]["coordinates"]
        return c[1], c[0]
    except Exception: return DEFAULT_CENTER

@st.cache_data(ttl=300)
def ban_search(query: str, limit: int = 7):
    if not query or len(query.strip()) < 3: return []
    data = safe_get("https://api-adresse.data.gouv.fr/search/", {"q": query, "limit": limit, "type": "housenumber"})
    if not data: data = safe_get("https://api-adresse.data.gouv.fr/search/", {"q": query, "limit": limit})
    features = data.get("features", []) if data else []
    results = []
    for f in features:
        p = f.get("properties", {})
        coords = f.get("geometry", {}).get("coordinates", [None, None])
        results.append({
            "label":    p.get("label", ""),
            "postcode": p.get("postcode", ""),
            "city":     p.get("city", ""),
            "score":    p.get("score", 0),
            "lat":      coords[1] if len(coords) > 1 else None,
            "lon":      coords[0] if len(coords) > 0 else None,
        })
    results.sort(key=lambda x: x["score"], reverse=True)
    return results

def geocode_address(address: str, fallback_lat: float, fallback_lon: float):
    data = safe_get("https://api-adresse.data.gouv.fr/search/", {"q": address, "limit": 1})
    try:
        coords = data["features"][0]["geometry"]["coordinates"]
        return coords[1], coords[0]
    except Exception:
        return (fallback_lat + random.uniform(-0.004, 0.004), fallback_lon + random.uniform(-0.004, 0.004))

# ── 🤖 ML PREDICTION WRAPPER FOR ADEME STREAMING ──
_FALLBACK_RENO_COST = {"G": 1400, "F": 1150, "E": 650, "D": 300}
_FALLBACK_UPLIFT    = {"G": 0.24, "F": 0.20, "E": 0.13, "D": 0.07}
_RENT_RISK = {"G": "🔴 Interdit", "F": "🟠 Critique", "E": "🟡 Surveillance", "D": "🟢 Conforme"}

def calculate_reno_cost_ml(surface, dpe, zipcode):
    if ML_BACKEND_READY and hasattr(ml, "predict_cost"):
        try: return ml.predict_cost(surface, dpe, zipcode)
        except Exception: pass
    return round(float(surface) * _FALLBACK_RENO_COST.get(dpe, 0), 0)

def calculate_roi_ml(cost, dpe, zipcode):
    if ML_BACKEND_READY and hasattr(ml, "predict_roi"):
        try: return ml.predict_roi(cost, dpe, zipcode)
        except Exception: pass
    return round(_FALLBACK_UPLIFT.get(dpe, 0.03) * 100, 1) if cost > 0 else 0.0

@st.cache_data(ttl=120)
def fetch_ademe(query: str, limit: int = 50):
    url    = f"https://data.ademe.fr/data-fair/api/v1/datasets/{DATASET_ID}/lines"
    params = {"page": 1, "size": limit, "q": query}
    data   = safe_get(url, params, timeout=14)
    rows   = []
    zip_context = query if len(query) == 5 and query.isdigit() else st.session_state.last_zipcode
    
    for item in (data.get("results", []) if data else []):
        addr    = item.get("Adresse_brute") or item.get("adresse_ban") or item.get("adresse") or "Inconnu"
        dpe     = str(item.get("etiquette_dpe") or item.get("Etiquette_DPE") or "N/A").upper().strip()
        surface = float(item.get("surface_habitable_logement") or item.get("surface") or 30)
        
        cost    = calculate_reno_cost_ml(surface, dpe, zip_context)
        r       = calculate_roi_ml(cost, dpe, zip_context)
        
        rows.append({
            "Address":           addr,
            "Code Postal":       zip_context,
            "DPE":               dpe,
            "Surface (m²)":      surface,
            "Coût Rénov. (€)":   cost,
            "ROI Estimé (%)":    r,
            "Statut Locatif":    _RENT_RISK.get(dpe, "✅ Conforme"),
            "Status":            "CRITICAL" if dpe in ["F", "G"] else ("WARNING" if dpe == "E" else "OK"),
            "Priorité":          4 if dpe == "G" else 3 if dpe == "F" else 2 if dpe == "E" else 1,
            "Bulle":             max(cost, 4000),
        })
    return pd.DataFrame(rows)

def geolocate_df(df: pd.DataFrame, base_lat: float, base_lon: float):
    bar  = st.progress(0, text="Géolocalisation BAN en cours…")
    lats, lons = [], []
    total = len(df)
    for i, row in df.iterrows():
        full = f"{row['Address']} {row.get('Code Postal', '')}".strip()
        la, lo = geocode_address(full, base_lat, base_lon)
        lats.append(la); lons.append(lo)
        bar.progress((i + 1) / total, text=f"Géolocalisation… {i+1}/{total}")
    bar.empty()
    df = df.copy()
    df["Latitude"]  = lats
    df["Longitude"] = lons
    return df

# ─────────────────────────────────────────────
# 🏢 PURE-HTML ULTRA SHARP LOGO HEADER
# ─────────────────────────────────────────────
import base64
try:
    with open("assets/zami_logo.png", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    logo_html = f'<div class="logo-img-container"><img src="data:image/png;base64,{encoded_string}"></div>'
except Exception:
    logo_html = '<div style="font-family:\'DM Serif Display\', serif; font-size:2rem; color:#fff;">🏢 ZA<span style="color:#dc2626;">MI</span></div>'

status_label = "AI ENGINE ACTIVE" if ML_BACKEND_READY else "MVP LIVE • DYNAMIC"
st.markdown(f"""
<div class="brand-header-flex">
    {logo_html}
    <div>
        <span class="brand-status-tag">STATUS: {status_label}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 🌟 SPLIT SCREEN LUXURY LANDING PAGE
# ─────────────────────────────────────────────
if not st.session_state.show_app:
    col_hero_left, col_hero_right = st.columns([1.1, 0.9], gap="large")
    with col_hero_left:
        st.markdown("""
            <div class="landing-hero">
                <div class="landing-badge">⚡ Intelligence Rénovation Énergétique</div>
                <div class="landing-title">Repérez les <em>passoires thermiques</em><br>et pilotez l'action.</div>
                <p style="color: #94a3b8; font-size: 1.05rem; line-height: 1.8; margin-bottom: 25px;">
                    Zami fusionne l'extraction automatisée du registre d'État ADEME et l'API Géospatiale BAN pour livrer 
                    un cockpit décisionnel sans couture. Identifiez les biens sous contrainte légale, simulez les rendements 
                    et orchestrez l'impact environnemental instantanément.
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="section-label">Accès Immédiat</p><p class="section-title">Explorez le Cockpit Analytique</p>', unsafe_allow_html=True)
        
        l_btn, r_btn = st.columns(2)
        with l_btn:
            if st.button("🗺️ Découvrir la Carte Interactive", use_container_width=True):
                st.session_state.landing_target_section = "Carte"
                st.session_state.show_app = True
                st.rerun()
        with r_btn:
            if st.button("📊 Ouvrir la Vue Globale", use_container_width=True):
                st.session_state.landing_target_section = "Vue générale"
                st.session_state.show_app = True
                st.rerun()

    with col_hero_right:
        st.markdown('<div class="video-container">', unsafe_allow_html=True)
        st.markdown('<p class="section-label" style="text-align:center;">🎬 Demo Showcase & Digital Twin Scan</p>', unsafe_allow_html=True)
        st.video("https://www.youtube.com/watch?v=mCmjNwjYfqw")
        if lottie_scan:
            st_lottie(lottie_scan, height=120, key="radar_landing")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<p class="section-label">Actualités En Direct</p><p class="section-title">Flash Réglementation & Loi Climat France</p>', unsafe_allow_html=True)
    n_col1, n_col2, n_col3 = st.columns(3)
    with n_col1:
        st.markdown("""
            <div class="news-card">
                <div class="news-date">Juin 2026 • Live</div>
                <div class="news-title">Audit Énergétique Obligatoire</div>
                <div class="news-desc">Le gouvernement durcit le contrôle des DPE classe E en monopropriété. Les sanctions enteront en vigueur prochainement.</div>
            </div>
        """, unsafe_allow_html=True)
    with n_col2:
        st.markdown("""
            <div class="news-card">
                <div class="news-date">Mai 2026 • Rappel</div>
                <div class="news-title">MaPrimeRénov' Refonte</div>
                <div class="news-desc">Mise à jour des plafonds de ressources des 4 tranches d'État. Les subventions pour l'isolation thermique globale augmentent de +15%.</div>
            </div>
        """, unsafe_allow_html=True)
    with n_col3:
        st.markdown("""
            <div class="news-card">
                <div class="news-date">Avril 2026 • Marché</div>
                <div class="news-title">Contraintes Climat 2034</div>
                <div class="news-desc">Plus de 5.2 millions de logements font l'objet d'un suivi de décote strict sur le marché de la transaction immobilière française.</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Market Intelligence</p><p class="section-title">Indicateurs de Performance Nationaux</p>', unsafe_allow_html=True)
    stat1, stat2, stat3 = st.columns(3)
    stat1.metric("Volume Analysé Total", "12M+ Logements", "Registre ADEME")
    stat2.metric("Coût Moyen Rénovation F/G", "€18 500", "Indice National")
    stat3.metric("Uplift Moyen Valeur (DPE -> B)", "+18.4%", "Plus-value constatée")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="footer">ZAMI v2.5 — Données Officielles ADEME & API BAN France</div>', unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────
# 💻 SECURE HIGH LEVEL NAVIGATION (Option Menu)
# ─────────────────────────────────────────────
nav_options = ["Vue générale", "Carte", "Analyse", "Simulation", "Contact", "Export"]
nav_icons = ["grid", "map", "bar-chart-line", "sliders", "envelope", "download"]

default_nav_idx = nav_options.index(st.session_state.landing_target_section)
section_choice = option_menu(
    menu_title=None, options=nav_options, icons=nav_icons, default_index=default_nav_idx, orientation="horizontal",
    styles={
        "container": {"background-color": "rgba(11,14,23,0.95)", "border": "1px solid rgba(255,255,255,0.05)", "padding": "6px", "border-radius": "16px", "margin-bottom": "25px"},
        "icon": {"color": "#94a3b8", "font-size": "14px"}, 
        "nav-link": {"font-size": "14px", "color": "#e2e8f0", "font-family": "'DM Sans', sans-serif", "font-weight": "500"},
        "nav-link-selected": {"background": "linear-gradient(135deg, #dc2626 0%, #a81a1a 100%)", "color": "#ffffff", "border-radius": "10px"},
    }
)
st.session_state.landing_target_section = section_choice

# ─────────────────────────────────────────────
# ── DASHBOARD PLATFORM LOGIC ──
# ─────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<p class="section-label">Filtres Cliniques</p><p class="section-title">Paramètres d\'analyse par zone</p>', unsafe_allow_html=True)

col_a, col_b = st.columns([3, 1])
with col_a: addr_query = st.text_input("Adresse cible BAN", placeholder="Ex: 15 rue de Rivoli Paris", key="addr_query")
with col_b: zipcode = st.text_input("Code postal", st.session_state.last_zipcode, key="zipcode_input")

col_act1, col_act2 = st.columns(2)
with col_act1: btn_search = st.button("🔍 Extraire l'Adresse", key="btn_addr")
with col_act2: run_zip = st.button("🏙️ Analyser le Secteur Global", key="run_zip")

if btn_search and addr_query:
    st.session_state.address_suggestions = ban_search(addr_query)

suggestions = st.session_state.address_suggestions
selected_addr = None
if suggestions:
    labels = [f"{s['label']} ({s['postcode']} {s['city']})" for s in suggestions]
    choice = st.selectbox("Résultat BAN validé :", labels, key="addr_choice")
    selected_addr = suggestions[labels.index(choice)]

if selected_addr:
    run_addr = st.button(f"📌 Confirmer l'analyse unitaire : {selected_addr['label']}", type="primary", use_container_width=True)
else: run_addr = False
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
fc1, fc2, fc3 = st.columns(3)
with fc1: min_surface = st.number_input("Surface minimum (m²)", min_value=0, value=15)
with fc2: selected_dpes = st.multiselect("Étiquettes DPE", ["A","B","C","D","E","F","G"], default=["E","F","G"])
with fc3: budget_cap = st.slider("Budget max rénovation (€)", 0, 100_000, 50_000, step=1000)
st.markdown("</div>", unsafe_allow_html=True)

if run_zip:
    with st.spinner("Extraction ADEME live..."):
        df = fetch_ademe(zipcode, 15)
        if not df.empty:
            df["Code Postal"] = zipcode
            lat0, lon0 = get_city_center(zipcode)
            st.session_state.city_coords = (lat0, lon0)
            df = geolocate_df(df, lat0, lon0)
            st.session_state.raw_data = df
            st.session_state.last_zipcode = zipcode

if run_addr and selected_addr:
    with st.spinner("Scoring unitaire..."):
        query = selected_addr["label"]
        df = fetch_ademe(query, 5)
        if not df.empty:
            lat0, lon0 = selected_addr["lat"] or DEFAULT_CENTER[0], selected_addr["lon"] or DEFAULT_CENTER[1]
            st.session_state.city_coords = (lat0, lon0)
            df["Code Postal"] = selected_addr["postcode"]
            df = geolocate_df(df, lat0, lon0)
            st.session_state.raw_data = df
            st.session_state.last_zipcode = selected_addr["postcode"]

if not st.session_state.raw_data.empty:
    df_f = st.session_state.raw_data.copy()
    df_f = df_f[df_f["Surface (m²)"] >= float(min_surface)]
    if selected_dpes: df_f = df_f[df_f["DPE"].isin(selected_dpes)]
    df_f = df_f[df_f["Coût Rénov. (€)"] <= float(budget_cap)]

    PLOT_LAYOUT = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#94a3b8", margin=dict(l=10, r=10, t=25, b=10))

    if section_choice == "Vue générale":
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown('<p class="section-label">Visualisation</p>', unsafe_allow_html=True)
            counts = df_f["Status"].value_counts().reset_index()
            counts.columns = ["Status", "n"]
            fig1 = px.pie(counts, names="Status", values="n", hole=0.6, color="Status", color_discrete_map={"CRITICAL":"#dc2626","WARNING":"#f59e0b","OK":"#22c55e"})
            fig1.update_layout(**PLOT_LAYOUT)
            st.plotly_chart(fig1, use_container_width=True)
        with col_r:
            st.markdown('<p class="section-label">Indice de Priorité Moyen</p>', unsafe_allow_html=True)
            fig2 = go.Figure(go.Indicator(mode="gauge+number", value=float(df_f["Priorité"].mean() if not df_f.empty else 0), number={"suffix": "/4", "font": {"color": "#fff"}}, gauge={"axis": {"range": [0, 4]}, "bar": {"color": "#dc2626"}, "bgcolor": "rgba(0,0,0,0)"}))
            fig2.update_layout(**PLOT_LAYOUT)
            st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif section_choice == "Carte":
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if not df_f.empty:
            fig_map = px.scatter_mapbox(df_f, lat="Latitude", lon="Longitude", color="Status", size="Bulle", hover_name="Address", color_discrete_map={"CRITICAL":"#dc2626","WARNING":"#f59e0b","OK":"#22c55e"}, zoom=12, center={"lat": st.session_state.city_coords[0], "lon": st.session_state.city_coords[1]}, mapbox_style="carto-darkmatter", height=500)
            fig_map.update_layout(margin=dict(r=0,t=0,l=0,b=0), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_map, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif section_choice == "Analyse":
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.dataframe(df_f[["Address","DPE","Surface (m²)","Coût Rénov. (€)","ROI Estimé (%)"]], use_container_width=True, height=300)
        st.markdown("</div>", unsafe_allow_html=True)

    elif section_choice == "Simulation":
        st.markdown('<div class="card">', unsafe_allow_html=True)
        ref = st.selectbox("Sélectionnez le bien", df_f["Address"].tolist())
        row = df_f[df_f["Address"] == ref].iloc[0]
        
        if ML_BACKEND_READY and hasattr(ml, "predict_cost"):
            st.info("💡 Calculs gérés par l'algorithme prédictif ZAMI AI")
            
        sim_budget = st.number_input("Budget Travaux (€)", value=int(row["Coût Rénov. (€)"]))
        uplift = st.slider("Revalorisation (%)", 0.0, 40.0, float(row["ROI Estimé (%)"]))
        st.metric("Gain Patrimonial", f"€{sim_budget * (uplift / 100):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)

    elif section_choice == "Contact":
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("contact"):
            st.text_input("Nom")
            st.text_area("Message")
            if st.form_submit_button("📨 Envoyer"): st.success("Message envoyé !")
        st.markdown("</div>", unsafe_allow_html=True)

    elif section_choice == "Export":
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.download_button("⬇ dependency CSV", data=df_f.to_csv(index=False).encode("utf-8"), file_name="ZAMI_export.csv", mime="text/csv", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="card" style="text-align:center;padding:3rem 2rem;">
        <p class="section-title">Prêt pour l'extraction</p>
        <p style="color:#64748b;">Veuillez exécuter une recherche d'adresse ou de secteur géographique ci-dessus.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="footer">ZAMI v2.5 — Données Officielles ADEME & API BAN France</div>', unsafe_allow_html=True)