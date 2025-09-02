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
# CONFIGURATION DE LA PAGE
# =========================
st.set_page_config(
    page_title="🤖 ARIA - AI Strategic Intelligence Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CSS — LISIBILITÉ & NÉON
# =========================
st.markdown("""
<style>
    :root{
        --bg1:#111827;           /* gris très sombre */
        --bg2:#0b1020;           /* bleu nuit */
        --card: rgba(18, 24, 38, 0.95); /* quasi opaque pour un texte net */
        --white:#ffffff;
        --muted:#dfe7ff;
        --soft:#c7cdd8;
        --blue:#3b82f6;
        --violet:#8b5cf6;
        --teal:#06b6d4;
        --green:#10b981;
        --yellow:#FFD700;
        --danger:#ef4444;
    }

    .main {
        background: radial-gradient(1200px 800px at 10% -10%, rgba(59,130,246,.15), transparent 50%),
                    radial-gradient(1000px 700px at 90% 10%, rgba(139,92,246,.18), transparent 60%),
                    linear-gradient(135deg, var(--bg1) 0%, var(--bg2) 100%);
        color: var(--white);
    }

    /* Cartes très lisibles */
    .analysis-card, .metric-card, .thought-bubble, .glass, .neon-card {
        background: var(--card);
        backdrop-filter: blur(2px);
        -webkit-backdrop-filter: blur(2px);
        border: 1px solid rgba(255,255,255,.18);
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 12px 40px rgba(0,0,0,.35);
    }

    /* Titres / sous-titres ULTRA lisibles */
    h1, h2, h3, h4, h5, h6 { color: var(--white) !important; }
    .subtitle-white {
        color: var(--white) !important;
        font-weight: 800 !important;
        letter-spacing: .3px;
        text-shadow: 0 0 6px rgba(0,0,0,.55);
    }
    .subtitle-yellow {
        color: var(--yellow) !important;
        font-weight: 800 !important;
        letter-spacing: .3px;
        text-shadow: 0 0 10px rgba(255,215,0,.75);
    }
    .muted { color: var(--soft) !important; }

    /* Boutons */
    .stButton > button {
        background: linear-gradient(135deg, var(--blue), var(--violet));
        color: var(--white);
        border: 0;
        border-radius: 12px;
        font-weight: 700;
        box-shadow: 0 10px 25px rgba(59,130,246,.35);
        transition: transform .2s ease, box-shadow .2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 16px 35px rgba(139,92,246,.45);
    }

    /* Selectbox contrasté */
    .stSelectbox > div > div {
        background: rgba(255,255,255,.06) !important;
        color: var(--white) !important;
        border: 1px solid rgba(255,255,255,.25) !important;
        border-radius: 10px !important;
    }

    /* Pensées */
    .thought-bubble{
        border-left: 5px solid var(--blue);
        animation: slideIn .45s ease-out;
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-18px); }
        to   { opacity: 1; transform: translateX(0); }
    }

    /* Indicateurs de statut */
    .status-dot {
        width: 14px; height: 14px; border-radius: 50%;
        border: 2px solid rgba(255,255,255,.85);
        box-shadow: 0 0 12px currentColor;
    }

    /* Badge clignotant SIMULATION ACTIVE */
    .sim-badge {
        display:inline-flex; align-items:center; gap:.5rem;
        background: rgba(255,215,0,.12);
        border:1px solid rgba(255,215,0,.6);
        padding:.35rem .75rem; border-radius: 999px;
        color: var(--yellow); font-weight:800; letter-spacing:.5px;
        text-shadow: 0 0 10px rgba(255,215,0,.75);
        box-shadow: 0 0 18px rgba(255,215,0,.25), inset 0 0 10px rgba(255,215,0,.12);
        animation: neonBlink 1.2s ease-in-out infinite;
    }
    .sim-dot {
        width:10px; height:10px; border-radius: 50%;
        background: var(--yellow);
        box-shadow: 0 0 10px var(--yellow), 0 0 20px var(--yellow);
    }
    @keyframes neonBlink {
        0%, 100% { filter: drop-shadow(0 0 8px rgba(255,215,0,.9)); opacity: 1; }
        50% { filter: drop-shadow(0 0 2px rgba(255,215,0,.3)); opacity: .65; }
    }

    /* Avatar agent avec halo */
    .agent-avatar {
        width: 100px; height: 100px; border-radius: 50%;
        margin: 0 auto;
        background: conic-gradient(from 180deg, var(--yellow), var(--blue), var(--violet), var(--yellow));
        position: relative;
        box-shadow: 0 0 24px rgba(59,130,246,.6);
        animation: slowSpin 10s linear infinite;
    }
    .agent-avatar::after{
        content:'🤖';
        position:absolute; inset:10px;
        display:flex; align-items:center; justify-content:center;
        background: radial-gradient(circle at 50% 35%, rgba(0,0,0,.0), rgba(0,0,0,.35) 65%);
        border-radius:50%;
        font-size: 2rem;
        text-shadow: 0 2px 8px rgba(0,0,0,.65);
        color: var(--white);
    }
    @keyframes slowSpin { from{ transform: rotate(0deg); } to { transform: rotate(360deg); } }

    /* Cartes d’insight colorées */
    .ins-card { border-radius:16px; padding:16px; margin:10px 0; }
    .ins-opp { background: rgba(16,185,129,.12); border-left: 6px solid var(--green); }
    .ins-thr { background: rgba(239,68,68,.12);  border-left: 6px solid var(--danger); }
    .ins-trd { background: rgba(139,92,246,.12);  border-left: 6px solid var(--violet); }
</style>
""", unsafe_allow_html=True)

# =========================
# Modèles de données
# =========================
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
    category: str  # opportunity, threat, trend

# =========================
# ARIA Agent (structure conservée)
# =========================
class ARIAAgent:
    def __init__(self, language: str = "fr"):
        self.language = language
        self.status = "idle"  # idle, thinking, analyzing, completed
        self.thoughts: List[AgentThought] = []
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
            self.thoughts.append(AgentThought(
                content=thought_text,
                timestamp=datetime.now(),
                confidence=random.uniform(0.7, 0.95)
            ))

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
            title = {'text': "Confidence Level"},
            delta = {'reference': 80},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#3b82f6"},
                'steps': [
                    {'range': [0, 50], 'color': "#ef4444"},
                    {'range': [50, 80], 'color': "#f59e0b"},
                    {'range': [80, 100], 'color': "#10b981"}
                ],
                'threshold': {'line': {'color': "#8b5cf6", 'width': 4}, 'thickness': 0.75, 'value': 90}
            }
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "white", 'family': "Inter, Arial"},
            height=320
        )
        return fig

    def generate_neural_network_viz(self) -> go.Figure:
        n_nodes = 20
        x = [random.uniform(0, 10) for _ in range(n_nodes)]
        y = [random.uniform(0, 10) for _ in range(n_nodes)]
        edge_x, edge_y = [], []
        for i in range(n_nodes):
            for j in range(i+1, min(i+4, n_nodes)):
                if random.random() > 0.6:
                    edge_x.extend([x[i], x[j], None])
                    edge_y.extend([y[i], y[j], None])
        edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color='#3b82f6'),
                                hoverinfo='none', mode='lines', opacity=0.6)
        node_trace = go.Scatter(x=x, y=y, mode='markers', hoverinfo='text',
                                marker=dict(size=8, color='#60a5fa', line=dict(width=2, color='#3b82f6')))
        fig = go.Figure(data=[edge_trace, node_trace])
        fig.update_layout(showlegend=False, hovermode='closest',
                          margin=dict(b=20,l=5,r=5,t=30),
                          xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                          yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        return fig

# =========================
# UI
# =========================
def main():
    if 'agent' not in st.session_state:
        st.session_state.agent = ARIAAgent()
    if 'language' not in st.session_state:
        st.session_state.language = 'fr'

    agent = st.session_state.agent
    agent.language = st.session_state.language

    # Header
    c1, c2, c3 = st.columns([6,1,1])
    with c1:
        st.markdown(f"""
        <div class="glass" style="padding:20px; margin-bottom:18px;">
            <h1 class="subtitle-white" style="margin:0; font-size:2.4rem;">🧠 {agent.get_translation('agent_name')}</h1>
            <p class="muted" style="margin:.25rem 0 0 0;">{agent.get_translation('agent_desc')}</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        lang = st.selectbox("🌐", ["🇫🇷 FR", "🇺🇸 EN"], key="lang_select")
        new_language = "fr" if "FR" in lang else "en"
        if new_language != st.session_state.language:
            st.session_state.language = new_language
            st.rerun()

    # Layout
    col1, col2 = st.columns([1,2])

    # ---------------- LEFT PANEL ----------------
    with col1:
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="subtitle-white" style="text-align:center;margin-bottom:14px;">🤖 Agent Control Panel</h3>', unsafe_allow_html=True)

        status_color = {
            "idle": "#6b7280",
            "thinking": "#f59e0b",
            "analyzing": "#3b82f6",
            "completed": "#10b981"
        }.get(agent.status, "#6b7280")

        st.markdown(f"""
        <div style='text-align:center; margin: 8px 0 14px 0;'>
            <div class="agent-avatar"></div>
            <div style="margin-top:8px; display:flex; align-items:center; gap:8px; justify-content:center;">
                <span class="status-dot" style="background:{status_color};"></span>
                <span class="sim-badge"><span class="sim-dot"></span>SIMULATION ACTIVE</span>
            </div>
            <p class="muted" style='margin:.5rem 0 0 0;'>Neural Activity: {agent.neural_activity}</p>
        </div>
        """, unsafe_allow_html=True)

        status_text = agent.get_translation(f"status_{agent.status}")
        st.markdown(f"""
        <div class="neon-card" style='padding:12px; text-align:center;'>
            <p class="subtitle-white" style='margin:0; font-size:1rem;'>{status_text}</p>
        </div>
        """, unsafe_allow_html=True)

        # Secteurs (inchangé)
        st.markdown('<p class="subtitle-white" style="margin:16px 0 8px 0;">🎯 Target Sector</p>', unsafe_allow_html=True)
        sectors = agent.get_translation("sectors")
        selected_sector = st.selectbox("Select sector", list(sectors.keys()),
                                       format_func=lambda x: sectors[x], label_visibility="collapsed")

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

        # Metrics
        if agent.status != "idle":
            st.markdown('<h4 class="subtitle-white" style="margin-top:18px;">📊 Real-time Metrics</h4>', unsafe_allow_html=True)
            metrics = {
                "Neural Activity": f"{agent.neural_activity}",
                "Data Sources": "847",
                "Insights Generated": f"{len([t for t in agent.thoughts if t.confidence > 0.8])}",
                "Confidence": f"{agent.confidence_level:.1f}%" if agent.confidence_level > 0 else "N/A"
            }
            for k, v in metrics.items():
                st.markdown(f"""
                <div class="metric-card">
                    <p class="muted" style="margin:0; font-size:.8rem;">{k}</p>
                    <p class="subtitle-white" style="margin:0; font-size:1.2rem;">{v}</p>
                </div>""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- RIGHT PANEL ----------------
    with col2:

        # Pensées
        if agent.status != "idle" and agent.thoughts:
            st.markdown('<div class="analysis-card"><h3 class="subtitle-yellow" style="margin-bottom:10px;">🧠 Agent Thought Process</h3></div>', unsafe_allow_html=True)
            for i, thought in enumerate(agent.thoughts):
                st.markdown(f"""
                <div class="thought-bubble">
                    <div style='display:flex; align-items:flex-start; gap:12px;'>
                        <div style='background:linear-gradient(135deg, var(--blue), var(--violet)); width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;'>🤖</div>
                        <div>
                            <p class="subtitle-white" style='margin:0; font-size:.98rem;'>{thought.content}</p>
                            <p class='muted' style='margin:4px 0 0 0; font-size:.78rem;'>{thought.timestamp.strftime("%H:%M:%S")} • {thought.confidence:.0%} conf.</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Résultats
        if agent.current_analysis and agent.status == "completed":
            st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

            # Executive Summary
            st.markdown(f"""
            <div class='analysis-card'>
                <h3 class="subtitle-white" style='margin-bottom:12px;'>📋 Executive Summary</h3>
                <div style='background:linear-gradient(135deg, rgba(59,130,246,.18), rgba(139,92,246,.18)); border-left: 6px solid var(--blue); border-radius:12px; padding:16px;'>
                    <p style='color:var(--muted); margin:0; line-height:1.6; font-size:1rem;'>{agent.current_analysis.get("summary","")}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Confidence gauge
            if agent.confidence_level > 0:
                st.markdown('<div class="analysis-card"><h3 class="subtitle-yellow" style="margin-bottom:10px;">📊 Confidence Analysis</h3></div>', unsafe_allow_html=True)
                st.plotly_chart(agent.generate_confidence_gauge(), use_container_width=True)

            # Insights
            insights = agent.current_analysis.get("insights", [])
            if insights:
                st.markdown('<div class="analysis-card"><h3 class="subtitle-white" style="margin-bottom:10px;">🎯 Detected Insights</h3></div>', unsafe_allow_html=True)
                opps   = [i for i in insights if i.category == "opportunity"]
                thrs   = [i for i in insights if i.category == "threat"]
                trnds  = [i for i in insights if i.category == "trend"]

                if opps:
                    st.markdown('<h4 class="subtitle-white">💡 Opportunities</h4>', unsafe_allow_html=True)
                    for it in opps:
                        st.markdown(f"""
                        <div class="ins-card ins-opp">
                            <h5 class="subtitle-white" style="margin:0 0 6px 0;">{it.title}</h5>
                            <p class="muted" style="margin:0 0 8px 0;">{it.description}</p>
                            <div style="display:flex;gap:18px;color:#a7f3d0;font-size:.85rem;">
                                <span>Impact: <b>{it.impact_score}/10</b></span>
                                <span>Confidence: <b>{it.confidence}%</b></span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                if thrs:
                    st.markdown('<h4 class="subtitle-white">⚠️ Threats</h4>', unsafe_allow_html=True)
                    for it in thrs:
                        st.markdown(f"""
                        <div class="ins-card ins-thr">
                            <h5 class="subtitle-white" style="margin:0 0 6px 0;">{it.title}</h5>
                            <p class="muted" style="margin:0 0 8px 0;">{it.description}</p>
                            <div style="display:flex;gap:18px;color:#fecaca;font-size:.85rem;">
                                <span>Impact: <b>{it.impact_score}/10</b></span>
                                <span>Confidence: <b>{it.confidence}%</b></span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                if trnds:
                    st.markdown('<h4 class="subtitle-white">📈 Trends</h4>', unsafe_allow_html=True)
                    for it in trnds:
                        st.markdown(f"""
                        <div class="ins-card ins-trd">
                            <h5 class="subtitle-white" style="margin:0 0 6px 0;">{it.title}</h5>
                            <p class="muted" style="margin:0 0 8px 0;">{it.description}</p>
                            <div style="display:flex;gap:18px;color:#ddd6fe;font-size:.85rem;">
                                <span>Impact: <b>{it.impact_score}/10</b></span>
                                <span>Confidence: <b>{it.confidence}%</b></span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

            # Recommandations
            recs = agent.current_analysis.get("recommendations", [])
            if recs:
                st.markdown('<div class="analysis-card"><h3 class="subtitle-yellow" style="margin-bottom:10px;">🎯 AI Recommendations</h3></div>', unsafe_allow_html=True)
                for i, rec in enumerate(recs, 1):
                    st.markdown(f"""
                    <div class="neon-card" style="background:rgba(139,92,246,.12); border-radius:14px; padding:14px; margin:10px 0;">
                        <div style="display:flex; gap:12px; align-items:flex-start;">
                            <div style="width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg, var(--blue), var(--violet)); display:flex;align-items:center;justify-content:center;color:white;font-weight:800;">{i}</div>
                            <p class="subtitle-white" style="margin:0; line-height:1.55;">{rec}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # Actions
            st.markdown('<div class="analysis-card"><h3 class="subtitle-white" style="margin-bottom:10px;">📤 Export & Actions</h3></div>', unsafe_allow_html=True)
            cxa, cxb, cxc = st.columns(3)
            with cxa:
                if st.button("📄 Export Report", key="export_btn"):
                    report = f"""
ARIA - STRATEGIC INTELLIGENCE REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Sector: {selected_sector}
Confidence: {agent.confidence_level:.1f}%

EXECUTIVE SUMMARY:
{agent.current_analysis.get('summary','')}

KEY INSIGHTS:
"""
                    for i in insights:
                        report += f"- {i.title} | Impact {i.impact_score}/10 | Conf. {i.confidence}%\n  {i.description}\n"
                    report += "\nRECOMMENDATIONS:\n"
                    for idx, rec in enumerate(recs, 1):
                        report += f"{idx}. {rec}\n"

                    st.download_button("⬇️ Download Report",
                                       data=report.encode('utf-8'),
                                       file_name=f"aria_report_{selected_sector}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                                       mime="text/plain")
            with cxb:
                if st.button("🔔 Setup Alerts", key="alerts_btn"):
                    st.success("✅ Alert system configured! You'll receive notifications for market changes.")
            with cxc:
                if st.button("🔄 Re-analyze", key="reanalyze_btn"):
                    agent.status = "idle"
                    agent.thoughts = []
                    agent.current_analysis = None
                    agent.confidence_level = 0
                    st.rerun()

        # État initial
        elif agent.status == "idle":
            st.markdown("""
            <div class='analysis-card' style='text-align:center; padding:46px 26px;'>
                <div style='font-size:4rem;margin-bottom:18px;'>🤖</div>
                <h3 class='subtitle-white' style='margin-bottom:10px;'>ARIA Ready for Mission</h3>
                <p class='muted' style='margin-bottom:22px;'>Select a target sector and activate the agent to begin strategic market analysis.</p>
                <div style='background: rgba(59,130,246,.12); border:1px solid rgba(59,130,246,.35); border-radius:12px; padding:18px;'>
                    <h4 class='subtitle-yellow' style='margin:0 0 10px 0;'>🧠 Agent Capabilities</h4>
                    <ul style='text-align:left; margin:0;'>
                        <li>🔍 Multi-source market intelligence</li>
                        <li>⚡ Real-time trend prediction</li>
                        <li>🎯 Strategic opportunity identification</li>
                        <li>📊 Risk assessment & mitigation</li>
                        <li>🤖 AI-powered recommendations</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Neural viz en sidebar pendant thinking/analyzing
    if agent.status in ["thinking", "analyzing"]:
        with st.sidebar:
            st.markdown('<h4 class="subtitle-white">🧠 Neural Network Activity</h4>', unsafe_allow_html=True)
            st.plotly_chart(agent.generate_neural_network_viz(), use_container_width=True)

    # Footer
    st.markdown(f"""
    <div style='margin-top:26px; padding:16px 0; text-align:center; opacity:.85;'>
        <p class='muted' style='margin:0;'>
            🤖 ARIA • Confidence: {f"{agent.confidence_level:.1f}%" if agent.confidence_level>0 else "N/A"} • Last Update: {datetime.now().strftime('%H:%M:%S')}
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
