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

# CSS personnalisé (UNIQUEMENT style : fond bleu, texte blanc, titres en blanc gras, accents jaunes, clignotement)
st.markdown("""
<style>
    :root{
        --bg1:#0b1224; --bg2:#08101f; 
        --card: rgba(10,17,33,.96);
        --white:#ffffff; --muted:#e9f0ff; 
        --blue:#2f7df4; --violet:#7c58f4; 
        --green:#10b981; --yellow:#ffd84d; --danger:#ef4444;
        --border: rgba(255,255,255,.18);
    }

    /* Fond global bleu + halo léger */
    .main {
        background:
          radial-gradient(1200px 800px at 10% -10%, rgba(47,125,244,.15), transparent 50%),
          radial-gradient(1000px 700px at 90% 10%, rgba(124,88,244,.18), transparent 60%),
          linear-gradient(135deg, var(--bg1) 0%, var(--bg2) 100%);
        color: var(--white);
    }

    /* Tout le texte = blanc lisible (désactive les anciennes couleurs trop grisées) */
    h1, h2, h3, h4, h5, h6 { 
        color: var(--white) !important; 
        font-weight: 800 !important; 
        letter-spacing: .2px;
        text-shadow: 0 0 8px rgba(0,0,0,.5);
    }
    p, span, div, li { color: var(--white) !important; }
    /* Sous-titres bien visibles + possibilité d’accent jaune si besoin */
    .subtitle-white { color: var(--white) !important; font-weight: 800 !important; }
    .subtitle-yellow { color: var(--yellow) !important; font-weight: 800 !important; text-shadow: 0 0 10px rgba(255,216,77,.9); }

    /* Neutralise le h1 en dégradé défini inline pour le rendre blanc net */
    h1[style*="-webkit-text-fill-color: transparent"]{
        -webkit-text-fill-color: #fff !important;
        background: none !important;
        color: #fff !important;
        text-shadow: 0 0 10px rgba(0,0,0,.6);
    }

    /* Cartes contrastées (moins de flou, plus de lisibilité) */
    .analysis-card, .metric-card, .thought-bubble {
        background: var(--card) !important;
        backdrop-filter: blur(3px) !important;
        -webkit-backdrop-filter: blur(3px) !important;
        border: 1px solid var(--border) !important;
        border-radius: 18px !important;
        box-shadow: 0 16px 40px rgba(0,0,0,.45), 0 0 24px rgba(47,125,244,.12) !important;
    }

    /* Select & Buttons relookés (bleu → violet) */
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.06) !important;
        color: #fff !important;
        border: 1px solid rgba(255, 255, 255, 0.28) !important;
        border-radius: 10px !important;
    }
    .stButton > button {
        background: linear-gradient(45deg, var(--blue), var(--violet)) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        box-shadow: 0 10px 25px rgba(47,125,244,.35), 0 0 16px rgba(124,88,244,.25) !important;
        transition: transform .2s, box-shadow .2s, filter .2s !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 16px 35px rgba(124,88,244,.45), 0 0 24px rgba(47,125,244,.35) !important;
        filter: brightness(1.05) !important;
    }

    /* Pulsation agent et clignotement statut + plus lumineux */
    .agent-thinking {
        background: linear-gradient(45deg, #153a6b, #2f7df4) !important;
        animation: pulse 2s infinite !important;
        border-radius: 15px !important;
        padding: 15px !important;
        margin: 10px 0 !important;
        box-shadow: 0 0 14px rgba(47,125,244,.45) !important;
    }
    @keyframes pulse {
        0% { opacity: 0.86; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.01); }
        100% { opacity: 0.86; transform: scale(1); }
    }
    .status-indicator {
        width: 12px; height: 12px; border-radius: 50%;
        display: inline-block; margin-right: 8px;
        animation: statusBlink 1.2s infinite;
        box-shadow: 0 0 10px currentColor, 0 0 20px currentColor;
    }
    @keyframes statusBlink {
        0%, 100% { opacity: 1; filter: drop-shadow(0 0 6px rgba(255,255,255,.5)); }
        50% { opacity: .55; filter: drop-shadow(0 0 2px rgba(255,255,255,.2)); }
    }

    /* Bulles de pensée plus nettes */
    .thought-bubble {
        background: rgba(47,125,244, 0.10) !important;
        border-left: 5px solid var(--blue) !important;
        animation: slideIn .45s ease-out !important;
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-18px); }
        to   { opacity: 1; transform: translateX(0); }
    }

    /* Zone “réseau neuronal” bleu sombre */
    .neural-network {
        background: linear-gradient(135deg, #0a1730, #0d1b3a) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        position: relative !important;
        overflow: hidden !important;
        border: 1px solid rgba(255,255,255,.12);
    }
    .neural-node {
        width: 8px; height: 8px; background: #89b7ff !important;
        border-radius: 50%; position: absolute;
        animation: neuralPulse 2s infinite ease-in-out;
        box-shadow: 0 0 10px #2f7df4, 0 0 18px #2f7df4;
    }
    @keyframes neuralPulse {
        0%, 100% { opacity: 0.4; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.2); }
    }

    /* Cartes d’analyse */
    .analysis-card {
        background: rgba(12, 20, 40, 0.98) !important;
        backdrop-filter: blur(4px) !important;
        border: 1px solid rgba(255, 255, 255, 0.14) !important;
        border-radius: 20px !important;
        padding: 25px !important;
        margin: 15px 0 !important;
        box-shadow: 0 16px 40px rgba(0,0,0,0.45), 0 0 20px rgba(47,125,244,0.12) !important;
    }

    /* Encarts de catégories (opportunités/menaces/tendances) */
    .ins-opp { background: rgba(16,185,129,.12) !important; border-left: 6px solid var(--green) !important; }
    .ins-thr { background: rgba(239,68,68,.12) !important;  border-left: 6px solid var(--danger) !important; }
    .ins-trd { background: rgba(124,88,244,.12) !important;  border-left: 6px solid var(--violet) !important; }

    /* Renforce la lisibilité des petits textes métriques */
    .metric-card p:first-child{ color: var(--muted) !important; }
</style>
""", unsafe_allow_html=True)

