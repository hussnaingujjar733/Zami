"""
reportlab_generator.py — ZAMI Rapport Français
French version, perfect alignment, clean layout
"""

from fpdf import FPDF
from datetime import datetime


class FrenchPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=25)
    
    def header(self):
        self.set_draw_color(34, 197, 94)
        self.set_line_width(1)
        self.line(10, 15, 200, 15)
        
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(34, 197, 94)
        self.set_xy(15, 6)
        self.cell(0, 6, 'ZAMI', ln=False)
        
        self.set_font('Helvetica', '', 8)
        self.set_text_color(128, 128, 128)
        self.set_xy(180, 7)
        self.cell(0, 4, f'Page {self.page_no()}', ln=False)
        
        self.ln(22)
    
    def footer(self):
        self.set_y(-22)
        self.set_font('Helvetica', 'I', 7)
        self.set_text_color(150, 150, 150)
        self.cell(0, 4, 'ZAMI - Intelligence Rénovation', ln=True, align='C')
    
    def titre1(self, texte):
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, texte, ln=True)
        self.set_draw_color(34, 197, 94)
        self.line(10, self.get_y(), 50, self.get_y())
        self.ln(6)
    
    def titre2(self, texte):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(34, 197, 94)
        self.cell(0, 8, texte, ln=True)
        self.ln(3)
    
    def texte(self, texte):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(80, 80, 80)
        self.multi_cell(0, 6, texte, align='L')
        self.ln(2)
    
    def ligne_deux(self, gauche, droite):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(80, 80, 80)
        self.cell(70, 7, gauche, ln=False)
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(0, 0, 0)
        self.cell(0, 7, droite, ln=True)
    
    def carte(self, x, y, label, valeur):
        self.set_xy(x, y)
        self.set_fill_color(248, 250, 252)
        self.rect(x, y, 55, 32, 'F')
        self.set_font('Helvetica', '', 7)
        self.set_text_color(100, 100, 100)
        self.set_xy(x + 5, y + 5)
        self.cell(0, 4, label)
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(0, 0, 0)
        self.set_xy(x + 5, y + 15)
        self.cell(0, 6, valeur)


