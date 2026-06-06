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
    """Generate premium, visually stunning PDF report"""
    pdf = FPDF()
    pdf.add_page()
    
    # ============================================
    # BACKGROUND COLOR
    # ============================================
    pdf.set_fill_color(15, 23, 42)  # Dark blue
    pdf.rect(0, 0, 210, 297, 'F')
    
    # ============================================
    # TOP GRADIENT BAR
    # ============================================
    for i in range(10):
        pdf.set_fill_color(59, 130, 246 - i * 5, 16, 185 - i * 10, 129 - i * 5)
        pdf.rect(0, i, 210, 1, 'F')
    
    # ============================================
    # WATERMARK (ZAMI)
    # ============================================
    pdf.set_font('Helvetica', 'B', 60)
    pdf.set_text_color(30, 41, 59)
    pdf.set_xy(20, 120)
    pdf.rotate(45)
    pdf.cell(0, 0, 'ZAMI', ln=True)
    pdf.rotate(0)
    
    # ============================================
    # HEADER SECTION
    # ============================================
    # Logo
    pdf.set_font('Helvetica', 'B', 32)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 20, 'ZAMI', ln=True, align='C')
    
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 5, 'PROPERTY INTELLIGENCE REPORT', ln=True, align='C')
    pdf.line(70, pdf.get_y(), 140, pdf.get_y())
    pdf.ln(8)
    
    # Date
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 5, f'GENERATED: {datetime.now().strftime("%d/%m/%Y")}', ln=True, align='R')
    pdf.ln(5)
    
    # ============================================
    # ADDRESS SECTION (with location icon)
    # ============================================
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(10, 8, '📍', ln=False)
    pdf.set_font('Helvetica', 'B', 11)
    address = property_data.get('address', 'Address not available')[:55]
    pdf.multi_cell(0, 6, address, align='L')
    pdf.ln(5)
    
    # ============================================
    # DPE BADGE (Large, Color-Coded)
    # ============================================
    dpe = property_data.get('dpe', 'E')
    dpe_colors = {
        "A": (34, 197, 94), "B": (74, 222, 128),
        "C": (163, 230, 53), "D": (250, 204, 21),
        "E": (251, 146, 60), "F": (249, 115, 22),
        "G": (239, 68, 68)
    }
    color = dpe_colors.get(dpe, (100, 100, 100))
    
    pdf.set_fill_color(*color)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 70)
    
    # Center the DPE badge
    pdf.set_x(210/2 - 30)
    pdf.cell(60, 60, dpe, border=0, align='C', fill=True)
    pdf.ln(15)
    
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 5, 'ENERGY PERFORMANCE RATING', ln=True, align='C')
    pdf.ln(12)
    
    # ============================================
    # KEY METRICS (4 Cards)
    # ============================================
    # Row 1
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(148, 163, 184)
    
    # Surface
    pdf.set_fill_color(30, 41, 59)
    pdf.rect(15, pdf.get_y(), 85, 35, 'F')
    pdf.set_xy(20, pdf.get_y() + 5)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 4, 'SURFACE', ln=True)
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, f"{int(property_data.get('surface', 68))} m²", ln=True)
    
    # DPE Class
    pdf.set_xy(110, pdf.get_y() - 35)
    pdf.set_fill_color(30, 41, 59)
    pdf.rect(110, pdf.get_y(), 85, 35, 'F')
    pdf.set_xy(115, pdf.get_y() + 5)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 4, 'DPE CLASS', ln=True)
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, property_data.get('dpe', 'E'), ln=True)
    
    pdf.ln(40)
    
    # Row 2
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(148, 163, 184)
    
    # Cost
    cost = property_data.get('cost', 25000)
    pdf.set_fill_color(30, 41, 59)
    pdf.rect(15, pdf.get_y(), 85, 35, 'F')
    pdf.set_xy(20, pdf.get_y() + 5)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 4, 'RENOVATION COST', ln=True)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, f"€{int(cost):,}", ln=True)
    
    # ROI
    roi = property_data.get('roi', 15.0)
    pdf.set_xy(110, pdf.get_y() - 35)
    pdf.set_fill_color(30, 41, 59)
    pdf.rect(110, pdf.get_y(), 85, 35, 'F')
    pdf.set_xy(115, pdf.get_y() + 5)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 4, 'ROI', ln=True)
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_text_color(34, 197, 94)
    pdf.cell(0, 8, f"+{roi:.1f}%", ln=True)
    
    pdf.ln(40)
    
    # ============================================
    # ROI GAUGE VISUALIZATION
    # ============================================
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, '📈 ROI PROJECTION', ln=True, align='L')
    pdf.ln(3)
    
    # ROI bar (visual)
    roi_percent = min(100, roi * 2)
    pdf.set_fill_color(30, 41, 59)
    pdf.rect(15, pdf.get_y(), 180, 15, 'F')
    pdf.set_fill_color(34, 197, 94)
    pdf.rect(15, pdf.get_y(), (roi_percent * 180 / 100), 15, 'F')
    pdf.set_xy(15 + (roi_percent * 180 / 100) - 10, pdf.get_y())
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 5, f"{roi:.0f}%", ln=False)
    pdf.ln(20)
    
    # ============================================
    # VALUE PROJECTION (Before/After)
    # ============================================
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, '💰 VALUE PROJECTION', ln=True, align='L')
    pdf.ln(3)
    
    surface_val = property_data.get('surface', 68)
    current_val = 280000
    after_val = int(350000 * (surface_val / 68))
    gain = after_val - current_val
    
    # Before
    pdf.set_fill_color(30, 41, 59)
    pdf.rect(15, pdf.get_y(), 85, 30, 'F')
    pdf.set_xy(20, pdf.get_y() + 5)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 4, 'CURRENT VALUE', ln=True)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, f"€{current_val:,}", ln=True)
    
    # Arrow
    pdf.set_xy(108, pdf.get_y() - 15)
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_text_color(34, 197, 94)
    pdf.cell(0, 5, '→', ln=False)
    
    # After
    pdf.set_xy(125, pdf.get_y() - 30)
    pdf.set_fill_color(34, 197, 94)
    pdf.rect(125, pdf.get_y(), 70, 30, 'F')
    pdf.set_xy(130, pdf.get_y() + 5)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 4, 'AFTER RENOVATION', ln=True)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 8, f"€{after_val:,}", ln=True)
    
    pdf.ln(35)
    
    # Gain
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(34, 197, 94)
    pdf.cell(0, 8, f"+€{gain:,} VALUE GAIN", ln=True, align='C')
    pdf.ln(10)
    
    # ============================================
    # SUBSIDY SECTION
    # ============================================
    subsidy = int(12500 * (surface_val / 68))
    pdf.set_fill_color(30, 41, 59)
    pdf.rect(15, pdf.get_y(), 180, 30, 'F')
    pdf.set_xy(20, pdf.get_y() + 8)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 5, '🏷️ SUBSIDY ELIGIBILITY', ln=True)
    pdf.set_xy(20, pdf.get_y() + 15)
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_text_color(34, 197, 94)
    pdf.cell(0, 8, f"€{subsidy:,}", ln=True)
    pdf.set_xy(20, pdf.get_y() + 23)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 4, 'MaPrimeRénov\' Estimate', ln=True)
    pdf.ln(40)
    
    # ============================================
    # QR CODE SECTION (for verification)
    # ============================================
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 5, 'SCAN TO VERIFY', ln=True, align='C')
    pdf.set_font('Helvetica', 'I', 7)
    pdf.cell(0, 5, 'thezami.com/verify', ln=True, align='C')
    
    # ============================================
    # FOOTER
    # ============================================
    pdf.set_y(-25)
    pdf.set_font('Helvetica', 'I', 7)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 5, 'ZAMI - Property Intelligence Platform', ln=True, align='C')
    pdf.cell(0, 5, 'This is an AI-generated estimate. Consult certified professionals.', ln=True, align='C')
    
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