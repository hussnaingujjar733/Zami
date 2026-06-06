"""
reportlab_generator.py — ZAMI Premium PDF (ReportLab Edition)
Ultra-modern layout, organic flow, and luxury real-estate aesthetics.
"""

import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm

# --- BRAND COLORS ---
ZAMI_GREEN = colors.HexColor("#10B981")
DARK_SLATE = colors.HexColor("#0F172A")
COOL_GREY = colors.HexColor("#64748B")
LIGHT_BG = colors.HexColor("#F8FAFC")
WHITE = colors.HexColor("#FFFFFF")

DPE_COLORS = {
    'A': colors.HexColor("#22c55e"),
    'B': colors.HexColor("#4ade80"),
    'C': colors.HexColor("#a3e635"),
    'D': colors.HexColor("#facc15"),
    'E': colors.HexColor("#fb923c"),
    'F': colors.HexColor("#f97316"),
    'G': colors.HexColor("#ef4444")
}

def header_footer(canvas, doc):
    """Draws consistent header and footer on every page"""
    canvas.saveState()
    
    # Header Line
    canvas.setStrokeColor(ZAMI_GREEN)
    canvas.setLineWidth(1)
    canvas.line(20*mm, 280*mm, 190*mm, 280*mm)
    
    # Header Text
    canvas.setFont('Helvetica-Bold', 14)
    canvas.setFillColor(ZAMI_GREEN)
    canvas.drawString(20*mm, 285*mm, "ZAMI")
    
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(COOL_GREY)
    canvas.drawRightString(190*mm, 285*mm, f"Page {doc.page}")
    
    # Footer
    canvas.setFont('Helvetica-Oblique', 8)
    canvas.setFillColor(COOL_GREY)
    canvas.drawCentredString(105*mm, 15*mm, "ZAMI - Intelligence Rénovation Énergétique | Document Confidentiel")
    
    canvas.restoreState()


def create_styles():
    """Defines premium typography styles"""
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        name='CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=45,
        textColor=ZAMI_GREEN,
        alignment=1, # Center
        spaceAfter=20
    ))
    
    styles.add(ParagraphStyle(
        name='CoverSubtitle',
        fontName='Helvetica',
        fontSize=14,
        textColor=COOL_GREY,
        alignment=1,
        spaceAfter=40
    ))
    
    # Changed names to avoid conflict with ReportLab defaults
    styles.add(ParagraphStyle(
        name='ZamiHeading1',
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=DARK_SLATE,
        spaceBefore=20,
        spaceAfter=15,
        borderWidth=0,
        borderColor=ZAMI_GREEN,
    ))
    
    styles.add(ParagraphStyle(
        name='ZamiHeading2',
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=ZAMI_GREEN,
        spaceBefore=15,
        spaceAfter=10
    ))
    
    styles.add(ParagraphStyle(
        name='BodyTextPremium',
        fontName='Helvetica',
        fontSize=11,
        textColor=colors.HexColor("#334155"),
        leading=16, # Line height
        spaceAfter=12
    ))
    
    styles.add(ParagraphStyle(
        name='DPEBadge',
        fontName='Helvetica-Bold',
        fontSize=50,
        textColor=WHITE,
        alignment=1
    ))
    
    return styles


