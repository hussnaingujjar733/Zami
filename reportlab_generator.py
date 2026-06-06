"""
reportlab_generator.py — ZAMI Simple PDF Generator
No complex styles, just works
"""

import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors

# Colors
DARK_BLUE = colors.HexColor('#0F172A')
LIGHT_BLUE = colors.HexColor('#3B82F6')
GREEN = colors.HexColor('#22C55E')
GRAY_LIGHT = colors.HexColor('#F1F5F9')
GRAY_MID = colors.HexColor('#CBD5E1')
GRAY_TEXT = colors.HexColor('#475569')
WHITE = colors.white


def make_report(property_data):
    """Generate PDF report - simple and working"""
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=15*mm,
        rightMargin=15*mm,
        topMargin=15*mm,
        bottomMargin=15*mm,
    )
    
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    heading_style = styles['Heading2']
    
    # Get values
    surface = property_data.get('surface', 75)
    dpe = property_data.get('dpe', 'E')
    cost = property_data.get('cost', 46500)
    roi = property_data.get('roi', 13.1)
    
    current_val = 280000
    subsidy = int(12500 * (surface / 68))
    net = cost - subsidy
    future_val = int(current_val * (1 + roi / 100))
    gain = future_val - current_val - net
    
    # Score
    dpe_scores = {'A': 95, 'B': 85, 'C': 70, 'D': 55, 'E': 40, 'F': 25, 'G': 10}
    score = dpe_scores.get(dpe, 40)
    
    story = []
    
    # ========== COVER PAGE (using callback) ==========
    def cover_page(canvas, doc):
        canvas.saveState()
        
        # Background
        canvas.setFillColor(DARK_BLUE)
        canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
        
        # Top bar
        canvas.setFillColor(LIGHT_BLUE)
        canvas.rect(0, A4[1] - 5, A4[0], 5, fill=1, stroke=0)
        
        # Logo
        canvas.setFillColor(WHITE)
        canvas.setFont('Helvetica-Bold', 48)
        canvas.drawCentredString(A4[0]/2, A4[1] - 100, 'ZAMI')
        canvas.setFont('Helvetica', 9)
        canvas.drawCentredString(A4[0]/2, A4[1] - 120, 'RAPPORT D\'ANALYSE')
        
        # DPE badge
        dpe_colors = {
            'A': (0.13, 0.77, 0.37), 'B': (0.29, 0.87, 0.50),
            'C': (0.64, 0.90, 0.21), 'D': (0.98, 0.80, 0.08),
            'E': (0.98, 0.57, 0.24), 'F': (0.98, 0.45, 0.09),
            'G': (0.94, 0.27, 0.27)
        }
        r, g, b = dpe_colors.get(dpe, (0.5, 0.5, 0.5))
        canvas.setFillColorRGB(r, g, b)
        canvas.roundRect(A4[0]/2 - 35, A4[1] - 250, 70, 70, 15, fill=1, stroke=0)
        canvas.setFillColor(WHITE)
        canvas.setFont('Helvetica-Bold', 32)
        canvas.drawCentredString(A4[0]/2, A4[1] - 220, dpe)
        
        # Address
        canvas.setFont('Helvetica-Bold', 12)
        addr = property_data.get('address', 'Adresse')[:55]
        canvas.drawCentredString(A4[0]/2, A4[1] - 350, addr)
        
        # Score
        canvas.setFont('Helvetica', 9)
        canvas.drawCentredString(A4[0]/2, A4[1] - 390, 'POTENTIEL')
        canvas.setFont('Helvetica-Bold', 40)
        canvas.setFillColor(GREEN)
        canvas.drawCentredString(A4[0]/2, A4[1] - 440, str(score))
        
        # Date
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(GRAY_TEXT)
        canvas.drawCentredString(A4[0]/2, A4[1] - 510, datetime.now().strftime("%d/%m/%Y"))
        
        canvas.restoreState()
    
    # ========== PAGE 1: Summary ==========
    story.append(Paragraph('SYNTHESE', heading_style))
    story.append(Spacer(1, 5))
    story.append(Paragraph(
        "Analyse du potentiel de renovation energetique du bien.",
        normal_style
    ))
    story.append(Spacer(1, 20))
    
    # KPI table
    kpi_data = [
        ['Valeur actuelle', f'{current_val:,} €'],
        ['Cout travaux', f'{cost:,} €'],
        ['Subventions', f'{subsidy:,} €'],
        ['Valeur finale', f'{future_val:,} €'],
        ['Investissement net', f'{net:,} €'],
        ['ROI', f'+{roi:.1f}%'],
    ]
    
    # 3 columns layout
    table_data = [
        [kpi_data[0][0], kpi_data[1][0], kpi_data[2][0]],
        [kpi_data[0][1], kpi_data[1][1], kpi_data[2][1]],
        ['', '', ''],
        [kpi_data[3][0], kpi_data[4][0], kpi_data[5][0]],
        [kpi_data[3][1], kpi_data[4][1], kpi_data[5][1]],
    ]
    
    t = Table(table_data, colWidths=[A4[0]/3 - 15] * 3)
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 8),
        ('FONT', (0, 1), (-1, 1), 'Helvetica-Bold', 16),
        ('FONT', (0, 3), (-1, 3), 'Helvetica-Bold', 8),
        ('FONT', (0, 4), (-1, 4), 'Helvetica-Bold', 16),
        ('TEXTCOLOR', (0, 4), (-1, 4), GREEN),
        ('BACKGROUND', (0, 1), (-1, 1), GRAY_LIGHT),
        ('BACKGROUND', (0, 4), (-1, 4), GRAY_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))
    story.append(Paragraph(f'Gain net estime: {gain:,} €', heading_style))
    
    # ========== PAGE 2: Property details ==========
    story.append(PageBreak())
    story.append(Paragraph('CARACTERISTIQUES', heading_style))
    story.append(Spacer(1, 10))
    
    details = [
        ['Adresse', property_data.get('address', 'N/A')[:65]],
        ['Surface', f'{int(surface)} m²'],
        ['DPE', dpe],
        ['Construction', 'Avant 1975' if dpe in ['F','G'] else '1980-2000'],
    ]
    
    t2 = Table(details, colWidths=[50, A4[0] - 85])
    t2.setStyle(TableStyle([
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
        ('FONT', (1, 0), (1, -1), 'Helvetica', 10),
        ('BACKGROUND', (0, 0), (-1, -1), GRAY_LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY_MID),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t2)
    
    # ========== PAGE 3: Recommendations ==========
    story.append(PageBreak())
    story.append(Paragraph('RECOMMANDATIONS', heading_style))
    story.append(Spacer(1, 10))
    
    recos = [
        '1. Realiser un audit energetique complet',
        '2. Deposer une demande MaPrimeRenov',
        '3. Contacter des artisans certifies RGE',
        '4. Planifier les travaux par priorite',
    ]
    for rec in recos:
        story.append(Paragraph(rec, normal_style))
        story.append(Spacer(1, 5))
    
    # ========== PAGE 4: Contact ==========
    story.append(PageBreak())
    story.append(Spacer(1, 80))
    story.append(Paragraph('CONTACTEZ NOS EXPERTS', heading_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph(' experts@thezami.com', normal_style))
    story.append(Paragraph(' +33 1 23 45 67 89', normal_style))
    story.append(Spacer(1, 30))
    story.append(Paragraph(
        "Rapport preliminaire - validation sur site recommandee",
        normal_style
    ))
    
    # Build document
    doc.build(story, onFirstPage=cover_page, onLaterPages=lambda c, d: None)
    
    return buffer.getvalue()


def generer_rapport(property_data):
    """Main function to generate PDF report"""
    return make_report(property_data)