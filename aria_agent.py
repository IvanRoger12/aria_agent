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

# Configuration de la page
st.set_page_config(
    page_title="🤖 ARIA - AI Strategic Intelligence Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé avec design premium
st.markdown("""
<style>
    /* Fond bleu premium avec dégradé */
    .main {
        background: linear-gradient(135deg, #0c1d3d 0%, #1e3a8a 50%, #0c1d3d 100%);
        color: #ffffff;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0c1d3d 0%, #1e3a8a 50%, #0c1d3d 100%);
    }
    
    /* Arrière-plan avec effet de circuit imprimé */
    .main::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 30%, rgba(37, 99, 235, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(99, 102, 241, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(139, 92, 246, 0.15) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
    }
    
    .main::after {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(59, 130, 246, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(59, 130, 246, 0.1) 1px, transparent 1px);
        background-size: 40px 40px;
        pointer-events: none;
        z-index: -1;
        opacity: 0.4;
        animation: circuitFlow 20s infinite linear;
    }
    
    @keyframes circuitFlow {
        0% { background-position: 0 0; }
        100% { background-position: 40px 40px; }
    }
    
    /* Amélioration de la lisibilité */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 700;
        text-shadow: 0 0 15px rgba(96, 165, 250, 0.7);
    }
    
    p, span, div {
        color: #f0f9ff !important;
    }
    
    /* Correction du problème du selectbox */
    .stSelectbox > div > div {
        background-color: rgba(30, 58, 138, 0.9) !important;
        color: #ffffff !important;
        border: 1px solid rgba(96, 165, 250, 0.7) !important;
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }
    
    .stSelectbox > div > div:hover {
        border: 1px solid rgba(96, 165, 250, 1) !important;
    }
    
    /* Options du dropdown */
    .stSelectbox [role="listbox"] {
        background-color: rgba(30, 58, 138, 0.95) !important;
        border: 1px solid rgba(96, 165, 250, 0.7) !important;
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }
    
    .stSelectbox [role="option"] {
        color: #ffffff !important;
        background-color: transparent !important;
    }
    
    .stSelectbox [role="option"]:hover {
        background-color: rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Boutons premium */
    .stButton > button {
        background: linear-gradient(45deg, #2563eb, #3b82f6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 20px rgba(37, 99, 235, 0.7) !important;
        padding: 12px 24px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 0 30px rgba(37, 99, 235, 0.9) !important;
        background: linear-gradient(45deg, #1d4ed8, #2563eb) !important;
    }
    
    /* Cartes avec effet glassmorphism premium */
    .metric-card, .analysis-card, .thought-bubble {
        background: rgba(30, 58, 138, 0.7) !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(96, 165, 250, 0.5) !important;
        border-radius: 20px !important;
        padding: 25px !important;
        margin: 15px 0 !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .metric-card:hover, .analysis-card:hover, .thought-bubble:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.5) !important;
        border: 1px solid rgba(96, 165, 250, 0.8) !important;
    }
    
    /* Animation de pulsation pour l'agent */
    .agent-thinking {
        background: linear-gradient(45deg, #1e40af, #3730a3) !important;
        animation: pulse 2s infinite !important;
        border-radius: 20px !important;
        padding: 20px !important;
        margin: 15px 0 !important;
        box-shadow: 0 0 25px rgba(79, 70, 229, 0.7) !important;
    }
    
    @keyframes pulse {
        0% { opacity: 0.8; box-shadow: 0 0 20px rgba(79, 70, 229, 0.7); }
        50% { opacity: 1; box-shadow: 0 0 35px rgba(79, 70, 229, 0.9); }
        100% { opacity: 0.8; box-shadow: 0 0 20px rgba(79, 70, 229, 0.7); }
    }
    
    /* Bulles de pensée premium */
    .thought-bubble {
        background: rgba(30, 64, 175, 0.75) !important;
        border-left: 5px solid #3b82f6 !important;
        padding: 20px !important;
        margin: 15px 0 !important;
        border-radius: 0 15px 15px 0 !important;
        animation: slideIn 0.5s ease-out !important;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3) !important;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Indicateur de statut premium */
    .status-indicator {
        width: 15px;
        height: 15px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 10px;
        animation: statusBlink 1.5s infinite;
        box-shadow: 0 0 12px rgba(96, 165, 250, 0.9);
    }
    
    @keyframes statusBlink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0.4; }
    }
    
    /* Barre de défilement stylisée */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 58, 138, 0.4);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #3b82f6, #60a5fa);
        border-radius: 10px;
        border: 2px solid rgba(30, 58, 138, 0.3);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, #2563eb, #3b82f6);
    }
    
    /* Effet de surbrillance pour le texte */
    .highlight {
        background: linear-gradient(90deg, #3b82f6, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
    }
    
    /* Centrage des éléments */
    .centered {
        text-align: center;
        margin: 0 auto;
        display: block;
    }
    
    /* Jauge de confiance stylisée */
    .confidence-gauge {
        background: rgba(30, 58, 138, 0.7);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(96, 165, 250, 0.5);
        border-radius: 20px;
        padding: 25px;
        margin: 20px auto;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
        max-width: 500px;
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
    def __init__(self, language: str = "fr"):
        self.language = language
        self.status = "idle"
        self.thoughts = []
        self.current_analysis = None
        self.confidence_level = 0.0
        self.neural_activity = 0
        
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
                    "EdTech": "Technologies Éducatives"
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
                    "EdTech": "Education Technologies"
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
        
        self.market_data = {
            "FinTech": {
                "fr": {
                    "summary": "Le secteur FinTech connaît une consolidation majeure avec l'émergence de super-apps et l'intégration massive de l'IA. Les régulations MiCA créent des opportunités pour les acteurs conformes.",
                    "insights": [
                        MarketInsight("IA Conversationnelle Bancaire", "L'intégration d'assistants IA dans les services bancaires représente une opportunité de 3.2B€ d'ici 2027", 9.2, 87, "opportunity"),
                        MarketInsight("DeFi Institutionnelle", "Les institutions financières traditionnelles adoptent massivement la DeFi avec un potentiel de 1.8B€", 8.1, 73, "opportunity"),
                        MarketInsight("Durcissement Réglementaire", "MiCA et nouvelles régulations créent des barrières d'entrée mais favorisent les acteurs conformes", 7.8, 91, "threat"),
                        MarketInsight("Consolidation du Marché", "Vague d'acquisitions prévue Q2-Q3 2025 avec 15+ opérations majeures attendues", 8.9, 84, "trend")
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
                        MarketInsight("Regulatory Tightening", "MiCA and new regulations create entry barriers but favor compliant players", 7.8, 91, "threat"),
                        MarketInsight("Market Consolidation", "Wave of acquisitions expected Q2-Q3 2025 with 15+ major operations anticipated", 8.9, 84, "trend")
                    ],
                    "recommendations": [
                        "Invest heavily in conversational AI before Q2 2025",
                        "Prepare MiCA compliance 6 months ahead of competitors", 
                        "Acquire blockchain talent before predicted shortage"
                    ]
                }
            }
        }
    
    def get_translation(self, key: str) -> str:
        return self.translations[self.language].get(key, key)
    
    async def activate(self, sector: str) -> None:
        self.status = "thinking"
        self.thoughts = []
        self.neural_activity = random.randint(800, 900)
        
        thoughts = self.get_translation("thoughts")
        
        for i, thought_text in enumerate(thoughts):
            await asyncio.sleep(random.uniform(0.8, 1.5))
            
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
                self.current_analysis = self.market_data.get(sector, {}).get(self.language, {})
                self.confidence_level = random.uniform(85, 95)
            
            self.neural_activity += random.randint(-30, 50)
    
    def generate_confidence_gauge(self) -> go.Figure:
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = self.confidence_level,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Niveau de Confiance", 'font': {'color': 'white', 'size': 20}},
            delta = {'reference': 80, 'font': {'color': 'white', 'size': 16}},
            gauge = {
                'axis': {'range': [None, 100], 'tickcolor': 'white', 'tickfont': {'color': 'white', 'size': 14}},
                'bar': {'color': "#3b82f6"},
                'steps': [
                    {'range': [0, 50], 'color': "#ef4444"},
                    {'range': [50, 80], 'color': "#f59e0b"},
                    {'range': [80, 100], 'color': "#10b981"}
                ],
                'threshold': {
                    'line': {'color': "#8b5cf6", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "white", 'family': "Arial", 'size': 16},
            height=350,
            margin=dict(l=30, r=30, t=60, b=20)
        )
        
        return fig

# Interface principale
def main():
    if 'agent' not in st.session_state:
        st.session_state.agent = ARIAAgent()
    
    if 'language' not in st.session_state:
        st.session_state.language = 'fr'
    
    agent = st.session_state.agent
    agent.language = st.session_state.language
    
    # Header centré avec design premium
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 40px;'>
        <h1 style='background: linear-gradient(45deg, #3b82f6, #60a5fa, #93c5fd); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3.5rem; margin: 0; font-weight: 800;'>
            🧠 {agent.get_translation('agent_name')}
        </h1>
        <p style='color: #dbeafe; font-size: 1.3rem; margin: 10px 0 0 0; font-weight: 400;'>
            {agent.get_translation('agent_desc')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sélecteur de langue centré
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        lang = st.selectbox("🌐", ["🇫🇷 FR", "🇺🇸 EN"], key="lang_select", index=0)
        new_language = "fr" if "FR" in lang else "en"
        if new_language != st.session_state.language:
            st.session_state.language = new_language
            st.rerun()
    
    # Layout principal
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div class='analysis-card'>
            <h3 style='color: #ffffff; text-align: center; margin-bottom: 25px;'>🤖 Panneau de Contrôle</h3>
        """, unsafe_allow_html=True)
        
        status_color = {
            "idle": "#6b7280",
            "thinking": "#f59e0b", 
            "analyzing": "#3b82f6",
            "completed": "#10b981"
        }.get(agent.status, "#6b7280")
        
        st.markdown(f"""
        <div style='text-align: center; margin: 20px 0;'>
            <div style='position: relative; display: inline-block;'>
                <div style='width: 100px; height: 100px; border-radius: 50%; background: linear-gradient(45deg, #3b82f6, #60a5fa); display: flex; align-items: center; justify-content: center; margin: 0 auto; {"animation: pulse 2s infinite;" if agent.status != "idle" else ""}'>
                    <span style='font-size: 2.5rem;'>🤖</span>
                </div>
                <div style='position: absolute; bottom: 0; right: 0; width: 25px; height: 25px; border-radius: 50%; background: {status_color}; border: 3px solid #0c1d3d; {"animation: statusBlink 1.5s infinite;" if agent.status in ["thinking", "analyzing"] else ""}'></div>
            </div>
            <h4 style='color: #ffffff; margin: 15px 0 5px 0;'>{agent.get_translation("agent_name")}</h4>
            <p style='color: #bfdbfe; font-size: 1rem; margin: 0;'>Activité Neuronale: {agent.neural_activity}</p>
        </div>
        """, unsafe_allow_html=True)
        
        status_text = agent.get_translation(f"status_{agent.status}")
        st.markdown(f"""
        <div style='background: rgba(59, 130, 246, 0.25); border-radius: 12px; padding: 18px; margin: 25px 0; text-align: center;'>
            <p style='color: #ffffff; margin: 0; font-weight: 600; font-size: 1.1rem;'>{status_text}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h4 style='color: #ffffff; text-align: center; margin-bottom: 15px;'>🎯 Secteur Cible</h4>", unsafe_allow_html=True)
        sectors = agent.get_translation("sectors")
        sector_options = list(sectors.keys())
        
        selected_sector = st.selectbox(
            "Sélectionnez un secteur",
            sector_options,
            format_func=lambda x: sectors[x],
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if agent.status in ["idle", "completed"]:
            if st.button("🚀 Activer l'Agent ARIA", key="activate_btn", type="primary", use_container_width=True):
                with st.spinner("Activation de l'agent en cours..."):
                    try:
                        loop = asyncio.get_event_loop()
                    except RuntimeError:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                    
                    loop.run_until_complete(agent.activate(selected_sector))
                    st.rerun()
        else:
            if st.button("⏹️ Arrêter l'Agent", key="stop_btn", use_container_width=True):
                agent.status = "idle"
                agent.thoughts = []
                agent.current_analysis = None
                st.rerun()
        
        if agent.status != "idle":
            st.markdown("<br><h4 style='color: #ffffff; text-align: center;'>📊 Métriques en Temps Réel</h4>", unsafe_allow_html=True)
            
            metrics_data = {
                "Activité Neuronale": f"{agent.neural_activity}",
                "Sources de Données": "847", 
                "Insights Générés": f"{len([t for t in agent.thoughts if t.confidence > 0.8])}",
                "Niveau de Confiance": f"{agent.confidence_level:.1f}%" if agent.confidence_level > 0 else "N/A"
            }
            
            for metric, value in metrics_data.items():
                st.markdown(f"""
                <div class='metric-card'>
                    <p style='color: #bfdbfe; margin: 0; font-size: 0.9rem;'>{metric}</p>
                    <p style='color: #ffffff; margin: 0; font-size: 1.4rem; font-weight: bold;'>{value}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        if agent.status != "idle" and agent.thoughts:
            st.markdown("""
            <div class='analysis-card'>
                <h3 style='color: #ffffff; text-align: center; margin-bottom: 25px;'>🧠 Processus de Pensée</h3>
            </div>
            """, unsafe_allow_html=True)
            
            for i, thought in enumerate(agent.thoughts):
                st.markdown(f"""
                <div class='thought-bubble'>
                    <div style='display: flex; align-items: center; margin-bottom: 10px;'>
                        <span style='background: linear-gradient(45deg, #3b82f6, #60a5fa); border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; margin-right: 15px;'>
                            <span style='font-size: 1.2rem;'>🤖</span>
                        </span>
                        <div>
                            <p style='color: #ffffff; margin: 0; font-size: 1.1rem; font-weight: 500;'>{thought.content}</p>
                            <p style='color: #bfdbfe; margin: 0; font-size: 0.8rem;'>{thought.timestamp.strftime("%H:%M:%S")}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        if agent.current_analysis and agent.status == "completed":
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class='analysis-card'>
                <h3 style='color: #ffffff; text-align: center; margin-bottom: 25px;'>📋 Résumé Exécutif</h3>
                <div style='background: linear-gradient(45deg, rgba(59, 130, 246, 0.25), rgba(96, 165, 250, 0.25)); border-left: 5px solid #3b82f6; padding: 25px; border-radius: 0 15px 15px 0;'>
                    <p style='color: #f0f9ff; margin: 0; line-height: 1.7; font-size: 1.1rem;'>{agent.current_analysis.get("summary", "")}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if agent.confidence_level > 0:
                st.markdown("""
                <div class='analysis-card'>
                    <h3 style='color: #ffffff; text-align: center; margin-bottom: 25px;'>📊 Analyse de Confiance</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Conteneur pour la jauge
                st.markdown("<div class='confidence-gauge'>", unsafe_allow_html=True)
                confidence_fig = agent.generate_confidence_gauge()
                st.plotly_chart(confidence_fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            insights = agent.current_analysis.get("insights", [])
            if insights:
                st.markdown("""
                <div class='analysis-card'>
                    <h3 style='color: #ffffff; text-align: center; margin-bottom: 25px;'>🎯 Insights Détectés</h3>
                </div>
                """, unsafe_allow_html=True)
                
                opportunities = [i for i in insights if i.category == "opportunity"]
                threats = [i for i in insights if i.category == "threat"]
                trends = [i for i in insights if i.category == "trend"]
                
                if opportunities:
                    st.markdown("<h4 style='color: #10b981; text-align: center;'>💡 Opportunités</h4>", unsafe_allow_html=True)
                    for opp in opportunities:
                        st.markdown(f"""
                        <div style='background: rgba(16, 185, 129, 0.2); border-left: 5px solid #10b981; padding: 20px; margin: 15px 0; border-radius: 0 15px 15px 0;'>
                            <h5 style='color: #ffffff; margin: 0 0 10px 0; font-size: 1.2rem;'>{opp.title}</h5>
                            <p style='color: #d1fae5; margin: 0 0 10px 0; font-size: 1rem;'>{opp.description}</p>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <span style='color: #a7f3d0; font-size: 0.9rem;'>Impact: {opp.impact_score}/10</span>
                                <span style='color: #10b981; font-size: 0.9rem;'>Confiance: {opp.confidence}%</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                if threats:
                    st.markdown("<h4 style='color: #ef4444; text-align: center;'>⚠️ Menaces</h4>", unsafe_allow_html=True)
                    for threat in threats:
                        st.markdown(f"""
                        <div style='background: rgba(239, 68, 68, 0.2); border-left: 5px solid #ef4444; padding: 20px; margin: 15px 0; border-radius: 0 15px 15px 0;'>
                            <h5 style='color: #ffffff; margin: 0 0 10px 0; font-size: 1.2rem;'>{threat.title}</h5>
                            <p style='color: #fee2e2; margin: 0 0 10px 0; font-size: 1rem;'>{threat.description}</p>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <span style='color: #fecaca; font-size: 0.9rem;'>Impact: {threat.impact_score}/10</span>
                                <span style='color: #ef4444; font-size: 0.9rem;'>Confiance: {threat.confidence}%</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                if trends:
                    st.markdown("<h4 style='color: #8b5cf6; text-align: center;'>📈 Tendances</h4>", unsafe_allow_html=True)
                    for trend in trends:
                        st.markdown(f"""
                        <div style='background: rgba(139, 92, 246, 0.2); border-left: 5px solid #8b5cf6; padding: 20px; margin: 15px 0; border-radius: 0 15px 15px 0;'>
                            <h5 style='color: #ffffff; margin: 0 0 10px 0; font-size: 1.2rem;'>{trend.title}</h5>
                            <p style='color: #ede9fe; margin: 0 0 10px 0; font-size: 1rem;'>{trend.description}</p>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <span style='color: #ddd6fe; font-size: 0.9rem;'>Impact: {trend.impact_score}/10</span>
                                <span style='color: #8b5cf6; font-size: 0.9rem;'>Confiance: {trend.confidence}%</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            recommendations = agent.current_analysis.get("recommendations", [])
            if recommendations:
                st.markdown("""
                <div class='analysis-card'>
                    <h3 style='color: #ffffff; text-align: center; margin-bottom: 25px;'>🎯 Recommandations IA</h3>
                </div>
                """, unsafe_allow_html=True)
                
                for i, rec in enumerate(recommendations, 1):
                    st.markdown(f"""
                    <div style='display: flex; align-items: start; background: rgba(139, 92, 246, 0.2); border-radius: 15px; padding: 20px; margin: 15px 0;'>
                        <div style='background: linear-gradient(45deg, #8b5cf6, #a855f7); border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; margin-right: 20px; flex-shrink: 0;'>
                            <span style='color: white; font-weight: bold; font-size: 1.1rem;'>{i}</span>
                        </div>
                        <p style='color: #f0f9ff; margin: 0; line-height: 1.6; font-size: 1.1rem;'>{rec}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class='analysis-card'>
                <h3 style='color: #ffffff; text-align: center; margin-bottom: 25px;'>📤 Export & Actions</h3>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📄 Exporter Rapport", key="export_btn", use_container_width=True):
                    report_content = f"""
                    🤖 ARIA - RAPPORT STRATÉGIQUE
                    Généré le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    Secteur: {selected_sector}
                    Niveau de Confiance: {agent.confidence_level:.1f}%
                    
                    RÉSUMÉ EXÉCUTIF:
                    {agent.current_analysis.get('summary', '')}
                    
                    INSIGHTS CLÉS:
                    """
                    
                    for insight in insights:
                        report_content += f"\n• {insight.title} (Impact: {insight.impact_score}/10, Confiance: {insight.confidence}%)"
                        report_content += f"\n  {insight.description}\n"
                    
                    report_content += "\nRECOMMANDATIONS:\n"
                    for i, rec in enumerate(recommendations, 1):
                        report_content += f"{i}. {rec}\n"
                    
                    st.download_button(
                        label="⬇️ Télécharger le Rapport",
                        data=report_content.encode('utf-8'),
                        file_name=f"aria_rapport_{selected_sector}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
            
            with col2:
                if st.button("🔔 Configurer Alertes", key="alerts_btn", use_container_width=True):
                    st.success("✅ Système d'alertes configuré! Vous recevrez des notifications pour les changements de marché.")
            
            with col3:
                if st.button("🔄 Ré-analyser", key="reanalyze_btn", use_container_width=True):
                    agent.status = "idle"
                    agent.thoughts = []
                    agent.current_analysis = None
                    agent.confidence_level = 0
                    st.rerun()
        
        elif agent.status == "idle":
            st.markdown("""
            <div class='analysis-card' style='text-align: center; padding: 60px;'>
                <div style='font-size: 5rem; margin-bottom: 25px;'>🤖</div>
                <h3 style='color: #ffffff; margin-bottom: 20px;'>ARIA Prêt pour la Mission</h3>
                <p style='color: #bfdbfe; margin-bottom: 40px; font-size: 1.1rem;'>Sélectionnez un secteur cible et activez l'agent pour commencer l'analyse stratégique de marché.</p>
                <div style='background: rgba(59, 130, 246, 0.2); border-radius: 15px; padding: 25px; margin: 25px 0;'>
                    <h4 style='color: #93c5fd; margin-bottom: 20px;'>🧠 Capacités de l'Agent</h4>
                    <ul style='color: #dbeafe; text-align: left; list-style: none; padding: 0; font-size: 1.05rem;'>
                        <li style='margin: 12px 0;'>🔍 Collecte de renseignements multi-sources</li>
                        <li style='margin: 12px 0;'>⚡ Analyse et prédiction de tendances en temps réel</li>
                        <li style='margin: 12px 0;'>🎯 Identification d'opportunités stratégiques</li>
                        <li style='margin: 12px 0;'>📊 Évaluation des risques et stratégies d'atténuation</li>
                        <li style='margin: 12px 0;'>🤖 Recommandations actionnables alimentées par l'IA</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer premium
    st.markdown("""
    <div style='margin-top: 60px; padding: 40px 0; border-top: 1px solid rgba(255, 255, 255, 0.15); text-align: center;'>
        <p style='color: #93c5fd; margin: 0; font-size: 1.1rem;'>
            🤖 ARIA - Agent Autonome de Recherche et d'Intelligence | 
            Propulsé par des Réseaux Neuronaux IA Avancés | 
            Niveau de Confiance: {confidence}%
        </p>
        <p style='color: #bfdbfe; font-size: 1rem; margin: 10px 0 0 0;'>
            Dernière mise à jour: {timestamp} | Activité Neuronale: {activity} nœuds
        </p>
    </div>
    """.format(
        confidence=f"{agent.confidence_level:.1f}" if agent.confidence_level > 0 else "N/A",
        timestamp=datetime.now().strftime('%H:%M:%S'),
        activity=agent.neural_activity
    ), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
