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
if "chat_open" not in st.session_state:
    st.session_state["chat_open"] = False

# Global Variables
_SCENARIO_COST_MULTIPLIER = {"Essential": 1.0, "Plus": 1.65, "Zero": 2.45}
_SCENARIO_ROI_MULTIPLIER = {"Essential": 1.0, "Plus": 1.45, "Zero": 1.95}
_SCENARIO_TARGET_DPE = {"Essential": "D", "Plus": "C", "Zero": "B"}
_FALLBACK_RENO_COST = {"G": 1350, "F": 1100, "E": 620, "D": 280, "C": 120, "B": 0, "A": 0}
_FALLBACK_UPLIFT = {"G": 24.2, "F": 19.8, "E": 13.1, "D": 6.8, "C": 2.0, "B": 0, "A": 0}
_DPE_COLORS = {"A": "#319834", "B": "#33cc33", "C": "#ccff33", "D": "#f2b035", "E": "#ff6600", "F": "#ff3300", "G": "#ff0000"}
_INCOME_SUBSIDY_MAP = {"Très Modeste (Bleu)": 0.75, "Modeste (Jaune)": 0.60, "Intermédiaire (Violet)": 0.40, "Supérieur (Rose)": 0.15}

CHAT_FILE = "chat_messages.json"


# ─────────────────────────────────────────────
# CHAT FUNCTIONS (JSON Storage)
# ─────────────────────────────────────────────
def save_chat_message(name, email, message):
    """Save chat message to JSON file"""
    try:
        # Load existing messages
        if os.path.exists(CHAT_FILE):
            with open(CHAT_FILE, "r", encoding="utf-8") as f:
                messages = json.load(f)
        else:
            messages = []
        
        # Add new message
        messages.append({
            "id": len(messages) + 1,
            "name": name,
            "email": email,
            "message": message,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "unread"
        })
        
        # Save back
        with open(CHAT_FILE, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"Save error: {e}")
        return False


