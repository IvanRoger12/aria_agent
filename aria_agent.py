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

# Configuration de la page
st.set_page_config(
    page_title="🤖 ARIA - AI Strategic Intelligence Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS avancé avec animations et design premium (avec quelques améliorations)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Background animé */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 25%, #3b82f6 50%, #1e40af 75%, #0f172a 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        color: white;
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
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(59, 130, 246, 0.25);
        border-color: rgba(59, 130, 246, 0.4);
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
        background: rgba(59, 130, 246, 0.1);
        border-left: 4px solid #3b82f6;
        padding: 20px;
        margin-bottom: 15px;
        border-radius: 0 15px 15px 0;
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.1);
    }
    
    /* Métriques en temps réel */
    .metric-value {
        font-size: 2.2rem;
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
        border-radius: 12px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        padding: 12px 30px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.5);
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
        from { filter: drop-shadow(0 0 15px rgba(96, 165, 250, 0.6)); }
        to { filter: drop-shadow(0 0 30px rgba(167, 139, 250, 0.9)); }
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
    
    .status-idle { background: #6b7280; }
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
        background: rgba(255, 255, 255, 0.06);
        border-radius: 15px;
        padding: 20px;
        margin: 12px 0;
        border-left: 4px solid;
        transition: all 0.3s ease;
    }
    
    .insight-card:hover {
        transform: translateY(-3px) scale(1.01);
        background: rgba(255, 255, 255, 0.1);
    }
    
    .opportunity-card { border-left-color: #10b981; box-shadow: 0 5px 15px rgba(16, 185, 129, 0.1); }
    .threat-card { border-left-color: #ef4444; box-shadow: 0 5px 15px rgba(239, 68, 68, 0.1); }
    .trend-card { border-left-color: #8b5cf6; box-shadow: 0 5px 15px rgba(139, 92, 246, 0.1); }
    
    /* Recommandations stylisées */
    .recommendation-bubble {
        display: flex;
        align-items: start;
        gap: 20px;
        background: rgba(139, 92, 246, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border-left: 4px solid #8b5cf6;
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
        box-shadow: 0 0 15px rgba(139, 92, 246, 0.5);
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
                    "FinTech": "Technologies Financières",
                    "HealthTech": "Technologies de la Santé",
                    "SaaS": "Logiciels en tant que Service",
                    "E-commerce": "Commerce Électronique",
                    "PropTech": "Technologies Immobilières",
                    "EdTech": "Technologies de l'Éducation"
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
            },
            "en": {
                "agent_name": "ARIA",
                "agent_desc": "Autonomous Research & Intelligence Agent",
                "status_idle": "On standby - Ready to analyze",
                "status_thinking": "Strategic thinking...",
                "status_analyzing": "Multi-dimensional analysis...",
                "status_completed": "Analysis complete",
                "sectors": {
                    "FinTech": "Financial Technologies",
                    "HealthTech": "Health Technologies",
                    "SaaS": "Software as a Service",
                    "E-commerce": "Electronic Commerce",
                    "PropTech": "Property Technologies",
                    "EdTech": "Education Technologies"
                },
                "thoughts": [
                    "Initializing market sensors...",
                    "Activating sectoral neural networks...",
                    "Ingesting 1.2 GB of real-time data...",
                    "Processing via deep learning algorithms...",
                    "Correlating detected weak signals...",
                    "Predictive modeling of trends...",
                    "Generating actionable insights...",
                    "Final strategic synthesis..."
                ]
            }
        }
        self.market_data = self._generate_all_sector_data()

    def get_translation(self, key: str, lang: Optional[str] = None) -> str:
        if lang is None:
            lang = self.language
        return self.translations[lang].get(key, key)

    def _generate_sector_data(self, sector_name: str, lang: str) -> Dict:
        """Génère des données d'analyse fictives pour un secteur."""
        is_fr = lang == "fr"
        # Templates for dynamic data generation
        summaries = {
            "fr": f"Le secteur {sector_name} est en pleine mutation, tiré par l'IA générative et une demande accrue pour des solutions hyper-personnalisées. La consolidation du marché s'accélère.",
            "en": f"The {sector_name} sector is undergoing rapid transformation, driven by generative AI and increased demand for hyper-personalized solutions. Market consolidation is accelerating."
        }
        opportunities = {
            "fr": [
                MarketInsight(f"IA dans {sector_name}", f"L'intégration de l'IA pourrait débloquer un marché de {random.uniform(1.5, 5.0):.1f}B€.", 9.2, 88, "opportunity"),
                MarketInsight("Solutions Durables", "La demande pour des options écologiques crée une nouvelle niche de marché.", 8.5, 75, "opportunity")
            ],
            "en": [
                MarketInsight(f"AI in {sector_name}", f"AI integration could unlock a ${random.uniform(1.8, 5.5):.1f}B market.", 9.2, 88, "opportunity"),
                MarketInsight("Sustainable Solutions", "Demand for eco-friendly options is creating a new market niche.", 8.5, 75, "opportunity")
            ]
        }
        threats = {
            "fr": [MarketInsight("Régulation Accrue", "De nouvelles lois pourraient augmenter les coûts de conformité de 20%.", 7.8, 91, "threat")],
            "en": [MarketInsight("Increased Regulation", "New laws could increase compliance costs by 20%.", 7.8, 91, "threat")]
        }
        trends = {
            "fr": [MarketInsight("Hyper-personnalisation", "Les clients exigent des expériences sur mesure, poussant à l'innovation.", 8.9, 84, "trend")],
            "en": [MarketInsight("Hyper-personalization", "Customers are demanding tailored experiences, driving innovation.", 8.9, 84, "trend")]
        }
        recommendations = {
            "fr": [f"Investir dans une plateforme d'IA avant le T3 2026.", f"Lancer un audit de conformité réglementaire.", f"Développer un pilote de solution durable."],
            "en": [f"Invest in an AI platform before Q3 2026.", f"Initiate a regulatory compliance audit.", f"Develop a sustainable solution pilot."]
        }

        return {
            "summary": summaries[lang],
            "insights": opportunities[lang] + threats[lang] + trends[lang],
            "recommendations": recommendations[lang]
        }
        
    def _generate_all_sector_data(self) -> Dict:
        """Génère des données pour tous les secteurs dans toutes les langues."""
        all_data = {}
        sectors = self.get_translation("sectors", "en").keys() # Use EN as base for keys
        for sector in sectors:
            all_data[sector] = {
                "fr": self._generate_sector_data(self.get_translation("sectors", "fr")[sector], "fr"),
                "en": self._generate_sector_data(self.get_translation("sectors", "en")[sector], "en")
            }
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
        
    def chat_with_agent(self, message: str, sector: str) -> str:
        """Chat amélioré avec l'agent."""
        message = message.lower()
        insights = self.current_analysis.get("insights", [])
        
        if any(keyword in message for keyword in ["opportunit", "opportunity"]):
            opps = [i for i in insights if i.category == "opportunity"]
            return self.get_translation("fr" if self.language == "fr" else "en").get("chat_opps", f"J'ai identifié {len(opps)} opportunités, notamment : {opps[0].title}.")
        
        if any(keyword in message for keyword in ["menace", "threat", "risk"]):
            thrs = [i for i in insights if i.category == "threat"]
            return self.get_translation("fr" if self.language == "fr" else "en").get("chat_threats", f"La menace principale est : {thrs[0].title}.")
            
        return self.get_translation("fr" if self.language == "fr" else "en").get(
            "default_chat", 
            f"Dans le secteur {sector}, l'IA et la durabilité sont les deux axes majeurs de mon analyse."
        )

# --- Interface Principale ---
def main():
    # Initialisation de l'état de session
    if 'agent' not in st.session_state:
        st.session_state.agent = ARIAAgent()
    if 'language' not in st.session_state:
        st.session_state.language = 'fr'
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []

    agent = st.session_state.agent
    agent.language = st.session_state.language

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
            selected_sector = st.selectbox(
                "Select sector", list(sectors.keys()),
                format_func=lambda x: sectors[x],
                label_visibility="collapsed"
            )

            # Bouton d'activation
            st.markdown("<br>", unsafe_allow_html=True)
            if agent.status in ["idle", "completed"]:
                if st.button("🚀 ACTIVER ARIA", type="primary"):
                    st.session_state.running_analysis = True
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
                time.sleep(random.uniform(0.6, 1.2))
                
                # Mise à jour du statut
                if i >= 2 and agent.status == "thinking":
                    agent.status = "analyzing"
                
                # Mise à jour des métriques
                agent.neural_activity += random.randint(-40, 60)
                agent.activity_history.append(agent.neural_activity)
                agent.confidence_level = (i + 1) / len(thoughts) * 80
                
                # Ajout de la pensée
                thought = AgentThought(content=thought_text)
                agent.thoughts.append(thought)
                
                # Mise à jour de l'affichage
                thought_item_html = f"""
                <div class='thought-bubble'>
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
            agent.current_analysis = agent.market_data.get(selected_sector, {}).get(agent.language, {})
            st.session_state.running_analysis = False
            st.rerun()

        elif agent.status == "completed" and agent.current_analysis:
            # --- AFFICHAGE DES RÉSULTATS FINAUX ---
            with results_placeholder.container():
                st.markdown(f"""
                <div class='glass-card' style='animation: fadeInUp 0.5s ease-out;'>
                    <h3 style='color: white;'>📋 Synthèse Stratégique</h3>
                    <p style='color: #e2e8f0; font-size: 1.1rem;'>{agent.current_analysis.get("summary", "")}</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown('<div class="glass-card"><h3 style="color: white;">⚡ Insights Clés</h3></div>', unsafe_allow_html=True)
                
                insights = agent.current_analysis.get("insights", [])
                for i, insight in enumerate(insights):
                    icon = {"opportunity": "💡", "threat": "🚨", "trend": "📊"}.get(insight.category, "🔹")
                    st.markdown(f"""
                    <div class='insight-card {insight.category}-card' style='animation: fadeInUp {0.6 + i*0.1}s ease-out backwards;'>
                        <h5 style='color: white; margin-bottom: 10px;'>{icon} {insight.title}</h5>
                        <p style='color: #cbd5e1; margin-bottom: 12px;'>{insight.description}</p>
                        <div style='display: flex; gap: 10px; font-size: 0.8rem;'>
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
                        <p style='color: #e2e8f0; margin: auto 0;'>{rec}</p>
                    </div>
                    """, unsafe_allow_html=True)

                # --- Section Chat ---
                st.markdown('<div class="glass-card"><h3 style="color: white;">💬 Discuter avec ARIA</h3></div>', unsafe_allow_html=True)
                for msg in st.session_state.chat_messages[-3:]: # Afficher les 3 derniers messages
                    st.chat_message(msg["role"]).write(msg["content"])
                
                if user_question := st.chat_input("Posez votre question..."):
                    st.session_state.chat_messages.append({"role": "user", "content": user_question})
                    st.chat_message("user").write(user_question)
                    
                    response = agent.chat_with_agent(user_question, sectors[selected_sector])
                    st.session_state.chat_messages.append({"role": "assistant", "content": response})
                    st.chat_message("assistant").write(response)

        else:
            # --- Écran d'accueil ---
            with results_placeholder.container():
                st.markdown("""
                <div class='glass-card' style='text-align: center; padding: 40px;'>
                    <div style='font-size: 4rem; margin-bottom: 20px;'>🤖</div>
                    <h2 style='color: white;'>ARIA est prête à analyser le marché.</h2>
                    <p style='color: #94a3b8;'>Sélectionnez un secteur et cliquez sur 'Activer ARIA' pour lancer une analyse stratégique en temps réel.</p>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
