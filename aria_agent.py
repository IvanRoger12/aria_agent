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

# =========================
# CONFIG DE PAGE (inchangé)
# =========================
st.set_page_config(
    page_title="🤖 ARIA - AI Strategic Intelligence Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CSS — FOND BLEU & TEXTE BLANC (lisible) + Logo ARIA lumineux
# =========================
st.markdown("""
<style>
/* Palette: bleu foncé + blanc, contrastes élevés */
:root{
  --bg:#0b1b3b;                 /* Bleu foncé uniforme (fond) */
  --card: rgba(16, 33, 74, .95); /* Cartes bleu profond, opaques pour lisibilité */
  --white:#ffffff;               /* Texte principal */
  --muted:#dbe7ff;               /* Texte secondaire */
  --blue:#2aa0ff;                /* Bleu accent (bordures, jauges) */
  --blue-soft:#78c3ff;           /* Bleu clair secondaire */
  --green:#10b981;               /* Vert (opportunités) */
  --red:#ef4444;                 /* Rouge (menaces) */
  --violet:#8b5cf6;              /* Violet (tendance / accent) */
}

.main {
  background: var(--bg) !important;   /* FOND UNIFORME */
  color: var(--white) !important;
}

/* TITRES => BLANC, gras, super lisibles */
h1, h2, h3, h4, h5, h6 {
  color: var(--white) !important;
  font-weight: 800 !important;
  letter-spacing: 0.2px;
  text-shadow: 0 0 6px rgba(0,0,0,.45);
  margin-top: .2rem;
  margin-bottom: .6rem;
}

/* Paragraphes / textes */
p, span, div, li {
  color: var(--white) !important;
}

/* Sélecteur (fond sombre, texte blanc) */
.stSelectbox > div > div {
  background: rgba(255,255,255,.06) !important;
  color: var(--white) !important;
  border: 1px solid rgba(255,255,255,.25) !important;
  border-radius: 10px !important;
}

/* Boutons (bleu -> violet mais discrets) */
.stButton > button {
  background: linear-gradient(135deg, #1f7ed8, #315bff) !important;
  color: #fff !important;
  border: 0 !important;
  border-radius: 12px !important;
  font-weight: 700 !important;
  box-shadow: 0 10px 25px rgba(31,126,216,.25) !important;
  transition: transform .15s ease, box-shadow .15s ease !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 18px 35px rgba(49,91,255,.35) !important;
}

/* Cartes (contrastées, pas de couleurs flashy en fond) */
.metric-card, .analysis-card {
  background: var(--card) !important;
  border: 1px solid rgba(255,255,255,.15) !important;
  border-radius: 18px !important;
  padding: 20px !important;
  margin: 12px 0 !important;
  box-shadow: 0 12px 40px rgba(0,0,0,.35) !important;
}

/* Avatar / badge ARIA lumineux (emoji “⭐” animée) */
.aria-logo-wrap{
  display:flex; align-items:center; gap:.6rem; justify-content:center;
}
.aria-logo{
  width:84px; height:84px; border-radius:50%;
  background: radial-gradient(circle at 50% 40%, rgba(255,255,255,.12), rgba(0,0,0,.25) 65%);
  border:2px solid rgba(255,255,255,.25);
  box-shadow: 0 0 24px rgba(42,160,255,.65), inset 0 0 18px rgba(255,255,255,.12);
  display:flex; align-items:center; justify-content:center;
  position:relative;
}
.aria-logo::after{
  content:"✨";                 /* EMOJI “lumières” */
  font-size:1.35rem;
  position:absolute;
  right:-6px; top:-6px;
  animation: twinkle 1.6s ease-in-out infinite;
}
@keyframes twinkle {
  0%,100% { transform: scale(1); opacity: 1; filter: drop-shadow(0 0 8px rgba(255,255,255,.8)); }
  50% { transform: scale(1.15); opacity: .8; filter: drop-shadow(0 0 2px rgba(255,255,255,.3)); }
}

/* Statut clignotant discret */
.status-dot{
  width: 12px; height: 12px; border-radius: 50%;
  border:2px solid rgba(255,255,255,.85);
  box-shadow: 0 0 12px rgba(255,255,255,.35);
  display:inline-block;
  animation: blink 1.4s ease-in-out infinite;
}
@keyframes blink {
  0%,100% { opacity: 1; }
  50% { opacity: .55; }
}

/* Pensées (bord bleu, fond sombre, lisibles) */
.thought-bubble {
  background: rgba(255,255,255,.06) !important;
  border-left: 5px solid var(--blue) !important;
  padding: 14px !important;
  border-radius: 0 12px 12px 0 !important;
  animation: slideIn .45s ease-out;
}
@keyframes slideIn { from{opacity:0; transform:translateX(-12px);} to{opacity:1; transform:translateX(0);} }

/* Sections “insights” gardent le code original mais plus lisibles */
.ins-op-bg { background: rgba(16,185,129,.12); border-left: 5px solid var(--green); }
.ins-th-bg { background: rgba(239,68,68,.12);  border-left: 5px solid var(--red);   }
.ins-tr-bg { background: rgba(139,92,246,.12);  border-left: 5px solid var(--violet);}

/* Encarts d’information */
.info-block {
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(255,255,255,.18);
  border-radius: 12px;
  padding: 12px;
}

/* Footer fin */
.footer {
  border-top: 1px solid rgba(255,255,255,.12);
  padding: 26px 0;
  text-align:center;
  opacity: .92;
}

/* Supprimer dégradés flashy pré-existants dans header */
.no-gradient {
  -webkit-text-fill-color: var(--white) !important;
  background: none !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# DATA MODELS (inchangé)
# =========================
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

# =========================
# AGENT (inchangé)
# =========================
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

        # Données simulées (inchangé)
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
        """Génère un graphique de confiance (inchangé)"""
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = self.confidence_level,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Confidence Level"},
            delta = {'reference': 80},
            gauge = {
                'axis': {'range': [None, 100], 'tickcolor':'#ffffff'},
                'bar': {'color': "#2aa0ff"},
                'steps': [
                    {'range': [0, 50], 'color': "#2d3e66"},
                    {'range': [50, 80], 'color': "#345994"},
                    {'range': [80, 100], 'color': "#3b7fce"}
                ],
                'threshold': {
                    'line': {'color': "#78c3ff", 'width': 4},
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
        """Génère une visualisation du réseau neuronal (inchangé)"""
        n_nodes = 20
        x = [random.uniform(0, 10) for _ in range(n_nodes)]
        y = [random.uniform(0, 10) for _ in range(n_nodes)]
        edge_x = []; edge_y = []
        for i in range(n_nodes):
            for j in range(i+1, min(i+4, n_nodes)):
                if random.random() > 0.6:
                    edge_x.extend([x[i], x[j], None])
                    edge_y.extend([y[i], y[j], None])
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y, line=dict(width=0.6, color='#2aa0ff'),
            hoverinfo='none', mode='lines', opacity=0.7
        )
        node_trace = go.Scatter(
            x=x, y=y, mode='markers', hoverinfo='text',
            marker=dict(size=8, color='#78c3ff', line=dict(width=2, color='#2aa0ff'))
        )
        fig = go.Figure(data=[edge_trace, node_trace])
        fig.update_layout(
            showlegend=False, hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            annotations=[ dict(
                text="Neural Network Activity", showarrow=False,
                xref="paper", yref="paper", x=0.005, y=-0.002,
                xanchor='left', yanchor='bottom',
                font=dict(color="white", size=12)
            )],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        return fig

# =========================
# UI (structure inchangée, styles corrigés)
# =========================
def main():
    # Init
    if 'agent' not in st.session_state:
        st.session_state.agent = ARIAAgent()
    if 'language' not in st.session_state:
        st.session_state.language = 'fr'

    agent = st.session_state.agent
    agent.language = st.session_state.language

    # Header (même structure — texte blanc, pas de gradient flashy)
    col1, col2, col3 = st.columns([6, 1, 1])
    with col1:
        st.markdown(f"""
        <div style='margin-bottom: 22px;'>
            <div class="aria-logo-wrap">
                <div class="aria-logo"><div style="font-size:2rem;">🤖</div></div>
            </div>
            <h1 class="no-gradient" style="font-size: 2.6rem; margin: 6px 0 2px 0;">{agent.get_translation('agent_name')}</h1>
            <p style='color: var(--muted); font-size: 1.05rem; margin: 0;'>
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

    # Layout principal (inchangé)
    col1, col2 = st.columns([1, 2])

    with col1:
        # Panneau de contrôle (inchangé)
        st.markdown("""
        <div class='analysis-card'>
            <h3 style='text-align: center; margin-bottom: 12px;'>🤖 Agent Control Panel</h3>
        """, unsafe_allow_html=True)

        status_color = {
            "idle": "#9aa3b2",
            "thinking": "#ffd166",
            "analyzing": "#2aa0ff",
            "completed": "#10b981"
        }.get(agent.status, "#9aa3b2")

        st.markdown(f"""
        <div style='text-align: center; margin: 10px 0 16px 0;'>
            <div style='position: relative; display: inline-flex; flex-direction:column; align-items:center; gap:10px;'>
                <div class="aria-logo"></div>
                <div style="display:flex; align-items:center; gap:8px;">
                    <span class="status-dot" style="background:{status_color};"></span>
                    <span style="color:var(--muted); font-weight:700; letter-spacing:.3px;">SIMULATION AGENT IA</span>
                </div>
            </div>
            <h4 style='margin: 10px 0 5px 0;'>{agent.get_translation("agent_name")}</h4>
            <p style='color: var(--muted); font-size: 0.9rem; margin: 0;'>Neural Activity: {agent.neural_activity}</p>
        </div>
        """, unsafe_allow_html=True)

        status_text = agent.get_translation(f"status_{agent.status}")
        st.markdown(f"""
        <div class="info-block" style='text-align:center; margin-bottom:10px;'>
            <p style='margin:0; font-weight:700;'>{status_text}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<p style='font-weight:700; margin:12px 0 8px 0;'>🎯 Target Sector:</p>", unsafe_allow_html=True)
        sectors = agent.get_translation("sectors")
        sector_options = list(sectors.keys())
        selected_sector = st.selectbox(
            "Select sector",
            sector_options,
            format_func=lambda x: sectors[x],
            label_visibility="collapsed"
        )

        st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

        if agent.status in ["idle", "completed"]:
            if st.button("🚀 Activate ARIA Agent", key="activate_btn", type="primary", use_container_width=True):
                with st.spinner("Agent activation in progress..."):
                    try:
                        loop = asyncio.get_event_loop()
                    except RuntimeError:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                    loop.run_until_complete(agent.activate(selected_sector))
                    st.rerun()
        else:
            if st.button("⏹️ Stop Agent", key="stop_btn", use_container_width=True):
                agent.status = "idle"
                agent.thoughts = []
                agent.current_analysis = None
                st.rerun()

        if agent.status != "idle":
            st.markdown("<h4 style='margin-top:14px;'>📊 Real-time Metrics</h4>", unsafe_allow_html=True)
            metrics_data = {
                "Neural Activity": f"{agent.neural_activity}",
                "Data Sources": "847",
                "Insights Generated": f"{len([t for t in agent.thoughts if t.confidence > 0.8])}",
                "Confidence": f"{agent.confidence_level:.1f}%" if agent.confidence_level > 0 else "N/A"
            }
            for metric, value in metrics_data.items():
                st.markdown(f"""
                <div class='metric-card'>
                    <p style='color: var(--muted); margin: 0; font-size: 0.85rem;'>{metric}</p>
                    <p style='margin: 0; font-size: 1.2rem; font-weight: 800;'>{value}</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        # Pensées (inchangé)
        if agent.status != "idle" and agent.thoughts:
            st.markdown("""
            <div class='analysis-card'>
                <h3 style='margin-bottom: 12px;'>🧠 Agent Thought Process</h3>
            </div>
            """, unsafe_allow_html=True)
            for i, thought in enumerate(agent.thoughts):
                st.markdown(f"""
                <div class='thought-bubble'>
                    <div style='display: flex; align-items: center; margin-bottom: 6px; gap:12px;'>
                        <span style='background: rgba(255,255,255,.08); border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center;'>
                            🤖
                        </span>
                        <div>
                            <p style='margin: 0; font-size: 0.98rem; font-weight:700;'>{thought.content}</p>
                            <p style='color: var(--muted); margin: 2px 0 0 0; font-size: 0.78rem;'>{thought.timestamp.strftime("%H:%M:%S")}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Résultats (inchangé)
        if agent.current_analysis and agent.status == "completed":
            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

            st.markdown(f"""
            <div class='analysis-card'>
                <h3 style='margin-bottom: 12px;'>📋 Executive Summary</h3>
                <div class='info-block' style='border-left: 5px solid var(--blue);'>
                    <p style='margin: 0; line-height: 1.6; font-size: 1rem; color: var(--muted);'>{agent.current_analysis.get("summary", "")}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # JAUGE (conservée)
            if agent.confidence_level > 0:
                st.markdown("""
                <div class='analysis-card'>
                    <h3 style='margin-bottom: 12px;'>📊 Confidence Analysis</h3>
                </div>
                """, unsafe_allow_html=True)
                confidence_fig = agent.generate_confidence_gauge()
                st.plotly_chart(confidence_fig, use_container_width=True)

            insights = agent.current_analysis.get("insights", [])
            if insights:
                st.markdown("""
                <div class='analysis-card'>
                    <h3 style='margin-bottom: 12px;'>🎯 Detected Insights</h3>
                </div>
                """, unsafe_allow_html=True)

                opportunities = [i for i in insights if i.category == "opportunity"]
                threats = [i for i in insights if i.category == "threat"]
                trends = [i for i in insights if i.category == "trend"]

                if opportunities:
                    st.markdown("<h4>💡 Opportunities</h4>", unsafe_allow_html=True)
                    for opp in opportunities:
                        st.markdown(f"""
                        <div class='info-block ins-op-bg'>
                            <h5 style='margin: 0 0 6px 0;'>{opp.title}</h5>
                            <p style='color: var(--muted); margin: 0 0 8px 0; font-size: 0.95rem;'>{opp.description}</p>
                            <div style='display: flex; gap: 18px; font-size: .9rem;'>
                                <span>Impact: <b>{opp.impact_score}/10</b></span>
                                <span>Confidence: <b>{opp.confidence}%</b></span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                if threats:
                    st.markdown("<h4>⚠️ Threats</h4>", unsafe_allow_html=True)
                    for threat in threats:
                        st.markdown(f"""
                        <div class='info-block ins-th-bg'>
                            <h5 style='margin: 0 0 6px 0;'>{threat.title}</h5>
                            <p style='color: var(--muted); margin: 0 0 8px 0; font-size: 0.95rem;'>{threat.description}</p>
                            <div style='display: flex; gap: 18px; font-size: .9rem;'>
                                <span>Impact: <b>{threat.impact_score}/10</b></span>
                                <span>Confidence: <b>{threat.confidence}%</b></span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                if trends:
                    st.markdown("<h4>📈 Trends</h4>", unsafe_allow_html=True)
                    for trend in trends:
                        st.markdown(f"""
                        <div class='info-block ins-tr-bg'>
                            <h5 style='margin: 0 0 6px 0;'>{trend.title}</h5>
                            <p style='color: var(--muted); margin: 0 0 8px 0; font-size: 0.95rem;'>{trend.description}</p>
                            <div style='display: flex; gap: 18px; font-size: .9rem;'>
                                <span>Impact: <b>{trend.impact_score}/10</b></span>
                                <span>Confidence: <b>{trend.confidence}%</b></span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

            # Actions & Export (inchangé)
            recommendations = agent.current_analysis.get("recommendations", [])
            if recommendations:
                st.markdown("""
                <div class='analysis-card'>
                    <h3 style='margin-bottom: 12px;'>🎯 AI Recommendations</h3>
                </div>
                """, unsafe_allow_html=True)
                for i, rec in enumerate(recommendations, 1):
                    st.markdown(f"""
                    <div class='info-block' style='background: rgba(255,255,255,.06); border-left: 5px solid var(--blue);'>
                        <div style='display: flex; align-items: start; gap: 12px;'>
                            <div style='min-width: 30px; height: 30px; border-radius: 50%; background: #2a67ff; display:flex; align-items:center; justify-content:center; color:#fff; font-weight:800;'>{i}</div>
                            <p style='margin:0; line-height:1.55;'>{rec}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("""
            <div class='analysis-card'>
                <h3 style='margin-bottom: 12px;'>📤 Export & Actions</h3>
            </div>
            """, unsafe_allow_html=True)

            colA, colB, colC = st.columns(3)
            with colA:
                if st.button("📄 Export Report", key="export_btn"):
                    report_content = f"""
ARIA - STRATEGIC INTELLIGENCE REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Sector: {selected_sector}
Confidence Level: {agent.confidence_level:.1f}%

EXECUTIVE SUMMARY:
{agent.current_analysis.get('summary', '')}

KEY INSIGHTS:
"""
                    for insight in insights:
                        report_content += f"- {insight.title} (Impact: {insight.impact_score}/10, Confidence: {insight.confidence}%)\n  {insight.description}\n"
                    report_content += "\nRECOMMENDATIONS:\n"
                    for i, rec in enumerate(recommendations, 1):
                        report_content += f"{i}. {rec}\n"

                    st.download_button(
                        label="⬇️ Download Report (TXT)",
                        data=report_content.encode('utf-8'),
                        file_name=f"aria_report_{selected_sector}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain"
                    )
            with colB:
                if st.button("🔔 Setup Alerts", key="alerts_btn"):
                    st.success("✅ Alert system configured! You'll receive notifications for market changes.")
            with colC:
                if st.button("🔄 Re-analyze", key="reanalyze_btn"):
                    agent.status = "idle"
                    agent.thoughts = []
                    agent.current_analysis = None
                    agent.confidence_level = 0
                    st.rerun()

        # Écran initial (inchangé)
        elif agent.status == "idle":
            st.markdown("""
            <div class='analysis-card' style='text-align: center; padding: 36px;'>
                <div style='font-size: 3rem; margin-bottom: 12px;'>🤖</div>
                <h3 style='margin-bottom: 8px;'>ARIA Ready for Mission</h3>
                <p style='color: var(--muted); margin-bottom: 18px;'>Select a target sector and activate the agent to begin strategic market analysis.</p>
                <div class='info-block' style='border-left:5px solid var(--blue);'>
                    <h4 style='margin: 0 0 8px 0;'>🧠 Agent Capabilities</h4>
                    <ul style='text-align: left; margin:0;'>
                        <li>🔍 Multi-source market intelligence gathering</li>
                        <li>⚡ Real-time trend analysis and prediction</li>
                        <li>🎯 Strategic opportunity identification</li>
                        <li>📊 Risk assessment and mitigation strategies</li>
                        <li>🤖 AI-powered actionable recommendations</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Neural viz (inchangé)
    if agent.status in ["thinking", "analyzing"]:
        with st.sidebar:
            st.markdown("### 🧠 Neural Network Activity")
            neural_fig = agent.generate_neural_network_viz()
            st.plotly_chart(neural_fig, use_container_width=True)

    # Footer (blanc/bleu)
    st.markdown(f"""
    <div class='footer'>
        <p style='margin:0; color: var(--muted);'>
            🤖 ARIA - Autonomous Research & Intelligence Agent |
            Confidence: {f"{agent.confidence_level:.1f}%" if agent.confidence_level > 0 else "N/A"} |
            Last Update: {datetime.now().strftime('%H:%M:%S')}
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

# =======================
# DEPLOIEMENT (inchangé)
# =======================
"""
Requirements (requirements.txt):
-------------------------------
streamlit>=1.28.0
plotly>=5.17.0
asyncio
requests>=2.31.0

Run:
----
streamlit run app.py
"""
