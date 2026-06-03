"""
utils_pdf.py — ZAMI Professional PDF Generator
Generates bank-grade, investment-ready PDF reports with:
- Logo, colors, charts
- Property details, DPE badge
- Financial analysis, ROI projections
- Renovation recommendations
"""

from fpdf import FPDF
from datetime import datetime
import io
import os
import base64

# Color definitions
COLORS = {
    'primary': (34, 197, 94),      # ZAMI Green
    'secondary': (59, 130, 246),   # Blue
    'danger': (239, 68, 68),       # Red
    'warning': (245, 158, 11),     # Orange
    'dark': (15, 23, 42),          # Dark blue
    'light': (241, 245, 249),      # Light gray
    'text': (51, 65, 85),          # Text color
    'text_light': (100, 116, 139)  # Light text
}

DPE_COLORS = {
    'A': (34, 197, 94),     # Green
    'B': (74, 222, 128),    # Light green
    'C': (163, 230, 53),    # Yellow-green
    'D': (250, 204, 21),    # Yellow
    'E': (251, 146, 60),    # Orange
    'F': (249, 115, 22),    # Dark orange
    'G': (239, 68, 68)      # Red
}


class ZAMIPDF(FPDF):
    """Custom PDF class with ZAMI branding"""
    
    def __init__(self, property_data, scenario_data=None):
        super().__init__()
        self.prop = property_data
        self.scenario = scenario_data
        self.WIDTH = 210
        self.HEIGHT = 297
        self.set_auto_page_break(auto=True, margin=25)
        
    def header(self):
        """Professional header with logo and branding"""
        # Background line
        self.set_draw_color(*COLORS['primary'])
        self.set_line_width(0.5)
        self.line(10, 25, self.WIDTH - 10, 25)
        
        # Brand name
        self.set_y(15)
        self.set_font('Helvetica', 'B', 20)
        self.set_text_color(*COLORS['primary'])
        self.cell(0, 8, 'ZAMI', ln=False, align='L')
        
        self.set_font('Helvetica', '', 9)
        self.set_text_color(*COLORS['text_light'])
        self.cell(0, 8, 'Property Intelligence Report', ln=True, align='R')
        
        self.ln(10)
        
    def footer(self):
        """Professional footer with timestamp and page number"""
        self.set_y(-20)
        self.set_font('Helvetica', 'I', 7)
        self.set_text_color(*COLORS['text_light'])
        self.cell(0, 5, f'Generated: {datetime.now().strftime("%d/%m/%Y %H:%M")}', align='L')
        self.cell(0, 5, f'Page {self.page_no()}', align='R')
        
    def section_title(self, title, icon='📊'):
        """Render a styled section title"""
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(*COLORS['primary'])
        self.cell(0, 10, f'{icon} {title}', ln=True)
        self.set_draw_color(*COLORS['primary'])
        self.line(10, self.get_y(), 50, self.get_y())
        self.ln(5)
        
    def dpe_badge(self, dpe_class, size=40):
        """Creates DPE badge with appropriate color"""
        color = DPE_COLORS.get(dpe_class.upper(), COLORS['warning'])
        self.set_fill_color(*color)
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', size)
        
        # Square badge
        self.rect(self.get_x(), self.get_y(), size, size, 'F')
        self.set_xy(self.get_x() + (size / 2) - 12, self.get_y() + (size / 2) - 10)
        self.cell(0, 0, dpe_class.upper())
        self.set_x(self.get_x() + size)
        
    def metric_card(self, label, value, unit='', width=85):
        """Creates a professional metric card"""
        # Card background
        self.set_fill_color(248, 250, 252)
        self.rect(self.get_x(), self.get_y(), width, 35, 'F')
        self.set_draw_color(*COLORS['text_light'])
        self.set_line_width(0.3)
        self.rect(self.get_x(), self.get_y(), width, 35)
        
        # Label
        self.set_font('Helvetica', '', 7)
        self.set_text_color(*COLORS['text_light'])
        self.set_xy(self.get_x() + 5, self.get_y() + 5)
        self.cell(0, 4, label)
        
        # Value
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(*COLORS['text'])
        self.set_xy(self.get_x() + 5, self.get_y() + 12)
        self.cell(0, 6, f'{value:,}{unit}')
        
        # Move cursor
        self.set_x(self.get_x() + width)
        
    def info_row(self, label, value, y=None):
        """Two-column info row"""
        if y:
            self.set_y(y)
        self.set_font('Helvetica', '', 10)
        self.set_text_color(*COLORS['text_light'])
        self.cell(70, 8, label, ln=False)
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*COLORS['text'])
        self.cell(0, 8, str(value), ln=True)
        self.ln(2)


