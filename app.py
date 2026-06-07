import os
import json
import time
import requests
import streamlit as st
import pandas as pd
from datetime import datetime
import folium
from streamlit_folium import st_folium

# ── ⚡ IMPORT MODULES ──
import utils_styles
from reportlab_generator import generer_rapport

# ─────────────────────────────────────────────
# LEAD STORAGE FUNCTION (JSON)
# ─────────────────────────────────────────────
LEADS_FILE = "leads.json"

def save_lead(lead_data):
    """Save lead to JSON file"""
    try:
        if os.path.exists(LEADS_FILE):
            with open(LEADS_FILE, "r", encoding="utf-8") as f:
                leads = json.load(f)
        else:
            leads = []
        
        leads.append({
            "id": len(leads) + 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": lead_data.get("name"),
            "email": lead_data.get("email"),
            "phone": lead_data.get("phone"),
            "address": lead_data.get("address"),
            "zipcode": lead_data.get("zipcode"),
            "dpe": lead_data.get("dpe"),
            "surface": lead_data.get("surface"),
            "cost": lead_data.get("cost"),
            "roi": lead_data.get("roi"),
            "status": "new"
        })
        
        with open(LEADS_FILE, "w", encoding="utf-8") as f:
            json.dump(leads, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Save error: {e}")
        return False

# Run Premium Style Injections
utils_styles.inject_premium_styles()

# Hide sidebar
st.markdown("""
<style>
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stSidebarNav"] { display: none !important; }
    [data-testid="stSidebarCollapsedControl"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CHECK FOR ADMIN MODE (via query parameter)
# ─────────────────────────────────────────────
query_params = st.query_params
if query_params.get("admin") == "true":
    st.session_state.admin_mode = True
else:
    st.session_state.admin_mode = False

# ─────────────────────────────────────────────
# ADMIN MODE - Show Admin Panel
# ─────────────────────────────────────────────
if st.session_state.admin_mode:
    st.markdown("""
    <style>
    .admin-header {
        background: linear-gradient(135deg, #0F172A, #020617);
        border-radius: 28px;
        padding: 30px 20px;
        text-align: center;
        margin-bottom: 30px;
        border: 1px solid rgba(34,197,94,0.3);
    }
    .admin-header h1 {
        color: #22c55e;
        margin-bottom: 10px;
    }
    .admin-header p {
        color: #94a3b8;
    }
    .back-btn {
        position: fixed;
        top: 20px;
        left: 20px;
        background: linear-gradient(135deg, #1E293B, #0F172A);
        border: 1px solid rgba(34,197,94,0.3);
        border-radius: 50px;
        padding: 8px 18px;
        cursor: pointer;
        z-index: 9999;
        transition: all 0.3s ease;
    }
    .back-btn:hover {
        border-color: #22c55e;
        transform: translateY(-2px);
    }
    </style>
    
    <div class="back-btn" id="backBtn">
        <span>← Retour à l'accueil</span>
    </div>
    <script>
        document.getElementById('backBtn').onclick = function() {
            window.location.href = window.location.pathname;
        };
    </script>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="admin-header">
        <h1>🔐 ZAMI - Panneau Administrateur</h1>
        <p>Gestion sécurisée des leads clients</p>
    </div>
    """, unsafe_allow_html=True)
    
    if "admin_auth" not in st.session_state:
        st.session_state.admin_auth = False
    
    if not st.session_state.admin_auth:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🔑 Accès Administrateur")
            pwd = st.text_input("Mot de passe", type="password")
            if st.button("🔐 Se connecter", type="primary", use_container_width=True):
                if pwd == "ZAMI2026":
                    st.session_state.admin_auth = True
                    st.rerun()
                else:
                    st.error("❌ Mot de passe incorrect")
        st.stop()
    
    st.success("✅ Accès autorisé - Bienvenue Administrateur")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if os.path.exists(LEADS_FILE):
            with open(LEADS_FILE, "r", encoding="utf-8") as f:
                leads_data = json.load(f)
            total = len(leads_data)
            new = len([l for l in leads_data if l.get("status") == "new"])
            st.metric("📊 Total Leads", total)
            st.metric("🆕 Nouveaux Leads", new)
        else:
            st.metric("📊 Total Leads", "0")
            st.metric("🆕 Nouveaux Leads", "0")
    
    with col2:
        st.markdown("### 📈 Statistiques")
        if os.path.exists(LEADS_FILE):
            with open(LEADS_FILE, "r", encoding="utf-8") as f:
                leads_data = json.load(f)
            dpe_counts = {}
            for lead in leads_data:
                dpe = lead.get("dpe", "Inconnu")
                dpe_counts[dpe] = dpe_counts.get(dpe, 0) + 1
            if dpe_counts:
                st.write("**Distribution par DPE:**")
                for dpe, count in dpe_counts.items():
                    st.write(f"- DPE {dpe}: {count} leads")
            else:
                st.info("Aucune donnée DPE")
        else:
            st.info("Aucune donnée disponible")
    
    st.markdown("---")
    st.markdown("### 📋 Liste complète des leads")
    
    if os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, "r", encoding="utf-8") as f:
            leads_data = json.load(f)
        
        if leads_data:
            df = pd.DataFrame(leads_data)
            st.dataframe(df, use_container_width=True, height=500)
            
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Exporter en CSV",
                data=csv,
                file_name=f"zami_leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True,
                type="primary"
            )
            st.info(f"📊 Total: {len(leads_data)} leads capturés")
        else:
            st.info("Aucun lead capturé pour le moment")
    else:
        st.info("Aucun fichier de leads trouvé")
    
    st.stop()

# ─────────────────────────────────────────────
# STYLISH ADMIN BUTTON (TOP RIGHT CORNER)
# ─────────────────────────────────────────────
st.markdown("""
<style>
.admin-btn-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
}

.admin-btn {
    background: linear-gradient(135deg, #1E293B, #0F172A);
    border: 1px solid rgba(34, 197, 94, 0.3);
    border-radius: 50px;
    padding: 8px 18px;
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.admin-btn:hover {
    border-color: #22c55e;
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(34, 197, 94, 0.15);
}

.admin-icon {
    font-size: 16px;
}

.admin-text {
    font-size: 12px;
    font-weight: 600;
    color: #CBD5E1;
    letter-spacing: 0.5px;
}
</style>

<div class="admin-btn-container">
    <div class="admin-btn" id="adminBtn">
        <span class="admin-icon">🔐</span>
        <span class="admin-text">ADMIN</span>
    </div>
</div>

<script>
    document.getElementById('adminBtn').onclick = function() {
        window.location.href = window.location.pathname + '?admin=true';
    };
</script>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# STATE INITIALIZATION
# ─────────────────────────────────────────────
if "property_data" not in st.session_state:
    st.session_state.property_data = None
if "address_suggestions" not in st.session_state:
    st.session_state.address_suggestions = []
if "user_responses" not in st.session_state:
    st.session_state.user_responses = None
if "step" not in st.session_state:
    st.session_state.step = "address"
if "wizard_step" not in st.session_state:
    st.session_state.wizard_step = 1
if "lead_submitted" not in st.session_state:
    st.session_state.lead_submitted = False

# Global Variables
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
        "dpe": dpe,
        "surface": surface,
        "cost": cost,
        "roi": roi,
        "zipcode": zipcode,
        "lat": selected_address["lat"],
        "lon": selected_address["lon"],
    }

# ─────────────────────────────────────────────
# UI COMPONENTS
# ─────────────────────────────────────────────
def hero_section():
    st.markdown("""
    <style>
    .hero-small {
        background: linear-gradient(135deg, #0F172A, #020617);
        border-radius: 28px;
        padding: 35px 20px 25px 20px;
        text-align: center;
        margin-bottom: 35px;
        border: 1px solid rgba(59,130,246,0.2);
    }
    .hero-logo-text {
        font-size: 3.8rem;
        font-weight: 800;
        font-family: 'Space Grotesk', sans-serif;
        background: linear-gradient(135deg, #F8FAFC, #3B82F6, #10B981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    .hero-tagline {
        font-size: 0.7rem;
        letter-spacing: 0.15em;
        color: #3B82F6;
        text-transform: uppercase;
        margin-bottom: 25px;
    }
    .hero-title-fr {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #F8FAFC, #CBD5E1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .hero-subtitle-fr {
        font-size: 0.9rem;
        color: #94A3B8;
        max-width: 500px;
        margin: 0 auto 20px auto;
    }
    .hero-features {
        display: flex;
        justify-content: center;
        gap: 25px;
        flex-wrap: wrap;
        margin-top: 15px;
        padding-top: 15px;
        border-top: 1px solid rgba(255,255,255,0.05);
    }
    .hero-feature {
        font-size: 0.8rem;
        color: #CBD5E1;
    }
    @media (max-width: 768px) {
        .hero-logo-text { font-size: 2.2rem; }
        .hero-title-fr { font-size: 1.3rem; }
    }
    </style>
    
    <div class="hero-small">
        <div class="hero-logo-text">ZAMI</div>
        <div class="hero-tagline">⚡ FRANCE'S #1 RENOVATION INTELLIGENCE</div>
        <div class="hero-title-fr">L'avenir de la rénovation immobilière</div>
        <div class="hero-subtitle-fr">Entrez votre adresse et recevez votre rapport personnalisé</div>
        <div class="hero-features">
            <span class="hero-feature">✓ Subventions disponibles</span>
            <span class="hero-feature">✓ ROI de rénovation</span>
            <span class="hero-feature">✓ Conformité légale</span>
            <span class="hero-feature">✓ Plus-value immobilière</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_skeleton_loader():
    return """
    <style>
    .skeleton-box {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        margin-bottom: 15px;
    }
    </style>
    <div class="card" style="padding: 30px; margin-top: 20px;">
        <div style="display: flex; gap: 20px; align-items: center; margin-bottom: 30px;">
            <div class="skeleton-box shimmer-effect" style="height: 80px; width: 80px; border-radius: 50%;"></div>
            <div style="flex: 1;">
                <div class="skeleton-box shimmer-effect" style="height: 25px; width: 60%;"></div>
                <div class="skeleton-box shimmer-effect" style="height: 15px; width: 40%;"></div>
            </div>
        </div>
        <div class="skeleton-box shimmer-effect" style="height: 120px; width: 100%;"></div>
        <div style="text-align: center; margin-top: 25px;">
            <span style="color: #3B82F6; font-size: 0.9rem; font-weight: 600; animation: pulse 1.5s infinite;">⚡ ZAMI AI analyse les données ADEME & DVF...</span>
        </div>
    </div>
    """

def display_premium_map(lat, lon):
    st.markdown("<div class='section-label' style='margin-top: 20px;'>Vue Satellite ZAMI</div>", unsafe_allow_html=True)
    m = folium.Map(location=[lat, lon], zoom_start=16, tiles="CartoDB dark_matter", control_scale=True)
    folium.Marker(
        [lat, lon],
        popup="<b>ZAMI Analyzed Property</b>",
        icon=folium.Icon(color="green", icon="bolt", prefix='fa')
    ).add_to(m)
    st_folium(m, height=350, use_container_width=True, returned_objects=[])

# ─────────────────────────────────────────────
# MAIN APP FLOW
# ─────────────────────────────────────────────
hero_section()

# STEP 1: Address Selection
if st.session_state.step == "address":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📍 Étape 1 : Entrez votre adresse")
    
    search_query = st.text_input("Adresse", placeholder="Ex: 39 Rue du Sergent Bobillot, Montreuil", key="address_input")
    
    if search_query and len(search_query.strip()) >= 3:
        suggestions = ban_search(search_query)
        st.session_state.address_suggestions = suggestions
    
    if st.session_state.address_suggestions:
        labels = [f"{s['label']} ({s['postcode']} {s['city']})" for s in st.session_state.address_suggestions]
        selected_label = st.selectbox("Sélectionnez votre adresse", labels, key="address_select")
        
        if st.button("✅ Valider cette adresse", type="primary", use_container_width=True):
            loader_placeholder = st.empty()
            loader_placeholder.markdown(show_skeleton_loader(), unsafe_allow_html=True)
            time.sleep(2) 
            
            for s in st.session_state.address_suggestions:
                if f"{s['label']} ({s['postcode']} {s['city']})" == selected_label:
                    st.session_state.property_data = fetch_base_property_data(s)
                    st.session_state.step = "questions"
                    st.session_state.wizard_step = 1
                    
            loader_placeholder.empty()
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 2: Interactive Wizard Questions
elif st.session_state.step == "questions":
    st.markdown("### 📋 Étape 2 : Améliorez la précision")
    if st.session_state.user_responses is None:
        st.session_state.user_responses = {}
        
    progress = st.session_state.wizard_step / 3
    st.progress(progress)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    if st.session_state.wizard_step == 1:
        st.markdown("#### 🪟 Quel type de vitrage possède le bien ?")
        win_val = st.radio("", ["Simple vitrage", "Double vitrage", "Je ne sais pas"], key="win")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Suivant ➡️", type="primary", use_container_width=True):
            st.session_state.user_responses["windows"] = win_val
            st.session_state.wizard_step = 2
            st.rerun()
            
    elif st.session_state.wizard_step == 2:
        st.markdown("#### 🔥 Quel est le système de chauffage principal ?")
        heat_val = st.radio("", ["Gaz ancien", "Électrique", "Pompe à chaleur", "Je ne sais pas"], key="heat")
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Retour", use_container_width=True):
                st.session_state.wizard_step = 1
                st.rerun()
        with col2:
            if st.button("Suivant ➡️", type="primary", use_container_width=True):
                st.session_state.user_responses["heating"] = heat_val
                st.session_state.wizard_step = 3
                st.rerun()

    elif st.session_state.wizard_step == 3:
        st.markdown("#### 🧱 Comment est l'isolation actuelle ?")
        colA, colB = st.columns(2)
        with colA:
            roof_val = st.radio("Toiture isolée ?", ["Oui", "Non", "Je ne sais pas"], key="roof")
        with colB:
            wall_val = st.radio("Murs isolés ?", ["Oui", "Non", "Je ne sais pas"], key="wall")
            
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Retour", use_container_width=True):
                st.session_state.wizard_step = 2
                st.rerun()
        with col2:
            if st.button("📊 Générer mon rapport", type="primary", use_container_width=True):
                st.session_state.user_responses["roof_insulation"] = roof_val
                st.session_state.user_responses["wall_insulation"] = wall_val
                st.session_state.step = "report"
                st.rerun()
                
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("⏩ Passer les questions (Générer avec l'IA)", use_container_width=True):
        st.session_state.user_responses = None
        st.session_state.step = "report"
        st.rerun()

# STEP 3: Report, PDF Download & LEAD CAPTURE
elif st.session_state.step == "report":
    st.markdown("### 📄 Votre rapport est prêt")
    
    prop = st.session_state.property_data
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    display_premium_map(prop["lat"], prop["lon"])
    
    st.info(f"""
    **Adresse:** {prop['address'][:60]}  
    **DPE Actuel:** {prop['dpe']}  
    **Surface:** {prop['surface']:.0f} m²  
    **Budget estimé:** €{prop['cost']:,.0f}  
    **ROI projeté:** +{prop['roi']:.1f}%
    """)
    
    # PDF Download
    try:
        with st.spinner("📄 Génération du PDF..."):
            pdf_bytes = generer_rapport(prop)
        
        if pdf_bytes and len(pdf_bytes) > 100:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    label="⬇️ Télécharger le rapport PDF",
                    data=pdf_bytes,
                    file_name=f"ZAMI_Rapport_{prop['zipcode']}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary"
                )
            st.success("✅ Rapport généré avec succès !")
        else:
            st.error("Erreur: PDF vide")
    except Exception as e:
        st.error(f"Erreur PDF: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ── LEAD CAPTURE FORM ──
    st.markdown('<div class="card" style="border: 1px solid rgba(34,197,94,0.3);">', unsafe_allow_html=True)
    st.markdown("### 📩 Recevez des devis gratuits")
    st.markdown("Obtenez jusqu'à 3 devis d'artisans RGE certifiés dans votre région")
    
    with st.form("lead_form"):
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom complet *", placeholder="Jean Dupont")
            email = st.text_input("Email *", placeholder="jean@email.com")
        with col2:
            telephone = st.text_input("Téléphone *", placeholder="06 12 34 56 78")
            st.markdown("<br>", unsafe_allow_html=True)
        
        if st.form_submit_button("📩 Demander mes devis gratuits", type="primary", use_container_width=True):
            if not nom or not email or not telephone:
                st.error("⚠️ Veuillez remplir tous les champs obligatoires (*).")
            else:
                with st.spinner("Enregistrement de votre demande..."):
                    lead_data = {
                        "address": prop['address'],
                        "zipcode": prop['zipcode'],
                        "dpe": prop['dpe'],
                        "surface": prop['surface'],
                        "cost": prop['cost'],
                        "roi": prop['roi'],
                        "name": nom,
                        "email": email,
                        "phone": telephone
                    }
                    
                    saved = save_lead(lead_data)
                    
                    if saved:
                        st.success("✅ Demande enregistrée ! Un expert vous contactera sous 24h.")
                        st.balloons()
                    else:
                        st.error("❌ Erreur lors de l'enregistrement. Veuillez réessayer.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🔍 Nouvelle analyse", use_container_width=True):
        st.session_state.step = "address"
        st.session_state.property_data = None
        st.session_state.address_suggestions = []
        st.session_state.user_responses = None
        st.session_state.wizard_step = 1
        st.session_state.lead_submitted = False
        st.rerun()

# Footer
st.markdown('<div class="footer">ZAMI - Intelligence Rénovation Énergétique</div>', unsafe_allow_html=True)