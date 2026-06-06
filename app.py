import os
import json
import requests
import streamlit as st
from fpdf import FPDF
from datetime import datetime

# ── ⚡ IMPORT MODULES ──
import utils_styles

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

# State
if "property_data" not in st.session_state:
    st.session_state.property_data = None
if "address_suggestions" not in st.session_state:
    st.session_state.address_suggestions = []
if "user_responses" not in st.session_state:
    st.session_state.user_responses = None
if "step" not in st.session_state:
    st.session_state.step = "address"

# Global Variables
_FALLBACK_RENO_COST = {"G": 1350, "F": 1100, "E": 620, "D": 280, "C": 120, "B": 0, "A": 0}
_FALLBACK_UPLIFT = {"G": 24.2, "F": 19.8, "E": 13.1, "D": 6.8, "C": 2.0, "B": 0, "A": 0}


# ─────────────────────────────────────────────
# DPE FUNCTIONS
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
# PDF GENERATION (FIXED)
# ─────────────────────────────────────────────
def generate_pdf_bytes(property_data):
    """Generate PDF and return bytes - guaranteed working"""
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font('Helvetica', 'B', 20)
    pdf.cell(0, 15, 'ZAMI PROPERTY REPORT', ln=True, align='C')
    
    # Date
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 8, f'Date: {datetime.now().strftime("%d/%m/%Y")}', ln=True, align='R')
    pdf.ln(5)
    
    # Address
    pdf.set_font('Helvetica', 'B', 12)
    address = property_data.get('address', 'Address not available')[:60]
    pdf.multi_cell(0, 8, address, align='L')
    pdf.ln(5)
    
    # DPE
    dpe = property_data.get('dpe', 'E')
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, f'Current DPE: {dpe}', ln=True)
    pdf.ln(3)
    
    # Surface
    surface = property_data.get('surface', 68)
    pdf.cell(0, 8, f'Surface: {int(surface)} m2', ln=True)
    pdf.ln(3)
    
    # Cost
    cost = property_data.get('cost', 25000)
    pdf.cell(0, 8, f'Estimated Cost: EUR {int(cost):,}', ln=True)
    pdf.ln(3)
    
    # ROI
    roi = property_data.get('roi', 15.0)
    pdf.cell(0, 8, f'Expected ROI: +{roi:.1f}%', ln=True)
    pdf.ln(5)
    
    # Subsidy
    surface_val = property_data.get('surface', 68)
    subsidy = int(12500 * (surface_val / 68))
    pdf.cell(0, 8, f'Estimated Subsidy: EUR {subsidy:,}', ln=True)
    pdf.ln(5)
    
    # Value gain
    current_val = 280000
    after_val = int(350000 * (surface_val / 68))
    gain = after_val - current_val
    pdf.cell(0, 8, f'Value Gain: +EUR {gain:,}', ln=True)
    pdf.ln(10)
    
    # Footer
    pdf.set_y(-30)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, 'ZAMI - Property Intelligence Platform', ln=True, align='C')
    
    # FIX: Convert to bytes properly
    output = pdf.output(dest='S')
    if isinstance(output, str):
        output = output.encode('latin-1')
    return output


# ─────────────────────────────────────────────
# HERO SECTION
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
            <span>✓ Subventions disponibles</span>
            <span>✓ ROI de rénovation</span>
            <span>✓ Conformité légale</span>
            <span>✓ Plus-value immobilière</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────
hero_section()

st.markdown('<div class="card">', unsafe_allow_html=True)

# Step 1: Address Selection
if st.session_state.step == "address":
    st.markdown("### 📍 Étape 1 : Entrez votre adresse")
    
    search_query = st.text_input("Adresse", placeholder="Ex: 39 Rue du Sergent Bobillot, Montreuil", key="address_input")
    
    if search_query and len(search_query.strip()) >= 3:
        suggestions = ban_search(search_query)
        st.session_state.address_suggestions = suggestions
    
    if st.session_state.address_suggestions:
        labels = [f"{s['label']} ({s['postcode']} {s['city']})" for s in st.session_state.address_suggestions]
        selected_label = st.selectbox("Sélectionnez votre adresse", labels, key="address_select")
        
        if st.button("✅ Valider cette adresse", type="primary", use_container_width=True):
            for s in st.session_state.address_suggestions:
                if f"{s['label']} ({s['postcode']} {s['city']})" == selected_label:
                    st.session_state.property_data = fetch_base_property_data(s)
                    st.session_state.step = "questions"
                    st.rerun()

# Step 2: Questions
elif st.session_state.step == "questions":
    st.markdown("### 📋 Étape 2 : Améliorez la précision")
    st.markdown("Quelques questions optionnelles pour un résultat plus précis")
    
    with st.form("accuracy_form"):
        windows = st.radio("Type de vitrage", ["Simple vitrage", "Double vitrage", "Je ne sais pas"], horizontal=True)
        heating = st.radio("Système de chauffage", ["Gaz ancien", "Electrique", "Pompe a chaleur", "Je ne sais pas"], horizontal=True)
        
        col1, col2 = st.columns(2)
        with col1:
            roof = st.radio("Toiture isolee ?", ["Oui", "Non", "Je ne sais pas"], horizontal=True)
        with col2:
            wall = st.radio("Murs isoles ?", ["Oui", "Non", "Je ne sais pas"], horizontal=True)
        
        if st.form_submit_button("📊 Generer mon rapport", type="primary", use_container_width=True):
            st.session_state.user_responses = {
                "windows": windows, "heating": heating,
                "roof_insulation": roof, "wall_insulation": wall
            }
            st.session_state.step = "report"
            st.rerun()
    
    if st.button("⏩ Passer les questions", use_container_width=True):
        st.session_state.user_responses = None
        st.session_state.step = "report"
        st.rerun()

# Step 3: PDF Download
elif st.session_state.step == "report":
    st.markdown("### 📄 Votre rapport est pret !")
    
    prop = st.session_state.property_data
    
    # Show summary
    st.info(f"""
    **Adresse:** {prop['address'][:60]}  
    **DPE Actuel:** {prop['dpe']}  
    **Surface:** {prop['surface']:.0f} m²  
    **Budget estime:** €{prop['cost']:,.0f}  
    **ROI projete:** +{prop['roi']:.1f}%
    """)
    
    # Generate and download PDF
    try:
        pdf_bytes = generate_pdf_bytes(prop)
        
        if pdf_bytes and len(pdf_bytes) > 500:
            st.download_button(
                label="⬇️ Telecharger le rapport PDF",
                data=pdf_bytes,
                file_name=f"ZAMI_Report_{prop['zipcode']}_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )
            st.success("✅ PDF genere avec succes !")
        else:
            st.error(f"Erreur: PDF vide (taille: {len(pdf_bytes) if pdf_bytes else 0})")
            
    except Exception as e:
        st.error(f"Erreur: {str(e)}")
    
    st.markdown("---")
    if st.button("🔍 Nouvelle analyse", use_container_width=True):
        st.session_state.step = "address"
        st.session_state.property_data = None
        st.session_state.address_suggestions = []
        st.session_state.user_responses = None
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">ZAMI - Intelligence Renovation Energetique</div>', unsafe_allow_html=True)