import os
import base64
import random
import io
import sqlite3
import requests
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from fpdf import FPDF
from streamlit_folium import st_folium
import folium

# ── ⚡ IMPORT REFACTORED COMMERCIAL ENTERPRISE ENGINE MODULES ──
import utils_styles
import utils_db
import utils_charts

try:
    import ml_engine as ml
    ML_BACKEND_READY = True
except ImportError:
    ML_BACKEND_READY = False

try:
    from ademe_api import lookup_dpe_by_address
    ADEME_API_READY = True
except ImportError:
    ADEME_API_READY = False

# Boot systems databases
utils_db.init_db()

# Run Trillion-Dollar Style Injection Layers
utils_styles.inject_premium_styles()

# ─────────────────────────────────────────────
# STATE INTERFACE STORAGE ROUTING
# ─────────────────────────────────────────────
if "logged_in_user_id" not in st.session_state: st.session_state["logged_in_user_id"] = None
if "logged_in_username" not in st.session_state: st.session_state["logged_in_username"] = None
if "confirmed_owner_property" not in st.session_state: st.session_state["confirmed_owner_property"] = None
if "address_suggestions" not in st.session_state: st.session_state["address_suggestions"] = []
if "selected_scenario" not in st.session_state: st.session_state["selected_scenario"] = "Essential"

# Global Variables setup
_SCENARIO_COST_MULTIPLIER = {"Essential": 1.0, "Plus": 1.65, "Zero": 2.45}
_SCENARIO_ROI_MULTIPLIER  = {"Essential": 1.0, "Plus": 1.45, "Zero": 1.95}
_SCENARIO_TARGET_DPE     = {"Essential": "D", "Plus": "C", "Zero": "B"}
_FALLBACK_RENO_COST = {"G": 1350, "F": 1100, "E": 620, "D": 280, "C": 120, "B": 0, "A": 0}
_FALLBACK_UPLIFT    = {"G": 24.2, "F": 19.8, "E": 13.1, "D": 6.8, "C": 2.0, "B": 0, "A": 0}
_DPE_COLORS         = {"A": "#319834", "B": "#33cc33", "C": "#ccff33", "D": "#f2b035", "E": "#ff6600", "F": "#ff3300", "G": "#ff0000"}
_INCOME_SUBSIDY_MAP = {"Très Modeste (Bleu)": 0.75, "Modeste (Jaune)": 0.60, "Intermédiaire (Violet)": 0.40, "Supérieur (Rose)": 0.15}

def safe_get(url, params=None):
    try:
        r = requests.get(url, params=params, timeout=10)
        return r.json()
    except Exception: return None

def ban_search(query: str, limit: int = 5):
    if not query or len(query.strip()) < 3: return []
    data = safe_get("https://api-adresse.data.gouv.fr/search/", {"q": query, "limit": limit})
    features = data.get("features", []) if data else []
    results = []
    for f in features:
        p = f.get("properties", {})
        c = f.get("geometry", {}).get("coordinates", [2.3522, 48.8566])
        results.append({"label": p.get("label", ""), "postcode": p.get("postcode", ""), "city": p.get("city", ""), "lon": c[0], "lat": c[1]})
    return results

def fetch_single_property_ademe(query_address: str, zipcode: str, lat=48.8566, lon=2.3522):
    """
    Real ADEME DPE lookup — replaces the old random mock data.
    Fetches official certified DPE records from ADEME Open Data (25M+ records).
    Falls back to intelligent zone-based estimate if address not found.
    """
    if ADEME_API_READY:
        return lookup_dpe_by_address(
            address_label=query_address,
            zipcode=zipcode,
            lat=lat,
            lon=lon,
            fallback_cost_map=_FALLBACK_RENO_COST,
            fallback_uplift_map=_FALLBACK_UPLIFT,
        )
    # Emergency fallback if ademe_api.py not present (keeps app running)
    dpe_by_region = {"75": "E", "92": "E", "93": "F", "94": "E", "69": "D", "13": "D", "31": "D"}
    region = str(zipcode)[:2]
    dpe = dpe_by_region.get(region, "E")
    surface = 62.0 if region == "75" else 75.0
    cost = round(surface * _FALLBACK_RENO_COST.get(dpe, 620), 0)
    roi  = _FALLBACK_UPLIFT.get(dpe, 13.1)
    return {
        "address": query_address, "dpe": dpe, "surface": surface,
        "cost": cost, "roi": roi, "zipcode": zipcode, "lat": lat, "lon": lon,
        "source": "FALLBACK_ZONALE", "data_found": False,
    }

