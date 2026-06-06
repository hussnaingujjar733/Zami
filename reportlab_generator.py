"""
reportlab_generator.py — ZAMI Simple PDF
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

COLOR_BLUE = (0.22, 0.51, 0.96)  # #3B82F6
COLOR_GREEN = (0.13, 0.77, 0.37)  # #22C55E
COLOR_DARK = (0.06, 0.09, 0.16)   # #0F172A


class SimpleReport:
    def __init__(self, data):
        self.data = data
        self.buffer = io.BytesIO()
        self.styles = getSampleStyleSheet()
        
        # Values
        self.surface = data.get('surface', 75)
        self.dpe = data.get('dpe', 'E')
        self.cost = data.get('cost', 46500)
        self.roi = data.get('roi', 13.1)
        
        self.current_val = 280000
        self.subsidy = int(12500 * (self.surface / 68))
        self.net = self.cost - self.subsidy
        self.future_val = int(self.current_val * (1 + self.roi / 100))
        self.gain = self.future_val - self.current_val - self.net
        
        # Score
        dpe_scores = {'A': 95, 'B': 85, 'C': 70, 'D': 55, 'E': 40, 'F': 25, 'G': 10}
        self.score = dpe_scores.get(self.dpe, 40)
        
        self._create_styles()
    
    def _create_styles(self):
        self.styles.add(ParagraphStyle(
            name='Title',
            parent=self.styles['Title'],
            fontSize=32,
            alignment=TA_CENTER,
            spaceAfter=20,
        ))
        self.styles.add(ParagraphStyle(
            name='Section',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceBefore=15,
            spaceAfter=10,
        ))
        self.styles.add(ParagraphStyle(
            name='Subsection',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=12,
            spaceAfter=6,
        ))
        self.styles.add(ParagraphStyle(
            name='KPIValue',
            parent=self.styles['Normal'],
            fontSize=20,
            alignment=TA_CENTER,
            spaceAfter=2,
        ))
        self.styles.add(ParagraphStyle(
            name='KPILabel',
            parent=self.styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
        ))
        self.styles.add(ParagraphStyle(
            name='Normal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
        ))
    
    def _dpe_color(self, dpe):
        colors = {
            'A': (0.13, 0.77, 0.37), 'B': (0.29, 0.87, 0.50),
            'C': (0.64, 0.90, 0.21), 'D': (0.98, 0.80, 0.08),
            'E': (0.98, 0.57, 0.24), 'F': (0.98, 0.45, 0.09),
            'G': (0.94, 0.27, 0.27)
        }
        return colors.get(dpe, (0.5, 0.5, 0.5))
    
    def _cover(self, canvas, doc):
        canvas.saveState()
        
        # Background
        canvas.setFillColorRGB(*COLOR_DARK)
        canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
        
        # Top bar
        canvas.setFillColorRGB(*COLOR_BLUE)
        canvas.rect(0, A4[1] - 5, A4[0], 5, fill=1, stroke=0)
        
        # Title
        canvas.setFillColorRGB(1, 1, 1)
        canvas.setFont('Helvetica-Bold', 48)
        canvas.drawCentredString(A4[0]/2, A4[1] - 100, 'ZAMI')
        canvas.setFont('Helvetica', 9)
        canvas.drawCentredString(A4[0]/2, A4[1] - 120, 'RAPPORT D\'ANALYSE')
        
        # DPE Badge
        r, g, b = self._dpe_color(self.dpe)
        canvas.setFillColorRGB(r, g, b)
        canvas.roundRect(A4[0]/2 - 35, A4[1] - 250, 70, 70, 15, fill=1, stroke=0)
        canvas.setFillColorRGB(1, 1, 1)
        canvas.setFont('Helvetica-Bold', 32)
        canvas.drawCentredString(A4[0]/2, A4[1] - 220, self.dpe)
        
        # Address
        canvas.setFont('Helvetica-Bold', 12)
        addr = self.data.get('address', 'Adresse')[:55]
        canvas.drawCentredString(A4[0]/2, A4[1] - 350, addr)
        
        # Score
        canvas.setFont('Helvetica', 9)
        canvas.drawCentredString(A4[0]/2, A4[1] - 390, 'SCORE')
        canvas.setFont('Helvetica-Bold', 40)
        canvas.setFillColorRGB(*COLOR_GREEN)
        canvas.drawCentredString(A4[0]/2, A4[1] - 440, str(self.score))
        
        # Date
        canvas.setFont('Helvetica', 8)
        canvas.setFillColorRGB(0.4, 0.4, 0.4)
        canvas.drawCentredString(A4[0]/2, A4[1] - 510, datetime.now().strftime("%d/%m/%Y"))
        
        canvas.restoreState()
    
    def build(self):
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            leftMargin=15*mm,
            rightMargin=15*mm,
            topMargin=15*mm,
            bottomMargin=15*mm,
        )
        
        story = []
        
        # Page 1: Summary
        story.append(Paragraph('Synthèse', self.styles['Section']))
        story.append(Spacer(1, 5))
        story.append(Paragraph(
            "Analyse du potentiel de rénovation énergétique.",
            self.styles['Normal']
        ))
        story.append(Spacer(1, 20))
        
        # KPIs in 2 rows x 3 columns
        kpis = [
            ('Valeur actuelle', f'{self.current_val:,} €'),
            ('Coût travaux', f'{self.cost:,} €'),
            ('Subventions', f'{self.subsidy:,} €'),
            ('Valeur finale', f'{self.future_val:,} €'),
            ('Invest. net', f'{self.net:,} €'),
            ('ROI', f'+{self.roi:.1f}%'),
        ]
        
        data = []
        row = []
        for i, (label, val) in enumerate(kpis):
            row.append([Paragraph(label, self.styles['KPILabel']),
                       Paragraph(val, self.styles['KPIValue'])])
            if (i + 1) % 3 == 0:
                data.append(row)
                row = []
        
        t = Table(data, colWidths=[A4[0]/3 - 15] * 3)
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, -1), (0.95, 0.95, 0.95)),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(t)
        story.append(Spacer(1, 20))
        story.append(Paragraph(f'Gain net estimé: {self.gain:,} €', self.styles['Subsection']))
        
        # Page 2: Property details
        story.append(PageBreak())
        story.append(Paragraph('Caractéristiques', self.styles['Section']))
        story.append(Spacer(1, 10))
        
        details = [
            ['Adresse', self.data.get('address', 'N/A')[:60]],
            ['Surface', f'{int(self.surface)} m²'],
            ['DPE', self.dpe],
            ['Année', 'Avant 1975' if self.dpe in ['F','G'] else '1980-2000'],
        ]
        
        t2 = Table(details, colWidths=[60, A4[0] - 90])
        t2.setStyle(TableStyle([
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
            ('BACKGROUND', (0, 0), (-1, -1), (0.95, 0.95, 0.95)),
            ('GRID', (0, 0), (-1, -1), 0.5, (0.8, 0.8, 0.8)),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(t2)
        
        # Page 3: Recommendations
        story.append(PageBreak())
        story.append(Paragraph('Recommandations', self.styles['Section']))
        story.append(Spacer(1, 5))
        
        recos = [
            '1. Réaliser un audit énergétique complet',
            '2. Déposer une demande MaPrimeRénov\'',
            '3. Contacter des artisans certifiés RGE',
            '4. Planifier les travaux par priorité',
        ]
        for rec in recos:
            story.append(Paragraph(rec, self.styles['Normal']))
            story.append(Spacer(1, 5))
        
        # Page 4: Contact
        story.append(PageBreak())
        story.append(Spacer(1, 80))
        story.append(Paragraph('Contactez nos experts', self.styles['Section']))
        story.append(Spacer(1, 10))
        story.append(Paragraph('📧 experts@thezami.com', self.styles['Normal']))
        story.append(Paragraph('📞 +33 1 23 45 67 89', self.styles['Normal']))
        
        doc.build(story, onFirstPage=self._cover, onLaterPages=lambda c, d: None)
        return self.buffer.getvalue()


def generer_rapport(data):
    r = SimpleReport(data)
    return r.build()