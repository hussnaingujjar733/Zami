import os
import base64
import json
import requests
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from fpdf import FPDF
from streamlit_folium import st_folium
import folium
from typing import Optional
from datetime import datetime
import hashlib

# ── ⚡ IMPORT MODULES ──
import utils_styles
import utils_charts
import utils_animations as anim
import utils_transitions as trans

# Run Premium Style Injections
utils_styles.inject_premium_styles()
trans.inject_page_transitions()
trans.add_loading_spinner()


# ─────────────────────────────────────────────
# HIDE SIDEBAR COMPLETELY
# ─────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stSidebarNav"] { display: none !important; }
    [data-testid="stSidebarCollapsedControl"] { display: none !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STATE MANAGEMENT
# ─────────────────────────────────────────────
if "confirmed_owner_property" not in st.session_state:
    st.session_state["confirmed_owner_property"] = None
if "address_suggestions" not in st.session_state:
    st.session_state["address_suggestions"] = []
if "selected_scenario" not in st.session_state:
    st.session_state["selected_scenario"] = "Essential"
if "selected_address_label" not in st.session_state:
    st.session_state["selected_address_label"] = None
if "property_surface" not in st.session_state:
    st.session_state["property_surface"] = 68
if "user_responses" not in st.session_state:
    st.session_state["user_responses"] = None
if "photos_uploaded" not in st.session_state:
    st.session_state["photos_uploaded"] = False
if "accuracy_level" not in st.session_state:
    st.session_state["accuracy_level"] = 1

# Global Variables
_SCENARIO_COST_MULTIPLIER = {"Essential": 1.0, "Plus": 1.65, "Zero": 2.45}
_SCENARIO_ROI_MULTIPLIER = {"Essential": 1.0, "Plus": 1.45, "Zero": 1.95}
_SCENARIO_TARGET_DPE = {"Essential": "D", "Plus": "C", "Zero": "B"}
_FALLBACK_RENO_COST = {"G": 1350, "F": 1100, "E": 620, "D": 280, "C": 120, "B": 0, "A": 0}
_FALLBACK_UPLIFT = {"G": 24.2, "F": 19.8, "E": 13.1, "D": 6.8, "C": 2.0, "B": 0, "A": 0}
_DPE_COLORS = {"A": "#319834", "B": "#33cc33", "C": "#ccff33", "D": "#f2b035", "E": "#ff6600", "F": "#ff3300", "G": "#ff0000"}
_INCOME_SUBSIDY_MAP = {"Très Modeste (Bleu)": 0.75, "Modeste (Jaune)": 0.60, "Intermédiaire (Violet)": 0.40, "Supérieur (Rose)": 0.15}

CHAT_FILE = "chat_messages.json"
LEADS_FILE = "homeowner_leads.json"


# ─────────────────────────────────────────────
# LEAD FUNCTIONS (JSON Storage)
# ─────────────────────────────────────────────
def save_lead(email, address, dpe, subsidy, roi):
    try:
        if os.path.exists(LEADS_FILE):
            with open(LEADS_FILE, "r", encoding="utf-8") as f:
                leads = json.load(f)
        else:
            leads = []
        leads.append({
            "id": len(leads) + 1, "email": email, "address": address, "dpe": dpe,
            "subsidy": subsidy, "roi": roi,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "status": "new"
        })
        with open(LEADS_FILE, "w", encoding="utf-8") as f:
            json.dump(leads, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False

def get_all_leads():
    try:
        if os.path.exists(LEADS_FILE):
            with open(LEADS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    except:
        return []


# ─────────────────────────────────────────────
# CHAT FUNCTIONS (JSON Storage)
# ─────────────────────────────────────────────
def save_chat_message(name, email, message):
    try:
        if os.path.exists(CHAT_FILE):
            with open(CHAT_FILE, "r", encoding="utf-8") as f:
                messages = json.load(f)
        else:
            messages = []
        messages.append({
            "id": len(messages) + 1, "name": name, "email": email, "message": message,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "status": "unread"
        })
        with open(CHAT_FILE, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False

def get_all_chat_messages():
    try:
        if os.path.exists(CHAT_FILE):
            with open(CHAT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    except:
        return []

def mark_message_read(msg_id):
    try:
        messages = get_all_chat_messages()
        for msg in messages:
            if msg.get("id") == msg_id:
                msg["status"] = "read"
                break
        with open(CHAT_FILE, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False


# ─────────────────────────────────────────────
# LOGO FUNCTION
# ─────────────────────────────────────────────
def get_logo_html():
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "zami_logo.png")
    if os.path.exists(logo_path):
        try:
            with open(logo_path, "rb") as img_f:
                logo_base64 = base64.b64encode(img_f.read()).decode()
                return f'<img src="data:image/png;base64,{logo_base64}" style="height:45px; width:auto;">'
        except:
            pass
    return '<div style="font-family: Space Grotesk, sans-serif; font-size:1.8rem; font-weight:800; background:linear-gradient(135deg,#3B82F6,#10B981); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">ZAMI</div>'


# ─────────────────────────────────────────────
# ACCURACY IMPROVEMENT FUNCTIONS
# ─────────────────────────────────────────────
def calculate_enhanced_roi(property_data, user_responses):
    base_roi = property_data.get("roi", 15.0)
    windows_multiplier = {"Simple vitrage": 1.0, "Double vitrage": 0.6, "Triple vitrage": 0.4, "Je ne sais pas": 0.8}
    heating_multiplier = {"Gaz (ancien)": 1.0, "Gaz (condensation)": 0.7, "Électrique": 0.9, "Pompe à chaleur": 0.5, "Bois / granulés": 0.6, "Je ne sais pas": 0.8}
    insulation_factor = 1.0
    if user_responses.get("roof_insulation") == "Non":
        insulation_factor += 0.2
    if user_responses.get("wall_insulation") == "Non":
        insulation_factor += 0.25
    window_factor = windows_multiplier.get(user_responses.get("windows", "Je ne sais pas"), 0.8)
    heating_factor = heating_multiplier.get(user_responses.get("heating", "Je ne sais pas"), 0.8)
    accuracy_boost = (1 - window_factor) * 0.3 + (1 - heating_factor) * 0.3 + (insulation_factor - 1) * 0.4
    enhanced_roi = base_roi * (1 + accuracy_boost)
    return min(enhanced_roi, 35.0)

def accuracy_progress_bar():
    levels = {1: {"name": "Données officielles", "accuracy": "70-75%", "color": "#64748b"},
              2: {"name": "Questionnaire", "accuracy": "85-90%", "color": "#eab308"},
              3: {"name": "Photos IA", "accuracy": "90-95%", "color": "#22c55e"},
              4: {"name": "Audit certifié", "accuracy": "98-99%", "color": "#22c55e"}}
    current_level = st.session_state.get("accuracy_level", 1)
    cols = st.columns(4)
    for i, (level, info) in enumerate(levels.items(), 1):
        with cols[i-1]:
            if level <= current_level:
                st.markdown(f"<div style='text-align:center'><div style='background:{info['color']}; width:30px; height:30px; border-radius:15px; margin:0 auto 5px auto; display:flex; align-items:center; justify-content:center;'>✓</div><div style='font-size:12px'>{info['name']}</div><div style='font-size:11px; color:#22c55e'>{info['accuracy']}</div></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align:center; opacity:0.4'><div style='background:#1e293b; width:30px; height:30px; border-radius:15px; margin:0 auto 5px auto; display:flex; align-items:center; justify-content:center;'>{level}</div><div style='font-size:12px'>{info['name']}</div><div style='font-size:11px; color:#64748b'>{info['accuracy']}</div></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PROPERTY VISUAL FUNCTIONS
# ─────────────────────────────────────────────
def get_property_visual(lat, lon, dpe_class, is_after=False):
    coord_hash = int(hashlib.md5(f"{lat},{lon}".encode()).hexdigest()[:8], 16)
    if is_after:
        base_url = "https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg"
    else:
        if dpe_class in ["F", "G"]:
            base_url = "https://images.pexels.com/photos/280229/pexels-photo-280229.jpeg"
        elif dpe_class in ["D", "E"]:
            base_url = "https://images.pexels.com/photos/1643384/pexels-photo-1643384.jpeg"
        else:
            base_url = "https://images.pexels.com/photos/2587054/pexels-photo-2587054.jpeg"
    return f"{base_url}?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&sig={coord_hash}"

def dynamic_before_after_section(address, dpe_class, surface, lat, lon):
    before_image = get_property_visual(lat, lon, dpe_class, is_after=False)
    after_image = get_property_visual(lat, lon, dpe_class, is_after=True)
    current_value = int(280000 * (surface / 68))
    after_value = int(350000 * (surface / 68))
    subsidy = int(12500 * (surface / 68))
    gain = after_value - current_value
    target_dpe = "C" if dpe_class in ["F", "G"] else ("D" if dpe_class == "E" else "B")
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, rgba(59,130,246,0.05), rgba(16,185,129,0.02)); border-radius:32px; padding:40px; margin:30px 0; text-align:center;">
        <h3 style="font-size:1.8rem; margin-bottom:10px;">🔄 Avant / Après Rénovation</h3>
        <p style="color:#64748b; margin-bottom:30px;">Visualisez le potentiel de votre bien à {address[:50]}</p>
        <div style="display:flex; justify-content:center; align-items:center; gap:30px; flex-wrap:wrap;">
            <div style="background:linear-gradient(135deg, #1e293b, #0f172a); border-radius:24px; padding:20px; width:280px; text-align:center; border:1px solid rgba(239,68,68,0.3);">
                <img src="{before_image}" style="width:100%; height:180px; border-radius:16px; object-fit:cover; margin-bottom:15px;">
                <div style="font-weight:800; font-size:28px;">DPE: {dpe_class}</div>
                <div style="font-size:13px; color:#ef4444;">Passoire thermique</div>
                <div style="margin-top:15px;"><div style="font-size:12px; color:#64748b;">Valeur estimée</div><div style="font-weight:700; font-size:20px;">{current_value:,} €</div></div>
            </div>
            <div style="font-size:48px; animation:arrowPulse 1.5s infinite;">→</div>
            <div style="background:linear-gradient(135deg, rgba(16,185,129,0.15), rgba(16,185,129,0.05)); border-radius:24px; padding:20px; width:280px; text-align:center; border:1px solid #10B981;">
                <img src="{after_image}" style="width:100%; height:180px; border-radius:16px; object-fit:cover; margin-bottom:15px;">
                <div style="font-weight:800; font-size:28px; color:#10B981;">DPE: {target_dpe}</div>
                <div style="font-size:13px; color:#10B981;">Performance énergétique</div>
                <div style="margin-top:15px;"><div style="font-size:12px; color:#64748b;">Valeur estimée</div><div style="font-weight:700; font-size:20px; color:#10B981;">{after_value:,} €</div></div>
            </div>
        </div>
        <div style="background:rgba(16,185,129,0.1); border-radius:60px; padding:12px 24px; display:inline-block; margin-top:30px;">
            💰 <span style="font-size:20px; font-weight:800; color:#10B981;">+{gain:,} €</span> de valeur ajoutée • 🏷️ Subvention: <span style="font-size:20px; font-weight:800; color:#10B981;">{subsidy:,} €</span>
        </div>
    </div>
    <style>@keyframes arrowPulse{{0%,100%{{transform:translateX(0); opacity:0.6;}}50%{{transform:translateX(8px); opacity:1;}}}}</style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DPE FUNCTIONS
# ─────────────────────────────────────────────
def fetch_by_dpe_number(numero_dpe: str) -> Optional[dict]:
    if not numero_dpe or len(numero_dpe.strip()) < 5:
        return None
    url = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines"
    params = {"qs": f"numero_dpe:{numero_dpe.strip()}", "size": 1, "select": "numero_dpe,etiquette_dpe,etiquette_ges,surface_habitable_logement,code_postal_ban,adresse_ban,date_etablissement_dpe,annee_construction,type_batiment,conso_5_usages_ef_energie_n1,emission_ges_5_usages_n1,type_energie_principale_chauffage"}
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            results = data.get("results", [])
            if results:
                record = results[0]
                dpe_class = str(record.get("etiquette_dpe", "E")).upper().strip()
                surface = record.get("surface_habitable_logement") or 68.0
                postcode = record.get("code_postal_ban", "75000")
                address = record.get("adresse_ban", "")
                cost = surface * _FALLBACK_RENO_COST.get(dpe_class, 250)
                roi = _FALLBACK_UPLIFT.get(dpe_class, 13.1)
                return {"address": address, "dpe": dpe_class, "surface": surface, "cost": cost, "roi": roi, "zipcode": postcode, "lat": 48.8566, "lon": 2.3522, "data_found": True, "source": "ADEME_DPE_NUMBER", "current_value": 280000}
    except:
        pass
    return None

def safe_get(url, params=None):
    try:
        r = requests.get(url, params=params, timeout=10)
        return r.json()
    except:
        return None

def ban_search(query: str, limit: int = 5):
    if not query or len(query.strip()) < 3:
        return []
    data = safe_get("https://api-adresse.data.gouv.fr/search/", {"q": query, "limit": limit})
    features = data.get("features", []) if data else []
    results = []
    for f in features:
        p = f.get("properties", {})
        c = f.get("geometry", {}).get("coordinates", [2.3522, 48.8566])
        results.append({"label": p.get("label", ""), "postcode": p.get("postcode", ""), "city": p.get("city", ""), "lon": c[0], "lat": c[1], "citycode": p.get("citycode", "")})
    return results

def fetch_single_property_ademe(query_address: str, zipcode: str, lat=48.8566, lon=2.3522, citycode: str = ""):
    dpe_by_region = {"75": "E", "92": "E", "93": "F", "94": "E", "69": "D", "13": "D", "31": "D"}
    region = str(zipcode)[:2]
    dpe = dpe_by_region.get(region, "E")
    surface = 52.0 if region == "75" else 75.0
    cost = round(surface * _FALLBACK_RENO_COST.get(dpe, 620), 0)
    roi = _FALLBACK_UPLIFT.get(dpe, 13.1)
    st.session_state["property_surface"] = surface
    return {"address": query_address, "dpe": dpe, "surface": surface, "cost": cost, "roi": roi, "zipcode": zipcode, "lat": lat, "lon": lon, "data_found": False, "source": "ESTIMATION", "current_value": 280000}

def generate_professional_pdf(property_data, scenario, target_dpe, active_cost, net_cost, subsidy, roi):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 20)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 15, 'ZAMI PROPERTY REPORT', ln=True, align='C')
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 8, f'Date: {datetime.now().strftime("%d/%m/%Y")}', ln=True, align='R')
    pdf.ln(5)
    address = property_data.get('address', 'Address not available')
    pdf.set_font('Helvetica', 'B', 12)
    pdf.multi_cell(0, 8, str(address))
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, 'Property Details', ln=True)
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 8, f"Current DPE: {property_data.get('dpe', 'N/A')}", ln=True)
    pdf.cell(0, 8, f"Target DPE: {target_dpe}", ln=True)
    pdf.cell(0, 8, f"Surface: {int(property_data.get('surface', 0))} m2", ln=True)
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, 'Financial Summary', ln=True)
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 8, f"Renovation Cost: EUR {active_cost:,.0f}", ln=True)
    pdf.cell(0, 8, f"Subsidy: EUR {subsidy:,.0f}", ln=True)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, f"Net Investment: EUR {net_cost:,.0f}", ln=True)
    pdf.cell(0, 8, f"Expected ROI: +{roi}%", ln=True)
    pdf.set_y(-30)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 8, 'ZAMI - Property Intelligence Platform', ln=True, align='C')
    output = pdf.output(dest='S')
    if isinstance(output, bytearray):
        output = bytes(output)
    return output


