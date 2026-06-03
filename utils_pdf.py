"""
utils_pdf.py — ZAMI PDF Generator
Fixed: properly returns bytes, not bytearray
"""

from fpdf import FPDF
from datetime import datetime


def generate_professional_pdf(property_data, scenario, target_dpe, active_cost, net_cost, subsidy, roi):
    """
    Generate PDF report - returns proper bytes format
    """
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font('Helvetica', 'B', 20)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 15, 'ZAMI PROPERTY REPORT', ln=True, align='C')
    
    # Date
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 8, f'Date: {datetime.now().strftime("%d/%m/%Y")}', ln=True, align='R')
    pdf.ln(5)
    
    # Address
    address = property_data.get('address', 'Address not available')
    pdf.set_font('Helvetica', 'B', 12)
    pdf.multi_cell(0, 8, str(address))
    pdf.ln(5)
    
    # Property Details
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, 'Property Details', ln=True)
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 8, f"Current DPE: {property_data.get('dpe', 'N/A')}", ln=True)
    pdf.cell(0, 8, f"Target DPE: {target_dpe}", ln=True)
    pdf.cell(0, 8, f"Surface: {int(property_data.get('surface', 0))} m2", ln=True)
    pdf.ln(5)
    
    # Financial Summary
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, 'Financial Summary', ln=True)
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 8, f"Renovation Cost: EUR {active_cost:,.0f}", ln=True)
    pdf.cell(0, 8, f"Subsidy: EUR {subsidy:,.0f}", ln=True)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, f"Net Investment: EUR {net_cost:,.0f}", ln=True)
    pdf.cell(0, 8, f"Expected ROI: +{roi}%", ln=True)
    pdf.ln(5)
    
    # Scenario
    pdf.set_font('Helvetica', 'I', 10)
    pdf.cell(0, 8, f"Selected Scenario: {scenario}", ln=True)
    pdf.ln(10)
    
    # Footer
    pdf.set_y(-30)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 8, 'ZAMI - Property Intelligence Platform', ln=True, align='C')
    pdf.cell(0, 8, 'This document is an estimate only.', ln=True, align='C')
    
    # CRITICAL FIX: Convert bytearray to bytes
    output = pdf.output(dest='S')
    
    # If it's bytearray, convert to bytes
    if isinstance(output, bytearray):
        output = bytes(output)
    
    return output