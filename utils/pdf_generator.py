"""
Professional PDF Report Generator for ZAMI
Generates complete renovation report for homeowners
"""

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import datetime
import os

try:
    # Try to register a nice font
    pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
except:
    pass

def generate_complete_report(data):
    """Generate professional PDF report"""
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15*mm,
        leftMargin=15*mm,
        topMargin=20*mm,
        bottomMargin=20*mm,
        title=f"ZAMI_Rapport_{data.get('postcode', '')}_{datetime.datetime.now().strftime('%Y%m%d')}"
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1B5E20'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='DejaVuSans-Bold'
    )
    
    heading1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2E7D32'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='DejaVuSans-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=colors.HexColor('#1976D2'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='DejaVuSans-Bold'
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        fontName='DejaVuSans'
    )
    
    small_style = ParagraphStyle(
        'Small',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#666666'),
        spaceAfter=4,
        fontName='DejaVuSans'
    )
    
    story = []
    
    # ==================== TITLE PAGE ====================
    story.append(Paragraph("ZAMI", title_style))
    story.append(Paragraph("Rapport de Diagnostic Énergétique", title_style))
    story.append(Spacer(1, 10*mm))
    
    # Property info box
    info_data = [
        ["Adresse du bien", data.get('address', 'N/A')],
        ["Date du rapport", datetime.datetime.now().strftime("%d/%m/%Y")],
        ["Surface habitable", f"{data.get('surface', 0)} m²"],
        ["Type de bien", data.get('property_type', 'Appartement')],
        ["Code postal", data.get('postcode', 'N/A')]
    ]
    
    info_table = Table(info_data, colWidths=[60*mm, 100*mm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E8F5E9')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 15*mm))
    
    # ==================== EXECUTIVE SUMMARY ====================
    story.append(Paragraph("Résumé Exécutif", heading1_style))
    
    summary_data = [
        ["Diagnostic actuel", f"DPE {data.get('current_dpe', 'N/A')}", f"Consommation: {data.get('current_consumption', 0)} kWh/m²/an"],
        ["Objectif après travaux", f"DPE {data.get('target_dpe', 'N/A')}", f"Consommation: {data.get('target_consumption', 0)} kWh/m²/an"],
        ["Gain énergétique", f"{data.get('savings_percentage', 0)}%", f"Économie: {data.get('annual_savings', 0):,.0f} €/an"],
    ]
    
    summary_table = Table(summary_data, colWidths=[50*mm, 50*mm, 60*mm])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E7D32')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 10*mm))
    
    # ==================== FINANCIAL ANALYSIS ====================
    story.append(Paragraph("Score d'Opportunité ZAMI", heading1_style))

    opportunity_score = 0
    if data.get('savings_percentage', 0) >= 40:
        opportunity_score += 25
    elif data.get('savings_percentage', 0) >= 25:
        opportunity_score += 15

    if data.get('roi', 0) >= 70:
        opportunity_score += 25
    elif data.get('roi', 0) >= 40:
        opportunity_score += 15

    if data.get('subsidy', 0) > 0:
        opportunity_score += 20

    if data.get('confidence_score', 0) >= 80:
        opportunity_score += 20
    elif data.get('confidence_score', 0) >= 65:
        opportunity_score += 10

    if data.get('payback', 99) <= 10:
        opportunity_score += 10

    opportunity_score = min(opportunity_score, 100)

    if opportunity_score >= 80:
        opportunity_label = "Excellent projet de rénovation"
    elif opportunity_score >= 60:
        opportunity_label = "Projet intéressant à étudier"
    else:
        opportunity_label = "Projet à qualifier avec un artisan"

    score_data = [
        ["Score ZAMI", f"{opportunity_score}/100"],
        ["Analyse", opportunity_label],
        ["Facteurs pris en compte", "Économies, aides, ROI, fiabilité et temps de retour"],
    ]

    score_table = Table(score_data, colWidths=[2.4*inch, 4.2*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F5F5F5')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#333333')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#DDDDDD')),
        ('PADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("Pourquoi cette estimation ?", heading1_style))

    source_dpe = "Données ADEME trouvées" if data.get("dpe_source") == "ADEME_API" else "Estimation basée sur les informations saisies"

    explanation_data = [
        ["Surface utilisée", f"{data.get('surface', 0)} m²"],
        ["DPE actuel", data.get("current_dpe", "N/A")],
        ["Objectif DPE", data.get("target_dpe", "N/A")],
        ["Localisation", f"{data.get('postcode', '')}"],
        ["Source DPE", source_dpe],
        ["Méthode", "Fourchette de coût pour éviter une fausse précision"],
        ["Niveau de fiabilité", data.get("confidence_label", "Moyenne")],
    ]

    explanation_table = Table(explanation_data, colWidths=[2.8*inch, 3.8*inch])
    explanation_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F5F5F5')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#333333')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#DDDDDD')),
        ('PADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(explanation_table)
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("Analyse Financière", heading1_style))
    
    financial_data = [
        ["Coût estimé des travaux", f"{data.get('cost_min', data.get('renovation_cost', 0)):,.0f} € - {data.get('cost_max', data.get('renovation_cost', 0)):,.0f} €", "Estimation initiale"],
        ["Confiance estimation", f"{data.get('confidence_score', 70)}%", data.get('confidence_label', 'Moyenne')],
        ["MaPrimeRénov'", f"- {data.get('subsidy', 0):,.0f} €", f"Taux: {data.get('subsidy_rate', 0)}%"],
        ["", "", ""],
        ["Reste à charge (investissement net)", f"{data.get('net_investment', 0):,.0f} €", ""],
        ["", "", ""],
        ["Valeur actuelle du bien", f"{data.get('current_value', 0):,.0f} €", ""],
        ["Valeur après rénovation", f"{data.get('future_value', 0):,.0f} €", f"+{data.get('added_value', 0):,.0f} €"],
        ["", "", ""],
        ["Retour sur investissement (ROI)", f"{data.get('roi', 0)}%", ""],
        ["Économies annuelles", f"{data.get('annual_savings', 0):,.0f} €", "sur facture énergétique"],
        ["Économies estimées sur 10 ans", f"{data.get('annual_savings', 0) * 10:,.0f} €", "avant évolution des prix"],
        ["Temps de retour sur investissement", f"{data.get('payback', 0)} ans", ""],
    ]
    
    financial_table = Table(financial_data, colWidths=[80*mm, 50*mm, 40*mm])
    financial_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 1), colors.HexColor('#FFF3E0')),
        ('BACKGROUND', (0, 3), (0, 3), colors.HexColor('#E3F2FD')),
        ('BACKGROUND', (0, 5), (0, 6), colors.HexColor('#E8F5E9')),
        ('BACKGROUND', (0, 8), (0, 10), colors.HexColor('#F3E5F5')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(financial_table)
    story.append(Spacer(1, 10*mm))
    
    # ==================== DPE DETAILS ====================
    story.append(Paragraph("Comprendre le niveau de fiabilité", heading1_style))

    confidence_text = f"""
    Le niveau de fiabilité indique la qualité des informations utilisées pour produire cette estimation.
    Une fiabilité élevée signifie que l'adresse et le DPE ont pu être mieux identifiés.
    Cette fiabilité ne remplace pas une visite technique, mais permet de mieux comprendre la précision de l'estimation.
    """
    story.append(Paragraph(confidence_text, normal_style))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("Répartition estimative des travaux", heading1_style))

    breakdown_data = [
        ["Poste de travaux", "Part estimée"],
        ["Isolation thermique", "45%"],
        ["Chauffage / système énergétique", "30%"],
        ["Ventilation", "15%"],
        ["Menuiseries", "10%"],
    ]

    breakdown_table = Table(breakdown_data, colWidths=[4.2*inch, 2.0*inch])
    breakdown_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D4AF37')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#DDDDDD')),
        ('PADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(breakdown_table)
    story.append(Paragraph(
        "Cette répartition est indicative et dépendra du diagnostic technique, des matériaux choisis et des devis artisans.",
        normal_style
    ))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("Détail du Diagnostic de Performance Énergétique", heading1_style))
    
    dpe_data = [
        ["Paramètre", "Actuel", "Après travaux"],
        ["Étiquette DPE", data.get('current_dpe', 'N/A'), data.get('target_dpe', 'N/A')],
        ["Consommation (kWh/m²/an)", f"{data.get('current_consumption', 0)}", f"{data.get('target_consumption', 0)}"],
        ["Consommation totale (kWh/an)", f"{data.get('current_consumption', 0) * data.get('surface', 0):,.0f}", f"{data.get('target_consumption', 0) * data.get('surface', 0):,.0f}"],
        ["Coût énergétique annuel", f"{data.get('current_energy_cost', 0):,.0f} €", f"{data.get('target_energy_cost', 0):,.0f} €"],
    ]
    
    dpe_table = Table(dpe_data, colWidths=[60*mm, 50*mm, 50*mm])
    dpe_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E7D32')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FAFAFA')),
    ]))
    story.append(dpe_table)
    story.append(Spacer(1, 10*mm))
    
    # ==================== RECOMMENDATIONS ====================
    story.append(Paragraph("Recommandations Personnalisées", heading1_style))
    
    recommendations = [
        "1. Audit énergétique approfondi",
        "   • Faire réaliser un audit par un professionnel certifié (500-1000€)",
        "   • L'audit est obligatoire pour bénéficier des aides MaPrimeRénov'",
        "",
        "2. Isolation thermique (priorité n°1)",
        "   • Isolation des murs par l'extérieur ou l'intérieur",
        "   • Isolation des combles et de la toiture",
        "   • Isolation des planchers bas",
        "",
        "3. Système de chauffage performant",
        "   • Pompes à chaleur air-eau ou air-air",
        "   • Chaudière biomasse (granulés de bois)",
        "   • Système solaire combiné",
        "",
        "4. Ventilation",
        "   • Installation d'une VMC double flux",
        "   • Récupération de chaleur sur l'air extrait",
        "",
        "5. Menuiseries",
        "   • Remplacement des fenêtres simple vitrage",
        "   • Double ou triple vitrage performant",
    ]
    
    for rec in recommendations:
        if rec == "":
            story.append(Spacer(1, 5))
        elif rec.startswith(" "):
            story.append(Paragraph(rec, small_style))
        else:
            story.append(Paragraph(rec, normal_style))
    
    story.append(Spacer(1, 10*mm))
    
    # ==================== MAINTENANCE TIPS ====================
    story.append(Paragraph("Conseils d'Entretien", heading1_style))
    
    maintenance_data = [
        ["Action", "Fréquence", "Bénéfice"],
        ["Entretien chaudière", "Annuel", "Performance +15%"],
        ["Nettoyage VMC", "Tous les 6 mois", "Qualité d'air"],
        ["Vérification isolation", "Tous les 5 ans", "Maintien des performances"],
        ["Calorifugeage des tuyaux", "Une fois", "Économies +5%"],
    ]
    
    maintenance_table = Table(maintenance_data, colWidths=[50*mm, 40*mm, 50*mm])
    maintenance_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976D2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (1, 1), (1, -1), 'CENTER'),
        ('ALIGN', (2, 1), (2, -1), 'CENTER'),
    ]))
    story.append(maintenance_table)
    story.append(Spacer(1, 15*mm))
    
    # ==================== FOOTER / DISCLAIMER ====================
    story.append(Paragraph("Notes importantes", heading2_style))
    disclaimer_text = """
    <font size="8" color="#666666">
    * Ce rapport est une estimation initiale basée sur les informations saisies et les données publiques disponibles.<br/>
    * Les montants des aides sont indicatifs et sous réserve d'éligibilité après étude de dossier.<br/>
    * Un devis détaillé par un professionnel certifié RGE est recommandé avant tout début de travaux.<br/>
    * Les prix et les aides sont susceptibles d'évoluer selon la réglementation en vigueur.
    </font>
    """
    story.append(Paragraph(disclaimer_text, small_style))
    story.append(Spacer(1, 10*mm))
    
    # ==================== CONTACT ====================
    contact_text = """
    <b>ZAMI - Intelligence Artificielle pour la Rénovation Énergétique</b><br/>
    📧 thezamifrance@gmail.com | 📞 07 59 82 35 32<br/>
    🌐 www.thezami.com | Données: ADEME lorsque disponible, Base Adresse Nationale (BAN)<br/>
    © 2026 ZAMI. Tous droits réservés.
    """
    story.append(Paragraph(contact_text, small_style))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
