"""
reportlab_generator.py — ZAMI Premium Institutional Report Generator
ReportLab based - McKinsey/Deloitte/JLL/CBRE/BNP Paribas Grade
"""

import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak
)
from reportlab.graphics.shapes import Drawing, Rect, Circle, String
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# Register fonts (using standard fonts for compatibility)
try:
    pdfmetrics.registerFont(TTFont('HelveticaNeue', 'Helvetica'))
    pdfmetrics.registerFont(TTFont('HelveticaNeue-Bold', 'Helvetica-Bold'))
except:
    pass

# Color Palette - Institutional Premium
COLORS = {
    'primary': colors.HexColor('#0F172A'),
    'secondary': colors.HexColor('#1E293B'),
    'accent_blue': colors.HexColor('#3B82F6'),
    'success': colors.HexColor('#22C55E'),
    'warning': colors.HexColor('#F59E0B'),
    'danger': colors.HexColor('#EF4444'),
    'gray_light': colors.HexColor('#F1F5F9'),
    'gray_mid': colors.HexColor('#CBD5E1'),
    'gray_dark': colors.HexColor('#475569'),
    'white': colors.HexColor('#FFFFFF'),
    'black': colors.HexColor('#1E293B'),
}


class ReportStyles:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        self.styles.add(ParagraphStyle(
            name='CoverTitle',
            fontName='Helvetica-Bold',
            fontSize=42,
            textColor=COLORS['white'],
            alignment=TA_CENTER,
            spaceAfter=30,
        ))
        self.styles.add(ParagraphStyle(
            name='CoverSubtitle',
            fontName='Helvetica',
            fontSize=12,
            textColor=colors.HexColor('#CBD5E1'),
            alignment=TA_CENTER,
            spaceAfter=40,
        ))
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            fontName='Helvetica-Bold',
            fontSize=18,
            textColor=COLORS['primary'],
            spaceBefore=20,
            spaceAfter=10,
        ))
        self.styles.add(ParagraphStyle(
            name='SectionHeaderLine',
            fontName='Helvetica-Bold',
            fontSize=16,
            textColor=COLORS['accent_blue'],
            spaceBefore=15,
            spaceAfter=8,
        ))
        self.styles.add(ParagraphStyle(
            name='KPILarge',
            fontName='Helvetica-Bold',
            fontSize=24,
            textColor=COLORS['primary'],
            alignment=TA_CENTER,
        ))
        self.styles.add(ParagraphStyle(
            name='KPIMedium',
            fontName='Helvetica-Bold',
            fontSize=16,
            textColor=COLORS['primary'],
            alignment=TA_CENTER,
        ))
        self.styles.add(ParagraphStyle(
            name='BodyText',
            fontName='Helvetica',
            fontSize=10,
            textColor=COLORS['gray_dark'],
            alignment=TA_LEFT,
            spaceAfter=6,
        ))
        self.styles.add(ParagraphStyle(
            name='MetricLabel',
            fontName='Helvetica',
            fontSize=8,
            textColor=COLORS['gray_mid'],
            alignment=TA_CENTER,
        ))
        self.styles.add(ParagraphStyle(
            name='ScoreValue',
            fontName='Helvetica-Bold',
            fontSize=36,
            textColor=COLORS['accent_blue'],
            alignment=TA_CENTER,
        ))