# Language translations matrix
LANG_DICT = {
    "FR": {
        "title": "Portail Propriétaire Énergétique", "subtitle": "Estimez instantanément la valeur et les travaux de votre bien", 
        "input_label": "Saisissez l'adresse de votre logement :", "select_certified": "Sélectionnez l'adresse certifiée BAN France :", 
        "btn_analyze": "⚡ Lancer l'Analyse Temporelle AI", "btn_back": "⬅️ Nouvelle recherche", "bilan_title": "BILAN PATRIMONIAL EXCLUSIF", 
        "choose_plan": "PLAN DE CONFIGURATION ÉNERGÉTIQUE", "eco_ess": "🛠️ Éco Essential", "eco_ess_sub": "DPE D • Conformité Légale 2026", 
        "conf_plus": "⚡ Confort Plus", "conf_plus_sub": "DPE C • Isolation Enveloppe Globale", "carb_zero": "🟢 Carbone Zéro", 
        "carb_zero_sub": "DPE B • Décarbonation Pompe à Chaleur", "current_class": "Classe Initiale", "target_class": "🎯 Objectif Scénario", 
        "surface": "Surface Habitable", "budget_est": "Investissement Global", "uplift_label": "Uplift Marché Estimé", "visual_prog": "Vecteur de Progression Énergétique", 
        "your_property": "Actif 🏠", "target_label": "Cible", "fin_title": "Analyse d'Ingénierie Financière", "fin_sub": "Subventions Publiques vs Reste à Charge Net", 
        "subvention_label": "Aides MaPrimeRénov'", "reste_charge": "Reste à Charge Net", "impact_facture": "Impact Facture: Le plan {sc} génère une économie moyenne de {saving} par an sur vos factures de fluide.", 
        "chart_5yr_title": "📊 Évolution Prédictive de l'Actif (2026 - 2031)", "chart_5yr_sub": "Modélisation de la trajectoire patrimoniale : Stratégie de rénovation vs Obsolescence Passoire Thermique", 
        "form_title": "Mise en Relation avec un Gestionnaire RGE Audit", "form_sub": "Planifiez une visite technique sur site pour valider l'éligibilité aux aides d'État.", 
        "form_name": "Nom Complet *", "form_phone": "Numéro de Téléphone *", "form_email": "Adresse Email Professionnelle *", "form_time": "Créneau de rappel", 
        "form_notes": "Notes de projet particulières (facultatif)", "form_btn": "📨 Transmettre le Dossier Technique", "form_err": "⚠️ Paramètres requis manquants.", 
        "form_success": "🎉 Dossier sécurisé consigné dans le registre. Un consultant RGE prendra contact sous 24h.", "download_btn": "⬇️ Exporter le Rapport d'Audit Certifié (PDF)", 
        "map_title": "🗺️ Cadastre Registre & Géolocalisation Spatiale", "loss_title": "🌡️ Diagnostic Prédictif des Déperditons Thermiques Estimées", 
        "income_label": "💰 Profil de Revenu Fiscal de Référence (Anah) :", "loan_title": "💶 Simulateur d'Effet de Levier Financier : Eco-PTZ Framework", 
        "loan_duration": "Maturité d'Amortissement (Années)", "monthly_pay": "Mensualité Arbitrée (0% Interest)", "footer": "ZAMI PRO v8.3 Supreme Freemium — Header Architecture Aligned • Baseline ADEME Cloud Backend"
    },
    "EN": {
        "title": "Energy Portal Platform", "subtitle": "Track, simulate and view certified real-estate properties free", 
        "input_label": "Enter certified property address:", "select_certified": "Select official line from BAN France Registry:", 
        "btn_analyze": "⚡ Execute AI Temporal Assessment", "btn_back": "⬅️ Return to Search Canvas", "bilan_title": "EXCLUSIVE PATRIMONIAL AUDIT", 
        "choose_plan": "ENERGY SCOPE MATRIX CONFIGURATION", "eco_ess": "🛠️ Eco Essential", "eco_ess_sub": "DPE D • Legal Compliance Bounds", 
        "conf_plus": "⚡ Comfort Plus", "conf_plus_sub": "DPE C • Envelope Thermal Insulation", "carb_zero": "🟢 Carbon Zero", 
        "carb_zero_sub": "High Performance & Heat-Pump (DPE B)", "current_class": "Initial Rating", "target_class": "🎯 Target Scenario", 
        "surface": "Surface Area", "budget_est": "Budget Estimate", "uplift_label": "Asset Value Growth", "visual_prog": "Energy Progression Flow Chart View", 
        "your_property": "Your Asset 🏠", "target_label": "Target", "fin_title": "Capital Deployment Analysis Charting", 
        "fin_sub": "State Financing Allocations vs Net Capital Out", "subvention_label": "State Grants Matrix", "reste_charge": "Net remaining", 
        "impact_facture": "Energy Invoices Vector: Choosing plan {sc} yields ~{saving} annual savings matrix on utilities.", 
        "chart_5yr_title": "📊 5-Year Asset Value Predictive Evolution", "chart_5yr_sub": "Asset Trajectory Mapping Layout", 
        "form_title": "Book an Appointment with a Certified RGE Contractor", "form_sub": "Receive 3 free quotes from state-audited local contractors.", 
        "form_name": "Full Name *", "form_phone": "Phone Number *", "form_email": "Corporate Email Address *", "form_time": "Callback window preference", 
        "form_notes": "Project specifications notes (optional)", "form_btn": "📨 Transmit Technical File Folder", "form_err": "⚠️ Required parameters missing initialization.", 
        "form_success": "🎉 Technical file safely logged. An audited RGE consultant will call you within 24h.", "download_btn": "⬇️ Export Certified Audit Report Ledger (PDF)", 
        "map_title": "🗺️ Geospatial Location Mapping & Registry Registry", "loss_title": "🌡️ AI Estimation of Structural Heat Losses", 
        "income_label": "💰 Select Fiscal Revenue Profile (Anah Bands):", "loan_title": "💶 Capital Leverage Simulator: Eco-PTZ 0% Interest Framework", 
        "loan_duration": "Amortization Matrix Maturity (Years)", "monthly_pay": "Estimated Monthly Installment (0% Interest)", "footer": "ZAMI PRO v8.3 Supreme Freemium — Header Architecture Aligned • Baseline ADEME Core"
    }
}

