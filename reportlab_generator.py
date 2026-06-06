"""
reportlab_generator.py — ZAMI Professional PDF Generator
"""

from fpdf import FPDF
from datetime import datetime


class ZamiPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=25)
    
    def header(self):
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(0, 0, 0)
        self.cell(0, 8, 'ZAMI', ln=True, align='C')
        self.set_font('Helvetica', '', 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, 'PROPERTY INTELLIGENCE REPORT', ln=True, align='C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-25)
        self.set_font('Helvetica', 'I', 7)
        self.set_text_color(128, 128, 128)
        self.cell(0, 5, 'ZAMI - Property Intelligence Platform', ln=True, align='C')
        self.cell(0, 5, 'This is an AI-generated estimate. Consult certified professionals.', ln=True, align='C')


def generer_rapport(property_data):
    """Generate professional PDF report"""
    
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
    energy_score = dpe_scores.get(dpe, 40)
    compliance_score = 100 if dpe in ['A','B','C'] else (70 if dpe in ['D','E'] else 40)
    investment_score = 90 if roi >= 20 else (70 if roi >= 12 else 40)
    market_score = 80 if property_data.get('zipcode', '75')[:2] in ['75','92','94'] else 60
    
    pdf = ZamiPDF()
    pdf.add_page()
    
    # ============================================
    # PAGE 1: COVER + SUMMARY
    # ============================================
    
    # Date
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, f'Generated: {datetime.now().strftime("%d/%m/%Y")}', ln=True, align='R')
    pdf.ln(5)
    
    # Address
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(0, 0, 0)
    address = property_data.get('address', 'Address not available')[:65]
    pdf.multi_cell(0, 7, address, align='C')
    pdf.ln(8)
    
    # DPE Badge
    dpe_colors = {'A': (34,197,94), 'B': (74,222,128), 'C': (163,230,53),
                  'D': (250,204,21), 'E': (251,146,60), 'F': (249,115,22),
                  'G': (239,68,68)}
    color = dpe_colors.get(dpe, (100,100,100))
    pdf.set_fill_color(*color)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 52)
    pdf.set_x(210/2 - 25)
    pdf.cell(50, 50, dpe, border=0, align='C', fill=True)
    pdf.ln(15)
    
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, 'ENERGY PERFORMANCE RATING', ln=True, align='C')
    pdf.ln(12)
    
    # Key Metrics Section
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, 'KEY METRICS', ln=True, align='L')
    pdf.line(10, pdf.get_y(), 55, pdf.get_y())
    pdf.ln(5)
    
    # Metrics in 3 columns
    metrics = [
        ('SURFACE', f"{int(surface)} m²"),
        ('CURRENT DPE', dpe),
        ('RENOVATION COST', f"€{cost:,}"),
        ('SUBSIDY', f"€{subsidy:,}"),
        ('NET INVESTMENT', f"€{net:,}"),
        ('EXPECTED ROI', f"+{roi:.1f}%"),
    ]
    
    y_start = pdf.get_y()
    for i, (label, value) in enumerate(metrics):
        x = 15 + (i % 3) * 60
        y = y_start + (i // 3) * 20
        pdf.set_xy(x, y)
        pdf.set_font('Helvetica', '', 7)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(50, 5, label, ln=False, align='C')
        pdf.set_xy(x, y + 5)
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(50, 7, value, ln=False, align='C')
    
    pdf.ln(45)
    
    # Value Projection
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, 'VALUE PROJECTION', ln=True, align='L')
    pdf.line(10, pdf.get_y(), 55, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(60, 8, 'Current Property Value:', ln=False)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, f"€{current_val:,}", ln=True)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(60, 8, 'After Renovation:', ln=False)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(34, 197, 94)
    pdf.cell(0, 8, f"€{future_val:,}", ln=True)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(60, 8, 'Total Value Gain:', ln=False)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(34, 197, 94)
    pdf.cell(0, 8, f"+€{gain:,}", ln=True)
    
    pdf.ln(10)
    
    # ============================================
    # PAGE 2: SCORES & RECOMMENDATIONS
    # ============================================
    pdf.add_page()
    
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, 'ZAMI INTELLIGENCE SCORES', ln=True, align='L')
    pdf.line(10, pdf.get_y(), 65, pdf.get_y())
    pdf.ln(8)
    
    # Scores display
    scores = [
        ('ENERGY PERFORMANCE', energy_score),
        ('COMPLIANCE STATUS', compliance_score),
        ('INVESTMENT POTENTIAL', investment_score),
        ('MARKET CONDITIONS', market_score),
    ]
    
    for name, score in scores:
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(60, 8, name, ln=False)
        pdf.set_font('Helvetica', 'B', 9)
        pdf.set_text_color(34, 197, 94 if score >= 70 else (245, 158, 11))
        pdf.cell(0, 8, f"{score}/100", ln=True)
        pdf.ln(2)
    
    pdf.ln(5)
    
    # Overall Score
    total_score = (energy_score + compliance_score + investment_score + market_score) // 4
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, f'OVERALL ZAMI SCORE: {total_score}/100', ln=True, align='C')
    pdf.ln(10)
    
    # Recommendations
    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 8, 'RECOMMENDATIONS', ln=True, align='L')
    pdf.line(10, pdf.get_y(), 55, pdf.get_y())
    pdf.ln(8)
    
    if dpe in ['F', 'G']:
        recos = [
            '1. Complete energy audit by certified professional (mandatory)',
            '2. Apply for MaPrimeRénov\' subsidy immediately',
            '3. Prioritize wall and attic insulation (highest ROI)',
            '4. Replace heating system with heat pump',
            '5. Contact certified RGE contractors for quotes',
        ]
    elif dpe == 'E':
        recos = [
            '1. Upgrade heating system to condensing boiler or heat pump',
            '2. Replace single-glazed windows with double glazing',
            '3. Improve attic insulation',
            '4. Install programmable thermostat',
        ]
    else:
        recos = [
            '1. Optimize existing heating system settings',
            '2. Consider solar panels for additional savings',
            '3. Upgrade to energy-efficient appliances',
            '4. Install smart home energy monitoring',
        ]
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(50, 50, 50)
    for rec in recos:
        pdf.multi_cell(0, 6, rec, align='L')
        pdf.ln(1)
    
    pdf.ln(8)
    
    # Subsidy info
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, 'SUBSIDY ELIGIBILITY', ln=True, align='L')
    pdf.line(10, pdf.get_y(), 55, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 6, f'Estimated MaPrimeRénov\' Subsidy: €{subsidy:,}', ln=True, align='L')
    pdf.ln(2)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, 'Apply through official France Rénov\' platform', ln=True, align='L')
    
    # ============================================
    # PAGE 3: CONTACT & NEXT STEPS
    # ============================================
    pdf.add_page()
    pdf.set_y(60)
    
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, 'Need Professional Help?', ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 7, 'Our certified experts can help you:', ln=True, align='C')
    pdf.ln(5)
    
    services = [
        '✓ Validate this analysis with on-site audit',
        '✓ Identify additional subsidies and financing options',
        '✓ Connect you with trusted RGE-certified contractors',
        '✓ Prepare complete subsidy application files',
        '✓ Project management and quality control',
    ]
    
    pdf.set_font('Helvetica', '', 10)
    for service in services:
        pdf.cell(0, 7, service, ln=True, align='C')
        pdf.ln(1)
    
    pdf.ln(15)
    
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(59, 130, 246)
    pdf.cell(0, 8, 'CONTACT US', ln=True, align='C')
    pdf.ln(5)
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 7, '📧 experts@thezami.com', ln=True, align='C')
    pdf.cell(0, 7, '📞 +33 (0)1 23 45 67 89', ln=True, align='C')
    pdf.cell(0, 7, '🌐 thezami.com', ln=True, align='C')
    
    # Return PDF as bytes
    output = pdf.output(dest='S')
    if isinstance(output, str):
        output = output.encode('latin-1')
    
    return output


make_report = generer_rapport