class PremiumZamiReport:
    def __init__(self, property_data):
        self.property_data = property_data
        self.styles = ReportStyles().styles
        self.buffer = io.BytesIO()
        
        # Calculate derived values
        self.surface = property_data.get('surface', 75.0)
        self.dpe = property_data.get('dpe', 'E')
        self.current_value = 280000
        self.renovation_cost = property_data.get('cost', 46500)
        self.roi = property_data.get('roi', 13.1)
        self.subsidy = int(12500 * (self.surface / 68))
        self.net_investment = self.renovation_cost - self.subsidy
        self.future_value = int(self.current_value * (1 + self.roi / 100))
        self.net_gain = self.future_value - self.current_value - self.net_investment
        
        # ZAMI Scores
        dpe_scores = {'A': 95, 'B': 85, 'C': 70, 'D': 55, 'E': 40, 'F': 25, 'G': 10}
        self.energy_score = dpe_scores.get(self.dpe, 40)
        
        compliance_scores = {'A': 100, 'B': 100, 'C': 85, 'D': 65, 'E': 45, 'F': 25, 'G': 10}
        self.compliance_score = compliance_scores.get(self.dpe, 45)
        
        if self.roi >= 25:
            self.investment_score = 90
        elif self.roi >= 18:
            self.investment_score = 75
        elif self.roi >= 12:
            self.investment_score = 55
        elif self.roi >= 8:
            self.investment_score = 35
        else:
            self.investment_score = 20
        
        zipcode = self.property_data.get('zipcode', '75000')
        region = str(zipcode)[:2]
        market_scores = {'75': 85, '92': 80, '93': 65, '94': 75, '69': 70, '13': 65, '31': 60}
        self.market_score = market_scores.get(region, 50)
        
        self.zami_score = int((self.energy_score + self.compliance_score + 
                               self.investment_score + self.market_score) / 4)
    
    def _draw_dpe_badge(self, canvas, x, y, size, dpe):
        colors_map = {
            'A': (34, 197, 94), 'B': (74, 222, 128), 'C': (163, 230, 53),
            'D': (250, 204, 21), 'E': (251, 146, 60), 'F': (249, 115, 22),
            'G': (239, 68, 68)
        }
        bg_color = colors_map.get(dpe, (100, 100, 100))
        canvas.setFillColorRGB(bg_color[0]/255, bg_color[1]/255, bg_color[2]/255)
        canvas.roundRect(x, y, size, size, size/4, fill=1, stroke=0)
        canvas.setFillColorRGB(1, 1, 1)
        canvas.setFont('Helvetica-Bold', size * 0.5)
        canvas.drawCentredString(x + size/2, y + size/2 - size*0.1, dpe)
    
    def create_cover_page(self):
        def draw_cover(canvas, doc):
            canvas.saveState()
            canvas.setFillColor(COLORS['primary'])
            canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
            canvas.setFillColor(COLORS['accent_blue'])
            canvas.rect(0, A4[1] - 8, A4[0], 8, fill=1, stroke=0)
            
            canvas.setFillColor(COLORS['white'])
            canvas.setFont('Helvetica-Bold', 48)
            canvas.drawCentredString(A4[0]/2, A4[1] - 120, 'ZAMI')
            canvas.setFont('Helvetica', 10)
            canvas.setFillColor(colors.HexColor('#CBD5E1'))
            canvas.drawCentredString(A4[0]/2, A4[1] - 140, 'PROPERTY INTELLIGENCE REPORT')
            
            self._draw_dpe_badge(canvas, A4[0]/2 - 40, A4[1] - 280, 80, self.dpe)
            
            canvas.setFont('Helvetica-Bold', 16)
            canvas.setFillColor(COLORS['white'])
            address = self.property_data.get('address', 'Property Address')[:60]
            canvas.drawCentredString(A4[0]/2, A4[1] - 400, address)
            
            canvas.setFont('Helvetica', 10)
            canvas.setFillColor(colors.HexColor('#94A3B8'))
            canvas.drawCentredString(A4[0]/2, A4[1] - 440, 'OPPORTUNITY SCORE')
            canvas.setFont('Helvetica-Bold', 48)
            canvas.setFillColor(COLORS['success'])
            canvas.drawCentredString(A4[0]/2, A4[1] - 480, str(self.zami_score))
            canvas.setFont('Helvetica', 8)
            canvas.drawCentredString(A4[0]/2, A4[1] - 500, 'out of 100')
            
            canvas.setFont('Helvetica', 8)
            canvas.setFillColor(colors.HexColor('#64748B'))
            canvas.drawCentredString(A4[0]/2, A4[1] - 560, 
                                    f'Generated: {datetime.now().strftime("%d %B %Y")}')
            
            canvas.setFillColor(colors.HexColor('#1E293B'))
            canvas.rect(0, 0, A4[0], 60, fill=1, stroke=0)
            canvas.setFont('Helvetica', 7)
            canvas.setFillColor(colors.HexColor('#64748B'))
            canvas.drawCentredString(A4[0]/2, 25, 'ZAMI - France\'s Property Intelligence Platform')
            canvas.drawCentredString(A4[0]/2, 15, 'Confidential - For Professional Use Only')
            canvas.restoreState()
        return draw_cover
    
    def create_executive_summary(self):
        story = []
        story.append(Paragraph('Executive Summary', self.styles['SectionHeader']))
        story.append(Spacer(1, 5))
        story.append(Paragraph(
            'This report provides a comprehensive analysis of the property\'s energy renovation potential.',
            self.styles['BodyText']
        ))
        story.append(Spacer(1, 20))
        
        kpi_data = [
            [Paragraph('Current Value', self.styles['MetricLabel']),
             Paragraph('Renovation Cost', self.styles['MetricLabel']),
             Paragraph('Available Subsidies', self.styles['MetricLabel'])],
            [Paragraph(f'€{self.current_value:,}', self.styles['KPILarge']),
             Paragraph(f'€{self.renovation_cost:,}', self.styles['KPILarge']),
             Paragraph(f'€{self.subsidy:,}', self.styles['KPILarge'])],
            [Spacer(1, 5), Spacer(1, 5), Spacer(1, 5)],
            [Paragraph('Expected Value', self.styles['MetricLabel']),
             Paragraph('Net Investment', self.styles['MetricLabel']),
             Paragraph('Total ROI', self.styles['MetricLabel'])],
            [Paragraph(f'€{self.future_value:,}', self.styles['KPILarge']),
             Paragraph(f'€{self.net_investment:,}', self.styles['KPILarge']),
             Paragraph(f'+{self.roi:.1f}%', self.styles['KPILarge'])],
        ]
        
        kpi_table = Table(kpi_data, colWidths=[A4[0]/3 - 20] * 3)
        kpi_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 1), (-1, 1), COLORS['gray_light']),
            ('BACKGROUND', (0, 4), (-1, 4), COLORS['gray_light']),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(kpi_table)
        story.append(Spacer(1, 30))
        story.append(Paragraph(
            f'<b>Estimated Net Gain After Renovation: €{self.net_gain:,}</b>',
            self.styles['SectionHeaderLine']
        ))
        return story
    
    def create_property_intelligence(self):
        story = []
        story.append(Paragraph('Property Intelligence', self.styles['SectionHeader']))
        story.append(Spacer(1, 10))
        
        details_data = [
            ['Address', self.property_data.get('address', 'N/A')[:80]],
            ['Surface', f"{int(self.surface)} m²"],
            ['Current DPE', self.dpe],
            ['Construction Year', 'Estimated: Pre-1975' if self.dpe in ['F', 'G'] else 'Estimated: 1980-2000'],
        ]
        
        details_table = Table(details_data, colWidths=[80, A4[0] - 100])
        details_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
            ('TEXTCOLOR', (0, 0), (0, -1), COLORS['accent_blue']),
            ('BACKGROUND', (0, 0), (-1, -1), COLORS['white']),
            ('GRID', (0, 0), (-1, -1), 0.5, COLORS['gray_mid']),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(details_table)
        return story
    
    def create_zami_score(self):
        story = []
        story.append(Paragraph('ZAMI Intelligence Score', self.styles['SectionHeader']))
        story.append(Spacer(1, 15))
        
        scores = [
            ('Energy Performance', self.energy_score, COLORS['warning']),
            ('Compliance Status', self.compliance_score, COLORS['accent_blue']),
            ('Investment Potential', self.investment_score, COLORS['success']),
            ('Market Conditions', self.market_score, COLORS['warning']),
        ]
        
        for name, score, color in scores:
            drawing = Drawing(400, 40)
            bg_rect = Rect(120, 10, 250, 12, fillColor=COLORS['gray_light'])
            drawing.add(bg_rect)
            fill_rect = Rect(120, 10, 250 * score / 100, 12, fillColor=color)
            drawing.add(fill_rect)
            label_text = String(15, 20, name, fontSize=10, fillColor=COLORS['gray_dark'])
            drawing.add(label_text)
            score_text = String(380, 20, f'{score}/100', fontSize=10, fillColor=color, textAnchor='end')
            drawing.add(score_text)
            story.append(drawing)
            story.append(Spacer(1, 10))
        
        story.append(Spacer(1, 20))
        story.append(Paragraph('OVERALL ZAMI SCORE', self.styles['SectionHeaderLine']))
        
        score_drawing = Drawing(200, 120)
        circle_bg = Circle(100, 60, 45, fillColor=COLORS['gray_light'], strokeColor=COLORS['gray_mid'])
        score_drawing.add(circle_bg)
        score_text = String(100, 60, str(self.zami_score), fontSize=36, 
                           fillColor=COLORS['accent_blue'], textAnchor='middle')
        score_drawing.add(score_text)
        out_of_text = String(100, 85, 'out of 100', fontSize=8, 
                            fillColor=COLORS['gray_dark'], textAnchor='middle')
        score_drawing.add(out_of_text)
        story.append(score_drawing)
        
        if self.zami_score >= 70:
            interpretation = 'Strong investment opportunity with excellent renovation potential.'
        elif self.zami_score >= 50:
            interpretation = 'Good potential. Strategic renovation can unlock significant value.'
        else:
            interpretation = 'Attention required. Immediate renovation recommended to capture value.'
        story.append(Spacer(1, 10))
        story.append(Paragraph(interpretation, self.styles['BodyText']))
        return story
    
    def create_renovation_roadmap(self):
        story = []
        story.append(PageBreak())
        story.append(Paragraph('Renovation Roadmap', self.styles['SectionHeader']))
        story.append(Spacer(1, 15))
        
        if self.dpe in ['F', 'G']:
            priorities = [
                ('1. Wall Insulation', '€12,000 - €18,000', '25-30% reduction', '+8-10% ROI'),
                ('2. Roof/Attic Insulation', '€8,000 - €12,000', '20-25% reduction', '+6-8% ROI'),
                ('3. Heating System Upgrade', '€10,000 - €15,000', '30-35% reduction', '+10-12% ROI'),
            ]
        elif self.dpe == 'E':
            priorities = [
                ('1. Heating System Upgrade', '€10,000 - €15,000', '30-35% reduction', '+10-12% ROI'),
                ('2. Window Replacement', '€8,000 - €12,000', '15-20% reduction', '+5-7% ROI'),
                ('3. Ventilation System', '€4,000 - €7,000', '10-15% reduction', '+3-5% ROI'),
            ]
        else:
            priorities = [
                ('1. Window Optimization', '€6,000 - €10,000', '10-15% reduction', '+4-6% ROI'),
                ('2. Smart Thermostat', '€500 - €1,500', '8-12% reduction', '+2-3% ROI'),
                ('3. Lighting Upgrade', '€2,000 - €4,000', '5-8% reduction', '+1-2% ROI'),
            ]
        
        for priority in priorities:
            story.append(Spacer(1, 10))
            story.append(Paragraph(f'<b>{priority[0]}</b>', self.styles['SectionHeaderLine']))
            metrics = [['Estimated Cost', 'Energy Impact', 'ROI Contribution'],
                       [priority[1], priority[2], priority[3]]]
            metrics_table = Table(metrics, colWidths=[120, 130, 130])
            metrics_table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 9),
                ('BACKGROUND', (0, 0), (-1, 0), COLORS['gray_light']),
                ('FONT', (0, 1), (-1, 1), 'Helvetica', 10),
                ('BACKGROUND', (0, 1), (-1, 1), COLORS['white']),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 0.5, COLORS['gray_mid']),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(metrics_table)
            story.append(Spacer(1, 5))
        
        story.append(Spacer(1, 20))
        story.append(Paragraph(
            f'<b>Total Recommended Investment: €{self.renovation_cost:,}</b>',
            self.styles['SectionHeaderLine']
        ))
        return story
    
    def create_cta_section(self):
        story = []
        story.append(PageBreak())
        story.append(Spacer(1, 80))
        story.append(Paragraph('Book a ZAMI Expert Consultation', self.styles['SectionHeader']))
        story.append(Spacer(1, 10))
        story.append(Paragraph(
            'Our certified experts will validate this analysis, identify additional subsidies, '
            'and connect you with trusted RGE contractors.',
            self.styles['BodyText']
        ))
        story.append(Spacer(1, 20))
        story.append(Paragraph('<b>Contact our team:</b>', self.styles['BodyText']))
        story.append(Paragraph('📧 experts@thezami.com', self.styles['BodyText']))
        story.append(Paragraph('📞 +33 (0)1 23 45 67 89', self.styles['BodyText']))
        story.append(Spacer(1, 30))
        story.append(Paragraph(
            '<i>This report is a preliminary analysis. Final figures require on-site technical audit.</i>',
            self.styles['BodyText']
        ))
        return story
    
    def build_report(self):
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            leftMargin=20*mm,
            rightMargin=20*mm,
            topMargin=15*mm,
            bottomMargin=15*mm,
        )
        
        all_elements = []
        cover_callback = self.create_cover_page()
        all_elements.extend(self.create_executive_summary())
        all_elements.append(PageBreak())
        all_elements.extend(self.create_property_intelligence())
        all_elements.append(PageBreak())
        all_elements.extend(self.create_zami_score())
        all_elements.append(PageBreak())
        all_elements.extend(self.create_renovation_roadmap())
        all_elements.append(PageBreak())
        all_elements.extend(self.create_cta_section())
        
        doc.build(all_elements, onFirstPage=cover_callback, onLaterPages=lambda c, d: None)
        return self.buffer.getvalue()


def generate_premium_report(property_data):
    """Main entry point - generates institutional-grade PDF report"""
    report = PremiumZamiReport(property_data)
    return report.build_report()