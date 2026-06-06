"""
reportlab_generator.py — ZAMI Simple Working PDF
"""

from fpdf import FPDF
from datetime import datetime


def generer_rapport(property_data):
    """Generate simple working PDF report"""
    
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
    
    # Calculate scores
    dpe_scores = {'A': 95, 'B': 85, 'C': 70, 'D': 55, 'E': 40, 'F': 25, 'G': 10}
    total_score = dpe_scores.get(dpe, 40)
    
    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    
    # ============================================
    # TITLE SECTION
    # ============================================
    pdf.set_font('Helvetica', 'B', 24)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 15, 'ZAMI PROPERTY REPORT', ln=True, align='C')
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, datetime.now().strftime("%d/%m/%Y"), ln=True, align='R')
    pdf.ln(5)
    
    # Address
    pdf.set_font('Helvetica', 'B', 12)
    address = property_data.get('address', 'Address not available')[:60]
    pdf.multi_cell(0, 7, address, align='C')
    pdf.ln(10)
    
    # ============================================
    # DPE BADGE
    # ============================================
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
    pdf.ln(15)
    
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, 'ENERGY PERFORMANCE RATING', ln=True, align='C')
    pdf.ln(15)
    
    # ============================================
    # SCORE
    # ============================================
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(34, 197, 94)
    pdf.cell(0, 8, f'ZAMI SCORE: {total_score}/100', ln=True, align='C')
    pdf.ln(15)
    
    # ============================================
    # KEY METRICS
    # ============================================
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, 'KEY METRICS', ln=True)
    pdf.ln(5)
    
    # Metrics in simple list
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(80, 80, 80)
    
    pdf.cell(60, 8, 'Surface Area:', ln=False)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, f"{int(surface)} m2", ln=True)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(60, 8, 'Current DPE:', ln=False)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, dpe, ln=True)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(60, 8, 'Renovation Cost:', ln=False)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, f"EUR {cost:,}", ln=True)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(60, 8, 'Available Subsidy:', ln=False)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, f"EUR {subsidy:,}", ln=True)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(60, 8, 'Net Investment:', ln=False)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, f"EUR {net:,}", ln=True)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(60, 8, 'Expected ROI:', ln=False)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(34, 197, 94)
    pdf.cell(0, 8, f"+{roi:.1f}%", ln=True)
    
    pdf.ln(10)
    
    # ============================================
    # VALUE PROJECTION
    # ============================================
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, 'VALUE PROJECTION', ln=True)
    pdf.ln(5)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(70, 8, 'Current Property Value:', ln=False)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, f"EUR {current_val:,}", ln=True)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(70, 8, 'After Renovation:', ln=False)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(34, 197, 94)
    pdf.cell(0, 8, f"EUR {future_val:,}", ln=True)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(70, 8, 'Total Value Gain:', ln=False)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(34, 197, 94)
    pdf.cell(0, 8, f"+EUR {gain:,}", ln=True)
    
    pdf.ln(10)
    
    # ============================================
    # RECOMMENDATIONS
    # ============================================
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, 'RECOMMENDATIONS', ln=True)
    pdf.ln(5)
    
    if dpe in ['F', 'G']:
        recos = [
            '1. Complete energy audit by certified professional',
            '2. Apply for MaPrimeRenev subsidy immediately',
            '3. Prioritize wall and attic insulation',
            '4. Replace heating system with heat pump',
            '5. Contact certified RGE contractors',
        ]
    elif dpe == 'E':
        recos = [
            '1. Upgrade heating system',
            '2. Replace single-glazed windows',
            '3. Improve attic insulation',
            '4. Install programmable thermostat',
        ]
    else:
        recos = [
            '1. Optimize heating system settings',
            '2. Consider solar panels',
            '3. Upgrade to energy-efficient appliances',
            '4. Install smart home monitoring',
        ]
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(50, 50, 50)
    for rec in recos:
        pdf.multi_cell(0, 7, rec, align='L')
        pdf.ln(2)
    
    pdf.ln(10)
    
    # ============================================
    # CONTACT
    # ============================================
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, 'CONTACT US', ln=True)
    pdf.ln(5)
    
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(59, 130, 246)
    pdf.cell(0, 8, 'Email: experts@thezami.com', ln=True, align='C')
    pdf.cell(0, 8, 'Phone: +33 (0)1 23 45 67 89', ln=True, align='C')
    pdf.cell(0, 8, 'Web: thezami.com', ln=True, align='C')
    
    pdf.ln(15)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 5, 'This report is an AI-generated estimate. Consult certified professionals.', ln=True, align='C')
    
    # Footer on all pages
    pdf.set_y(-20)
    pdf.set_font('Helvetica', 'I', 7)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 5, 'ZAMI - Property Intelligence Platform', ln=True, align='C')
    
    # Return PDF bytes
    output = pdf.output(dest='S')
    if isinstance(output, str):
        output = output.encode('latin-1', errors='replace')
    
    return output


make_report = generer_rapport