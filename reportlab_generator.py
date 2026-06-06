from fpdf import FPDF
from datetime import datetime

def generer_rapport(data):
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font('Helvetica', 'B', 20)
    pdf.cell(0, 15, 'ZAMI REPORT', ln=True, align='C')
    
    # Date
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 8, datetime.now().strftime("%d/%m/%Y"), ln=True, align='R')
    pdf.ln(5)
    
    # Address
    pdf.set_font('Helvetica', 'B', 11)
    addr = data.get('address', 'Address')[:50]
    pdf.multi_cell(0, 7, addr)
    pdf.ln(5)
    
    # DPE
    dpe = data.get('dpe', 'E')
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, f'DPE: {dpe}', ln=True)
    pdf.ln(3)
    
    # Surface
    surf = data.get('surface', 75)
    pdf.cell(0, 8, f'Surface: {int(surf)} m2', ln=True)
    pdf.ln(3)
    
    # Cost
    cost = data.get('cost', 46500)
    pdf.cell(0, 8, f'Cost: EUR {int(cost):,}', ln=True)
    pdf.ln(3)
    
    # ROI
    roi = data.get('roi', 13.1)
    pdf.cell(0, 8, f'ROI: +{roi:.1f}%', ln=True)
    pdf.ln(5)
    
    # Subsidy
    subsidy = int(12500 * (surf / 68))
    pdf.cell(0, 8, f'Subsidy: EUR {subsidy:,}', ln=True)
    pdf.ln(5)
    
    # Value gain
    after_val = int(350000 * (surf / 68))
    gain = after_val - 280000
    pdf.cell(0, 8, f'Value Gain: EUR {gain:,}', ln=True)
    pdf.ln(15)
    
    # Footer
    pdf.set_y(-25)
    pdf.set_font('Helvetica', 'I', 7)
    pdf.cell(0, 8, 'ZAMI - Property Intelligence', ln=True, align='C')
    
    return pdf.output(dest='S')