def generate_professional_pdf(property_data, scenario, target_dpe, active_cost, net_cost, subsidy, roi):
    """
    Generates a professional, investment-grade PDF report.
    
    Args:
        property_data (dict): Property information (address, dpe, surface, etc.)
        scenario (str): Selected renovation scenario (Essential/Plus/Zero)
        target_dpe (str): Target DPE class after renovation
        active_cost (float): Total renovation cost
        net_cost (float): Cost after subsidies
        subsidy (float): Total subsidy amount
        roi (float): Expected ROI percentage
    
    Returns:
        bytes: PDF file as bytes ready for download
    """
    pdf = ZAMIPDF(property_data, scenario)
    pdf.add_page()
    
    # ============================================
    # PROPERTY INFO SECTION
    # ============================================
    pdf.section_title('Property Information', '🏠')
    
    # Address
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(*COLORS['text'])
    address = property_data.get('address', 'Address not available')
    pdf.multi_cell(0, 6, address, align='L')
    pdf.ln(8)
    
    # DPE Badge and metrics row
    start_y = pdf.get_y()
    pdf.set_x(15)
    pdf.dpe_badge(property_data.get('dpe', 'E'), 50)
    
    pdf.set_x(75)
    pdf.metric_card('Surface', int(property_data.get('surface', 0)), ' m²')
    pdf.set_x(75)
    pdf.metric_card('Current Value (est.)', int(property_data.get('current_value', 250000)), ' €')
    
    pdf.set_y(start_y + 45)
    pdf.ln(10)
    
    # Additional property details
    pdf.info_row('Building Type', property_data.get('type_batiment', 'Not specified'))
    pdf.info_row('Construction Year', property_data.get('annee_construction', 'Not specified') or 'Not specified')
    pdf.info_row('Heating System', property_data.get('energie_chauffage', 'Not specified') or 'Not specified')
    pdf.info_row('Energy Consumption', f"{property_data.get('conso_kwh', 'N/A')} kWh/an" if property_data.get('conso_kwh') else 'Not specified')
    pdf.info_row('CO₂ Emissions', f"{property_data.get('emission_ges', 'N/A')} kg CO₂/an" if property_data.get('emission_ges') else 'Not specified')
    
    pdf.ln(10)
    
    # ============================================
    # RENOVATION SCENARIO SECTION
    # ============================================
    pdf.section_title('Renovation Scenario', '🛠️')
    
    # Scenario highlight box
    pdf.set_fill_color(*COLORS['primary'])
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 12)
    scenario_box_height = 12
    pdf.rect(15, pdf.get_y(), 80, scenario_box_height, 'F')
    pdf.set_xy(20, pdf.get_y() + 3)
    pdf.cell(0, 5, f'Scenario: {scenario}', ln=False)
    pdf.set_y(pdf.get_y() + scenario_box_height)
    pdf.ln(5)
    
    # Target DPE
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(*COLORS['text'])
    pdf.cell(70, 8, 'Target DPE After Renovation:', ln=False)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(*DPE_COLORS.get(target_dpe.upper(), COLORS['primary']))
    pdf.cell(0, 8, target_dpe.upper(), ln=True)
    pdf.ln(5)
    
    # Financial metrics
    pdf.info_row('Total Renovation Cost', f'€{active_cost:,.0f}')
    pdf.info_row('MaPrimeRénov\' Subsidy', f'€{subsidy:,.0f}')
    pdf.info_row('Net Investment', f'€{net_cost:,.0f}')
    pdf.info_row('Expected ROI', f'+{roi}%')
    
    pdf.ln(10)
    
    # ============================================
    # FINANCIAL SUMMARY TABLE
    # ============================================
    pdf.section_title('Financial Summary', '💰')
    
    # Table header
    pdf.set_fill_color(*COLORS['primary'])
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(100, 10, 'Item', border=1, fill=True, ln=False)
    pdf.cell(75, 10, 'Amount (€)', border=1, fill=True, ln=True)
    
    # Table rows
    pdf.set_fill_color(255, 255, 255)
    pdf.set_text_color(*COLORS['text'])
    pdf.set_font('Helvetica', '', 10)
    
    rows = [
        ('Renovation Cost', f'{active_cost:,.0f}'),
        ('MaPrimeRénov\' Subsidy', f'-{subsidy:,.0f}'),
        ('Regional Aids', '0'),  # Placeholder for future
        ('', ''),
        ('Net Investment', f'{net_cost:,.0f}')
    ]
    
    for i, (label, value) in enumerate(rows):
        if label == '':
            pdf.cell(100, 5, '', border=0, ln=True)
            continue
            
        pdf.cell(100, 10, label, border=1)
        pdf.cell(75, 10, value, border=1, ln=True)
        
    pdf.ln(8)
    
    # Value increase calculation
    current_value = property_data.get('current_value', 250000)
    value_increase = int(current_value * (roi / 100))
    new_value = current_value + value_increase
    
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 8, f'Expected Value After Renovation: €{new_value:,.0f}', ln=True)
    pdf.set_text_color(*COLORS['primary'])
    pdf.cell(0, 8, f'Value Increase: +€{value_increase:,.0f} (+{roi}%)', ln=True)
    
    pdf.ln(15)
    
    # ============================================
    # RECOMMENDATIONS SECTION
    # ============================================
    pdf.section_title('Smart Recommendations', '🔧')
    
    recommendations = get_recommendations(property_data.get('dpe', 'E'), target_dpe)
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(*COLORS['text'])
    
    for i, rec in enumerate(recommendations, 1):
        pdf.multi_cell(0, 6, f'{i}. {rec}', align='L')
        pdf.ln(2)
    
    pdf.ln(10)
    
    # ============================================
    # NEXT STEPS SECTION
    # ============================================
    pdf.section_title('Next Steps', '✅')
    
    next_steps = [
        '1. Download this report and share with certified RGE contractors',
        '2. Contact our team for a personalized consultation',
        '3. Apply for MaPrimeRénov\' subsidy through official channels',
        '4. Start your renovation project with government-backed financing',
        '5. Track your project progress on ZAMI dashboard'
    ]
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(*COLORS['text'])
    for step in next_steps:
        pdf.multi_cell(0, 6, step, align='L')
        pdf.ln(2)
    
    pdf.ln(10)
    
    # ============================================
    # DISCLAIMER
    # ============================================
    pdf.set_font('Helvetica', 'I', 7)
    pdf.set_text_color(*COLORS['text_light'])
    disclaimer = "Disclaimer: This report is an estimate based on available data and should not be considered as professional financial or legal advice. Please consult certified professionals for final decisions."
    pdf.multi_cell(0, 4, disclaimer, align='L')
    
    return pdf.output(dest='S').encode('latin1')