def generate_zami_pdf_bytes(prop_details, sc, target_dpe, cost, net):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(5, 7, 12)
    pdf.rect(0, 0, 210, 45, 'F')
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(255, 255, 255)
    pdf.text(15, 28, "ZAMI | COCKPIT REPORT V8.3")
    return pdf.output()

# ─────────────────────────────────────────────
# 🏔️ TRILLION-DOLLAR SYMMETRICAL HEADER & NAVBAR ARCHITECTURE (FIXED ALIGNMENT)
# ─────────────────────────────────────────────
col_left_brand, col_right_actions = st.columns([1.6, 1.4])

# 🏢 Left Grid Area: Absolute Logo Presentation
with col_left_brand:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(base_dir, "assets", "zami_logo.png")
    
    if os.path.exists(logo_path):
        try:
            with open(logo_path, "rb") as img_f:
                logo_html = f'<div class="logo-img-container" style="margin-top:-10px; margin-left:-10px;"><img src="data:image/png;base64,{base64.b64encode(img_f.read()).decode()}" style="height:auto; width:150px;"></div>'
        except Exception:
            logo_html = '<div style="font-family:\'SF Pro Display\', sans-serif; font-size:2.4rem; color:#fff; font-weight:900; letter-spacing:-0.03em; margin-top:-15px;">🏢 ZA<span style="color:#22c55e;">MI</span><span style="color:#22c55e; font-size:1rem; font-weight:600; margin-left:4px; vertical-align:super;">PRO</span></div>'
    else:
        logo_html = '<div style="font-family:\'SF Pro Display\', sans-serif; font-size:2.4rem; color:#fff; font-weight:900; letter-spacing:-0.03em; margin-top:-15px;">🏢 ZA<span style="color:#22c55e;">MI</span><span style="color:#22c55e; font-size:1rem; font-weight:600; margin-left:4px; vertical-align:super;">PRO</span></div>'
        
    st.markdown(logo_html, unsafe_allow_html=True)

