import os
import base64
import json
import requests
import pandas as pd
import streamlit as st
from fpdf import FPDF
from datetime import datetime
import hashlib

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
if "report_generated" not in st.session_state:
    st.session_state.report_generated = False

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

def ban_search(query: str, limit: int = 1):
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

def fetch_property_data(address):
    """Fetch DPE data for given address"""
    geo = ban_search(address, 1)
    if not geo:
        return None
    
    # Estimate DPE based on postcode
    zipcode = geo[0]["postcode"]
    region = str(zipcode)[:2]
    dpe_by_region = {"75": "E", "92": "E", "93": "F", "94": "E", "69": "D", "13": "D", "31": "D"}
    dpe = dpe_by_region.get(region, "E")
    surface = 52.0 if region == "75" else 75.0
    cost = round(surface * _FALLBACK_RENO_COST.get(dpe, 620), 0)
    roi = _FALLBACK_UPLIFT.get(dpe, 13.1)
    
    return {
        "address": geo[0]["label"],
        "dpe": dpe,
        "surface": surface,
        "cost": cost,
        "roi": roi,
        "zipcode": zipcode,
        "lat": geo[0]["lat"],
        "lon": geo[0]["lon"],
    }


# ─────────────────────────────────────────────
# BEAUTIFUL PDF GENERATION
# ─────────────────────────────────────────────
def generate_beautiful_pdf(property_data):
    """Generate premium PDF report"""
    pdf = FPDF()
    pdf.add_page()
    
    # Background color
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, 210, 297, 'F')
    
    # Top gradient bar
    pdf.set_fill_color(59, 130, 246)
    pdf.rect(0, 0, 210, 8, 'F')
    
    # Title
    pdf.set_font('Helvetica', 'B', 28)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 30, 'ZAMI', ln=True, align='C')
    
    # Subtitle
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, 'PROPERTY INTELLIGENCE REPORT', ln=True, align='C')
    pdf.ln(10)
    
    # Date
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 5, f'Generated: {datetime.now().strftime("%d/%m/%Y")}', ln=True, align='R')
    pdf.ln(5)
    
    # Address
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(255, 255, 255)
    pdf.multi_cell(0, 8, property_data['address'], align='C')
    pdf.ln(10)
    
    # DPE Badge
    dpe = property_data['dpe']
    dpe_colors = {"A": (34,197,94), "B": (74,222,128), "C": (163,230,53), "D": (250,204,21), "E": (251,146,60), "F": (249,115,22), "G": (239,68,68)}
    color = dpe_colors.get(dpe, (100,100,100))
    pdf.set_fill_color(*color)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 72)
    
    # Center DPE badge
    pdf.set_x(210/2 - 30)
    pdf.cell(60, 60, dpe, border=0, align='C', fill=True)
    pdf.ln(15)
    
    # DPE label
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(180, 180, 180)
    pdf.cell(0, 5, 'Energy Performance Rating', ln=True, align='C')
    pdf.ln(15)
    
    # Key Metrics Table
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, 'KEY METRICS', ln=True, align='L')
    pdf.ln(5)
    
    # Line
    pdf.set_draw_color(59, 130, 246)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)
    
    # Metrics rows
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(200, 200, 200)
    
    # Surface
    pdf.cell(80, 10, 'Surface Area:', ln=False)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, f"{property_data['surface']} m²", ln=True)
    
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(200, 200, 200)
    pdf.cell(80, 10, 'Current DPE:', ln=False)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, f"Class {property_data['dpe']}", ln=True)
    
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(200, 200, 200)
    pdf.cell(80, 10, 'Renovation Cost:', ln=False)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, f"€{property_data['cost']:,}", ln=True)
    
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(200, 200, 200)
    pdf.cell(80, 10, 'Expected ROI:', ln=False)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(100, 255, 100)
    pdf.cell(0, 10, f"+{property_data['roi']}%", ln=True)
    
    pdf.ln(15)
    
    # Estimated Value Increase
    current_val = 280000
    after_val = int(350000 * (property_data['surface'] / 68))
    gain = after_val - current_val
    
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, 'VALUE PROJECTION', ln=True, align='L')
    pdf.ln(5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)
    
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(200, 200, 200)
    pdf.cell(80, 10, 'Current Value:', ln=False)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, f"€{current_val:,}", ln=True)
    
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(200, 200, 200)
    pdf.cell(80, 10, 'After Renovation:', ln=False)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(100, 255, 100)
    pdf.cell(0, 10, f"€{after_val:,}", ln=True)
    
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(200, 200, 200)
    pdf.cell(80, 10, 'Value Gain:', ln=False)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(100, 255, 100)
    pdf.cell(0, 10, f"+€{gain:,}", ln=True)
    
    pdf.ln(15)
    
    # Subsidy estimate
    subsidy = int(12500 * (property_data['surface'] / 68))
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, 'SUBSIDY ELIGIBILITY', ln=True, align='L')
    pdf.ln(5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)
    
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(200, 200, 200)
    pdf.cell(0, 10, f"MaPrimeRénov' Estimate: €{subsidy:,}", ln=True, align='C')
    
    pdf.ln(15)
    
    # Footer
    pdf.set_y(-30)
    pdf.set_font('Helvetica', 'I', 7)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 5, 'ZAMI - Property Intelligence Platform', ln=True, align='C')
    pdf.cell(0, 5, 'This is an estimate. Consult certified professionals.', ln=True, align='C')
    
    return pdf.output(dest='S')


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
        .hero-feature { font-size: 0.65rem; }
    }
    </style>
    
    <div class="hero-small">
        <div class="hero-logo-text">ZAMI</div>
        <div class="hero-tagline">⚡ FRANCE'S #1 RENOVATION INTELLIGENCE</div>
        <div class="hero-title-fr">L'avenir de la rénovation immobilière</div>
        <div class="hero-subtitle-fr">Entrez votre adresse et recevez votre rapport instantanément</div>
        <div class="hero-features">
            <span class="hero-feature">✓ Subventions disponibles</span>
            <span class="hero-feature">✓ ROI de rénovation</span>
            <span class="hero-feature">✓ Conformité légale</span>
            <span class="hero-feature">✓ Plus-value immobilière</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────
hero_section()

st.markdown('<div class="card">', unsafe_allow_html=True)

address = st.text_input("📍 Adresse complète", placeholder="Ex: 39 Rue du Sergent Bobillot, Montreuil")

if st.button("📊 Générer mon rapport", type="primary", use_container_width=True):
    if address and len(address.strip()) >= 5:
        with st.spinner("🔍 Analyse en cours..."):
            property_data = fetch_property_data(address)
            if property_data:
                pdf_bytes = generate_beautiful_pdf(property_data)
                st.success("✅ Rapport prêt !")
                
                # Direct download button
                st.download_button(
                    label="⬇️ Télécharger mon rapport PDF",
                    data=pdf_bytes,
                    file_name=f"ZAMI_Report_{property_data['zipcode']}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary"
                )
                
                # Show preview message
                st.markdown("""
                <div style="background:rgba(34,197,94,0.1); border-radius:12px; padding:15px; text-align:center; margin-top:15px;">
                    ✨ Votre rapport professionnel est prêt à être téléchargé !<br>
                    <span style="font-size:12px; color:#64748b;">DPE: {}</span>
                </div>
                """.format(property_data['dpe']), unsafe_allow_html=True)
            else:
                st.error("Adresse non trouvée. Veuillez réessayer.")
    else:
        st.warning("Veuillez entrer une adresse valide")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">ZAMI - Intelligence Rénovation Énergétique</div>', unsafe_allow_html=True)