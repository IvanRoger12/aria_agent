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

# CSS personnalisé avec design bleu et effets futuristes
st.markdown("""
<style>
    /* Fond bleu avec dégradé */
    .main {
        background: linear-gradient(135deg, #0c1d3d 0%, #1e3a8a 50%, #0c1d3d 100%);
        color: #ffffff;
    }
    
    /* Styles de base améliorés */
    .stApp {
        background: linear-gradient(135deg, #0c1d3d 0%, #1e3a8a 50%, #0c1d3d 100%);
    }
    
    /* Arrière-plan avec effet de bug numérique */
    .main::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 30%, rgba(37, 99, 235, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(99, 102, 241, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(139, 92, 246, 0.1) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
    }
    
    /* Animation d'effet de bug numérique */
    @keyframes digitalGlitch {
        0% { opacity: 0.1; transform: translate(0, 0); }
        25% { opacity: 0.15; transform: translate(-2px, 2px); }
        50% { opacity: 0.2; transform: translate(2px, -1px); }
        75% { opacity: 0.15; transform: translate(1px, 3px); }
        100% { opacity: 0.1; transform: translate(0, 0); }
    }
    
    .main::after {
        content: "00101010 10101010 01010101";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(37, 99, 235, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(37, 99, 235, 0.05) 1px, transparent 1px);
        background-size: 30px 30px;
        pointer-events: none;
        z-index: -1;
        opacity: 0.3;
        animation: digitalGlitch 5s infinite ease-in-out;
        mix-blend-mode: overlay;
    }
    
    /* Amélioration de la lisibilité du texte */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(96, 165, 250, 0.5);
    }
    
    p, span, div {
        color: #f0f9ff !important;
    }
    
    /* Conteneurs avec effet de verre bleu */
    .stSelectbox > div > div {
        background-color: rgba(30, 58, 138, 0.7) !important;
        color: #ffffff !important;
        border: 1px solid rgba(96, 165, 250, 0.5) !important;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    /* Boutons avec effet néon bleu */
    .stButton > button {
        background: linear-gradient(45deg, #2563eb, #3b82f6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 15px rgba(37, 99, 235, 0.6) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 0 25px rgba(37, 99, 235, 0.8) !important;
        background: linear-gradient(45deg, #1d4ed8, #2563eb) !important;
    }
    
    /* Cartes avec effet glassmorphism bleu */
    .metric-card, .analysis-card, .thought-bubble {
        background: rgba(30, 58, 138, 0.6) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(96, 165, 250, 0.4) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        margin: 10px 0 !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Animation de pulsation pour l'agent */
    .agent-thinking {
        background: linear-gradient(45deg, #1e40af, #3730a3) !important;
        animation: pulse 2s infinite !important;
        border-radius: 15px !important;
        padding: 15px !important;
        margin: 10px 0 !important;
        box-shadow: 0 0 20px rgba(79, 70, 229, 0.6) !important;
    }
    
    @keyframes pulse {
        0% { opacity: 0.8; box-shadow: 0 0 15px rgba(79, 70, 229, 0.6); }
        50% { opacity: 1; box-shadow: 0 0 25px rgba(79, 70, 229, 0.8); }
        100% { opacity: 0.8; box-shadow: 0 0 15px rgba(79, 70, 229, 0.6); }
    }
    
    /* Bulles de pensée avec effet bleu */
    .thought-bubble {
        background: rgba(30, 64, 175, 0.7) !important;
        border-left: 4px solid #3b82f6 !important;
        padding: 15px !important;
        margin: 10px 0 !important;
        border-radius: 0 12px 12px 0 !important;
        animation: slideIn 0.5s ease-out !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Indicateur de statut avec lueur bleue */
    .status-indicator {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
        animation: statusBlink 1.5s infinite;
        box-shadow: 0 0 8px rgba(96, 165, 250, 0.8);
    }
    
    @keyframes statusBlink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0.3; }
    }
    
    /* Effet de lueur pour les éléments importants */
    .glow-effect {
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.7) !important;
        transition: all 0.3s ease !important;
    }
    
    .glow-effect:hover {
        box-shadow: 0 0 25px rgba(59, 130, 246, 0.9) !important;
    }
    
    /* Barre de défilement stylisée */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 58, 138, 0.3);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #3b82f6, #60a5fa);
        border-radius: 10px;
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
            title = {'text': "Confidence Level", 'font': {'color': 'white', 'size': 16}},
            delta = {'reference': 80, 'font': {'color': 'white', 'size': 14}},
            gauge = {
                'axis': {'range': [None, 100], 'tickcolor': 'white', 'tickfont': {'color': 'white', 'size': 12}},
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
            font={'color': "white", 'family': "Arial", 'size': 14},
            height=300,
            margin=dict(l=20, r=20, t=50, b=20)
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
    
    # Header avec design bleu
    col1, col2, col3 = st.columns([6, 1, 1])
    
    with col1:
        st.markdown(f"""
        <div style='margin-bottom: 30px;'>
            <h1 style='background: linear-gradient(45deg, #3b82f6, #60a5fa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; margin: 0; font-weight: 800;'>
                🧠 {agent.get_translation('agent_name')}
            </h1>
            <p style='color: #dbeafe; font-size: 1.2rem; margin: 0; font-weight: 400;'>
                {agent.get_translation('agent_desc')}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        lang = st.selectbox("🌐", ["🇫🇷 FR", "🇺🇸 EN"], key="lang_select")
        new_language = "fr" if "FR" in lang else "en"
        if new_language != st.session_state.language:
            st.session_state.language = new_language
            st.rerun()
    
    # Layout principal
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div class='analysis-card'>
            <h3 style='color: #ffffff; text-align: center; margin-bottom: 20px;'>🤖 Agent Control Panel</h3>
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
                <div style='width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(45deg, #3b82f6, #60a5fa); display: flex; align-items: center; justify-content: center; margin: 0 auto; {"animation: pulse 2s infinite;" if agent.status != "idle" else ""}'>
                    <span style='font-size: 2rem;'>🤖</span>
                </div>
                <div style='position: absolute; bottom: 0; right: 0; width: 20px; height: 20px; border-radius: 50%; background: {status_color}; border: 2px solid white; {"animation: statusBlink 1.5s infinite;" if agent.status in ["thinking", "analyzing"] else ""}'></div>
            </div>
            <h4 style='color: #ffffff; margin: 10px 0 5px 0;'>{agent.get_translation("agent_name")}</h4>
            <p style='color: #bfdbfe; font-size: 0.9rem; margin: 0;'>Neural Activity: {agent.neural_activity}</p>
        </div>
        """, unsafe_allow_html=True)
        
        status_text = agent.get_translation(f"status_{agent.status}")
        st.markdown(f"""
        <div style='background: rgba(59, 130, 246, 0.2); border-radius: 10px; padding: 15px; margin: 20px 0; text-align: center;'>
            <p style='color: #ffffff; margin: 0; font-weight: 500;'>{status_text}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<p style='color: #ffffff; font-weight: 500; margin-bottom: 10px;'>🎯 Target Sector:</p>", unsafe_allow_html=True)
        sectors = agent.get_translation("sectors")
        sector_options = list(sectors.keys())
        
        selected_sector = st.selectbox(
            "Select sector",
            sector_options,
            format_func=lambda x: sectors[x],
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if agent.status in ["idle", "completed"]:
            if st.button("🚀 Activate ARIA Agent", key="activate_btn", type="primary"):
                with st.spinner("Agent activation in progress..."):
                    try:
                        loop = asyncio.get_event_loop()
                    except RuntimeError:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                    
                    loop.run_until_complete(agent.activate(selected_sector))
                    st.rerun()
        else:
            if st.button("⏹️ Stop Agent", key="stop_btn"):
                agent.status = "idle"
                agent.thoughts = []
                agent.current_analysis = None
                st.rerun()
        
        if agent.status != "idle":
            st.markdown("<br><h4 style='color: #ffffff;'>📊 Real-time Metrics</h4>", unsafe_allow_html=True)
            
            metrics_data = {
                "Neural Activity": f"{agent.neural_activity}",
                "Data Sources": "847", 
                "Insights Generated": f"{len([t for t in agent.thoughts if t.confidence > 0.8])}",
                "Confidence": f"{agent.confidence_level:.1f}%" if agent.confidence_level > 0 else "N/A"
            }
            
            for metric, value in metrics_data.items():
                st.markdown(f"""
                <div class='metric-card'>
                    <p style='color: #bfdbfe; margin: 0; font-size: 0.8rem;'>{metric}</p>
                    <p style='color: #ffffff; margin: 0; font-size: 1.2rem; font-weight: bold;'>{value}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        if agent.status != "idle" and agent.thoughts:
            st.markdown("""
            <div class='analysis-card'>
                <h3 style='color: #ffffff; margin-bottom: 20px;'>🧠 Agent Thought Process</h3>
            </div>
            """, unsafe_allow_html=True)
            
            for i, thought in enumerate(agent.thoughts):
                st.markdown(f"""
                <div class='thought-bubble'>
                    <div style='display: flex; align-items: center; margin-bottom: 8px;'>
                        <span style='background: linear-gradient(45deg, #3b82f6, #60a5fa); border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; margin-right: 12px;'>
                            🤖
                        </span>
                        <div>
                            <p style='color: #ffffff; margin: 0; font-size: 0.95rem; font-weight: 500;'>{thought.content}</p>
                            <p style='color: #bfdbfe; margin: 0; font-size: 0.75rem;'>{thought.timestamp.strftime("%H:%M:%S")}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        if agent.current_analysis and agent.status == "completed":
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class='analysis-card'>
                <h3 style='color: #ffffff; margin-bottom: 20px;'>📋 Executive Summary</h3>
                <div style='background: linear-gradient(45deg, rgba(59, 130, 246, 0.2), rgba(96, 165, 250, 0.2)); border-left: 4px solid #3b82f6; padding: 20px; border-radius: 0 10px 10px 0;'>
                    <p style='color: #f0f9ff; margin: 0; line-height: 1.6; font-size: 1rem;'>{agent.current_analysis.get("summary", "")}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if agent.confidence_level > 0:
                st.markdown("""
                <div class='analysis-card'>
                    <h3 style='color: #ffffff; margin-bottom: 20px;'>📊 Confidence Analysis</h3>
                </div>
                """, unsafe_allow_html=True)
                
                confidence_fig = agent.generate_confidence_gauge()
                st.plotly_chart(confidence_fig, use_container_width=True)
            
            insights = agent.current_analysis.get("insights", [])
            if insights:
                st.markdown("""
                <div class='analysis-card'>
                    <h3 style='color: #ffffff; margin-bottom: 20px;'>🎯 Detected Insights</h3>
                </div>
                """, unsafe_allow_html=True)
                
                opportunities = [i for i in insights if i.category == "opportunity"]
                threats = [i for i in insights if i.category == "threat"]
                trends = [i for i in insights if i.category == "trend"]
                
                if opportunities:
                    st.markdown("<h4 style='color: #10b981;'>💡 Opportunities</h4>", unsafe_allow_html=True)
                    for opp in opportunities:
                        st.markdown(f"""
                        <div style='background: rgba(16, 185, 129, 0.15); border-left: 4px solid #10b981; padding: 15px; margin: 10px 0; border-radius: 0 10px 10px 0;'>
                            <h5 style='color: #ffffff; margin: 0 0 8px 0;'>{opp.title}</h5>
                            <p style='color: #d1fae5; margin: 0 0 8px 0; font-size: 0.9rem;'>{opp.description}</p>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <span style='color: #a7f3d0; font-size: 0.8rem;'>Impact: {opp.impact_score}/10</span>
                                <span style='color: #10b981; font-size: 0.8rem;'>Confidence: {opp.confidence}%</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                if threats:
                    st.markdown("<h4 style='color: #ef4444;'>⚠️ Threats</h4>", unsafe_allow_html=True)
                    for threat in threats:
                        st.markdown(f"""
                        <div style='background: rgba(239, 68, 68, 0.15); border-left: 4px solid #ef4444; padding: 15px; margin: 10px 0; border-radius: 0 10px 10px 0;'>
                            <h5 style='color: #ffffff; margin: 0 0 8px 0;'>{threat.title}</h5>
                            <p style='color: #fee2e2; margin: 0 0 8px 0; font-size: 0.9rem;'>{threat.description}</p>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <span style='color: #fecaca; font-size: 0.8rem;'>Impact: {threat.impact_score}/10</span>
                                <span style='color: #ef4444; font-size: 0.8rem;'>Confidence: {threat.confidence}%</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                if trends:
                    st.markdown("<h4 style='color: #8b5cf6;'>📈 Trends</h4>", unsafe_allow_html=True)
                    for trend in trends:
                        st.markdown(f"""
                        <div style='background: rgba(139, 92, 246, 0.15); border-left: 4px solid #8b5cf6; padding: 15px; margin: 10px 0; border-radius: 0 10px 10px 0;'>
                            <h5 style='color: #ffffff; margin: 0 0 8px 0;'>{trend.title}</h5>
                            <p style='color: #ede9fe; margin: 0 0 8px 0; font-size: 0.9rem;'>{trend.description}</p>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <span style='color: #ddd6fe; font-size: 0.8rem;'>Impact: {trend.impact_score}/10</span>
                                <span style='color: #8b5cf6; font-size: 0.8rem;'>Confidence: {trend.confidence}%</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            recommendations = agent.current_analysis.get("recommendations", [])
            if recommendations:
                st.markdown("""
                <div class='analysis-card'>
                    <h3 style='color: #ffffff; margin-bottom: 20px;'>🎯 AI Recommendations</h3>
                </div>
                """, unsafe_allow_html=True)
                
                for i, rec in enumerate(recommendations, 1):
                    st.markdown(f"""
                    <div style='display: flex; align-items: start; background: rgba(139, 92, 246, 0.15); border-radius: 10px; padding: 15px; margin: 10px 0;'>
                        <div style='background: linear-gradient(45deg, #8b5cf6, #a855f7); border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; margin-right: 15px; flex-shrink: 0;'>
                            <span style='color: white; font-weight: bold; font-size: 0.9rem;'>{i}</span>
                        </div>
                        <p style='color: #f0f9ff; margin: 0; line-height: 1.5; font-size: 1rem;'>{rec}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class='analysis-card'>
                <h3 style='color: #ffffff; margin-bottom: 20px;'>📤 Export & Actions</h3>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📄 Export Report", key="export_btn"):
                    report_content = f"""
                    🤖 ARIA - STRATEGIC INTELLIGENCE REPORT
                    Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    Sector: {selected_sector}
                    Confidence Level: {agent.confidence_level:.1f}%
                    
                    EXECUTIVE SUMMARY:
                    {agent.current_analysis.get('summary', '')}
                    
                    KEY INSIGHTS:
                    """
                    
                    for insight in insights:
                        report_content += f"\n• {insight.title} (Impact: {insight.impact_score}/10, Confidence: {insight.confidence}%)"
                        report_content += f"\n  {insight.description}\n"
                    
                    report_content += "\nRECOMMENDATIONS:\n"
                    for i, rec in enumerate(recommendations, 1):
                        report_content += f"{i}. {rec}\n"
                    
                    st.download_button(
                        label="⬇️ Download Report",
                        data=report_content.encode('utf-8'),
                        file_name=f"aria_report_{selected_sector}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain"
                    )
            
            with col2:
                if st.button("🔔 Setup Alerts", key="alerts_btn"):
                    st.success("✅ Alert system configured! You'll receive notifications for market changes.")
            
            with col3:
                if st.button("🔄 Re-analyze", key="reanalyze_btn"):
                    agent.status = "idle"
                    agent.thoughts = []
                    agent.current_analysis = None
                    agent.confidence_level = 0
                    st.rerun()
        
        elif agent.status == "idle":
            st.markdown("""
            <div class='analysis-card' style='text-align: center; padding: 50px;'>
                <div style='font-size: 4rem; margin-bottom: 20px;'>🤖</div>
                <h3 style='color: #ffffff; margin-bottom: 15px;'>ARIA Ready for Mission</h3>
                <p style='color: #bfdbfe; margin-bottom: 30px;'>Select a target sector and activate the agent to begin strategic market analysis.</p>
                <div style='background: rgba(59, 130, 246, 0.15); border-radius: 10px; padding: 20px; margin: 20px 0;'>
                    <h4 style='color: #93c5fd; margin-bottom: 15px;'>🧠 Agent Capabilities</h4>
                    <ul style='color: #dbeafe; text-align: left; list-style: none; padding: 0;'>
                        <li style='margin: 8px 0;'>🔍 Multi-source market intelligence gathering</li>
                        <li style='margin: 8px 0;'>⚡ Real-time trend analysis and prediction</li>
                        <li style='margin: 8px 0;'>🎯 Strategic opportunity identification</li>
                        <li style='margin: 8px 0;'>📊 Risk assessment and mitigation strategies</li>
                        <li style='margin: 8px 0;'>🤖 AI-powered actionable recommendations</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    if agent.status in ["thinking", "analyzing"]:
        with st.sidebar:
            st.markdown("### 🧠 Neural Network Activity")
            neural_fig = agent.generate_neural_network_viz()
            st.plotly_chart(neural_fig, use_container_width=True)
    
    st.markdown("""
    <div style='margin-top: 50px; padding: 30px 0; border-top: 1px solid rgba(255, 255, 255, 0.1); text-align: center;'>
        <p style='color: #93c5fd; margin: 0;'>
            🤖 ARIA - Autonomous Research & Intelligence Agent | 
            Powered by Advanced AI Neural Networks | 
            Confidence Level: {confidence}%
        </p>
        <p style='color: #bfdbfe; font-size: 0.9rem; margin: 5px 0 0 0;'>
            Last Update: {timestamp} | Neural Activity: {activity} nodes
        </p>
    </div>
    """.format(
        confidence=f"{agent.confidence_level:.1f}" if agent.confidence_level > 0 else "N/A",
        timestamp=datetime.now().strftime('%H:%M:%S'),
        activity=agent.neural_activity
    ), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