def get_recommendations(current_dpe, target_dpe):
    """Returns renovation recommendations based on current and target DPE"""
    
    base_recs = [
        "Insulate attic and roof (reduces heat loss by up to 30%)",
        "Replace old windows with double/triple glazing",
        "Install programmable thermostat for better energy management"
    ]
    
    if current_dpe in ['F', 'G']:
        return [
            "🔴 URGENT: Install wall insulation (accounts for 25% of heat loss)",
            "🔴 Replace heating system with heat pump or biomass boiler",
            "🟡 Upgrade to energy-efficient appliances (Class A+++)",
            "🟡 Install solar panels for water heating",
        ] + base_recs
    elif current_dpe == 'E':
        return [
            "🟡 Upgrade heating system to condensing boiler",
            "🟡 Improve wall insulation where possible",
            "🟡 Install individual room temperature controls",
        ] + base_recs
    elif current_dpe in ['C', 'D']:
        return [
            "✅ Optimize existing heating system settings",
            "✅ Add smart home energy monitoring system",
            "✅ Consider solar panel installation for electricity generation",
        ] + base_recs[:2]
    else:
        return [
            "✅ Maintain existing equipment regularly",
            "✅ Consider small improvements: LED lighting, weatherstripping",
            "✅ Monitor energy consumption to identify waste"
        ]