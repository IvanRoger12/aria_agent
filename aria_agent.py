import streamlit as st
import json
import time
import random
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional
import asyncio
import requests
from dataclasses import dataclass
import base64
from io import BytesIO
import numpy as np
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="🤖 ARIA - AI Strategic Intelligence Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS avancé avec animations et design premium
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Background animé */
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 25%, #3b82f6 50%, #1e40af 75%, #0f172a 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        color: white;
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 25%, #3b82f6 50%, #1e40af 75%, #0f172a 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Conteneur principal */
    .block-container {
        background: transparent;
        padding-top: 2rem;
        max-width: 1400px;
    }
    
    /* Cards avec glassmorphism */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(59, 130, 246, 0.2);
        border-color: rgba(59, 130, 246, 0.3);
    }
    
    /* Agent avatar avec animations */
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
        position: relative;
    }
    
    /* Pensées avec animations slide-in */
    .thought-bubble {
        background: rgba(59, 130, 246, 0.1);
        border-left: 4px solid #3b82f6;
        padding: 20px;
        margin: 15px 0;
        border-radius: 0 15px 15px 0;
        animation: slideInFromLeft 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        opacity: 0;
        animation-fill-mode: forwards;
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.2);
    }
    
    @keyframes slideInFromLeft {
        0% {
            transform: translateX(-100px);
            opacity: 0;
        }
        100% {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    /* Métriques en temps réel */
    .metric-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        font-family: 'Orbitron', monospace;
        color: #60a5fa;
        text-shadow: 0 0 10px rgba(96, 165, 250, 0.5);
    }
    
    /* Boutons premium */
    .stButton > button {
        background: linear-gradient(45deg, #3b82f6, #8b5cf6);
        color: white;
        border: none;
        border-radius: 15px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        padding: 12px 30px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.4);
        background: linear-gradient(45deg, #2563eb, #7c3aed);
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.08);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    /* Header premium */
    .premium-header {
        text-align: center;
        padding: 40px 0;
        margin-bottom: 30px;
    }
    
    .premium-title {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(45deg, #60a5fa, #a78bfa, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 15px;
        text-shadow: none;
        animation: titleGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes titleGlow {
        from { filter: drop-shadow(0 0 20px rgba(96, 165, 250, 0.5)); }
        to { filter: drop-shadow(0 0 40px rgba(167, 139, 250, 0.8)); }
    }
    
    .premium-subtitle {
        font-size: 1.3rem;
        color: #cbd5e1;
        font-weight: 300;
        margin-bottom: 20px;
    }
    
    /* Status indicator premium */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 10px;
        animation: statusBlink 2s infinite;
    }
    
    .status-idle { background: #6b7280; }
    .status-thinking { background: #f59e0b; }
    .status-analyzing { background: #3b82f6; }
    .status-completed { background: #10b981; }
    
    @keyframes statusBlink {
        0%, 50% { opacity: 1; box-shadow: 0 0 10px currentColor; }
        51%, 100% { opacity: 0.4; box-shadow: none; }
    }
    
    /* Insights cards avec fade-in */
    .insight-card {
        background: rgba(255, 255, 255, 0.06);
        border-radius: 15px;
        padding: 20px;
        margin: 12px 0;
        border-left: 4px solid;
        animation: fadeInUp 0.6s ease-out;
        animation-fill-mode: backwards;
        transition: all 0.3s ease;
    }
    
    .insight-card:hover {
        transform: translateY(-3px);
        background: rgba(255, 255, 255, 0.1);
    }
    
    .opportunity-card {
        border-left-color: #10b981;
        box-shadow: 0 5px 15px rgba(16, 185, 129, 0.2);
    }
    
    .threat-card {
        border-left-color: #ef4444;
        box-shadow: 0 5px 15px rgba(239, 68, 68, 0.2);
    }
    
    .trend-card {
        border-left-color: #8b5cf6;
        box-shadow: 0 5px 15px rgba(139, 92, 246, 0.2);
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Chat container */
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 15px;
        scrollbar-width: thin;
        scrollbar-color: rgba(59, 130, 246, 0.5) transparent;
    }
    
    .chat-message {
        background: rgba(59, 130, 246, 0.1);
        padding: 12px 15px;
        border-radius: 18px;
        margin: 8px 0;
        animation: messageSlide 0.5s ease-out;
    }
    
    @keyframes messageSlide {
        from {
            transform: translateX(-20px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    /* Footer premium */
    .premium-footer {
        background: rgba(0, 0, 0, 0.3);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding: 30px 0;
        text-align: center;
        margin-top: 60px;
        backdrop-filter: blur(10px);
    }
    
    /* Particle animation */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    
    .particle {
        position: absolute;
        background: rgba(59, 130, 246, 0.3);
        border-radius: 50%;
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0.3; }
        50% { transform: translateY(-20px) rotate(180deg); opacity: 0.6; }
    }
</style>
""", unsafe_allow_html=True)

@dataclass
class AgentThought:
    content: str
    timestamp: datetime
    thought_type: str = "analysis"
    confidence: float = 0.0

@dataclass
class MarketInsight:
    title: str
    description: str
    impact_score: float
    confidence: float
    category: str

class ARIAAgent:
    """ARIA - Autonomous Research & Intelligence Agent Premium"""
    
    def __init__(self, language: str = "fr"):
        self.language = language
        self.status = "idle"
        self.thoughts = []
        self.current_analysis = None
        self.confidence_level = 0.0
        self.neural_activity = 850
        self.chat_history = []
        
        self.translations = {
            "fr": {
                "agent_name": "ARIA",
                "agent_desc": "Agent de Recherche et Intelligence Autonome",
                "status_idle": "🤖 Agent en veille - Prêt à analyser",
                "status_thinking": "🧠 Réflexion stratégique en cours...",
                "status_analyzing": "⚡ Analyse multi-dimensionnelle active", 
                "status_completed": "✨ Mission accomplie - Insights générés",
                "sectors": {
                    "FinTech": "Technologies Financières",
                    "HealthTech": "Technologies Médicales",
                    "SaaS": "Logiciels en Service",
                    "E-commerce": "Commerce Électronique",
                    "PropTech": "Technologies Immobilières",
                    "EdTech": "Technologies Éducatives",
                    "GreenTech": "Technologies Vertes",
                    "SpaceTech": "Technologies Spatiales",
                    "AI/ML": "Intelligence Artificielle"
                },
                "thoughts": [
                    "🔍 Initialisation des capteurs de marché...",
                    "🧠 Activation des réseaux neuronaux sectoriels...",
                    "📊 Ingestion de 847 sources de données temps réel...",
                    "⚡ Traitement par algorithmes de deep learning...",
                    "🎯 Corrélation des signaux faibles détectés...",
                    "📈 Modélisation prédictive des tendances...",
                    "🤖 Génération d'insights actionnables...",
                    "✨ Synthèse stratégique finalisée"
                ]
            },
            "en": {
                "agent_name": "ARIA",
                "agent_desc": "Autonomous Research & Intelligence Agent",
                "status_idle": "🤖 Agent on standby - Ready to analyze",
                "status_thinking": "🧠 Strategic thinking in progress...",
                "status_analyzing": "⚡ Multi-dimensional analysis active",
                "status_completed": "✨ Mission accomplished - Insights generated",
                "sectors": {
                    "FinTech": "Financial Technologies",
                    "HealthTech": "Health Technologies", 
                    "SaaS": "Software as a Service",
                    "E-commerce": "Electronic Commerce",
                    "PropTech": "Property Technologies",
                    "EdTech": "Education Technologies",
                    "GreenTech": "Green Technologies",
                    "SpaceTech": "Space Technologies",
                    "AI/ML": "Artificial Intelligence"
                },
                "thoughts": [
                    "🔍 Initializing market sensors...",
                    "🧠 Activating sectoral neural networks...",
                    "📊 Ingesting 847 real-time data sources...",
                    "⚡ Processing via deep learning algorithms...",
                    "🎯 Correlating detected weak signals...",
                    "📈 Predictive modeling of trends...",
                    "🤖 Generating actionable insights...",
                    "✨ Strategic synthesis completed"
                ]
            }
        }
        
        # Données d'analyse enrichies pour TOUS les secteurs
        self.market_data = {
            "FinTech": {
                "fr": {
                    "summary": "EdTech transforms education with adaptive AI, immersive reality, and personalized learning. European market at €24.5B post-pandemic.",
                    "insights": [
                        MarketInsight("Adaptive Pedagogical AI", "AI adaptive learning systems improve results by +43%", 9.4, 89, "opportunity"),
                        MarketInsight("Educational Metaverse", "Virtual campuses and immersive learning, 67% university adoption", 8.7, 84, "trend"),
                        MarketInsight("Mobile Micro-Learning", "Short mobile training explodes, +234% engagement", 8.3, 88, "opportunity"),
                        MarketInsight("Digital Divide", "Inequalities in access to educational technologies intensifying", 7.1, 85, "threat")
                    ],
                    "recommendations": [
                        "Create personalized pedagogical AI systems",
                        "Develop immersive learning experiences",
                        "Design mobile micro-learning solutions"
                    ]
                }
            },
            "GreenTech": {
                "fr": {
                    "summary": "GreenTech accélère avec 47B€ d'investissements UE. IA optimise l'énergie, blockchain trace carbone, IoT surveille environnement.",
                    "insights": [
                        MarketInsight("IA Efficacité Énergétique", "Optimisation IA réduit consommation énergétique de 35% dans l'industrie", 9.6, 92, "opportunity"),
                        MarketInsight("Carbon Tracking Blockchain", "Traçabilité carbone blockchain obligatoire, marché 1.8B€", 8.5, 86, "opportunity"),
                        MarketInsight("Smart Grid Revolution", "Réseaux électriques intelligents, déploiement massif prévu 2025-2027", 8.9, 88, "trend"),
                        MarketInsight("Greenwashing Regulations", "Durcissement des règles anti-greenwashing, risques de sanctions", 7.4, 90, "threat")
                    ],
                    "recommendations": [
                        "Développer solutions IA d'optimisation énergétique",
                        "Créer plateformes de traçabilité carbone blockchain",
                        "Investir dans technologies smart grid"
                    ]
                },
                "en": {
                    "summary": "GreenTech accelerating with €47B EU investments. AI optimizes energy, blockchain tracks carbon, IoT monitors environment.",
                    "insights": [
                        MarketInsight("AI Energy Efficiency", "AI optimization reduces industrial energy consumption by 35%", 9.6, 92, "opportunity"),
                        MarketInsight("Carbon Tracking Blockchain", "Blockchain carbon traceability becoming mandatory, €1.8B market", 8.5, 86, "opportunity"),
                        MarketInsight("Smart Grid Revolution", "Intelligent power grids, massive deployment planned 2025-2027", 8.9, 88, "trend"),
                        MarketInsight("Anti-Greenwashing Rules", "Tightening anti-greenwashing regulations, sanction risks", 7.4, 90, "threat")
                    ],
                    "recommendations": [
                        "Develop AI energy optimization solutions",
                        "Create blockchain carbon traceability platforms",
                        "Invest in smart grid technologies"
                    ]
                }
            },
            "SpaceTech": {
                "fr": {
                    "summary": "SpaceTech explose avec NewSpace européen 8.3B€. Satellites miniaturisés, tourisme spatial, mining astéroïdes émergent.",
                    "insights": [
                        MarketInsight("Constellations Satellites", "Satellites miniaturisés pour Internet global, marché 12B€ d'ici 2028", 9.2, 85, "opportunity"),
                        MarketInsight("Tourisme Spatial Commercial", "Vol suborbital commercial accessible, 150M€ de revenus prévus", 8.1, 78, "opportunity"),
                        MarketInsight("Space Mining Prep", "Préparation extraction astéroïdes, investissements R&D massifs", 7.8, 65, "trend"),
                        MarketInsight("Débris Spatiaux", "Pollution orbitale croissante menace missions spatiales", 8.3, 89, "threat")
                    ],
                    "recommendations": [
                        "Investir dans technologies satellites miniaturisés",
                        "Développer solutions nettoyage débris spatiaux",
                        "Préparer participation économie spatiale"
                    ]
                },
                "en": {
                    "summary": "SpaceTech exploding with European NewSpace at €8.3B. Miniaturized satellites, space tourism, asteroid mining emerging.",
                    "insights": [
                        MarketInsight("Satellite Constellations", "Miniaturized satellites for global Internet, €12B market by 2028", 9.2, 85, "opportunity"),
                        MarketInsight("Commercial Space Tourism", "Commercial suborbital flights accessible, €150M revenue projected", 8.1, 78, "opportunity"),
                        MarketInsight("Space Mining Preparation", "Asteroid mining preparation, massive R&D investments", 7.8, 65, "trend"),
                        MarketInsight("Space Debris Crisis", "Growing orbital pollution threatens space missions", 8.3, 89, "threat")
                    ],
                    "recommendations": [
                        "Invest in miniaturized satellite technologies",
                        "Develop space debris cleanup solutions",
                        "Prepare for space economy participation"
                    ]
                }
            },
            "AI/ML": {
                "fr": {
                    "summary": "IA/ML dominent avec 156B€ marché européen. AGI approche, IA générative intégrée partout, compute quantique émerge.",
                    "insights": [
                        MarketInsight("IA Générative Enterprise", "Intégration IA générative en entreprise génère +67% productivité", 9.8, 94, "opportunity"),
                        MarketInsight("AGI Timeline Acceleration", "Progression vers AGI s'accélère, timeline réduite à 3-5 ans", 9.1, 82, "trend"),
                        MarketInsight("Quantum-AI Hybrid", "Hybridation calcul quantique-IA, breakthrough performances attendues", 8.7, 76, "opportunity"),
                        MarketInsight("AI Regulation EU", "AI Act européen limite innovations, compliance coûteuse", 8.2, 91, "threat")
                    ],
                    "recommendations": [
                        "Intégrer massivement IA générative dans processes",
                        "Préparer transition vers AGI d'ici 2028",
                        "Investir R&D quantum computing + IA"
                    ]
                },
                "en": {
                    "summary": "AI/ML dominating with €156B European market. AGI approaching, generative AI integrated everywhere, quantum compute emerging.",
                    "insights": [
                        MarketInsight("Enterprise Generative AI", "Enterprise generative AI integration generates +67% productivity", 9.8, 94, "opportunity"),
                        MarketInsight("AGI Timeline Acceleration", "Progress toward AGI accelerating, timeline reduced to 3-5 years", 9.1, 82, "trend"),
                        MarketInsight("Quantum-AI Hybrid", "Quantum computing-AI hybridization, breakthrough performance expected", 8.7, 76, "opportunity"),
                        MarketInsight("EU AI Regulation", "European AI Act limits innovation, costly compliance", 8.2, 91, "threat")
                    ],
                    "recommendations": [
                        "Massively integrate generative AI into processes",
                        "Prepare for AGI transition by 2028",
                        "Invest in quantum computing + AI R&D"
                    ]
                }
            }
        }
    
    def get_translation(self, key: str) -> str:
        """Obtient la traduction pour une clé donnée"""
        return self.translations[self.language].get(key, key)
    
    def activate_simulation(self, sector: str):
        """Simulation d'activation synchrone pour l'interface"""
        self.status = "thinking"
        self.thoughts = []
        self.neural_activity = random.randint(800, 950)
        
        thoughts = self.get_translation("thoughts")
        
        for i, thought_text in enumerate(thoughts):
            thought = AgentThought(
                content=thought_text,
                timestamp=datetime.now(),
                confidence=random.uniform(0.7, 0.95)
            )
            self.thoughts.append(thought)
            
            if i == 2:
                self.status = "analyzing"
            elif i == len(thoughts) - 1:
                self.status = "completed"
                # S'assurer que les données existent pour le secteur
                sector_data = self.market_data.get(sector, self.market_data["FinTech"])
                self.current_analysis = sector_data.get(self.language, sector_data["fr"])
                self.confidence_level = random.uniform(85, 95)
            
            self.neural_activity += random.randint(-30, 50)
    
    def generate_confidence_gauge(self) -> go.Figure:
        """Génère un graphique de confiance amélioré"""
        try:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = self.confidence_level,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "AI Confidence", 'font': {'color': 'white', 'size': 16}},
                delta = {'reference': 80, 'valueformat': '.1f'},
                gauge = {
                    'axis': {'range': [None, 100], 'tickcolor': 'white', 'tickfont': {'color': 'white'}},
                    'bar': {'color': "#3b82f6", 'thickness': 0.8},
                    'steps': [
                        {'range': [0, 60], 'color': "rgba(239, 68, 68, 0.3)"},
                        {'range': [60, 85], 'color': "rgba(245, 158, 11, 0.3)"},
                        {'range': [85, 100], 'color': "rgba(16, 185, 129, 0.3)"}
                    ],
                    'threshold': {
                        'line': {'color': "#8b5cf6", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                },
                number = {'font': {'color': 'white', 'size': 24}}
            ))
            
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={'color': "white"},
                height=280,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            return fig
        except Exception as e:
            # Fallback en cas d'erreur
            return self.generate_simple_metric_chart("Confidence", self.confidence_level)
    
    def generate_neural_network_viz(self) -> go.Figure:
        """Visualisation réseau neuronal améliorée"""
        try:
            # Générer des données de réseau plus stables
            np.random.seed(42)  # Pour la reproductibilité
            n_nodes = 15
            
            # Positions des noeuds en cercle et centre
            angles = np.linspace(0, 2*np.pi, n_nodes-1, endpoint=False)
            x = [0] + [3 * np.cos(angle) for angle in angles]
            y = [0] + [3 * np.sin(angle) for angle in angles]
            
            # Connexions du centre vers les autres
            edge_x, edge_y = [], []
            for i in range(1, n_nodes):
                edge_x.extend([x[0], x[i], None])
                edge_y.extend([y[0], y[i], None])
            
            # Quelques connexions entre noeuds périphériques
            for i in range(1, n_nodes):
                next_node = i + 1 if i < n_nodes - 1 else 1
                if np.random.random() > 0.7:
                    edge_x.extend([x[i], x[next_node], None])
                    edge_y.extend([y[i], y[next_node], None])
            
            edge_trace = go.Scatter(
                x=edge_x, y=edge_y,
                line=dict(width=1.5, color='rgba(59, 130, 246, 0.6)'),
                hoverinfo='none',
                mode='lines'
            )
            
            # Couleurs des noeuds basées sur l'activité
            node_colors = ['#60a5fa' if i == 0 else f'rgba(59, 130, 246, {0.4 + 0.4 * np.random.random()})' 
                          for i in range(n_nodes)]
            node_sizes = [15 if i == 0 else 8 + 4 * np.random.random() for i in range(n_nodes)]
            
            node_trace = go.Scatter(
                x=x, y=y,
                mode='markers',
                hoverinfo='none',
                marker=dict(
                    size=node_sizes,
                    color=node_colors,
                    line=dict(width=1, color='#3b82f6')
                )
            )
            
            fig = go.Figure(data=[edge_trace, node_trace])
            fig.update_layout(
                showlegend=False,
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-4, 4]),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-4, 4]),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=300
            )
            return fig
        except Exception as e:
            return self.generate_simple_metric_chart("Neural Activity", self.neural_activity)
    
    def generate_simple_metric_chart(self, title: str, value: float) -> go.Figure:
        """Génère un graphique simple en cas d'erreur"""
        fig = go.Figure(data=[go.Bar(
            x=[title], 
            y=[value], 
            marker_color='#3b82f6',
            text=[f'{value:.1f}'],
            textposition='auto'
        )])
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "white"},
            height=280,
            showlegend=False,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        return fig
    
    def generate_sector_performance_chart(self, sector: str) -> go.Figure:
        """Génère un graphique de performance sectorielle"""
        try:
            # Données simulées de performance
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            performance = [85 + 10*np.sin(i*0.5) + np.random.normal(0, 3) for i in range(6)]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=months, 
                y=performance,
                mode='lines+markers',
                line=dict(color='#3b82f6', width=3),
                marker=dict(size=8, color='#60a5fa'),
                fill='tonexty',
                fillcolor='rgba(59, 130, 246, 0.1)',
                name=f'{sector} Performance'
            ))
            
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={'color': "white"},
                height=250,
                margin=dict(l=20, r=20, t=20, b=20),
                showlegend=False,
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)', range=[70, 110])
            )
            return fig
        except Exception as e:
            return self.generate_simple_metric_chart("Performance", 87.5)
    
    def chat_with_agent(self, message: str, sector: str) -> str:
        """Chat amélioré avec l'agent"""
        responses = {
            "fr": {
                "analysis": f"Selon mon analyse approfondie du secteur {sector}, les principales opportunités résident dans l'intégration IA et la transformation digitale.",
                "opportunities": f"Les opportunités majeures en {sector} incluent l'automatisation intelligente et les nouveaux modèles d'affaires data-driven.",
                "threats": f"Les défis principaux pour {sector} sont la régulation croissante et la concurrence technologique accrue.",
                "recommendations": f"Ma recommandation stratégique pour {sector} : investir massivement dans l'IA et former les équipes aux nouvelles technologies.",
                "default": f"Basé sur mes algorithmes prédictifs, {sector} montre un potentiel de croissance exceptionnel avec les bonnes stratégies."
            },
            "en": {
                "analysis": f"According to my deep analysis of the {sector} sector, main opportunities lie in AI integration and digital transformation.",
                "opportunities": f"Major opportunities in {sector} include intelligent automation and new data-driven business models.",
                "threats": f"Main challenges for {sector} are increasing regulation and heightened technological competition.",
                "recommendations": f"My strategic recommendation for {sector}: invest heavily in AI and train teams on new technologies.",
                "default": f"Based on my predictive algorithms, {sector} shows exceptional growth potential with the right strategies."
            }
        }
        
        message_lower = message.lower()
        response_type = "default"
        
        if any(word in message_lower for word in ["opportunit", "chance"]):
            response_type = "opportunities"
        elif any(word in message_lower for word in ["threat", "risk", "danger", "menace"]):
            response_type = "threats"
        elif any(word in message_lower for word in ["recommend", "advice", "conseil"]):
            response_type = "recommendations"
        elif any(word in message_lower for word in ["analy", "étud", "study"]):
            response_type = "analysis"
        
        return responses[self.language][response_type]

# Interface principale améliorée
def main():
    # Initialisation de l'état
    if 'agent' not in st.session_state:
        st.session_state.agent = ARIAAgent()
    
    if 'language' not in st.session_state:
        st.session_state.language = 'fr'
    
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
        
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = time.time()
    
    agent = st.session_state.agent
    agent.language = st.session_state.language
    
    # Refresh automatique des métriques
    current_time = time.time()
    if current_time - st.session_state.last_refresh > 5:  # Refresh toutes les 5 secondes
        if agent.status in ["thinking", "analyzing"]:
            agent.neural_activity += random.randint(-20, 30)
            agent.neural_activity = max(750, min(1000, agent.neural_activity))
        st.session_state.last_refresh = current_time
    
    # Particules animées
    st.markdown("""
    <div class="particles">
        <div class="particle" style="left: 10%; width: 4px; height: 4px; animation-delay: 0s;"></div>
        <div class="particle" style="left: 20%; width: 2px; height: 2px; animation-delay: 1s;"></div>
        <div class="particle" style="left: 70%; width: 3px; height: 3px; animation-delay: 2s;"></div>
        <div class="particle" style="left: 90%; width: 2px; height: 2px; animation-delay: 3s;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Header
    col1, col2 = st.columns([8, 1])
    
    with col1:
        st.markdown(f"""
        <div class='premium-header'>
            <h1 class='premium-title'>{agent.get_translation('agent_name')}</h1>
            <p class='premium-subtitle'>{agent.get_translation('agent_desc')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        lang = st.selectbox("🌐", ["🇫🇷 FR", "🇺🇸 EN"], key="language_selector")
        new_language = "fr" if "FR" in lang else "en"
        if new_language != st.session_state.language:
            st.session_state.language = new_language
            st.rerun()
    
    # Layout principal
    col1, col2, col3 = st.columns([3, 5, 3])
    
    with col1:
        # Panel de contrôle agent
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: white; text-align: center;">🤖 Agent Control</h3>', unsafe_allow_html=True)
        
        # Avatar agent amélioré
        status_class = f"status-{agent.status}"
        avatar_class = "agent-avatar active" if agent.status != "idle" else "agent-avatar"
        
        st.markdown(f"""
        <div style='text-align: center; margin: 25px 0;'>
            <div class='{avatar_class}'>
                <div class='agent-core'>🧠</div>
            </div>
            <h4 style='color: white; margin: 15px 0;'>{agent.get_translation("agent_name")}</h4>
            <div>
                <span class='status-indicator {status_class}'></span>
                <span style='color: white; font-size: 0.9rem;'>{agent.get_translation(f"status_{agent.status}")}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Configuration avec tous les secteurs
        st.markdown("<h4 style='color: white;'>🎯 Target Sector</h4>", unsafe_allow_html=True)
        
        sectors = agent.get_translation("sectors")
        selected_sector = st.selectbox(
            "Select sector",
            list(sectors.keys()),
            format_func=lambda x: sectors[x],
            label_visibility="collapsed",
            key="sector_selector"
        )
        
        # Bouton d'activation amélioré
        st.markdown("<br>", unsafe_allow_html=True)
        
        if agent.status in ["idle", "completed"]:
            if st.button("🚀 ACTIVATE ARIA", type="primary", key="activate_button"):
                with st.spinner("Activation en cours..."):
                    agent.activate_simulation(selected_sector)
                    st.success("✅ ARIA activated successfully!")
                    time.sleep(1)
                st.rerun()
        else:
            if st.button("⏹️ STOP AGENT", key="stop_button"):
                agent.status = "idle"
                agent.thoughts = []
                agent.current_analysis = None
                st.rerun()
        
        # Métriques temps réel améliorées
        if agent.status != "idle":
            st.markdown("<h4 style='color: white;'>📊 Real-time Metrics</h4>", unsafe_allow_html=True)
            
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value'>{agent.neural_activity}</div>
                    <div style='color: #94a3b8; font-size: 0.8rem;'>Neural Nodes</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_m2:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value'>{agent.confidence_level:.1f}%</div>
                    <div style='color: #94a3b8; font-size: 0.8rem;'>Confidence</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Graphique d'activité sectorielle
            if agent.status == "completed":
                st.markdown("<h5 style='color: #60a5fa; margin-top: 15px;'>📈 Sector Performance</h5>", unsafe_allow_html=True)
                try:
                    performance_fig = agent.generate_sector_performance_chart(selected_sector)
                    st.plotly_chart(performance_fig, use_container_width=True, key=f"performance_{selected_sector}")
                except Exception as e:
                    st.info("📊 Performance data loading...")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Neural Network amélioré
        if agent.status in ["thinking", "analyzing", "completed"]:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<h4 style="color: white; text-align: center;">🧠 Neural Network</h4>', unsafe_allow_html=True)
            try:
                neural_fig = agent.generate_neural_network_viz()
                st.plotly_chart(neural_fig, use_container_width=True, key=f"neural_viz_{agent.status}")
            except Exception as e:
                st.markdown("""
                <div style='text-align: center; padding: 20px;'>
                    <div style='font-size: 3rem; animation: pulse 2s infinite;'>🧠</div>
                    <p style='color: #94a3b8;'>Neural processing active...</p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Zone principale avec améliorations
        if agent.status != "idle" and agent.thoughts:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<h3 style="color: white;">🧠 Agent Thoughts Stream</h3>', unsafe_allow_html=True)
            
            for i, thought in enumerate(agent.thoughts):
                st.markdown(f"""
                <div class='thought-bubble' style='animation-delay: {i*0.2}s;'>
                    <div style='display: flex; align-items: start; gap: 15px;'>
                        <div style='background: linear-gradient(45deg, #3b82f6, #8b5cf6); border-radius: 50%; 
                                    width: 35px; height: 35px; display: flex; align-items: center; justify-content: center;
                                    position: relative;'>
                            🤖
                            <div style='position: absolute; inset: -2px; border-radius: 50%; 
                                        background: conic-gradient(from 0deg, transparent, #3b82f6, transparent);
                                        animation: rotate 3s linear infinite; z-index: -1;'></div>
                        </div>
                        <div style='flex: 1;'>
                            <p style='color: white; margin: 0 0 8px 0; font-weight: 500;'>{thought.content}</p>
                            <div style='display: flex; justify-content: between; align-items: center;'>
                                <span style='color: #94a3b8; font-size: 0.75rem;'>{thought.timestamp.strftime("%H:%M:%S")}</span>
                                <span style='color: #60a5fa; font-size: 0.75rem; margin-left: 10px;'>
                                    {thought.confidence:.0%} confidence
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Résultats d'analyse enrichis
        if agent.current_analysis and agent.status == "completed":
            st.markdown(f"""
            <div class='glass-card'>
                <h3 style='color: white;'>📋 Executive Summary</h3>
                <div style='background: rgba(59, 130, 246, 0.15); border-left: 4px solid #3b82f6; 
                            padding: 20px; border-radius: 0 15px 15px 0; position: relative;'>
                    <p style='color: #e2e8f0; margin: 0; line-height: 1.6;'>{agent.current_analysis.get("summary", "")}</p>
                    <div style='position: absolute; top: 10px; right: 15px; color: #60a5fa; font-size: 0.8rem;'>
                        Confidence: {agent.confidence_level:.1f}%
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Graphiques de confiance et métriques
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                st.markdown('<div class="glass-card"><h4 style="color: white; text-align: center;">🎯 AI Confidence</h4></div>', unsafe_allow_html=True)
                try:
                    confidence_fig = agent.generate_confidence_gauge()
                    st.plotly_chart(confidence_fig, use_container_width=True, key="confidence_gauge")
                except Exception as e:
                    st.markdown(f"""
                    <div style='text-align: center; padding: 40px;'>
                        <div style='font-size: 3rem; color: #60a5fa;'>{agent.confidence_level:.0f}%</div>
                        <div style='color: #94a3b8;'>Confidence Level</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col_chart2:
                st.markdown('<div class="glass-card"><h4 style="color: white; text-align: center;">Le secteur FinTech connaît une consolidation majeure avec l'émergence de super-apps et l'intégration massive de l'IA. Les régulations MiCA créent des opportunités pour les acteurs conformes.",
                    "insights": [
                        MarketInsight("IA Conversationnelle Bancaire", "L'intégration d'assistants IA dans les services bancaires représente une opportunité de 3.2B€ d'ici 2027", 9.2, 87, "opportunity"),
                        MarketInsight("DeFi Institutionnelle", "Les institutions financières traditionnelles adoptent massivement la DeFi avec un potentiel de 1.8B€", 8.1, 73, "opportunity"),
                        MarketInsight("Consolidation Accélérée", "Vague d'acquisitions prévue Q2-Q3 2025 avec 15+ opérations majeures attendues", 8.9, 84, "trend"),
                        MarketInsight("Durcissement Réglementaire", "MiCA et nouvelles régulations créent des barrières d'entrée mais favorisent les acteurs conformes", 7.8, 91, "threat")
                    ],
                    "recommendations": [
                        "Investir massivement dans l'IA conversationnelle avant Q2 2025",
                        "Préparer la conformité MiCA 6 mois avant les concurrents",
                        "Acquérir des talents blockchain avant la pénurie annoncée"
                    ]
                },
                "en": {
                    "summary": "The FinTech sector is experiencing major consolidation with the emergence of super-apps and massive AI integration. MiCA regulations create opportunities for compliant players.",
                    "insights": [
                        MarketInsight("Conversational Banking AI", "AI assistant integration in banking services represents a $3.5B opportunity by 2027", 9.2, 87, "opportunity"),
                        MarketInsight("Institutional DeFi", "Traditional financial institutions are massively adopting DeFi with $2.1B potential", 8.1, 73, "opportunity"),
                        MarketInsight("Market Consolidation", "Wave of acquisitions expected Q2-Q3 2025 with 15+ major operations anticipated", 8.9, 84, "trend"),
                        MarketInsight("Regulatory Tightening", "MiCA and new regulations create entry barriers but favor compliant players", 7.8, 91, "threat")
                    ],
                    "recommendations": [
                        "Invest heavily in conversational AI before Q2 2025",
                        "Prepare MiCA compliance 6 months ahead of competitors",
                        "Acquire blockchain talent before predicted shortage"
                    ]
                }
            },
            "HealthTech": {
                "fr": {
                    "summary": "HealthTech révolutionne les soins de santé avec l'IA prédictive, la télémédecine et les dispositifs médicaux connectés. Le marché européen croît de 18% annuellement.",
                    "insights": [
                        MarketInsight("Diagnostic IA", "Les solutions de diagnostic assisté par IA représentent un marché de 4.1B€ d'ici 2028", 9.5, 89, "opportunity"),
                        MarketInsight("Télémédecine Post-COVID", "Adoption permanente de la télémédecine avec 340% de croissance maintenue", 8.7, 92, "trend"),
                        MarketInsight("IoMT (Internet of Medical Things)", "Explosion des dispositifs médicaux connectés, marché de 2.8B€", 8.3, 85, "opportunity"),
                        MarketInsight("Réglementation GDPR Santé", "Durcissement des règles de protection des données médicales", 7.2, 88, "threat")
                    ],
                    "recommendations": [
                        "Développer des partenariats avec les hôpitaux pour l'IA diagnostic",
                        "Investir dans la cybersécurité médicale avant Q3 2025",
                        "Créer des solutions de télémédecine spécialisées"
                    ]
                },
                "en": {
                    "summary": "HealthTech is revolutionizing healthcare with predictive AI, telemedicine, and connected medical devices. European market growing 18% annually.",
                    "insights": [
                        MarketInsight("AI Diagnostics", "AI-assisted diagnostic solutions represent a $4.5B market by 2028", 9.5, 89, "opportunity"),
                        MarketInsight("Post-COVID Telemedicine", "Permanent adoption of telemedicine with sustained 340% growth", 8.7, 92, "trend"),
                        MarketInsight("IoMT Growth", "Explosion of connected medical devices, $3.1B market potential", 8.3, 85, "opportunity"),
                        MarketInsight("Healthcare Data Regulations", "Tightening of medical data protection rules", 7.2, 88, "threat")
                    ],
                    "recommendations": [
                        "Develop hospital partnerships for AI diagnostics",
                        "Invest in medical cybersecurity before Q3 2025",
                        "Create specialized telemedicine solutions"
                    ]
                }
            },
            "SaaS": {
                "fr": {
                    "summary": "Le marché SaaS européen atteint 85B€ avec l'IA générative intégrée. Les solutions verticales spécialisées dominent la croissance avec 23% CAGR.",
                    "insights": [
                        MarketInsight("SaaS + IA Générative", "Intégration massive de l'IA générative dans les SaaS existants, +45% de valeur", 9.1, 91, "opportunity"),
                        MarketInsight("Vertical SaaS", "Les solutions spécialisées par industrie surperforment le marché général", 8.8, 87, "trend"),
                        MarketInsight("API-First Architecture", "Migration vers des architectures API-first pour l'intégration IA", 8.4, 83, "trend"),
                        MarketInsight("Saturation du Marché Horizontal", "Saturation croissante des SaaS généralistes, concurrence accrue", 7.9, 89, "threat")
                    ],
                    "recommendations": [
                        "Intégrer l'IA générative dans votre stack SaaS existant",
                        "Se spécialiser sur des niches verticales spécifiques",
                        "Développer une API-first strategy"
                    ]
                },
                "en": {
                    "summary": "European SaaS market reaches €85B with integrated generative AI. Specialized vertical solutions dominate growth with 23% CAGR.",
                    "insights": [
                        MarketInsight("SaaS + Generative AI", "Massive integration of generative AI in existing SaaS, +45% value", 9.1, 91, "opportunity"),
                        MarketInsight("Vertical SaaS Dominance", "Industry-specialized solutions outperform general market", 8.8, 87, "trend"),
                        MarketInsight("API-First Migration", "Migration to API-first architectures for AI integration", 8.4, 83, "trend"),
                        MarketInsight("Horizontal Market Saturation", "Increasing saturation of generalist SaaS, heightened competition", 7.9, 89, "threat")
                    ],
                    "recommendations": [
                        "Integrate generative AI into existing SaaS stack",
                        "Specialize in specific vertical niches",
                        "Develop an API-first strategy"
                    ]
                }
            },
            "E-commerce": {
                "fr": {
                    "summary": "E-commerce européen de 887B€ transformé par l'IA conversationnelle, social commerce et durabilité. Le mobile représente 67% des transactions.",
                    "insights": [
                        MarketInsight("Commerce Conversationnel", "Chatbots IA et assistants vocaux génèrent +28% de conversion", 9.3, 88, "opportunity"),
                        MarketInsight("Social Commerce", "TikTok Shop et Instagram Shopping explosent, +156% de croissance", 8.9, 85, "trend"),
                        MarketInsight("E-commerce Durable", "Consommateurs privilégient les marques éco-responsables, +67% de demande", 8.2, 82, "opportunity"),
                        MarketInsight("Inflation Logistique", "Coûts de livraison en hausse de 23%, pression sur les marges", 7.6, 90, "threat")
                    ],
                    "recommendations": [
                        "Implémenter des assistants IA conversationnels avancés",
                        "Développer une stratégie social commerce multiplateforme",
                        "Intégrer la durabilité comme avantage concurrentiel"
                    ]
                },
                "en": {
                    "summary": "European e-commerce at €887B transformed by conversational AI, social commerce, and sustainability. Mobile accounts for 67% of transactions.",
                    "insights": [
                        MarketInsight("Conversational Commerce", "AI chatbots and voice assistants generate +28% conversion", 9.3, 88, "opportunity"),
                        MarketInsight("Social Commerce Explosion", "TikTok Shop and Instagram Shopping exploding, +156% growth", 8.9, 85, "trend"),
                        MarketInsight("Sustainable E-commerce", "Consumers favor eco-responsible brands, +67% demand", 8.2, 82, "opportunity"),
                        MarketInsight("Logistics Inflation", "Delivery costs up 23%, margin pressure", 7.6, 90, "threat")
                    ],
                    "recommendations": [
                        "Implement advanced conversational AI assistants",
                        "Develop multi-platform social commerce strategy",
                        "Integrate sustainability as competitive advantage"
                    ]
                }
            },
            "PropTech": {
                "fr": {
                    "summary": "PropTech révolutionne l'immobilier avec l'IA prédictive, réalité virtuelle et blockchain. Marché européen de 12.3B€ en croissance de 31% annuelle.",
                    "insights": [
                        MarketInsight("Valorisation IA", "Algorithmes d'estimation immobilière IA avec précision +85%", 9.0, 86, "opportunity"),
                        MarketInsight("VR/AR Immobilier", "Visites virtuelles deviennent standard, adoption 89% post-COVID", 8.6, 91, "trend"),
                        MarketInsight("Smart Buildings", "Bâtiments connectés et automatisés, marché de 2.1B€", 8.4, 83, "opportunity"),
                        MarketInsight("Régulation Airbnb", "Durcissement des régulations sur location courte durée", 7.3, 87, "threat")
                    ],
                    "recommendations": [
                        "Développer des outils d'évaluation immobilière IA",
                        "Investir dans les technologies VR/AR pour visites",
                        "Créer des solutions smart building IoT"
                    ]
                },
                "en": {
                    "summary": "PropTech revolutionizing real estate with predictive AI, virtual reality, and blockchain. European market at €12.3B growing 31% annually.",
                    "insights": [
                        MarketInsight("AI Valuation", "AI property valuation algorithms with +85% accuracy", 9.0, 86, "opportunity"),
                        MarketInsight("VR/AR Real Estate", "Virtual tours becoming standard, 89% adoption post-COVID", 8.6, 91, "trend"),
                        MarketInsight("Smart Buildings Boom", "Connected and automated buildings, €2.1B market", 8.4, 83, "opportunity"),
                        MarketInsight("Short-term Rental Regulations", "Tightening regulations on short-term rentals", 7.3, 87, "threat")
                    ],
                    "recommendations": [
                        "Develop AI-powered property valuation tools",
                        "Invest in VR/AR technologies for property tours",
                        "Create smart building IoT solutions"
                    ]
                }
            },
            "EdTech": {
                "fr": {
                    "summary": "EdTech transforme l'éducation avec IA adaptive, réalité immersive et apprentissage personnalisé. Marché européen de 24.5B€ post-pandémie.",
                    "insights": [
                        MarketInsight("IA Pédagogique Adaptive", "Systèmes d'apprentissage adaptatif IA améliorent résultats de +43%", 9.4, 89, "opportunity"),
                        MarketInsight("Métaverse Éducatif", "Campus virtuels et apprentissage immersif, adoption 67% universités", 8.7, 84, "trend"),
                        MarketInsight("Micro-Learning Mobile", "Formation courte sur mobile explose, +234% d'engagement", 8.3, 88, "opportunity"),
                        MarketInsight("Fracture Numérique", "Inégalités d'accès aux technologies éducatives s'accentuent", 7.1, 85, "threat")
                    ],
                    "recommendations": [
                        "Créer des systèmes d'IA pédagogique personnalisés",
                        "Développer des expériences d'apprentissage immersives",
                        "Concevoir des solutions mobiles de micro-learning"
                    ]
                },
                "en": {
                    "summary": "
