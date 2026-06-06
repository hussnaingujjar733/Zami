"""
reportlab_generator.py — ZAMI Corporate Report PDF
Fixed: No special characters, euro symbol replaced with EUR
"""

from fpdf import FPDF
from datetime import datetime


class CorporatePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=25)
        self.set_compression(True)
    
    def header(self):
        self.set_draw_color(34, 197, 94)
        self.set_line_width(1.5)
        self.line(10, 15, 200, 15)
        self.set_line_width(0.5)
        self.line(10, 18, 200, 18)
        
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(34, 197, 94)
        self.set_xy(15, 8)
        self.cell(0, 6, 'ZAMI', ln=False)
        
        self.set_font('Helvetica', '', 8)
        self.set_text_color(128, 128, 128)
        self.set_xy(170, 9)
        self.cell(0, 5, f'Page {self.page_no()}', ln=False)
        
        self.ln(25)
    
    def footer(self):
        self.set_y(-20)
        self.set_font('Helvetica', 'I', 7)
        self.set_text_color(128, 128, 128)
        self.cell(0, 4, 'ZAMI - Property Intelligence Platform | Confidential', ln=True, align='C')
        self.cell(0, 4, 'This report is an AI-generated estimate. Consult certified professionals.', ln=True, align='C')
    
    def section_title(self, title, color=(34, 197, 94)):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, title, ln=True)
        self.set_draw_color(color[0], color[1], color[2])
        self.set_line_width(1)
        self.line(10, self.get_y(), 40, self.get_y())
        self.ln(6)
    
    def corporate_table(self, headers, data, col_widths):
        self.set_fill_color(34, 197, 94)
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 9)
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, header, border=1, align='C', fill=True)
        self.ln()
        
        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', '', 9)
        fill = False
        for row in data:
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 7, str(cell), border=1, align='L', fill=fill)
            self.ln()
            fill = not fill
    
    def metric_card(self, label, value, subtext="", highlight=False):
        self.set_fill_color(248, 250, 252)
        self.set_draw_color(226, 232, 240)
        self.rect(self.get_x(), self.get_y(), 55, 35, 'FD')
        
        self.set_font('Helvetica', '', 7)
        self.set_text_color(100, 116, 139)
        self.set_xy(self.get_x() + 5, self.get_y() + 4)
        self.cell(0, 4, label)
        
        self.set_font('Helvetica', 'B', 14)
        if highlight:
            self.set_text_color(34, 197, 94)
        else:
            self.set_text_color(0, 0, 0)
        self.set_xy(self.get_x() + 5, self.get_y() + 12)
        self.cell(0, 6, value)
        
        if subtext:
            self.set_font('Helvetica', '', 6)
            self.set_text_color(128, 128, 128)
            self.set_xy(self.get_x() + 5, self.get_y() + 22)
            self.cell(0, 4, subtext)
        
        self.set_x(self.get_x() + 58)