@dataclass
class AgentThought:
    content: str
    timestamp: datetime
    thought_type: str = "analysis"  # analysis, insight, recommendation
    confidence: float = 0.0

@dataclass
class MarketInsight:
    title: str
    description: str
    impact_score: float
    confidence: float
    category: str  # opportunity, threat, trend

class ARIAAgent:
    """
    ARIA - Autonomous Research & Intelligence Agent
    Agent IA autonome pour l'analyse stratégique de marché
    """
    
    def __init__(self, language: str = "fr"):
        self.language = language
        self.status = "idle"  # idle, thinking, analyzing, completed
        self.thoughts = []
        self.current_analysis = None
        self.confidence_level = 0.0
        self.neural_activity = 0
        
        # Traductions
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
        
        # Données d'analyse simulées réalistes
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
        """Obtient la traduction pour une clé donnée"""
        return self.translations[self.language].get(key, key)
    
    async def activate(self, sector: str) -> None:
        """Active l'agent pour analyser un secteur"""
        self.status = "thinking"
        self.thoughts = []
        self.neural_activity = random.randint(800, 900)
        
        # Simulation du processus de pensée de l'agent
        thoughts = self.get_translation("thoughts")
        
        for i, thought_text in enumerate(thoughts):
            # Simulation d'un délai de réflexion variable
            await asyncio.sleep(random.uniform(0.8, 1.5))
            
            thought = AgentThought(
                content=thought_text,
                timestamp=datetime.now(),
                confidence=random.uniform(0.7, 0.95)
            )
            
            self.thoughts.append(thought)
            
            # Changement de statut pendant le processus
            if i == 2:
                self.status = "analyzing"
            elif i == len(thoughts) - 1:
                self.status = "completed"
                self.current_analysis = self.market_data.get(sector, {}).get(self.language, {})
                self.confidence_level = random.uniform(85, 95)
            
            # Simulation de l'activité neuronale
            self.neural_activity += random.randint(-30, 50)
    
    def generate_confidence_gauge(self) -> go.Figure:
        """Génère un graphique de confiance"""
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = self.confidence_level,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Confidence Level", 'font': {'color': '#ffffff'}},
            delta = {'reference': 80, 'increasing': {'color': '#2f7df4'}},
            gauge = {
                'axis': {'range': [None, 100], 'tickcolor':'#cfe1ff'},
                'bar': {'color': "#2f7df4"},
                'steps': [
                    {'range': [0, 50], 'color': "#1d2337"},
                    {'range': [50, 80], 'color': "#122245"},
                    {'range': [80, 100], 'color': "#0f2e5f"}
                ],
                'threshold': {
                    'line': {'color': "#ffd84d", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "white", 'family': "Arial"},
            height=300
        )
        
        return fig
    
    def generate_neural_network_viz(self) -> go.Figure:
        """Génère une visualisation du réseau neuronal"""
        # Positions des noeuds
        n_nodes = 20
        x = [random.uniform(0, 10) for _ in range(n_nodes)]
        y = [random.uniform(0, 10) for _ in range(n_nodes)]
        
        # Connexions aléatoires
        edge_x = []
        edge_y = []
        
        for i in range(n_nodes):
            for j in range(i+1, min(i+4, n_nodes)):  # Connexions locales
                if random.random() > 0.6:  # 40% de chance de connexion
                    edge_x.extend([x[i], x[j], None])
                    edge_y.extend([y[i], y[j], None])
        
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.8, color='rgba(47,125,244,.75)'),
            hoverinfo='none',
            mode='lines',
            opacity=0.85
        )
        
        node_trace = go.Scatter(
            x=x, y=y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                size=8,
                color='#7c58f4',
                line=dict(width=2, color='#2f7df4')
            )
        )
        
        fig = go.Figure(data=[edge_trace, node_trace])
        fig.update_layout(
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            annotations=[ dict(
                text="Neural Network Activity",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.005, y=-0.002,
                xanchor='left', yanchor='bottom',
                font=dict(color="white", size=12)
            )],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        
        return fig

# Interface principale
def main():
    # Initialisation de l'agent
    if 'agent' not in st.session_state:
        st.session_state.agent = ARIAAgent()
    
    if 'language' not in st.session_state:
        st.session_state.language = 'fr'
    
    agent = st.session_state.agent
    agent.language = st.session_state.language
    
    # Header futuriste
    col1, col2, col3 = st.columns([6, 1, 1])
    
    with col1:
        st.markdown(f"""
        <div style='margin-bottom: 30px;'>
            <h1 style='background: linear-gradient(45deg, #3b82f6, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; margin: 0; font-weight: 800;'>
                🧠 {agent.get_translation('agent_name')}
            </h1>
            <p style='font-size: 1.2rem; margin: 0;'>
                {agent.get_translation('agent_desc')}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Sélecteur de langue
        lang = st.selectbox("🌐", ["🇫🇷 FR", "🇺🇸 EN"], key="lang_select")
        new_language = "fr" if "FR" in lang else "en"
        if new_language != st.session_state.language:
            st.session_state.language = new_language
            st.rerun()
    
    # Layout principal
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Panel de contrôle de l'agent
        st.markdown("""
        <div class='analysis-card'>
            <h3 style='text-align: center; margin-bottom: 20px;'>🤖 Agent Control Panel</h3>
        """, unsafe_allow_html=True)
        
        # Avatar de l'agent avec statut
        status_color = {
            "idle": "#6b7280",
            "thinking": "#f59e0b", 
            "analyzing": "#2f7df4",
            "completed": "#10b981"
        }.get(agent.status, "#6b7280")
        
        st.markdown(f"""
        <div style='text-align: center; margin: 20px 0;'>
            <div style='position: relative; display: inline-block;'>
                <div style='width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(45deg, #2f7df4, #7c58f4); display: flex; align-items: center; justify-content: center; margin: 0 auto; {"animation: pulse 2s infinite;" if agent.status != "idle" else ""}'>
                    <span style='font-size: 2rem;'>🤖</span>
                </div>
                <div class='status-indicator' style='position: absolute; bottom: 0; right: 0; width: 20px; height: 20px; border-radius: 50%; background: {status_color}; border: 2px solid white;'></div>
            </div>
            <h4 style='margin: 10px 0 5px 0; font-weight: 800;'>{agent.get_translation("agent_name")}</h4>
            <p style='font-size: 0.9rem; margin: 0;'>Neural Activity: {agent.neural_activity}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Statut de l'agent
        status_text = agent.get_translation(f"status_{agent.status}")
        st.markdown(f"""
        <div style='background: rgba(47, 125, 244, 0.12); border:1px solid rgba(47,125,244,.35); border-radius: 12px; padding: 15px; margin: 20px 0; text-align: center; box-shadow: 0 0 14px rgba(47,125,244,.25);'>
            <p style='margin: 0; font-weight: 800;'>{status_text}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sélection du secteur
        st.markdown("<p style='font-weight: 800; margin-bottom: 10px;'>🎯 Target Sector:</p>", unsafe_allow_html=True)
        sectors = agent.get_translation("sectors")
        sector_options = list(sectors.keys())
        sector_labels = list(sectors.values())
        
        selected_sector = st.selectbox(
            "Select sector",
            sector_options,
            format_func=lambda x: sectors[x],
            label_visibility="collapsed"
        )
        
        # Bouton d'activation
        st.markdown("<br>", unsafe_allow_html=True)
        
        if agent.status in ["idle", "completed"]:
            if st.button("🚀 Activate ARIA Agent", key="activate_btn", type="primary"):
                with st.spinner("Agent activation in progress..."):
                    # Exécution de l'analyse asynchrone
                    import asyncio
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
        
        # Métriques temps réel
        if agent.status != "idle":
            st.markdown("<br><h4>📊 Real-time Metrics</h4>", unsafe_allow_html=True)
            
            metrics_data = {
                "Neural Activity": f"{agent.neural_activity}",
                "Data Sources": "847", 
                "Insights Generated": f"{len([t for t in agent.thoughts if t.confidence > 0.8])}",
                "Confidence": f"{agent.confidence_level:.1f}%" if agent.confidence_level > 0 else "N/A"
            }
            
            for metric, value in metrics_data.items():
                st.markdown(f"""
                <div class='metric-card'>
                    <p style='margin: 0; font-size: 0.8rem; color: var(--muted) !important;'>{metric}</p>
                    <p style='margin: 0; font-size: 1.2rem; font-weight: 800;'>{value}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # Zone d'affichage des pensées et résultats
        if agent.status != "idle" and agent.thoughts:
            st.markdown("""
            <div class='analysis-card'>
                <h3 style='margin-bottom: 20px;'>🧠 <span class='subtitle-yellow'>Agent Thought Process</span></h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Affichage des pensées en temps réel
            for i, thought in enumerate(agent.thoughts):
                st.markdown(f"""
                <div class='thought-bubble'>
                    <div style='display: flex; align-items: center; margin-bottom: 8px;'>
                        <span style='background: linear-gradient(45deg, #2f7df4, #7c58f4); border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; margin-right: 12px; box-shadow: 0 0 14px rgba(47,125,244,.35);'>
                            🤖
                        </span>
                        <div>
                            <p style='margin: 0; font-size: 0.95rem; font-weight: 700;'>{thought.content}</p>
                            <p style='margin: 0; font-size: 0.75rem; color: var(--muted) !important;'>{thought.timestamp.strftime("%H:%M:%S")}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Résultats d'analyse
        if agent.current_analysis and agent.status == "completed":
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Synthèse exécutive
            st.markdown(f"""
            <div class='analysis-card'>
                <h3 style='margin-bottom: 20px;'>📋 Executive Summary</h3>
                <div style='background: linear-gradient(45deg, rgba(47, 125, 244, 0.18), rgba(124, 88, 244, 0.18)); border-left: 6px solid #2f7df4; padding: 20px; border-radius: 12px;'>
                    <p style='margin: 0; line-height: 1.6; color: var(--muted) !important;'>{agent.current_analysis.get("summary", "")}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Graphique de confiance
            if agent.confidence_level > 0:
                st.markdown("""
                <div class='analysis-card'>
                    <h3 style='margin-bottom: 20px;'>📊 <span class='subtitle-yellow'>Confidence Analysis</span></h3>
                </div>
                """, unsafe_allow_html=True)
                
                confidence_fig = agent.generate_confidence_gauge()
                st.plotly_chart(confidence_fig, use_container_width=True)
            
            # Insights détectés
            insights = agent.current_analysis.get("insights", [])
            if insights:
                st.markdown("""
                <div class='analysis-card'>
                    <h3 style='margin-bottom: 20px;'>🎯 Detected Insights</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Séparation par catégorie
                opportunities = [i for i in insights if i.category == "opportunity"]
                threats = [i for i in insights if i.category == "threat"]
                trends = [i for i in insights if i.category == "trend"]
                
                if opportunities:
                    st.markdown("<h4>💡 Opportunities</h4>", unsafe_allow_html=True)
                    for opp in opportunities:
                        st.markdown(f"""
                        <div class='ins-opp' style='padding: 15px; margin: 10px 0; border-radius: 12px;'>
                            <h5 style='margin: 0 0 8px 0; font-weight: 800;'>{opp.title}</h5>
                            <p style='margin: 0 0 8px 0; font-size: 0.9rem; color: var(--muted) !important;'>{opp.description}</p>
                            <div style='display: flex; justify-content: space-between; align-items: center; font-size: .9rem;'>
                                <span>Impact: <b>{opp.impact_score}/10</b></span>
                                <span style='color: #22c55e;'>Confidence: <b>{opp.confidence}%</b></span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                if threats:
                    st.markdown("<h4>⚠️ Threats</h4>", unsafe_allow_html=True)
                    for threat in threats:
                        st.markdown(f"""
                        <div class='ins-thr' style='padding: 15px; margin: 10px 0; border-radius: 12px;'>
                            <h5 style='margin: 0 0 8px 0; font-weight: 800;'>{threat.title}</h5>
                            <p style='margin: 0 0 8px 0; font-size: 0.9rem; color: var(--muted) !important;'>{threat.description}</p>
                            <div style='display: flex; justify-content: space-between; align-items: center; font-size: .9rem;'>
                                <span>Impact: <b>{threat.impact_score}/10</b></span>
                                <span style='color: #f87171;'>Confidence: <b>{threat.confidence}%</b></span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                if trends:
                    st.markdown("<h4>📈 Trends</h4>", unsafe_allow_html=True)
                    for trend in trends:
                        st.markdown(f"""
                        <div class='ins-trd' style='padding: 15px; margin: 10px 0; border-radius: 12px;'>
                            <h5 style='margin: 0 0 8px 0; font-weight: 800;'>{trend.title}</h5>
                            <p style='margin: 0 0 8px 0; font-size: 0.9rem; color: var(--muted) !important;'>{trend.description}</p>
                            <div style='display: flex; justify-content: space-between; align-items: center; font-size: .9rem;'>
                                <span>Impact: <b>{trend.impact_score}/10</b></span>
                                <span style='color: #a78bfa;'>Confidence: <b>{trend.confidence}%</b></span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Recommandations IA
            recommendations = agent.current_analysis.get("recommendations", [])
            if recommendations:
                st.markdown("""
                <div class='analysis-card'>
                    <h3 style='margin-bottom: 20px;'>🎯 <span class='subtitle-yellow'>AI Recommendations</span></h3>
                </div>
                """, unsafe_allow_html=True)
                
                for i, rec in enumerate(recommendations, 1):
                    st.markdown(f"""
                    <div style='display: flex; align-items: start; background: rgba(124, 88, 244, 0.12); border-radius: 12px; padding: 15px; margin: 10px 0; border: 1px solid rgba(124,88,244,.25);'>
                        <div style='background: linear-gradient(45deg, #2f7df4, #7c58f4); border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; margin-right: 15px; flex-shrink: 0; color:#fff; font-weight: 800;'>
                            {i}
                        </div>
                        <p style='margin: 0; line-height: 1.55;'>{rec}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Actions et export
            st.markdown("""
            <div class='analysis-card'>
                <h3 style='margin-bottom: 20px;'>📤 Export & Actions</h3>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📄 Export Report", key="export_btn"):
                    # Génération d'un rapport texte simple
                    report_content = f"""
                    🤖 ARIA - STRATEGIC INTELLIGENCE REPORT
                    Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    Sector: {selected_sector}
                    Confidence Level: {agent.confidence_level:.1f}%
                    
                    EXECUTIVE SUMMARY:
                    {agent.current_analysis.get('summary', '')}
                    
                    KEY INSIGHTS:
                    """
                    insights = agent.current_analysis.get("insights", [])
                    for insight in insights:
                        report_content += f"\\n• {insight.title} (Impact: {insight.impact_score}/10, Confidence: {insight.confidence}%)"
                        report_content += f"\\n  {insight.description}\\n"
                    
                    report_content += "\\nRECOMMENDATIONS:\\n"
                    for i, rec in enumerate(recommendations, 1):
                        report_content += f"{i}. {rec}\\n"
                    
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
        
        # État initial
        elif agent.status == "idle":
            st.markdown("""
            <div class='analysis-card' style='text-align: center; padding: 50px;'>
                <div style='font-size: 4rem; margin-bottom: 20px;'>🤖</div>
                <h3 style='margin-bottom: 15px;'>ARIA Ready for Mission</h3>
                <p style='margin-bottom: 30px; color: var(--muted) !important;'>Select a target sector and activate the agent to begin strategic market analysis.</p>
                <div style='background: rgba(47, 125, 244, 0.12); border:1px solid rgba(47,125,244,.35); border-radius: 12px; padding: 20px; margin: 20px 0;'>
                    <h4 class='subtitle-yellow' style='margin-bottom: 15px;'>🧠 Agent Capabilities</h4>
                    <ul style='text-align: left; list-style: none; padding: 0; margin:0;'>
                        <li style='margin: 8px 0;'>🔍 Multi-source market intelligence gathering</li>
                        <li style='margin: 8px 0;'>⚡ Real-time trend analysis and prediction</li>
                        <li style='margin: 8px 0;'>🎯 Strategic opportunity identification</li>
                        <li style='margin: 8px 0;'>📊 Risk assessment and mitigation strategies</li>
                        <li style='margin: 8px 0;'>🤖 AI-powered actionable recommendations</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Neural network visualization (sidebar) — inchangé
    if agent.status in ["thinking", "analyzing"]:
        with st.sidebar:
            st.markdown("### 🧠 Neural Network Activity")
            neural_fig = agent.generate_neural_network_viz()
            st.plotly_chart(neural_fig, use_container_width=True)
    
    # Footer
    st.markdown("""
    <div style='margin-top: 50px; padding: 30px 0; border-top: 1px solid rgba(255, 255, 255, 0.1); text-align: center;'>
        <p style='margin: 0; color: var(--muted) !important;'>
            🤖 ARIA - Autonomous Research & Intelligence Agent | 
            Powered by Advanced AI Neural Networks | 
            Confidence Level: {confidence}%
        </p>
        <p style='font-size: 0.9rem; margin: 5px 0 0 0; color: var(--muted) !important;'>
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
