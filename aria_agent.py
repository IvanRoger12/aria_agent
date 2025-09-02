import streamlit as st
import json
import random
from datetime import datetime
import asyncio
from dataclasses import dataclass

# Plotly (optionnel mais recommandé)
try:
    import plotly.graph_objects as go
    PLOTLY_OK = True
except Exception:
    go = None
    PLOTLY_OK = False

# =========================
# CONFIG DE PAGE
# =========================
st.set_page_config(
    page_title="🤖 ARIA - AI Strategic Intelligence Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CSS — THÈME BLEU + TEXTE BLANC (LUMINEUX)
# =========================
st.markdown("""
<style>
:root{
  --bg1:#0b1224; --bg2:#08101f; --card: rgba(10,17,33,.96);
  --white:#ffffff; --muted:#dfe7ff; --soft:#c7cdd8;
  --blue:#2f7df4; --violet:#7c58f4; --green:#10b981; --yellow:#ffd84d; --danger:#ef4444;
  --border: rgba(255,255,255,.18);
}

/* Fond global : dégradés bleus subtils + halo */
.main{
  background:
    radial-gradient(1200px 800px at 10% -10%, rgba(47,125,244,.15), transparent 50%),
    radial-gradient(1000px 700px at 90% 10%, rgba(124,88,244,.18), transparent 60%),
    linear-gradient(135deg, var(--bg1) 0%, var(--bg2) 100%);
  color: var(--white);
}

/* Cartes & blocs */
.analysis-card,.metric-card,.thought-bubble,.glass,.neon-card{
  background: var(--card);
  -webkit-backdrop-filter: blur(3px);
  backdrop-filter: blur(3px);
  border:1px solid var(--border);
  border-radius:18px; padding:20px;
  box-shadow: 0 16px 40px rgba(0,0,0,.45),
              0 0 24px rgba(47,125,244,.10);
}

/* Titres ultra lisibles (blanc gras) */
h1,h2,h3,h4,h5,h6{ color: var(--white) !important; font-weight: 800 !important; letter-spacing:.2px; }
.subtitle-white{ color:var(--white)!important; font-weight:800!important; letter-spacing:.3px; text-shadow:0 0 8px rgba(0,0,0,.55); }
.subtitle-yellow{ color:var(--yellow)!important; font-weight:800!important; letter-spacing:.3px; text-shadow:0 0 12px rgba(255,216,77,.85); }
.muted{ color:var(--muted)!important; }

/* Boutons */
.stButton > button{
  background:linear-gradient(135deg,var(--blue),var(--violet));
  color:#fff; border:0; border-radius:12px; font-weight:800;
  box-shadow:0 10px 25px rgba(47,125,244,.35), 0 0 16px rgba(124,88,244,.25);
  transition: transform .2s, box-shadow .2s, filter .2s;
}
.stButton > button:hover{
  transform: translateY(-2px);
  box-shadow:0 16px 35px rgba(124,88,244,.45), 0 0 24px rgba(47,125,244,.35);
  filter: brightness(1.05);
}

/* Selectbox (fond bleu sombre + texte blanc) */
.stSelectbox > div > div{
  background: rgba(255,255,255,.06)!important;
  color:#fff!important;
  border:1px solid rgba(255,255,255,.28)!important;
  border-radius:10px!important;
}

/* Pensées (slide-in) */
.thought-bubble{
  border-left:5px solid var(--blue);
  animation: slideIn .45s ease-out;
}
@keyframes slideIn{ from{opacity:0; transform:translateX(-18px);} to{opacity:1; transform:translateX(0);} }

/* Badge “Simulation Active” clignotant (jaune) */
.sim-badge{
  display:inline-flex; align-items:center; gap:.5rem;
  background: rgba(255,216,77,.12);
  border:1px solid rgba(255,216,77,.65); padding:.38rem .8rem; border-radius:999px;
  color:var(--yellow); font-weight:900; letter-spacing:.6px;
  text-shadow:0 0 12px rgba(255,216,77,1);
  box-shadow:0 0 22px rgba(255,216,77,.28), inset 0 0 10px rgba(255,216,77,.15);
  animation: neonBlink 1.15s ease-in-out infinite;
}
.sim-dot{ width:10px; height:10px; border-radius:50%; background:var(--yellow); box-shadow:0 0 10px var(--yellow), 0 0 20px var(--yellow); }
@keyframes neonBlink{ 0%,100%{ filter:drop-shadow(0 0 10px rgba(255,216,77,1)); opacity:1;} 50%{ filter:drop-shadow(0 0 2px rgba(255,216,77,.35)); opacity:.68;} }

/* Avatar agent (anneau bleu/violet, emoji centré) */
.agent-avatar{
  width:100px; height:100px; border-radius:50%; margin:0 auto; position:relative;
  background: conic-gradient(from 180deg, var(--blue), var(--violet), var(--blue));
  box-shadow:0 0 30px rgba(47,125,244,.6), inset 0 0 18px rgba(124,88,244,.35);
  animation: slowSpin 10s linear infinite;
}
.agent-avatar::after{
  content:'🤖'; position:absolute; inset:10px; display:flex; align-items:center; justify-content:center;
  background: radial-gradient(circle at 50% 40%, rgba(0,0,0,.0), rgba(0,0,0,.35) 68%);
  border-radius:50%; font-size:2rem; color:#fff; text-shadow:0 2px 8px rgba(0,0,0,.65);
}
@keyframes slowSpin{ from{transform:rotate(0);} to{transform:rotate(360deg);} }

/* Insights (contraste bleu) */
.ins-card{ border-radius:16px; padding:16px; margin:10px 0; }
.ins-opp{ background: rgba(16,185,129,.12); border-left:6px solid var(--green); }
.ins-thr{ background: rgba(239,68,68,.12); border-left:6px solid var(--danger); }
.ins-trd{ background: rgba(124,88,244,.12); border-left:6px solid var(--violet); }

/* Petits séparateurs */
.hr-lite{ height:1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,.25), transparent); margin:10px 0; }
</style>
""", unsafe_allow_html=True)

# =========================
# DATA MODELS
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
# AGENT (structure conservée)
# =========================
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
        for i, t in enumerate(thoughts):
            await asyncio.sleep(random.uniform(0.6, 1.1))
            self.thoughts.append(AgentThought(t, datetime.now(), "analysis", random.uniform(0.7, 0.95)))
            if i == 2:
                self.status = "analyzing"
            elif i == len(thoughts) - 1:
                self.status = "completed"
                self.current_analysis = self.market_data.get(sector, {}).get(self.language, {})
                self.confidence_level = random.uniform(85, 95)
            self.neural_activity += random.randint(-30, 50)

    # --- Plotly Gauges (protégé) ---
    def generate_confidence_gauge(self):
        if not PLOTLY_OK:
            return None
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=self.confidence_level,
            domain={'x':[0,1],'y':[0,1]},
            title={'text':"Confidence Level", 'font':{'color':'#ffffff'}},
            delta={'reference':80, 'increasing':{'color':'#2f7df4'}},
            gauge={
                'axis':{'range':[None,100], 'tickcolor':'#cfe1ff'},
                'bar':{'color':"#2f7df4"},
                'steps':[{'range':[0,50],'color':"#2b2f45"},
                         {'range':[50,80],'color':"#1b2b4f"},
                         {'range':[80,100],'color':"#153a6b"}],
                'threshold':{'line':{'color':"#ffd84d",'width':4},'thickness':0.75,'value':90}
            }
        ))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font={'color':"#ffffff",'family':"Inter, Arial"}, height=320)
        return fig

    def generate_neural_network_viz(self):
        if not PLOTLY_OK:
            return None
        n_nodes = 20
        x = [random.uniform(0, 10) for _ in range(n_nodes)]
        y = [random.uniform(0, 10) for _ in range(n_nodes)]
        edge_x, edge_y = [], []
        for i in range(n_nodes):
            for j in range(i+1, min(i+4, n_nodes)):
                if random.random() > 0.6:
                    edge_x.extend([x[i], x[j], None])
                    edge_y.extend([y[i], y[j], None])
        edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.8, color='rgba(47,125,244,.75)'),
                                hoverinfo='none', mode='lines', opacity=0.85)
        node_trace = go.Scatter(x=x, y=y, mode='markers', hoverinfo='text',
                                marker=dict(size=8, color='#7c58f4', line=dict(width=2, color='#2f7df4')))
        fig = go.Figure(data=[edge_trace, node_trace])
        fig.update_layout(showlegend=False, hovermode='closest',
                          margin=dict(b=20,l=5,r=5,t=30),
                          xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                          yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        return fig

# =========================
# UI (structure identique)
# =========================
def main():
    if 'agent' not in st.session_state:
        st.session_state.agent = ARIAAgent()
    if 'language' not in st.session_state:
        st.session_state.language = 'fr'

    agent: ARIAAgent = st.session_state.agent
    agent.language = st.session_state.language

    # ----- HEADER (blanc, lisible)
    hcol1, _, hcol3 = st.columns([6,1,1])
    with hcol1:
        st.markdown(f"""
        <div class="glass" style="padding:18px; margin-bottom:16px;">
            <h1 class="subtitle-white" style="margin:0; font-size:2.4rem;">🧠 {agent.get_translation('agent_name')}</h1>
            <p class="muted" style="margin:.25rem 0 0 0;">{agent.get_translation('agent_desc')}</p>
            <div class="hr-lite"></div>
        </div>
        """, unsafe_allow_html=True)
    with hcol3:
        lang = st.selectbox("🌐", ["🇫🇷 FR", "🇺🇸 EN"], key="lang_select")
        new_lang = "fr" if "FR" in lang else "en"
        if new_lang != st.session_state.language:
            st.session_state.language = new_lang
            st.rerun()

    left, right = st.columns([1,2])

    # ----- LEFT PANEL (identique)
    with left:
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="subtitle-white" style="text-align:center;margin-bottom:12px;">🤖 Agent Control Panel</h3>', unsafe_allow_html=True)

        status_color = {
            "idle": "#6b7280", "thinking": "#f59e0b", "analyzing": "#2f7df4", "completed": "#10b981"
        }.get(agent.status, "#6b7280")

        st.markdown(f"""
        <div style='text-align:center; margin:8px 0 14px 0;'>
            <div class="agent-avatar"></div>
            <div style="margin-top:10px; display:flex; align-items:center; gap:10px; justify-content:center;">
                <span style="width:14px;height:14px;border-radius:50%;border:2px solid rgba(255,255,255,.9);background:{status_color}; box-shadow:0 0 12px {status_color};"></span>
                <span class="sim-badge"><span class="sim-dot"></span> SIMULATION AGENT IA</span>
            </div>
            <p class="muted" style='margin:.55rem 0 0 0;'>Neural Activity: {agent.neural_activity}</p>
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
            if st.button("🚀 Activate ARIA Agent", key="activate_btn", use_container_width=True):
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

    # ----- RIGHT PANEL (identique)
    with right:
        # Pensées
        if agent.status != "idle" and agent.thoughts:
            st.markdown('<div class="analysis-card"><h3 class="subtitle-yellow" style="margin-bottom:10px;">🧠 Agent Thought Process</h3></div>', unsafe_allow_html=True)
            for th in agent.thoughts:
                st.markdown(f"""
                <div class="thought-bubble">
                    <div style='display:flex; align-items:flex-start; gap:12px;'>
                        <div style='background:linear-gradient(135deg, var(--blue), var(--violet)); width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;'>🤖</div>
                        <div>
                            <p class="subtitle-white" style='margin:0; font-size:.98rem;'>{th.content}</p>
                            <p class='muted' style='margin:4px 0 0 0; font-size:.78rem;'>{th.timestamp.strftime("%H:%M:%S")} • {th.confidence:.0%} conf.</p>
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
                <div style='background:linear-gradient(135deg, rgba(47,125,244,.18), rgba(124,88,244,.18)); border-left: 6px solid var(--blue); border-radius:12px; padding:16px;'>
                    <p style='color:var(--muted); margin:0; line-height:1.6; font-size:1rem;'>{agent.current_analysis.get("summary","")}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Confidence gauge (protégé)
            if agent.confidence_level > 0:
                st.markdown('<div class="analysis-card"><h3 class="subtitle-yellow" style="margin-bottom:10px;">📊 Confidence Analysis</h3></div>', unsafe_allow_html=True)
                if PLOTLY_OK:
                    fig = agent.generate_confidence_gauge()
                    if fig is not None:
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Confidence chart unavailable (figure not created).")
                else:
                    st.info("Plotly non installé — jauge désactivée. Ajoute `plotly` dans requirements.txt.")

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
                for idx, rec in enumerate(recs, 1):
                    st.markdown(f"""
                    <div class="neon-card" style="background:rgba(124,88,244,.12); border-radius:14px; padding:14px; margin:10px 0;">
                        <div style="display:flex; gap:12px; align-items:flex-start;">
                            <div style="width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg, var(--blue), var(--violet)); display:flex;align-items:center;justify-content:center;color:white;font-weight:900;">{idx}</div>
                            <p class="subtitle-white" style="margin:0; line-height:1.55;">{rec}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        # Écran d’attente
        elif agent.status == "idle":
            st.markdown("""
            <div class='analysis-card' style='text-align:center; padding:46px 26px;'>
                <div style='font-size:4rem;margin-bottom:18px;'>🤖</div>
                <h3 class='subtitle-white' style='margin-bottom:10px;'>ARIA Ready for Mission</h3>
                <p class='muted' style='margin-bottom:22px;'>Select a target sector and activate the agent to begin strategic market analysis.</p>
                <div style='background: rgba(47,125,244,.12); border:1px solid rgba(47,125,244,.35); border-radius:12px; padding:18px;'>
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

    # ----- Sidebar Neural Viz (protégée)
    if agent.status in ["thinking", "analyzing"]:
        with st.sidebar:
            st.markdown('<h4 class="subtitle-white">🧠 Neural Network Activity</h4>', unsafe_allow_html=True)
            if PLOTLY_OK:
                try:
                    fig_nn = agent.generate_neural_network_viz()
                    if fig_nn is not None:
                        st.plotly_chart(fig_nn, use_container_width=True)
                    else:
                        st.info("Neural graph unavailable (figure not created).")
                except Exception:
                    st.info("Le graphe neural a été désactivé suite à une erreur.")
            else:
                st.info("Plotly non installé — neural graph désactivé.\nAjoute `plotly` dans requirements.txt.")

    # ----- Footer
    st.markdown(f"""
    <div style='margin-top:26px; padding:16px 0; text-align:center; opacity:.9;'>
        <p class='muted' style='margin:0;'>
            🤖 ARIA • Confidence: {f"{agent.confidence_level:.1f}%" if agent.confidence_level>0 else "N/A"} • Last Update: {datetime.now().strftime('%H:%M:%S')}
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
