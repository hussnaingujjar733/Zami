"""
reportlab_generator.py — ZAMI Premium PDF (ReportLab Edition)
Dynamic Platypus Layout + Native Vector Graphics (Pie & Line Charts)
"""

import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm

# Import ReportLab Graphics for Charts
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.linecharts import HorizontalLineChart

# --- BRAND COLORS ---
ZAMI_GREEN = colors.HexColor("#10B981")
ZAMI_RED = colors.HexColor("#EF4444")
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
    """En-tête et pied de page"""
    canvas.saveState()
    
    # Ligne Header
    canvas.setStrokeColor(ZAMI_GREEN)
    canvas.setLineWidth(1)
    canvas.line(20*mm, 280*mm, 190*mm, 280*mm)
    
    # Texte Header
    canvas.setFont('Helvetica-Bold', 14)
    canvas.setFillColor(ZAMI_GREEN)
    canvas.drawString(20*mm, 282*mm, "ZAMI")
    
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(COOL_GREY)
    canvas.drawRightString(190*mm, 282*mm, f"Page {doc.page}")
    
    # Footer
    canvas.setFont('Helvetica-Oblique', 8)
    canvas.setFillColor(COOL_GREY)
    canvas.drawCentredString(105*mm, 15*mm, "ZAMI - Intelligence Rénovation Énergétique | Document Confidentiel")
    
    canvas.restoreState()


def create_styles():
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(name='CoverTitle', fontName='Helvetica-Bold', fontSize=40, textColor=ZAMI_GREEN, alignment=TA_CENTER, spaceAfter=20))
    styles.add(ParagraphStyle(name='CoverSubtitle', fontName='Helvetica', fontSize=14, textColor=COOL_GREY, alignment=TA_CENTER, spaceAfter=40))
    styles.add(ParagraphStyle(name='ZamiHeading1', fontName='Helvetica-Bold', fontSize=18, textColor=DARK_SLATE, spaceBefore=20, spaceAfter=15))
    styles.add(ParagraphStyle(name='ZamiHeading2', fontName='Helvetica-Bold', fontSize=14, textColor=ZAMI_GREEN, spaceBefore=15, spaceAfter=10))
    styles.add(ParagraphStyle(name='BodyTextPremium', fontName='Helvetica', fontSize=10, textColor=colors.HexColor("#334155"), leading=16, spaceAfter=12))
    styles.add(ParagraphStyle(name='DPEBadge', fontName='Helvetica-Bold', fontSize=50, textColor=WHITE, alignment=TA_CENTER))
    
    return styles


