"""
reportlab_generator.py — ZAMI Simple PDF
Uses FPDF - reliable on Streamlit Cloud
"""

from fpdf import FPDF
from datetime import datetime


def generer_rapport(property_data):
    """Generate PDF report using FPDF"""
    
    pdf = FPDF()
    pdf.add_page()
    
    # Colors
    DARK_BLUE = (15, 23, 42)
    LIGHT_BLUE = (59, 130, 246)
    GREEN = (34, 197, 94)
    GRAY_LIGHT = (241, 245, 249)
    
    # Background
    pdf.set_fill_color(*DARK_BLUE)
    pdf.rect(0, 0, 210, 297, 'F')
    
    # Top bar
    pdf.set_fill_color(*LIGHT_BLUE)
    pdf.rect(0, 0, 210, 6, 'F')
    
    # Title
    pdf.set_font('Helvetica', 'B', 36)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 30, 'ZAMI', ln=True, align='C')
    pdf.set_font('Helvetica', '', 9)
    pdf.cell(0, 8, 'RAPPORT D\'ANALYSE', ln=True, align='C')
    pdf.ln(10)
    
    # DPE Badge
    dpe = property_data.get('dpe', 'E')
    dpe_colors = {'A': (34,197,94), 'B': (74,222,128), 'C': (163,230,53), 
                  'D': (250,204,21), 'E': (251,146,60), 'F': (249,115,22), 
                  'G': (239,68,68)}
    color = dpe_colors.get(dpe, (100,100,100))
    pdf.set_fill_color(*color)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 60)
    pdf.set_x(210/2 - 30)
    pdf.cell(60, 60, dpe, border=0, align='C', fill=True)
    pdf.ln(20)
    
    # Address
    pdf.set_font('Helvetica', 'B', 12)
    address = property_data.get('address', 'Adresse')[:55]
    pdf.cell(0, 8, address, ln=True, align='C')
    pdf.ln(15)
    
    # Score
    dpe_scores = {'A': 95, 'B': 85, 'C': 70, 'D': 55, 'E': 40, 'F': 25, 'G': 10}
    score = dpe_scores.get(dpe, 40)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 8, 'POTENTIEL DE RENOVATION', ln=True, align='C')
    pdf.set_font('Helvetica', 'B', 40)
    pdf.set_text_color(*GREEN)
    pdf.cell(0, 20, str(score), ln=True, align='C')
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, 'sur 100', ln=True, align='C')
    
    # Date
    pdf.set_y(260)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, datetime.now().strftime("%d/%m/%Y"), ln=True, align='C')
    
    # Page 2: Summary
    pdf.add_page()
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(0, 0, 210, 297, 'F')
    
    # Title
    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 15, 'SYNTHESE', ln=True)
    pdf.line(10, pdf.get_y(), 60, pdf.get_y())
    pdf.ln(10)
    
    # Get values
    surface = property_data.get('surface', 75)
    cost = property_data.get('cost', 46500)
    roi = property_data.get('roi', 13.1)
    current_val = 280000
    subsidy = int(12500 * (surface / 68))
    net = cost - subsidy
    future_val = int(current_val * (1 + roi / 100))
    gain = future_val - current_val - net
    
    # KPIs
    kpis = [
        ('Valeur actuelle', f'{current_val:,} €'),
        ('Coût travaux', f'{cost:,} €'),
        ('Subventions', f'{subsidy:,} €'),
        ('Valeur finale', f'{future_val:,} €'),
        ('Invest. net', f'{net:,} €'),
        ('ROI', f'+{roi:.1f}%'),
    ]
    
    y = pdf.get_y()
    for i, (label, value) in enumerate(kpis):
        x = 20 + (i % 3) * 60
        if i % 3 == 0 and i > 0:
            y += 45
        pdf.set_xy(x, y)
        pdf.set_font('Helvetica', '', 8)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(50, 6, label, ln=False, align='C')
        pdf.set_xy(x, y + 7)
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(50, 8, value, ln=False, align='C')
    
    pdf.ln(50)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(*GREEN)
    pdf.cell(0, 10, f'Gain net estime: {gain:,} €', ln=True, align='C')
    
    # Page 3: Details
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 15, 'CARACTERISTIQUES', ln=True)
    pdf.line(10, pdf.get_y(), 70, pdf.get_y())
    pdf.ln(10)
    
    details = [
        ('Adresse', property_data.get('address', 'N/A')[:60]),
        ('Surface', f'{int(surface)} m²'),
        ('DPE', dpe),
        ('Construction', 'Avant 1975' if dpe in ['F','G'] else '1980-2000'),
    ]
    
    for label, value in details:
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(59, 130, 246)
        pdf.cell(50, 10, label, ln=False)
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, value, ln=True)
        pdf.ln(2)
    
    # Page 4: Recommendations
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 15, 'RECOMMANDATIONS', ln=True)
    pdf.line(10, pdf.get_y(), 85, pdf.get_y())
    pdf.ln(10)
    
    recos = [
        '1. Realiser un audit energetique complet',
        '2. Deposer une demande MaPrimeRenov',
        '3. Contacter des artisans certifies RGE',
        '4. Planifier les travaux par priorite',
    ]
    
    pdf.set_font('Helvetica', '', 10)
    for rec in recos:
        pdf.cell(0, 8, rec, ln=True)
        pdf.ln(2)
    
    # Page 5: Contact
    pdf.add_page()
    pdf.set_y(100)
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'Besoin d\'accompagnement ?', ln=True, align='C')
    pdf.ln(15)
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 8, ' experts@thezami.com', ln=True, align='C')
    pdf.cell(0, 8, ' +33 1 23 45 67 89', ln=True, align='C')
    pdf.ln(30)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, 'Rapport preliminaire - validation sur site recommandee', ln=True, align='C')
    
    # Footer
    pdf.set_y(280)
    pdf.set_font('Helvetica', 'I', 7)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 6, 'ZAMI - Intelligence Renovation Energetique', ln=True, align='C')
    
    return pdf.output(dest='S')


def make_report(data):
    return generer_rapport(data)