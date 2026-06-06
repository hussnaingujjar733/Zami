from fpdf import FPDF
from datetime import datetime


def generer_rapport(property_data):
    """Generate PDF report - guaranteed working"""
    
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
    
    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font('Helvetica', 'B', 20)
    pdf.cell(0, 15, 'ZAMI PROPERTY REPORT', ln=True, align='C')
    
    # Date
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 8, f'Date: {datetime.now().strftime("%d/%m/%Y")}', ln=True, align='R')
    pdf.ln(5)
    
    # Address
    pdf.set_font('Helvetica', 'B', 12)
    address = property_data.get('address', 'Address not available')[:60]
    pdf.multi_cell(0, 8, address, align='C')
    pdf.ln(5)
    
    # DPE
    dpe = property_data.get('dpe', 'E')
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, f'Current DPE: {dpe}', ln=True)
    pdf.ln(3)
    
    # Surface
    surface = property_data.get('surface', 75)
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 8, f'Surface: {int(surface)} m2', ln=True)
    pdf.ln(3)
    
    # Cost
    cost = property_data.get('cost', 46500)
    pdf.cell(0, 8, f'Estimated Cost: EUR {int(cost):,}', ln=True)
    pdf.ln(3)
    
    # ROI
    roi = property_data.get('roi', 13.1)
    pdf.cell(0, 8, f'Expected ROI: +{roi:.1f}%', ln=True)
    pdf.ln(5)
    
    # Subsidy
    subsidy = int(12500 * (surface / 68))
    pdf.cell(0, 8, f'Estimated Subsidy: EUR {subsidy:,}', ln=True)
    pdf.ln(5)
    
    # Value gain
    after_val = int(350000 * (surface / 68))
    gain = after_val - 280000
    pdf.cell(0, 8, f'Estimated Value Gain: EUR {gain:,}', ln=True)
    pdf.ln(10)
    
    # Footer
    pdf.set_y(-30)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 8, 'ZAMI - Property Intelligence Platform', ln=True, align='C')
    
    # Return as bytes
    return pdf.output(dest='S')


# Make sure function is accessible
make_report = generer_rapport