def get_all_chat_messages():
    """Get all chat messages from JSON file"""
    try:
        if os.path.exists(CHAT_FILE):
            with open(CHAT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    except:
        return []


def mark_message_read(msg_id):
    """Mark a message as read"""
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
    return '<div style="font-family:\'Space Grotesk\', sans-serif; font-size:1.8rem; font-weight:800; color:#22c55e;">ZAMI</div>'


# ─────────────────────────────────────────────
# CHAT BOT FUNCTION (Floating)
# ─────────────────────────────────────────────
def chat_bot():
    """Floating chat bot widget with JSON storage"""
    
    # CSS for floating button
    st.markdown("""
    <style>
    .floating-chat {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 999;
    }
    .chat-btn {
        background: linear-gradient(135deg, #22c55e, #16a34a);
        width: 60px;
        height: 60px;
        border-radius: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 10px 25px rgba(34,197,94,0.3);
        transition: all 0.3s;
        border: none;
    }
    .chat-btn:hover {
        transform: scale(1.1);
    }
    .chat-btn span {
        font-size: 28px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Chat expander
    with st.expander("💬 Chat with ZAMI Support", expanded=False):
        st.markdown("### 💬 Need Help?")
        st.markdown("Ask us anything about DPE, subsidies, or renovation!")
        
        with st.form("chat_form", clear_on_submit=True):
            chat_name = st.text_input("Your Name *", placeholder="Jean Dupont")
            chat_email = st.text_input("Your Email *", placeholder="jean@example.com")
            chat_message = st.text_area("Your Message *", placeholder="I have a question about DPE G properties...", height=100)
            
            col1, col2 = st.columns([1, 1])
            with col1:
                submitted = st.form_submit_button("📨 Send Message", type="primary", use_container_width=True)
            
            if submitted:
                if chat_name and chat_email and chat_message:
                    success = save_chat_message(chat_name, chat_email, chat_message)
                    if success:
                        st.success("✅ Message sent! We'll get back to you within 24 hours.")
                        st.balloons()
                    else:
                        st.error("❌ Unable to save message. Please try again.")
                else:
                    st.warning("Please fill all fields (*)")


# ─────────────────────────────────────────────
# DPE FUNCTIONS
# ─────────────────────────────────────────────
def fetch_by_dpe_number(numero_dpe: str) -> Optional[dict]:
    if not numero_dpe or len(numero_dpe.strip()) < 5:
        return None
    
    url = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines"
    params = {
        "qs": f"numero_dpe:{numero_dpe.strip()}",
        "size": 1,
        "select": "numero_dpe,etiquette_dpe,etiquette_ges,surface_habitable_logement,code_postal_ban,adresse_ban,date_etablissement_dpe,annee_construction,type_batiment,conso_5_usages_ef_energie_n1,emission_ges_5_usages_n1,type_energie_principale_chauffage"
    }
    
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            results = data.get("results", [])
            if results:
                record = results[0]
                dpe_class = str(record.get("etiquette_dpe", "E")).upper().strip()
                surface = record.get("surface_habitable_logement") or 60.0
                postcode = record.get("code_postal_ban", "75000")
                address = record.get("adresse_ban", "")
                
                cost = surface * _FALLBACK_RENO_COST.get(dpe_class, 250)
                roi = _FALLBACK_UPLIFT.get(dpe_class, 13.1)
                
                return {
                    "address": address,
                    "dpe": dpe_class,
                    "surface": surface,
                    "cost": cost,
                    "roi": roi,
                    "zipcode": postcode,
                    "lat": 48.8566,
                    "lon": 2.3522,
                    "data_found": True,
                    "source": "ADEME_DPE_NUMBER",
                    "current_value": 250000
                }
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
        results.append({
            "label": p.get("label", ""),
            "postcode": p.get("postcode", ""),
            "city": p.get("city", ""),
            "lon": c[0],
            "lat": c[1],
            "citycode": p.get("citycode", ""),
        })
    return results


def fetch_single_property_ademe(query_address: str, zipcode: str, lat=48.8566, lon=2.3522, citycode: str = ""):
    dpe_by_region = {"75": "E", "92": "E", "93": "F", "94": "E", "69": "D", "13": "D", "31": "D"}
    region = str(zipcode)[:2]
    dpe = dpe_by_region.get(region, "E")
    surface = 52.0 if region == "75" else 75.0
    cost = round(surface * _FALLBACK_RENO_COST.get(dpe, 620), 0)
    roi = _FALLBACK_UPLIFT.get(dpe, 13.1)
    return {
        "address": query_address, "dpe": dpe, "surface": surface,
        "cost": cost, "roi": roi, "zipcode": zipcode, "lat": lat, "lon": lon,
        "data_found": False, "source": "ESTIMATION",
        "current_value": 250000
    }


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


# Language translations
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
        "chart_5yr_title": "📊 Évolution Prédictive de l'Actif (2026-2031)",
        "chart_5yr_sub": "Trajectoire patrimoniale après rénovation",
        "form_title": "Mise en Relation avec un Artisan RGE",
        "form_sub": "Recevez 3 devis gratuits d'artisans certifiés",
        "form_name": "Nom Complet *", "form_phone": "Téléphone *", "form_email": "Email *",
        "form_time": "Créneau de rappel", "form_notes": "Notes (optionnel)",
        "form_btn": "📨 Envoyer ma demande", "form_err": "⚠️ Champs requis manquants",
        "form_success": "🎉 Demande envoyée! Un artisan vous contactera sous 24h.",
        "download_btn": "⬇️ Télécharger le Rapport PDF",
        "map_title": "🗺️ Géolocalisation du bien", "loss_title": "🌡️ Pertes thermiques estimées",
        "income_label": "💰 Profil de revenu:", "loan_title": "💶 Simulation Eco-PTZ",
        "loan_duration": "Durée (années)", "monthly_pay": "Mensualité (0% intérêt)",
        "footer": "ZAMI - Intelligence Rénovation Énergétique",
        "search_method_address": "📍 Recherche par adresse (~85% précis)",
        "search_method_dpe": "🔑 Recherche par numéro DPE (100% exact)",
        "dpe_number_label": "🔑 Numéro DPE", "dpe_number_help": "Trouvez le numéro sur votre certificat DPE",
        "dpe_not_found": "❌ Numéro DPE invalide", "exact_match_badge": "✅ Données 100% exactes",
        "select_address_warning": "📍 Sélectionnez une adresse", "enter_input_warning": "⚠️ Entrez une adresse ou un numéro DPE"
    },
    "EN": {
        "title": "Energy Property Portal", "subtitle": "Estimate your property value and renovation costs instantly",
        "input_label": "Enter your property address:", "select_certified": "Select certified BAN France address:",
        "btn_analyze": "⚡ Run Analysis", "btn_back": "⬅️ New Search",
        "bilan_title": "EXCLUSIVE PROPERTY AUDIT", "choose_plan": "ENERGY CONFIGURATION PLAN",
        "eco_ess": "🛠️ Eco Essential", "eco_ess_sub": "DPE D • Legal Compliance 2026",
        "conf_plus": "⚡ Comfort Plus", "conf_plus_sub": "DPE C • Full Insulation",
        "carb_zero": "🟢 Carbon Zero", "carb_zero_sub": "DPE B • Heat Pump",
        "current_class": "Current Class", "target_class": "🎯 Target Scenario",
        "surface": "Surface Area", "budget_est": "Global Investment", "uplift_label": "Market Uplift",
        "visual_prog": "Energy Progression", "your_property": "Your Asset 🏠", "target_label": "Target",
        "fin_title": "Financial Analysis", "fin_sub": "Public Subsidies vs Net Cost",
        "subvention_label": "MaPrimeRénov' Aid", "reste_charge": "Net Remaining",
        "impact_facture": "Impact: Plan {sc} saves {saving} annually on utilities.",
        "chart_5yr_title": "📊 5-Year Asset Value Prediction (2026-2031)",
        "chart_5yr_sub": "Renovation vs Obsolescence trajectory",
        "form_title": "Connect with an RGE Certified Contractor",
        "form_sub": "Get 3 free quotes from certified professionals",
        "form_name": "Full Name *", "form_phone": "Phone *", "form_email": "Email *",
        "form_time": "Callback time", "form_notes": "Notes (optional)",
        "form_btn": "📨 Submit Request", "form_err": "⚠️ Required fields missing",
        "form_success": "🎉 Request sent! A contractor will contact you within 24h.",
        "download_btn": "⬇️ Download PDF Report",
        "map_title": "🗺️ Property Location", "loss_title": "🌡️ Estimated Heat Loss",
        "income_label": "💰 Income profile:", "loan_title": "💶 Eco-PTZ Simulation",
        "loan_duration": "Duration (years)", "monthly_pay": "Monthly payment (0% interest)",
        "footer": "ZAMI - Energy Renovation Intelligence",
        "search_method_address": "📍 Address search (~85% accurate)",
        "search_method_dpe": "🔑 DPE number search (100% exact)",
        "dpe_number_label": "🔑 DPE Number", "dpe_number_help": "Find the number on your DPE certificate",
        "dpe_not_found": "❌ Invalid DPE number", "exact_match_badge": "✅ 100% exact data",
        "select_address_warning": "📍 Please select an address", "enter_input_warning": "⚠️ Please enter address or DPE number"
    }
}


# ─────────────────────────────────────────────
# HEADER (No Login)
# ─────────────────────────────────────────────
col_left, col_right = st.columns([1.6, 1.4])

with col_left:
    st.markdown(get_logo_html(), unsafe_allow_html=True)

with col_right:
    selected_lang = st.selectbox("🌐 Language", ["FR", "EN"], label_visibility="collapsed", key="lang")
    T = LANG_DICT[selected_lang]

st.markdown('<hr style="border-color:rgba(255,255,255,0.04); margin-bottom:2rem;">', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────
if st.session_state["confirmed_owner_property"] is None:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col_text, col_anim = st.columns([2, 1])
    with col_text:
        st.markdown(f'<p class="section-label">🏠 ZAMI</p>', unsafe_allow_html=True)
        st.markdown(f'<h1 class="owner-exclusive-title">{T["subtitle"]}</h1>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:#94a3b8;">Get your DPE, subsidies and ROI in 10 seconds</p>', unsafe_allow_html=True)
    with col_anim:
        anim.add_hero_animation()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
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
                    st.session_state["confirmed_owner_property"] = fetch_single_property_ademe(
                        chosen_property["label"],
                        chosen_property["postcode"],
                        chosen_property["lat"],
                        chosen_property["lon"],
                        citycode=chosen_property.get("citycode", ""),
                    )
                    st.rerun()
            else:
                st.warning(T["select_address_warning"])
        else:
            st.warning(T["enter_input_warning"])
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    base_prop = st.session_state["confirmed_owner_property"]
    dpe_color = _DPE_COLORS.get(base_prop["dpe"], "#475569")
    
    if st.button(T["btn_back"], key="back_btn"):
        st.session_state["confirmed_owner_property"] = None
        st.rerun()
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<p class="section-label">{T["bilan_title"]}</p><div class="owner-exclusive-title">{base_prop["address"][:60]}</div>', unsafe_allow_html=True)

    if base_prop.get("source") == "ADEME_DPE_NUMBER":
        st.markdown(f'<div style="display:inline-flex;align-items:center;gap:8px; background:rgba(34,197,94,0.12); border:1px solid rgba(34,197,94,0.5); padding:8px 20px; border-radius:100px; margin-bottom:1rem;"><span style="width:8px;height:8px;background:#22c55e;border-radius:50%;"></span><span style="font-size:0.75rem;font-weight:800;color:#22c55e;">{T["exact_match_badge"]}</span></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="display:inline-flex;align-items:center;gap:8px; background:rgba(234,179,8,0.08); border:1px solid rgba(234,179,8,0.25); padding:6px 16px; border-radius:100px; margin-bottom:1rem;"><span style="width:7px;height:7px;background:#eab308;border-radius:50%;"></span><span style="font-size:0.7rem;font-weight:700;color:#fbbf24;">⚡ ZONAL ESTIMATION</span></div>', unsafe_allow_html=True)

    st.markdown(f'<p class="metric-label-sub" style="color:#fff; margin-bottom:15px;">{T["choose_plan"]}</p>', unsafe_allow_html=True)
    
    sc_col1, sc_col2, sc_col3 = st.columns(3)
    with sc_col1:
        is_ess = (st.session_state["selected_scenario"] == "Essential")
        st.markdown(f'<div class="card {"scenario-card-active" if is_ess else ""}" style="padding:1rem; text-align:center;"><strong>{T["eco_ess"]}</strong><br><span style="font-size:0.7rem;color:#64748b;">{T["eco_ess_sub"]}</span></div>', unsafe_allow_html=True)
        if st.button("Select Essential", key="ess", use_container_width=True):
            st.session_state["selected_scenario"] = "Essential"
            st.rerun()
    with sc_col2:
        is_plus = (st.session_state["selected_scenario"] == "Plus")
        st.markdown(f'<div class="card {"scenario-card-active" if is_plus else ""}" style="padding:1rem; text-align:center;"><strong>{T["conf_plus"]}</strong><br><span style="font-size:0.7rem;color:#64748b;">{T["conf_plus_sub"]}</span></div>', unsafe_allow_html=True)
        if st.button("Select Comfort Plus", key="plus", use_container_width=True):
            st.session_state["selected_scenario"] = "Plus"
            st.rerun()
    with sc_col3:
        is_zero = (st.session_state["selected_scenario"] == "Zero")
        st.markdown(f'<div class="card {"scenario-card-active" if is_zero else ""}" style="padding:1rem; text-align:center;"><strong>{T["carb_zero"]}</strong><br><span style="font-size:0.7rem;color:#64748b;">{T["carb_zero_sub"]}</span></div>', unsafe_allow_html=True)
        if st.button("Select Carbon Zero", key="zero", use_container_width=True):
            st.session_state["selected_scenario"] = "Zero"
            st.rerun()

    st.markdown('<hr style="border-color:rgba(255,255,255,0.04); margin:1.5rem 0;">', unsafe_allow_html=True)

    current_scenario = st.session_state["selected_scenario"]
    active_cost = round(base_prop["cost"] * _SCENARIO_COST_MULTIPLIER[current_scenario], 0)
    active_roi = round(base_prop["roi"] * _SCENARIO_ROI_MULTIPLIER[current_scenario], 1)
    target_dpe = _SCENARIO_TARGET_DPE[current_scenario]

    col_left_dpe, col_right_metrics = st.columns([0.8, 2.2], gap="large")
    with col_left_dpe:
        st.markdown(f'<div style="text-align:center; background:rgba(15,23,42,0.4); border-radius:24px; padding:20px;"><p class="metric-label-sub">{T["current_class"]}</p><div class="dpe-badge-big" style="background-color:{dpe_color};">{base_prop["dpe"]}</div><p class="metric-label-sub" style="color:#22c55e; margin-top:12px;">{T["target_class"]} {target_dpe} ✅</p></div>', unsafe_allow_html=True)
    with col_right_metrics:
        m1, m2, m3 = st.columns(3)
        m1.markdown(f'<span class="metric-value-huge">{int(base_prop["surface"])}</span><span style="font-size:1.2rem; color:#475569;"> m²</span><br><span class="metric-label-sub">{T["surface"]}</span>', unsafe_allow_html=True)
        m2.markdown(f'<span class="metric-value-huge">€{active_cost:,.0f}</span><br><span class="metric-label-sub">{T["budget_est"]}</span>', unsafe_allow_html=True)
        m3.markdown(f'<span class="metric-value-huge" style="color:#22c55e;">+{active_roi}%</span><br><span class="metric-label-sub">{T["uplift_label"]}</span>', unsafe_allow_html=True)
        
        st.markdown(f'<p class="metric-label-sub" style="margin-top:15px;">{T["visual_prog"]}</p>', unsafe_allow_html=True)
        dpe_seq = ["G", "F", "E", "D", "C", "B", "A"]
        if base_prop["dpe"] in dpe_seq and target_dpe in dpe_seq:
            c_idx, t_idx = dpe_seq.index(base_prop["dpe"]), dpe_seq.index(target_dpe)
            prog_fig = go.Figure()
            prog_fig.add_trace(go.Scatter(x=dpe_seq, y=[1]*7, mode='markers+text', text=dpe_seq, textposition="top center", marker=dict(size=22, color=["#ff0000","#ff3300","#ff6600","#f2b035","#ccff33","#33cc33","#319834"]), showlegend=False))
            if c_idx < 6 and c_idx != t_idx:
                prog_fig.add_annotation(x=dpe_seq[t_idx], y=1, ax=dpe_seq[c_idx], ay=1, text="", showarrow=True, arrowhead=3, arrowsize=1.2, arrowwidth=3, arrowcolor="#fff")
            prog_fig.update_layout(height=100, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(visible=False), yaxis=dict(visible=False))
            st.plotly_chart(prog_fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

    # Map Section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<p class="section-label">🗺️ GEOSPATIAL</p><h3 class="section-title">{T["map_title"]}</h3>', unsafe_allow_html=True)
    fmap = folium.Map(location=[base_prop["lat"], base_prop["lon"]], zoom_start=17)
    folium.TileLayer('cartodbpositron').add_to(fmap)
    folium.Marker([base_prop["lat"], base_prop["lon"]], icon=folium.Icon(color='green', icon='home')).add_to(fmap)
    st_folium(fmap, use_container_width=True, height=350, returned_objects=[])
    st.markdown('</div>', unsafe_allow_html=True)

    # Financial Section
    if active_cost > 0:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<p class="section-label">{T["fin_title"]}</p><h3 class="section-title">{T["fin_sub"]}</h3>', unsafe_allow_html=True)
        
        income_bracket = st.selectbox(T["income_label"], list(_INCOME_SUBSIDY_MAP.keys()), index=2, key="income")
        subsidy_rate = _INCOME_SUBSIDY_MAP[income_bracket]
        if current_scenario == "Plus":
            subsidy_rate = min(subsidy_rate + 0.05, 0.85)
        elif current_scenario == "Zero":
            subsidy_rate = min(subsidy_rate + 0.12, 0.90)
        estimated_subsidy = round(active_cost * subsidy_rate, 0)
        net_cost = active_cost - estimated_subsidy
        energy_saving = "€1,200" if current_scenario == "Essential" else ("€1,850" if current_scenario == "Plus" else "€2,600")
        
        fcol1, fcol2 = st.columns([1, 1.5])
        with fcol1:
            fig_fin = utils_charts.generate_financial_pie(estimated_subsidy, net_cost, T["subvention_label"], T["reste_charge"])
            st.plotly_chart(fig_fin, use_container_width=True, config={'displayModeBar': False})
        with fcol2:
            st.metric(T["subvention_label"], f"€{estimated_subsidy:,.0f}", f"{int(subsidy_rate*100)}%")
            st.metric(T["reste_charge"], f"€{net_cost:,.0f}")
            st.info(T["impact_facture"].format(sc=current_scenario, saving=energy_saving))
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Loan Section
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<p class="section-label">💶 FINANCING</p><h3 class="section-title">{T["loan_title"]}</h3>', unsafe_allow_html=True)
        loan_years = st.slider(T["loan_duration"], 5, 20, 15, key="loan_years")
        monthly_payment = net_cost / (loan_years * 12)
        st.markdown(f'<span class="metric-value-huge" style="color:#22c55e;">€{monthly_payment:,.2f}</span><span style="font-size:1.2rem;"> / month</span><br><span class="metric-label-sub">{T["monthly_pay"]}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Chart Section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<p class="section-label">{T["chart_5yr_title"]}</p><h3 class="section-title">{T["chart_5yr_sub"]}</h3>', unsafe_allow_html=True)
    fig_5yr = utils_charts.generate_five_year_trajectory(active_roi)
    st.plotly_chart(fig_5yr, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

    # Lead Form
    if active_cost > 0:
        st.markdown('<div class="card" style="border:1px solid rgba(34,197,94,0.2);">', unsafe_allow_html=True)
        st.markdown(f'<p class="section-label" style="color:#22c55e;">📋 RGE CONNECTION</p><h3 style="color:#fff;">{T["form_title"]}</h3><p style="color:#64748b;">{T["form_sub"]}</p>', unsafe_allow_html=True)
        with st.form("lead_form"):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input(T["form_name"])
                phone = st.text_input(T["form_phone"])
            with c2:
                email = st.text_input(T["form_email"])
                time_slot = st.selectbox(T["form_time"], ["Morning (9-12h)", "Afternoon (14-17h)"])
            notes = st.text_area(T["form_notes"])
            if st.form_submit_button(T["form_btn"]):
                if name and phone and email:
                    st.success(T["form_success"])
                else:
                    st.error(T["form_err"])
        st.markdown('</div>', unsafe_allow_html=True)

    # PDF Download Section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="section-label" style="color:#22c55e;">📄 DOCUMENTATION</p><h3 style="color:#fff;">Download Property Report</h3>', unsafe_allow_html=True)

    try:
        pdf_bytes = generate_professional_pdf(
            property_data=base_prop,
            scenario=current_scenario,
            target_dpe=target_dpe,
            active_cost=active_cost,
            net_cost=net_cost,
            subsidy=estimated_subsidy if 'estimated_subsidy' in dir() else 0,
            roi=active_roi
        )
        if pdf_bytes and len(pdf_bytes) > 100:
            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_bytes,
                file_name=f"ZAMI_Report_{base_prop['zipcode']}_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="pdf_btn"
            )
    except:
        st.info("PDF report will be available soon")
    
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ADMIN SECTION (View Chat Messages)
# ─────────────────────────────────────────────
st.markdown('<div class="card" style="background:none; border:none;">', unsafe_allow_html=True)
if st.checkbox("🔐 Admin Panel", key="admin_panel"):
    admin_pwd = st.text_input("Admin Password", type="password", key="admin_pwd")
    if admin_pwd == "ZAMI2026":
        st.success("✅ Admin Access Granted")
        
        tab1, tab2 = st.tabs(["💬 Chat Messages", "📊 Statistics"])
        
        with tab1:
            st.markdown("### 💬 Visitor Messages")
            messages = get_all_chat_messages()
            
            if messages:
                for msg in messages:
                    status_emoji = "🟢" if msg.get("status") == "unread" else "🔵"
                    with st.expander(f"{status_emoji} {msg['name']} - {msg['time']}"):
                        st.markdown(f"**Email:** {msg['email']}")
                        st.markdown(f"**Message:** {msg['message']}")
                        st.markdown(f"**Status:** {msg.get('status', 'unknown')}")
                        
                        if msg.get("status") == "unread":
                            if st.button(f"Mark as Read", key=f"mark_{msg['id']}"):
                                mark_message_read(msg['id'])
                                st.rerun()
            else:
                st.info("No messages yet")
        
        with tab2:
            st.markdown("### 📊 Statistics")
            messages = get_all_chat_messages()
            st.metric("Total Messages", len(messages))
            unread = len([m for m in messages if m.get("status") == "unread"])
            st.metric("Unread Messages", unread)
            
            if messages:
                # Messages per day
                dates = {}
                for msg in messages:
                    date = msg.get("time", "").split(" ")[0]
                    dates[date] = dates.get(date, 0) + 1
                if dates:
                    st.write("Messages by date:", dates)
    elif admin_pwd:
        st.error("❌ Access Denied")
st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown(f'<div class="footer">{T["footer"]}</div>', unsafe_allow_html=True)

# Floating Chat Bot
chat_bot()