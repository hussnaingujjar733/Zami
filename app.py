import os
import json
import time
import requests
import streamlit as st
import pandas as pd
from datetime import datetime
import folium
from streamlit_folium import st_folium

# ── ⚡ MUST BE FIRST COMMAND ──
st.set_page_config(page_title="ZAMI - Property Intelligence", page_icon="🏠", layout="wide", initial_sidebar_state="collapsed")

# ── ⚡ IMPORT MODULES ──
import utils_styles
import utils_animations
try:
    from reportlab_generator import generer_rapport
except ImportError:
    pass 

# ── ⚡ INJECT PREMIUM CSS ──
utils_styles.inject_premium_styles()

# ─────────────────────────────────────────────
# CHECK FOR ADMIN MODE
# ─────────────────────────────────────────────
admin_val = st.query_params.get("admin", "false")
if str(admin_val).lower() == "true":
    st.session_state.admin_mode = True
else:
    st.session_state.admin_mode = False

# ─────────────────────────────────────────────
# LEAD STORAGE FUNCTION
# ─────────────────────────────────────────────
LEADS_FILE = "leads.json"

def save_lead(lead_data):
    try:
        if os.path.exists(LEADS_FILE):
            with open(LEADS_FILE, "r", encoding="utf-8") as f:
                leads = json.load(f)
        else:
            leads = []
        
        leads.append({
            "id": len(leads) + 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **lead_data,
            "status": "new"
        })
        
        with open(LEADS_FILE, "w", encoding="utf-8") as f:
            json.dump(leads, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Save error: {e}")
        return False

# ─────────────────────────────────────────────
# ADMIN MODE - Show Admin Panel
# ─────────────────────────────────────────────
if st.session_state.admin_mode:
    st.markdown("""
    <style>
    .admin-header {
        background: linear-gradient(135deg, #064e3b, #022c22);
        border-radius: 20px;
        padding: 30px 20px;
        text-align: center;
        margin-bottom: 30px;
        border: 1px solid #34d399;
        box-shadow: 0 10px 25px rgba(52, 211, 153, 0.1);
    }
    .admin-header h1 { color: #34d399; margin-bottom: 10px; font-weight: 800;}
    .admin-header p { color: #a7f3d0; font-size: 1.1rem;}
    .back-btn {
        position: fixed;
        top: 20px;
        left: 20px;
        background: #1e293b;
        border: 1px solid #34d399;
        color: white;
        text-decoration: none;
        border-radius: 50px;
        padding: 10px 20px;
        font-weight: bold;
        z-index: 9999;
        transition: all 0.3s ease;
    }
    .back-btn:hover { background: #34d399; color: black; }
    </style>
    
    <a href="/" class="back-btn" target="_self">← Retour à l'accueil</a>
    
    <div class="admin-header">
        <h1>🔐 ZAMI Intelligence - Admin Panel</h1>
        <p>Gestion sécurisée des leads clients et analyses</p>
    </div>
    """, unsafe_allow_html=True)
    
    if "admin_auth" not in st.session_state:
        st.session_state.admin_auth = False
    
    if not st.session_state.admin_auth:
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align:center;'>🔑 Accès Restreint</h3>", unsafe_allow_html=True)
            pwd = st.text_input("Mot de passe", type="password")
            if st.button("Se connecter", type="primary", use_container_width=True):
                if pwd == "ZAMI2026":
                    st.session_state.admin_auth = True
                    st.rerun()
                else:
                    st.error("❌ Mot de passe incorrect")
            st.markdown("</div>", unsafe_allow_html=True)
        st.stop()
    
    st.success("✅ Accès autorisé - Bienvenue dans le centre de contrôle ZAMI.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        if os.path.exists(LEADS_FILE):
            with open(LEADS_FILE, "r", encoding="utf-8") as f:
                leads_data = json.load(f)
            total = len(leads_data)
            new = len([l for l in leads_data if l.get("status") == "new"])
            c1, c2 = st.columns(2)
            c1.metric("📊 Total Leads", total)
            c2.metric("🆕 Nouveaux Leads", new, delta="Action requise", delta_color="inverse")
        else:
            st.metric("📊 Total Leads", "0")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.markdown("### 📈 Distribution DPE")
        if os.path.exists(LEADS_FILE):
            dpe_counts = {}
            for lead in leads_data:
                dpe = lead.get("dpe", "Inconnu")
                dpe_counts[dpe] = dpe_counts.get(dpe, 0) + 1
            if dpe_counts:
                for dpe, count in sorted(dpe_counts.items()):
                    st.write(f"**DPE {dpe}:** {count} propriétés")
        else:
            st.write("Aucune donnée disponible.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("### 📋 Base de Données Clients")
    if os.path.exists(LEADS_FILE) and leads_data:
        df = pd.DataFrame(leads_data)
        st.dataframe(df, use_container_width=True, height=400)
    else:
        st.info("La base de données est actuellement vide.")
    st.stop()

# ─────────────────────────────────────────────
# STYLISH ADMIN BUTTON (TOP RIGHT CORNER)
# ─────────────────────────────────────────────
st.markdown("""
<style>
.admin-btn-container { position: fixed; top: 15px; right: 20px; z-index: 9999; }
.admin-btn {
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(56, 189, 248, 0.4);
    border-radius: 50px;
    padding: 8px 16px;
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    text-decoration: none;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}
.admin-btn:hover { border-color: #38bdf8; transform: translateY(-2px); background: rgba(15, 23, 42, 0.9); }
.admin-text { font-size: 12px; font-weight: 700; color: #e2e8f0; letter-spacing: 1px; }
</style>
<div class="admin-btn-container">
    <a href="?admin=true" target="_self" style="text-decoration: none;">
        <div class="admin-btn">
            <span>🔐</span>
            <span class="admin-text">ADMIN</span>
        </div>
    </a>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# STATE INITIALIZATION
# ─────────────────────────────────────────────
if "property_data" not in st.session_state: st.session_state.property_data = None
if "address_suggestions" not in st.session_state: st.session_state.address_suggestions = []
if "user_responses" not in st.session_state: st.session_state.user_responses = None
if "step" not in st.session_state: st.session_state.step = "address"
if "wizard_step" not in st.session_state: st.session_state.wizard_step = 1

_FALLBACK_RENO_COST = {"G": 1350, "F": 1100, "E": 620, "D": 280, "C": 120, "B": 0, "A": 0}
_FALLBACK_UPLIFT = {"G": 24.2, "F": 19.8, "E": 13.1, "D": 6.8, "C": 2.0, "B": 0, "A": 0}

# ─────────────────────────────────────────────
# DPE & API FUNCTIONS
# ─────────────────────────────────────────────
def safe_get(url, params=None):
    try:
        r = requests.get(url, params=params, timeout=10)
        return r.json()
    except:
        return None

def ban_search(query: str, limit: int = 5):
    if not query or len(query.strip()) < 3: return []
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
            "lon": c[0], "lat": c[1],
        })
    return results

def fetch_base_property_data(selected_address):
    zipcode = selected_address["postcode"]
    region = str(zipcode)[:2]
    dpe_by_region = {"75": "E", "92": "E", "93": "F", "94": "E", "69": "D", "13": "D", "31": "D"}
    dpe = dpe_by_region.get(region, "E")
    surface = 52.0 if region == "75" else 75.0
    cost = round(surface * _FALLBACK_RENO_COST.get(dpe, 620), 0)
    roi = _FALLBACK_UPLIFT.get(dpe, 13.1)
    return {
        "address": selected_address["label"],
        "dpe": dpe, "surface": surface, "cost": cost, "roi": roi,
        "zipcode": zipcode, "lat": selected_address["lat"], "lon": selected_address["lon"],
    }

# ─────────────────────────────────────────────
# UI COMPONENTS
# ─────────────────────────────────────────────
def hero_section():
    st.markdown("""
    <style>
    .hero-container {
        background: radial-gradient(circle at top right, #1e3a8a 0%, #020617 60%);
        border-radius: 24px;
        padding: 50px 20px;
        text-align: center;
        margin-bottom: 40px;
        border: 1px solid rgba(56, 189, 248, 0.2);
        box-shadow: 0 15px 40px rgba(0,0,0,0.4);
    }
    .hero-logo-text {
        font-size: 4.5rem;
        font-weight: 900;
        letter-spacing: -1px;
        background: linear-gradient(to right, #38bdf8, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
        line-height: 1;
    }
    .hero-title {
        font-size: 2.2rem;
        color: #f8fafc;
        font-weight: 700;
        margin-top: 15px;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        max-width: 600px;
        margin: 15px auto;
    }
    </style>
    <div class="hero-container">
        <div class="hero-logo-text">ZAMI</div>
        <div class="hero-title">L'Intelligence Artificielle au service de votre Rénovation</div>
        <div class="hero-subtitle">Analysez le potentiel de votre bien, découvrez vos subventions et maximisez votre ROI instantanément.</div>
    </div>
    """, unsafe_allow_html=True)

def display_premium_map(lat, lon):
    m = folium.Map(location=[lat, lon], zoom_start=17, tiles="CartoDB dark_matter", control_scale=True)
    folium.Marker(
        [lat, lon], popup="<b>Propriété Analysée</b>",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)
    st_folium(m, height=300, use_container_width=True, returned_objects=[])

# ─────────────────────────────────────────────
# MAIN APP FLOW
# ─────────────────────────────────────────────
hero_section()

# STEP 1: Address
if st.session_state.step == "address":
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-header">📍 Étape 1 : Localisez votre bien</div>', unsafe_allow_html=True)
    
    search_query = st.text_input("Saisissez votre adresse postale", placeholder="Ex: 10 Rue de la Paix, Paris", key="address_input")
    
    if search_query and len(search_query.strip()) >= 3:
        suggestions = ban_search(search_query)
        st.session_state.address_suggestions = suggestions
    
    if st.session_state.address_suggestions:
        labels = [f"{s['label']} ({s['postcode']} {s['city']})" for s in st.session_state.address_suggestions]
        selected_label = st.selectbox("Sélectionnez l'adresse exacte", labels, key="address_select")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Démarrer l'Analyse IA", type="primary", use_container_width=True):
            loader_placeholder = st.empty()
            with loader_placeholder:
                utils_animations.ai_analyzing_animation()
                time.sleep(2) # Fake delay for effect
            
            for s in st.session_state.address_suggestions:
                if f"{s['label']} ({s['postcode']} {s['city']})" == selected_label:
                    st.session_state.property_data = fetch_base_property_data(s)
                    st.session_state.step = "questions"
                    st.session_state.wizard_step = 1
            
            loader_placeholder.empty()
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 2: Wizard
elif st.session_state.step == "questions":
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-header">🎯 Étape 2 : Affinons l\'analyse</div>', unsafe_allow_html=True)
    
    if st.session_state.user_responses is None: st.session_state.user_responses = {}
    st.progress(st.session_state.wizard_step / 3)
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.session_state.wizard_step == 1:
        st.subheader("🪟 Quel type de vitrage possède le bien ?")
        win_val = st.radio("Sélectionnez une option :", ["Simple vitrage", "Double vitrage", "Je ne sais pas"], key="win")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Continuer ➡️", type="primary", use_container_width=True):
            st.session_state.user_responses["windows"] = win_val
            st.session_state.wizard_step = 2
            st.rerun()
            
    elif st.session_state.wizard_step == 2:
        st.subheader("🔥 Quel est le système de chauffage principal ?")
        heat_val = st.radio("Sélectionnez une option :", ["Gaz ancien", "Électrique (Convecteurs)", "Pompe à chaleur", "Je ne sais pas"], key="heat")
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("⬅️ Précédent", use_container_width=True):
                st.session_state.wizard_step = 1
                st.rerun()
        with c2:
            if st.button("Continuer ➡️", type="primary", use_container_width=True):
                st.session_state.user_responses["heating"] = heat_val
                st.session_state.wizard_step = 3
                st.rerun()

    elif st.session_state.wizard_step == 3:
        st.subheader("🧱 État de l'isolation actuelle")
        cA, cB = st.columns(2)
        with cA: roof_val = st.radio("Toiture isolée ?", ["Oui", "Non", "Je ne sais pas"], key="roof")
        with cB: wall_val = st.radio("Murs isolés ?", ["Oui", "Non", "Je ne sais pas"], key="wall")
        st.markdown("<br>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("⬅️ Précédent", use_container_width=True):
                st.session_state.wizard_step = 2
                st.rerun()
        with c2:
            if st.button("📊 Générer le Rapport Final", type="primary", use_container_width=True):
                st.session_state.user_responses["roof_insulation"] = roof_val
                st.session_state.user_responses["wall_insulation"] = wall_val
                st.session_state.step = "report"
                st.rerun()
                
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("⏩ Passer les questions (Estimation IA standard)", use_container_width=True):
        st.session_state.user_responses = None
        st.session_state.step = "report"
        st.rerun()

# STEP 3: Report & Lead Capture
elif st.session_state.step == "report":
    prop = st.session_state.property_data
    
    # Report Card
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-header">📄 Rapport d\'Intelligence ZAMI</div>', unsafe_allow_html=True)
    
    st.markdown(f"**📍 Bien localisé :** {prop['address']}")
    display_premium_map(prop["lat"], prop["lon"])
    
    # Render Premium Dashboard Metrics
    utils_animations.display_premium_metrics(prop['dpe'], prop['surface'], prop['cost'], prop['roi'])
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    
    # Download Button
    try:
        pdf_bytes = None
        if "generer_rapport" in globals():
            with st.spinner("Préparation de votre document certifié..."):
                pdf_bytes = generer_rapport(prop)
        
        if pdf_bytes:
            st.download_button(
                label="⬇️ TÉLÉCHARGER LE DOSSIER COMPLET (PDF)",
                data=pdf_bytes,
                file_name=f"ZAMI_Audit_{prop['zipcode']}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
    except Exception as e:
        pass
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Lead Capture Form
    st.markdown('<div class="premium-card" style="border: 1px solid #34d399;">', unsafe_allow_html=True)
    st.markdown("<h3 style='color: #34d399; text-align: center;'>🛠️ Passez à l'action avec des experts RGE</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #cbd5e1; margin-bottom: 20px;'>Recevez 3 devis qualifiés d'artisans locaux pour concrétiser votre projet.</p>", unsafe_allow_html=True)
    
    with st.form("lead_form"):
        c1, c2 = st.columns(2)
        with c1:
            nom = st.text_input("Nom & Prénom *", placeholder="Ex: Jean Dupont")
            email = st.text_input("Adresse Email *", placeholder="jean.dupont@email.com")
        with c2:
            telephone = st.text_input("Téléphone *", placeholder="06 12 34 56 78")
            
        st.markdown("<br>", unsafe_allow_html=True)
        submit = st.form_submit_button("Demander mes devis gratuits", type="primary", use_container_width=True)
        
        if submit:
            if not nom or not email or not telephone:
                st.error("⚠️ Veuillez remplir tous les champs obligatoires.")
            else:
                lead_data = {
                    "address": prop['address'], "zipcode": prop['zipcode'], "dpe": prop['dpe'],
                    "surface": prop['surface'], "cost": prop['cost'], "roi": prop['roi'],
                    "name": nom, "email": email, "phone": telephone
                }
                if save_lead(lead_data):
                    st.success("✅ Félicitations ! Votre demande est validée. Un conseiller ZAMI vous contactera sous 24h.")
                    st.balloons()
                else:
                    st.error("❌ Une erreur est survenue.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔍 Lancer une nouvelle analyse", use_container_width=True):
        st.session_state.step = "address"
        st.session_state.property_data = None
        st.session_state.wizard_step = 1
        st.rerun()

# Modern Footer
st.markdown("""
<div style='text-align: center; color: #475569; padding: 20px; font-size: 0.9rem; font-weight: 500;'>
    &copy; 2026 ZAMI Intelligence. L'expertise data au service de l'immobilier Français.
</div>
""", unsafe_allow_html=True)