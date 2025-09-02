# app.py
# 🤖 ARIA – Autonomous Research & Intelligence Agent (Streamlit)
# Design futuriste (glassmorphism), bilingue FR/EN, animations, jauges, export.

import streamlit as st
import asyncio
import random
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional
import plotly.graph_objects as go

# ============== CONFIG PAGE ==============
st.set_page_config(
    page_title="🤖 ARIA - AI Strategic Intelligence Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============== CSS ULTRA FUTURISTE ==============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    .main {
        background: linear-gradient(135deg, #070B1A 0%, #0E0C2B 25%, #261B5E 50%, #0E0C2B 75%, #070B1A 100%);
        background-size: 400% 400%;
        animation: gradientShift 16s ease infinite;
        color: white; font-family: 'Inter', sans-serif; min-height: 100vh; overflow-x: hidden;
    }
    .stApp > div > div { position: relative; z-index: 2; }

    .main::before, .main::after { content:""; position: fixed; inset:0; pointer-events:none; }
    .main::before {
        background-image:
          radial-gradient(circle at 20% 50%, rgba(59,130,246,0.12) 0%, transparent 50%),
          radial-gradient(circle at 80% 20%, rgba(168,85,247,0.12) 0%, transparent 50%),
          radial-gradient(circle at 40% 80%, rgba(34,197,94,0.08) 0%, transparent 50%);
        animation: floatingOrbs 20s ease-in-out infinite;
        z-index:1;
    }
    .main::after {
        background: url('data:image/svg+xml,<svg width="40" height="40" xmlns="http://www.w3.org/2000/svg"><g fill="%233b82f6" fill-opacity="0.08"><circle cx="5" cy="5" r="1"/><circle cx="20" cy="5" r="1"/><circle cx="35" cy="5" r="1"/><circle cx="5" cy="20" r="1"/><circle cx="20" cy="20" r="1"/><circle cx="35" cy="20" r="1"/><circle cx="5" cy="35" r="1"/><circle cx="20" cy="35" r="1"/><circle cx="35" cy="35" r="1"/></g></svg>');
        opacity:.28; animation: gridMove 24s linear infinite; z-index:1;
    }

    @keyframes gradientShift { 0%,100%{background-position:0% 50%} 50%{background-position:100% 50%} }
    @keyframes floatingOrbs { 0%,100%{transform:translate(0,0) scale(1)} 33%{transform:translate(30px,-24px) scale(1.15)} 66%{transform:translate(-22px,18px) scale(.92)} }
    @keyframes gridMove { 0%{transform:translate(0,0)} 100%{transform:translate(40px,40px)} }

    .premium-header {
        background: rgba(15,23,42,0.85);
        border: 2px solid rgba(59,130,246,0.35);
        border-radius: 24px; padding: 28px; margin-bottom: 24px; position:relative;
        backdrop-filter: blur(20px);
        box-shadow: 0 20px 40px rgba(0,0,0,.35), 0 0 60px rgba(59,130,246,.08);
        overflow: hidden;
    }
    .premium-header::before {
        content:""; position:absolute; left:0; right:0; top:0; height:2px;
        background: linear-gradient(90deg, transparent, #3b82f6, #a855f7, transparent);
        animation: shimmer 3.2s ease-in-out infinite;
    }
    @keyframes shimmer { 0%,100%{opacity:.3} 50%{opacity:1} }

    .title-gradient { 
        background: linear-gradient(135deg, #60A5FA 0%, #A78BFA 50%, #22D3EE 100%);
        -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;
        font-size: 3.2rem; font-weight: 800; line-height: 1.05; margin:0;
        text-shadow: 0 0 30px rgba(96,165,250,.25);
    }
    .subtitle-glow { color:#cbd5e1; font-size:1.15rem; margin:8px 0 0 0; }

    .premium-card {
        background: rgba(15,23,42,0.78);
        border: 2px solid rgba(59,130,246,0.22);
        border-radius: 20px; padding: 24px; margin: 16px 0; position: relative;
        backdrop-filter: blur(18px);
        box-shadow: 0 18px 48px rgba(0,0,0,.45), 0 0 40px rgba(59,130,246,.05);
        transition: transform .28s ease, border-color .28s ease;
    }
    .premium-card:hover { transform: translateY(-4px); border-color: rgba(59,130,246,0.4); }

    .agent-avatar{
        width:120px;height:120px;border-radius:50%;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6, #06b6d4);
        display:flex;align-items:center;justify-content:center;margin: 0 auto 10px; position:relative;
        box-shadow: 0 20px 40px rgba(59,130,246,.5); border:3px solid rgba(255,255,255,.18);
    }
    .agent-avatar.active { animation: agentPulse 2.2s ease-in-out infinite; }
    @keyframes agentPulse { 0%,100%{transform:scale(1)} 50%{transform:scale(1.06)} }

    .status-dot{ width:22px;height:22px;border-radius:50%; position:absolute; bottom:8px; right: calc(50% - 11px);
        border:3px solid rgba(15,23,42,.9); box-shadow: 0 0 16px currentColor; }
    .status-dot.idle{ background:#64748b; color:#64748b; }
    .status-dot.thinking{ background:#f59e0b; color:#f59e0b; animation: blink 1.3s ease-in-out infinite; }
    .status-dot.analyzing{ background:#3b82f6; color:#3b82f6; animation: blink 1s ease-in-out infinite; }
    .status-dot.completed{ background:#22c55e; color:#22c55e; }
    @keyframes blink{ 0%,100%{opacity:1; transform:scale(1)} 50%{opacity:.75; transform:scale(1.12)} }

    .thought-bubble {
        background: rgba(59,130,246,0.15);
        border: 2px solid rgba(59,130,246,0.3);
        border-left: 5px solid #3b82f6; border-radius: 16px; padding: 18px; margin: 14px 0;
        backdrop-filter: blur(10px); box-shadow: 0 10px 26px rgba(59,130,246,.1);
        animation: slideIn .55s cubic-bezier(.175,.885,.32,1.275);
    }
    @keyframes slideIn { 0%{opacity:0; transform: translateX(-24px);} 100%{opacity:1; transform: translateX(0);} }

    .metric-premium{
        background: rgba(15, 23, 42, 0.85);
        border: 2px solid rgba(59,130,246,0.22);
        border-radius: 16px; padding: 18px; margin: 8px 0; text-align:center;
    }

    .progress-premium{ background: rgba(15,23,42,.86); border:2px solid rgba(59,130,246,.24);
        border-radius:18px; padding:6px; margin:16px 0; }
    .progress-fill{ height:14px; border-radius:12px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #06b6d4);
        box-shadow: 0 0 24px rgba(59,130,246,.65); transition: width .45s ease; }

    .insight-card{ background: rgba(15,23,42,.9); border-radius: 18px; padding: 18px; margin: 12px 0; }
    .insight-card.opportunity{ border:2px solid rgba(34,197,94,.4); box-shadow:0 8px 28px rgba(34,197,94,.15); }
    .insight-card.threat{ border:2px solid rgba(239,68,68,.4); box-shadow:0 8px 28px rgba(239,68,68,.15); }
    .insight-card.trend{ border:2px solid rgba(168,85,247,.4); box-shadow:0 8px 28px rgba(168,85,247,.15); }

    .footer-premium{
        background: rgba(15,23,42,.95); border-top: 2px solid rgba(59,130,246,.22);
        padding: 28px 0; margin-top: 36px; text-align:center; position:relative;
    }
    .footer-premium::before{ content:""; position:absolute; top:0; left:0; right:0; height:2px;
        background: linear-gradient(90deg, transparent, #3b82f6, #8b5cf6, transparent);
        animation: shimmer 4s ease-in-out infinite;
    }

    .stSelectbox > div > div {
        background: rgba(15,23,42,.94) !important; border: 2px solid rgba(59,130,246,.5) !important;
        border-radius: 12px !important; color: #e2e8f0 !important; font-weight: 500 !important;
    }
    .stButton > button{
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #06b6d4 100%) !important;
        border:none !important; border-radius:16px !important; color:white !important; font-weight:700 !important;
        padding: 12px 22px !important; box-shadow:0 12px 32px rgba(59,130,246,.42) !important; transition: all .25s ease !important;
    }
    .stButton > button:hover{ transform: translateY(-2px) scale(1.015) !important; }
</style>
""", unsafe_allow_html=True)

# ============== DATA MODELS ==============
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
    category: str  # "opportunity" | "threat" | "trend"

# ============== AGENT CORE ==============
class ARIAAgent:
    def __init__(self, language: str = "fr"):
        self.language = language
        self.status = "idle"  # idle | thinking | analyzing | completed
        self.thoughts: List[AgentThought] = []
        self.current_analysis: Optional[Dict] = None
        self.confidence_level: float = 0.0
        self.neural_activity: int = 0
        self.analysis_progress: float = 0.0

        self.translations = {
            "fr": {
                "agent_name": "ARIA",
                "agent_desc": "Agent de Recherche & d'Intelligence Autonome",
                "status_idle": "🤖 Agent en veille - Prêt à analyser",
                "status_thinking": "🧠 Réflexion stratégique en cours...",
                "status_analyzing": "⚡ Analyse multi-dimensionnelle active",
                "status_completed": "✨ Mission accomplie - Insights générés",
                "sectors": {
                    "FinTech": "Technologies Financières",
                    "AI": "Intelligence Artificielle",
                    "SaaS": "Logiciels en Service",
                    "E-commerce": "Commerce Électronique",
                },
                "thoughts": [
                    "🔍 Initialisation des capteurs de marché...",
                    "🧠 Activation des réseaux neuronaux sectoriels...",
                    "📊 Ingestion de 1 247 sources en temps réel...",
                    "⚡ Traitement par modèles de deep learning...",
                    "🎯 Corrélation des signaux faibles détectés...",
                    "📈 Modélisation prédictive des tendances...",
                    "🔬 Analyse concurrentielle multi-axes...",
                    "🤖 Génération d'insights actionnables...",
                    "✨ Synthèse stratégique avec confiance élevée.",
                ],
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
                    "AI": "Artificial Intelligence",
                    "SaaS": "Software as a Service",
                    "E-commerce": "E-commerce",
                },
                "thoughts": [
                    "🔍 Initializing advanced market sensors...",
                    "🧠 Activating sector neural networks...",
                    "📊 Ingesting 1,247 real-time sources...",
                    "⚡ Processing via deep learning models...",
                    "🎯 Correlating detected weak signals...",
                    "📈 Predictive modeling of trends...",
                    "🔬 Competitive analysis on multiple axes...",
                    "🤖 Generating actionable insights...",
                    "✨ Strategic synthesis with high confidence.",
                ],
            },
        }

        # Données d'exemple (2 secteurs bien remplis)
        self.market_data = {
            "FinTech": {
                "fr": {
                    "summary": (
                        "La FinTech se transforme via les agents IA conversationnels, "
                        "l’automatisation du risque, et l’intégration blockchain. Le cadre MiCA "
                        "renforce la confiance et favorise les acteurs conformes."
                    ),
                    "insights": [
                        MarketInsight("IA Conversationnelle Bancaire",
                                      "Assistants IA pour KYC, support client et scoring temps réel.",
                                      9.5, 91, "opportunity"),
                        MarketInsight("DeFi Institutionnelle",
                                      "Accès institutionnel aux produits tokenisés et paiements programmables.",
                                      8.8, 87, "opportunity"),
                        MarketInsight("Super-Apps",
                                      "Vers des plateformes financières unifiées (paiement, crédit, épargne).",
                                      8.2, 79, "trend"),
                        MarketInsight("Durcissement Réglementaire",
                                      "MiCA/AML créent des barrières mais aussi un avantage compétitif aux conformes.",
                                      7.9, 94, "threat"),
                    ],
                    "recommendations": [
                        "Investir dans l’IA conversationnelle avant T2 2025",
                        "Anticiper la conformité MiCA 6–9 mois à l’avance",
                        "Acquérir des talents blockchain avant la pénurie",
                        "Concevoir une feuille de route Super-App progressive",
                    ],
                },
                "en": {
                    "summary": (
                        "FinTech is reshaped by conversational AI agents, risk automation, and "
                        "blockchain integration. MiCA provides trust and advantages for compliant players."
                    ),
                    "insights": [
                        MarketInsight("Conversational Banking AI",
                                      "AI assistants for KYC, customer support, and real-time scoring.",
                                      9.5, 91, "opportunity"),
                        MarketInsight("Institutional DeFi",
                                      "Institutional access to tokenized products and programmable payments.",
                                      8.8, 87, "opportunity"),
                        MarketInsight("Super-Apps",
                                      "Consolidated financial platforms (payments, credit, savings).",
                                      8.2, 79, "trend"),
                        MarketInsight("Regulatory Tightening",
                                      "MiCA/AML create barriers but reward compliance.",
                                      7.9, 94, "threat"),
                    ],
                    "recommendations": [
                        "Invest in conversational AI before Q2 2025",
                        "Prepare MiCA compliance 6–9 months ahead",
                        "Acquire blockchain talent before shortage",
                        "Design a phased Super-App roadmap",
                    ],
                },
            },
            "AI": {
                "fr": {
                    "summary": (
                        "L’IA connaît une croissance explosive portée par les agents autonomes, "
                        "l’edge computing et l’intégration enterprise. Marché UE visé ~47 Md€ d’ici 2027."
                    ),
                    "insights": [
                        MarketInsight("Agents IA Autonomes",
                                      "Automatisation multi-process, copilotes métiers et orchestration d’outils.",
                                      9.8, 96, "opportunity"),
                        MarketInsight("IA Enterprise",
                                      "ROI moyen 18 mois sur data quality, décision et productivité.",
                                      9.4, 89, "opportunity"),
                        MarketInsight("Edge AI Computing",
                                      "Traitement proche de la source: latence, coûts et privacy optimisés.",
                                      8.7, 83, "trend"),
                        MarketInsight("Pénurie de Talents",
                                      "Demande senior +423% et salaires en forte hausse.",
                                      9.2, 94, "threat"),
                    ],
                    "recommendations": [
                        "Capitaliser sur la vague d’agents IA sectoriels",
                        "Investir dans l’Edge AI pour anticiper la décentralisation",
                        "Bâtir une expertise AI Act & gouvernance",
                        "Acquérir des équipes IA avant l’explosion des coûts",
                    ],
                },
                "en": {
                    "summary": (
                        "AI is booming via autonomous agents, edge computing, and enterprise integration. "
                        "EU market ≈ $52B by 2027."
                    ),
                    "insights": [
                        MarketInsight("Autonomous AI Agents",
                                      "Multi-process automation, domain copilots, tool orchestration.",
                                      9.8, 96, "opportunity"),
                        MarketInsight("Enterprise AI",
                                      "18-month average ROI across data quality, decisioning, productivity.",
                                      9.4, 89, "opportunity"),
                        MarketInsight("Edge AI Computing",
                                      "Near-source processing: latency, cost, and privacy gains.",
                                      8.7, 83, "trend"),
                        MarketInsight("Talent Shortage",
                                      "Senior demand +423% and rising compensation.",
                                      9.2, 94, "threat"),
                    ],
                    "recommendations": [
                        "Invest in edge AI for decentralization",
                        "Build AI Act compliance expertise",
                        "Acquire AI teams before cost explosion",
                        "Launch sector-specific autonomous agents",
                    ],
                },
            },
        }

    def get_translation(self, key: str) -> str:
        return self.translations.get(self.language, {}).get(key, key)

    async def activate(self, sector: str) -> None:
        self.status = "thinking"
        self.thoughts = []
        self.analysis_progress = 0.0
        self.neural_activity = random.randint(820, 1220)

        thoughts = self.translations[self.language]["thoughts"]

        for i, text in enumerate(thoughts):
            await asyncio.sleep(random.uniform(0.55, 1.2))
            self.thoughts.append(
                AgentThought(
                    content=text,
                    timestamp=datetime.now(),
                    confidence=random.uniform(0.86, 0.97),
                )
            )
            self.analysis_progress = ((i + 1) / len(thoughts)) * 100
            if i == 3:
                self.status = "analyzing"
            if i == len(thoughts) - 1:
                self.status = "completed"
                self.current_analysis = self.market_data.get(sector, {}).get(self.language, {})
                self.confidence_level = float(random.uniform(88.0, 97.0))
            self.neural_activity += random.randint(-45, 85)

    def gauge(self) -> go.Figure:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=max(0.0, float(self.confidence_level)),
            title={'text': "Confidence Level", 'font': {'size': 20, 'color': '#e2e8f0'}},
            number={'font': {'size': 36, 'color': '#60a5fa'}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': '#94a3b8'},
                'bar': {'color': "#3b82f6", 'thickness': 0.82},
                'steps': [
                    {'range': [0, 60], 'color': "rgba(239, 68, 68, 0.30)"},
                    {'range': [60, 85], 'color': "rgba(245, 158, 11, 0.30)"},
                    {'range': [85, 100], 'color': "rgba(34, 197, 94, 0.30)"},
                ],
                'threshold': {
                    'line': {'color': "#a855f7", 'width': 6},
                    'thickness': 0.85,
                    'value': 90
                }
            }
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "#e2e8f0"}, height=340, margin=dict(l=20, r=20, t=60, b=10)
        )
        return fig

# ============== APP LOGIC ==============
def main():
    # State init
    if "agent" not in st.session_state:
        st.session_state.agent = ARIAAgent(language="fr")
    if "language" not in st.session_state:
        st.session_state.language = "fr"

    agent: ARIAAgent = st.session_state.agent
    agent.language = st.session_state.language

    # HEADER
    st.markdown(f"""
    <div class='premium-header'>
        <div style='display:flex;gap:24px;align-items:flex-start;justify-content:space-between;'>
            <div style='flex:1;'>
                <h1 class='title-gradient'>🧠 {agent.get_translation('agent_name')}</h1>
                <p class='subtitle-glow'>{agent.get_translation('agent_desc')}</p>
                <div style='display:flex;gap:18px;margin-top:14px;font-size:.95rem;color:#60a5fa;'>
                    <span>🧠 Neural Activity: {agent.neural_activity}</span>
                    <span>📚 Sources: 1,247</span>
                    <span>⚡ Real-time Analysis</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Language & Sector
    col_lang, col_spacer, col_sector = st.columns([1, .2, 2])
    with col_lang:
        lang = st.selectbox("🌐 Language / Langue", ["🇫🇷 Français", "🇺🇸 English"])
        new_language = "fr" if "Français" in lang else "en"
        if new_language != st.session_state.language:
            st.session_state.language = new_language
            st.rerun()

    sectors = agent.translations[agent.language]["sectors"]
    with col_sector:
        selected_sector = st.selectbox(
            "🎯 Sector",
            list(sectors.keys()),
            format_func=lambda k: sectors[k],
        )

    # LAYOUT
    left, right = st.columns([1, 2])

    # LEFT – Control Panel & Metrics
    with left:
        st.markdown("""
        <div class='premium-card' style='text-align:center;'>
            <div class='agent-avatar {active}'><span style='font-size:2.4rem;'>🤖</span></div>
            <div class='status-dot {status}'></div>
            <h4 style='margin:6px 0 2px 0;'>ARIA</h4>
            <p style='color:#94a3b8;margin:0;'>Autonomous Intelligence System</p>
        </div>
        """.format(active=("active" if agent.status != "idle" else ""), status=agent.status), unsafe_allow_html=True)

        # Status text
        st.markdown(f"""
        <div class='premium-card' style='text-align:center; padding:16px;'>
            <p style='margin:0; font-weight:600; color:#e2e8f0;'>{agent.get_translation(f"status_{agent.status}")}</p>
        </div>
        """, unsafe_allow_html=True)

        # Progress
        if agent.status != "idle":
            st.markdown(f"""
            <div class='progress-premium'>
                <div class='progress-fill' style='width:{agent.analysis_progress:.1f}%'></div>
            </div>
            <p style='text-align:center; color:#cbd5e1; font-size:.92rem;'>
                Analysis Progress: {agent.analysis_progress:.1f}%
            </p>
            """, unsafe_allow_html=True)

        # Buttons
        c1, c2 = st.columns(2)
        with c1:
            if agent.status in ("idle", "completed"):
                if st.button("🚀 Activate ARIA Agent"):
                    with st.spinner("🤖 Initializing autonomous analysis..."):
                        asyncio.run(agent.activate(selected_sector))
                        st.rerun()
            else:
                if st.button("⏹️ Stop Agent"):
                    agent.status = "idle"
                    agent.thoughts = []
                    agent.current_analysis = None
                    agent.analysis_progress = 0.0
                    agent.confidence_level = 0.0
                    st.rerun()
        with c2:
            if st.button("🔄 Reset"):
                agent.status = "idle"
                agent.thoughts = []
                agent.current_analysis = None
                agent.analysis_progress = 0.0
                agent.confidence_level = 0.0
                st.rerun()

        # Live Metrics
        if agent.status != "idle":
            st.markdown("<h4 style='margin:12px 0;'>📊 Real-time Metrics</h4>", unsafe_allow_html=True)
            metrics = [
                ("Neural Activity", f"{agent.neural_activity}", "🧠"),
                ("Data Sources", "1,247", "📚"),
                ("Insights Generated", f"{len([t for t in agent.thoughts if t.confidence>0.85])}", "💡"),
                ("Confidence Level", f"{agent.confidence_level:.1f}%" if agent.confidence_level > 0 else "N/A", "⚡"),
            ]
            for label, value, icon in metrics:
                st.markdown(f"""
                <div class='metric-premium'>
                    <div style='display:flex;justify-content:space-between;align-items:center;'>
                        <span style='color:#94a3b8;font-size:.9rem;'>{label}</span>
                        <span style='font-size:1.2rem'>{icon}</span>
                    </div>
                    <p style='margin:6px 0 0 0; font-size:1.35rem; font-weight:800;'>{value}</p>
                </div>
                """, unsafe_allow_html=True)

    # RIGHT – Thoughts, Results
    with right:
        # Thought process
        if agent.status != "idle" and agent.thoughts:
            st.markdown("""
            <div class='premium-card'>
                <h3 style='margin:0 0 12px 0; display:flex; align-items:center; gap:10px;'>
                    🧠 Agent Thought Process
                    <span style='margin-left:auto; display:flex; gap:6px;'>
                        <i style='width:8px;height:8px;border-radius:50%;background:#22c55e;animation: blink 1s infinite;'></i>
                        <i style='width:8px;height:8px;border-radius:50%;background:#3b82f6;animation: blink 1.2s infinite;'></i>
                        <i style='width:8px;height:8px;border-radius:50%;background:#a855f7;animation: blink 1.4s infinite;'></i>
                    </span>
                </h3>
            </div>
            """, unsafe_allow_html=True)

            for i, t in enumerate(agent.thoughts):
                st.markdown(f"""
                <div class='thought-bubble' style='animation-delay:{i*0.08}s'>
                    <div style='display:flex; gap:12px; align-items:flex-start;'>
                        <div style='background:linear-gradient(135deg,#3b82f6,#8b5cf6);border-radius:50%;width:38px;height:38px;display:flex;align-items:center;justify-content:center;flex-shrink:0;'>
                            🤖
                        </div>
                        <div style='flex:1;'>
                            <p style='margin:0 0 8px 0;'>{t.content}</p>
                            <div style='display:flex;justify-content:space-between;color:#94a3b8;font-size:.85rem;'>
                                <span>{t.timestamp.strftime("%H:%M:%S")}</span>
                                <span style='color:#22c55e;background:rgba(34,197,94,.15);padding:2px 8px;border-radius:10px;'>
                                    {t.confidence:.1%} confidence
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Results
        if agent.current_analysis and agent.status == "completed":
            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
            # Executive Summary
            st.markdown(f"""
            <div class='premium-card'>
              <h3 style='margin:0 0 14px 0; display:flex; align-items:center; gap:10px;'>
                📋 Executive Summary
                <span style='margin-left:auto;background:rgba(34,197,94,.16);color:#22c55e;padding:4px 10px;border-radius:16px;font-size:.8rem;'>High Confidence</span>
              </h3>
              <div style='background:linear-gradient(135deg,rgba(59,130,246,.19),rgba(168,85,247,.18)); border:1px solid rgba(59,130,246,.35); border-left:5px solid #3b82f6; border-radius:14px; padding:18px;'>
                <p style='margin:0; line-height:1.6;'>{agent.current_analysis.get("summary","")}</p>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # Confidence Gauge
            st.markdown("<div class='premium-card'><h3 style='text-align:center;margin:0 0 10px 0;'>📊 Analysis Confidence</h3></div>", unsafe_allow_html=True)
            st.plotly_chart(agent.gauge(), use_container_width=True)

            # Insights
            insights: List[MarketInsight] = agent.current_analysis.get("insights") or []
            if insights:
                st.markdown("<div class='premium-card'><h3 style='margin:0 0 12px 0;'>🎯 Strategic Insights</h3></div>", unsafe_allow_html=True)
                categories = {
                    "opportunity": [i for i in insights if i.category == "opportunity"],
                    "threat": [i for i in insights if i.category == "threat"],
                    "trend": [i for i in insights if i.category == "trend"],
                }
                if categories["opportunity"]:
                    st.markdown("<h4 style='color:#22c55e; margin:10px 0;'>💡 Market Opportunities</h4>", unsafe_allow_html=True)
                    for opp in categories["opportunity"]:
                        st.markdown(f"""
                        <div class='insight-card opportunity'>
                            <h5 style='margin:0 0 8px 0;'>{opp.title}</h5>
                            <p style='margin:0 0 10px 0; color:#cbd5e1;'>{opp.description}</p>
                            <div style='display:flex;justify-content:space-between;'>
                                <div style='color:#94a3b8; font-size:.9rem;'>
                                    Impact: <b style='color:#22c55e;'>{opp.impact_score}/10</b> &nbsp;|&nbsp;
                                    Confidence: <b style='color:#22c55e;'>{opp.confidence}%</b>
                                </div>
                                <span style='background:rgba(34,197,94,.16);color:#22c55e;padding:3px 10px;border-radius:14px;font-size:.8rem;'>High Priority</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                if categories["threat"]:
                    st.markdown("<h4 style='color:#ef4444; margin:10px 0;'>⚠️ Strategic Threats</h4>", unsafe_allow_html=True)
                    for th in categories["threat"]:
                        st.markdown(f"""
                        <div class='insight-card threat'>
                            <h5 style='margin:0 0 8px 0;'>{th.title}</h5>
                            <p style='margin:0 0 10px 0; color:#cbd5e1;'>{th.description}</p>
                            <div style='display:flex;justify-content:space-between;'>
                                <div style='color:#94a3b8; font-size:.9rem;'>
                                    Impact: <b style='color:#ef4444;'>{th.impact_score}/10</b> &nbsp;|&nbsp;
                                    Confidence: <b style='color:#ef4444;'>{th.confidence}%</b>
                                </div>
                                <span style='background:rgba(239,68,68,.16);color:#ef4444;padding:3px 10px;border-radius:14px;font-size:.8rem;'>Monitor</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                if categories["trend"]:
                    st.markdown("<h4 style='color:#a855f7; margin:10px 0;'>📈 Emerging Trends</h4>", unsafe_allow_html=True)
                    for tr in categories["trend"]:
                        st.markdown(f"""
                        <div class='insight-card trend'>
                            <h5 style='margin:0 0 8px 0;'>{tr.title}</h5>
                            <p style='margin:0 0 10px 0; color:#cbd5e1;'>{tr.description}</p>
                            <div style='display:flex;justify-content:space-between;'>
                                <div style='color:#94a3b8; font-size:.9rem;'>
                                    Impact: <b style='color:#a855f7;'>{tr.impact_score}/10</b> &nbsp;|&nbsp;
                                    Confidence: <b style='color:#a855f7;'>{tr.confidence}%</b>
                                </div>
                                <span style='background:rgba(168,85,247,.16);color:#a855f7;padding:3px 10px;border-radius:14px;font-size:.8rem;'>Track</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

            # Recommendations
            recos: List[str] = agent.current_analysis.get("recommendations") or []
            if recos:
                st.markdown("""
                <div class='premium-card'>
                    <h3 style='margin:0 0 12px 0; display:flex; align-items:center; gap:10px;'>
                        🧭 AI Strategic Recommendations
                        <span style='margin-left:auto;background:rgba(168,85,247,.16);color:#a78bfa;padding:4px 10px;border-radius:16px;font-size:.8rem;'>Actionable</span>
                    </h3>
                </div>
                """, unsafe_allow_html=True)
                for i, rec in enumerate(recos, 1):
                    st.markdown(f"""
                    <div style='display:flex; gap:14px; background:rgba(168,85,247,.14); border:1px solid rgba(168,85,247,.28); border-radius:16px; padding:16px; margin:10px 0;'>
                        <div style='background:linear-gradient(135deg,#3b82f6,#8b5cf6); width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;'>
                            <b>{i}</b>
                        </div>
                        <div style='flex:1;'>
                            <p style='margin:0;'>{rec}</p>
                            <div style='margin-top:8px; display:flex; gap:8px;'>
                                <span style='background:rgba(34,197,94,.16);color:#22c55e;padding:2px 8px;border-radius:12px;font-size:.75rem;'>High Impact</span>
                                <span style='background:rgba(59,130,246,.16);color:#60a5fa;padding:2px 8px;border-radius:12px;font-size:.75rem;'>Strategic</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # Export / Actions
            st.markdown("<div class='premium-card'><h3 style='margin:0 0 12px 0;'>📤 Export & Actions</h3>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("📄 Export Report (.txt)"):
                    # Build report
                    insights = agent.current_analysis.get("insights") or []
                    report = [
                        "🤖 ARIA - STRATEGIC INTELLIGENCE REPORT",
                        "═══════════════════════════════════════════════",
                        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                        f"Sector: {selected_sector}",
                        f"Confidence Level: {agent.confidence_level:.1f}%",
                        f"Neural Activity: {agent.neural_activity} nodes",
                        "",
                        "EXECUTIVE SUMMARY:",
                        agent.current_analysis.get('summary', ''),
                        "",
                        "KEY STRATEGIC INSIGHTS:",
                        "═══════════════════════════════════════════════",
                    ]
                    for ins in insights:
                        report += [
                            f"\n🎯 {ins.title.upper()}",
                            f"   Category: {ins.category.title()}",
                            f"   Impact Score: {ins.impact_score}/10",
                            f"   Confidence: {ins.confidence}%",
                            f"   Description: {ins.description}",
                        ]
                    report += ["", "AI STRATEGIC RECOMMENDATIONS:", "═══════════════════════════════════════════════"]
                    for i, rec in enumerate(recos, 1):
                        report.append(f"{i}. {rec}")
                    report += [
                        "", "═══════════════════════════════════════════════",
                        f"Generated by ARIA • Confidence: {agent.confidence_level:.1f}% • Neural: {agent.neural_activity} nodes"
                    ]
                    st.download_button(
                        label="⬇️ Download Report",
                        data=("\n".join(report)).encode("utf-8"),
                        file_name=f"aria_report_{selected_sector}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain",
                    )
            with c2:
                if st.button("🔔 Setup Alerts"):
                    st.success("✅ Alerts configured! Real-time notifications enabled.")
            with c3:
                if st.button("🔄 Re-analyze"):
                    agent.status = "idle"
                    agent.thoughts = []
                    agent.current_analysis = None
                    agent.confidence_level = 0.0
                    agent.analysis_progress = 0.0
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        # IDLE state
        if agent.status == "idle":
            st.markdown("""
            <div class='premium-card' style='text-align:center; padding:48px 24px;'>
                <div style='font-size:4rem; margin-bottom:14px;'>🤖</div>
                <h3 style='margin:0 0 8px 0;'>ARIA Ready for Mission</h3>
                <p style='margin:0 0 16px 0; color:#cbd5e1;'>
                    Select a target sector and activate the autonomous intelligence agent to begin a comprehensive strategic market analysis.
                </p>
                <div style='background:rgba(59,130,246,.12); border:1px solid rgba(59,130,246,.28); border-radius:16px; padding:18px; margin-top:14px;'>
                    <b>Capabilities</b> — multi-source intelligence • predictive analytics • autonomous insights • exportable reports
                </div>
            </div>
            """, unsafe_allow_html=True)

    # FOOTER
    conf = f"{agent.confidence_level:.1f}%" if agent.confidence_level > 0 else "0.0%"
    st.markdown(f"""
    <div class='footer-premium'>
        <div style='max-width: 1200px; margin: 0 auto; padding: 0 16px; text-align:left;'>
            <div style='display:flex; justify-content:space-between; align-items:center; gap:20px; flex-wrap:wrap;'>
                <div style='display:flex; align-items:center; gap:14px;'>
                    <div style='width:40px;height:40px;border-radius:12px;background:linear-gradient(135deg,#3b82f6,#8b5cf6);display:flex;align-items:center;justify-content:center;'>🤖</div>
                    <div>
                        <div style='font-weight:700;'>ARIA — Autonomous Research & Intelligence Agent</div>
                        <div style='color:#94a3b8; font-size:.92rem;'>Advanced Neural Networks • Predictive Analytics • Real-time Intelligence</div>
                    </div>
                </div>
                <div style='text-align:right;'>
                    <div style='display:flex; gap:14px; flex-wrap:wrap; justify-content:flex-end; color:#cbd5e1;'>
                        <span>⚡ Confidence: {conf}</span>
                        <span>🧠 Neural Activity: {agent.neural_activity}</span>
                        <span>📚 Sources: 1,247</span>
                    </div>
                    <div style='color:#94a3b8; font-size:.9rem;'>
                        Last Analysis: {datetime.now().strftime('%H:%M:%S')} • Status: {"Active" if agent.status!="idle" else "Standby"} • Uptime: 99.97%
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