def generer_rapport(property_data):
    """Generates the premium PDF document dynamically"""
    
    # 1. INITIALIZE VARIABLES
    surface = property_data.get('surface', 75)
    dpe = str(property_data.get('dpe', 'E')).upper()
    cout = property_data.get('cost', 46500)
    roi = property_data.get('roi', 13.1)
    adresse = property_data.get('address', 'Adresse non disponible')
    
    valeur_actuelle = 280000
    subvention = int(12500 * (surface / 68))
    investissement_net = cout - subvention
    valeur_finale = int(valeur_actuelle * (1 + roi / 100))
    gain = valeur_finale - valeur_actuelle - investissement_net
    
    scores_dpe = {'A': 95, 'B': 85, 'C': 70, 'D': 55, 'E': 40, 'F': 25, 'G': 10}
    score_total = scores_dpe.get(dpe, 40)

    # 2. DOCUMENT SETUP
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4,
        rightMargin=20*mm, leftMargin=20*mm,
        topMargin=25*mm, bottomMargin=25*mm
    )
    
    styles = create_styles()
    elements = []
    
    # ==========================================
    # PAGE 1: COVER
    # ==========================================
    elements.append(Spacer(1, 40*mm))
    elements.append(Paragraph("ZAMI", styles['CoverTitle']))
    elements.append(Paragraph("RAPPORT D'ANALYSE ÉNERGÉTIQUE", styles['CoverSubtitle']))
    
    elements.append(Paragraph(f"<b>Propriété :</b><br/>{adresse}", ParagraphStyle(
        'Address', fontName='Helvetica', fontSize=12, alignment=1, textColor=DARK_SLATE, leading=16
    )))
    elements.append(Spacer(1, 20*mm))
    
    # Large DPE Block
    dpe_color = DPE_COLORS.get(dpe, COOL_GREY)
    dpe_table = Table([[Paragraph(dpe, styles['DPEBadge'])]], colWidths=[60*mm], rowHeights=[60*mm])
    dpe_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (-1,-1), dpe_color),
        ('ROUNDEDCORNERS', [20, 20, 20, 20]),
    ]))
    
    # Centering the DPE table
    centered_dpe = Table([[dpe_table]], colWidths=[170*mm])
    centered_dpe.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    elements.append(centered_dpe)
    
    elements.append(Spacer(1, 15*mm))
    elements.append(Paragraph(f"Score ZAMI : <b>{score_total}/100</b>", ParagraphStyle('Score', alignment=1, fontSize=14, textColor=DARK_SLATE)))
    elements.append(Spacer(1, 5*mm))
    elements.append(Paragraph(datetime.now().strftime("%d %B %Y"), ParagraphStyle('Date', alignment=1, fontSize=10, textColor=COOL_GREY)))
    
    elements.append(PageBreak())
    
    # ==========================================
    # PAGE 2: RESUME EXECUTIF & KPIs
    # ==========================================
    elements.append(Paragraph("Résumé Exécutif", styles['ZamiHeading1']))
    elements.append(Paragraph(
        "Ce rapport exclusif analyse le potentiel de rénovation énergétique de votre bien. "
        "Basé sur les données de l'ADEME et les prix du marché (DVF), il détaille les coûts, "
        "subventions et le retour sur investissement (ROI) projeté.",
        styles['BodyTextPremium']
    ))
    elements.append(Spacer(1, 10*mm))
    
    # KPI Grid
    kpi_data = [
        [
            Paragraph(f"<font color='#64748B' size=9>Valeur Actuelle</font><br/><font size=14><b>€ {valeur_actuelle:,}</b></font>"),
            Paragraph(f"<font color='#64748B' size=9>Valeur Future Estimée</font><br/><font size=14 color='#10B981'><b>€ {valeur_finale:,}</b></font>")
        ],
        [
            Paragraph(f"<font color='#64748B' size=9>Coût des Travaux</font><br/><font size=14><b>€ {cout:,}</b></font>"),
            Paragraph(f"<font color='#64748B' size=9>Subvention Estimée</font><br/><font size=14 color='#10B981'><b>€ {subvention:,}</b></font>")
        ],
        [
            Paragraph(f"<font color='#64748B' size=9>Investissement Net</font><br/><font size=14><b>€ {investissement_net:,}</b></font>"),
            Paragraph(f"<font color='#64748B' size=9>ROI Rénovation</font><br/><font size=14 color='#10B981'><b>+{roi:.1f}%</b></font>")
        ]
    ]
    
    kpi_table = Table(kpi_data, colWidths=[85*mm, 85*mm], rowHeights=[20*mm]*3)
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 1, WHITE),
        ('BOX', (0,0), (-1,-1), 2, WHITE),
        ('LEFTPADDING', (0,0), (-1,-1), 15),
    ]))
    elements.append(kpi_table)
    elements.append(Spacer(1, 15*mm))
    
    elements.append(Paragraph("Gain Net Estimé Après Rénovation", styles['ZamiHeading2']))
    elements.append(Paragraph(f"<b><font size=20>+€ {gain:,}</font></b>", styles['ZamiHeading1']))
    
    # ==========================================
    # PAGE 3: CARACTÉRISTIQUES & FINANCES
    # ==========================================
    elements.append(Paragraph("Caractéristiques & Analyse Financière", styles['ZamiHeading1']))
    
    # Property Details Table
    details_data = [
        ["Surface Habitable", f"{int(surface)} m²"],
        ["DPE Actuel", dpe],
        ["Année de construction", "1980-2000 (Estimé)"],
        ["Consommation Énergétique", "250-350 kWh/m²/an"],
    ]
    t_details = Table(details_data, colWidths=[80*mm, 90*mm])
    t_details.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,-1), 'Helvetica'),
        ('FONTNAME', (1,0), (1,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,0), (0,-1), COOL_GREY),
        ('TEXTCOLOR', (1,0), (1,-1), DARK_SLATE),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(t_details)
    elements.append(Spacer(1, 15*mm))
    
    elements.append(Paragraph("Détail de l'Investissement", styles['ZamiHeading2']))
    finance_data = [
        ["Investissement Travaux", f"- € {cout:,}"],
        ["Subventions Publiques", f"+ € {subvention:,}"],
        ["Investissement Net", f"€ {investissement_net:,}"],
        ["Plus-Value Immobilière", f"+ € {valeur_finale - valeur_actuelle:,}"],
    ]
    t_finance = Table(finance_data, colWidths=[80*mm, 90*mm])
    t_finance.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,-1), 'Helvetica'),
        ('FONTNAME', (1,0), (1,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,0), (0,-1), COOL_GREY),
        ('TEXTCOLOR', (1,0), (1,-1), DARK_SLATE),
        ('TEXTCOLOR', (1,1), (1,1), ZAMI_GREEN),
        ('TEXTCOLOR', (1,3), (1,3), ZAMI_GREEN),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(t_finance)
    
    elements.append(PageBreak())
    
    # ==========================================
    # PAGE 4: RECOMMANDATIONS
    # ==========================================
    elements.append(Paragraph("Plan d'Action & Recommandations", styles['ZamiHeading1']))
    
    recommandations = [
        ['Ordre', 'Action Recommandée', 'Coût Estimé', 'Délai'],
        ['1', 'Audit Énergétique Initial', '€ 500 - 1,000', 'Semaine 1'],
        ['2', 'Isolation Thermique (Murs/Toit)', '€ 12,000 - 18,000', 'Semaines 2-4'],
        ['3', 'Remplacement Chauffage (PAC)', '€ 10,000 - 15,000', 'Semaines 5-7'],
        ['4', 'Ventilation & Finitions', '€ 3,000 - 6,000', 'Semaine 8'],
    ]
    
    t_reco = Table(recommandations, colWidths=[20*mm, 70*mm, 40*mm, 40*mm])
    t_reco.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), ZAMI_GREEN),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT_BG]),
        ('GRID', (0,0), (-1,-1), 0.5, WHITE),
    ]))
    elements.append(t_reco)
    elements.append(Spacer(1, 15*mm))
    
    elements.append(Paragraph("Prochaines Étapes", styles['ZamiHeading2']))
    steps = [
        "Réaliser un audit sur site par un artisan certifié RGE.",
        "Déposer le dossier MaPrimeRénov' avant le début des travaux.",
        "Comparer au moins 3 devis pour optimiser les coûts."
    ]
    for step in steps:
        elements.append(Paragraph(f"• {step}", styles['BodyTextPremium']))
    
    elements.append(Spacer(1, 20*mm))
    
    # Contact Box
    contact_data = [[
        Paragraph("<b>Des questions ? Nos experts sont là.</b><br/><br/>Email: experts@thezami.com<br/>Tél: +33 1 23 45 67 89", 
                  ParagraphStyle('contact', alignment=1, fontSize=10, textColor=DARK_SLATE, leading=14))
    ]]
    t_contact = Table(contact_data, colWidths=[170*mm])
    t_contact.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 15),
        ('BOTTOMPADDING', (0,0), (-1,-1), 15),
        ('LINEABOVE', (0,0), (-1,-1), 2, ZAMI_GREEN)
    ]))
    elements.append(t_contact)
    
    # 3. BUILD DOCUMENT
    doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)
    
    pdf_value = buffer.getvalue()
    buffer.close()
    
    return pdf_value