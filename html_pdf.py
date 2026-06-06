"""
html_pdf.py — HTML to PDF Generator
Reliable, no style errors, proper layout
"""

import io
from datetime import datetime
from weasyprint import HTML, CSS
from jinja2 import Template


def generer_rapport(property_data):
    """Generate PDF using HTML template"""
    
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
    
    # Score
    dpe_scores = {'A': 95, 'B': 85, 'C': 70, 'D': 55, 'E': 40, 'F': 25, 'G': 10}
    score = dpe_scores.get(dpe, 40)
    
    # DPE color
    dpe_colors = {'A': '#22c55e', 'B': '#4ade80', 'C': '#a3e635', 'D': '#facc15', 'E': '#fb923c', 'F': '#f97316', 'G': '#ef4444'}
    dpe_color = dpe_colors.get(dpe, '#64748b')
    
    # HTML Template
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>ZAMI - Rapport d'analyse</title>
        <style>
            @page {{
                size: A4;
                margin: 2cm;
            }}
            body {{
                font-family: 'Helvetica', 'Arial', sans-serif;
                line-height: 1.5;
                color: #1e293b;
            }}
            .cover {{
                text-align: center;
                padding: 40px 0;
            }}
            .logo {{
                font-size: 48px;
                font-weight: bold;
                color: #0f172a;
                margin-bottom: 10px;
            }}
            .logo span {{
                color: #3b82f6;
            }}
            .dpe-badge {{
                display: inline-block;
                width: 80px;
                height: 80px;
                line-height: 80px;
                font-size: 36px;
                font-weight: bold;
                background: {dpe_color};
                color: white;
                border-radius: 20px;
                margin: 20px auto;
            }}
            .score {{
                font-size: 48px;
                font-weight: bold;
                color: #22c55e;
            }}
            .section-title {{
                font-size: 20px;
                font-weight: bold;
                color: #0f172a;
                border-left: 4px solid #3b82f6;
                padding-left: 12px;
                margin: 25px 0 15px 0;
            }}
            .kpi-grid {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 15px;
                margin: 20px 0;
            }}
            .kpi-card {{
                background: #f1f5f9;
                border-radius: 12px;
                padding: 15px;
                text-align: center;
            }}
            .kpi-value {{
                font-size: 22px;
                font-weight: bold;
                color: #0f172a;
            }}
            .kpi-label {{
                font-size: 11px;
                color: #64748b;
                margin-top: 5px;
            }}
            .info-table {{
                width: 100%;
                border-collapse: collapse;
                background: #f8fafc;
                border-radius: 12px;
            }}
            .info-table td {{
                padding: 12px;
                border-bottom: 1px solid #e2e8f0;
            }}
            .info-table td:first-child {{
                font-weight: bold;
                width: 35%;
                color: #3b82f6;
            }}
            .recommendations {{
                list-style: none;
                padding: 0;
            }}
            .recommendations li {{
                padding: 8px 0;
                border-bottom: 1px solid #e2e8f0;
            }}
            .footer {{
                text-align: center;
                padding-top: 30px;
                margin-top: 40px;
                border-top: 1px solid #e2e8f0;
                font-size: 10px;
                color: #94a3b8;
            }}
            .gain {{
                font-size: 18px;
                font-weight: bold;
                color: #22c55e;
                text-align: center;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        <!-- COVER PAGE -->
        <div class="cover">
            <div class="logo">ZAMI<span>.</span></div>
            <div style="font-size: 11px; color: #64748b; letter-spacing: 2px;">RAPPORT D'ANALYSE</div>
            
            <div class="dpe-badge">{dpe}</div>
            
            <div style="font-size: 14px; font-weight: bold; margin: 15px 0;">{property_data.get('address', 'Adresse')[:55]}</div>
            
            <div style="font-size: 11px; color: #64748b; margin-top: 20px;">POTENTIEL DE RENOVATION</div>
            <div class="score">{score}</div>
            <div style="font-size: 10px; color: #64748b;">sur 100</div>
            
            <div style="margin-top: 40px; font-size: 10px; color: #94a3b8;">{datetime.now().strftime("%d/%m/%Y")}</div>
        </div>
        
        <div style="page-break-before: always;"></div>
        
        <!-- PAGE 1: SYNOPSIS -->
        <div class="section-title">SYNTHESE</div>
        <p>Analyse du potentiel de rénovation énergétique du bien.</p>
        
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-value">{current_val:,} €</div>
                <div class="kpi-label">Valeur actuelle</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{cost:,} €</div>
                <div class="kpi-label">Coût travaux</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{subsidy:,} €</div>
                <div class="kpi-label">Subventions</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{future_val:,} €</div>
                <div class="kpi-label">Valeur finale</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{net:,} €</div>
                <div class="kpi-label">Invest. net</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">+{roi:.1f}%</div>
                <div class="kpi-label">ROI</div>
            </div>
        </div>
        
        <div class="gain">💰 Gain net estimé : {gain:,} €</div>
        
        <div style="page-break-before: always;"></div>
        
        <!-- PAGE 2: CARACTERISTIQUES -->
        <div class="section-title">CARACTERISTIQUES</div>
        
        <table class="info-table">
            <tr><td>Adresse</td><td>{property_data.get('address', 'N/A')[:65]}</td></tr>
            <tr><td>Surface</td><td>{int(surface)} m²</td></tr>
            <tr><td>DPE</td><td>{dpe}</td></tr>
            <tr><td>Construction</td><td>{"Avant 1975" if dpe in ['F','G'] else "1980-2000"}</td></tr>
        </table>
        
        <div style="page-break-before: always;"></div>
        
        <!-- PAGE 3: TRAVAUX -->
        <div class="section-title">TRAVAUX RECOMMANDES</div>
        
        <ul class="recommendations">
            <li><strong>Isolation des murs</strong> - 12 000 - 18 000 € (économie: 25-30%)</li>
            <li><strong>Isolation des combles</strong> - 8 000 - 12 000 € (économie: 20-25%)</li>
            <li><strong>Remplacement chauffage</strong> - 10 000 - 15 000 € (économie: 30-35%)</li>
        </ul>
        
        <div class="gain">Budget total estimé : {cost:,} €</div>
        
        <div style="page-break-before: always;"></div>
        
        <!-- PAGE 4: CONTACT -->
        <div style="text-align: center; margin-top: 100px;">
            <div class="section-title" style="text-align: center; border-left: none;">BESOIN D'ACCOMPAGNEMENT ?</div>
            <p style="margin: 20px 0;">Nos experts vous aident à concrétiser votre projet.</p>
            <p><strong>📧 experts@thezami.com</strong></p>
            <p><strong>📞 +33 1 23 45 67 89</strong></p>
            <p style="margin-top: 50px; font-size: 11px; color: #94a3b8;">Rapport préliminaire - validation sur site recommandée</p>
        </div>
        
        <div class="footer">ZAMI - Intelligence Rénovation Énergétique</div>
    </body>
    </html>
    """
    
    # Generate PDF
    html = HTML(string=html_template)
    pdf_bytes = html.write_pdf()
    
    return pdf_bytes