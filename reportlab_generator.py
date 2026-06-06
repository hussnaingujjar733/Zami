"""
reportlab_generator.py — ZAMI Rapport Professionnel
Layout propre, pas de chevauchement
"""

import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.graphics.shapes import Drawing, Rect, Circle, String
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# Couleurs
BLEU_FONCE = colors.HexColor('#0F172A')
BLEU_CLAIR = colors.HexColor('#3B82F6')
VERT = colors.HexColor('#22C55E')
ROUGE = colors.HexColor('#EF4444')
GRIS_CLAIR = colors.HexColor('#F1F5F9')
GRIS_MOYEN = colors.HexColor('#CBD5E1')
GRIS_TEXTE = colors.HexColor('#475569')
BLANC = colors.white


class RapportZAMI:
    def __init__(self, donnees):
        self.donnees = donnees
        
        # Valeurs calculées
        self.surface = donnees.get('surface', 75)
        self.dpe = donnees.get('dpe', 'E')
        self.cout = donnees.get('cost', 46500)
        self.roi = donnees.get('roi', 13.1)
        
        self.valeur_actuelle = 280000
        self.subvention = int(12500 * (self.surface / 68))
        self.investissement_net = self.cout - self.subvention
        self.valeur_finale = int(self.valeur_actuelle * (1 + self.roi / 100))
        self.gain = self.valeur_finale - self.valeur_actuelle - self.investissement_net
        
        # Calcul du score
        scores_dpe = {'A': 95, 'B': 85, 'C': 70, 'D': 55, 'E': 40, 'F': 25, 'G': 10}
        self.score = scores_dpe.get(self.dpe, 40)
        
        self.buffer = io.BytesIO()
        self.styles = getSampleStyleSheet()
        self._creer_styles()
    
    def _creer_styles(self):
        self.styles.add(ParagraphStyle(
            name='TitrePrincipal',
            parent=self.styles['Title'],
            fontSize=42,
            textColor=BLANC,
            alignment=TA_CENTER,
            spaceAfter=25,
        ))
        self.styles.add(ParagraphStyle(
            name='SousTitre',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#CBD5E1'),
            alignment=TA_CENTER,
        ))
        self.styles.add(ParagraphStyle(
            name='TitreSection',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=BLEU_FONCE,
            spaceBefore=15,
            spaceAfter=8,
        ))
        self.styles.add(ParagraphStyle(
            name='TitreSousSection',
            parent=self.styles['Heading2'],
            fontSize=13,
            textColor=BLEU_CLAIR,
            spaceBefore=12,
            spaceAfter=6,
        ))
        self.styles.add(ParagraphStyle(
            name='ValeurKPI',
            parent=self.styles['Normal'],
            fontSize=18,
            textColor=BLEU_FONCE,
            alignment=TA_CENTER,
            spaceAfter=3,
        ))
        self.styles.add(ParagraphStyle(
            name='LabelKPI',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=GRIS_MOYEN,
            alignment=TA_CENTER,
        ))
        self.styles.add(ParagraphStyle(
            name='TexteNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=GRIS_TEXTE,
            alignment=TA_LEFT,
            spaceAfter=5,
        ))
        self.styles.add(ParagraphStyle(
            name='InfoBien',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=11,
            textColor=GRIS_TEXTE,
            alignment=TA_LEFT,
            leading=14,
        ))
    
    def _badge_dpe(self, canvas, x, y, taille, lettre):
        couleurs = {
            'A': (34, 197, 94), 'B': (74, 222, 128), 'C': (163, 230, 53),
            'D': (250, 204, 21), 'E': (251, 146, 60), 'F': (249, 115, 22),
            'G': (239, 68, 68)
        }
        r, g, b = couleurs.get(lettre, (100, 100, 100))
        canvas.setFillColorRGB(r/255, g/255, b/255)
        canvas.roundRect(x, y, taille, taille, taille/4, fill=1, stroke=0)
        canvas.setFillColorRGB(1, 1, 1)
        canvas.setFont('Helvetica-Bold', taille * 0.42)
        canvas.drawCentredString(x + taille/2, y + taille/2 - taille*0.08, lettre)
    
    def page_couverture(self):
        def dessiner(canvas, doc):
            canvas.saveState()
            # Fond
            canvas.setFillColor(BLEU_FONCE)
            canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
            # Bande bleue
            canvas.setFillColor(BLEU_CLAIR)
            canvas.rect(0, A4[1] - 6, A4[0], 6, fill=1, stroke=0)
            
            # Logo
            canvas.setFillColor(BLANC)
            canvas.setFont('Helvetica-Bold', 52)
            canvas.drawCentredString(A4[0]/2, A4[1] - 95, 'ZAMI')
            canvas.setFont('Helvetica', 9)
            canvas.setFillColor(colors.HexColor('#CBD5E1'))
            canvas.drawCentredString(A4[0]/2, A4[1] - 115, 'RAPPORT D\'ANALYSE')
            
            # Badge DPE
            self._badge_dpe(canvas, A4[0]/2 - 35, A4[1] - 240, 70, self.dpe)
            
            # Adresse
            canvas.setFont('Helvetica-Bold', 13)
            canvas.setFillColor(BLANC)
            adresse = self.donnees.get('address', 'Adresse')[:55]
            canvas.drawCentredString(A4[0]/2, A4[1] - 345, adresse)
            
            # Score
            canvas.setFont('Helvetica', 9)
            canvas.setFillColor(colors.HexColor('#94A3B8'))
            canvas.drawCentredString(A4[0]/2, A4[1] - 385, 'POTENTIEL DE RENOVATION')
            canvas.setFont('Helvetica-Bold', 44)
            canvas.setFillColor(VERT)
            canvas.drawCentredString(A4[0]/2, A4[1] - 435, str(self.score))
            canvas.setFont('Helvetica', 7)
            canvas.drawCentredString(A4[0]/2, A4[1] - 455, 'sur 100')
            
            # Date
            canvas.setFont('Helvetica', 8)
            canvas.setFillColor(colors.HexColor('#64748B'))
            canvas.drawCentredString(A4[0]/2, A4[1] - 520, datetime.now().strftime("%d/%m/%Y"))
            
            # Footer
            canvas.setFillColor(colors.HexColor('#1E293B'))
            canvas.rect(0, 0, A4[0], 50, fill=1, stroke=0)
            canvas.setFont('Helvetica', 7)
            canvas.setFillColor(colors.HexColor('#64748B'))
            canvas.drawCentredString(A4[0]/2, 22, 'ZAMI - Intelligence Rénovation')
            canvas.restoreState()
        return dessiner
    
    def page_resume(self):
        story = []
        story.append(Paragraph('Synthèse', self.styles['TitreSection']))
        story.append(Spacer(1, 5))
        story.append(Paragraph(
            "Ce rapport présente l'analyse du potentiel de rénovation énergétique de votre bien.",
            self.styles['TexteNormal']
        ))
        story.append(Spacer(1, 15))
        
        # 2x3 grid de KPIs
        kpis = [
            ('Valeur actuelle', f"{self.valeur_actuelle:,} €"),
            ('Coût des travaux', f"{self.cout:,} €"),
            ('Subventions', f"{self.subvention:,} €"),
            ('Valeur après travaux', f"{self.valeur_finale:,} €"),
            ('Investissement net', f"{self.investissement_net:,} €"),
            ('ROI estimé', f"+{self.roi:.1f}%"),
        ]
        
        # Disposition en 3 colonnes
        data = [[], [], []]
        for i, (label, valeur) in enumerate(kpis):
            col = i % 3
            data[col].append([Paragraph(label, self.styles['LabelKPI']),
                             Paragraph(valeur, self.styles['ValeurKPI'])])
        
        # Construire le tableau
        tableau_data = []
        for i in range(2):  # 2 lignes
            ligne = []
            for col in range(3):
                if i < len(data[col]):
                    cellule = data[col][i]
                    ligne.append(cellule)
                else:
                    ligne.append(['', ''])
            tableau_data.append(ligne)
        
        t = Table(tableau_data, colWidths=[A4[0]/3 - 15] * 3)
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, -1), GRIS_CLAIR),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(t)
        story.append(Spacer(1, 20))
        
        # Gain net
        story.append(Paragraph(
            f"<b>Gain net estimé après rénovation : {self.gain:,} €</b>",
            self.styles['TitreSousSection']
        ))
        return story
    
    def page_caracteristiques(self):
        story = []
        story.append(PageBreak())
        story.append(Paragraph('Caractéristiques du bien', self.styles['TitreSection']))
        story.append(Spacer(1, 10))
        
        details = [
            ['Adresse', self.donnees.get('address', 'Non renseignée')[:65]],
            ['Surface habitable', f"{int(self.surface)} m²"],
            ['Diagnostic DPE', self.dpe],
            ['Année construction', 'Estimée avant 1975' if self.dpe in ['F','G'] else 'Estimée 1980-2000'],
        ]
        
        t = Table(details, colWidths=[60, A4[0] - 85])
        t.setStyle(TableStyle([
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
            ('TEXTCOLOR', (0, 0), (0, -1), BLEU_CLAIR),
            ('FONT', (1, 0), (1, -1), 'Helvetica', 10),
            ('BACKGROUND', (0, 0), (-1, -1), GRIS_CLAIR),
            ('GRID', (0, 0), (-1, -1), 0.5, GRIS_MOYEN),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(t)
        return story
    
    def page_travaux(self):
        story = []
        story.append(PageBreak())
        story.append(Paragraph('Préconisations techniques', self.styles['TitreSection']))
        story.append(Spacer(1, 5))
        story.append(Paragraph(
            "Travaux recommandés pour améliorer la performance énergétique :",
            self.styles['TexteNormal']
        ))
        story.append(Spacer(1, 15))
        
        if self.dpe in ['F', 'G']:
            travaux = [
                ('1. Isolation des murs', '12 000 - 18 000 €', '25-30%', '+8-10%'),
                ('2. Isolation des combles', '8 000 - 12 000 €', '20-25%', '+6-8%'),
                ('3. Remplacement chauffage', '10 000 - 15 000 €', '30-35%', '+10-12%'),
            ]
        else:
            travaux = [
                ('1. Remplacement chauffage', '10 000 - 15 000 €', '30-35%', '+10-12%'),
                ('2. Remplacement fenêtres', '8 000 - 12 000 €', '15-20%', '+5-7%'),
                ('3. Ventilation mécanique', '4 000 - 7 000 €', '10-15%', '+3-5%'),
            ]
        
        for nom, cout, econ, rend in travaux:
            story.append(Paragraph(f"<b>{nom}</b>", self.styles['TitreSousSection']))
            data = [
                ['Coût estimé', 'Économies', 'ROI'],
                [cout, econ, rend],
            ]
            t = Table(data, colWidths=[120, 100, 100])
            t.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 9),
                ('BACKGROUND', (0, 0), (-1, 0), GRIS_CLAIR),
                ('FONT', (0, 1), (-1, 1), 'Helvetica', 10),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 0.5, GRIS_MOYEN),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(t)
            story.append(Spacer(1, 10))
        
        story.append(Spacer(1, 10))
        story.append(Paragraph(
            f"<b>Enveloppe budgétaire estimée : {self.cout:,} €</b>",
            self.styles['TitreSousSection']
        ))
        return story
    
    def page_contact(self):
        story = []
        story.append(PageBreak())
        story.append(Spacer(1, 100))
        story.append(Paragraph('Besoin d\'un accompagnement ?', self.styles['TitreSection']))
        story.append(Spacer(1, 10))
        story.append(Paragraph(
            "Nos experts vous aident à concrétiser votre projet de rénovation.",
            self.styles['TexteNormal']
        ))
        story.append(Spacer(1, 20))
        story.append(Paragraph("<b>Nous contacter</b>", self.styles['TexteNormal']))
        story.append(Paragraph("📧 experts@thezami.com", self.styles['TexteNormal']))
        story.append(Paragraph("📞 +33 1 23 45 67 89", self.styles['TexteNormal']))
        story.append(Spacer(1, 30))
        story.append(Paragraph(
            "<i>Rapport préliminaire - validation sur site recommandée</i>",
            self.styles['TexteNormal']
        ))
        return story
    
    def generer(self):
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            leftMargin=15*mm,
            rightMargin=15*mm,
            topMargin=18*mm,
            bottomMargin=18*mm,
        )
        
        elements = []
        elements.extend(self.page_resume())
        elements.append(PageBreak())
        elements.extend(self.page_caracteristiques())
        elements.append(PageBreak())
        elements.extend(self.page_travaux())
        elements.append(PageBreak())
        elements.extend(self.page_contact())
        
        doc.build(elements, onFirstPage=self.page_couverture(), onLaterPages=lambda c, d: None)
        return self.buffer.getvalue()


def generer_rapport(donnees):
    """Génère le rapport PDF"""
    rapport = RapportZAMI(donnees)
    return rapport.generer()