# Language translations (simplified)
LANG_DICT = {
    "FR": {
        "title": "Portail Propriétaire Énergétique", "subtitle": "Estimez instantanément la valeur et les travaux de votre bien",
        "input_label": "Saisissez l'adresse de votre logement :", "select_certified": "Sélectionnez l'adresse certifiée BAN France :",
        "btn_analyze": "⚡ Lancer l'Analyse", "btn_back": "⬅️ Nouvelle recherche",
        "bilan_title": "BILAN PATRIMONIAL EXCLUSIF", "choose_plan": "PLAN DE CONFIGURATION ÉNERGÉTIQUE",
        "eco_ess": "🛠️ Éco Essential", "eco_ess_sub": "DPE D • Conformité Légale 2026",
        "conf_plus": "⚡ Confort Plus", "conf_plus_sub": "DPE C • Isolation Enveloppe Globale",
        "carb_zero": "🟢 Carbone Zéro", "carb_zero_sub": "DPE B • Décarbonation Pompe à Chaleur",
        "current_class": "Classe Initiale", "target_class": "🎯 Objectif Scénario",
        "surface": "Surface Habitable", "budget_est": "Investissement Global", "uplift_label": "Uplift Marché Estimé",
        "visual_prog": "Vecteur de Progression Énergétique", "your_property": "Actif 🏠", "target_label": "Cible",
        "fin_title": "Analyse d'Ingénierie Financière", "fin_sub": "Subventions Publiques vs Reste à Charge Net",
        "subvention_label": "Aides MaPrimeRénov'", "reste_charge": "Reste à Charge Net",
        "impact_facture": "Impact: Le plan {sc} génère {saving} d'économies par an.",
        "chart_5yr_title": "📊 Évolution Prédictive de l'Actif (2026-2031)", "chart_5yr_sub": "Trajectoire patrimoniale après rénovation",
        "form_title": "Mise en Relation avec un Artisan RGE", "form_sub": "Recevez 3 devis gratuits d'artisans certifiés",
        "form_name": "Nom Complet *", "form_phone": "Téléphone *", "form_email": "Email *", "form_time": "Créneau de rappel",
        "form_notes": "Notes (optionnel)", "form_btn": "📨 Envoyer ma demande", "form_err": "⚠️ Champs requis manquants",
        "form_success": "🎉 Demande envoyée! Un artisan vous contactera sous 24h.", "download_btn": "⬇️ Télécharger le Rapport PDF",
        "map_title": "🗺️ Géolocalisation du bien", "loss_title": "🌡️ Pertes thermiques estimées", "income_label": "💰 Profil de revenu:",
        "loan_title": "💶 Simulation Eco-PTZ", "loan_duration": "Durée (années)", "monthly_pay": "Mensualité (0% intérêt)",
        "footer": "ZAMI - Intelligence Rénovation Énergétique", "search_method_address": "📍 Recherche par adresse (~85% précis)",
        "search_method_dpe": "🔑 Recherche par numéro DPE (100% exact)", "dpe_number_label": "🔑 Numéro DPE",
        "dpe_number_help": "Trouvez le numéro sur votre certificat DPE", "dpe_not_found": "❌ Numéro DPE invalide",
        "exact_match_badge": "✅ Données 100% exactes", "select_address_warning": "📍 Sélectionnez une adresse",
        "enter_input_warning": "⚠️ Entrez une adresse ou un numéro DPE"
    },
    "EN": {
        "title": "Energy Property Portal", "subtitle": "Estimate your property value and renovation costs instantly",
        "input_label": "Enter your property address:", "select_certified": "Select certified BAN France address:",
        "btn_analyze": "⚡ Run Analysis", "btn_back": "⬅️ New Search", "bilan_title": "EXCLUSIVE PROPERTY AUDIT",
        "choose_plan": "ENERGY CONFIGURATION PLAN", "eco_ess": "🛠️ Eco Essential", "eco_ess_sub": "DPE D • Legal Compliance 2026",
        "conf_plus": "⚡ Comfort Plus", "conf_plus_sub": "DPE C • Full Insulation", "carb_zero": "🟢 Carbon Zero",
        "carb_zero_sub": "DPE B • Heat Pump", "current_class": "Current Class", "target_class": "🎯 Target Scenario",
        "surface": "Surface Area", "budget_est": "Global Investment", "uplift_label": "Market Uplift", "visual_prog": "Energy Progression",
        "your_property": "Your Asset 🏠", "target_label": "Target", "fin_title": "Financial Analysis", "fin_sub": "Public Subsidies vs Net Cost",
        "subvention_label": "MaPrimeRénov' Aid", "reste_charge": "Net Remaining", "impact_facture": "Impact: Plan {sc} saves {saving} annually on utilities.",
        "chart_5yr_title": "📊 5-Year Asset Value Prediction (2026-2031)", "chart_5yr_sub": "Renovation vs Obsolescence trajectory",
        "form_title": "Connect with an RGE Certified Contractor", "form_sub": "Get 3 free quotes from certified professionals",
        "form_name": "Full Name *", "form_phone": "Phone *", "form_email": "Email *", "form_time": "Callback time", "form_notes": "Notes (optional)",
        "form_btn": "📨 Submit Request", "form_err": "⚠️ Required fields missing", "form_success": "🎉 Request sent! A contractor will contact you within 24h.",
        "download_btn": "⬇️ Download PDF Report", "map_title": "🗺️ Property Location", "loss_title": "🌡️ Estimated Heat Loss",
        "income_label": "💰 Income profile:", "loan_title": "💶 Eco-PTZ Simulation", "loan_duration": "Duration (years)",
        "monthly_pay": "Monthly payment (0% interest)", "footer": "ZAMI - Energy Renovation Intelligence",
        "search_method_address": "📍 Address search (~85% accurate)", "search_method_dpe": "🔑 DPE number search (100% exact)",
        "dpe_number_label": "🔑 DPE Number", "dpe_number_help": "Find the number on your DPE certificate", "dpe_not_found": "❌ Invalid DPE number",
        "exact_match_badge": "✅ 100% exact data", "select_address_warning": "📍 Please select an address",
        "enter_input_warning": "⚠️ Please enter address or DPE number"
    }
}


