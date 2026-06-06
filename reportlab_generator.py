"""
reportlab_generator.py — ZAMI Enhanced PDF Generator
Better quality, professional layout
"""

from fpdf import FPDF
from datetime import datetime
import os


class ZamiPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=25)
        self.set_compression(True)  # Better compression
    
    def header(self):
        # Add small logo area
        self.set_font('Helvetica', 'B', 20)
        self.set_text_color(34, 197, 94)  # ZAMI Green
        self.cell(0, 8, 'ZAMI', ln=True, align='C')
        self.set_font('Helvetica', '', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 4, 'PROPERTY INTELLIGENCE REPORT', ln=True, align='C')
        self.ln(3)
        # Decorative line
        self.set_draw_color(34, 197, 94)
        self.set_line_width(0.5)
        self.line(60, self.get_y(), 150, self.get_y())
        self.ln(6)
    
    def footer(self):
        self.set_y(-20)
        self.set_font('Helvetica', 'I', 7)
        self.set_text_color(150, 150, 150)
        self.cell(0, 4, f'ZAMI - Property Intelligence Platform | Page {self.page_no()}', ln=True, align='C')
    
    def section_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(0, 0, 0)
        self.cell(0, 8, title, ln=True, align='L')
        self.set_draw_color(34, 197, 94)
        self.line(10, self.get_y(), 50, self.get_y())
        self.ln(6)
    
    def metric_card(self, x, y, label, value, highlight=False):
        self.set_xy(x, y)
        self.set_fill_color(245, 248, 250)
        self.rect(x, y, 55, 30, 'F')
        self.set_font('Helvetica', '', 7)
        self.set_text_color(100, 100, 100)
        self.set_xy(x + 5, y + 5)
        self.cell(45, 4, label, ln=False)
        self.set_font('Helvetica', 'B', 12)
        if highlight:
            self.set_text_color(34, 197, 94)
        else:
            self.set_text_color(0, 0, 0)
        self.set_xy(x + 5, y + 15)
        self.cell(45, 6, value, ln=False)


