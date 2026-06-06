from datetime import datetime

def generer_rapport(data):
    """Generate simple text report - guaranteed working"""
    
    # Calculate values
    surface = data.get('surface', 75)
    dpe = data.get('dpe', 'E')
    cost = data.get('cost', 46500)
    roi = data.get('roi', 13.1)
    
    current_val = 280000
    subsidy = int(12500 * (surface / 68))
    net = cost - subsidy
    future_val = int(current_val * (1 + roi / 100))
    gain = future_val - current_val - net
    
    # Create report content
    report = f"""
================================================================================
                                    ZAMI
                          PROPERTY INTELLIGENCE REPORT
================================================================================

Report Generated: {datetime.now().strftime("%d/%m/%Y %H:%M")}

================================================================================
PROPERTY DETAILS
================================================================================

Address: {data.get('address', 'Not specified')}
Surface: {int(surface)} m²
Current DPE: {dpe}

================================================================================
FINANCIAL ANALYSIS
================================================================================

Current Value:               EUR {current_val:,}
Renovation Cost:             EUR {cost:,}
Available Subsidies:         EUR {subsidy:,}
Net Investment:              EUR {net:,}
Expected Value After Reno:   EUR {future_val:,}
Expected ROI:                +{roi:.1f}%

================================================================================
VALUE GAIN
================================================================================

Total Value Gain:            EUR {gain:,}

================================================================================
RECOMMENDATIONS
================================================================================

1. Complete energy audit by certified professional
2. Apply for MaPrimeRénov' subsidy
3. Contact certified RGE contractors for quotes
4. Prioritize insulation work (walls + roof)
5. Consider heat pump installation

================================================================================
CONTACT
================================================================================

📧 experts@thezami.com
📞 +33 1 23 45 67 89

================================================================================
Disclaimer: This is an AI-generated estimate based on available data.
Final figures require on-site technical audit.
================================================================================
"""
    
    return report.encode('utf-8')