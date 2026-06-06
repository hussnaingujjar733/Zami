"""
reportlab_generator.py — ZAMI Simple PDF
"""

from fpdf import FPDF
from datetime import datetime


def generer_rapport(property_data):
    """Generate PDF report"""
    
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font('Helvetica', 'B', 24)
    pdf.cell(0, 15, 'ZAMI PROPERTY REPORT', ln=True, align='C')
    
    # Date
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 8, f'Date: {datetime.now().strftime("%d/%m/%Y")}', ln=True, align='R')
    pdf.ln(5)
    
    # Address
    pdf.set_font('Helvetica', 'B', 12)
    address = property_data.get('address', 'Address')[:60]
    pdf.multi_cell(0, 8, address, align='C')
    pdf.ln(8)
    
    # DPE
    dpe = property_data.get('dpe', 'E')
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, f'Current DPE: {dpe}', ln=True, align='C')
    pdf.ln(5)
    
    # Surface
    surface = property_data.get('surface', 75)
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 8, f'Surface: {int(surface)} m2', ln=True, align='C')
    pdf.ln(3)
    
    # Cost
    cost = property_data.get('cost', 46500)
    pdf.cell(0, 8, f'Estimated Cost: EUR {int(cost):,}', ln=True, align='C')
    pdf.ln(3)
    
    # ROI
    roi = property_data.get('roi', 13.1)
    pdf.cell(0, 8, f'Expected ROI: +{roi:.1f}%', ln=True, align='C')
    pdf.ln(8)
    
    # Subsidy
    surface_val = surface
    subsidy = int(12500 * (surface_val / 68))
    pdf.cell(0, 8, f'Estimated Subsidy: EUR {subsidy:,}', ln=True, align='C')
    pdf.ln(8)
    
    # Value gain
    current_val = 280000
    after_val = int(350000 * (surface_val / 68))
    gain = after_val - current_val
    pdf.cell(0, 8, f'Estimated Value Gain: EUR {gain:,}', ln=True, align='C')
    pdf.ln(15)
    
    # Footer
    pdf.set_y(-30)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 8, 'ZAMI - Property Intelligence Platform', ln=True, align='C')
    
    return pdf.output(dest='S')


def make_report(data):
    return generer_rapport(data)