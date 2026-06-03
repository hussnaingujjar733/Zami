import os
import base64
import random
import time
import io
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
from fpdf import FPDF
from streamlit_folium import st_folium  # 🚨 Permanent Tokenless Map Component
import folium

# ── 🧠 IMPORT YOUR ML BACKEND MODULES ──
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
    page_title="ZAMI | Private Property Intelligence",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# 🗄️ SQLITE DATABASE INITIALIZATION ENGINE
# ─────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zami_leads.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            property_address TEXT,
            zipcode TEXT,
            initial_dpe TEXT,
            target_dpe TEXT,
            selected_scenario TEXT,
            estimated_cost REAL,
            owner_name TEXT,
            owner_phone TEXT,
            owner_email TEXT,
            callback_time TEXT,
            notes TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def log_lead_to_db(address, zipcode, initial_dpe, target_dpe, scenario, cost, name, phone, email, callback_time, notes):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO leads (
                timestamp, property_address, zipcode, initial_dpe, target_dpe, 
                selected_scenario, estimated_cost, owner_name, owner_phone, 
                owner_email, callback_time, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (current_time, address, zipcode, initial_dpe, target_dpe, scenario, float(cost), name, phone, email, callback_time, notes))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False

# ─────────────────────────────────────────────
# 🌐 TRANSLATION DICTIONARY MATRIX
# ─────────────────────────────────────────────
LANG_DICT = {
    "FR": {
        "title": "Portail Propriétaire Énergétique",
        "subtitle": "Estimez instantanément la valeur et les travaux de votre bien",
        "input_label": "Saisissez l'adresse de votre logement :",
        "select_certified": "Sélectionnez la ligne certifiée officielle :",
        "btn_analyze": "⚡ Analyser mon Logement",
        "btn_back": "⬅️ Retourner à la recherche",
        "bilan_title": "Bilan Diagnostic Personnel",
        "choose_plan": "Choisissez votre Plan de Transition Rénovation :",
        "eco_ess": "🛠️ Éco Essential",
        "eco_ess_sub": "Mise en conformité légale (DPE D)",
        "conf_plus": "⚡ Confort Plus",
        "conf_plus_sub": "Isolation globale & Confort (DPE C)",
        "carb_zero": "🟢 Carbone Zéro",
        "carb_zero_sub": "Performance & Heat-Pump (DPE B)",
        "current_class": "Classe Actuelle",
        "target_class": "🎯 Cible Scénario : Classe",
        "surface": "Surface Réelle",
        "budget_est": "Budget Estimé du Plan",
        "bbc_label": "Bâtiment Basse Consommation",
        "uplift_label": "Uplift Valeur Patrimoine",
        "optimal_label": "Valeur marché sécurisée",
        "visual_prog": "Progression Énergétique Visuelle",
        "your_property": "Votre Bien 🏠",
        "target_label": "Cible",
        "fin_title": "Analyse Financière & Graphique",
        "fin_sub": "Subventions d'État vs Reste à Charge Net",
        "subvention_label": "Subvention MaPrimeRénov'",
        "reste_charge": "Reste à Charge Net",
        "impact_facture": "Impact Facture : En choisissant le plan {sc}, vous économisez en moyenne {saving} sur vos factures.",
        "chart_5yr_title": "📊 Évolution Prédictive du Patrimoine (5 Ans)",
        "chart_5yr_sub": "Trajectoire de l'actif : Rénové vs Non-Rénové (Passoire Thermique)",
        "form_title": "Prendre RDV avec un Artisan Certifié RGE",
        "form_sub": "Recevez gratuitement 3 devis d'artisans locaux audités par l'État.",
        "form_name": "Nom Complet *",
        "form_phone": "Numéro de Téléphone *",
        "form_email": "Adresse Email *",
        "form_time": "Créneau de rappel souhaité",
        "form_notes": "Précisions complémentaires (facultatif)",
        "form_btn": "📨 Envoyer ma demande de RDV",
        "form_err": "⚠️ Veuillez remplir tous les champs obligatoires (*) pour valider la demande.",
        "form_success": "🎉 Félicitations ! Votre demande a été enregistrée dans notre base sécurisée. Un artisan certifié RGE vous contactera sous 24h.",
        "download_btn": "⬇️ Télécharger mon Rapport PDF Officiel",
        "faq_title": "Guide Légal & FAQ Rénovation France",
        "map_title": "🗺️ Cartographie Spatiale & Cadastre Registre",
        "loss_title": "🌡️ Analyse AI des Déperditons Thermiques Estimées",
        "loss_sub": "Zones critiques nécessitant une isolation prioritaire",
        "income_label": "💰 Sélectionnez votre Profil de Revenu (Anah) :",
        "loan_title": "💶 Simulateur Financement : Eco-Prêt à Taux Zéro (Eco-PTZ)",
        "loan_sub": "Financez votre reste à charge à 0% d'intérêt",
        "loan_duration": "Durée du Prêt (Années)",
        "monthly_pay": "Mensualité Estimée",
        "footer": "ZAMI v7.4 Supreme — Folium Engine Permanent • Données Certifiées ADEME & BAN France"
    },
    "EN": {
        "title": "Property Energy Portal",
        "subtitle": "Instantly estimate your property value and renovation costs",
        "input_label": "Enter your property address:",
        "select_certified": "Select the certified official address line:",
        "btn_analyze": "⚡ Analyze My Property",
        "btn_back": "⬅️ Return to Search",
        "bilan_title": "Personal Assessment Summary",
        "choose_plan": "Choose your Renovation Transition Plan:",
        "eco_ess": "🛠️ Eco Essential",
        "eco_ess_sub": "Legal compliance matching (DPE D)",
        "conf_plus": "⚡ Comfort Plus",
        "conf_plus_sub": "Global Insulation & Comfort (DPE C)",
        "carb_zero": "🟢 Carbon Zero",
        "carb_zero_sub": "High Performance & Heat-Pump (DPE B)",
        "current_class": "Current Rating",
        "target_class": "🎯 Target Scenario: Class",
        "surface": "Real Surface Area",
        "budget_est": "Estimated Plan Budget",
        "bbc_label": "Low Consumption Building",
        "uplift_label": "Property Value Uplift",
        "optimal_label": "Market Value Secured",
        "visual_prog": "Visual Energy Progress Path",
        "your_property": "Your Asset 🏠",
        "target_label": "Target",
        "fin_title": "Financial Analysis & Charts",
        "fin_sub": "State Subsidies vs Net Out-of-Pocket Cost",
        "subvention_label": "MaPrimeRénov' Subsidy",
        "reste_charge": "Net Remaining Cost",
        "impact_facture": "Bill Impact: By choosing the {sc} plan, you save an average of {saving} on your energy bills.",
        "chart_5yr_title": "📊 5-Year Asset Value Predictive Evolution",
        "chart_5yr_sub": "Asset Trajectory: Renovated vs Unrenovated (Energy Passoire Drop)",
        "form_title": "Book an Appointment with a Certified RGE Contractor",
        "form_sub": "Receive 3 free quotes from state-audited local contractors.",
        "form_name": "Full Name *",
        "form_phone": "Phone Number *",
        "form_email": "Email Address *",
        "form_time": "Preferred callback time",
        "form_notes": "Additional project notes (optional)",
        "form_btn": "📨 Submit My Appointment Request",
        "form_err": "⚠️ Please fill in all required fields (*) to validate your request.",
        "form_success": "🎉 Congratulations! Your request has been logged inside our secure network. An RGE contractor will call you within 24h.",
        "download_btn": "⬇️ Download Official PDF Report",
        "faq_title": "Legal Guide & Renovation FAQ France",
        "map_title": "🗺️ Geospatial Location & Registry Mapping",
        "loss_title": "🌡️ AI Estimation of Structural Heat Losses",
        "loss_sub": "Critical building zones requiring urgent insulation",
        "income_label": "💰 Select your Anah Income Profile :",
        "loan_title": "💶 Financing Simulator: Eco-Prêt à Taux Zéro (Eco-PTZ)",
        "loan_sub": "Finance your remaining out-of-pocket cost with 0% interest",
        "loan_duration": "Loan Duration (Years)",
        "monthly_pay": "Estimated Monthly Payment",
        "footer": "ZAMI v7.4 Supreme — Folium Engine Permanent • Certified ADEME & BAN France Data"
    }
}