def generer_rapport(property_data):
    """Generate French PDF report with perfect alignment"""
    
    # Calcul des valeurs
    surface = property_data.get('surface', 75)
    dpe = property_data.get('dpe', 'E')
    cout = property_data.get('cost', 46500)
    roi = property_data.get('roi', 13.1)
    
    valeur_actuelle = 280000
    subvention = int(12500 * (surface / 68))
    investissement_net = cout - subvention
    valeur_finale = int(valeur_actuelle * (1 + roi / 100))
    gain = valeur_finale - valeur_actuelle - investissement_net
    
    # Score
    scores_dpe = {'A': 95, 'B': 85, 'C': 70, 'D': 55, 'E': 40, 'F': 25, 'G': 10}
    score_total = scores_dpe.get(dpe, 40)
    
    pdf = FrenchPDF()
    
    # ============================================
    # PAGE DE COUVERTURE
    # ============================================
    pdf.add_page()
    
    pdf.set_y(60)
    pdf.set_font('Helvetica', 'B', 44)
    pdf.set_text_color(34, 197, 94)
    pdf.cell(0, 20, 'ZAMI', ln=True, align='C')
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 8, 'RAPPORT D\'ANALYSE', ln=True, align='C')
    pdf.ln(15)
    
    # Adresse
    adresse = property_data.get('address', 'Adresse non disponible')[:60]
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 7, adresse, align='C')
    pdf.ln(10)
    
    # Badge DPE
    couleurs_dpe = {
        'A': (34, 197, 94), 'B': (74, 222, 128), 'C': (163, 230, 53),
        'D': (250, 204, 21), 'E': (251, 146, 60), 'F': (249, 115, 22),
        'G': (239, 68, 68)
    }
    couleur = couleurs_dpe.get(dpe, (100, 100, 100))
    pdf.set_fill_color(couleur[0], couleur[1], couleur[2])
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 48)
    pdf.set_x(210/2 - 25)
    pdf.cell(50, 50, dpe, border=0, align='C', fill=True)
    pdf.ln(18)
    
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, f'SCORE ZAMI: {score_total}/100', ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 5, datetime.now().strftime("%d %B %Y"), ln=True, align='C')
    
    # ============================================
    # PAGE 1: RESUME
    # ============================================
    pdf.add_page()
    pdf.titre1('Résumé Exécutif')
    pdf.texte('Ce rapport analyse le potentiel de rénovation énergétique de votre bien, incluant les projections financières, les subventions disponibles et les recommandations stratégiques.')
    
    pdf.ln(8)
    
    # Cartes KPI
    debut_y = pdf.get_y()
    cartes = [
        ('Valeur Actuelle', f'EUR {valeur_actuelle:,}'),
        ('Coût des Travaux', f'EUR {cout:,}'),
        ('Subvention', f'EUR {subvention:,}'),
        ('Valeur Future', f'EUR {valeur_finale:,}'),
        ('Invest. Net', f'EUR {investissement_net:,}'),
        ('ROI', f'+{roi:.1f}%'),
    ]
    
    for i, (label, valeur) in enumerate(cartes):
        x = 15 + (i % 3) * 60
        y = debut_y + (i // 3) * 38
        pdf.carte(x, y, label, valeur)
    
    pdf.ln(80)
    
    pdf.titre2('Gain Net Estimé Après Rénovation')
    pdf.set_font('Helvetica', 'B', 15)
    pdf.set_text_color(34, 197, 94)
    pdf.cell(0, 8, f'+EUR {gain:,}', ln=True)
    
    # ============================================
    # PAGE 2: CARACTERISTIQUES
    # ============================================
    pdf.add_page()
    pdf.titre1('Caractéristiques du Bien')
    
    pdf.ligne_deux('Adresse:', property_data.get('address', 'N/A')[:50])
    pdf.ligne_deux('Surface:', f'{int(surface)} m²')
    pdf.ligne_deux('DPE Actuel:', dpe)
    
    annee = 'Avant 1975 (estimé)' if dpe in ['F','G'] else '1980-2000 (estimé)'
    pdf.ligne_deux('Année de Construction:', annee)
    
    pdf.ligne_deux('Consommation Énergétique:', 'Estimée 250-350 kWh/m²/an')
    pdf.ligne_deux('Émissions CO2:', 'Estimées 45-65 kg/m²/an')
    
    pdf.ln(8)
    pdf.titre1('Détail du Score ZAMI')
    
    pdf.ligne_deux('Performance Énergétique:', f'{score_total}/100')
    pdf.ligne_deux('Potentiel d\'Investissement:', f'{roi:.1f}% de ROI')
    pdf.ligne_deux('Conditions du Marché:', 'Standard')
    
    # ============================================
    # PAGE 3: ANALYSE FINANCIERE
    # ============================================
    pdf.add_page()
    pdf.titre1('Analyse Financière')
    
    pdf.titre2('Détail de l\'Investissement')
    pdf.ligne_deux('Valeur Actuelle du Bien:', f'EUR {valeur_actuelle:,}')
    pdf.ligne_deux('Investissement Travaux:', f'-EUR {cout:,}')
    pdf.ligne_deux('Subventions Publiques:', f'+EUR {subvention:,}')
    pdf.ligne_deux('Investissement Net:', f'EUR {investissement_net:,}')
    pdf.ligne_deux('Plus-Value Estimée:', f'+EUR {valeur_finale - valeur_actuelle:,}')
    pdf.ligne_deux('Valeur Après Travaux:', f'EUR {valeur_finale:,}')
    pdf.ligne_deux('Gain Total:', f'+EUR {gain:,}')
    
    pdf.ln(8)
    pdf.titre2('Détail des Subventions')
    pdf.texte(f'Subvention MaPrimeRénov\' estimée: EUR {subvention:,}')
    pdf.texte('Des aides régionales supplémentaires peuvent être disponibles selon la localisation.')
    
    # ============================================
    # PAGE 4: RECOMMANDATIONS
    # ============================================
    pdf.add_page()
    pdf.titre1('Recommandations de Rénovation')
    
    if dpe in ['F', 'G']:
        recommandations = [
            ('Priorité 1', 'Audit Énergétique', 'EUR 500-1 000', 'Semaine 1'),
            ('Priorité 2', 'Isolation des Murs', 'EUR 12 000-18 000', 'Semaines 2-4'),
            ('Priorité 3', 'Isolation des Combles', 'EUR 8 000-12 000', 'Semaines 4-5'),
            ('Priorité 4', 'Remplacement Chauffage', 'EUR 10 000-15 000', 'Semaines 6-8'),
            ('Priorité 5', 'Audit Final', 'EUR 500-1 000', 'Semaine 9'),
        ]
    elif dpe == 'E':
        recommandations = [
            ('Priorité 1', 'Remplacement Chauffage', 'EUR 10 000-15 000', 'Semaines 1-3'),
            ('Priorité 2', 'Remplacement Fenêtres', 'EUR 8 000-12 000', 'Semaines 3-5'),
            ('Priorité 3', 'Ventilation', 'EUR 4 000-7 000', 'Semaines 5-6'),
        ]
    else:
        recommandations = [
            ('Priorité 1', 'Optimisation Chauffage', 'EUR 500-2 000', 'Semaine 1'),
            ('Priorité 2', 'Remplacement Fenêtres', 'EUR 6 000-10 000', 'Semaines 2-3'),
            ('Priorité 3', 'Étude Solaire', 'EUR 500', 'Semaine 3-4'),
        ]
    
    # En-tête du tableau
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(34, 197, 94)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(30, 8, 'Priorité', border=1, align='C', fill=True)
    pdf.cell(60, 8, 'Action', border=1, align='C', fill=True)
    pdf.cell(45, 8, 'Coût Estimé', border=1, align='C', fill=True)
    pdf.cell(45, 8, 'Délai', border=1, align='C', fill=True)
    pdf.ln()
    
    # Lignes du tableau
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Helvetica', '', 9)
    fill = False
    for rec in recommandations:
        pdf.cell(30, 7, rec[0], border=1, align='L', fill=fill)
        pdf.cell(60, 7, rec[1], border=1, align='L', fill=fill)
        pdf.cell(45, 7, rec[2], border=1, align='L', fill=fill)
        pdf.cell(45, 7, rec[3], border=1, align='L', fill=fill)
        pdf.ln()
        fill = not fill
    
    pdf.ln(8)
    
    if dpe in ['F', 'G']:
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(239, 68, 68)
        pdf.cell(0, 6, 'URGENT: Ce bien risque l\'interdiction de location dès 2025.', ln=True)
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(80, 80, 80)
        pdf.multi_cell(0, 6, 'Une rénovation immédiate est recommandée pour maintenir la valeur du bien et les revenus locatifs.')
    
    # ============================================
    # PAGE 5: PROCHAINES ETAPES
    # ============================================
    pdf.add_page()
    pdf.titre1('Prochaines Étapes')
    
    etapes = [
        '1. Réaliser un audit énergétique sur site par un professionnel certifié',
        '2. Déposer une demande de subvention MaPrimeRénov\' (délai: 4-6 semaines)',
        '3. Obtenir au moins 3 devis d\'artisans certifiés RGE',
        '4. Étudier les options de financement (Eco-PTZ, prêts bancaires)',
        '5. Planifier les travaux selon l\'ordre de priorité',
        '6. Réaliser un audit post-travaux pour valider l\'amélioration du DPE',
    ]
    
    for etape in etapes:
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(80, 80, 80)
        pdf.multi_cell(0, 7, etape, align='L')
        pdf.ln(2)
    
    pdf.ln(15)
    
    pdf.titre1('Contactez nos Experts')
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 7, 'Email: experts@thezami.com', ln=True, align='C')
    pdf.cell(0, 7, 'Téléphone: +33 (0)1 23 45 67 89', ln=True, align='C')
    pdf.cell(0, 7, 'Site Web: thezami.com', ln=True, align='C')
    
    pdf.ln(10)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 5, 'Ce rapport est une estimation générée par IA. Un audit technique sur site est recommandé.', ln=True, align='C')
    
    # Retourner le PDF
    output = pdf.output(dest='S')
    if isinstance(output, str):
        output = output.encode('latin-1', errors='replace')
    
    return output


make_report = generer_rapport