# 🎛️ Right Grid Area: Symmetrical Integration of Lang Select + Member Expander
with col_right_actions:
    # Creating micro inner sub-columns to line up Lang Dropdown and Account Gate side-by-side
    sub_col_lang, sub_col_auth = st.columns([0.4, 0.6])
    
    with sub_col_lang:
        selected_lang = st.selectbox("🌐 Language", ["FR", "EN"], label_visibility="collapsed", key="global_lang_selector")
        T = LANG_DICT[selected_lang]
        
    with sub_col_auth:
        if st.session_state["logged_in_user_id"] is None:
            with st.expander("👤 Workspace Account", expanded=False):
                auth_mode = st.radio("Gate Mode", ["Login", "Sign Up"], horizontal=True, label_visibility="collapsed", key="nav_auth_mode")
                u_input = st.text_input("Username", key="main_user_input")
                e_input = st.text_input("Email", key="main_mail_input") if auth_mode == "Sign Up" else None
                p_input = st.text_input("Password", type="password", key="main_pwd_input")
                
                if st.button("Verify Identity", use_container_width=True, type="primary", key="nav_submit_auth"):
                    if u_input and p_input:
                        if auth_mode == "Sign Up":
                            if utils_db.create_user(u_input, e_input if e_input else "", p_input):
                                st.success("Account Created! Login now.")
                            else: st.error("Credentials conflict.")
                        else:
                            user_check = utils_db.authenticate_user(u_input, p_input)
                            if user_check:
                                st.session_state["logged_in_user_id"] = user_check
                                st.session_state["logged_in_username"] = u_input
                                st.rerun()
                            else: st.error("Access Refused.")
                    else: st.error("Fill missing keys.")
        else:
            col_inner_user, col_inner_out = st.columns([0.6, 0.4])
            with col_inner_user:
                st.markdown(f"<p style='color:#86efac; font-size:0.8rem; font-weight:700; font-family:\"SF Pro Display\"; margin-top:8px; text-align:right;'>🟢 {st.session_state['logged_in_username'].upper()}</p>", unsafe_allow_html=True)
            with col_inner_out:
                if st.button("Log Out", type="secondary", key="nav_logout_btn"):
                    st.session_state["logged_in_user_id"] = None
                    st.session_state["logged_in_username"] = None
                    st.session_state["confirmed_owner_property"] = None
                    st.rerun()

