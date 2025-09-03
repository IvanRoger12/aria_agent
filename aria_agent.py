import streamlit as st
import json
import time
import random
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional
import asyncio
from dataclasses import dataclass, field
import numpy as np
from fpdf import FPDF # NOUVEAU : Pour la génération de PDF

# Configuration de la page
st.set_page_page_config(
    page_title="🤖 ARIA - AI Strategic Intelligence Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS avancé avec animations et design premium (rendu plus lisible)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Background animé */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 25%, #3b82f6 50%, #1e40af 75%, #0f172a 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        color: #e2e8f0; /* Texte général plus clair pour la lisibilité */
        font-family: 'Inter', sans-serif;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Cacher les éléments par défaut de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Conteneur principal */
    .block-container {
        padding-top: 2rem;
        max-width: 1400px;
    }
    
    /* Cartes avec effet glassmorphism */
    .glass-card {
        background: rgba(255, 255, 255, 0.08); /* Légèrement plus opaque */
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.15); /* Bordure plus visible */
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4); /* Ombre plus prononcée */
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(59, 130, 246, 0.35); /* Ombre au survol plus prononcée */
        border-color: rgba(59, 130, 246, 0.6); /* Bordure au survol plus prononcée */
    }
    
    /* Avatar de l'agent avec animations */
    .agent-avatar {
        position: relative;
        width: 100px;
        height: 100px;
        margin: 20px auto;
        border-radius: 50%;
        background: conic-gradient(from 0deg, #3b82f6, #8b5cf6, #ec4899, #3b82f6);
        display: flex;
        align-items: center;
        justify-content: center;
        animation: rotate 10s linear infinite;
    }
    
    .agent-avatar.active {
        animation: rotate 2s linear infinite, pulse 1.5s ease-in-out infinite;
        box-shadow: 0 0 50px rgba(59, 130, 246, 0.8);
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    .agent-core {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(45deg, #1e40af, #3b82f6);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
    }
    
    /* Pensées avec animations */
    .thought-bubble {
        background: rgba(59, 130, 246, 0.15); /* Plus opaque */
        border-left: 4px solid #3b82f6;
        padding: 20px;
        margin-bottom: 15px;
        border-radius: 0 15px 15px 0;
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.15);
    }
    
    /* Métriques en temps réel */
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        font-family: 'Orbitron', monospace;
        color: #60a5fa;
        text-shadow: 0 0 15px rgba(96, 165, 250, 0.7); /* Ombre plus nette */
    }
    
    /* Boutons premium */
    .stButton > button {
        background: linear-gradient(45deg, #3b82f6, #8b5cf6);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        padding: 12px 30px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4); /* Ombre plus visible */
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.6); /* Ombre au survol plus visible */
        background: linear-gradient(45deg, #2563eb, #7c3aed);
    }
    
    /* Titre Premium */
    .premium-title {
        font-size: 3.5rem;
        font-weight: 900;
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(45deg, #60a5fa, #a78bfa, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: none;
        animation: titleGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes titleGlow {
        from { filter: drop-shadow(0 0 15px rgba(96, 165, 250, 0.8)); }
        to { filter: drop-shadow(0 0 30px rgba(167, 139, 250, 1)); }
    }
    
    /* Indicateur de statut */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 10px;
        animation: statusBlink 1.5s infinite;
    }
    
    .status-idle { background: #94a3b8; } /* Plus clair */
    .status-thinking { background: #f59e0b; }
    .status-analyzing { background: #3b82f6; }
    .status-completed { background: #10b981; }
    
    @keyframes statusBlink {
        0% { opacity: 1; box-shadow: 0 0 8px currentColor; }
        50% { opacity: 0.5; box-shadow: none; }
        100% { opacity: 1; box-shadow: 0 0 8px currentColor; }
    }
    
    /* Cartes d'insights */
    .insight-card {
        background: rgba(255, 255, 255, 0.1); /* Plus opaque pour le texte */
        border-radius: 15px;
        padding: 20px;
        margin: 12px 0;
        border-left: 4px solid;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .insight-card:hover {
        transform: translateY(-3px) scale(1.01);
        background: rgba(255, 255, 255, 0.15);
    }
    
    .opportunity-card { border-left-color: #10b981; }
    .threat-card { border-left-color: #ef4444; }
    .trend-card { border-left-color: #8b5cf6; }
    
    /* Recommandations stylisées */
    .recommendation-bubble {
        display: flex;
        align-items: start;
        gap: 20px;
        background: rgba(139, 92, 246, 0.15); /* Plus opaque */
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border-left: 4px solid #8b5cf6;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .recommendation-number {
        background: linear-gradient(45deg, #8b5cf6, #ec4899);
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        font-weight: bold;
        font-size: 1.2rem;
        color: white; /* Numéro en blanc */
        box-shadow: 0 0 15px rgba(139, 92, 246, 0.7);
    }

    /* Texte dans les cartes */
    .glass-card p, .insight-card p, .recommendation-bubble p {
        color: #f8fafc; /* Texte très clair pour la lisibilité */
    }
    .glass-card h2, .glass-card h3, .glass-card h4, .insight-card h5 {
        color: white; /* Titres en blanc pur */
    }

    /* Styles pour la page d'accueil avec effet machine à écrire */
    .typewriter-text {
        font-size: 2.5rem; /* Plus grand */
        font-weight: 700;
        color: white;
        min-height: 1.2em; /* Pour éviter le saut de mise en page */
    }
    .capabilities-list {
        margin-top: 30px;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 15px;
    }
    .capability-item {
        padding: 10px 18px;
        background: linear-gradient(45deg, rgba(59,130,246,0.3), rgba(139,92,246,0.3));
        border-radius: 25px;
        color: white;
        font-weight: 500;
        font-size: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }

    /* Slider Streamlit customisé */
    div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        color: white;
    }
    div[data-baseweb="select"] > div:hover {
        border-color: #3b82f6;
    }
    div[data-baseweb="select"] > div > div > span {
        color: white !important;
    }
    div[data-baseweb="slider"] {
        padding: 10px 0;
    }
    .stSlider > div > div[data-testid="stTickBar"] {
        background-color: rgba(255, 255, 255, 0.2);
    }
    .stSlider > div > div[data-testid="stTickBar"] > div {
        background-color: #3b82f6;
    }
    .stSlider > div > div[data-testid="stThumbValue"] {
        color: white;
        background-color: #3b82f6;
        border-radius: 5px;
    }
    .stSlider > div > div > div[role="slider"] {
        background-color: #8b5cf6;
        border: 2px solid white;
    }

</style>
""", unsafe_allow_html=True)


# --- Data Classes ---
@dataclass
class AgentThought:
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    
@dataclass
class MarketInsight:
    title: str
    description: str
    impact_score: float
    confidence: float
    category: str  # "opportunity", "threat", "trend"

# --- Classe de Génération PDF ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.set_text_color(255, 255, 255)
        self.set_fill_color(15, 23, 42)
        self.cell(0, 15, '🧠 RAPPORT D\'INTELLIGENCE STRATÉGIQUE - ARIA', 0, 1, 'C', True)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def section_title(self, title):
        self.add_font('Inter', '', 'Inter-Regular.ttf', uni=True) # Assurez-vous d'avoir ce fichier de police si nécessaire
        self.add_font('Inter', 'B', 'Inter-Bold.ttf', uni=True)
        self.set_font('Inter', 'B', 12)
        self.set_fill_color(30, 64, 175) # Bleu foncé
        self.set_text_color(255, 255, 255) # Blanc
        self.cell(0, 10, f' {title}', 0, 1, 'L', True)
        self.ln(4)
        self.set_text_color(0, 0, 0) # Texte noir pour le corps

    def section_body(self, body):
        self.set_font('Inter', '', 10)
        # IMPORTANT: Utilisation de 'utf-8' et gestion des erreurs pour FPDF
        self.multi_cell(0, 5, body.encode('utf-8', 'replace').decode('utf-8'))
        self.ln()

    def insight_card(self, insight: MarketInsight):
        self.set_font('Inter', 'B', 10)
        self.cell(0, 5, f"{insight.title} ({insight.category.capitalize()})", 0, 1)
        self.set_font('Inter', '', 9)
        self.multi_cell(0, 5, insight.description.encode('utf-8', 'replace').decode('utf-8'))
        self.set_font('Inter', 'I', 9)
        self.cell(0, 5, f"Impact: {insight.impact_score}/10 | Confiance: {insight.confidence}%", 0, 1)
        self.ln(2)

# --- ARIA Agent Class ---
class ARIAAgent:
    def __init__(self, language: str = "fr"):
        self.language = language
        self.status = "idle"  # idle, thinking, analyzing, completed
        self.thoughts: List[AgentThought] = []
        self.current_analysis: Optional[Dict] = None
        self.confidence_level: float = 0.0
        self.neural_activity: int = 850
        self.activity_history: List[int] = []
        
        self.translations = {
            "fr": {
                "agent_name": "ARIA",
                "agent_desc": "Agent de Recherche et Intelligence Autonome",
                "status_idle": "En veille - Prêt pour l'analyse",
                "status_thinking": "Réflexion stratégique...",
                "status_analyzing": "Analyse multi-dimensionnelle...",
                "status_completed": "Analyse terminée",
                "sectors": {
                    "FinTech": "🏦 Technologies Financières",
                    "HealthTech": "❤️ Technologies de la Santé",
                    "SaaS": "☁️ Logiciels en tant que Service",
                    "E-commerce": "🛒 Commerce Électronique",
                    "PropTech": "🏠 Technologies Immobilières",
                    "EdTech": "🎓 Technologies de l'Éducation"
                },
                "thoughts": [
                    "Initialisation des capteurs de marché...",
                    "Activation des réseaux neuronaux sectoriels...",
                    "Ingestion de 1,2 Go de données temps réel...",
                    "Traitement par algorithmes de deep learning...",
                    "Corrélation des signaux faibles détectés...",
                    "Modélisation prédictive des tendances...",
                    "Génération d'insights actionnables...",
                    "Synthèse stratégique finale..."
                ]
            }
            # Version anglaise omise pour la concision (peut être ajoutée si besoin)
        }
        self.market_data = self._generate_all_sector_data()

    def get_translation(self, key: str) -> str:
        return self.translations[self.language].get(key, key)

    def _generate_sector_data(self, sector_key: str) -> Dict:
        """Génère des données d'analyse fictives pour un secteur."""
        sector_display_name = self.get_translation("sectors")[sector_key]
        
        # Templates for dynamic data generation
        summary = f"Le secteur {sector_display_name} est en pleine mutation, tiré par l'IA générative et une demande accrue pour des solutions hyper-personnalisées. La consolidation du marché s'accélère."
        opportunities = [
            MarketInsight(f"IA dans {sector_key}", f"L'intégration de l'IA pourrait débloquer un marché de {random.uniform(1.5, 5.0):.1f}B€ d'ici 2028.", 9.2, 88, "opportunity"),
            MarketInsight("Solutions Durables", "La demande pour des options écologiques et responsables crée une nouvelle niche de marché en croissance rapide.", 8.5, 75, "opportunity")
        ]
        threats = [
            MarketInsight("Régulation Accrue", "De nouvelles lois de protection des données et de l'environnement pourraient augmenter les coûts de conformité de 20% sur 3 ans.", 7.8, 91, "threat"),
            MarketInsight("Concurrence Féroce", "L'entrée de nouveaux acteurs perturbateurs exerce une pression constante sur les marges.", 7.0, 80, "threat")
        ]
        trends = [
            MarketInsight("Hyper-personnalisation", "Les clients exigent des expériences sur mesure, poussant les entreprises à innover dans la gestion de la relation client.", 8.9, 84, "trend"),
            MarketInsight("Blockchain & Web3", "L'adoption progressive de la blockchain pourrait transformer les infrastructures sous-jacentes du secteur.", 6.5, 60, "trend")
        ]
        recommendations = [
            f"Investir massivement dans une plateforme d'IA générative pour automatiser les processus clés avant le T3 2026.",
            f"Lancer un audit complet de conformité réglementaire et anticiper les futures législations ESG (Environnemental, Social, Gouvernance).",
            f"Développer un pilote de solution durable ou un programme RSE (Responsabilité Sociale des Entreprises) pour capter la demande croissante.",
            f"Renforcer la veille concurrentielle et envisager des partenariats stratégiques pour maintenir l'avantage sur le marché."
        ]
        
        # NOUVEAU : Métriques et informations enrichies pour les secteurs
        key_metrics = {
            "Taux d'Adoption": f"{random.randint(15, 40)}%",
            "Croissance Annuelle (YoY)": f"+{random.randint(5, 25)}%",
            "Panier Moyen": f"{random.randint(100, 500)}€" if "Commerce" in sector_display_name else f"{random.randint(50, 200)}€",
        }
        key_players = [f"Géant {random.choice(['Tech', 'Fin', 'Health'])}", f"Startup Innovante {random.randint(1, 10)}", f"Acteur Historique {random.choice(['X', 'Y', 'Z'])}"]
        investment_trend = random.choice(["En forte hausse (Capital Risque très actif)", "Stable (Investissements modérés)", "Hausse modérée (Focus sur la rentabilité)"])


        return {
            "summary": summary,
            "insights": opportunities + threats + trends,
            "recommendations": recommendations,
            "key_metrics": key_metrics,
            "key_players": key_players,
            "investment_trend": investment_trend
        }
        
    def _generate_all_sector_data(self) -> Dict:
        """Génère des données pour tous les secteurs dans toutes les langues."""
        all_data = {}
        sectors = self.get_translation("sectors").keys()
        for sector_key in sectors:
            all_data[sector_key] = self._generate_sector_data(sector_key)
        return all_data

    def reset(self):
        """Réinitialise l'agent à son état initial."""
        self.status = "idle"
        self.thoughts = []
        self.current_analysis = None
        self.confidence_level = 0.0
        self.neural_activity = 850
        self.activity_history = []
        st.session_state.chat_messages = []


    def generate_confidence_gauge(self) -> go.Figure:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=self.confidence_level,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Niveau de Confiance", 'font': {'color': 'white', 'size': 18}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "#3b82f6", 'thickness': 0.8},
                'bgcolor': "rgba(0,0,0,0.1)",
                'borderwidth': 2,
                'bordercolor': "rgba(255, 255, 255, 0.1)",
                'steps': [
                    {'range': [0, 60], 'color': 'rgba(239, 68, 68, 0.3)'},
                    {'range': [60, 85], 'color': 'rgba(245, 158, 11, 0.3)'},
                    {'range': [85, 100], 'color': 'rgba(16, 185, 129, 0.3)'}],
            }))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"}, height=250, margin=dict(t=40, b=20))
        return fig

    def generate_activity_chart(self) -> go.Figure:
        """Génère un graphique de l'activité neuronale au fil du temps."""
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(len(self.activity_history))), 
            y=self.activity_history,
            mode='lines+markers',
            line=dict(color='#3b82f6', width=3, shape='spline'),
            marker=dict(size=5),
            fill='tozeroy',
            fillcolor='rgba(59, 130, 246, 0.2)'
        ))
        fig.update_layout(
            title={'text': "Activité Neuronale", 'font': {'color': 'white', 'size': 18}},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "white"},
            height=250,
            margin=dict(t=40, b=20),
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.1)')
        )
        return fig

    def generate_swot_chart(self) -> go.Figure:
        insights = self.current_analysis.get("insights", [])
        
        # Simplified for visualization, focusing on opportunities and threats based on impact and confidence
        opps = [(i.impact_score, i.confidence, f"💡 {i.title}") for i in insights if i.category == "opportunity"]
        thrs = [(i.impact_score, i.confidence, f"🚨 {i.title}") for i in insights if i.category == "threat"]

        fig = go.Figure()

        if opps:
            fig.add_trace(go.Scatter(
                x=[o[0] for o in opps], y=[o[1] for o in opps],
                mode='markers+text', text=[o[2] for o in opps],
                marker=dict(color='#10b981', size=15, symbol='circle', line=dict(width=1, color='white')), name='Opportunités',
                textposition="top center"
            ))
        if thrs:
            fig.add_trace(go.Scatter(
                x=[t[0] for t in thrs], y=[t[1] for t in thrs],
                mode='markers+text', text=[t[2] for t in thrs],
                marker=dict(color='#ef4444', size=15, symbol='diamond', line=dict(width=1, color='white')), name='Menaces',
                textposition="bottom center"
            ))

        fig.update_layout(
            title={'text': "Matrice Stratégique (Impact / Confiance)", 'font': {'color': 'white', 'size': 18}},
            xaxis_title="Impact Stratégique (0-10)", yaxis_title="Confiance de l'IA (%)",
            xaxis=dict(range=[0, 10], showgrid=True, gridcolor='rgba(255,255,255,0.1)', title_font=dict(color='white'), tickfont=dict(color='white')),
            yaxis=dict(range=[0, 100], showgrid=True, gridcolor='rgba(255,255,255,0.1)', title_font=dict(color='white'), tickfont=dict(color='white')),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0.1)",
            font={'color': "white"}, legend_title_text='Catégories',
            legend=dict(font=dict(color='white'))
        )
        return fig

    def chat_with_agent(self, message: str, sector_display_name: str) -> str:
        """Chat amélioré avec l'agent."""
        message = message.lower()
        insights = self.current_analysis.get("insights", [])
        
        if any(keyword in message for keyword in ["opportunit", "opportunity"]):
            opps = [i for i in insights if i.category == "opportunity"]
            if opps:
                return f"J'ai identifié {len(opps)} opportunités clés. Par exemple, l'intégration de l'IA dans votre secteur est une opportunité majeure : '{opps[0].title}' - '{opps[0].description}'."
            else:
                return "Je n'ai pas trouvé d'opportunités spécifiques dans cette analyse, mais je peux chercher plus en profondeur."
        
        if any(keyword in message for keyword in ["menace", "threat", "risk"]):
            thrs = [i for i in insights if i.category == "threat"]
            if thrs:
                return f"Oui, la menace principale est liée à la '{thrs[0].title}': '{thrs[0].description}'. Il est crucial d'y prêter attention."
            else:
                return "Je n'ai pas trouvé de menaces spécifiques dans cette analyse. Le secteur semble stable pour l'instant."
        
        if any(keyword in message for keyword in ["tendance", "trend"]):
            trnds = [i for i in insights if i.category == "trend"]
            if trnds:
                return f"Une tendance majeure est l''{trnds[0].title}': '{trnds[0].description}'. Il est essentiel de s'y adapter."
            else:
                return "Je n'ai pas identifié de tendances distinctes dans cette analyse. Peut-être est-ce un secteur plus mature."
            
        return f"Dans le secteur {sector_display_name}, mon analyse a souligné l'importance de l'innovation et de l'adaptation. Puis-je vous aider avec des questions spécifiques sur les opportunités, les menaces ou les tendances ?"

    # NOUVEAU: Fonction pour générer le rapport PDF
    def generate_pdf_report(self, sector_key: str) -> bytes:
        pdf = PDF()
        # Il peut être nécessaire d'inclure des fichiers de police .ttf si des caractères spéciaux sont utilisés
        # exemple: pdf.add_font('DejaVuSans', '', 'DejaVuSans.ttf', uni=True)
        # pdf.add_font('DejaVuSans', 'B', 'DejaVuSans-Bold.ttf', uni=True)
        
        pdf.add_page()
        
        # En-tête du rapport
        pdf.set_font('Arial', '', 11)
        pdf.set_text_color(0, 0, 0) # Texte noir pour le PDF
        sector_display_name = self.get_translation("sectors")[sector_key]
        pdf.cell(0, 6, f"Secteur Analysé : {sector_display_name}", 0, 1)
        pdf.cell(0, 6, f"Date du Rapport : {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1)
        pdf.cell(0, 6, f"Niveau de Confiance Global : {self.confidence_level:.1f}%", 0, 1)
        pdf.ln(10)

        # Sections
        analysis = self.current_analysis
        
        pdf.section_title("Synthèse Stratégique")
        pdf.section_body(analysis["summary"])

        pdf.section_title("Insights Clés")
        for insight in analysis["insights"]:
            pdf.insight_card(insight)

        pdf.section_title("Recommandations Stratégiques")
        for i, rec in enumerate(analysis["recommendations"], 1):
            pdf.section_body(f"{i}. {rec}")
        
        pdf.section_title("Métriques et Contexte du Marché")
        metrics_body = (
            f"Tendance d'Investissement VC : {analysis['investment_trend']}\n"
            f"Acteurs Majeurs : {', '.join(analysis['key_players'])}\n"
            f"KPIs Notables : " + ", ".join([f"{k}: {v}" for k,v in analysis['key_metrics'].items()])
        )
        pdf.section_body(metrics_body)

        return pdf.output(dest='S').encode('latin-1') # Encodage 'latin-1' est souvent plus sûr pour FPDF standard

# --- Interface Principale ---
def main():
    # Initialisation de l'état de session
    if 'agent' not in st.session_state:
        st.session_state.agent = ARIAAgent()
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    if 'running_analysis' not in st.session_state:
        st.session_state.running_analysis = False
    if 'analysis_speed' not in st.session_state:
        st.session_state.analysis_speed = 1.0


    agent = st.session_state.agent

    # --- Header ---
    with st.container():
        st.markdown(f"""
        <div style='text-align: center; margin-bottom: 30px;'>
            <h1 class='premium-title'>ARIA</h1>
            <p style='color: #cbd5e1; font-size: 1.3rem;'>{agent.get_translation('agent_desc')}</p>
        </div>
        """, unsafe_allow_html=True)

    # --- Layout Principal ---
    col1, col2 = st.columns([0.35, 0.65])

    # --- COLONNE 1 : Contrôle de l'Agent ---
    with col1:
        with st.container():
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            
            # Avatar et Statut
            avatar_class = "agent-avatar active" if agent.status != "idle" else "agent-avatar"
            st.markdown(f"""
            <div style='text-align: center; margin-bottom: 25px;'>
                <div class='{avatar_class}'><div class='agent-core'>🧠</div></div>
                <div>
                    <span class='status-indicator status-{agent.status}'></span>
                    <span style='color: white; font-weight: 500;'>{agent.get_translation(f"status_{agent.status}")}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Sélecteur de secteur
            st.markdown(f"<h4 style='color: white; text-align: center;'>🎯 Secteur d'Analyse</h4>", unsafe_allow_html=True)
            sectors = agent.get_translation("sectors")
            selected_sector_key = st.selectbox(
                "Select sector", list(sectors.keys()),
                format_func=lambda x: sectors[x],
                label_visibility="collapsed"
            )
            selected_sector_display_name = sectors[selected_sector_key] # Nom affichable

            # NOUVEAU : Slider de profondeur d'analyse
            depth_map = {"Rapide": 0.5, "Normale": 1.0, "Profonde": 1.5}
            depth_choice = st.select_slider(
                "⚙️ Profondeur d'Analyse", 
                options=list(depth_map.keys()), 
                value="Normale",
                help="Détermine le temps de l'analyse et la 'profondeur' simulée des résultats."
            )
            analysis_speed = depth_map[depth_choice]


            # Bouton d'activation
            st.markdown("<br>", unsafe_allow_html=True)
            if agent.status in ["idle", "completed"]:
                if st.button("🚀 ACTIVER ARIA", type="primary"):
                    st.session_state.running_analysis = True
                    st.session_state.analysis_speed = analysis_speed # Stocker la vitesse
                    agent.reset()
                    agent.status = "thinking"
                    st.rerun()
            else:
                if st.button("⏹️ STOPPER L'AGENT"):
                    st.session_state.running_analysis = False
                    agent.reset()
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Affichage des métriques et graphiques PENDANT l'analyse
        if agent.status not in ["idle"]:
            with st.container():
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                m_col1, m_col2 = st.columns(2)
                with m_col1:
                    st.markdown(f"<div style='text-align:center'><div class='metric-value'>{agent.neural_activity}</div><div style='color: #94a3b8;'>Noeuds</div></div>", unsafe_allow_html=True)
                with m_col2:
                    st.markdown(f"<div style='text-align:center'><div class='metric-value'>{agent.confidence_level:.1f}%</div><div style='color: #94a3b8;'>Confiance</div></div>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        if agent.status == "completed":
            st.plotly_chart(agent.generate_confidence_gauge(), use_container_width=True)
            st.plotly_chart(agent.generate_activity_chart(), use_container_width=True)

            # NOUVEAU: Bouton de téléchargement PDF
            with st.container():
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown('<h4 style="color: white; text-align: center;">📥 Export du Rapport</h4>', unsafe_allow_html=True)
                pdf_bytes = agent.generate_pdf_report(selected_sector_key)
                st.download_button(
                    label="📄 Télécharger le Rapport PDF",
                    data=pdf_bytes,
                    file_name=f"Rapport_ARIA_{selected_sector_key}_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                st.markdown('</div>', unsafe_allow_html=True)


    # --- COLONNE 2 : Affichage des Résultats ---
    with col2:
        # Placeholder pour les pensées et résultats
        results_placeholder = st.empty()

        if st.session_state.get("running_analysis", False):
            # --- SIMULATION DE L'ANALYSE EN DIRECT ---
            thoughts = agent.get_translation("thoughts")
            agent.thoughts = []
            agent.activity_history = [agent.neural_activity]
            
            thoughts_html = '<div class="glass-card">'
            thoughts_html += '<h3 style="color: white;">🧠 Pensées de l\'Agent</h3>'
            
            for i, thought_text in enumerate(thoughts):
                time.sleep(random.uniform(0.6, 1.2) * st.session_state.analysis_speed) # Utilise la vitesse du slider
                
                # Mise à jour du statut
                if i >= 2 and agent.status == "thinking":
                    agent.status = "analyzing"
                
                # Mise à jour des métriques
                agent.neural_activity += random.randint(-40, 60)
                agent.activity_history.append(agent.neural_activity)
                agent.confidence_level = (i + 1) / len(thoughts) * 80 + random.uniform(-5, 5) # Petites variations
                if agent.confidence_level > 100: agent.confidence_level = 100
                if agent.confidence_level < 0: agent.confidence_level = 0
                
                # Ajout de la pensée
                thought = AgentThought(content=thought_text)
                agent.thoughts.append(thought)
                
                # Mise à jour de l'affichage
                thought_item_html = f"""
                <div class='thought-bubble' style='animation: fadeInUp 0.5s ease-out backwards;'>
                    <div style='display: flex; align-items: center; gap: 15px;'>
                        <div style='font-size: 1.5rem;'>{random.choice(['🔍', '🧠', '📊', '⚡', '🎯', '📈', '🤖', '✨'])}</div>
                        <div>
                            <p style='color: white; margin: 0;'>{thought.content}</p>
                            <span style='color: #94a3b8; font-size: 0.75rem;'>{thought.timestamp.strftime("%H:%M:%S")}</span>
                        </div>
                    </div>
                </div>"""
                thoughts_html += thought_item_html
                
                with results_placeholder.container():
                    st.markdown(thoughts_html + '</div>', unsafe_allow_html=True)
            
            # Finalisation de l'analyse
            agent.status = "completed"
            agent.confidence_level = random.uniform(88, 97)
            agent.current_analysis = agent.market_data.get(selected_sector_key, {})
            st.session_state.running_analysis = False
            st.rerun()

        elif agent.status == "completed" and agent.current_analysis:
            # --- AFFICHAGE DES RÉSULTATS FINAUX ---
            with results_placeholder.container():
                st.markdown(f"""
                <div class='glass-card' style='animation: fadeInUp 0.5s ease-out;'>
                    <h3 style='color: white;'>📋 Synthèse Stratégique</h3>
                    <p style='color: #f8fafc; font-size: 1.1rem;'>{agent.current_analysis.get("summary", "")}</p>
                </div>
                """, unsafe_allow_html=True)

                # NOUVEAU: Affichage des métriques enrichies
                st.markdown("<div class='glass-card' style='animation: fadeInUp 0.6s ease-out;'><h3>📊 Contexte du Marché</h3></div>", unsafe_allow_html=True)
                m_cols = st.columns(3)
                with m_cols[0]:
                    st.metric("📈 Tendance Invest. VC", agent.current_analysis.get('investment_trend'))
                
                # Utilisation d'un itérateur sûr pour les métriques
                current_metrics = list(agent.current_analysis.get('key_metrics', {}).items())
                if len(current_metrics) > 0:
                     with m_cols[1]:
                        st.metric(f"🔑 {current_metrics[0][0]}", current_metrics[0][1])
                if len(current_metrics) > 1:
                     with m_cols[2]:
                        st.metric(f"🔑 {current_metrics[1][0]}", current_metrics[1][1])

                st.markdown(f"<p style='color: #f8fafc;'>**Acteurs Majeurs:** {', '.join(agent.current_analysis.get('key_players', []))}</p>", unsafe_allow_html=True)

                # NOUVEAU : Matrice SWOT
                st.plotly_chart(agent.generate_swot_chart(), use_container_width=True)

                st.markdown('<div class="glass-card"><h3 style="color: white;">⚡ Insights Clés</h3></div>', unsafe_allow_html=True)
                
                insights = agent.current_analysis.get("insights", [])
                for i, insight in enumerate(insights):
                    icon = {"opportunity": "💡", "threat": "🚨", "trend": "📊"}.get(insight.category, "🔹")
                    st.markdown(f"""
                    <div class='insight-card {insight.category}-card' style='animation: fadeInUp {0.6 + i*0.1}s ease-out backwards;'>
                        <h5 style='color: white; margin-bottom: 10px;'>{icon} {insight.title}</h5>
                        <p style='color: #f8fafc; margin-bottom: 12px;'>{insight.description}</p>
                        <div style='display: flex; gap: 10px; font-size: 0.8rem; color: #cbd5e1;'>
                            <span><b>Impact:</b> {insight.impact_score}/10</span>
                            <span><b>Confiance:</b> {insight.confidence}%</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('<div class="glass-card"><h3 style="color: white;">🎯 Recommandations IA</h3></div>', unsafe_allow_html=True)
                recommendations = agent.current_analysis.get("recommendations", [])
                for i, rec in enumerate(recommendations):
                    st.markdown(f"""
                    <div class='recommendation-bubble' style='animation: fadeInUp {0.8 + i*0.15}s ease-out backwards;'>
                        <div class='recommendation-number'>{i+1}</div>
                        <p style='color: #f8fafc; margin: auto 0;'>{rec}</p>
                    </div>
                    """, unsafe_allow_html=True)

                # --- Section Chat ---
                st.markdown('<div class="glass-card"><h3 style="color: white;">💬 Discuter avec ARIA</h3></div>', unsafe_allow_html=True)
                for msg in st.session_state.chat_messages[-3:]: # Afficher les 3 derniers messages
                    st.chat_message(msg["role"]).write(msg["content"])
                
                if user_question := st.chat_input("Posez votre question..."):
                    st.session_state.chat_messages.append({"role": "user", "content": user_question})
                    st.chat_message("user").write(user_question)
                    
                    response = agent.chat_with_agent(user_question, selected_sector_display_name)
                    st.session_state.chat_messages.append({"role": "assistant", "content": response})
                    st.chat_message("assistant").write(response)

        else:
            # --- Écran d'accueil Dynamique et "Waouh" ---
            with results_placeholder.container():
                st.markdown("""
                <div class='glass-card' style='text-align: center; padding: 40px;'>
                    <div style='font-size: 4rem; margin-bottom: 20px;'>🤖</div>
                """, unsafe_allow_html=True)
                
                title_placeholder = st.empty()
                subtitle_placeholder = st.empty()
                
                title_text = "ARIA est prête à analyser le marché."
                displayed_text = ""
                for char in title_text:
                    displayed_text += char
                    title_placeholder.markdown(f"<h2 class='typewriter-text'>{displayed_text}</h2>", unsafe_allow_html=True)
                    time.sleep(0.04)
                
                subtitle_placeholder.markdown("<p style='color: #cbd5e1;'>Sélectionnez un secteur et configurez la profondeur de l'analyse pour démarrer une exploration stratégique.</p>", unsafe_allow_html=True)
                
                st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 25px 0;'>", unsafe_allow_html=True)
                
                capabilities = ["🔍 Intelligence de Marché en Temps Réel", "⚡ Analyse Prédictive Avancée", "🎯 Identification d'Opportunités", "📊 Visualisation de Données Stratégiques", "📝 Rapports Stratégiques Exportables"]
                cap_placeholder = st.empty()
                
                caps_html = "<div class='capabilities-list'>"
                for i in range(len(capabilities) + 1):
                    if i > 0:
                        caps_html += f"<div class='capability-item' style='animation: fadeInUp 0.5s ease-out backwards; animation-delay: {i*0.1}s;'>{capabilities[i-1]}</div>"
                    cap_placeholder.markdown(caps_html + "</div>", unsafe_allow_html=True)
                    time.sleep(0.5)

                st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