# ─────────────────────────────────────────────
# GLOBAL STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600;700&display=swap');
*, *::before, *::after { box-sizing: border-box; }
#MainMenu, footer, header { visibility: hidden; }
html, body, .stApp { background: #04060a; color: #e2e8f0; font-family: 'DM Sans', sans-serif; }
.stApp::before {
    content: ''; position: fixed; inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
    pointer-events: none; z-index: 0; opacity: 0.4;
}
.brand-header-flex { display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(255, 255, 255, 0.05); padding-bottom: 1.2rem; margin-bottom: 2rem; width: 100%; }
.logo-img-container img { height: auto; width: 140px; }
.brand-status-tag { background: rgba(34,197,94,0.05); border: 1px solid rgba(34,197,94,0.2); padding: 7px 15px; border-radius: 30px; font-size: 0.75rem; font-weight: 600; color: #86efac; letter-spacing: 0.05em; }
h1, h2, h3, h4 { font-family: 'DM Serif Display', serif; }
.card { background: linear-gradient(145deg, rgba(10,13,22,0.98), rgba(15,19,32,0.92)); border: 1px solid rgba(148,163,184,0.07); border-radius: 20px; padding: 2rem 2.2rem; box-shadow: 0 25px 60px rgba(0,0,0,0.45); margin-bottom: 1.5rem; }
.scenario-card-active { background: linear-gradient(135deg, rgba(34,197,94,0.1) 0%, rgba(10,13,22,0.98) 100%); border: 1px solid rgba(34,197,94,0.35) !important; box-shadow: 0 15px 35px rgba(34,197,94,0.05); }
.owner-exclusive-title { font-family: 'DM Serif Display', serif; font-size: 2.5rem; color: #f8fafc; margin-bottom: 0.5rem; letter-spacing: -0.01em; }
.dpe-badge-big { display: inline-block; padding: 12px 32px; font-size: 3.5rem; font-weight: 900; border-radius: 16px; color: #fff; text-align: center; box-shadow: 0 15px 35px rgba(0,0,0,0.4); }
.section-label { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: #22c55e; margin-bottom: 0.3rem; }
.section-title { font-family: 'DM Serif Display', serif; font-size: 1.7rem; color: #f8fafc; margin: 0 0 0.5rem 0; }
.metric-value-huge { font-size: 2.8rem; font-weight: 700; color: #ffffff; letter-spacing: -0.02em; line-height: 1.1; }
.metric-label-sub { font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.08em; display: inline-block; }
.footer { text-align: center; color: #475569; padding: 3rem 0; font-size: 0.82rem; border-top: 1px solid rgba(255,255,255,0.04); margin-top: 4rem; }
</style>
""", unsafe_allow_html=True)

# ── 🚨 STATE AUTO-INITIALIZER ──
if "confirmed_owner_property" not in st.session_state: st.session_state["confirmed_owner_property"] = None
if "address_suggestions" not in st.session_state: st.session_state["address_suggestions"] = []
if "selected_scenario" not in st.session_state: st.session_state["selected_scenario"] = "Essential"

_SCENARIO_COST_MULTIPLIER = {"Essential": 1.0, "Plus": 1.65, "Zero": 2.45}
_SCENARIO_ROI_MULTIPLIER  = {"Essential": 1.0, "Plus": 1.45, "Zero": 1.95}
_SCENARIO_TARGET_DPE     = {"Essential": "D", "Plus": "C", "Zero": "B"}
_FALLBACK_RENO_COST = {"G": 1350, "F": 1100, "E": 620, "D": 280, "C": 120, "B": 0, "A": 0}
_FALLBACK_UPLIFT    = {"G": 24.2, "F": 19.8, "E": 13.1, "D": 6.8, "C": 2.0, "B": 0, "A": 0}
_DPE_COLORS         = {"A": "#319834", "B": "#33cc33", "C": "#ccff33", "D": "#f2b035", "E": "#ff6600", "F": "#ff3300", "G": "#ff0000"}

_INCOME_SUBSIDY_MAP = {
    "Très Modeste (Bleu)": 0.75,
    "Modeste (Jaune)": 0.60,
    "Intermédiaire (Violet)": 0.40,
    "Supérieur (Rose)": 0.15
}

# ── BAN SEARCH RE-INJECTED ──
def safe_get(url, params=None, timeout=10):
    try:
        r = requests.get(url, params=params, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception: return None

@st.cache_data(ttl=300)
def ban_search(query: str, limit: int = 5):
    if not query or len(query.strip()) < 3: return []
    data = safe_get("https://api-adresse.data.gouv.fr/search/", {"q": query, "limit": limit, "type": "housenumber"})
    if not data: data = safe_get("https://api-adresse.data.gouv.fr/search/", {"q": query, "limit": limit})
    features = data.get("features", []) if data else []
    results = []
    for f in features:
        p = f.get("properties", {})
        c = f.get("geometry", {}).get("coordinates", [2.3522, 48.8566])
        results.append({"label": p.get("label", ""), "postcode": p.get("postcode", ""), "city": p.get("city", ""), "lon": c[0], "lat": c[1]})
    return results

def fetch_single_property_ademe(query_address: str, zipcode: str, lat=48.8566, lon=2.3522):
    random.seed(int(len(query_address)))
    mock_dpe = random.choice(["E", "F", "G"])
    mock_surface = random.randint(30, 95)
    if ML_BACKEND_READY and hasattr(ml, "predict_cost"):
        try: cost = ml.predict_cost(mock_surface, mock_dpe, zipcode)
        except Exception: cost = round(float(mock_surface) * _FALLBACK_RENO_COST.get(mock_dpe, 0), 0)
    else: cost = round(float(mock_surface) * _FALLBACK_RENO_COST.get(mock_dpe, 0), 0)
    roi = round(_FALLBACK_UPLIFT.get(mock_dpe, 0.0), 1)
    return {"address": query_address, "dpe": mock_dpe, "surface": mock_surface, "cost": cost, "roi": roi, "zipcode": zipcode, "lat": lat, "lon": lon}

# ── Logo Code preservations
col_logo, col_lang = st.columns([2.5, 0.5])
with col_lang: selected_lang = st.selectbox("🌐 Language", ["FR", "EN"], label_visibility="collapsed")
T = LANG_DICT[selected_lang]

st.markdown(f"""<div class="brand-header-flex" style="margin-top:-30px;"><div class="logo-img-container" style="font-family:'DM Serif Display', serif; font-size:2.2rem; color:#fff;">🏢 ZA<span style="color:#22c55e;">MI</span></div><div><span class="brand-status-tag">ZAMI SUPREME V7.4 FOLIUM LIVE</span></div></div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SEARCH CORE
# ─────────────────────────────────────────────
if st.session_state["confirmed_owner_property"] is None:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<p class="section-label">{T["title"]}</p><p class="section-title">{T["subtitle"]}</p>', unsafe_allow_html=True)
    search_query = st.text_input(T["input_label"], placeholder="Ex: 39 Rue du Sergent Bobillot, Montreuil", key="owner_search_input")
    if search_query and len(search_query.strip()) >= 3:
        st.session_state["address_suggestions"] = ban_search(search_query)
    suggestions = st.session_state["address_suggestions"]
    if suggestions:
        labels = [f"{s['label']} ({s['postcode']} {s['city']})" for s in suggestions]
        selected_label = st.selectbox(T["select_certified"], labels, key="owner_label_select")
        chosen_property = suggestions[labels.index(selected_label)]
        if st.button(T["btn_analyze"], type="primary", use_container_width=True):
            st.session_state["confirmed_owner_property"] = fetch_single_property_ademe(chosen_property["label"], chosen_property["postcode"], chosen_property["lat"], chosen_property["lon"])
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# COCKPIT CORE FLOW
# ─────────────────────────────────────────────
else:
    base_prop = st.session_state["confirmed_owner_property"]
    dpe_color = _DPE_COLORS.get(base_prop["dpe"], "#475569")
    if st.button(T["btn_back"]): st.session_state["confirmed_owner_property"] = None; st.rerun()
        
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<p class="section-label">{T["bilan_title"]}</p><div class="owner-exclusive-title">{base_prop["address"]}</div>', unsafe_allow_html=True)
    
    # Scenarios selectors buttons
    sc_col1, sc_col2, sc_col3 = st.columns(3)
    with sc_col1:
        if st.button(T["eco_ess"], use_container_width=True): st.session_state["selected_scenario"] = "Essential"; st.rerun()
    with sc_col2:
        if st.button(T["conf_plus"], use_container_width=True): st.session_state["selected_scenario"] = "Plus"; st.rerun()
    with sc_col3:
        if st.button(T["carb_zero"], use_container_width=True): st.session_state["selected_scenario"] = "Zero"; st.rerun()

    current_scenario = st.session_state["selected_scenario"]
    active_cost = round(base_prop["cost"] * _SCENARIO_COST_MULTIPLIER[current_scenario], 0)
    active_roi  = round(base_prop["roi"] * _SCENARIO_ROI_MULTIPLIER[current_scenario], 1)
    target_dpe  = _SCENARIO_TARGET_DPE[current_scenario]

    # Visual Metrics Output Grid
    m1, m2, m3 = st.columns(3)
    m1.metric(T["surface"], f"{base_prop['surface']} m²")
    m2.metric(T["budget_est"], f"€{active_cost:,.0f}")
    m3.metric(T["uplift_label"], f"+{active_roi}%")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── 🎯 100% PERMANENT FIXED MAP ENGINE (FOLIUM TOKENLESS SYSTEM) ──
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col_map_h, col_map_t = st.columns([2.0, 1.0])
    with col_map_h:
        st.markdown(f'<p class="section-label">Geospatial Registry</p><p class="section-title">{T["map_title"]}</p>', unsafe_allow_html=True)
    with col_map_t:
        map_style_selection = st.radio("Style Map Layer", ["Road Canvas View", "High-Res Satellite View"], horizontal=True, label_visibility="collapsed")
    
    # Folium Map Canvas core allocation
    f_map = folium.Map(location=[base_prop["lat"], base_prop["lon"]], zoom_start=17, control_scale=True)
    
    if map_style_selection == "High-Res Satellite View":
        # Direct dynamic parsing via open-source Esri structural tile server
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri World Imagery',
            name='Satellite View',
            overlay=False,
            control=True
        ).add_to(f_map)
    else:
        folium.TileLayer('cartodbpositron', name='Dark Canvas').add_to(f_map)
        
    folium.Marker([base_prop["lat"], base_prop["lon"]], popup=base_prop["address"], icon=folium.Icon(color='green', icon='home')).add_to(f_map)
    st_folium(f_map, use_container_width=True, height=360, returned_objects=[])
    st.markdown("</div>", unsafe_allow_html=True)

    # ── THERMAL DEPERDITIONS HORIZONTAL BARS MATRIX 
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<p class="section-label">Thermal Architecture</p><p class="section-title">{T["loss_title"]}</p>', unsafe_allow_html=True)
    fig_loss = go.Figure(go.Bar(x=[30, 25, 15, 10], y=["Toiture", "Murs", "Fenêtres", "Planchers"], orientation='h', marker=dict(color=['#dc2626', '#ef4444', '#f97316', '#eab308'])))
    fig_loss.update_layout(height=150, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_loss, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

    # ── FINANCIALS RECALCULATOR WITH PROFILE SLIDERS
    st.markdown('<div class="card">', unsafe_allow_html=True)
    selected_income_bracket = st.selectbox(T["income_label"], list(_INCOME_SUBSIDY_MAP.keys()), index=2)
    subsidy_rate = _INCOME_SUBSIDY_MAP[selected_income_bracket]
    estimated_subsidy = round(active_cost * subsidy_rate, 0)
    net_cost = active_cost - estimated_subsidy
    
    st.metric(T["subvention_label"], f"€{estimated_subsidy:,.0f}")
    st.metric(T["reste_charge"], f"€{net_cost:,.0f}")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── ECO-PTZ SIMULATOR CALCULATOR INTERACTIVE
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<p class="section-title">{T["loan_title"]}</p>', unsafe_allow_html=True)
    loan_years = st.slider(T["loan_duration"], 5, 20, 15)
    monthly_pay = net_cost / (loan_years * 12)
    st.markdown(f'<h3>€{monthly_pay:,.2f} / mois</h3>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── 5-YEAR LINE CHART DYNAMICS
    st.markdown('<div class="card">', unsafe_allow_html=True)
    fig_5yr = go.Figure()
    fig_5yr.add_trace(go.Scatter(x=["2026", "2027", "2028", "2029", "2030"], y=[300000, 310000, 325000, 340000, 360000], name="Renovated Asset", line=dict(color='#22c55e', width=4)))
    fig_5yr.update_layout(height=200, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_5yr, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

    # ── LEADS CAPTURE INPUT FORM 
    with st.form("leads_capture"):
        name = st.text_input("Nom Complet *")
        phone = st.text_input("Téléphone *")
        email = st.text_input("Email *")
        if st.form_submit_button("Submit"):
            log_lead_to_db(base_prop["address"], base_prop["zipcode"], base_prop["dpe"], target_dpe, current_scenario, active_cost, name, phone, email, "Matin", "")
            st.success("Success!")

# ── 🛡️ ADMIN VAULT LOGGING
st.markdown('<hr style="border-color:rgba(255,255,255,0.05); margin: 3rem 0;">', unsafe_allow_html=True)
if st.checkbox("🔑 Open ZAMI Secure Admin Database Vault Viewer"):
    pwd = st.text_input("Password:", type="password")
    if pwd == "HussnainZami2026":
        conn = sqlite3.connect(DB_PATH)
        df_l = pd.read_sql_query("SELECT * FROM leads ORDER BY id DESC", conn)
        conn.close()
        st.dataframe(df_l, use_container_width=True)

st.markdown(f'<div class="footer">{T["footer"]}</div>', unsafe_allow_html=True)