st.markdown('<hr style="border-color:rgba(255,255,255,0.04); margin-top:-10px; margin-bottom:2.5rem;">', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 📂 SIDEBAR PORTFOLIO CONSOLE (USER STATE ONLY)
# ─────────────────────────────────────────────
if st.session_state["logged_in_user_id"] is not None:
    st.sidebar.markdown("<p style='font-size:0.75rem; font-weight:800; color:#22c55e; letter-spacing:0.1em; text-transform:uppercase;'>📂 Portefeuille Géré</p>", unsafe_allow_html=True)
    user_saved_portfolio_df = utils_db.fetch_user_portfolio(st.session_state["logged_in_user_id"])
    
    if not user_saved_portfolio_df.empty:
        for idx, row in user_saved_portfolio_df.iterrows():
            if st.sidebar.button(f"🏠 {row['address'][:25]}...", key=f"saved_prop_{row['id']}", use_container_width=True):
                st.session_state["confirmed_owner_property"] = {
                    "address": row["address"], "dpe": row["dpe"], "surface": row["surface"],
                    "cost": row["cost"], "roi": row["roi"], "zipcode": row["zipcode"],
                    "lat": row["lat"], "lon": row["lon"]
                }
                st.rerun()
    else:
        st.sidebar.info("Portfolio Instance Empty.")

# ─────────────────────────────────────────────
# MAIN PAGE ROUTING: 100% OPEN FOR FREE SEARCHES
# ─────────────────────────────────────────────
if st.session_state["confirmed_owner_property"] is None:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<p class="section-label">Engine Search Core Layer</p><h2 class="section-title">{T["subtitle"]}</h2>', unsafe_allow_html=True)
    search_query = st.text_input(T["input_label"], placeholder="Ex: 39 Rue du Sergent Bobillot, Montreuil", key="main_search_input_field")
    if search_query and len(search_query.strip()) >= 3:
        st.session_state["address_suggestions"] = ban_search(search_query)
    suggestions = st.session_state["address_suggestions"]
    if suggestions:
        labels = [f"{s['label']} ({s['postcode']} {s['city']})" for s in suggestions]
        selected_label = st.selectbox(T["select_certified"], labels, key="main_address_selectbox")
        chosen_property = suggestions[labels.index(selected_label)]
        if st.button(T["btn_analyze"], type="primary", use_container_width=True, key="execute_analysis_btn"):
            st.session_state["confirmed_owner_property"] = fetch_single_property_ademe(chosen_property["label"], chosen_property["postcode"], chosen_property["lat"], chosen_property["lon"])
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    base_prop = st.session_state["confirmed_owner_property"]
    dpe_color = _DPE_COLORS.get(base_prop["dpe"], "#475569")
    
    btn_col1, btn_col2 = st.columns([4, 1])
    with btn_col1:
        if st.button(T["btn_back"], key="dashboard_back_btn"): st.session_state["confirmed_owner_property"] = None; st.rerun()
    with btn_col2:
        if st.session_state["logged_in_user_id"] is not None:
            if st.button("💾 Sauvegarder l'Actif", type="primary", use_container_width=True, key="save_asset_dashboard"):
                utils_db.save_property_to_portfolio(
                    st.session_state["logged_in_user_id"], base_prop["address"], base_prop["zipcode"],
                    base_prop["dpe"], base_prop["surface"], base_prop["cost"], base_prop["roi"],
                    base_prop["lat"], base_prop["lon"]
                )
                st.success("Asset locked inside portfolio!")
                time.sleep(0.3)
                st.rerun()
        else:
            st.markdown('<button disabled style="width:100%; opacity:0.35; cursor:not-allowed; background:#1e293b; color:#94a3b8; border:1px solid rgba(255,255,255,0.05); padding:10px; border-radius:14px; font-weight:700; font-size:0.85rem; font-family:\'SF Pro Display\'">🔒 Login Header to Save Asset</button>', unsafe_allow_html=True)
            
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<p class="section-label">{T["bilan_title"]}</p><div class="owner-exclusive-title">{base_prop["address"]}</div>', unsafe_allow_html=True)

    # ── ADEME Data Source Badge ──
    if base_prop.get("data_found"):
        numero = base_prop.get("numero_dpe") or "—"
        date_dpe = base_prop.get("date_dpe", "")[:10] if base_prop.get("date_dpe") else ""
        st.markdown(f'''
        <div style="display:inline-flex;align-items:center;gap:8px;
                    background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.3);
                    padding:6px 16px;border-radius:100px;margin-bottom:1.2rem;">
            <span style="width:7px;height:7px;background:#22c55e;border-radius:50%;
                         box-shadow:0 0 8px #22c55e;display:inline-block;"></span>
            <span style="font-size:0.72rem;font-weight:700;color:#4ade80;letter-spacing:0.08em;">
                ✓ DONNÉES OFFICIELLES ADEME · DPE N° {numero}
                {"· " + date_dpe if date_dpe else ""}
            </span>
        </div>''', unsafe_allow_html=True)
        # Show enriched fields if available
        annee = base_prop.get("annee_construction")
        conso = base_prop.get("conso_kwh")
        ges   = base_prop.get("emission_ges")
        energie = base_prop.get("energie_chauffage", "")
        if annee or conso or ges:
            ec1, ec2, ec3, ec4 = st.columns(4)
            if annee:
                ec1.markdown(f'<span class="metric-label-sub">Année construction</span><br><span style="font-size:1.3rem;font-weight:800;color:#f8fafc;">{annee}</span>', unsafe_allow_html=True)
            if conso:
                ec2.markdown(f'<span class="metric-label-sub">Consommation</span><br><span style="font-size:1.3rem;font-weight:800;color:#f8fafc;">{int(conso):,} kWh/an</span>', unsafe_allow_html=True)
            if ges:
                ec3.markdown(f'<span class="metric-label-sub">Émissions GES</span><br><span style="font-size:1.3rem;font-weight:800;color:#f8fafc;">{int(ges):,} kg CO₂</span>', unsafe_allow_html=True)
            if energie:
                ec4.markdown(f'<span class="metric-label-sub">Chauffage</span><br><span style="font-size:1.3rem;font-weight:800;color:#f8fafc;">{energie[:20]}</span>', unsafe_allow_html=True)
            st.markdown('<hr style="border-color:rgba(255,255,255,0.04);margin:1rem 0;">', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div style="display:inline-flex;align-items:center;gap:8px;
                    background:rgba(234,179,8,0.08);border:1px solid rgba(234,179,8,0.25);
                    padding:6px 16px;border-radius:100px;margin-bottom:1.2rem;">
            <span style="width:7px;height:7px;background:#eab308;border-radius:50%;display:inline-block;"></span>
            <span style="font-size:0.72rem;font-weight:700;color:#fbbf24;letter-spacing:0.08em;">
                ⚡ ESTIMATION ZONALE — Aucun DPE officiel trouvé · Données estimées
            </span>
        </div>''', unsafe_allow_html=True)

    st.markdown(f'<p class="metric-label-sub" style="color:#ffffff; margin-bottom:15px; font-weight:600;">{T["choose_plan"]}</p>', unsafe_allow_html=True)
    
    sc_col1, sc_col2, sc_col3 = st.columns(3)
    with sc_col1:
        is_ess = (st.session_state["selected_scenario"] == "Essential")
        st.markdown(f'<div class="card {"scenario-card-active" if is_ess else ""}" style="padding:1.5rem; margin-bottom:0.5rem; text-align:center; border-radius:18px;"><strong>{T["eco_ess"]}</strong><br><span style="font-size:0.8rem;color:#64748b;">{T["eco_ess_sub"]}</span></div>', unsafe_allow_html=True)
        if st.button("Trigger Essential", key="ess", use_container_width=True): st.session_state["selected_scenario"] = "Essential"; st.rerun()
    with sc_col2:
        is_plus = (st.session_state["selected_scenario"] == "Plus")
        st.markdown(f'<div class="card {"scenario-card-active" if is_plus else ""}" style="padding:1.5rem; margin-bottom:0.5rem; text-align:center; border-radius:18px;"><strong>{T["conf_plus"]}</strong><br><span style="font-size:0.8rem;color:#64748b;">{T["conf_plus_sub"]}</span></div>', unsafe_allow_html=True)
        if st.button("Trigger Comfort Plus", key="plus", use_container_width=True): st.session_state["selected_scenario"] = "Plus"; st.rerun()
    with sc_col3:
        is_zero = (st.session_state["selected_scenario"] == "Zero")
        st.markdown(f'<div class="card {"scenario-card-active" if is_zero else ""}" style="padding:1.5rem; margin-bottom:0.5rem; text-align:center; border-radius:18px;"><strong>{T["carb_zero"]}</strong><br><span style="font-size:0.8rem;color:#64748b;">{T["carb_zero_sub"]}</span></div>', unsafe_allow_html=True)
        if st.button("Trigger Carbon Zero", key="zero", use_container_width=True): st.session_state["selected_scenario"] = "Zero"; st.rerun()

    st.markdown('<hr style="border-color:rgba(255,255,255,0.04); margin: 2rem 0;">', unsafe_allow_html=True)

    current_scenario = st.session_state["selected_scenario"]
    active_cost = round(base_prop["cost"] * _SCENARIO_COST_MULTIPLIER[current_scenario], 0)
    active_roi  = round(base_prop["roi"] * _SCENARIO_ROI_MULTIPLIER[current_scenario], 1)
    target_dpe  = _SCENARIO_TARGET_DPE[current_scenario]

    # Metrics Display Block
    col_left_dpe, col_right_metrics = st.columns([0.9, 2.1], gap="large")
    with col_left_dpe:
        st.markdown(f'<div style="text-align: center; background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255,255,255,0.04); padding: 25px; border-radius:24px;"><p class="metric-label-sub" style="margin-bottom:12px;">{T["current_class"]}</p><div class="dpe-badge-big" style="background-color:{dpe_color}; margin-bottom:18px;">{base_prop["dpe"]}</div><br><p class="metric-label-sub" style="color:#22c55e;">{T["target_class"]} {target_dpe} ✅</p></div>', unsafe_allow_html=True)
        
    with col_right_metrics:
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1: st.markdown(f'<span class="metric-value-huge">{base_prop["surface"]}</span><span style="font-size:1.5rem; font-weight:700; color:#475569;"> m²</span><br><span class="metric-label-sub">{T["surface"]}</span>', unsafe_allow_html=True)
        with m_col2: st.markdown(f'<span class="metric-value-huge">€{active_cost:,.0f}</span><br><span class="metric-label-sub">{T["budget_est"]}</span>', unsafe_allow_html=True)
        with m_col3: st.markdown(f'<span class="metric-value-huge" style="color:#22c55e;">+{active_roi}%</span><br><span class="metric-label-sub">{T["uplift_label"]}</span>', unsafe_allow_html=True)

        st.markdown(f'<br><p class="metric-label-sub" style="color:#fff; font-weight:600; margin-bottom:5px;">{T["visual_prog"]}</p>', unsafe_allow_html=True)
        dpe_sequence = ["G", "F", "E", "D", "C", "B", "A"]
        if base_prop["dpe"] in dpe_sequence and target_dpe in dpe_sequence:
            c_idx, t_idx = dpe_sequence.index(base_prop["dpe"]), dpe_sequence.index(target_dpe)
            fig_progress = go.Figure()
            fig_progress.add_trace(go.Scatter(x=dpe_sequence, y=[1]*7, mode='markers+text', text=dpe_sequence, textposition="top center", marker=dict(size=24, color=["#ff0000", "#ff3300", "#ff6600", "#f2b035", "#ccff33", "#33cc33", "#319834"]), showlegend=False))
            if c_idx < 6 and c_idx != t_idx:
                fig_progress.add_annotation(x=dpe_sequence[t_idx], y=1, ax=dpe_sequence[c_idx], ay=1, text="", showarrow=True, arrowhead=3, arrowsize=1.5, arrowwidth=4, arrowcolor="#fff")
            fig_progress.update_layout(height=110, margin=dict(l=20,r=20,t=20,b=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(visible=False), yaxis=dict(visible=False))
            st.plotly_chart(fig_progress, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

    # ── 🗺️ GEOSPATIAL MAP LAYERS ──
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col_map_h, col_map_t = st.columns([2.0, 1.0])
    with col_map_h: st.markdown(f'<p class="section-label">Geospatial Registry</p><h3 class="section-title">{T["map_title"]}</h3>', unsafe_allow_html=True)
    with col_map_t: map_style_selection = st.radio("Style Map Layer Layer", ["Standard Grid view", "High-Res Satellite View"], horizontal=True, label_visibility="collapsed", key="dashboard_map_radio")
    
    f_map = folium.Map(location=[base_prop["lat"], base_prop["lon"]], zoom_start=17)
    if map_style_selection == "High-Res Satellite View":
        folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri', name='Satellite').add_to(f_map)
    else:
        folium.TileLayer('cartodbpositron', name='Dark Canvas').add_to(f_map)
    folium.Marker([base_prop["lat"], base_prop["lon"]], icon=folium.Icon(color='green', icon='home')).add_to(f_map)
    st_folium(f_map, use_container_width=True, height=360, returned_objects=[])
    st.markdown("</div>", unsafe_allow_html=True)

    # ── 🌡️ HEAT LOSS MATRIX ──
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<p class="section-label">Thermal Defect Matrix</p><h3 class="section-title">{T["loss_title"]}</h3>', unsafe_allow_html=True)
    fig_loss = go.Figure(go.Bar(x=[30, 25, 15, 10], y=["Toiture (Roof)", "Murs (Walls)", "Fenêtres (Windows)", "Planchers (Floors)"], orientation='h', marker=dict(color=['#dc2626', '#ef4444', '#f97316', '#eab308']), text=[f"{val}%" for val in [30, 25, 15, 10]], textposition='auto'))
    fig_loss.update_layout(height=160, margin=dict(l=20, r=20, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(visible=False), yaxis=dict(color="#f1f5f9"))
    st.plotly_chart(fig_loss, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

    # ── FINANCIAL ANALYTICAL BLOCKS ──
    if active_cost > 0:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<p class="section-label">{T["fin_title"]}</p><h3 class="section-title">{T["fin_sub"]}</h3>', unsafe_allow_html=True)
        selected_income_bracket = st.selectbox(T["income_label"], list(_INCOME_SUBSIDY_MAP.keys()), index=2, key="income_bracket_selectbox")
        subsidy_rate = _INCOME_SUBSIDY_MAP[selected_income_bracket]
        if current_scenario == "Plus": subsidy_rate = min(subsidy_rate + 0.05, 0.85)
        elif current_scenario == "Zero": subsidy_rate = min(subsidy_rate + 0.12, 0.90)
            
        estimated_subsidy = round(active_cost * subsidy_rate, 0)
        net_cost = active_cost - estimated_subsidy
        energy_saving = "€1,200 / an" if current_scenario == "Essential" else ("€1,850 / an" if current_scenario == "Plus" else "€2,600 / an")
        
        chart_col, metrics_col = st.columns([1.2, 1.8], gap="large")
        with chart_col:
            fig_financial = utils_charts.generate_financial_pie(estimated_subsidy, net_cost, T["subvention_label"], T["reste_charge"])
            st.plotly_chart(fig_financial, use_container_width=True, config={'displayModeBar': False})
        with metrics_col:
            sub1, sub2 = st.columns(2)
            sub1.metric(T["subvention_label"], f"€{estimated_subsidy:,.0f}", f"~{int(subsidy_rate*100)}%")
            sub2.metric(T["reste_charge"], f"€{net_cost:,.0f}", "Net remaining allocation")
            st.markdown(f'<div style="background: rgba(255,255,255,0.01); padding: 16px; border-radius: 14px; border: 1px solid rgba(255,255,255,0.04); font-size:0.9rem;">{T["impact_facture"].format(sc=current_scenario, saving=energy_saving)}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # ECO-PTZ LOAN SLIDER SIMULATOR
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<p class="section-label">Financing Optimization</p><h3 class="section-title">{T["loan_title"]}</h3>', unsafe_allow_html=True)
        loan_years_duration = st.slider(T["loan_duration"], 5, 20, 15, key="loan_duration_slider")
        calculated_monthly_installment = net_cost / (loan_years_duration * 12)
        col_ln_m1, col_ln_m2 = st.columns(2)
        with col_ln_m1: st.markdown(f'<br><span class="metric-value-huge" style="color:#22c55e;">€{calculated_monthly_installment:,.2f}</span><span style="font-size:1.3rem;color:#64748b; font-weight:700;"> / mois</span><br><span class="metric-label-sub">{T["monthly_pay"]} (0% TAEG Credit Leverage)</span>', unsafe_allow_html=True)
        with col_ln_m2:
            fig_gauge = go.Figure(go.Indicator(mode = "gauge+number", value = calculated_monthly_installment, domain = {'x': [0, 1], 'y': [0, 1]}, gauge = {'axis': {'range': [0, 500 if net_cost < 20000 else 1300]}, 'bar': {'color': "#22c55e"}}))
            fig_gauge.update_layout(height=110, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<p class="section-label">{T["chart_5yr_title"]}</p><h3 class="section-title">{T["chart_5yr_sub"]}</h3>', unsafe_allow_html=True)
    fig_5yr = utils_charts.generate_five_year_trajectory(active_roi)
    st.plotly_chart(fig_5yr, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

    # LEAD GENERATION DATA INTAKE FORM
    if active_cost > 0:
        st.markdown('<div class="card" style="border: 1px solid rgba(34,197,94,0.22); background: linear-gradient(135deg, #070c12, #04070c);">', unsafe_allow_html=True)
        st.markdown(f'<p class="section-label" style="color:#22c55e;">Verified Deployment Connection</p><h3 style="color:#f8fafc; margin-top:0;">{T["form_title"]}</h3><p style="color:#64748b; font-size:0.9rem; margin-top:-5px;">{T["form_sub"]}</p>', unsafe_allow_html=True)
        with st.form("rge_lead_capture_form"):
            col_lead1, col_lead2 = st.columns(2)
            with col_lead1:
                owner_name = st.text_input(T["form_name"], placeholder="M. Jean Dupont")
                owner_phone = st.text_input(T["form_phone"], placeholder="06 12 34 56 78")
            with col_lead2:
                owner_email = st.text_input(T["form_email"], placeholder="jean.dupont@gmail.com")
                time_slot = st.selectbox(T["form_time"], ["Matin (9h - 12h)", "Après-midi (14h - 17h)"])
            additional_notes = st.text_area(T["form_notes"])
            if st.form_submit_button(T["form_btn"]):
                if owner_name and owner_phone and owner_email:
                    db_logged = utils_db.log_lead_to_db(base_prop["address"], base_prop["zipcode"], base_prop["dpe"], target_dpe, current_scenario, active_cost, owner_name, owner_phone, owner_email, time_slot, additional_notes)
                    if db_logged: st.success(T["form_success"])
                else: st.error(T["form_err"])
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    try:
        pdf_string_data = generate_zami_pdf_bytes(base_prop, current_scenario, target_dpe, active_cost, net_cost)
        pdf_bytes_io = io.BytesIO(pdf_string_data.encode('latin1') if isinstance(pdf_string_data, str) else pdf_string_data)
        st.download_button(label=T["download_btn"], data=pdf_bytes_io, file_name=f"ZAMI_Rapport_{base_prop['zipcode']}.pdf", mime="application/pdf", use_container_width=True, key="pdf_download_button_dashboard")
    except Exception: pass
    st.markdown("</div>", unsafe_allow_html=True)

# ── 🛡️ OPERATIONAL ENVIRONMENT SECURED VAULT MONITORING ──
st.markdown('<div class="card" style="background:none; border:none; box-shadow:none; margin-bottom:0; padding-bottom:0;">', unsafe_allow_html=True)
if st.checkbox("🔑 Open ZAMI Secure Admin Database Vault Viewer", key="admin_vault_checkbox"):
    admin_password_input = st.text_input("Enter Secret Admin System Password :", type="password", key="admin_vault_password")
    if admin_password_input:
        SECRET_MASTER_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "HussnainZami2026")
        if admin_password_input == SECRET_MASTER_PASSWORD:
            st.markdown('<div class="card" style="border:1px solid rgba(234,179,8,0.25); background: #070b11;">', unsafe_allow_html=True)
            try:
                conn = sqlite3.connect(utils_db.DB_PATH)
                leads_df = pd.read_sql_query("SELECT * FROM leads ORDER BY id DESC", conn)
                conn.close()
                if not leads_df.empty: st.dataframe(leads_df, use_container_width=True)
                else: st.info("La base de données est vide.")
            except Exception as e: st.error(f"Error: {e}")
            st.markdown('</div>', unsafe_allow_html=True)
        else: st.markdown('<span style="color:#dc2626; font-size:0.85rem; font-weight:600;">❌ ACCESS DENIED: Invalid Password token.</span>', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown(f'<div class="footer">{T["footer"]}</div>', unsafe_allow_html=True)