# ─────────────────────────────────────────────
# HERO SECTION (Minimal: Logo + Badge + Video)
# ─────────────────────────────────────────────
def hero_section():
    st.markdown("""
    <style>
    .hero-container {
        position: relative;
        border-radius: 32px;
        overflow: hidden;
        margin-bottom: 30px;
        min-height: 400px;
        background: linear-gradient(135deg, #0F172A, #020617);
    }
    
    .hero-iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        z-index: 0;
        border: none;
        pointer-events: none;
    }
    
    .hero-overlay {
        position: relative;
        background: linear-gradient(135deg, rgba(15,23,42,0.5), rgba(2,6,23,0.6));
        border-radius: 32px;
        padding: 80px 40px;
        text-align: center;
        z-index: 1;
        min-height: 400px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .hero-logo {
        font-size: 4rem;
        font-weight: 800;
        font-family: 'Space Grotesk', sans-serif;
        background: linear-gradient(135deg, #F8FAFC, #3B82F6, #10B981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(59,130,246,0.2);
        backdrop-filter: blur(10px);
        padding: 8px 20px;
        border-radius: 100px;
        border: 1px solid rgba(59,130,246,0.3);
    }
    
    .hero-badge span {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        color: #3B82F6;
        text-transform: uppercase;
    }
    
    @media (max-width: 768px) {
        .hero-overlay {
            padding: 60px 20px;
            min-height: 350px;
        }
        .hero-logo {
            font-size: 2.5rem;
        }
    }
    </style>
    
    <div class="hero-container">
        <iframe class="hero-iframe" 
            src="https://www.youtube.com/embed/mCmjNwjYfqw?autoplay=1&loop=1&mute=1&controls=0&modestbranding=1&showinfo=0&rel=0&iv_load_policy=3&playsinline=1&playlist=mCmjNwjYfqw&enablejsapi=1"
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen>
        </iframe>
        <div class="hero-overlay">
            <div class="hero-logo">ZAMI</div>
            <div class="hero-badge">
                <span>⚡ FRANCE'S #1 RENOVATION INTELLIGENCE</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


premium_hero_section = hero_section


# ─────────────────────────────────────────────
# HEADER (No AI Assistant button)
# ─────────────────────────────────────────────
col_left, col_mid, col_right = st.columns([1.2, 1.5, 1.3])

with col_left:
    st.markdown(get_logo_html(), unsafe_allow_html=True)

with col_mid:
    selected_lang = st.selectbox("🌐 Language", ["FR", "EN"], label_visibility="collapsed", key="lang")

with col_right:
    # Empty - removed AI Assistant button
    st.write("")

T = LANG_DICT[selected_lang]

st.markdown('<hr style="border-color:rgba(255,255,255,0.04); margin-bottom:2rem;">', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────
if st.session_state["confirmed_owner_property"] is None:
    # Only hero section, no trust badges, no counters
    premium_hero_section()
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    search_method = st.radio(
        "🔍 Search method:",
        [T["search_method_address"], T["search_method_dpe"]],
        key="search_method",
        horizontal=True
    )
    
    if search_method == T["search_method_address"]:
        search_query = st.text_input(T["input_label"], placeholder="Ex: 39 Rue du Sergent Bobillot, Montreuil", key="search_input")
        if search_query and len(search_query.strip()) >= 3:
            st.session_state["address_suggestions"] = ban_search(search_query)
        suggestions = st.session_state["address_suggestions"]
        if suggestions:
            labels = [f"{s['label']} ({s['postcode']} {s['city']})" for s in suggestions]
            selected_label = st.selectbox(T["select_certified"], labels, key="address_select")
            st.session_state["selected_address_label"] = selected_label
    else:
        dpe_number = st.text_input(T["dpe_number_label"], placeholder="Ex: 1234ABCD5678", key="dpe_input")
        st.caption(T["dpe_number_help"])
    
    if st.button(T["btn_analyze"], type="primary", use_container_width=True, key="analyze_btn"):
        if search_method == T["search_method_dpe"] and dpe_number:
            with st.spinner("🔍 Searching official DPE certificate..."):
                exact_property = fetch_by_dpe_number(dpe_number)
                if exact_property:
                    geo_data = ban_search(exact_property["address"], limit=1)
                    if geo_data:
                        exact_property["lat"] = geo_data[0]["lat"]
                        exact_property["lon"] = geo_data[0]["lon"]
                    st.session_state["confirmed_owner_property"] = exact_property
                    st.session_state["property_surface"] = exact_property.get("surface", 68)
                    st.success(T["exact_match_badge"])
                    st.rerun()
                else:
                    st.error(T["dpe_not_found"])
        elif search_method == T["search_method_address"] and search_query and st.session_state.get("address_suggestions"):
            selected_label = st.session_state.get("selected_address_label")
            suggestions = st.session_state["address_suggestions"]
            labels = [f"{s['label']} ({s['postcode']} {s['city']})" for s in suggestions]
            if selected_label and selected_label in labels:
                chosen_property = suggestions[labels.index(selected_label)]
                with st.spinner("Analyzing..."):
                    prop = fetch_single_property_ademe(
                        chosen_property["label"],
                        chosen_property["postcode"],
                        chosen_property["lat"],
                        chosen_property["lon"],
                        citycode=chosen_property.get("citycode", ""),
                    )
                    st.session_state["confirmed_owner_property"] = prop
                    st.session_state["property_surface"] = prop.get("surface", 68)
                    st.rerun()
            else:
                st.warning(T["select_address_warning"])
        else:
            st.warning(T["enter_input_warning"])
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    base_prop = st.session_state["confirmed_owner_property"]
    dpe_color = _DPE_COLORS.get(base_prop["dpe"], "#475569")
    
    # Show accuracy progress bar
    accuracy_progress_bar()
    
    # Show dynamic before/after section
    dynamic_before_after_section(
        base_prop["address"], 
        base_prop["dpe"], 
        st.session_state["property_surface"], 
        base_prop["lat"], 
        base_prop["lon"]
    )
    
    if st.button(T["btn_back"], key="back_btn"):
        st.session_state["confirmed_owner_property"] = None
        st.session_state["user_responses"] = None
        st.session_state["photos_uploaded"] = False
        st.session_state["accuracy_level"] = 1
        st.rerun()
    
    # Questionnaire (Level 2)
    if st.session_state.get("user_responses") is None:
        st.markdown("### 📋 Améliorez la précision")
        with st.form("acc_form"):
            windows = st.radio("Type de vitrage", ["Simple vitrage", "Double vitrage", "Triple vitrage", "Je ne sais pas"], horizontal=True)
            heating = st.radio("Système de chauffage", ["Gaz (ancien)", "Gaz (condensation)", "Électrique", "Pompe à chaleur", "Je ne sais pas"], horizontal=True)
            roof = st.radio("Toiture isolée ?", ["Oui", "Non", "Je ne sais pas"], horizontal=True)
            wall = st.radio("Murs isolés ?", ["Oui", "Non", "Je ne sais pas"], horizontal=True)
            if st.form_submit_button("Améliorer l'estimation"):
                st.session_state["user_responses"] = {"windows": windows, "heating": heating, "roof_insulation": roof, "wall_insulation": wall}
                st.session_state["accuracy_level"] = 2
                st.rerun()
    else:
        st.markdown(f"<div style='background:rgba(16,185,129,0.1); border-radius:16px; padding:12px; margin:10px 0'><span style='background:#22c55e; padding:5px 12px; border-radius:20px;'>✓ LEVEL 2</span> Questionnaire - Précision 85-90%</div>", unsafe_allow_html=True)
        
        # Photos (Level 3)
        if not st.session_state.get("photos_uploaded"):
            st.markdown("### 📸 Photos")
            with st.form("photo_form"):
                st.file_uploader("Photo de la facade", type=["jpg","png"], key="facade")
                if st.form_submit_button("Analyser les photos"):
                    st.session_state["photos_uploaded"] = True
                    st.session_state["accuracy_level"] = 3
                    st.rerun()
        else:
            st.markdown(f"<div style='background:rgba(16,185,129,0.1); border-radius:16px; padding:12px; margin:10px 0'><span style='background:#22c55e; padding:5px 12px; border-radius:20px;'>✓ LEVEL 3</span> Photos IA - Précision 90-95%</div>", unsafe_allow_html=True)
            st.markdown("""
            <div style="background:linear-gradient(135deg,rgba(59,130,246,0.1),rgba(16,185,129,0.05)); border-radius:20px; padding:20px; margin:10px 0; border:1px solid rgba(59,130,246,0.3)">
                <div style="display:flex; justify-content:space-between; flex-wrap:wrap"><div><strong>Audit Certifié</strong><br>99% précision</div><div><span style="font-size:28px; font-weight:800">€199</span></div></div>
                <button style="background:linear-gradient(135deg,#3B82F6,#10B981); border:none; padding:10px 20px; border-radius:50px; color:white; margin-top:15px">🎯 Commander</button>
            </div>
            """, unsafe_allow_html=True)
    
    # Enhanced ROI
    if st.session_state.get("user_responses"):
        enhanced_roi = calculate_enhanced_roi(base_prop, st.session_state["user_responses"])
        if enhanced_roi != base_prop.get("roi", 15.0):
            base_prop["roi"] = enhanced_roi
            st.session_state["confirmed_owner_property"] = base_prop
    
    # Property details
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<p class="section-label">{T["bilan_title"]}</p><div style="font-size:1.5rem; font-weight:800; margin-bottom:1rem;">{base_prop["address"][:60]}</div>', unsafe_allow_html=True)
    
    # Scenario selection
    st.markdown(f'<p>{T["choose_plan"]}</p>', unsafe_allow_html=True)
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        if st.button(T["eco_ess"], use_container_width=True): st.session_state["selected_scenario"] = "Essential"; st.rerun()
    with sc2:
        if st.button(T["conf_plus"], use_container_width=True): st.session_state["selected_scenario"] = "Plus"; st.rerun()
    with sc3:
        if st.button(T["carb_zero"], use_container_width=True): st.session_state["selected_scenario"] = "Zero"; st.rerun()
    
    current_scenario = st.session_state["selected_scenario"]
    active_cost = round(base_prop["cost"] * _SCENARIO_COST_MULTIPLIER[current_scenario], 0)
    active_roi = round(base_prop["roi"] * _SCENARIO_ROI_MULTIPLIER[current_scenario], 1)
    target_dpe = _SCENARIO_TARGET_DPE[current_scenario]
    
    # Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("DPE Actuel", base_prop["dpe"])
    m2.metric("Budget Estimé", f"€{active_cost:,.0f}")
    m3.metric("ROI Projeté", f"+{active_roi}%")
    
    # DPE progression
    dpe_seq = ["G","F","E","D","C","B","A"]
    if base_prop["dpe"] in dpe_seq and target_dpe in dpe_seq:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dpe_seq, y=[1]*7, mode='markers+text', text=dpe_seq, textposition="top center", marker=dict(size=22, color=["#ff0000","#ff3300","#ff6600","#f2b035","#ccff33","#33cc33","#319834"]), showlegend=False))
        fig.update_layout(height=100, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(visible=False), yaxis=dict(visible=False))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Financials
    st.markdown('<div class="card">', unsafe_allow_html=True)
    income = st.selectbox(T["income_label"], list(_INCOME_SUBSIDY_MAP.keys()), index=2)
    rate = _INCOME_SUBSIDY_MAP[income]
    if current_scenario == "Plus":
        rate = min(rate + 0.05, 0.85)
    elif current_scenario == "Zero":
        rate = min(rate + 0.12, 0.90)
    sub = round(active_cost * rate, 0)
    net = active_cost - sub
    st.metric("Subvention", f"€{sub:,.0f}", f"{int(rate*100)}%")
    st.metric("Reste à charge", f"€{net:,.0f}")
    years = st.slider(T["loan_duration"], 5, 20, 15)
    st.metric("Mensualité", f"€{net/(years*12):,.2f}/mois")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Map
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<p class="section-label">{T["map_title"]}</p>', unsafe_allow_html=True)
    m = folium.Map(location=[base_prop["lat"], base_prop["lon"]], zoom_start=17)
    folium.Marker([base_prop["lat"], base_prop["lon"]], icon=folium.Icon(color='green', icon='home')).add_to(m)
    st_folium(m, use_container_width=True, height=300, returned_objects=[])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Lead form
    if active_cost > 0:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("lead"):
            name = st.text_input(T["form_name"])
            phone = st.text_input(T["form_phone"])
            email = st.text_input(T["form_email"])
            if st.form_submit_button(T["form_btn"]):
                if name and phone and email:
                    st.success(T["form_success"])
                    save_lead(email, base_prop["address"], base_prop["dpe"], sub, active_roi)
                else:
                    st.error(T["form_err"])
        st.markdown('</div>', unsafe_allow_html=True)
    
    # PDF
    st.markdown('<div class="card">', unsafe_allow_html=True)
    try:
        pdf = generate_professional_pdf(base_prop, current_scenario, target_dpe, active_cost, net, sub, active_roi)
        st.download_button("📥 Télécharger le Rapport PDF", data=pdf, file_name=f"ZAMI_Report_{base_prop['zipcode']}.pdf", mime="application/pdf")
    except:
        st.info("PDF bientôt disponible")
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# AGENCY PORTAL BUTTON
# ─────────────────────────────────────────────
st.markdown("---")
c1, c2, c3 = st.columns([1,2,1])
with c2:
    if st.button("🏢 Agency Portal →", use_container_width=True, type="primary"):
        st.switch_page("pages/agency_dashboard.py")


# ─────────────────────────────────────────────
# ADMIN PANEL
# ─────────────────────────────────────────────
with st.expander("🔐 Admin Panel"):
    pwd = st.text_input("Password", type="password")
    if pwd == "ZAMI2026":
        st.success("Admin Access")
        tab1, tab2 = st.tabs(["💬 Messages", "📊 Leads"])
        with tab1:
            msgs = get_all_chat_messages()
            if msgs:
                st.dataframe(pd.DataFrame(msgs))
            else:
                st.info("No messages")
        with tab2:
            leads = get_all_leads()
            if leads:
                st.dataframe(pd.DataFrame(leads))
                st.download_button("Export CSV", pd.DataFrame(leads).to_csv(index=False), "leads.csv")
            else:
                st.info("No leads")
    elif pwd:
        st.error("Access Denied")


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown(f'<div class="footer">{T["footer"]}</div>', unsafe_allow_html=True)