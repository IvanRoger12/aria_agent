import streamlit as st
import json
import time
import random
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional
from dataclasses import dataclass
import numpy as np
import math

# Configuration de la page
st.set_page_config(
    page_title="🧠 ARIA - Advanced AI Intelligence System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Ultra-Premium avec effets avancés
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@300;400;700;900&family=JetBrains+Mono:wght@300;400;500;700&family=Space+Grotesk:wght@300;400;500;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a0033 25%, #000a1f 50%, #1a0033 75%, #0a0a0f 100%);
        background-size: 400% 400%;
        animation: holographicShift 20s ease-in-out infinite;
        color: white;
        font-family: 'Space Grotesk', sans-serif;
        position: relative;
        min-height: 100vh;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a0033 25%, #000a1f 50%, #1a0033 75%, #0a0a0f 100%);
        background-size: 400% 400%;
        animation: holographicShift 20s ease-in-out infinite;
    }
    
    @keyframes holographicShift {
        0%, 100% { 
            background-position: 0% 50%;
            filter: hue-rotate(0deg);
        }
        25% { 
            background-position: 100% 50%;
            filter: hue-rotate(90deg);
        }
        50% { 
            background-position: 100% 100%;
            filter: hue-rotate(180deg);
        }
        75% { 
            background-position: 0% 100%;
            filter: hue-rotate(270deg);
        }
    }
    
    #MainMenu, footer, header, .stDeployButton {visibility: hidden !important;}
    .stApp > div:first-child {display: none;}
    
    .block-container {
        background: transparent;
        padding: 2rem 1rem;
        max-width: 1600px;
        position: relative;
        z-index: 1;
    }
    
    .neural-glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(25px) saturate(200%);
        border: 1px solid rgba(0, 245, 255, 0.2);
        border-radius: 24px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), 0 0 20px rgba(0, 245, 255, 0.1);
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1);
    }
    
    .neural-glass-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5), 0 0 40px rgba(0, 245, 255, 0.2);
        border-color: rgba(0, 245, 255, 0.4);
    }
    
    .aria-avatar-container {
        position: relative;
        width: 140px;
        height: 140px;
        margin: 30px auto;
    }
    
    .aria-avatar {
        position: relative;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background: conic-gradient(from 0deg, #00f5ff, #8b5cf6, #ff0080, #8000ff, #00f5ff);
        display: flex;
        align-items: center;
        justify-content: center;
        animation: avatarRotate 8s linear infinite;
        box-shadow: 0 0 30px rgba(0, 245, 255, 0.8);
    }
    
    .aria-avatar.active {
        animation: avatarRotate 3s linear infinite, avatarPulse 2s ease-in-out infinite;
    }
    
    @keyframes avatarRotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes avatarPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    .aria-core {
        width: 110px;
        height: 110px;
        border-radius: 50%;
        background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.3), transparent 50%), linear-gradient(135deg, rgba(14, 165, 233, 0.8), rgba(139, 92, 246, 0.8));
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    .thought-hologram {
        background: linear-gradient(135deg, rgba(0, 245, 255, 0.1) 0%, rgba(139, 92, 246, 0.1) 50%, rgba(236, 72, 153, 0.1) 100%);
        border-left: 3px solid #00f5ff;
        border-radius: 0 20px 20px 0;
        padding: 25px;
        margin: 20px 0;
        backdrop-filter: blur(15px);
        animation: thoughtSlide 1s cubic-bezier(0.34, 1.56, 0.64, 1);
        animation-fill-mode: both;
        box-shadow: 0 8px 25px rgba(0, 245, 255, 0.15);
        position: relative;
        overflow: hidden;
    }
    
    @keyframes thoughtSlide {
        0% {
            transform: translateX(-100px) rotateY(-15deg);
            opacity: 0;
        }
        100% {
            transform: translateX(0) rotateY(0deg);
            opacity: 1;
        }
    }
    
    .neural-metric {
        background: rgba(0, 245, 255, 0.05);
        border: 1px solid rgba(0, 245, 255, 0.2);
        border-radius: 16px;
        padding: 20px;
        margin: 15px 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .neural-metric:hover {
        border-color: #00f5ff;
        box-shadow: 0 0 20px rgba(0, 245, 255, 0.2);
        transform: scale(1.02);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        color: #00f5ff;
        animation: digitalFlicker 3s ease-in-out infinite alternate;
        line-height: 1;
    }
    
    @keyframes digitalFlicker {
        0%, 100% { 
            filter: brightness(1);
            text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
        }
        50% { 
            filter: brightness(1.2);
            text-shadow: 0 0 20px rgba(0, 245, 255, 0.8);
        }
    }
    
    .metric-label {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 8px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, rgba(0, 245, 255, 0.2) 0%, rgba(139, 92, 246, 0.2) 50%, rgba(236, 72, 153, 0.2) 100%) !important;
        color: white !important;
        border: 2px solid #00f5ff !important;
        border-radius: 20px !important;
        font-weight: 600 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        padding: 15px 35px !important;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1) !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 10px 30px rgba(0, 245, 255, 0.4) !important;
        border-color: rgba(255, 255, 255, 0.8) !important;
    }
    
    .stSelectbox > div > div {
        background: rgba(0, 245, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(0, 245, 255, 0.3) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    .aria-header {
        text-align: center;
        padding: 50px 0;
        margin-bottom: 40px;
        position: relative;
    }
    
    .aria-title {
        font-size: 4rem;
        font-weight: 900;
        font-family: 'Orbitron', monospace;
        background: linear-gradient(45deg, #00f5ff 0%, #a78bfa 25%, #ff0080 50%, #8000ff 75%, #00f5ff 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: titleShift 6s ease-in-out infinite;
        margin-bottom: 20px;
        filter: drop-shadow(0 0 30px rgba(0, 245, 255, 0.5));
    }
    
    @keyframes titleShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .aria-subtitle {
        font-size: 1.4rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 300;
        font-family: 'Space Grotesk', sans-serif;
        margin-bottom: 25px;
        animation: subtitleGlow 4s ease-in-out infinite alternate;
    }
    
    @keyframes subtitleGlow {
        0% { text-shadow: 0 0 10px rgba(255, 255, 255, 0.3); }
        100% { text-shadow: 0 0 20px rgba(0, 245, 255, 0.6); }
    }
    
    .neural-stats {
        display: flex;
        justify-content: center;
        gap: 40px;
        margin-top: 30px;
        flex-wrap: wrap;
    }
    
    .neural-stat {
        text-align: center;
    }
    
    .neural-stat-value {
        font-size: 1.8rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        color: #00f5ff;
        animation: statFlicker 2s ease-in-out infinite alternate;
    }
    
    .neural-stat-label {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.6);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 5px;
    }
    
    @keyframes statFlicker {
        0% { opacity: 0.8; }
        100% { opacity: 1; text-shadow: 0 0 15px currentColor; }
    }
    
    .status-indicator {
        display: inline-block;
        width: 14px;
        height: 14px;
        border-radius: 50%;
        margin-right: 12px;
        position: relative;
        animation: statusPulse 2s ease-in-out infinite;
    }
    
    @keyframes statusPulse {
        0%, 100% { 
            opacity: 1; 
            box-shadow: 0 0 10px currentColor; 
        }
        50% { 
            opacity: 0.6; 
            box-shadow: 0 0 20px currentColor; 
        }
    }
    
    .status-idle { background: #64748b; color: #64748b; }
    .status-thinking { background: #f59e0b; color: #f59e0b; }
    .status-analyzing { background: #00f5ff; color: #00f5ff; }
    .status-completed { background: #10b981; color: #10b981; }
    
    .neural-chat {
        background: rgba(0, 245, 255, 0.05);
        border: 1px solid rgba(0, 245, 255, 0.2);
        border-radius: 20px;
        padding: 20px;
        margin: 15px 0;
        animation: chatFloat 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    
    @keyframes chatFloat {
        0% {
            transform: translateX(-30px);
            opacity: 0;
        }
        100% {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .insight-neural {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 18px;
        padding: 25px;
        margin: 18px 0;
        border-left: 4px solid;
        animation: insightFade 0.8s ease-out;
        animation-fill-mode: both;
        backdrop-filter: blur(20px);
        transition: all 0.4s ease;
    }
    
    .insight-neural:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
    }
    
    .opportunity-neural {
        border-left-color: #10b981;
        color: #10b981;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.15);
    }
    
    .threat-neural {
        border-left-color: #ef4444;
        color: #ef4444;
        box-shadow: 0 8px 25px rgba(239, 68, 68, 0.15);
    }
    
    .trend-neural {
        border-left-color: #8b5cf6;
        color: #8b5cf6;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.15);
    }
    
    @keyframes insightFade {
        0% {
            opacity: 0;
            transform: translateY(40px);
        }
        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .aria-footer {
        background: rgba(0, 0, 0, 0.4);
        border-top: 1px solid rgba(0, 245, 255, 0.3);
        padding: 40px 0;
        text-align: center;
        margin-top: 60px;
        backdrop-filter: blur(20px);
    }
    
    @media (max-width: 768px) {
        .aria-title {
            font-size: 2.5rem;
        }
        
        .neural-glass-card {
            padding: 20px;
            margin: 15px 0;
        }
        
        .aria-avatar-container {
            width: 100px;
            height: 100px;
        }
        
        .neural-stats {
            gap: 20px;
        }
    }
    
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.2);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(to bottom, #00f5ff, #8b5cf6);
        border-radius: 4px;
        box-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
    }
</style>
""", unsafe_allow_html=True)

@dataclass
class AgentThought:
    content: str
    timestamp: datetime
    thought_type: str = "analysis"
    confidence: float = 0.0
    neural_pattern: str = "standard"

@dataclass
class MarketInsight:
    title: str
    description: str
    impact_score: float
    confidence: float
    category: str
    urgency: str = "medium"

class ARIAAgent:
    """ARIA - Advanced Research Intelligence Agent"""
    
    def __init__(self, language: str = "fr"):
        self.language = language
        self.status = "idle"
        self.thoughts = []
        self.current_analysis = None
        self.confidence_level = 0.0
        self.neural_activity = random.randint(850, 950)
        self.quantum_coherence = 85.0
        self.processing_nodes = 0
        self.data_streams = 847
        
        self.translations = {
            "fr": {
                "agent_name": "ARIA",
                "agent_desc": "Système d'Intelligence Artificielle de Recherche Autonome",
                "status_idle": "💤 Système en veille - Réseaux neuronaux prêts",
                "status_thinking": "🧠 Initialisation des matrices cognitives...",
                "status_analyzing": "⚡ Traitement neuronal multi-dimensionnel actif",
                "status_completed": "✨ Analyse terminée - Insights synthétisés",
                "sectors": {
                    "FinTech": "Technologies Financières",
                    "HealthTech": "Technologies Médicales", 
                    "SaaS": "Logiciels as a Service",
                    "E-commerce": "Commerce Numérique",
                    "PropTech": "Technologies Immobilières",
                    "EdTech": "Technologies Éducatives"
                },
                "thoughts": [
                    "🔮 Initialisation des capteurs quantiques multi-dimensionnels...",
                    "🌐 Synchronisation avec les flux de données globaux...",
                    "🧠 Activation des réseaux neuronaux spécialisés sectoriels...",
                    "📊 Ingestion de 847 sources de données temps réel...",
                    "⚡ Traitement par algorithmes d'apprentissage profond...",
                    "🎯 Détection et corrélation des signaux faibles émergents...",
                    "📈 Modélisation prédictive avancée des dynamiques de marché...",
                    "🤖 Génération d'insights actionnables multi-sectoriels...",
                    "✨ Finalisation du rapport d'intelligence stratégique"
                ]
            },
            "en": {
                "agent_name": "ARIA",
                "agent_desc": "Advanced Research Intelligence Agent",
                "status_idle": "💤 System on standby - Neural networks ready",
                "status_thinking": "🧠 Initializing cognitive matrices...",
                "status_analyzing": "⚡ Multi-dimensional neural processing active",
                "status_completed": "✨ Analysis complete - Insights synthesized",
                "sectors": {
                    "FinTech": "Financial Technologies",
                    "HealthTech": "Health Technologies",
                    "SaaS": "Software as a Service",
                    "E-commerce": "Digital Commerce",
                    "PropTech": "Property Technologies", 
                    "EdTech": "Education Technologies"
                },
                "thoughts": [
                    "🔮 Initializing quantum multi-dimensional sensors...",
                    "🌐 Synchronizing with global data streams...",
                    "🧠 Activating specialized sectoral neural networks...",
                    "📊 Ingesting 847 real-time data sources...",
                    "⚡ Processing via deep learning algorithms...",
                    "🎯 Detecting and correlating emerging weak signals...",
                    "📈 Advanced predictive modeling of market dynamics...",
                    "🤖 Generating actionable multi-sectoral insights...",
                    "✨ Finalizing strategic intelligence report"
                ]
            }
        }
        
        self.market_data = {
            "FinTech": {
                "fr": {
                    "summary": "Le secteur FinTech traverse une transformation quantique avec l'émergence d'écosystèmes d'IA conversationnelle et de super-apps intégrées. Les régulations MiCA créent des opportunités stratégiques pour les acteurs conformes.",
                    "insights": [
                        MarketInsight("IA Conversationnelle Bancaire", "L'intégration d'assistants IA multimodaux représente une opportunité de 3.2B€ d'ici 2027", 9.4, 89, "opportunity", "high"),
                        MarketInsight("Consolidation M&A Accélérée", "Vague d'acquisitions prévue Q2-Q3 2025 avec 18+ opérations majeures", 8.9, 84, "trend", "high"),
                        MarketInsight("Durcissement Réglementaire", "L'implémentation MiCA créent des barrières mais favorisent les acteurs conformes", 7.6, 91, "threat", "medium")
                    ],
                    "recommendations": [
                        "Investissement stratégique dans l'IA conversationnelle avant Q2 2025",
                        "Préparation proactive de la conformité MiCA 8 mois avant les concurrents", 
                        "Acquisition de talents blockchain avant la pénurie critique"
                    ]
                }
            }
        }
    
    def get_translation(self, key: str) -> str:
        return self.translations[self.language].get(key, key)
    
    def update_neural_metrics(self):
        """Met à jour les métriques neuronales"""
        base_time = time.time()
        self.neural_activity = int(850 + 100 * math.sin(base_time / 10) + random.randint(-30, 30))
        self.quantum_coherence = min(100, max(0, 85 + 10 * math.cos(base_time / 8) + random.uniform(-5, 5)))
        self.processing_nodes = random.randint(15, 25) if self.status != "idle" else random.randint(3, 8)
    
    def generate_neural_confidence_gauge(self) -> go.Figure:
        """Génère un graphique de confiance cyberpunk"""
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = self.confidence_level,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Neural Confidence", 'font': {'color': '#00f5ff', 'size': 18}},
            delta = {'reference': 85, 'increasing': {'color': "#00f5ff"}},
            gauge = {
                'axis': {'range': [None, 100], 'tickcolor': '#00f5ff'},
                'bar': {'color': "#00f5ff", 'thickness': 0.6},
                'bgcolor': "rgba(0,0,0,0.3)",
                'borderwidth': 2,
                'bordercolor': "#00f5ff",
                'steps': [
                    {'range': [0, 70], 'color': "rgba(239, 68, 68, 0.2)"},
                    {'range': [70, 90], 'color': "rgba(245, 158, 11, 0.2)"},
                    {'range': [90, 100], 'color': "rgba(0, 245, 255, 0.2)"}
                ]
            }
        ))
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "#00f5ff"},
            height=300
        )
        
        return fig
    
    def generate_quantum_neural_network(self) -> go.Figure:
        """Visualisation du réseau neuronal"""
        n_nodes = 25
        x = [random.uniform(0, 10) for _ in range(n_nodes)]
        y = [random.uniform(0, 10) for _ in range(n_nodes)]
        
        edge_x, edge_y = [], []
        for i in range(n_nodes):
            for j in range(i+1, min(i+4, n_nodes)):
                if random.random() > 0.4:
                    edge_x.extend([x[i], x[j], None])
                    edge_y.extend([y[i], y[j], None])
        
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='rgba(0, 245, 255, 0.4)'),
            hoverinfo='none', mode='lines', opacity=0.7
        )
        
        node_colors = ['#00f5ff' if random.random() > 0.4 else '#64748b' for _ in range(n_nodes)]
        node_sizes = [12 if color == '#00f5ff' else 8 for color in node_colors]
        
        node_trace = go.Scatter(
            x=x, y=y, mode='markers', hoverinfo='none',
            marker=dict(size=node_sizes, color=node_colors, opacity=0.9)
        )
        
        fig = go.Figure(data=[edge_trace, node_trace])
        fig.update_layout(
            showlegend=False, margin=dict(b=20,l=5,r=5,t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=350
        )
        
        return fig
    
    def chat_with_agent(self, message: str, sector: str) -> str:
        """Chat avec l'agent"""
        responses = {
            "fr": {
                "default": f"Système ARIA opérationnel. Analyse {sector} terminée avec {self.confidence_level:.1f}% de confiance. {self.processing_nodes} noeuds neuronaux actifs."
            },
            "en": {
                "default": f"ARIA system operational. {sector} analysis completed with {self.confidence_level:.1f}% confidence. {self.processing_nodes} neural nodes active."
            }
        }
        
        return responses[self.language]["default"]

def main():
    # Initialisation des états
    if 'agent' not in st.session_state:
        st.session_state.agent = ARIAAgent()
    if 'language' not in st.session_state:
        st.session_state.language = 'fr'
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    if 'last_update' not in st.session_state:
        st.session_state.last_update = time.time()
    
    agent = st.session_state.agent
    agent.language = st.session_state.language
    
    # Update neural metrics périodiquement
    if time.time() - st.session_state.last_update > 2:
        agent.update_neural_metrics()
        st.session_state.last_update = time.time()
    
    # Header cyberpunk
    col1, col2 = st.columns([9, 1])
    
    with col1:
        st.markdown(f"""
        <div class='aria-header'>
            <h1 class='aria-title'>🧠 {agent.get_translation('agent_name')}</h1>
            <p class='aria-subtitle'>{agent.get_translation('agent_desc')}</p>
            <div class='neural-stats'>
                <div class='neural-stat'>
                    <div class='neural-stat-value'>{agent.neural_activity}</div>
                    <div class='neural-stat-label'>Neural Nodes</div>
                </div>
                <div class='neural-stat'>
                    <div class='neural-stat-value'>{agent.quantum_coherence:.1f}%</div>
                    <div class='neural-stat-label'>Coherence</div>
                </div>
                <div class='neural-stat'>
                    <div class='neural-stat-value'>{agent.data_streams}</div>
                    <div class='neural-stat-label'>Data Streams</div>
                </div>
                <div class='neural-stat'>
                    <div class='neural-stat-value'>{agent.processing_nodes}</div>
                    <div class='neural-stat-label'>Active Cores</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Language selector
        lang_options = ["🇫🇷 FR", "🇺🇸 EN"]
        selected_lang = st.selectbox("🌐", lang_options, key="lang_select")
        new_language = "fr" if "FR" in selected_lang else "en"
        if new_language != st.session_state.language:
            st.session_state.language = new_language
            st.rerun()
    
    # Layout principal
    col1, col2, col3 = st.columns([3, 5, 3])
    
    with col1:
        # Panel de contrôle neuronal
        st.markdown('<div class="neural-glass-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #00f5ff; text-align: center; font-family: JetBrains Mono;">⚡ Neural Control Matrix</h3>', unsafe_allow_html=True)
        
        # Avatar ARIA
        status_class = f"status-{agent.status}"
        avatar_class = "aria-avatar active" if agent.status != "idle" else "aria-avatar"
        
        st.markdown(f"""
        <div class='aria-avatar-container'>
            <div class='{avatar_class}'>
                <div class='aria-core'>🤖</div>
            </div>
            <h4 style='color: #00f5ff; margin: 20px 0 10px 0; text-align: center; font-family: Orbitron;'>
                {agent.get_translation("agent_name")} v2.1
            </h4>
            <div style='text-align: center; margin-bottom: 25px;'>
                <span class='status-indicator {status_class}'></span>
                <span style='color: white; font-size: 0.9rem; font-family: JetBrains Mono;'>
                    {agent.get_translation(f"status_{agent.status}")}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Configuration
        st.markdown("<h4 style='color: #00f5ff; margin: 25px 0 15px 0; font-family: JetBrains Mono;'>🎯 Mission Parameters</h4>", unsafe_allow_html=True)
        
        sectors = agent.get_translation("sectors")
        selected_sector = st.selectbox(
            "Target Analysis Sector",
            list(sectors.keys()),
            format_func=lambda x: f"🔹 {sectors[x]}",
            key="sector_select"
        )
        
        # Bouton d'activation
        st.markdown("<br>", unsafe_allow_html=True)
        
        if agent.status in ["idle", "completed"]:
            if st.button("🚀 INITIATE NEURAL ANALYSIS", type="primary"):
                agent.status = "thinking"
                agent.thoughts = []
                thoughts = agent.get_translation("thoughts")
                
                for i, thought_text in enumerate(thoughts):
                    time.sleep(random.uniform(0.3, 0.8))
                    
                    thought = AgentThought(
                        content=thought_text,
                        timestamp=datetime.now(),
                        confidence=random.uniform(0.82, 0.97),
                        neural_pattern=["analytical", "creative", "predictive", "strategic"][i % 4]
                    )
                    
                    agent.thoughts.append(thought)
                    
                    if i == 3:
                        agent.status = "analyzing"
                    elif i == len(thoughts) - 1:
                        agent.status = "completed"
                        agent.current_analysis = agent.market_data.get(selected_sector, {}).get(agent.language, agent.market_data["FinTech"]["fr"])
                        agent.confidence_level = random.uniform(88, 96)
                        agent.quantum_coherence = random.uniform(92, 98)
                    
                    agent.update_neural_metrics()
                
                st.rerun()
        else:
            if st.button("⏹️ TERMINATE ANALYSIS", type="secondary"):
                agent.status = "idle"
                agent.thoughts = []
                agent.current_analysis = None
                st.rerun()
        
        # Métriques neuronales
        if agent.status != "idle":
            st.markdown("<br><h4 style='color: #00f5ff; font-family: JetBrains Mono;'>📊 Neural Metrics</h4>", unsafe_allow_html=True)
            
            metrics = [
                ("Neural Activity", agent.neural_activity, "#00f5ff"),
                ("Quantum Coherence", f"{agent.quantum_coherence:.1f}%", "#8b5cf6"),
                ("Processing Cores", agent.processing_nodes, "#ec4899"),
                ("Confidence", f"{agent.confidence_level:.1f}%" if agent.confidence_level > 0 else "N/A", "#10b981")
            ]
            
            for label, value, color in metrics:
                st.markdown(f"""
                <div class='neural-metric'>
                    <div class='metric-value' style='color: {color};'>{value}</div>
                    <div class='metric-label'>{label}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Réseau neuronal
        if agent.status in ["thinking", "analyzing", "completed"]:
            st.markdown('<div class="neural-glass-card">', unsafe_allow_html=True)
            st.markdown('<h4 style="color: #00f5ff; text-align: center; font-family: JetBrains Mono;">🧬 Neural Network</h4>', unsafe_allow_html=True)
            neural_fig = agent.generate_quantum_neural_network()
            st.plotly_chart(neural_fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Zone centrale
        if agent.status != "idle" and agent.thoughts:
            st.markdown('<div class="neural-glass-card">', unsafe_allow_html=True)
            st.markdown('<h3 style="color: #00f5ff; margin-bottom: 25px; font-family: Orbitron;">🧠 Neural Process</h3>', unsafe_allow_html=True)
            
            for i, thought in enumerate(agent.thoughts):
                delay = i * 0.15
                neural_icon = {"analytical": "🔬", "creative": "🎨", "predictive": "🔮", "strategic": "🎯"}.get(thought.neural_pattern, "⚡")
                
                st.markdown(f"""
                <div class='thought-hologram' style='animation-delay: {delay}s;'>
                    <div style='display: flex; align-items: start; gap: 18px;'>
                        <div style='background: linear-gradient(45deg, #00f5ff, #8b5cf6); border-radius: 50%; 
                                    width: 40px; height: 40px; display: flex; align-items: center; 
                                    justify-content: center; flex-shrink: 0; box-shadow: 0 0 15px rgba(0, 245, 255, 0.5);'>
                            {neural_icon}
                        </div>
                        <div style='flex: 1;'>
                            <p style='color: white; margin: 0 0 10px 0; font-size: 1rem; line-height: 1.5;'>
                                {thought.content}
                            </p>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <span style='color: #64748b; font-size: 0.75rem; font-family: JetBrains Mono;'>
                                    {thought.timestamp.strftime("%H:%M:%S")}
                                </span>
                                <span style='color: #10b981; font-size: 0.75rem; font-family: JetBrains Mono;'>
                                    {thought.confidence:.1%}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Résultats d'analyse
        if agent.current_analysis and agent.status == "completed":
            # Synthèse
            st.markdown(f"""
            <div class='neural-glass-card'>
                <h3 style='color: #00f5ff; margin-bottom: 25px; font-family: Orbitron;'>📋 Intelligence Report</h3>
                <div style='background: linear-gradient(135deg, rgba(0, 245, 255, 0.1), rgba(139, 92, 246, 0.1)); 
                            border-left: 4px solid #00f5ff; padding: 25px; border-radius: 0 20px 20px 0;'>
                    <p style='color: #e2e8f0; margin: 0; line-height: 1.7; font-size: 1.05rem;'>
                        {agent.current_analysis.get("summary", "")}
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Graphiques
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                st.markdown('<div class="neural-glass-card"><h4 style="color: #00f5ff; text-align: center;">🎯 Confidence</h4></div>', unsafe_allow_html=True)
                confidence_fig = agent.generate_neural_confidence_gauge()
                st.plotly_chart(confidence_fig, use_container_width=True)
            
            with col_chart2:
                st.markdown('<div class="neural-glass-card"><h4 style="color: #00f5ff; text-align: center;">📈 Activity</h4></div>', unsafe_allow_html=True)
                # Graphique simple
                fig = go.Figure(data=[go.Bar(x=['Neural Activity'], y=[agent.neural_activity], marker_color='#00f5ff')])
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font={'color': "#00f5ff"}, height=300
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Insights
            insights = agent.current_analysis.get("insights", [])
            if insights:
                st.markdown('<div class="neural-glass-card"><h3 style="color: #00f5ff; margin-bottom: 25px;">🎯 Strategic Insights</h3></div>', unsafe_allow_html=True)
                
                for i, insight in enumerate(insights):
                    category_colors = {"opportunity": "#10b981", "threat": "#ef4444", "trend": "#8b5cf6"}
                    color = category_colors.get(insight.category, "#64748b")
                    
                    st.markdown(f"""
                    <div class='insight-neural' style='border-left-color: {color}; animation-delay: {i*0.1}s;'>
                        <h5 style='color: white; margin: 0 0 10px 0; font-size: 1.1rem; font-weight: 600;'>
                            {insight.title}
                        </h5>
                        <p style='color: #cbd5e1; margin: 0 0 10px 0; line-height: 1.6;'>
                            {insight.description}
                        </p>
                        <div style='display: flex; gap: 10px;'>
                            <span style='background: rgba(255, 255, 255, 0.1); color: {color}; padding: 4px 8px; 
                                        border-radius: 10px; font-size: 0.7rem; font-weight: 500;'>
                                Impact: {insight.impact_score}/10
                            </span>
                            <span style='background: rgba(0, 245, 255, 0.2); color: #00f5ff; padding: 4px 8px; 
                                        border-radius: 10px; font-size: 0.7rem; font-weight: 500;'>
                                {insight.confidence}% Confidence
                            </span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Recommandations
            recommendations = agent.current_analysis.get("recommendations", [])
            if recommendations:
                st.markdown('<div class="neural-glass-card"><h3 style="color: #00f5ff; margin-bottom: 25px;">🎯 Recommendations</h3></div>', unsafe_allow_html=True)
                
                for i, rec in enumerate(recommendations, 1):
                    st.markdown(f"""
                    <div style='display: flex; align-items: start; gap: 25px; 
                                background: rgba(0, 245, 255, 0.05); border-radius: 20px; 
                                padding: 25px; margin: 20px 0; border-left: 4px solid #00f5ff;
                                animation: insightFade 0.8s ease-out {i*0.2}s both;'>
                        <div style='background: linear-gradient(45deg, #00f5ff, #8b5cf6); border-radius: 50%; 
                                    width: 45px; height: 45px; display: flex; align-items: center; 
                                    justify-content: center; flex-shrink: 0;'>
                            <span style='color: white; font-weight: bold; font-size: 1.2rem;'>{i}</span>
                        </div>
                        <p style='color: #e2e8f0; margin: 0; line-height: 1.7; font-size: 1rem;'>{rec}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # État initial
        elif agent.status == "idle":
            st.markdown("""
            <div class='neural-glass-card' style='text-align: center; padding: 60px 40px;'>
                <div style='font-size: 6rem; margin-bottom: 30px;'>🧠</div>
                <h3 style='color: #00f5ff; margin-bottom: 25px; font-family: Orbitron; font-size: 1.8rem;'>
                    ARIA System Ready
                </h3>
                <p style='color: #94a3b8; margin-bottom: 40px; font-size: 1.1rem; line-height: 1.7;'>
                    Advanced quantum intelligence system prepared for strategic analysis.
                </p>
                <div style='background: rgba(0, 245, 255, 0.08); border-radius: 20px; padding: 35px;'>
                    <h4 style='color: #00f5ff; margin-bottom: 25px;'>⚡ Core Capabilities</h4>
                    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px; text-align: left;'>
                        <div style='color: #cbd5e1; padding: 10px;'>🔮 Quantum analysis</div>
                        <div style='color: #cbd5e1; padding: 10px;'>⚡ Predictive modeling</div>
                        <div style='color: #cbd5e1; padding: 10px;'>🎯 Opportunity detection</div>
                        <div style='color: #cbd5e1; padding: 10px;'>📊 Risk assessment</div>
                        <div style='color: #cbd5e1; padding: 10px;'>🤖 Autonomous decisions</div>
                        <div style='color: #cbd5e1; padding: 10px;'>🧬 Pattern recognition</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        # Chat interface
        st.markdown('<div class="neural-glass-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #00f5ff; text-align: center;">💬 Neural Chat</h3>', unsafe_allow_html=True)
        
        if agent.current_analysis:
            for msg in st.session_state.chat_messages[-3:]:
                if msg['role'] == 'user':
                    st.markdown(f"""
                    <div style='background: rgba(0, 245, 255, 0.1); padding: 12px 16px; 
                                border-radius: 18px; margin: 10px 0; border-left: 3px solid #00f5ff;'>
                        <p style='color: white; margin: 0; font-size: 0.9rem;'>{msg['content']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='neural-chat'>
                        <div style='display: flex; gap: 12px;'>
                            <div style='background: linear-gradient(45deg, #00f5ff, #8b5cf6); border-radius: 50%; 
                                        width: 28px; height: 28px; display: flex; align-items: center; 
                                        justify-content: center; flex-shrink: 0;'>🤖</div>
                            <p style='color: #e2e8f0; margin: 0; font-size: 0.9rem; flex: 1;'>{msg['content']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            user_question = st.text_input("Ask ARIA...", key="chat_input", placeholder="What are the risks?")
            
            if user_question:
                st.session_state.chat_messages.append({"role": "user", "content": user_question})
                response = agent.chat_with_agent(user_question, selected_sector)
                st.session_state.chat_messages.append({"role": "assistant", "content": response})
                st.rerun()
        
        else:
            st.markdown("""
            <div style='text-align: center; padding: 25px;'>
                <div style='font-size: 3.5rem; margin-bottom: 20px; opacity: 0.6;'>💬</div>
                <p style='color: #94a3b8; margin-bottom: 25px;'>Chat available after analysis.</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Export
        if agent.current_analysis:
            st.markdown('<div class="neural-glass-card">', unsafe_allow_html=True)
            st.markdown('<h3 style="color: #00f5ff; text-align: center;">📤 Export</h3>', unsafe_allow_html=True)
            
            if st.button("📊 Generate Report", type="primary"):
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                report_content = f"""
ARIA INTELLIGENCE REPORT
Generated: {timestamp}
Sector: {selected_sector}
Confidence: {agent.confidence_level:.1f}%

EXECUTIVE SUMMARY:
{agent.current_analysis.get('summary', '')}

RECOMMENDATIONS:
"""
                for i, rec in enumerate(agent.current_analysis.get('recommendations', []), 1):
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
                if st.button("🔄 Reset"):
                    agent.status = "idle"
                    agent.thoughts = []
                    agent.current_analysis = None
                    st.session_state.chat_messages = []
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown(f"""
    <div class='aria-footer'>
        <div style='display: flex; justify-content: center; gap: 30px; margin-bottom: 15px; flex-wrap: wrap;'>
            <div style='color: #00f5ff; font-family: Orbitron; font-weight: 700;'>🧠 ARIA v2.1</div>
            <div style='color: #64748b;'>|</div>
            <div style='color: #00f5ff; font-family: JetBrains Mono;'>Neural: {agent.neural_activity}</div>
            <div style='color: #64748b;'>|</div>
            <div style='color: #10b981; font-family: JetBrains Mono;'>Coherence: {agent.quantum_coherence:.1f}%</div>
        </div>
        <p style='color: #64748b; margin: 0; font-size: 0.85rem;'>
            Advanced Research Intelligence Agent | Last Update: {datetime.now().strftime('%H:%M:%S')}
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
