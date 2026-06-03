"""
utils_pdf.py — ZAMI Simple PDF Generator
Working version — no fancy features, just works
"""

from fpdf import FPDF
from datetime import datetime


def generate_professional_pdf(property_data, scenario, target_dpe, active_cost, net_cost, subsidy, roi):
    """
    Generate a simple working PDF report
    """
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font('Helvetica', 'B', 24)
    pdf.set_text_color(34, 197, 94)
    pdf.cell(0, 20, 'ZAMI PROPERTY REPORT', ln=True, align='C')
    pdf.ln(5)
    
    # Date
    pdf.set_font('Helvetica', 'I', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, f'Generated: {datetime.now().strftime("%d/%m/%Y %H:%M")}', ln=True, align='R')
    pdf.ln(5)
    
    # Address
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(0, 0, 0)
    address = property_data.get('address', 'Address not available')
    pdf.multi_cell(0, 8, address, align='L')
    pdf.ln(5)
    
    # DPE
    dpe = property_data.get('dpe', 'E')
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, f'Current DPE: {dpe}', ln=True)
    pdf.cell(0, 10, f'Target DPE: {target_dpe}', ln=True)
    pdf.ln(5)
    
    # Surface
    surface = property_data.get('surface', 0)
    pdf.cell(0, 10, f'Surface: {int(surface)} m2', ln=True)
    pdf.ln(5)
    
    # Costs
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, 'FINANCIAL SUMMARY', ln=True)
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 10, f'Renovation Cost: EUR {active_cost:,.0f}', ln=True)
    pdf.cell(0, 10, f'Subsidy (MaPrimeRenov): EUR {subsidy:,.0f}', ln=True)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 10, f'Net Investment: EUR {net_cost:,.0f}', ln=True)
    pdf.cell(0, 10, f'Expected ROI: +{roi}%', ln=True)
    pdf.ln(5)
    
    # Scenario
    pdf.set_font('Helvetica', 'I', 10)
    pdf.cell(0, 10, f'Scenario: {scenario}', ln=True)
    pdf.ln(10)
    
    # Footer
    pdf.set_y(-30)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 10, 'ZAMI - Property Intelligence Platform', ln=True, align='C')
    pdf.cell(0, 10, 'This is an estimate. Consult certified professionals.', ln=True, align='C')
    
    return pdf.output(dest='S')