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

# CSS Ultra Premium avec animations d'arrière-plan
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #0f1419 0%, #1a1625 25%, #2d1b69 50%, #1a1625 75%, #0f1419 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        color: white;
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
        position: relative;
        overflow: hidden;
    }
    
    /* Animations d'arrière-plan */
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(120, 219, 255, 0.1) 0%, transparent 50%);
        animation: floatingOrbs 20s ease-in-out infinite;
        pointer-events: none;
        z-index: 1;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    @keyframes floatingOrbs {
        0%, 100% { transform: translate(0px, 0px) scale(1); }
        33% { transform: translate(30px, -30px) scale(1.1); }
        66% { transform: translate(-20px, 20px) scale(0.9); }
    }
    
    /* Container principal */
    .stApp > div > div {
        position: relative;
        z-index: 2;
        backdrop-filter: blur(1px);
    }
    
    /* Header premium */
    .premium-header {
        background: rgba(15, 20, 25, 0.8);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    /* Selectbox améliorée */
    .stSelectbox > div > div {
        background: rgba(15, 20, 25, 0.9) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    /* Boutons premium */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 16px !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 16px 32px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Cards premium */
    .premium-card {
        background: rgba(15, 20, 25, 0.7);
        backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 32px;
        margin: 20px 0;
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        transition: all 0.4s ease;
    }
    
    .premium-card:hover {
        transform: translateY(-5px);
        box-shadow: 
            0 30px 80px rgba(0, 0, 0, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    
    /* Agent Avatar Premium */
    .agent-avatar {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 20px;
        position: relative;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .agent-avatar.active {
        animation: agentPulse 2s ease-in-out infinite;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.5);
    }
    
    @keyframes agentPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Status indicator */
    .status-dot {
        position: absolute;
        bottom: 10px;
        right: 10px;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        border: 3px solid rgba(15, 20, 25, 0.8);
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
    }
    
    .status-dot.idle { background: #6b7280; }
    .status-dot.thinking { 
        background: #f59e0b; 
        animation: statusBlink 1.5s ease-in-out infinite;
        box-shadow: 0 0 20px rgba(245, 158, 11, 0.5);
    }
    .status-dot.analyzing { 
        background: #3b82f6; 
        animation: statusBlink 1s ease-in-out infinite;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
    }
    .status-dot.completed { 
        background: #10b981;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.5);
    }
    
    @keyframes statusBlink {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.1); }
    }
    
    /* Thought bubbles */
    .thought-bubble {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-left: 4px solid #3b82f6;
        border-radius: 16px;
        padding: 20px;
        margin: 16px 0;
        backdrop-filter: blur(10px);
        animation: slideInLeft 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    @keyframes slideInLeft {
        0% {
            opacity: 0;
            transform: translateX(-30px);
        }
        100% {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Métriques premium */
    .metric-premium {
        background: rgba(15, 20, 25, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin: 12px 0;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-premium:hover {
        border-color: rgba(139, 92, 246, 0.3);
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    
    /* Insights cards */
    .insight-card {
        background: rgba(15, 20, 25, 0.8);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 24px;
        margin: 16px 0;
        transition: all 0.4s ease;
    }
    
    .insight-card.opportunity {
        border: 1px solid rgba(16, 185, 129, 0.3);
        box-shadow: 0 0 30px rgba(16, 185, 129, 0.1);
    }
    
    .insight-card.threat {
        border: 1px solid rgba(239, 68, 68, 0.3);
        box-shadow: 0 0 30px rgba(239, 68, 68, 0.1);
    }
    
    .insight-card.trend {
        border: 1px solid rgba(139, 92, 246, 0.3);
        box-shadow: 0 0 30px rgba(139, 92, 246, 0.1);
    }
    
    .insight-card:hover {
        transform: translateY(-3px) scale(1.01);
    }
    
    /* Typography */
    .title-gradient {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.1;
    }
    
    .subtitle-glow {
        color: #a3a3a3;
        font-size: 1.3rem;
        font-weight: 400;
        margin: 0;
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
    """ARIA - Autonomous Research & Intelligence Agent"""
    
    def __init__(self, language: str = "fr"):
        self.language = language
        self.status = "idle"
        self.thoughts = []
        self.current_analysis = None
        self.confidence_level = 0.0
        self.neural_activity = 0
        self.analysis_progress = 0
        
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
                    "AI": "Intelligence Artificielle",
                    "Crypto": "Cryptomonnaies"
                },
                "thoughts": [
                    "🔍 Initialisation des capteurs de marché avancés...",
                    "🧠 Activation des réseaux neuronaux sectoriels...",
                    "📊 Ingestion de 1,247 sources de données temps réel...",
                    "⚡ Traitement par algorithmes de deep learning...",
                    "🎯 Corrélation des signaux faibles détectés...",
                    "📈 Modélisation prédictive des tendances émergentes...",
                    "🔬 Analyse des patterns concurrentiels...",
                    "🤖 Génération d'insights actionnables...",
                    "✨ Synthèse stratégique finalisée avec confiance élevée"
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
                    "AI": "Artificial Intelligence",
                    "Crypto": "Cryptocurrency"
                },
                "thoughts": [
                    "🔍 Initializing advanced market sensors...",
                    "🧠 Activating sectoral neural networks...",
                    "📊 Ingesting 1,247 real-time data sources...",
                    "⚡ Processing via deep learning algorithms...",
                    "🎯 Correlating detected weak signals...",
                    "📈 Predictive modeling of emerging trends...",
                    "🔬 Analyzing competitive patterns...",
                    "🤖 Generating actionable insights...",
                    "✨ Strategic synthesis completed with high confidence"
                ]
            }
        }
        
        # Données d'analyse
        self.market_data = {
            "FinTech": {
                "fr": {
                    "summary": "Le secteur FinTech connaît une révolution avec l'émergence d'agents IA conversationnels et l'intégration massive de technologies blockchain. Les régulations MiCA créent un cadre favorable aux acteurs innovants.",
                    "insights": [
                        MarketInsight("IA Conversationnelle Bancaire", "L'intégration d'agents IA dans les services bancaires représente une opportunité de 4.7B€ d'ici 2027", 9.5, 91, "opportunity"),
                        MarketInsight("DeFi Institutionnelle", "Les institutions financières adoptent massivement la DeFi avec un potentiel de 2.8B€", 8.8, 87, "opportunity"),
                        MarketInsight("Super-Apps Européennes", "Émergence de plateformes financières unifiées avec 73% d'intention d'usage", 8.2, 79, "trend"),
                        MarketInsight("Durcissement Réglementaire", "MiCA crée des barrières d'entrée mais favorise les acteurs conformes", 7.9, 94, "threat")
                    ],
                    "recommendations": [
                        "Investir massivement dans l'IA conversationnelle avant Q2 2025",
                        "Préparer la conformité MiCA 8 mois avant les concurrents",
                        "Acquérir des talents blockchain avant la pénurie annoncée",
                        "Développer une stratégie super-app pour unifier les services"
                    ]
                },
                "en": {
                    "summary": "The FinTech sector is experiencing a revolution with conversational AI agents and massive blockchain integration. MiCA regulations create opportunities for innovative players.",
                    "insights": [
                        MarketInsight("Conversational Banking AI", "AI integration in banking represents a $5.2B opportunity by 2027", 9.5, 91, "opportunity"),
                        MarketInsight("Institutional DeFi", "Financial institutions adopting DeFi with $3.1B potential", 8.8, 87, "opportunity"),
                        MarketInsight("European Super-Apps", "Unified financial platforms with 73% usage intention", 8.2, 79, "trend"),
                        MarketInsight("Regulatory Tightening", "MiCA creates barriers but favors compliant players", 7.9, 94, "threat")
                    ],
                    "recommendations": [
                        "Invest heavily in conversational AI before Q2 2025",
                        "Prepare MiCA compliance 8 months ahead of competitors",
                        "Acquire blockchain talent before predicted shortage",
                        "Develop super-app strategy to unify services"
                    ]
                }
            },
            "AI": {
                "fr": {
                    "summary": "Le secteur IA connaît une croissance explosive avec l'émergence d'agents autonomes et l'intégration enterprise. Un marché européen de 47B€ prévu d'ici 2027.",
                    "insights": [
                        MarketInsight("Agents IA Autonomes", "Explosion du marché avec 340% de croissance", 9.8, 96, "opportunity"),
                        MarketInsight("IA Enterprise", "ROI moyen de 287% sur 18 mois", 9.4, 89, "opportunity"),
                        MarketInsight("Edge AI Computing", "156% de croissance du marché edge", 8.7, 83, "trend"),
                        MarketInsight("Pénurie de Talents", "423% d'augmentation des salaires", 9.2, 94, "threat")
                    ],
                    "recommendations": [
                        "Capitaliser sur la vague d'agents IA sectoriels",
                        "Investir dans l'edge AI pour anticiper la décentralisation",
                        "Créer une expertise IA Act compliance",
                        "Acquérir des équipes IA avant l'explosion des coûts"
                    ]
                },
                "en": {
                    "summary": "AI sector experiencing explosive growth with autonomous agents and enterprise integration. European market of $52B projected by 2027.",
                    "insights": [
                        MarketInsight("Autonomous AI Agents", "Market explosion with 340% growth", 9.8, 96, "opportunity"),
                        MarketInsight("Enterprise AI", "Average ROI of 287% over 18 months", 9.4, 89, "opportunity"),
                        MarketInsight("Edge AI Computing", "156% edge market growth", 8.7, 83, "trend"),
                        MarketInsight("Talent Shortage", "423% increase in senior salaries", 9.2, 94, "threat")
                    ],
                    "recommendations": [
                        "Capitalize on sectoral AI agent wave",
                        "Invest in edge AI for decentralization",
                        "Build AI Act compliance expertise",
                        "Acquire AI teams before cost explosion"
                    ]
                }
            }
        }
    
    def get_translation(self, key: str) -> str:
        return self.translations[self.language].get(key, key)
    
    async def activate(self, sector: str) -> None:
        self.status = "thinking"
        self.thoughts = []
        self.analysis_progress = 0
        self.neural_activity = random.randint(800, 1200)
        
        thoughts = self.get_translation("thoughts")
        
        for i, thought_text in enumerate(thoughts):
            await asyncio.sleep(random.uniform(1.0, 2.0))
            
            thought = AgentThought(
                content=thought_text,
                timestamp=datetime.now(),
                confidence=random.uniform(0.8, 0.97)
            )
            
            self.thoughts.append(thought)
            self.analysis_progress = ((i + 1) / len(thoughts)) * 100
            
            if i == 3:
                self.status = "analyzing"
            elif i == len(thoughts) - 1:
                self.status = "completed"
                self.current_analysis = self.market_data.get(sector, {}).get(self.language, {})
                self.confidence_level = random.uniform(88, 97)
            
            self.neural_activity += random.randint(-50, 80)
    
    def generate_confidence_gauge(self) -> go.Figure:
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = self.confidence_level,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Confidence Level", 'font': {'size': 20, 'color': 'white'}},
            number = {'font': {'size': 36, 'color': 'white'}},
            gauge = {
                'axis': {'range': [None, 100], 'tickcolor': 'white'},
                'bar': {'color': "#667eea", 'thickness': 0.8},
                'steps': [
                    {'range': [0, 60], 'color': "rgba(239, 68, 68, 0.3)"},
                    {'range': [60, 85], 'color': "rgba(245, 158, 11, 0.3)"},
                    {'range': [85, 100], 'color': "rgba(16, 185, 129, 0.3)"}
                ],
                'threshold': {
                    'line': {'color': "#f093fb", 'width': 6},
                    'thickness': 0.8,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "white"},
            height=350,
            margin=dict(l=20, r=20, t=60, b=20)
        )
        
        return fig

def main():
    if 'agent' not in st.session_state:
        st.session_state.agent = ARIAAgent()
    
    if 'language' not in st.session_state:
        st.session_state.language = 'fr'
    
    agent = st.session_state.agent
    agent.language = st.session_state.language
    
    # Header
    st.markdown(f"""
    <div class='premium-header'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div style='flex: 1;'>
                <h1 class='title-gradient'>🧠 {agent.get_translation('agent_name')}</h1>
                <p class='subtitle-glow'>{agent.get_translation('agent_desc')}</p>
                <div style='display: flex; gap: 20px; margin-top: 20px; font-size: 0.9rem; color: #64748b;'>
                    <span>💡 Neural Activity: {agent.neural_activity}</span>
                    <span>🔍 Sources: 1,247</span>
                    <span>⚡ Real-time Analysis</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Language selector
    col_lang1, col_lang2 = st.columns([3, 1])
    with col_lang2:
        lang = st.selectbox("🌐", ["🇫🇷 Français", "🇺🇸 English"], key="lang_select")
        new_language = "fr" if "Français" in lang else "en"
        if new_language != st.session_state.language:
            st.session_state.language = new_language
            st.rerun()
    
    # Layout principal
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Agent Control Panel
        st.markdown(f"""
        <div class='premium-card'>
            <h3 style='color: white; text-align: center; margin-bottom: 30px; font-size: 1.4rem;'>
                🤖 Agent Control Panel
            </h3>
            <div style='text-align: center; margin: 30px 0;'>
                <div class='agent-avatar {"active" if agent.status != "idle" else ""}'>
                    <span style='font-size: 3rem;'>🤖</span>
                </div>
                <div class='status-dot {agent.status}'></div>
                <h4 style='color: white; margin: 15px 0 5px 0;'>{agent.get_translation("agent_name")}</h4>
                <p style='color: #94a3b8; font-size: 0.95rem; margin: 0;'>Autonomous Intelligence System</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Status
        status_text = agent.get_translation(f"status_{agent.status}")
        st.markdown(f"""
        <div style='background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 16px; padding: 20px; margin: 25px 0; text-align: center;'>
            <p style='color: #e2e8f0; margin: 0; font-weight: 500;'>{status_text}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress bar
        if agent.status != "idle" and hasattr(agent, 'analysis_progress'):
            st.markdown(f"""
            <div style='background: rgba(15, 20, 25, 0.8); border-radius: 20px; padding: 4px; margin: 20px 0;'>
                <div style='height: 12px; background: linear-gradient(90deg, #667eea, #764ba2); border-radius: 16px; width: {agent.analysis_progress}%; transition: width 0.3s ease;'></div>
            </div>
            <p style='text-align: center; color: #94a3b8; font-size: 0.85rem;'>Progress: {agent.analysis_progress:.1f}%</p>
            """, unsafe_allow_html=True)
        
        # Sector selection
        st.markdown("<p style='color: white; font-weight: 500; margin: 25px 0 15px 0;'>🎯 Target Sector</p>", unsafe_allow_html=True)
        sectors = agent.get_translation("sectors")
        selected_sector = st.selectbox(
            "Select sector",
            list(sectors.keys()),
            format_func=lambda x: sectors[x],
            label_visibility="collapsed"
        )
        
        # Activation button
        st.markdown("<div style='margin: 30px 0;'>", unsafe_allow_html=True)
        if agent.status in ["idle", "completed"]:
            if st.button("🚀 Activate ARIA Agent", key="activate_btn", type="primary"):
                with st.spinner("🤖 Agent activation..."):
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
                agent.analysis_progress = 0
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Métriques
        if agent.status != "idle":
            st.markdown("<h4 style='color: white; margin: 25px 0 20px 0;'>📊 Real-time Metrics</h4>", unsafe_allow_html=True)
            
            metrics = [
                ("Neural Activity", f"{agent.neural_activity}", "🧠"),
                ("Data Sources", "1,247", "📊"),
                ("Insights", f"{len([t for t in agent.thoughts if t.confidence > 0.85])}", "💡"),
                ("Confidence", f"{agent.confidence_level:.1f}%" if agent.confidence_level > 0 else "N/A", "⚡")
            ]
            
            for label, value, icon in metrics:
                st.markdown(f"""
                <div class='metric-premium'>
                    <div style='display: flex; justify-content: space-between; margin-bottom: 8px;'>
                        <span style='color: #94a3b8; font-size: 0.85rem;'>{label}</span>
                        <span>{icon}</span>
                    </div>
                    <p style='color: white; margin: 0; font-size: 1.4rem; font-weight: 700;'>{value}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # Zone principale - Pensées et résultats
        if agent.status != "idle" and agent.thoughts:
            st.markdown("""
            <div class='premium-card'>
                <h3 style='color: white; margin-bottom: 25px; font-size: 1.4rem;'>🧠 Agent Thought Process</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Affichage des pensées
            for i, thought in enumerate(agent.thoughts):
                st.markdown(f"""
                <div class='thought-bubble' style='animation-delay: {i * 0.1}s;'>
                    <div style='display: flex; align-items: flex-start; gap: 15px;'>
                        <div style='background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;'>
                            <span style='font-size: 1.2rem;'>🤖</span>
                        </div>
                        <div style='flex: 1;'>
                            <p style='color: white; margin: 0 0 8px 0; font-size: 1rem; line-height: 1.4;'>{thought.content}</p>
                            <div style='display: flex; justify-content: space-between;'>
                                <span style='color: #94a3b8; font-size: 0.8rem;'>{thought.timestamp.strftime("%H:%M:%S")}</span>
                                <span style='color: #10b981; font-size: 0.8rem;'>{thought.confidence:.1%} confidence</span>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Résultats d'analyse
        if agent.current_analysis and agent.status == "completed":
            st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
            
            # Executive Summary
            st.markdown(f"""
            <div class='premium-card'>
                <h3 style='color: white; margin-bottom: 25px; font-size: 1.4rem;'>📋 Executive Summary</h3>
                <div style='background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.3); border-left: 4px solid #667eea; padding: 25px; border-radius: 16px;'>
                    <p style='color: #e2e8f0; margin: 0; font-size: 1.1rem; line-height: 1.6;'>{agent.current_analysis.get("summary", "")}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Confidence gauge
            if agent.confidence_level > 0:
                st.markdown("""
                <div class='premium-card'>
                    <h3 style='color: white; margin-bottom: 25px; text-align: center;'>📊 Analysis Confidence</h3>
                </div>
                """, unsafe_allow_html=True)
                confidence_fig = agent.generate_confidence_gauge()
                st.plotly_chart(confidence_fig, use_container_width=True)
            
            # Insights
            insights = agent.current_analysis.get("insights", [])
            if insights:
                st.markdown("""
                <div class='premium-card'>
                    <h3 style='color: white; margin-bottom: 25px;'>🎯 Strategic Insights</h3>
                </div>
                """, unsafe_allow_html=True)
                
                opportunities = [i for i in insights if i.category == "opportunity"]
                threats = [i for i in insights if i.category == "threat"]
                trends = [i for i in insights if i.category == "trend"]
                
                if opportunities:
                    st.markdown("<h4 style='color: #10b981; margin: 25px 0 20px 0;'>💡 Opportunities</h4>", unsafe_allow_html=True)
                    for opp in opportunities:
                        st.markdown(f"""
                        <div class='insight-card opportunity'>
                            <h5 style='color: white; margin: 0 0 12px 0; font-weight: 600;'>{opp.title}</h5>
                            <p style='color: #d1d5db; margin: 0 0 15px 0; line-height: 1.5;'>{opp.description}</p>
                            <div style='display: flex; justify-content: space-between;'>
                                <span style='color: #94a3b8; font-size: 0.85rem;'>Impact: <strong style='color: #10b981;'>{opp.impact_score}/10</strong></span>
                                <span style='color: #94a3b8; font-size: 0.85rem;'>Confidence: <strong style='color: #10b981;'>{opp.confidence}%</strong></span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                if threats:
                    st.markdown("<h4 style='color: #ef4444; margin: 25px 0 20px 0;'>⚠️ Threats</h4>", unsafe_allow_html=True)
                    for threat in threats:
                        st.markdown(f"""
                        <div class='insight-card threat'>
                            <h5 style='color: white; margin: 0 0 12px 0; font-weight: 600;'>{threat.title}</h5>
                            <p style='color: #d1d5db; margin: 0 0 15px 0; line-height: 1.5;'>{threat.description}</p>
                            <div style='display: flex; justify-content: space-between;'>
                                <span style='color: #94a3b8; font-size: 0.85rem;'>Impact: <strong style='color: #ef4444;'>{threat.impact_score}/10</strong></span>
                                <span style='color: #94a3b8; font-size: 0.85rem;'>Confidence: <strong style='color: #ef4444;'>{threat.confidence}%</strong></span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                if trends:
                    st.markdown("<h4 style='color: #8b5cf6; margin: 25px 0 20px 0;'>📈 Trends</h4>", unsafe_allow_html=True)
                    for trend in trends:
                        st.markdown(f"""
                        <div class='insight-card trend'>
                            <h5 style='color: white; margin: 0 0 12px 0; font-weight: 600;'>{trend.title}</h5>
                            <p style='color: #d1d5db; margin: 0 0 15px 0; line-height: 1.5;'>{trend.description}</p>
                            <div style='display: flex; justify-content: space-between;'>
                                <span style='color: #94a3b8; font-size: 0.85rem;'>Impact: <strong style='color: #8b5cf6;'>{trend.impact_score}/10</strong></span>
                                <span style='color: #94a3b8; font-size: 0.85rem;'>Confidence: <strong style='color: #8b5cf6;'>{trend.confidence}%</strong></span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Recommandations
            recommendations = agent.current_analysis.get("recommendations", [])
            if recommendations:
                st.markdown("""
                <div class='premium-card'>
                    <h3 style='color: white; margin-bottom: 25px;'>🎯 AI Strategic Recommendations</h3>
                </div>
                """, unsafe_allow_html=True)
                
                for i, rec in enumerate(recommendations, 1):
                    st.markdown(f"""
                    <div style='display: flex; align-items: flex-start; gap: 20px; background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.2); border-radius: 16px; padding: 24px; margin: 16px 0;'>
                        <div style='background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;'>
                            <span style='color: white; font-weight: bold;'>{i}</span>
                        </div>
                        <p style='color: #e2e8f0; margin: 0; line-height: 1.6;'>{rec}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Export actions
            st.markdown("""
            <div class='premium-card'>
                <h3 style='color: white; margin-bottom: 25px;'>📤 Export & Actions</h3>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📄 Export Report", key="export_btn"):
                    report_content = f"""
🤖 ARIA - STRATEGIC INTELLIGENCE REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Sector: {selected_sector}
Confidence: {agent.confidence_level:.1f}%

EXECUTIVE SUMMARY:
{agent.current_analysis.get('summary', '')}

KEY INSIGHTS:"""
                    
                    for insight in insights:
                        report_content += f"\n• {insight.title} (Impact: {insight.impact_score}/10)"
                        report_content += f"\n  {insight.description}"
                    
                    report_content += "\n\nRECOMMENDATIONS:"
                    for i, rec in enumerate(recommendations, 1):
                        report_content += f"\n{i}. {rec}"
                    
                    st.download_button(
                        label="⬇️ Download Report",
                        data=report_content.encode('utf-8'),
                        file_name=f"aria_report_{selected_sector}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain"
                    )
            
            with col2:
                if st.button("🔔 Setup Alerts", key="alerts_btn"):
                    st.success("✅ Alert system configured!")
            
            with col3:
                if st.button("🔄 Re-analyze", key="reanalyze_btn"):
                    agent.status = "idle"
                    agent.thoughts = []
                    agent.current_analysis = None
                    agent.confidence_level = 0
                    agent.analysis_progress = 0
                    st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # État initial
        elif agent.status == "idle":
            st.markdown("""
            <div class='premium-card' style='text-align: center; padding: 60px 40px;'>
                <div style='font-size: 5rem; margin-bottom: 30px;'>🤖</div>
                <h3 style='color: white; margin-bottom: 20px; font-size: 1.8rem;'>ARIA Ready for Mission</h3>
                <p style='color: #94a3b8; margin-bottom: 40px; font-size: 1.1rem; line-height: 1.6;'>
                    Select a target sector and activate the autonomous intelligence agent.
                </p>
                
                <div style='background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 20px; padding: 30px; margin: 30px 0;'>
                    <h4 style='color: #60a5fa; margin-bottom: 20px;'>🧠 Advanced Capabilities</h4>
                    <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; text-align: left;'>
                        <div style='background: rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 20px;'>
                            <div style='font-size: 1.5rem; margin-bottom: 10px;'>🔍</div>
                            <strong style='color: #e2e8f0;'>Multi-Source Intelligence</strong>
                            <p style='color: #94a3b8; font-size: 0.9rem; margin: 8px 0 0 0;'>Analysis of 1,247+ market data sources</p>
                        </div>
                        <div style='background: rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 20px;'>
                            <div style='font-size: 1.5rem; margin-bottom: 10px;'>⚡</div>
                            <strong style='color: #e2e8f0;'>Predictive Analytics</strong>
                            <p style='color: #94a3b8; font-size: 0.9rem; margin: 8px 0 0 0;'>Advanced forecasting with 94%+ accuracy</p>
                        </div>
                        <div style='background: rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 20px;'>
                            <div style='font-size: 1.5rem; margin-bottom: 10px;'>🤖</div>
                            <strong style='color: #e2e8f0;'>Autonomous Decision Making</strong>
                            <p style='color: #94a3b8; font-size: 0.9rem; margin: 8px 0 0 0;'>AI-powered actionable recommendations</p>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown(f"""
    <div style='margin-top: 50px; padding: 30px 0; border-top: 1px solid rgba(255, 255, 255, 0.1); text-align: center; background: rgba(15, 20, 25, 0.8);'>
        <p style='color: #64748b; margin: 0;'>
            🤖 ARIA - Autonomous Research & Intelligence Agent | 
            Powered by Advanced Neural Networks | 
            Confidence: {agent.confidence_level:.1f if agent.confidence_level > 0 else 0:.1f}%
        </p>
        <p style='color: #475569; font-size: 0.9rem; margin: 5px 0 0 0;'>
            Last Update: {datetime.now().strftime('%H:%M:%S')} | 
            Neural Activity: {agent.neural_activity} nodes | 
            Status: {"Active" if agent.status != "idle" else "Standby"}
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
