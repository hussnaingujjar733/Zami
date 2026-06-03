"""
utils_pdf.py — ZAMI Professional PDF Generator
Uses only standard FPDF fonts — no external font files needed
"""

from fpdf import FPDF
from datetime import datetime
import re

# Color definitions
COLORS = {
    'primary': (34, 197, 94),
    'secondary': (59, 130, 246),
    'danger': (239, 68, 68),
    'warning': (245, 158, 11),
    'dark': (15, 23, 42),
    'light': (241, 245, 249),
    'text': (51, 65, 85),
    'text_light': (100, 116, 139)
}

DPE_COLORS = {
    'A': (34, 197, 94),
    'B': (74, 222, 128),
    'C': (163, 230, 53),
    'D': (250, 204, 21),
    'E': (251, 146, 60),
    'F': (249, 115, 22),
    'G': (239, 68, 68)
}


class ZAMIPDF(FPDF):
    """Custom PDF class with ZAMI branding — uses standard fonts only"""
    
    def __init__(self, property_data, scenario_data=None):
        super().__init__()
        self.prop = property_data
        self.scenario = scenario_data
        self.WIDTH = 210
        self.HEIGHT = 297
        self.set_auto_page_break(auto=True, margin=25)
        
    def header(self):
        """Professional header with branding"""
        self.set_font('Helvetica', 'B', 20)
        self.set_text_color(*COLORS['primary'])
        self.cell(0, 8, 'ZAMI', ln=False, align='L')
        
        self.set_font('Helvetica', '', 9)
        self.set_text_color(*COLORS['text_light'])
        self.cell(0, 8, 'Property Intelligence Report', ln=True, align='R')
        
        self.set_draw_color(*COLORS['primary'])
        self.set_line_width(0.5)
        self.line(10, 25, self.WIDTH - 10, 25)
        self.ln(10)
        
    def footer(self):
        """Professional footer with timestamp and page number"""
        self.set_y(-20)
        self.set_font('Helvetica', 'I', 7)
        self.set_text_color(*COLORS['text_light'])
        self.cell(0, 5, f'Generated: {datetime.now().strftime("%d/%m/%Y %H:%M")}', align='L')
        self.cell(0, 5, f'Page {self.page_no()}', align='R')
        
    def section_title(self, title):
        """Render a styled section title"""
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(*COLORS['primary'])
        self.cell(0, 10, self.clean_text(title), ln=True)
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
        self.set_fill_color(248, 250, 252)
        self.rect(self.get_x(), self.get_y(), width, 35, 'F')
        self.set_draw_color(*COLORS['text_light'])
        self.set_line_width(0.3)
        self.rect(self.get_x(), self.get_y(), width, 35)
        
        self.set_font('Helvetica', '', 7)
        self.set_text_color(*COLORS['text_light'])
        self.set_xy(self.get_x() + 5, self.get_y() + 5)
        self.cell(0, 4, self.clean_text(label))
        
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(*COLORS['text'])
        self.set_xy(self.get_x() + 5, self.get_y() + 12)
        self.cell(0, 6, f'{value:,}{unit}')
        
        self.set_x(self.get_x() + width)
        
    def info_row(self, label, value, y=None):
        """Two-column info row"""
        if y:
            self.set_y(y)
        self.set_font('Helvetica', '', 10)
        self.set_text_color(*COLORS['text_light'])
        self.cell(70, 8, self.clean_text(label), ln=False)
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*COLORS['text'])
        self.cell(0, 8, self.clean_text(str(value)), ln=True)
        self.ln(2)
        
    def clean_text(self, text):
        """Remove emojis and special characters that FPDF can't handle"""
        if not text:
            return ""
        # Remove emojis and other non-ASCII chars
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"
            u"\U0001F300-\U0001F5FF"
            u"\U0001F680-\U0001F6FF"
            u"\U0001F1E0-\U0001F1FF"
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            u"\U0001F900-\U0001F9FF"
            u"\U0001FA70-\U0001FAFF"
            u"\U000025A0-\U000027BF"
            u"\U00002B50-\U00002B59"
            "]+", flags=re.UNICODE)
        text = emoji_pattern.sub(r'', text)
        # Replace common symbols
        replacements = {
            '✓': '[OK]', '⚠️': '[!]', '✅': '[OK]', '❌': '[X]',
            '🔴': '[!]', '🟡': '[*]', '🔧': '[Tool]', '🏠': '[Home]',
            '📊': '[Data]', '💰': '[Euro]', '💶': '[Euro]', '🗺️': '[Map]',
            '🌡️': '[Temp]', '📨': '[Mail]', '⬇️': '[Download]',
            '⚡': '[AI]', '🛠️': '[Tool]', '🟢': '[Green]', 'é': 'e',
            'è': 'e', 'ê': 'e', 'ë': 'e', 'à': 'a', 'â': 'a', 'ä': 'a',
            'ô': 'o', 'ö': 'o', 'û': 'u', 'ü': 'u', 'ï': 'i', 'î': 'i',
            'ç': 'c', '€': 'EUR'
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text.encode('latin-1', errors='replace').decode('latin-1')


def generate_professional_pdf(property_data, scenario, target_dpe, active_cost, net_cost, subsidy, roi):
    """
    Generates a professional, investment-grade PDF report.
    """
    pdf = ZAMIPDF(property_data, scenario)
    pdf.add_page()
    
    # ============================================
    # PROPERTY INFO SECTION
    # ============================================
    pdf.section_title('Property Information')
    
    # Address
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(*COLORS['text'])
    address = property_data.get('address', 'Address not available')
    clean_address = pdf.clean_text(address)
    pdf.multi_cell(0, 6, clean_address, align='L')
    pdf.ln(8)
    
    # DPE Badge and metrics row
    start_y = pdf.get_y()
    pdf.set_x(15)
    pdf.dpe_badge(property_data.get('dpe', 'E'), 50)
    
    pdf.set_x(75)
    pdf.metric_card('Surface', int(property_data.get('surface', 0)), ' m2')
    pdf.set_x(75)
    pdf.metric_card('Current Value (est.)', int(property_data.get('current_value', 250000)), ' EUR')
    
    pdf.set_y(start_y + 45)
    pdf.ln(10)
    
    # Additional property details
    pdf.info_row('Building Type', property_data.get('type_batiment', 'Not specified'))
    pdf.info_row('Construction Year', property_data.get('annee_construction', 'Not specified') or 'Not specified')
    pdf.info_row('Heating System', property_data.get('energie_chauffage', 'Not specified') or 'Not specified')
    
    conso_kwh = property_data.get('conso_kwh')
    if conso_kwh:
        pdf.info_row('Energy Consumption', f"{conso_kwh} kWh/year")
    
    emission_ges = property_data.get('emission_ges')
    if emission_ges:
        pdf.info_row('CO2 Emissions', f"{emission_ges} kg CO2/year")
    
    pdf.ln(10)
    
    # ============================================
    # RENOVATION SCENARIO SECTION
    # ============================================
    pdf.section_title('Renovation Scenario')
    
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
    dpe_color = DPE_COLORS.get(target_dpe.upper(), COLORS['primary'])
    pdf.set_text_color(*dpe_color)
    pdf.cell(0, 8, target_dpe.upper(), ln=True)
    pdf.ln(5)
    
    # Financial metrics
    pdf.info_row('Total Renovation Cost', f'EUR {active_cost:,.0f}')
    pdf.info_row('MaPrimeRenov Subsidy', f'EUR {subsidy:,.0f}')
    pdf.info_row('Net Investment', f'EUR {net_cost:,.0f}')
    pdf.info_row('Expected ROI', f'+{roi}%')
    
    pdf.ln(10)
    
    # ============================================
    # FINANCIAL SUMMARY TABLE
    # ============================================
    pdf.section_title('Financial Summary')
    
    # Table header
    pdf.set_fill_color(*COLORS['primary'])
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(100, 10, 'Item', border=1, fill=True, ln=False)
    pdf.cell(75, 10, 'Amount (EUR)', border=1, fill=True, ln=True)
    
    # Table rows
    pdf.set_fill_color(255, 255, 255)
    pdf.set_text_color(*COLORS['text'])
    pdf.set_font('Helvetica', '', 10)
    
    rows = [
        ('Renovation Cost', f'{active_cost:,.0f}'),
        ('MaPrimeRenov Subsidy', f'-{subsidy:,.0f}'),
        ('', ''),
        ('Net Investment', f'{net_cost:,.0f}')
    ]
    
    for label, value in rows:
        if label == '':
            pdf.cell(100, 5, '', border=0, ln=True)
            continue
        pdf.cell(100, 10, pdf.clean_text(label), border=1)
        pdf.cell(75, 10, value, border=1, ln=True)
        
    pdf.ln(8)
    
    # Value increase calculation
    current_value = property_data.get('current_value', 250000)
    value_increase = int(current_value * (roi / 100))
    new_value = current_value + value_increase
    
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 8, f'Expected Value After Renovation: EUR {new_value:,.0f}', ln=True)
    pdf.set_text_color(*COLORS['primary'])
    pdf.cell(0, 8, f'Value Increase: +EUR {value_increase:,.0f} (+{roi}%)', ln=True)
    
    pdf.ln(15)
    
    # ============================================
    # RECOMMENDATIONS SECTION
    # ============================================
    pdf.section_title('Smart Recommendations')
    
    recommendations = get_recommendations(property_data.get('dpe', 'E'), target_dpe)
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(*COLORS['text'])
    
    for i, rec in enumerate(recommendations, 1):
        clean_rec = pdf.clean_text(rec)
        pdf.multi_cell(0, 6, f'{i}. {clean_rec}', align='L')
        pdf.ln(2)
    
    pdf.ln(10)
    
    # ============================================
    # NEXT STEPS SECTION
    # ============================================
    pdf.section_title('Next Steps')
    
    next_steps = [
        'Download this report and share with certified RGE contractors',
        'Contact our team for a personalized consultation',
        'Apply for MaPrimeRenov subsidy through official channels',
        'Start your renovation project with government-backed financing',
        'Track your project progress on ZAMI dashboard'
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
    pdf.multi_cell(0, 4, pdf.clean_text(disclaimer), align='L')
    
    return pdf.output(dest='S').encode('latin-1')


def get_recommendations(current_dpe, target_dpe):
    """Returns renovation recommendations based on current and target DPE"""
    
    base_recs = [
        "Insulate attic and roof (reduces heat loss by up to 30%)",
        "Replace old windows with double/triple glazing",
        "Install programmable thermostat for better energy management"
    ]
    
    if current_dpe in ['F', 'G']:
        return [
            "URGENT: Install wall insulation (accounts for 25 percent of heat loss)",
            "URGENT: Replace heating system with heat pump or biomass boiler",
            "Upgrade to energy-efficient appliances (Class A+++)",
            "Install solar panels for water heating",
        ] + base_recs
    elif current_dpe == 'E':
        return [
            "Upgrade heating system to condensing boiler",
            "Improve wall insulation where possible",
            "Install individual room temperature controls",
        ] + base_recs
    elif current_dpe in ['C', 'D']:
        return [
            "Optimize existing heating system settings",
            "Add smart home energy monitoring system",
            "Consider solar panel installation for electricity generation",
        ] + base_recs[:2]
    else:
        return [
            "Maintain existing equipment regularly",
            "Consider small improvements: LED lighting, weatherstripping",
            "Monitor energy consumption to identify waste"
        ]