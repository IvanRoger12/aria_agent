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

# =========================
# CSS — BLEU FONCÉ + TEXTE BLEU (lisible) / pas d’effets flous
# =========================
st.markdown("""
<style>
  :root{
    --bg:#0b1530;          /* bleu foncé (fond) */
    --blue:#1d4ed8;        /* bleu principal (titres) */
    --blueDark:#1e3a8a;    /* bleu foncé pour textes dans cartes */
    --white:#ffffff;
    --border:#e5e7eb;
    --muted:#64748b;
  }
  .main{ background:var(--bg)!important; color:var(--white)!important; font-family:Inter,system-ui,Arial; }

  /* TITRES GLOBAUX : BLEU, SANS TEXT-SHADOW (fin du flou) */
  h1,h2,h3,h4,h5,h6{ color:var(--blue)!important; font-weight:800!important; text-shadow:none!important; letter-spacing:.2px; }

  /* Sélecteur & boutons */
  .stSelectbox > div > div{
    background:var(--white)!important; color:#0f172a!important; border:1px solid var(--border)!important; border-radius:10px!important;
  }
  .stButton>button{
    background:var(--blue)!important; color:#fff!important; border:0!important; border-radius:10px!important; font-weight:700!important;
    box-shadow:0 8px 18px rgba(29,78,216,.25)!important; transition:transform .15s, box-shadow .2s!important;
  }
  .stButton>button:hover{ transform:translateY(-1px)!important; box-shadow:0 10px 22px rgba(29,78,216,.30)!important; }

  /* CARTES : BLANCHES (contenu lisible bleu foncé) */
  .metric-card,.analysis-card,.thought-bubble{
    background:var(--white)!important; color:var(--blueDark)!important; border:1px solid var(--border)!important;
    border-radius:16px!important; padding:20px!important; box-shadow:0 10px 24px rgba(2,8,23,.18)!important;
  }
  .analysis-card h3,.analysis-card h4,.metric-card h3,.metric-card h4,.thought-bubble h3,.thought-bubble h4{
    color:var(--blue)!important; font-weight:800!important; margin:0 0 10px 0!important;
  }
  .analysis-card p,.metric-card p,.thought-bubble p{ color:var(--blueDark)!important; }

  /* Bulle pensée : liseré bleu sur fond blanc */
  .thought-bubble{ border-left:5px solid var(--blue)!important; animation:slideIn .3s ease-out; }
  @keyframes slideIn{ from{opacity:0; transform:translateX(-10px);} to{opacity:1; transform:translateX(0);} }

  /* Sections insights couleurs très légères */
  .ins-op{ background:#f0fdf4!important; border-left:6px solid #10b981!important; }
  .ins-th{ background:#fef2f2!important; border-left:6px solid #ef4444!important; }
  .ins-tr{ background:#eef2ff!important; border-left:6px solid #8b5cf6!important; }

  .block-container{ padding-top:1.2rem!important; }
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
        """Jauge de confiance (lisible sur fond blanc)"""
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = max(self.confidence_level, 0.1),  # valeur minimale pour affichage
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Confidence Level"},
            delta = {'reference': 80},
            gauge = {
                'axis': {'range': [None, 100], 'tickcolor': '#0f172a'},
                'bar': {'color': "#2563eb"},
                'steps': [
                    {'range': [0, 50], 'color': "#fee2e2"},
                    {'range': [50, 80], 'color': "#fef3c7"},
                    {'range': [80, 100], 'color': "#dcfce7"}
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
            font={'color': "#0f172a", 'family': "Inter, Arial"},
            height=300
        )
        return fig
    
    def generate_neural_network_viz(self) -> go.Figure:
        """Génère une visualisation du réseau neuronal"""
        n_nodes = 20
        x = [random.uniform(0, 10) for _ in range(n_nodes)]
        y = [random.uniform(0, 10) for _ in range(n_nodes)]
        edge_x, edge_y = [], []
        for i in range(n_nodes):
            for j in range(i+1, min(i+4, n_nodes)):
                if random.random() > 0.6:
                    edge_x.extend([x[i], x[j], None])
                    edge_y.extend([y[i], y[j], None])
        edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.7, color='#2563eb'),
                                hoverinfo='none', mode='lines', opacity=0.75)
        node_trace = go.Scatter(x=x, y=y, mode='markers', hoverinfo='text',
                                marker=dict(size=8, color='#60a5fa', line=dict(width=2, color='#1d4ed8')))
        fig = go.Figure(data=[edge_trace, node_trace])
        fig.update_layout(showlegend=False, hovermode='closest', margin=dict(b=20,l=5,r=5,t=40),
                          annotations=[dict(text="Neural Network Activity", showarrow=False,
                                            xref="paper", yref="paper", x=0.005, y=-0.002,
                                            xanchor='left', yanchor='bottom', font=dict(color="#0f172a", size=12))],
                          xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                          yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
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
            <h1 style='color:#1d4ed8!important; font-size: 3rem; margin: 0; font-weight:800;'>
                🧠 {agent.get_translation('agent_name')}
            </h1>
            <p style='color:#c7d2fe; font-size: 1.1rem; margin: 0;'>
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
            <h3>🧩 Agent Control Panel</h3>
        """, unsafe_allow_html=True)
        
        # Avatar de l'agent avec statut
        status_color = {
            "idle": "#6b7280",
            "thinking": "#f59e0b", 
            "analyzing": "#1d4ed8",
            "completed": "#10b981"
        }.get(agent.status, "#6b7280")
        
        st.markdown(f"""
        <div style='text-align: center; margin: 20px 0;'>
            <div style='position: relative; display: inline-block;'>
                <div style='width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(45deg, #1d4ed8, #2563eb); display: flex; align-items: center; justify-content: center; margin: 0 auto;'>
                    <span style='font-size: 2rem; color:#fff;'>🤖</span>
                </div>
                <div style='position: absolute; bottom: 0; right: 0; width: 20px; height: 20px; border-radius: 50%; background: {status_color}; border: 2px solid white;'></div>
            </div>
            <h4 style='color: #1e3a8a; margin: 10px 0 5px 0; font-weight:800;'>{agent.get_translation("agent_name")}</h4>
            <p style='color: var(--muted); font-size: 0.9rem; margin: 0;'>Neural Activity: {agent.neural_activity}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Statut de l'agent
        status_text = agent.get_translation(f"status_{agent.status}")
        st.markdown(f"""
        <div class='metric-card' style='text-align: center;'>
            <p style='color: #1e3a8a; margin: 0; font-weight: 800;'>{status_text}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sélection du secteur
        st.markdown("<p style='color:#ffffff; font-weight:700; margin-bottom: 8px;'>🎯 Target Sector:</p>", unsafe_allow_html=True)
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
                    <p style='color: var(--muted); margin: 0; font-size: 0.8rem;'>{metric}</p>
                    <p style='color: #1e3a8a; margin: 0; font-size: 1.2rem; font-weight: 800;'>{value}</p>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # Zone pensées
        if agent.status != "idle" and agent.thoughts:
            st.markdown("""
            <div class='analysis-card'>
                <h3>🧠 Agent Thought Process</h3>
            </div>
            """, unsafe_allow_html=True)
            for i, thought in enumerate(agent.thoughts):
                st.markdown(f"""
                <div class='thought-bubble'>
                    <div style='display: flex; align-items: center; margin-bottom: 8px;'>
                        <span style='background: linear-gradient(45deg, #1d4ed8, #2563eb); border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; margin-right: 12px; color:#fff;'>🤖</span>
                        <div>
                            <p style='margin: 0; font-size: 0.95rem; font-weight:700;'>{thought.content}</p>
                            <p style='color: var(--muted); margin: 0; font-size: 0.75rem;'>{thought.timestamp.strftime("%H:%M:%S")}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Résultats d'analyse
        if agent.current_analysis and agent.status == "completed":
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='analysis-card'>
                <h3>📋 Executive Summary</h3>
                <div style='background:#f8fbff; border:1px solid #e6efff; border-left:4px solid #1d4ed8; padding:18px; border-radius:10px;'>
                    <p style='margin:0; line-height:1.6;'>{agent.current_analysis.get("summary", "")}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # >>> JAUGE TOUJOURS VISIBLE PENDANT ANALYSE OU APRÈS <<<
        if agent.status in ["analyzing", "completed"]:
            st.markdown("""
            <div class='analysis-card'>
                <h3>📊 Confidence Analysis</h3>
            </div>
            """, unsafe_allow_html=True)
            confidence_fig = agent.generate_confidence_gauge()
            st.plotly_chart(confidence_fig, use_container_width=True)

        if agent.current_analysis and agent.status == "completed":
            # Insights
            insights = agent.current_analysis.get("insights", [])
            if insights:
                st.markdown("""
                <div class='analysis-card'>
                    <h3>🎯 Detected Insights</h3>
                </div>
                """, unsafe_allow_html=True)
                opportunities = [i for i in insights if i.category == "opportunity"]
                threats = [i for i in insights if i.category == "threat"]
                trends = [i for i in insights if i.category == "trend"]
                if opportunities:
                    st.markdown("<h4 style='color:#1d4ed8;'>💡 Opportunities</h4>", unsafe_allow_html=True)
                    for opp in opportunities:
                        st.markdown(f"""
                        <div class="metric-card ins-op">
                            <h5 style='color:#1e3a8a; margin:0 0 6px 0; font-weight:800;'>{opp.title}</h5>
                            <p style='margin:0 0 8px 0; font-size:.95rem;'>{opp.description}</p>
                            <div style='display:flex; gap:16px; align-items:center; color:#065f46; font-size:.9rem;'>
                                <span>Impact: <b>{opp.impact_score}/10</b></span>
                                <span>Confidence: <b>{opp.confidence}%</b></span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                if threats:
                    st.markdown("<h4 style='color:#1d4ed8;'>⚠️ Threats</h4>", unsafe_allow_html=True)
                    for threat in threats:
                        st.markdown(f"""
                        <div class="metric-card ins-th">
                            <h5 style='color:#1e3a8a; margin:0 0 6px 0; font-weight:800;'>{threat.title}</h5>
                            <p style='margin:0 0 8px 0; font-size:.95rem;'>{threat.description}</p>
                            <div style='display:flex; gap:16px; align-items:center; color:#7f1d1d; font-size:.9rem;'>
                                <span>Impact: <b>{threat.impact_score}/10</b></span>
                                <span>Confidence: <b>{threat.confidence}%</b></span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                if trends:
                    st.markdown("<h4 style='color:#1d4ed8;'>📈 Trends</h4>", unsafe_allow_html=True)
                    for trend in trends:
                        st.markdown(f"""
                        <div class="metric-card ins-tr">
                            <h5 style='color:#1e3a8a; margin:0 0 6px 0; font-weight:800;'>{trend.title}</h5>
                            <p style='margin:0 0 8px 0; font-size:.95rem;'>{trend.description}</p>
                            <div style='display:flex; gap:16px; align-items:center; color:#4c1d95; font-size:.9rem;'>
                                <span>Impact: <b>{trend.impact_score}/10</b></span>
                                <span>Confidence: <b>{trend.confidence}%</b></span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

            # Recommandations IA
            recommendations = agent.current_analysis.get("recommendations", [])
            if recommendations:
                st.markdown("""
                <div class='analysis-card'>
                    <h3>🎯 AI Recommendations</h3>
                </div>
                """, unsafe_allow_html=True)
                for i, rec in enumerate(recommendations, 1):
                    st.markdown(f"""
                    <div style='display:flex; align-items:start; background:#eef2ff; border:1px solid #e0e7ff; border-radius:12px; padding:14px; margin:10px 0;'>
                        <div style='background: linear-gradient(45deg,#1d4ed8,#2563eb); color:#fff; border-radius:50%; width:30px; height:30px; display:flex; align-items:center; justify-content:center; margin-right:12px; font-weight:800;'>{i}</div>
                        <p style='margin:0; line-height:1.55;'>{rec}</p>
                    </div>
                    """, unsafe_allow_html=True)

            # Actions & export (inchangés)
            st.markdown("""
            <div class='analysis-card'>
                <h3>📤 Export & Actions</h3>
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
                <div style='font-size: 4rem; margin-bottom: 20px; color: #1d4ed8;'>🤖</div>
                <h3>ARIA Ready for Mission</h3>
                <p style='color: var(--muted); margin-bottom: 26px;'>Select a target sector and activate the agent to begin strategic market analysis.</p>
                <div style='background:#f0f7ff; border:1px solid #dbeafe; border-radius:10px; padding:18px;'>
                    <h4 style='margin-bottom: 12px;'>🧠 Agent Capabilities</h4>
                    <ul style='color:#0f172a; text-align: left; list-style: none; padding: 0; margin:0;'>
                        <li style='margin: 8px 0;'>🔍 Multi-source market intelligence gathering</li>
                        <li style='margin: 8px 0;'>⚡ Real-time trend analysis and prediction</li>
                        <li style='margin: 8px 0;'>🎯 Strategic opportunity identification</li>
                        <li style='margin: 8px 0;'>📊 Risk assessment and mitigation strategies</li>
                        <li style='margin: 8px 0;'>🤖 AI-powered actionable recommendations</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Neural network visualization (sidebar)
    if agent.status in ["thinking", "analyzing"]:
        with st.sidebar:
            st.markdown("### 🧠 Neural Network Activity")
            neural_fig = agent.generate_neural_network_viz()
            st.plotly_chart(neural_fig, use_container_width=True)
    
    # Footer
    st.markdown("""
    <div style='margin-top: 36px; padding: 20px 0; border-top: 1px solid rgba(255,255,255,.12); text-align: center;'>
        <p style='color: #c7d2fe; margin: 0;'>
            🤖 ARIA - Autonomous Research & Intelligence Agent • Confidence Level: {confidence} 
        </p>
        <p style='color: #a5b4fc; font-size: 0.9rem; margin: 6px 0 0 0;'>
            Last Update: {timestamp} • Neural Activity: {activity} nodes
        </p>
    </div>
    """.format(
        confidence=f"{agent.confidence_level:.1f}%" if agent.confidence_level > 0 else "N/A",
        timestamp=datetime.now().strftime('%H:%M:%S'),
        activity=agent.neural_activity
    ), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