def generer_rapport(property_data):
    """Generate enhanced professional PDF report"""
    
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
    # COVER SECTION
    # ============================================
    
    # Date
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 5, f'Generated: {datetime.now().strftime("%d %B %Y")}', ln=True, align='R')
    pdf.ln(15)
    
    # Address
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_text_color(0, 0, 0)
    address = property_data.get('address', 'Address not available')[:60]
    pdf.multi_cell(0, 9, address, align='C')
    pdf.ln(15)
    
    # DPE Badge - Larger and better
    dpe_colors = {
        'A': (34, 197, 94), 'B': (74, 222, 128), 'C': (163, 230, 53),
        'D': (250, 204, 21), 'E': (251, 146, 60), 'F': (249, 115, 22),
        'G': (239, 68, 68)
    }
    color = dpe_colors.get(dpe, (100, 100, 100))
    pdf.set_fill_color(color[0], color[1], color[2])
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 56)
    pdf.set_x(210/2 - 30)
    pdf.cell(60, 60, dpe, border=0, align='C', fill=True)
    pdf.ln(20)
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 5, 'ENERGY PERFORMANCE RATING', ln=True, align='C')
    pdf.ln(5)
    
    # Score circle simulation
    total_score = (energy_score + compliance_score + investment_score + market_score) // 4
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(34, 197, 94)
    pdf.cell(0, 6, f'ZAMI Score: {total_score}/100', ln=True, align='C')
    
    pdf.ln(20)
    
    # ============================================
    # KEY METRICS SECTION
    # ============================================
    pdf.section_title('Key Metrics')
    
    # 2x3 grid
    metrics = [
        ('Property Surface', f"{int(surface)} m2"),
        ('Current DPE', dpe),
        ('Renovation Cost', f"EUR {cost:,}"),
        ('Available Subsidy', f"EUR {subsidy:,}"),
        ('Net Investment', f"EUR {net:,}"),
        ('Expected ROI', f"+{roi:.1f}%"),
    ]
    
    y_start = pdf.get_y()
    for i, (label, value) in enumerate(metrics):
        x = 15 + (i % 3) * 60
        y = y_start + (i // 3) * 22
        pdf.set_xy(x, y)
        pdf.set_font('Helvetica', '', 7)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(55, 5, label, ln=False, align='C')
        pdf.set_xy(x, y + 6)
        pdf.set_font('Helvetica', 'B', 12)
        if i % 3 == 2:  # ROI in green
            pdf.set_text_color(34, 197, 94)
        else:
            pdf.set_text_color(0, 0, 0)
        pdf.cell(55, 7, value, ln=False, align='C')
    
    pdf.ln(55)
    
    # ============================================
    # VALUE PROJECTION
    # ============================================
    pdf.section_title('Value Projection')
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(80, 8, 'Current Property Value:', ln=False)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, f"EUR {current_val:,}", ln=True)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(80, 8, 'After Renovation:', ln=False)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(34, 197, 94)
    pdf.cell(0, 8, f"EUR {future_val:,}", ln=True)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(80, 8, 'Value Gain:', ln=False)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(34, 197, 94)
    pdf.cell(0, 8, f"+EUR {gain:,}", ln=True)
    
    pdf.ln(12)
    
    # Simple progress bar for gain percentage
    gain_percent = (gain / current_val) * 100
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, f'Expected appreciation: {gain_percent:.1f}%', ln=True)
    
    pdf.set_fill_color(220, 220, 220)
    pdf.rect(15, pdf.get_y(), 120, 6, 'F')
    pdf.set_fill_color(34, 197, 94)
    pdf.rect(15, pdf.get_y(), int(120 * gain_percent / 30), 6, 'F')
    pdf.ln(12)
    
    # ============================================
    # PAGE 2: SCORES
    # ============================================
    pdf.add_page()
    pdf.section_title('ZAMI Intelligence Scores')
    
    scores = [
        ('Energy Performance', energy_score),
        ('Compliance Status', compliance_score),
        ('Investment Potential', investment_score),
        ('Market Conditions', market_score),
    ]
    
    for name, score in scores:
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(80, 8, name, ln=False)
        pdf.set_font('Helvetica', 'B', 10)
        if score >= 70:
            pdf.set_text_color(34, 197, 94)
        elif score >= 50:
            pdf.set_text_color(245, 158, 11)
        else:
            pdf.set_text_color(239, 68, 68)
        pdf.cell(0, 8, f"{score}/100", ln=True)
        
        # Progress bar
        pdf.set_fill_color(220, 220, 220)
        pdf.rect(90, pdf.get_y() - 6, 80, 4, 'F')
        pdf.set_fill_color(34, 197, 94 if score >= 70 else (245, 158, 11 if score >= 50 else 239, 68, 68))
        pdf.rect(90, pdf.get_y() - 6, int(80 * score / 100), 4, 'F')
        pdf.ln(6)
    
    pdf.ln(5)
    
    # Overall Score
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, f'OVERALL ZAMI SCORE: {total_score}/100', ln=True, align='C')
    pdf.ln(8)
    
    # ============================================
    # RECOMMENDATIONS
    # ============================================
    pdf.section_title('Recommendations')
    
    if dpe in ['F', 'G']:
        recos = [
            '1. Complete energy audit by certified professional',
            '2. Apply for MaPrimeRenev subsidy immediately',
            '3. Prioritize wall and attic insulation',
            '4. Replace heating system with heat pump',
            '5. Contact certified RGE contractors for quotes',
        ]
    elif dpe == 'E':
        recos = [
            '1. Upgrade heating system to condensing boiler',
            '2. Replace single-glazed windows',
            '3. Improve attic insulation',
            '4. Install programmable thermostat',
        ]
    else:
        recos = [
            '1. Optimize heating system settings',
            '2. Consider solar panels installation',
            '3. Upgrade to energy-efficient appliances',
            '4. Install smart home energy monitoring',
        ]
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(50, 50, 50)
    for rec in recos:
        pdf.multi_cell(0, 6, rec, align='L')
        pdf.ln(2)
    
    pdf.ln(5)
    
    # Subsidy info
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, 'Subsidy Eligibility', ln=True, align='L')
    pdf.set_draw_color(34, 197, 94)
    pdf.line(10, pdf.get_y(), 55, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 6, f'Estimated MaPrimeRenev Subsidy: EUR {subsidy:,}', ln=True, align='L')
    pdf.ln(3)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, 'Apply through official France Renev platform', ln=True, align='L')
    
    # ============================================
    # PAGE 3: CONTACT
    # ============================================
    pdf.add_page()
    pdf.set_y(80)
    
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, 'Need Professional Help?', ln=True, align='C')
    pdf.ln(8)
    
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 7, 'Our certified experts can help you with:', ln=True, align='C')
    pdf.ln(8)
    
    services = [
        '- On-site technical audit and validation',
        '- Additional subsidies and financing options',
        '- Connection with trusted RGE-certified contractors',
        '- Complete subsidy application assistance',
        '- Project management and quality control',
    ]
    
    pdf.set_font('Helvetica', '', 10)
    for service in services:
        pdf.cell(0, 7, service, ln=True, align='C')
        pdf.ln(2)
    
    pdf.ln(20)
    
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(34, 197, 94)
    pdf.cell(0, 8, 'CONTACT US', ln=True, align='C')
    pdf.ln(5)
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 7, 'Email: experts@thezami.com', ln=True, align='C')
    pdf.cell(0, 7, 'Phone: +33 (0)1 23 45 67 89', ln=True, align='C')
    pdf.cell(0, 7, 'Web: thezami.com', ln=True, align='C')
    
    pdf.ln(15)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 5, 'This report is an AI-generated estimate. Final figures require on-site technical audit.', ln=True, align='C')
    
    # Return PDF as bytes
    output = pdf.output(dest='S')
    if isinstance(output, str):
        output = output.encode('latin-1', errors='replace')
    
    return output


make_report = generer_rapport