def generer_rapport(property_data):
    # 1. CALCULATIONS
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
    score_total = {'A': 95, 'B': 85, 'C': 70, 'D': 55, 'E': 40, 'F': 25, 'G': 10}.get(dpe, 40)

    # 2. DOCUMENT SETUP
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=20*mm, leftMargin=20*mm, topMargin=25*mm, bottomMargin=25*mm)
    styles = create_styles()
    elements = []
    
    # ================= PAGE 1 : COUVERTURE =================
    elements.append(Spacer(1, 40*mm))
    elements.append(Paragraph("ZAMI", styles['CoverTitle']))
    elements.append(Paragraph("RAPPORT D'ANALYSE ÉNERGÉTIQUE", styles['CoverSubtitle']))
    
    elements.append(Paragraph(f"<b>Propriété :</b><br/>{adresse}", ParagraphStyle('Address', fontName='Helvetica', fontSize=12, alignment=TA_CENTER, textColor=DARK_SLATE, leading=16)))
    elements.append(Spacer(1, 20*mm))
    
    # DPE Badge
    dpe_table = Table([[Paragraph(dpe, styles['DPEBadge'])]], colWidths=[60*mm], rowHeights=[60*mm])
    dpe_table.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('BACKGROUND', (0,0), (-1,-1), DPE_COLORS.get(dpe, COOL_GREY))]))
    centered_dpe = Table([[dpe_table]], colWidths=[170*mm])
    centered_dpe.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    elements.append(centered_dpe)
    
    elements.append(Spacer(1, 15*mm))
    elements.append(Paragraph(f"Score ZAMI : <b>{score_total}/100</b>", ParagraphStyle('Score', alignment=TA_CENTER, fontSize=14, textColor=DARK_SLATE)))
    elements.append(Spacer(1, 5*mm))
    elements.append(Paragraph(datetime.now().strftime("%d %B %Y"), ParagraphStyle('Date', alignment=TA_CENTER, fontSize=10, textColor=COOL_GREY)))
    elements.append(PageBreak())
    
    # ================= PAGE 2 : RÉSUMÉ & GRAPHIQUE PIE =================
    elements.append(Paragraph("Résumé Exécutif", styles['ZamiHeading1']))
    elements.append(Paragraph("Ce rapport détaille les coûts, subventions et le retour sur investissement (ROI) projeté pour votre rénovation énergétique globale.", styles['BodyTextPremium']))
    
    # KPI Grid
    kpi_data = [
        [Paragraph(f"<font color='#64748B' size=9>Valeur Actuelle</font><br/><font size=14><b>€ {valeur_actuelle:,}</b></font>"), Paragraph(f"<font color='#64748B' size=9>Valeur Future Estimée</font><br/><font size=14 color='#10B981'><b>€ {valeur_finale:,}</b></font>")],
        [Paragraph(f"<font color='#64748B' size=9>Coût des Travaux</font><br/><font size=14><b>€ {cout:,}</b></font>"), Paragraph(f"<font color='#64748B' size=9>Subvention Estimée</font><br/><font size=14 color='#10B981'><b>€ {subvention:,}</b></font>")],
        [Paragraph(f"<font color='#64748B' size=9>Investissement Net</font><br/><font size=14><b>€ {investissement_net:,}</b></font>"), Paragraph(f"<font color='#64748B' size=9>ROI Rénovation</font><br/><font size=14 color='#10B981'><b>+{roi:.1f}%</b></font>")]
    ]
    kpi_table = Table(kpi_data, colWidths=[85*mm, 85*mm], rowHeights=[20*mm]*3)
    kpi_table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), LIGHT_BG), ('INNERGRID', (0,0), (-1,-1), 1, WHITE), ('BOX', (0,0), (-1,-1), 2, WHITE), ('LEFTPADDING', (0,0), (-1,-1), 15), ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
    elements.append(kpi_table)
    elements.append(Spacer(1, 10*mm))
    
    # --- VISUALIZATION 1: FINANCIAL PIE CHART ---
    elements.append(Paragraph("Répartition de l'Investissement", styles['ZamiHeading2']))
    d_pie = Drawing(width=400, height=180)
    pie = Pie()
    pie.x = 100
    pie.y = 20
    pie.width = 140
    pie.height = 140
    pie.data = [investissement_net, subvention]
    pie.labels = ['Reste à charge', "Subvention"]
    pie.slices[0].fillColor = ZAMI_RED
    pie.slices[1].fillColor = ZAMI_GREEN
    pie.sideLabels = 1
    d_pie.add(pie)
    
    # Legend for pie
    legend_table = Table([
        [Paragraph("<b>Reste à charge (Net)</b>", styles['BodyTextPremium']), Paragraph(f"€ {investissement_net:,}", styles['BodyTextPremium'])],
        [Paragraph("<b>Subventions (MaPrimeRénov)</b>", styles['BodyTextPremium']), Paragraph(f"€ {subvention:,}", styles['BodyTextPremium'])]
    ], colWidths=[60*mm, 30*mm])
    
    # Align chart and legend side by side
    chart_row = Table([[d_pie, legend_table]], colWidths=[100*mm, 70*mm])
    chart_row.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
    elements.append(chart_row)
    
    elements.append(PageBreak())
    
    # ================= PAGE 3 : TRAJECTOIRE & GRAPHIQUE LIGNE =================
    elements.append(Paragraph("Trajectoire de Valorisation (5 Ans)", styles['ZamiHeading1']))
    elements.append(Paragraph("Comparaison de la valeur de votre patrimoine avec et sans rénovation énergétique.", styles['BodyTextPremium']))
    
    # --- VISUALIZATION 2: ROI LINE CHART ---
    d_line = Drawing(400, 200)
    lc = HorizontalLineChart()
    lc.x = 40
    lc.y = 30
    lc.height = 140
    lc.width = 320
    
    # Generate curve data
    renovated_curve = [valeur_actuelle * (1 + (roi/100) + (i*0.02)) for i in range(6)]
    unrenovated_curve = [valeur_actuelle * (1 - (i * 0.035)) for i in range(6)]
    
    lc.data = [renovated_curve, unrenovated_curve]
    lc.categoryAxis.categoryNames = ["2026", "2027", "2028", "2029", "2030", "2031"]
    lc.categoryAxis.labels.boxAnchor = 'n'
    lc.categoryAxis.labels.dy = -5
    
    # Styling lines
    lc.lines[0].strokeColor = ZAMI_GREEN
    lc.lines[0].strokeWidth = 3
    lc.lines[1].strokeColor = ZAMI_RED
    lc.lines[1].strokeWidth = 2
    lc.lines[1].strokeDashArray = [4, 4] # Dashed line for unrenovated
    
    d_line.add(lc)
    
    chart_legend2 = Table([
        [Paragraph("<font color='#10B981'><b>▬ Asset Rénové (DPE C)</b></font>", styles['BodyTextPremium'])],
        [Paragraph("<font color='#EF4444'><b>- - Passoire Non-Rénovée</b></font>", styles['BodyTextPremium'])]
    ])
    
    elements.append(d_line)
    elements.append(chart_legend2)
    elements.append(Spacer(1, 15*mm))
    
    # Gain Highlight
    elements.append(Paragraph("Gain Net Estimé Après Rénovation", styles['ZamiHeading2']))
    elements.append(Paragraph(f"<b><font size=20>+€ {gain:,}</font></b>", styles['ZamiHeading1']))
    
    elements.append(PageBreak())
    
    # ================= PAGE 4 : RECOMMANDATIONS =================
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
        ('BACKGROUND', (0,0), (-1,0), ZAMI_GREEN), ('TEXTCOLOR', (0,0), (-1,0), WHITE), 
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('ALIGN', (0,0), (-1,-1), 'LEFT'), 
        ('ALIGN', (0,0), (0,-1), 'CENTER'), ('BOTTOMPADDING', (0,0), (-1,-1), 10), 
        ('TOPPADDING', (0,0), (-1,-1), 10), ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT_BG]), 
        ('GRID', (0,0), (-1,-1), 0.5, WHITE)
    ]))
    elements.append(t_reco)
    elements.append(Spacer(1, 20*mm))
    
    # Contact Box
    contact_data = [[Paragraph("<b>Des questions ? Nos experts sont là.</b><br/><br/>Email: thezamifrance@gmail.com<br/>Tél: 07 59 82 35 32", ParagraphStyle('contact', alignment=TA_CENTER, fontSize=10, textColor=DARK_SLATE, leading=14))]]
    t_contact = Table(contact_data, colWidths=[170*mm])
    t_contact.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), LIGHT_BG), ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('TOPPADDING', (0,0), (-1,-1), 15), ('BOTTOMPADDING', (0,0), (-1,-1), 15), ('LINEABOVE', (0,0), (-1,-1), 2, ZAMI_GREEN)]))
    elements.append(t_contact)
    
    # 3. BUILD DOCUMENT
    doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)
    
    pdf_value = buffer.getvalue()
    buffer.close()
    
    return pdf_value