def generer_rapport(property_data):
    """Generate corporate-style professional PDF report"""
    
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
    total_score = (energy_score + compliance_score + investment_score + market_score) // 4
    
    pdf = CorporatePDF()
    
    # ============================================
    # COVER PAGE
    # ============================================
    pdf.add_page()
    
    pdf.set_y(60)
    pdf.set_font('Helvetica', 'B', 42)
    pdf.set_text_color(34, 197, 94)
    pdf.cell(0, 20, 'ZAMI', ln=True, align='C')
    
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 8, 'PROPERTY INTELLIGENCE REPORT', ln=True, align='C')
    pdf.ln(15)
    
    # Address
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(0, 0, 0)
    address = property_data.get('address', 'Property Address')[:60]
    pdf.multi_cell(0, 8, address, align='C')
    pdf.ln(15)
    
    # DPE Badge
    dpe_colors = {
        'A': (34, 197, 94), 'B': (74, 222, 128), 'C': (163, 230, 53),
        'D': (250, 204, 21), 'E': (251, 146, 60), 'F': (249, 115, 22),
        'G': (239, 68, 68)
    }
    color = dpe_colors.get(dpe, (100, 100, 100))
    pdf.set_fill_color(color[0], color[1], color[2])
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 52)
    pdf.set_x(210/2 - 30)
    pdf.cell(60, 60, dpe, border=0, align='C', fill=True)
    pdf.ln(20)
    
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, f'ZAMI OPPORTUNITY SCORE: {total_score}/100', ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 5, datetime.now().strftime("%d %B %Y"), ln=True, align='C')
    
    # ============================================
    # EXECUTIVE SUMMARY
    # ============================================
    pdf.add_page()
    pdf.section_title('Executive Summary')
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(71, 85, 105)
    pdf.multi_cell(0, 6, 'This report provides a comprehensive analysis of the property\'s energy renovation potential, including financial projections, subsidy eligibility, and strategic recommendations.', align='L')
    pdf.ln(15)
    
    # KPI Cards
    start_x = pdf.get_x()
    start_y = pdf.get_y()
    
    metrics = [
        ('Current Value', f'EUR {current_val:,}', 'Pre-renovation'),
        ('Renovation Cost', f'EUR {cost:,}', 'Estimated investment'),
        ('Subsidy', f'EUR {subsidy:,}', 'MaPrimeRenev'),
        ('Future Value', f'EUR {future_val:,}', 'Post-renovation'),
        ('Net Investment', f'EUR {net:,}', 'After subsidies'),
        ('ROI', f'+{roi:.1f}%', 'Expected return'),
    ]
    
    for i, (label, value, sub) in enumerate(metrics):
        x = 15 + (i % 3) * 60
        y = start_y + (i // 3) * 40
        pdf.set_xy(x, y)
        pdf.metric_card(label, value, sub, highlight=(i == 5))
    
    pdf.ln(85)
    
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(34, 197, 94)
    pdf.cell(0, 8, f'Estimated Net Gain After Renovation: +EUR {gain:,}', ln=True, align='C')
    
    # ============================================
    # PROPERTY INTELLIGENCE
    # ============================================
    pdf.add_page()
    pdf.section_title('Property Intelligence')
    
    headers = ['Parameter', 'Value', 'Assessment']
    data = [
        ['Address', property_data.get('address', 'N/A')[:50], 'Verified'],
        ['Surface Area', f'{int(surface)} m2', 'Standard'],
        ['Current DPE Rating', dpe, 'Needs Improvement' if dpe in ['F','G'] else 'Moderate' if dpe in ['D','E'] else 'Good'],
        ['Construction Year', 'Pre-1975' if dpe in ['F','G'] else '1980-2000', 'Typical for area'],
        ['Energy Consumption', 'Estimated 250-350 kWh/m2/year', 'High' if dpe in ['F','G'] else 'Moderate'],
    ]
    pdf.corporate_table(headers, data, [80, 55, 55])
    pdf.ln(10)
    
    # ============================================
    # ZAMI INTELLIGENCE SCORES
    # ============================================
    pdf.section_title('ZAMI Intelligence Scores')
    
    score_data = [
        ['Energy Performance', f'{energy_score}/100', 'Based on DPE rating', 'Critical' if energy_score < 40 else 'Standard' if energy_score < 70 else 'Good'],
        ['Compliance Status', f'{compliance_score}/100', '2025-2028 regulations', 'Attention Required' if compliance_score < 70 else 'Compliant'],
        ['Investment Potential', f'{investment_score}/100', 'Based on ROI projection', 'High' if investment_score >= 70 else 'Medium'],
        ['Market Conditions', f'{market_score}/100', 'Location-based assessment', 'Favorable' if market_score >= 70 else 'Standard'],
    ]
    pdf.corporate_table(['Score Category', 'Score', 'Basis', 'Outlook'], score_data, [50, 40, 60, 50])
    pdf.ln(10)
    
    # Overall score with visual bar
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, f'OVERALL ZAMI SCORE: {total_score}/100', ln=True, align='C')
    pdf.set_fill_color(226, 232, 240)
    pdf.rect(30, pdf.get_y(), 150, 8, 'F')
    pdf.set_fill_color(34, 197, 94)
    pdf.rect(30, pdf.get_y(), 150 * total_score / 100, 8, 'F')
    pdf.ln(15)
    
    if total_score >= 70:
        interpretation = 'Strong investment opportunity with excellent renovation potential.'
    elif total_score >= 50:
        interpretation = 'Good potential. Strategic renovation can unlock significant value.'
    else:
        interpretation = 'Attention required. Immediate renovation recommended to capture value.'
    
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 6, interpretation, ln=True, align='C')
    
    # ============================================
    # FINANCIAL ANALYSIS
    # ============================================
    pdf.add_page()
    pdf.section_title('Financial Analysis')
    
    headers = ['Component', 'Amount (EUR)', 'Impact']
    financial_data = [
        ['Current Property Value', f'{current_val:,}', 'Baseline'],
        ['Renovation Investment', f'-{cost:,}', 'Total project cost'],
        ['Government Subsidies', f'+{subsidy:,}', 'MaPrimeRenev'],
        ['Net Investment', f'{net:,}', 'Out-of-pocket cost'],
        ['Value Appreciation', f'+{future_val - current_val:,}', 'Post-renovation uplift'],
        ['Future Property Value', f'{future_val:,}', 'Expected market value'],
        ['Net Gain', f'+{gain:,}', 'Total return on investment'],
    ]
    pdf.corporate_table(headers, financial_data, [70, 60, 60])
    pdf.ln(10)
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, 'ROI Projection vs Market Average', ln=True)
    
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 5, f'Your Property ROI: +{roi:.1f}%', ln=True)
    pdf.set_fill_color(34, 197, 94)
    pdf.rect(15, pdf.get_y(), min(180, 180 * roi / 25), 6, 'F')
    pdf.ln(8)
    
    pdf.cell(0, 5, f'Market Average ROI: +12.0%', ln=True)
    pdf.set_fill_color(148, 163, 184)
    pdf.rect(15, pdf.get_y(), 180 * 12 / 25, 6, 'F')
    pdf.ln(12)
    
    # ============================================
    # RENOVATION ROADMAP
    # ============================================
    pdf.add_page()
    pdf.section_title('Renovation Roadmap')
    
    if dpe in ['F', 'G']:
        roadmap = [
            ['1', 'Energy Audit', 'Week 1', 'EUR 500-1,000', 'Mandatory first step'],
            ['2', 'Wall Insulation', 'Week 2-4', 'EUR 12,000-18,000', 'Highest ROI (25-30%)'],
            ['3', 'Attic Insulation', 'Week 4-5', 'EUR 8,000-12,000', 'Second priority (20-25%)'],
            ['4', 'Heating System', 'Week 6-8', 'EUR 10,000-15,000', 'Major energy saving (30-35%)'],
            ['5', 'Final Audit', 'Week 9', 'EUR 500-1,000', 'Validate DPE improvement'],
        ]
    elif dpe == 'E':
        roadmap = [
            ['1', 'Heating Upgrade', 'Week 1-3', 'EUR 10,000-15,000', 'Primary energy saving'],
            ['2', 'Window Replacement', 'Week 3-5', 'EUR 8,000-12,000', 'Secondary priority'],
            ['3', 'Ventilation', 'Week 5-6', 'EUR 4,000-7,000', 'Air quality improvement'],
        ]
    else:
        roadmap = [
            ['1', 'Heating Optimization', 'Week 1', 'EUR 500-2,000', 'Quick win'],
            ['2', 'Window Upgrade', 'Week 2-3', 'EUR 6,000-10,000', 'Moderate ROI'],
            ['3', 'Solar Assessment', 'Week 3-4', 'EUR 500', 'Future planning'],
        ]
    
    pdf.corporate_table(['Priority', 'Action', 'Timeline', 'Cost Range', 'Impact'], roadmap, [15, 55, 30, 40, 40])
    
    # ============================================
    # RISK ASSESSMENT
    # ============================================
    pdf.add_page()
    pdf.section_title('Risk & Compliance Assessment')
    
    risk_data = [
        ['Rental Ban Risk (2025)', 'High' if dpe in ['F','G'] else 'Low', 'Action Required' if dpe in ['F','G'] else 'Compliant'],
        ['Climate Compliance', 'Medium' if dpe in ['E','F','G'] else 'Low', 'Monitor' if dpe in ['D','E'] else 'Compliant'],
        ['Energy Cost Exposure', 'High' if dpe in ['F','G'] else 'Medium', 'Reducible via renovation'],
        ['Asset Depreciation', 'High' if dpe in ['F','G'] else 'Low', 'Immediate action needed' if dpe in ['F','G'] else 'Stable'],
    ]
    pdf.corporate_table(['Risk Factor', 'Severity', 'Mitigation'], risk_data, [70, 50, 70])
    pdf.ln(10)
    
    if dpe in ['F', 'G']:
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(239, 68, 68)
        pdf.cell(0, 6, 'URGENT: Property faces rental restrictions starting 2025.', ln=True)
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 6, 'Immediate renovation is recommended to maintain asset value and rental income potential.')
    
    # ============================================
    # APPENDIX & CONTACT
    # ============================================
    pdf.add_page()
    pdf.section_title('Next Steps & Contact')
    
    next_steps = [
        '1. Schedule an on-site energy audit with a certified professional',
        '2. Submit MaPrimeRenev application (estimated timeline: 4-6 weeks)',
        '3. Obtain at least 3 quotes from RGE-certified contractors',
        '4. Review financing options (Eco-PTZ, bank loans, local grants)',
        '5. Plan renovation work in priority order as outlined above',
    ]
    
    pdf.set_font('Helvetica', '', 10)
    for step in next_steps:
        pdf.multi_cell(0, 7, step, align='L')
        pdf.ln(2)
    
    pdf.ln(15)
    
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(34, 197, 94)
    pdf.cell(0, 8, 'Need Expert Assistance?', ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 7, 'Email: experts@thezami.com', ln=True, align='C')
    pdf.cell(0, 7, 'Phone: +33 (0)1 23 45 67 89', ln=True, align='C')
    pdf.cell(0, 7, 'Web: thezami.com', ln=True, align='C')
    
    # Return PDF bytes
    output = pdf.output(dest='S')
    if isinstance(output, str):
        output = output.encode('latin-1', errors='replace')
    
    return output


make_report = generer_rapport