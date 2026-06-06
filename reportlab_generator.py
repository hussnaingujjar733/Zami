"""
reportlab_generator.py — ZAMI Rapport Professionnel
"""

import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
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
        self.score_global = scores_dpe.get(self.dpe, 40)
        
        self.buffer = io.BytesIO()
        self.styles = getSampleStyleSheet()
        self._ajouter_styles()
    
    def _ajouter_styles(self):
        self.styles.add(ParagraphStyle(
            name='TitrePrincipal',
            parent=self.styles['Title'],
            fontSize=42,
            textColor=BLANC,
            alignment=TA_CENTER,
            spaceAfter=30,
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
            spaceBefore=20,
            spaceAfter=10,
        ))
        self.styles.add(ParagraphStyle(
            name='TitreSousSection',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=BLEU_CLAIR,
            spaceBefore=15,
            spaceAfter=8,
        ))
        self.styles.add(ParagraphStyle(
            name='ValeurKPI',
            parent=self.styles['Normal'],
            fontSize=20,
            textColor=BLEU_FONCE,
            alignment=TA_CENTER,
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
            spaceAfter=6,
        ))
    
    def _badge_dpe(self, canvas, x, y, taille, lettre):
        couleurs = {
            'A': (34, 197, 94), 'B': (74, 222, 128), 'C': (163, 230, 53),
            'D': (250, 204, 21), 'E': (251, 146, 60), 'F': (249, 115, 22), 'G': (239, 68, 68)
        }
        r, g, b = couleurs.get(lettre, (100, 100, 100))
        canvas.setFillColorRGB(r/255, g/255, b/255)
        canvas.roundRect(x, y, taille, taille, taille/4, fill=1, stroke=0)
        canvas.setFillColorRGB(1, 1, 1)
        canvas.setFont('Helvetica-Bold', taille * 0.45)
        canvas.drawCentredString(x + taille/2, y + taille/2 - taille*0.08, lettre)
    
    def page1_couverture(self):
        def dessiner(canvas, doc):
            canvas.saveState()
            canvas.setFillColor(BLEU_FONCE)
            canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
            canvas.setFillColor(BLEU_CLAIR)
            canvas.rect(0, A4[1] - 6, A4[0], 6, fill=1, stroke=0)
            
            canvas.setFillColor(BLANC)
            canvas.setFont('Helvetica-Bold', 52)
            canvas.drawCentredString(A4[0]/2, A4[1] - 100, 'ZAMI')
            canvas.setFont('Helvetica', 9)
            canvas.setFillColor(colors.HexColor('#CBD5E1'))
            canvas.drawCentredString(A4[0]/2, A4[1] - 120, 'RAPPORT D\'ANALYSE')
            
            self._badge_dpe(canvas, A4[0]/2 - 35, A4[1] - 250, 70, self.dpe)
            
            canvas.setFont('Helvetica-Bold', 14)
            canvas.setFillColor(BLANC)
            adresse = self.donnees.get('address', 'Adresse')[:60]
            canvas.drawCentredString(A4[0]/2, A4[1] - 360, adresse)
            
            canvas.setFont('Helvetica', 9)
            canvas.setFillColor(colors.HexColor('#94A3B8'))
            canvas.drawCentredString(A4[0]/2, A4[1] - 400, 'SCORE DE RENOVATION')
            canvas.setFont('Helvetica-Bold', 44)
            canvas.setFillColor(VERT)
            canvas.drawCentredString(A4[0]/2, A4[1] - 450, str(self.score_global))
            canvas.setFont('Helvetica', 7)
            canvas.drawCentredString(A4[0]/2, A4[1] - 470, 'sur 100')
            
            canvas.setFont('Helvetica', 8)
            canvas.setFillColor(colors.HexColor('#64748B'))
            canvas.drawCentredString(A4[0]/2, A4[1] - 530, datetime.now().strftime("%d/%m/%Y"))
            
            canvas.setFillColor(colors.HexColor('#1E293B'))
            canvas.rect(0, 0, A4[0], 50, fill=1, stroke=0)
            canvas.setFont('Helvetica', 7)
            canvas.setFillColor(colors.HexColor('#64748B'))
            canvas.drawCentredString(A4[0]/2, 22, 'ZAMI - Intelligence Rénovation')
            canvas.restoreState()
        return dessiner
    
    def section_resume(self):
        story = []
        story.append(Paragraph('Résumé', self.styles['TitreSection']))
        story.append(Spacer(1, 5))
        story.append(Paragraph(
            'Analyse du potentiel de rénovation énergétique de votre bien.',
            self.styles['TexteNormal']
        ))
        story.append(Spacer(1, 20))
        
        # Tableau des KPIs
        data = [
            ['Valeur Actuelle', 'Coût Travaux', 'Subvention'],
            [f'{self.valeur_actuelle:,} €', f'{self.cout:,} €', f'{self.subvention:,} €'],
            ['', '', ''],
            ['Valeur Future', 'Investissement Net', 'ROI'],
            [f'{self.valeur_finale:,} €', f'{self.investissement_net:,} €', f'+{self.roi:.1f}%'],
        ]
        
        t = Table(data, colWidths=[A4[0]/3 - 15] * 3)
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONT', (0, 1), (-1, 1), 'Helvetica-Bold', 16),
            ('FONT', (0, 4), (-1, 4), 'Helvetica-Bold', 16),
            ('TEXTCOLOR', (0, 4), (-1, 4), VERT),
            ('BACKGROUND', (0, 1), (-1, 1), GRIS_CLAIR),
            ('BACKGROUND', (0, 4), (-1, 4), GRIS_CLAIR),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(t)
        story.append(Spacer(1, 25))
        story.append(Paragraph(
            f'<b>Gain Net Estimé: {self.gain:,} €</b>',
            self.styles['TitreSousSection']
        ))
        return story
    
    def section_bien(self):
        story = []
        story.append(PageBreak())
        story.append(Paragraph('Caractéristiques du Bien', self.styles['TitreSection']))
        story.append(Spacer(1, 10))
        
        details = [
            ['Adresse', self.donnees.get('address', 'N/A')[:65]],
            ['Surface', f'{int(self.surface)} m²'],
            ['DPE Actuel', self.dpe],
            ['Année Construction', 'Avant 1975' if self.dpe in ['F','G'] else '1980-2000'],
        ]
        
        t = Table(details, colWidths=[60, A4[0] - 80])
        t.setStyle(TableStyle([
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
            ('TEXTCOLOR', (0, 0), (0, -1), BLEU_CLAIR),
            ('GRID', (0, 0), (-1, -1), 0.5, GRIS_MOYEN),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(t)
        return story
    
    def section_travaux(self):
        story = []
        story.append(PageBreak())
        story.append(Paragraph('Plan de Travaux Recommandé', self.styles['TitreSection']))
        story.append(Spacer(1, 10))
        
        if self.dpe in ['F', 'G']:
            travaux = [
                ('Isolation des murs', '12 000 - 18 000 €', '25-30%', '+8-10%'),
                ('Isolation des combles', '8 000 - 12 000 €', '20-25%', '+6-8%'),
                ('Changement chauffage', '10 000 - 15 000 €', '30-35%', '+10-12%'),
            ]
        else:
            travaux = [
                ('Changement chauffage', '10 000 - 15 000 €', '30-35%', '+10-12%'),
                ('Remplacement fenêtres', '8 000 - 12 000 €', '15-20%', '+5-7%'),
                ('Installation ventilation', '4 000 - 7 000 €', '10-15%', '+3-5%'),
            ]
        
        for nom, cout, impact, rendement in travaux:
            story.append(Paragraph(f'<b>{nom}</b>', self.styles['TitreSousSection']))
            data = [['Coût', 'Économie d\'énergie', 'ROI'], [cout, impact, rendement]]
            t = Table(data, colWidths=[120, 120, 120])
            t.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 9),
                ('BACKGROUND', (0, 0), (-1, 0), GRIS_CLAIR),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 0.5, GRIS_MOYEN),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(t)
            story.append(Spacer(1, 10))
        
        story.append(Spacer(1, 15))
        story.append(Paragraph(
            f'<b>Budget Total Estimé: {self.cout:,} €</b>',
            self.styles['TitreSousSection']
        ))
        return story
    
    def section_contact(self):
        story = []
        story.append(PageBreak())
        story.append(Spacer(1, 80))
        story.append(Paragraph('Besoin d\'un accompagnement ?', self.styles['TitreSection']))
        story.append(Spacer(1, 10))
        story.append(Paragraph(
            'Nos experts peuvent vous aider à concrétiser votre projet de rénovation.',
            self.styles['TexteNormal']
        ))
        story.append(Spacer(1, 20))
        story.append(Paragraph('<b>Contactez-nous</b>', self.styles['TexteNormal']))
        story.append(Paragraph(' experts@thezami.com', self.styles['TexteNormal']))
        story.append(Paragraph(' +33 1 23 45 67 89', self.styles['TexteNormal']))
        story.append(Spacer(1, 30))
        story.append(Paragraph(
            '<i>Rapport préliminaire - Validation sur site recommandée</i>',
            self.styles['TexteNormal']
        ))
        return story
    
    def generer(self):
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            leftMargin=18*mm,
            rightMargin=18*mm,
            topMargin=15*mm,
            bottomMargin=15*mm,
        )
        
        elements = []
        elements.extend(self.section_resume())
        elements.append(PageBreak())
        elements.extend(self.section_bien())
        elements.append(PageBreak())
        elements.extend(self.section_travaux())
        elements.append(PageBreak())
        elements.extend(self.section_contact())
        
        doc.build(elements, onFirstPage=self.page1_couverture(), onLaterPages=lambda c, d: None)
        return self.buffer.getvalue()


def generer_rapport(donnees):
    """Génère le rapport PDF"""
    rapport = RapportZAMI(donnees)
    return rapport.generer()