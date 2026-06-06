"""
reportlab_generator.py — ZAMI Clean Layout PDF
Properly organized text, professional spacing, clean design
"""

from fpdf import FPDF
from datetime import datetime


class CleanPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=25)
    
    def header(self):
        # Top decorative line
        self.set_draw_color(34, 197, 94)
        self.set_line_width(1)
        self.line(10, 15, 200, 15)
        
        # Logo
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(34, 197, 94)
        self.set_xy(15, 6)
        self.cell(0, 6, 'ZAMI', ln=False)
        
        # Page number
        self.set_font('Helvetica', '', 8)
        self.set_text_color(128, 128, 128)
        self.set_xy(180, 7)
        self.cell(0, 4, f'Page {self.page_no()}', ln=False)
        
        self.ln(22)
    
    def footer(self):
        self.set_y(-22)
        self.set_font('Helvetica', 'I', 7)
        self.set_text_color(150, 150, 150)
        self.cell(0, 4, 'ZAMI - Property Intelligence Platform', ln=True, align='C')
    
    def title1(self, text):
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, text, ln=True)
        self.set_draw_color(34, 197, 94)
        self.line(10, self.get_y(), 45, self.get_y())
        self.ln(6)
    
    def title2(self, text):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(34, 197, 94)
        self.cell(0, 8, text, ln=True)
        self.ln(3)
    
    def text_normal(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(80, 80, 80)
        self.multi_cell(0, 6, text, align='L')
        self.ln(2)
    
    def two_cols(self, left_text, right_text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(80, 80, 80)
        self.cell(70, 7, left_text, ln=False)
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(0, 0, 0)
        self.cell(0, 7, right_text, ln=True)
    
    def three_cols(self, col1, col2, col3):
        self.set_font('Helvetica', '', 9)
        self.set_text_color(80, 80, 80)
        self.cell(60, 7, col1, ln=False)
        self.cell(60, 7, col2, ln=False)
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(0, 0, 0)
        self.cell(0, 7, col3, ln=True)
    
    def line_break(self):
        self.ln(4)
    
    def card(self, x, y, label, value):
        self.set_xy(x, y)
        self.set_fill_color(248, 250, 252)
        self.rect(x, y, 55, 32, 'F')
        self.set_font('Helvetica', '', 7)
        self.set_text_color(100, 100, 100)
        self.set_xy(x + 5, y + 5)
        self.cell(0, 4, label)
        self.set_font('Helvetica', 'B', 13)
        self.set_text_color(0, 0, 0)
        self.set_xy(x + 5, y + 15)
        self.cell(0, 6, value)


def generer_rapport(property_data):
    """Generate clean, properly organized PDF report"""
    
    # Calculate values
    surface = property_data.get('surface', 75)
    dpe = property_data.get('dpe', 'E')
    cost = property_data.get('cost', 46500)
    roi = property_data.get('roi', 13.1)
    
    current_val = 280000
    subsidy = int(12500 * (surface / 68))
    net = cost - subsidy
    future_val = int(current_val * (1 + roi / 100))
    gain = future_val - current_val - net
    
    # Scores
    dpe_scores = {'A': 95, 'B': 85, 'C': 70, 'D': 55, 'E': 40, 'F': 25, 'G': 10}
    total_score = dpe_scores.get(dpe, 40)
    
    pdf = CleanPDF()
    
    # ============================================
    # COVER PAGE
    # ============================================
    pdf.add_page()
    
    pdf.set_y(60)
    pdf.set_font('Helvetica', 'B', 44)
    pdf.set_text_color(34, 197, 94)
    pdf.cell(0, 20, 'ZAMI', ln=True, align='C')
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 8, 'PROPERTY INTELLIGENCE REPORT', ln=True, align='C')
    pdf.ln(15)
    
    # Address
    address = property_data.get('address', 'Property Address')[:60]
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 7, address, align='C')
    pdf.ln(10)
    
    # DPE Badge
    dpe_colors = {
        'A': (34, 197, 94), 'B': (74, 222, 128), 'C': (163, 230, 53),
        'D': (250, 204, 21), 'E': (251, 146, 60), 'F': (249, 115, 22),
        'G': (239, 68, 68)
    }
    color = dpe_colors.get(dpe, (100, 100, 100))
    pdf.set_fill_color(color[0], color[1], color[2])
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 48)
    pdf.set_x(210/2 - 25)
    pdf.cell(50, 50, dpe, border=0, align='C', fill=True)
    pdf.ln(18)
    
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, f'ZAMI SCORE: {total_score}/100', ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 5, datetime.now().strftime("%d %B %Y"), ln=True, align='C')
    
    # ============================================
    # PAGE 1: EXECUTIVE SUMMARY
    # ============================================
    pdf.add_page()
    pdf.title1('Executive Summary')
    pdf.text_normal('This report provides a comprehensive analysis of the property\'s energy renovation potential, including financial projections, subsidy eligibility, and strategic recommendations.')
    
    pdf.ln(8)
    
    # KPI Cards
    start_y = pdf.get_y()
    cards = [
        ('Current Value', f'EUR {current_val:,}'),
        ('Renovation Cost', f'EUR {cost:,}'),
        ('Subsidy', f'EUR {subsidy:,}'),
        ('Future Value', f'EUR {future_val:,}'),
        ('Net Investment', f'EUR {net:,}'),
        ('ROI', f'+{roi:.1f}%'),
    ]
    
    for i, (label, value) in enumerate(cards):
        x = 15 + (i % 3) * 60
        y = start_y + (i // 3) * 38
        pdf.card(x, y, label, value)
    
    pdf.ln(80)
    
    # Net Gain
    pdf.title2('Estimated Net Gain After Renovation')
    pdf.set_font('Helvetica', 'B', 15)
    pdf.set_text_color(34, 197, 94)
    pdf.cell(0, 8, f'+EUR {gain:,}', ln=True)
    
    # ============================================
    # PAGE 2: PROPERTY DETAILS
    # ============================================
    pdf.add_page()
    pdf.title1('Property Details')
    
    pdf.two_cols('Address:', property_data.get('address', 'N/A')[:50])
    pdf.two_cols('Surface Area:', f'{int(surface)} m2')
    pdf.two_cols('Current DPE Rating:', dpe)
    
    year_text = 'Pre-1975 (estimated)' if dpe in ['F','G'] else '1980-2000 (estimated)'
    pdf.two_cols('Construction Year:', year_text)
    
    pdf.two_cols('Energy Consumption:', 'Estimated 250-350 kWh/m2/year')
    pdf.two_cols('CO2 Emissions:', 'Estimated 45-65 kg/m2/year')
    
    pdf.ln(8)
    pdf.title1('ZAMI Score Breakdown')
    
    pdf.three_cols('Energy Performance', f'{total_score}/100', 'Based on DPE rating')
    pdf.three_cols('Investment Potential', f'{roi:.1f}% ROI', 'Based on projected return')
    pdf.three_cols('Market Conditions', 'Standard', 'Location-based assessment')
    
    # ============================================
    # PAGE 3: FINANCIAL ANALYSIS
    # ============================================
    pdf.add_page()
    pdf.title1('Financial Analysis')
    
    pdf.title2('Investment Waterfall')
    pdf.two_cols('Current Property Value:', f'EUR {current_val:,}')
    pdf.two_cols('Renovation Investment:', f'-EUR {cost:,}')
    pdf.two_cols('Government Subsidies:', f'+EUR {subsidy:,}')
    pdf.two_cols('Net Investment:', f'EUR {net:,}')
    pdf.two_cols('Value Appreciation:', f'+EUR {future_val - current_val:,}')
    pdf.two_cols('Future Property Value:', f'EUR {future_val:,}')
    pdf.two_cols('Net Gain:', f'+EUR {gain:,}')
    
    pdf.ln(8)
    pdf.title2('Subsidy Details')
    pdf.text_normal(f'Estimated MaPrimeRenev Subsidy: EUR {subsidy:,}')
    pdf.text_normal('Additional regional subsidies may be available depending on location.')
    
    # ============================================
    # PAGE 4: RECOMMENDATIONS
    # ============================================
    pdf.add_page()
    pdf.title1('Renovation Recommendations')
    
    if dpe in ['F', 'G']:
        recos = [
            ('Priority 1', 'Energy Audit', 'EUR 500-1,000', 'Week 1'),
            ('Priority 2', 'Wall Insulation', 'EUR 12,000-18,000', 'Week 2-4'),
            ('Priority 3', 'Attic Insulation', 'EUR 8,000-12,000', 'Week 4-5'),
            ('Priority 4', 'Heating System', 'EUR 10,000-15,000', 'Week 6-8'),
            ('Priority 5', 'Final Audit', 'EUR 500-1,000', 'Week 9'),
        ]
    elif dpe == 'E':
        recos = [
            ('Priority 1', 'Heating Upgrade', 'EUR 10,000-15,000', 'Week 1-3'),
            ('Priority 2', 'Window Replacement', 'EUR 8,000-12,000', 'Week 3-5'),
            ('Priority 3', 'Ventilation', 'EUR 4,000-7,000', 'Week 5-6'),
        ]
    else:
        recos = [
            ('Priority 1', 'Heating Optimization', 'EUR 500-2,000', 'Week 1'),
            ('Priority 2', 'Window Upgrade', 'EUR 6,000-10,000', 'Week 2-3'),
            ('Priority 3', 'Solar Assessment', 'EUR 500', 'Week 3-4'),
        ]
    
    # Table header
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(34, 197, 94)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(30, 8, 'Priority', border=1, align='C', fill=True)
    pdf.cell(60, 8, 'Action', border=1, align='C', fill=True)
    pdf.cell(45, 8, 'Cost Range', border=1, align='C', fill=True)
    pdf.cell(45, 8, 'Timeline', border=1, align='C', fill=True)
    pdf.ln()
    
    # Table rows
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Helvetica', '', 9)
    fill = False
    for rec in recos:
        pdf.cell(30, 7, rec[0], border=1, align='L', fill=fill)
        pdf.cell(60, 7, rec[1], border=1, align='L', fill=fill)
        pdf.cell(45, 7, rec[2], border=1, align='L', fill=fill)
        pdf.cell(45, 7, rec[3], border=1, align='L', fill=fill)
        pdf.ln()
        fill = not fill
    
    pdf.ln(8)
    
    if dpe in ['F', 'G']:
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(239, 68, 68)
        pdf.cell(0, 6, 'IMPORTANT: This property faces rental restrictions starting 2025.', ln=True)
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(80, 80, 80)
        pdf.multi_cell(0, 6, 'Immediate renovation is recommended to maintain asset value and rental income.')
    
    # ============================================
    # PAGE 5: NEXT STEPS
    # ============================================
    pdf.add_page()
    pdf.title1('Next Steps')
    
    steps = [
        '1. Schedule an on-site energy audit with a certified professional',
        '2. Submit MaPrimeRenev subsidy application (processing: 4-6 weeks)',
        '3. Obtain at least 3 quotes from RGE-certified contractors',
        '4. Review financing options (Eco-PTZ, bank loans, local grants)',
        '5. Plan renovation work according to priority order',
        '6. Schedule post-renovation audit to validate DPE improvement',
    ]
    
    for step in steps:
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(80, 80, 80)
        pdf.multi_cell(0, 7, step, align='L')
        pdf.ln(2)
    
    pdf.ln(15)
    
    pdf.title1('Contact Information')
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 7, 'Email: experts@thezami.com', ln=True, align='C')
    pdf.cell(0, 7, 'Phone: +33 (0)1 23 45 67 89', ln=True, align='C')
    pdf.cell(0, 7, 'Website: thezami.com', ln=True, align='C')
    
    pdf.ln(10)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 5, 'This report is an AI-generated estimate. Final figures require on-site technical audit.', ln=True, align='C')
    
    # Return PDF bytes
    output = pdf.output(dest='S')
    if isinstance(output, str):
        output = output.encode('latin-1', errors='replace')
    
    return output


make_report = generer_rapport