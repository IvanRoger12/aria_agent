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
        
        # Données d'analyse enrichies
        self.market_data = {
            "FinTech": {
                "fr": {
                    "summary": "Le secteur FinTech connaît une consolidation majeure avec l'émergence de super-apps et l'intégration massive de l'IA. Les régulations MiCA créent des opportunités pour les acteurs conformes.",
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
            }
        }
    
    def get_translation(self, key: str) -> str:
        """Obtient la traduction pour une clé donnée"""
        return self.translations[self.language].get(key, key)
    
    async def activate(self, sector: str):
        """Active l'agent pour analyser un secteur"""
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
                self.current_analysis = self.market_data.get(sector, {}).get(self.language, self.market_data["FinTech"]["fr"])
                self.confidence_level = random.uniform(85, 95)
            
            self.neural_activity += random.randint(-30, 50)
            yield thought
    
    def generate_confidence_gauge(self) -> go.Figure:
        """Génère un graphique de confiance"""
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = self.confidence_level,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "AI Confidence", 'font': {'color': 'white', 'size': 16}},
            delta = {'reference': 80},
            gauge = {
                'axis': {'range': [None, 100], 'tickcolor': 'white'},
                'bar': {'color': "#3b82f6"},
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
            }
        ))
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "white"},
            height=280
        )
        
        return fig
    
    def generate_neural_network_viz(self) -> go.Figure:
        """Visualisation réseau neuronal"""
        n_nodes = 20
        x = [random.uniform(0, 10) for _ in range(n_nodes)]
        y = [random.uniform(0, 10) for _ in range(n_nodes)]
        
        # Connexions
        edge_x = []
        edge_y = []
        
        for i in range(n_nodes):
            for j in range(i+1, min(i+4, n_nodes)):
                if random.random() > 0.6:
                    edge_x.extend([x[i], x[j], None])
                    edge_y.extend([y[i], y[j], None])
        
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='#3b82f6'),
            hoverinfo='none',
            mode='lines',
            opacity=0.6
        )
        
        node_trace = go.Scatter(
            x=x, y=y,
            mode='markers',
            hoverinfo='none',
            marker=dict(
                size=8,
                color='#60a5fa',
                line=dict(width=2, color='#3b82f6')
            )
        )
        
        fig = go.Figure(data=[edge_trace, node_trace])
        fig.update_layout(
            showlegend=False,
            margin=dict(b=20,l=5,r=5,t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=300
        )
        
        return fig
    
    def chat_with_agent(self, message: str, sector: str) -> str:
        """Chat simple avec l'agent"""
        responses = {
            "fr": {
                "default": f"D'après mon analyse du secteur {sector}, les tendances principales sont l'intégration IA et la consolidation du marché."
            },
            "en": {
                "default": f"According to my {sector} analysis, main trends are AI integration and market consolidation."
            }
        }
        
        return responses[self.language]["default"]

# Interface principale
def main():
    # Initialisation de l'état
    if 'agent' not in st.session_state:
        st.session_state.agent = ARIAAgent()
    
    if 'language' not in st.session_state:
        st.session_state.language = 'fr'
    
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    
    agent = st.session_state.agent
    agent.language = st.session_state.language
    
    # Header
    col1, col2 = st.columns([8, 1])
    
    with col1:
        st.markdown(f"""
        <div class='premium-header'>
            <h1 class='premium-title'>🧠 {agent.get_translation('agent_name')}</h1>
            <p class='premium-subtitle'>{agent.get_translation('agent_desc')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        lang = st.selectbox("🌐", ["🇫🇷 FR", "🇺🇸 EN"])
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
        
        # Avatar agent
        status_class = f"status-{agent.status}"
        avatar_class = "agent-avatar active" if agent.status != "idle" else "agent-avatar"
        
        st.markdown(f"""
        <div style='text-align: center; margin: 25px 0;'>
            <div class='{avatar_class}'>
                <div class='agent-core'>🤖</div>
            </div>
            <h4 style='color: white; margin: 15px 0;'>{agent.get_translation("agent_name")}</h4>
            <div>
                <span class='status-indicator {status_class}'></span>
                <span style='color: white; font-size: 0.9rem;'>{agent.get_translation(f"status_{agent.status}")}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Configuration
        st.markdown("<h4 style='color: white;'>🎯 Target Sector</h4>", unsafe_allow_html=True)
        
        sectors = agent.get_translation("sectors")
        selected_sector = st.selectbox(
            "Select sector",
            list(sectors.keys()),
            format_func=lambda x: sectors[x],
            label_visibility="collapsed"
        )
        
        # Bouton d'activation
        st.markdown("<br>", unsafe_allow_html=True)
        
        if agent.status in ["idle", "completed"]:
            if st.button("🚀 ACTIVATE ARIA", type="primary"):
                # Simulation de l'activation
                agent.status = "thinking"
                agent.thoughts = []
                thoughts = agent.get_translation("thoughts")
                
                for i, thought_text in enumerate(thoughts):
                    time.sleep(random.uniform(0.5, 1.0))
                    
                    thought = AgentThought(
                        content=thought_text,
                        timestamp=datetime.now(),
                        confidence=random.uniform(0.7, 0.95)
                    )
                    
                    agent.thoughts.append(thought)
                    
                    if i == 2:
                        agent.status = "analyzing"
                    elif i == len(thoughts) - 1:
                        agent.status = "completed"
                        agent.current_analysis = agent.market_data.get(selected_sector, {}).get(agent.language, agent.market_data["FinTech"]["fr"])
                        agent.confidence_level = random.uniform(85, 95)
                    
                    agent.neural_activity += random.randint(-30, 50)
                
                st.rerun()
        else:
            if st.button("⏹️ STOP AGENT"):
                agent.status = "idle"
                agent.thoughts = []
                agent.current_analysis = None
                st.rerun()
        
        # Métriques temps réel
        if agent.status != "idle":
            st.markdown("<h4 style='color: white;'>📊 Metrics</h4>", unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{agent.neural_activity}</div>
                <div style='color: #94a3b8; font-size: 0.8rem;'>Neural Nodes</div>
            </div>
            <div class='metric-card'>
                <div class='metric-value'>{agent.confidence_level:.1f}%</div>
                <div style='color: #94a3b8; font-size: 0.8rem;'>Confidence</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Neural Network
        if agent.status in ["thinking", "analyzing", "completed"]:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<h4 style="color: white; text-align: center;">🧠 Neural Network</h4>', unsafe_allow_html=True)
            neural_fig = agent.generate_neural_network_viz()
            st.plotly_chart(neural_fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Zone principale
        if agent.status != "idle" and agent.thoughts:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<h3 style="color: white;">🧠 Agent Thoughts</h3>', unsafe_allow_html=True)
            
            for i, thought in enumerate(agent.thoughts):
                st.markdown(f"""
                <div class='thought-bubble' style='animation-delay: {i*0.2}s;'>
                    <div style='display: flex; align-items: start; gap: 15px;'>
                        <div style='background: linear-gradient(45deg, #3b82f6, #8b5cf6); border-radius: 50%; 
                                    width: 35px; height: 35px; display: flex; align-items: center; justify-content: center;'>
                            🤖
                        </div>
                        <div>
                            <p style='color: white; margin: 0 0 8px 0;'>{thought.content}</p>
                            <span style='color: #94a3b8; font-size: 0.75rem;'>{thought.timestamp.strftime("%H:%M:%S")}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Résultats d'analyse
        if agent.current_analysis and agent.status == "completed":
            st.markdown(f"""
            <div class='glass-card'>
                <h3 style='color: white;'>📋 Executive Summary</h3>
                <div style='background: rgba(59, 130, 246, 0.15); border-left: 4px solid #3b82f6; 
                            padding: 20px; border-radius: 0 15px 15px 0;'>
                    <p style='color: #e2e8f0; margin: 0;'>{agent.current_analysis.get("summary", "")}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Graphique de confiance
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                st.markdown('<div class="glass-card"><h4 style="color: white; text-align: center;">🎯 Confidence</h4></div>', unsafe_allow_html=True)
                confidence_fig = agent.generate_confidence_gauge()
                st.plotly_chart(confidence_fig, use_container_width=True)
            
            with col_chart2:
                st.markdown('<div class="glass-card"><h4 style="color: white; text-align: center;">📈 Activity</h4></div>', unsafe_allow_html=True)
                # Simple bar chart pour l'activité
                fig = go.Figure(data=[go.Bar(x=['Neural Activity'], y=[agent.neural_activity], marker_color='#3b82f6')])
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={'color': "white"},
                    height=280
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Insights
            insights = agent.current_analysis.get("insights", [])
            if insights:
                st.markdown('<div class="glass-card"><h3 style="color: white;">🎯 Strategic Insights</h3></div>', unsafe_allow_html=True)
                
                opportunities = [i for i in insights if i.category == "opportunity"]
                threats = [i for i in insights if i.category == "threat"]
                trends = [i for i in insights if i.category == "trend"]
                
                if opportunities:
                    st.markdown("<h4 style='color: #10b981;'>💎 Opportunities</h4>", unsafe_allow_html=True)
                    for i, opp in enumerate(opportunities):
                        st.markdown(f"""
                        <div class='insight-card opportunity-card' style='animation-delay: {i*0.15}s;'>
                            <h5 style='color: white; margin: 0 0 10px 0;'>💡 {opp.title}</h5>
                            <p style='color: #cbd5e1; margin: 0 0 10px 0;'>{opp.description}</p>
                            <div style='display: flex; gap: 10px;'>
                                <span style='background: rgba(16, 185, 129, 0.2); color: #10b981; 
                                            padding: 4px 8px; border-radius: 12px; font-size: 0.75rem;'>
                                    Impact: {opp.impact_score}/10
                                </span>
                                <span style='background: rgba(59, 130, 246, 0.2); color: #60a5fa; 
                                            padding: 4px 8px; border-radius: 12px; font-size: 0.75rem;'>
                                    {opp.confidence}% Confidence
                                </span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                if threats:
                    st.markdown("<h4 style='color: #ef4444;'>⚠️ Threats</h4>", unsafe_allow_html=True)
                    for i, threat in enumerate(threats):
                        st.markdown(f"""
                        <div class='insight-card threat-card' style='animation-delay: {(len(opportunities)+i)*0.15}s;'>
                            <h5 style='color: white; margin: 0 0 10px 0;'>🚨 {threat.title}</h5>
                            <p style='color: #cbd5e1; margin: 0 0 10px 0;'>{threat.description}</p>
                            <div style='display: flex; gap: 10px;'>
                                <span style='background: rgba(239, 68, 68, 0.2); color: #ef4444; 
                                            padding: 4px 8px; border-radius: 12px; font-size: 0.75rem;'>
                                    Impact: {threat.impact_score}/10
                                </span>
                                <span style='background: rgba(59, 130, 246, 0.2); color: #60a5fa; 
                                            padding: 4px 8px; border-radius: 12px; font-size: 0.75rem;'>
                                    {threat.confidence}% Confidence
                                </span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                if trends:
                    st.markdown("<h4 style='color: #8b5cf6;'>📈 Trends</h4>", unsafe_allow_html=True)
                    for i, trend in enumerate(trends):
                        st.markdown(f"""
                        <div class='insight-card trend-card' style='animation-delay: {(len(opportunities)+len(threats)+i)*0.15}s;'>
                            <h5 style='color: white; margin: 0 0 10px 0;'>📊 {trend.title}</h5>
                            <p style='color: #cbd5e1; margin: 0 0 10px 0;'>{trend.description}</p>
                            <div style='display: flex; gap: 10px;'>
                                <span style='background: rgba(139, 92, 246, 0.2); color: #8b5cf6; 
                                            padding: 4px 8px; border-radius: 12px; font-size: 0.75rem;'>
                                    Impact: {trend.impact_score}/10
                                </span>
                                <span style='background: rgba(59, 130, 246, 0.2); color: #60a5fa; 
                                            padding: 4px 8px; border-radius: 12px; font-size: 0.75rem;'>
                                    {trend.confidence}% Confidence
                                </span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Recommandations
            recommendations = agent.current_analysis.get("recommendations", [])
            if recommendations:
                st.markdown('<div class="glass-card"><h3 style="color: white;">🎯 AI Recommendations</h3></div>', unsafe_allow_html=True)
                
                for i, rec in enumerate(recommendations, 1):
                    st.markdown(f"""
                    <div style='display: flex; align-items: start; gap: 20px; 
                                background: rgba(139, 92, 246, 0.1); border-radius: 15px; 
                                padding: 20px; margin: 15px 0; border-left: 4px solid #8b5cf6;'>
                        <div style='background: linear-gradient(45deg, #8b5cf6, #ec4899); border-radius: 50%; 
                                    width: 40px; height: 40px; display: flex; align-items: center; 
                                    justify-content: center; flex-shrink: 0;'>
                            <span style='color: white; font-weight: bold;'>{i}</span>
                        </div>
                        <p style='color: #e2e8f0; margin: 0;'>{rec}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # État initial
        elif agent.status == "idle":
            st.markdown("""
            <div class='glass-card' style='text-align: center; padding: 60px 40px;'>
                <div style='font-size: 5rem; margin-bottom: 25px;'>🤖</div>
                <h3 style='color: white; margin-bottom: 20px;'>ARIA Ready</h3>
                <p style='color: #94a3b8; margin-bottom: 35px;'>
                    Advanced AI agent ready for strategic market analysis.
                </p>
                <div style='background: rgba(59, 130, 246, 0.1); border-radius: 15px; padding: 30px;'>
                    <h4 style='color: #60a5fa; margin-bottom: 20px;'>🧠 Core Capabilities</h4>
                    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 15px; text-align: left;'>
                        <div style='color: #cbd5e1; font-size: 0.95rem;'>🔍 Market intelligence</div>
                        <div style='color: #cbd5e1; font-size: 0.95rem;'>⚡ Predictive analysis</div>
                        <div style='color: #cbd5e1; font-size: 0.95rem;'>🎯 Opportunity identification</div>
                        <div style='color: #cbd5e1; font-size: 0.95rem;'>📊 Risk assessment</div>
                        <div style='color: #cbd5e1; font-size: 0.95rem;'>🤖 Autonomous decisions</div>
                        <div style='color: #cbd5e1; font-size: 0.95rem;'>📈 Neural processing</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        # Panel chat
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: white; text-align: center;">💬 Chat Interface</h3>', unsafe_allow_html=True)
        
        if agent.current_analysis:
            st.markdown("<h4 style='color: #60a5fa;'>Chat with ARIA</h4>", unsafe_allow_html=True)
            
            for msg in st.session_state.chat_messages[-3:]:
                if msg['role'] == 'user':
                    st.markdown(f"""
                    <div style='background: rgba(59, 130, 246, 0.1); padding: 10px 15px; 
                                border-radius: 15px; margin: 8px 0;'>
                        <p style='color: white; margin: 0; font-size: 0.9rem;'>{msg['content']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='chat-message'>
                        <div style='display: flex; gap: 10px;'>
                            <div style='background: linear-gradient(45deg, #3b82f6, #8b5cf6); 
                                        border-radius: 50%; width: 25px; height: 25px; 
                                        display: flex; align-items: center; justify-content: center;'>
                                🤖
                            </div>
                            <p style='color: #e2e8f0; margin: 0; font-size: 0.9rem;'>{msg['content']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            user_question = st.text_input("Ask ARIA...", key="chat_input")
            
            if user_question:
                st.session_state.chat_messages.append({"role": "user", "content": user_question})
                response = agent.chat_with_agent(user_question, selected_sector)
                st.session_state.chat_messages.append({"role": "assistant", "content": response})
                st.rerun()
        
        else:
            st.markdown("""
            <div style='text-align: center; padding: 20px;'>
                <div style='font-size: 3rem; margin-bottom: 15px; opacity: 0.6;'>💬</div>
                <p style='color: #94a3b8;'>Chat available after analysis completion.</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Export et actions
        if agent.current_analysis:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<h3 style="color: white; text-align: center;">📤 Export</h3>', unsafe_allow_html=True)
            
            if st.button("📄 Generate PDF Report", type="primary"):
                report_content = f"""
🧠 ARIA - STRATEGIC INTELLIGENCE REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Sector: {selected_sector}
Confidence: {agent.confidence_level:.1f}%

EXECUTIVE SUMMARY:
{agent.current_analysis.get('summary', '')}

RECOMMENDATIONS:
"""
                recommendations = agent.current_analysis.get('recommendations', [])
                for i, rec in enumerate(recommendations, 1):
                    report_content += f"{i}. {rec}\n"
                
                st.download_button(
                    label="⬇️ Download Report",
                    data=report_content.encode('utf-8'),
                    file_name=f"ARIA_Report_{selected_sector}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain"
                )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔔 Alerts"):
                    st.success("✅ Alerts configured!")
            
            with col2:
                if st.button("🔄 Re-analyze"):
                    agent.status = "idle"
                    agent.thoughts = []
                    agent.current_analysis = None
                    st.session_state.chat_messages = []
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown(f"""
    <div class='premium-footer'>
        <p style='color: #64748b; margin: 0;'>
            🤖 ARIA - Autonomous Research & Intelligence Agent | Neural Activity: {agent.neural_activity} nodes
        </p>
        <p style='color: #475569; font-size: 0.8rem; margin: 8px 0 0 0;'>
            Last Update: {datetime.now().strftime('%H:%M:%S')} | Version: 2.0.1-beta | Enterprise Ready
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

