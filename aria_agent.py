# app.py — ARIA v2 (lisible, contrasté, néon futuriste, LLM-ready, PDF, GIF, auto-mode)
# pip install streamlit plotly reportlab (reportlab optionnel)
import os, asyncio, random, textwrap, io
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Optional

import streamlit as st
import plotly.graph_objects as go

# ============================= CONFIG =============================
st.set_page_config(page_title="🤖 ARIA – Agent IA Stratégique", page_icon="🧠", layout="wide")
AUTONOMY_KEY = "autonomous_enabled"

# ============================= CSS CLAIR & LISIBLE =============================
st.markdown("""
<style>
/* Immersif (on peut l'enlever si besoin) */
header, footer, [data-testid="stToolbar"] { visibility: hidden; }

/* Palette à fort contraste */
:root{
  --bg:#0b1222; --panel:#0f1a33; --panel2:#0b152b; --txt:#eef3ff; --muted:#a8b3d9;
  --pri:#7aa2ff; --violet:#a78bfa; --teal:#22d3ee; --green:#34d399; --red:#ef4444; --amber:#f59e0b;
  --ring:rgba(122,162,255,.42);
}

/* Fond net (pas de flou) + grille & halos doux */
html, body, .main { background: var(--bg); color: var(--txt); }
.main::after{
  content:""; position:fixed; inset:0; pointer-events:none; opacity:.22;
  background-image: radial-gradient(circle at 24px 24px, rgba(122,162,255,.18) 1.2px, transparent 0);
  background-size: 48px 48px; animation:gridMove 28s linear infinite;
}
@keyframes gridMove { 0%{transform:translate(0,0)} 100%{transform:translate(48px,48px)} }
.main::before{
  content:""; position:fixed; inset:0; pointer-events:none;
  background:
    radial-gradient(600px 280px at 18% 22%, rgba(167,139,250,.16), transparent 60%),
    radial-gradient(600px 280px at 80% 28%, rgba(34,211,238,.14), transparent 60%),
    radial-gradient(520px 260px at 36% 82%, rgba(52,211,153,.14), transparent 60%);
  animation:float 18s ease-in-out infinite;
}
@keyframes float{0%,100%{transform:translate(0,0)}50%{transform:translate(10px,-8px)}}

/* Header héro clair & lisible */
.hero{
  background: linear-gradient(180deg, rgba(17,26,51,.96), rgba(10,18,36,.96));
  border:1px solid var(--ring); border-radius:22px; padding:18px 20px;
  box-shadow: 0 10px 40px rgba(0,0,0,.40), 0 0 90px rgba(122,162,255,.10);
}
.title{
  font-size:34px; font-weight:900; letter-spacing:.2px; margin:0;
  background:linear-gradient(90deg,#7aa2ff 0%, #a78bfa 50%, #22d3ee 100%);
  -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;
}
.sub{color:var(--muted); margin:.25rem 0 0 0; font-weight:600}

/* Cards très lisibles */
.card{
  background: linear-gradient(180deg, rgba(15,26,51,.98), rgba(12,20,40,.98));
  border:1px solid rgba(122,162,255,.30); border-radius:18px; padding:16px; margin:12px 0;
  box-shadow: 0 10px 30px rgba(0,0,0,.35), inset 0 0 0 1px rgba(255,255,255,.04);
}

/* Variantes avec glow net (pas de flou) */
.card.opportunity{ border-color: rgba(52,211,153,.55); box-shadow: 0 0 18px rgba(52,211,153,.20); }
.card.threat{ border-color: rgba(239,68,68,.55); box-shadow: 0 0 18px rgba(239,68,68,.20); }
.card.trend{ border-color: rgba(167,139,250,.55); box-shadow: 0 0 18px rgba(167,139,250,.20); }

/* Badges */
.badge{padding:4px 10px;border-radius:999px;font-size:.78rem;font-weight:800;letter-spacing:.2px}
.b-green{background:rgba(52,211,153,.18); color:#bfffe7; border:1px solid rgba(52,211,153,.45)}
.b-red{background:rgba(239,68,68,.18); color:#ffc9c9; border:1px solid rgba(239,68,68,.45)}
.b-violet{background:rgba(167,139,250,.18); color:#e9ddff; border:1px solid rgba(167,139,250,.45)}
.b-blue{background:rgba(122,162,255,.20); color:#d7e5ff; border:1px solid rgba(122,162,255,.45)}

/* Pensées (Framer-like) */
.thought{
  border-left:4px solid #7aa2ff; background:rgba(122,162,255,.10);
  border-radius:14px; padding:12px 14px; margin:10px 0;
  animation:slideIn .45s cubic-bezier(.175,.885,.32,1.275);
}
@keyframes slideIn{0%{opacity:0;transform:translateY(10px)}100%{opacity:1;transform:translateY(0)}}

/* Boutons primaires */
.stButton > button{
  background:linear-gradient(90deg,#7aa2ff,#22d3ee) !important; color:#051024 !important;
  border:none !important; border-radius:12px !important; font-weight:900 !important;
  box-shadow:0 12px 28px rgba(122,162,255,.35) !important;
}
.stButton > button:active{ transform: translateY(1px); }

/* Metrics */
.metric{ text-align:center; border:1px solid rgba(122,162,255,.35); border-radius:14px; padding:12px }
.metric .k{font-size:22px;font-weight:900}

/* Light mode lisible */
.light .hero,.light .card{ background:#fff; color:#0a1020; border-color: rgba(82,109,255,.28) }
.light body,.light .main{ background:#f4f7ff; color:#0a1020 }
.light .thought{ background:rgba(122,162,255,.10)}

/* Inputs plus lisibles */
.stSelectbox > div > div, .stTextInput > div > div > input {
  background: #0f1a33 !important; color: #eef3ff !important; border-radius: 10px !important;
  border: 1px solid rgba(122,162,255,.35) !important;
}
.light .stSelectbox > div > div, .light .stTextInput > div > div > input {
  background:#fff !important; color:#0a1020 !important; border-color: rgba(82,109,255,.35) !important;
}
</style>
""", unsafe_allow_html=True)

def apply_light_mode(is_light: bool):
    st.markdown(
        "<script>document.documentElement.classList."
        + ("add" if is_light else "remove")
        + "('light')</script>",
        unsafe_allow_html=True,
    )

# ============================= DATA MODELS =============================
@dataclass
class AgentThought:
    content: str
    timestamp: datetime
    confidence: float

@dataclass
class MarketInsight:
    title: str
    description: str
    impact_score: float
    confidence: float
    category: str  # opportunity | threat | trend

# ============================= AGENT =============================
class ARIAAgent:
    def __init__(self, language="fr"):
        self.language = language
        self.status = "idle"   # idle|thinking|analyzing|completed
        self.thoughts: List[AgentThought] = []
        self.current_analysis: Optional[Dict] = None
        self.confidence_level = 0.0
        self.neural_activity = 0
        self.analysis_progress = 0.0

        self.translations = {
            "fr":{
                "name":"ARIA","desc":"Agent de Recherche & d'Intelligence Autonome",
                "status_idle":"🤖 En veille — prêt à analyser",
                "status_thinking":"🧠 Réflexion stratégique…",
                "status_analyzing":"⚡ Analyse multi-dimensionnelle…",
                "status_completed":"✨ Mission accomplie — insights générés",
                "sectors":{"FinTech":"Technologies Financières","AI":"Intelligence Artificielle","Retail":"Distribution"},
                "thoughts":[
                    "Initialisation des capteurs de marché…",
                    "Activation des réseaux neuronaux sectoriels…",
                    "Ingestion de 1 247 sources en temps réel…",
                    "Traitement par modèles de deep learning…",
                    "Corrélation des signaux faibles détectés…",
                    "Modélisation prédictive des tendances…",
                    "Analyse concurrentielle multi-axes…",
                    "Génération d’insights actionnables…",
                    "Synthèse stratégique à haute confiance."
                ]
            },
            "en":{
                "name":"ARIA","desc":"Autonomous Research & Intelligence Agent",
                "status_idle":"🤖 Standby — ready to analyze",
                "status_thinking":"🧠 Strategic thinking…",
                "status_analyzing":"⚡ Multi-dimensional analysis…",
                "status_completed":"✨ Mission accomplished — insights generated",
                "sectors":{"FinTech":"Financial Technologies","AI":"Artificial Intelligence","Retail":"Retail"},
                "thoughts":[
                    "Initializing market sensors…","Activating sector neural nets…","Ingesting 1,247 live sources…",
                    "Processing via deep learning…","Correlating weak signals…","Predictive trend modeling…",
                    "Multi-axis competitive scan…","Generating actionable insights…","High-confidence synthesis."
                ]
            }
        }

        self.market_data = {
            "FinTech":{
                "fr":{
                    "summary":"La FinTech accélère via IA conversationnelle, risque automatisé et intégration blockchain. MiCA renforce la confiance et avantage les acteurs conformes.",
                    "insights":[
                        MarketInsight("IA Conversationnelle Bancaire","KYC, support, scoring temps réel.",9.5,91,"opportunity"),
                        MarketInsight("DeFi Institutionnelle","Produits tokenisés & paiements programmables.",8.8,87,"opportunity"),
                        MarketInsight("Super-Apps","Plateformes unifiées (paiement, crédit, épargne).",8.2,79,"trend"),
                        MarketInsight("Durcissement Réglementaire","MiCA/AML = barrières mais avantage aux conformes.",7.9,94,"threat"),
                    ],
                    "reco":[
                        "Investir dans l’IA conversationnelle avant T2 2025",
                        "Anticiper MiCA 6–9 mois à l’avance",
                        "Acquérir des talents blockchain avant la pénurie",
                        "Feuille de route Super-App progressive"
                    ]
                },
                "en":{
                    "summary":"FinTech is reshaped by conversational AI, risk automation and blockchain. MiCA boosts trust and rewards compliance.",
                    "insights":[
                        MarketInsight("Conversational Banking AI","KYC, support, real-time scoring.",9.5,91,"opportunity"),
                        MarketInsight("Institutional DeFi","Tokenized assets & programmable payments.",8.8,87,"opportunity"),
                        MarketInsight("Super-Apps","Unified platforms (payments, credit, savings).",8.2,79,"trend"),
                        MarketInsight("Regulatory Tightening","MiCA/AML barriers but reward compliance.",7.9,94,"threat"),
                    ],
                    "reco":[
                        "Invest in conversational AI before Q2 2025",
                        "Prepare MiCA 6–9 months ahead",
                        "Acquire blockchain talent before shortage",
                        "Phased Super-App roadmap"
                    ]
                }
            },
            "AI":{
                "fr":{
                    "summary":"Croissance explosive portée par agents autonomes, edge computing et intégration entreprise.",
                    "insights":[
                        MarketInsight("Agents IA Autonomes","Copilotes métiers & orchestration d’outils.",9.8,96,"opportunity"),
                        MarketInsight("IA Enterprise","ROI moyen à 18 mois (productivité/décision).",9.4,89,"opportunity"),
                        MarketInsight("Edge AI Computing","Traitement proche source (latence/coût/privacy).",8.7,83,"trend"),
                        MarketInsight("Pénurie de Talents","Demande senior +423%.",9.2,94,"threat"),
                    ],
                    "reco":[
                        "Capitaliser agents IA sectoriels",
                        "Investir dans l’Edge AI (décentralisation)",
                        "Bâtir expertise AI Act & gouvernance",
                        "Acquérir des équipes IA avant explosion des coûts"
                    ]
                },
                "en":{
                    "summary":"Autonomous agents, edge computing and enterprise integration drive explosive growth.",
                    "insights":[
                        MarketInsight("Autonomous AI Agents","Domain copilots & tool orchestration.",9.8,96,"opportunity"),
                        MarketInsight("Enterprise AI","18-month ROI across quality/productivity.",9.4,89,"opportunity"),
                        MarketInsight("Edge AI Computing","Near-source processing gains.",8.7,83,"trend"),
                        MarketInsight("Talent Shortage","+423% senior demand.",9.2,94,"threat"),
                    ],
                    "reco":[
                        "Capitalize on sector AI agents",
                        "Invest in edge AI for decentralization",
                        "Build AI Act compliance expertise",
                        "Acquire AI teams before cost explosion"
                    ]
                }
            },
            "Retail":{
                "fr":{
                    "summary":"Retail : demand-sensing IA, pricing dynamique et orchestration omnicanale.",
                    "insights":[
                        MarketInsight("Demand Sensing IA","Prévision J+7/J+14 multi-signaux.",9.3,90,"opportunity"),
                        MarketInsight("Dynamic Pricing","+2–4 pts de marge sur catégories sensibles.",8.7,85,"opportunity"),
                        MarketInsight("Orchestration Omnicanale","Click&Collect/Ship-from-store → NPS↑ délais↓.",8.1,78,"trend"),
                        MarketInsight("Pression Logistique","Volatilité transport/énergie → simuler coûts.",8.5,88,"threat"),
                    ],
                    "reco":[
                        "Pilote demand-sensing sur 3 familles top-SKU",
                        "Dynamic pricing sur 10% de l’assortiment",
                        "Optimiser Ship-from-store dans 5 magasins",
                        "Jumeau logistique pour scénarios de coûts"
                    ]
                },
                "en":{
                    "summary":"Retail: AI demand sensing, dynamic pricing, omnichannel orchestration.",
                    "insights":[
                        MarketInsight("AI Demand Sensing","J+7/J+14 multi-signal forecasting.",9.3,90,"opportunity"),
                        MarketInsight("Dynamic Pricing","+2–4 margin pts on sensitive cats.",8.7,85,"opportunity"),
                        MarketInsight("Omnichannel Orchestration","Click&Collect/Ship-from-store → NPS↑.",8.1,78,"trend"),
                        MarketInsight("Logistics Pressure","Volatile costs → scenario simulation.",8.5,88,"threat"),
                    ],
                    "reco":[
                        "Pilot demand sensing on 3 top-SKU families",
                        "Enable dynamic pricing on top 10%",
                        "Optimize Ship-from-store in 5 stores",
                        "Build a logistics digital twin"
                    ]
                }
            }
        }

    def t(self,key): return self.translations[self.language].get(key,key)

    async def activate(self, sector:str):
        self.status="thinking"; self.thoughts=[]; self.analysis_progress=0.0
        self.neural_activity = random.randint(820, 1180)
        for i,base in enumerate(self.translations[self.language]["thoughts"]):
            await asyncio.sleep(random.uniform(.35,.70))
            content = await maybe_llm_thought(base, self.language, sector)
            self.thoughts.append(AgentThought(content, datetime.now(), random.uniform(.86,.97)))
            self.analysis_progress = (i+1)/len(self.translations[self.language]["thoughts"])*100
            if i==3: self.status="analyzing"
        self.status="completed"
        self.current_analysis = self.market_data.get(sector,{}).get(self.language,{})
        self.confidence_level = float(random.uniform(88.0, 97.0))
        self.neural_activity += random.randint(-30, 60)

# ============================= LLM (optionnel) =============================
async def maybe_llm_thought(base:str, lang:str, sector:str)->str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return base
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        prompt = (f"Lang={lang}. Expand into 1 concise sentence for sector {sector}. "
                  f"Concrete and insightful, include one metric if relevant. Thought: {base}")
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":"You are ARIA: concise, clear, technical."},
                      {"role":"user","content":prompt}],
            max_tokens=50, temperature=0.7)
        return resp.choices[0].message.content.strip()
    except Exception:
        return base

# ============================= CHARTS =============================
def gauge(value: float)->go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=max(0.0, float(value)),
        number={'font':{'size':38,'color':'#d7e5ff'}},
        title={'text':"Confidence",'font':{'size':18,'color':'#d7e5ff'}},
        gauge={
            'axis':{'range':[0,100],'tickcolor':'#a8b3d9','tickwidth':1,'ticklen':4},
            'bar':{'color':"#7aa2ff",'thickness':0.78},
            'steps':[
                {'range':[0,60],'color':'rgba(239,68,68,.25)'},
                {'range':[60,85],'color':'rgba(245,158,11,.25)'},
                {'range':[85,100],'color':'rgba(52,211,153,.28)'}
            ],
            'threshold':{'line':{'color':'#a78bfa','width':5},'value':90}
        }
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                      height=320, margin=dict(l=10,r=10,t=40,b=10), font={'color':'#eef3ff'})
    return fig

def live_neural_chart(series: List[int])->go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=series, mode="lines+markers", line={'shape':'spline'}))
    fig.update_layout(
        height=220, margin=dict(l=10,r=10,t=20,b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(20,30,60,.85)",
        font={'color':'#d7e5ff'},
        xaxis={'visible':False}, yaxis={'gridcolor':'rgba(122,162,255,.25)'}
    )
    return fig

# ============================= STATE =============================
if "agent" not in st.session_state: st.session_state.agent = ARIAAgent("fr")
if "language" not in st.session_state: st.session_state.language = "fr"
if "neural_series" not in st.session_state: st.session_state.neural_series = [800, 830, 810, 890, 930]
if "chat" not in st.session_state: st.session_state.chat = []
agent: ARIAAgent = st.session_state.agent
agent.language = st.session_state.language

# ============================= HEADER (avec GIF) =============================
st.markdown(f"""
<div class="hero">
  <div style="display:flex;align-items:center;gap:14px;">
    <div style="width:46px;height:46px;border-radius:12px;border:1px solid rgba(255,255,255,.12);
         display:flex;align-items:center;justify-content:center;background:linear-gradient(120deg,#7aa2ff,#a78bfa)">🤖</div>
    <div style="flex:1 1 auto;">
      <h1 class="title">{agent.t('name')} • {agent.t('desc')}</h1>
      <p class="sub">🧠 Neural: {agent.neural_activity} &nbsp;|&nbsp; 📚 Sources: 1,247 &nbsp;|&nbsp; ⚡ Real-time</p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# Controls (lisibles)
cA, cB, cC, cD, cE = st.columns([1.1, 1.1, .9, 1.2, 1.4])
with cA:
    lang = st.selectbox("🌐 Language / Langue", ["🇫🇷 Français","🇺🇸 English"])
    new_lang = "fr" if "Français" in lang else "en"
    if new_lang != st.session_state.language:
        st.session_state.language = new_lang
        st.rerun()
with cB:
    sectors = agent.translations[agent.language]["sectors"]
    sector = st.selectbox("🎯 Sector", list(sectors.keys()), format_func=lambda k: sectors[k])
with cC:
    light = st.toggle("🌗 Light mode", value=False)
    apply_light_mode(light)
with cD:
    autonomous = st.toggle("🤖 Autonomous (every 5 min)", value=st.session_state.get(AUTONOMY_KEY, False))
    st.session_state[AUTONOMY_KEY] = autonomous
with cE:
    GIF_URL = st.text_input("🎞️ GIF (URL)", value="", help="Colle ton GIF (ex: animé de l'avatar).")

# Auto-refresh & auto-run
if autonomous:
    st.autorefresh(interval=5_000, key="autorefresh")   # refresh UI (démo)
    last = st.session_state.get("last_run")
    if (not last) or (datetime.now() - last > timedelta(minutes=5)):
        asyncio.run(agent.activate(sector)); st.session_state.last_run = datetime.now()

# ============================= LAYOUT =============================
left, right = st.columns([1,2], vertical_alignment="top")

# -------- LEFT : Panneau agent, Metrics, Live neural, GIF ----------
with left:
    # Panneau agent + barre de progression
    st.markdown(f"""
    <div class="card" style="text-align:center">
      <div style="font-size:40px;margin-bottom:6px">🧠</div>
      <div class="badge b-blue">{agent.t('status_'+agent.status)}</div>
      <div style="height:10px"></div>
      <div style="border:1px solid var(--ring);border-radius:12px;overflow:hidden">
        <div style="height:12px;width:{agent.analysis_progress:.1f}%;background:linear-gradient(90deg,#7aa2ff,#22d3ee)"></div>
      </div>
      <div style="margin-top:6px;color:var(--muted)">Progress: {agent.analysis_progress:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

    # Boutons
    c1, c2 = st.columns(2)
    with c1:
        if agent.status in ("idle","completed"):
            if st.button("🚀 Activate ARIA", use_container_width=True):
                asyncio.run(agent.activate(sector)); st.rerun()
        else:
            if st.button("⏹️ Stop", use_container_width=True):
                agent.status="idle"; agent.thoughts=[]; agent.current_analysis=None
                agent.analysis_progress=0; agent.confidence_level=0; st.rerun()
    with c2:
        if st.button("🔄 Reset", use_container_width=True):
            agent.status="idle"; agent.thoughts=[]; agent.current_analysis=None
            agent.analysis_progress=0; agent.confidence_level=0; st.rerun()

    # Metrics (bien lisibles)
    st.markdown("#### 📊 Real-time Metrics")
    m1, m2 = st.columns(2)
    with m1:
        st.markdown(f"""<div class="metric"><div>Neural Activity</div><div class="k">{agent.neural_activity}</div></div>""", unsafe_allow_html=True)
    with m2:
        conf_txt = f"{agent.confidence_level:.1f}%" if agent.confidence_level>0 else "—"
        st.markdown(f"""<div class="metric"><div>Confidence</div><div class="k">{conf_txt}</div></div>""", unsafe_allow_html=True)

    # Live neural
    new_point = max(720, min(1240, st.session_state.neural_series[-1] + random.randint(-40, 50)))
    st.session_state.neural_series.append(new_point)
    st.plotly_chart(live_neural_chart(st.session_state.neural_series[-30:]), use_container_width=True)

    # GIF (si fourni)
    if GIF_URL.strip():
        st.markdown("#### 🎞️ ARIA Avatar")
        st.image(GIF_URL, use_container_width=True, caption="Avatar animé ARIA")

# -------- RIGHT : Thoughts, Summary, Gauge, Insights, Reco, Chat, Export, Note projet --------
with right:
    # Thoughts (lisibles, animées)
    if agent.status != "idle" and agent.thoughts:
        st.markdown('<div class="card"><h3>🧠 Agent Thought Process</h3></div>', unsafe_allow_html=True)
        for th in agent.thoughts:
            st.markdown(f"""
            <div class="thought">
              <div style="display:flex;justify-content:space-between;align-items:center">
                <div>{th.content}</div>
                <div class="badge b-green">{th.confidence:.1%}</div>
              </div>
              <div style="color:var(--muted);font-size:.86rem;margin-top:4px">{th.timestamp.strftime("%H:%M:%S")}</div>
            </div>
            """, unsafe_allow_html=True)

    # Résultats
    if agent.current_analysis and agent.status == "completed":
        st.markdown(f"""
        <div class="card">
          <h3>📋 Executive Summary <span class="badge b-green" style="margin-left:6px">High confidence</span></h3>
          <div style="border:1px solid var(--ring);border-radius:14px;padding:14px;margin-top:6px;background:#0e1a33">
            {agent.current_analysis.get("summary","")}
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="card"><h3 style="text-align:center">📈 Analysis Confidence</h3></div>', unsafe_allow_html=True)
        st.plotly_chart(gauge(agent.confidence_level), use_container_width=True)

        insights: List[MarketInsight] = agent.current_analysis.get("insights") or []
        if insights:
            st.markdown('<div class="card"><h3>🎯 Strategic Insights</h3></div>', unsafe_allow_html=True)
            def render(cat, label, bclass):
                st.markdown(f'<h4 style="margin:.4rem 0">{label}</h4>', unsafe_allow_html=True)
                for ins in [i for i in insights if i.category==cat]:
                    st.markdown(f"""
                    <div class="card {cat}">
                      <div style="display:flex;justify-content:space-between;align-items:center">
                        <h5 style="margin:.1rem 0">{ins.title}</h5>
                        <span class="badge {bclass}">{'High' if ins.impact_score>=8.5 else 'Medium'}</span>
                      </div>
                      <div style="color:#dfe7ff">{ins.description}</div>
                      <div style="display:flex;gap:16px;margin-top:8px;">
                        <div>Impact: <b>{ins.impact_score}/10</b></div>
                        <div>Confidence: <b>{ins.confidence}%</b></div>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)
            render("opportunity","💡 Market Opportunities","b-green")
            render("threat","⚠️ Strategic Threats","b-red")
            render("trend","📈 Emerging Trends","b-violet")

        recos = agent.current_analysis.get("reco") or []
        if recos:
            st.markdown('<div class="card"><h3>🧭 AI Strategic Recommendations</h3></div>', unsafe_allow_html=True)
            for i, rec in enumerate(recos, 1):
                st.markdown(f"""
                <div class="card" style="border-color:rgba(167,139,250,.45);box-shadow:0 0 18px rgba(167,139,250,.18)">
                    <div style="display:flex;gap:10px">
                        <div class="badge b-blue">{i}</div>
                        <div style="font-weight:700">{rec}</div>
                    </div>
                    <div style="margin-top:8px;display:flex;gap:8px">
                        <span class="badge b-green">High Impact</span>
                        <span class="badge b-blue">Strategic</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Mini chat
        st.markdown('<div class="card"><h3>💬 Ask ARIA</h3></div>', unsafe_allow_html=True)
        q = st.text_input("Pose une question (risque, concurrence, tendance)…", key="ask")
        if st.button("Send"):
            st.session_state.chat.append({"role":"user","content":q,"time":datetime.now().strftime("%H:%M:%S")})
            ans = asyncio.run(maybe_llm_thought(f"Question: {q}", agent.language, sector))
            if ans == f"Question: {q}":
                ans = f"🔎 {'Indicateur clé' if agent.language=='fr' else 'Key indicator'}: {random.randint(8,12)}% " \
                      f"{'CAGR estimé' if agent.language=='fr' else 'estimated CAGR'} • " \
                      f"{'Priorité' if agent.language=='fr' else 'Priority'}: {'haute' if random.random()>0.5 else 'moyenne'}."
            st.session_state.chat.append({"role":"assistant","content":ans,"time":datetime.now().strftime("%H:%M:%S")})
            st.rerun()
        for m in st.session_state.chat[-6:]:
            who = "👤 You" if m["role"]=="user" else "🤖 ARIA"
            color = "rgba(122,162,255,.35)" if m["role"]=="user" else "rgba(52,211,153,.35)"
            st.markdown(f"""<div class="card" style="border-color:{color}">
                <b>{who}</b> <span style="float:right;color:var(--muted)">{m['time']}</span><div>{m['content']}</div></div>""",
                unsafe_allow_html=True)

        # Export (TXT & PDF)
        st.markdown('<div class="card"><h3>📤 Export & Actions</h3></div>', unsafe_allow_html=True)
        e1, e2, e3 = st.columns(3)
        with e1:
            if st.button("📄 Export TXT"):
                insights = agent.current_analysis.get("insights") or []
                lines = [
                    "ARIA – Strategic Intelligence Report",
                    f"Generated: {datetime.now():%Y-%m-%d %H:%M}",
                    f"Sector: {sector}",
                    f"Confidence: {agent.confidence_level:.1f}%",
                    "", "Executive Summary:", agent.current_analysis.get("summary",""), "", "Insights:"
                ]
                for ins in insights:
                    lines.append(f"- [{ins.category}] {ins.title} | Impact {ins.impact_score}/10 | Conf {ins.confidence}% — {ins.description}")
                lines += ["", "Recommendations:"] + [f"{i+1}. {r}" for i,r in enumerate(recos)]
                st.download_button("⬇️ Download .txt", "\n".join(lines).encode("utf-8"),
                                   file_name=f"ARIA_{sector}_{datetime.now():%Y%m%d_%H%M}.txt", mime="text/plain")
        with e2:
            if st.button("🧾 Export PDF"):
                try:
                    from reportlab.lib.pagesizes import A4
                    from reportlab.pdfgen import canvas
                    from reportlab.lib.units import cm
                    from reportlab.lib.colors import HexColor
                    fn = f"ARIA_{sector}_{datetime.now():%Y%m%d_%H%M}.pdf"
                    buff = io.BytesIO()
                    c = canvas.Canvas(buff, pagesize=A4)
                    W,H=A4
                    c.setFillColor(HexColor("#0b1222")); c.rect(0,0,W,H,stroke=0,fill=1)
                    c.setFillColor(HexColor("#7aa2ff")); c.setFont("Helvetica-Bold",22)
                    c.drawString(2*cm, H-2.5*cm, "ARIA — Strategic Intelligence Report")
                    c.setFillColor(HexColor("#d7e5ff")); c.setFont("Helvetica",10)
                    c.drawString(2*cm, H-3.2*cm, f"Sector: {sector}  |  Confidence: {agent.confidence_level:.1f}%  |  Generated: {datetime.now():%Y-%m-%d %H:%M}")
                    text=c.beginText(2*cm, H-4.2*cm); text.setFont("Helvetica",11); text.setFillColor(HexColor("#eef3ff"))
                    text.textLine("Executive Summary")
                    text.setFont("Helvetica",10); text.setFillColor(HexColor("#d7e5ff"))
                    for line in textwrap.wrap(agent.current_analysis.get("summary",""), 95): text.textLine(line)
                    text.textLine(""); text.setFont("Helvetica",11); text.setFillColor(HexColor("#eef3ff")); text.textLine("Insights")
                    for ins in agent.current_analysis.get("insights") or []:
                        text.setFont("Helvetica-Bold",10); text.setFillColor(HexColor("#7aa2ff")); text.textLine(f"• {ins.title} [{ins.category}]")
                        text.setFont("Helvetica",10); text.setFillColor(HexColor("#d7e5ff"))
                        for line in textwrap.wrap(f"Impact {ins.impact_score}/10 | Conf {ins.confidence}% — {ins.description}", 95): text.textLine(line)
                        text.textLine("")
                    text.setFont("Helvetica",11); text.setFillColor(HexColor("#eef3ff")); text.textLine("Recommendations")
                    for i,r in enumerate(recos,1):
                        text.setFont("Helvetica",10); text.setFillColor(HexColor("#d7e5ff")); text.textLine(f"{i}. {r}")
                    c.drawText(text); c.showPage(); c.save(); buff.seek(0)
                    st.download_button("⬇️ Download PDF", data=buff, file_name=fn, mime="application/pdf")
                except Exception:
                    st.warning("Reportlab non dispo — export Markdown proposé.")
                    md = f"# ARIA Report — {sector}\n\n**Confidence:** {agent.confidence_level:.1f}%\n\n## Executive Summary\n{agent.current_analysis.get('summary','')}\n\n## Insights\n" + \
                         "\n".join([f"- **{i.title}** [{i.category}] — Impact {i.impact_score}/10, Conf {i.confidence}%\n  {i.description}" for i in (agent.current_analysis.get('insights') or [])]) + \
                         "\n\n## Recommendations\n" + "\n".join([f"1. {r}" for r in recos])
                    st.download_button("⬇️ Download .md", md.encode("utf-8"), file_name="ARIA_report.md", mime="text/markdown")
        with e3:
            if st.button("🔔 Setup Alerts"):
                st.success("✅ Alerts ON — ARIA te notifie sur les changements majeurs.")

        # Note de projet — Résumé exécutif (copiable)
        note = f"""🧾 NOTE DE PROJET — ARIA : Autonomous Research & Intelligence Agent

Agent IA autonome pour l'analyse stratégique de marchés

🎯 Fonctionnalités core :
- Agent IA autonome avec processus de pensée visible
- Analyse sectorielle (FinTech, SaaS, E-commerce, Retail…)
- Interface futuriste glassmorphism + animations
- Multilingue FR/EN automatique
- Visualisations temps réel (neural, confiance, métriques)
- Génération d'insights (opportunités, menaces, recommandations)
- Export automatique de rapports stratégiques

🛠️ STACK TECHNIQUE :
- Frontend → Streamlit + CSS avancé
- Backend  → Python + Architecture d'agent
- Dataviz  → Plotly
- IA Logic → Processus décisionnel + scoring
- Deploy   → Streamlit Cloud
- Langages → Python, CSS, JS

🎨 DESIGN & UX :
- Avatar qui pulse (GIF)
- Pensées temps réel
- Graphiques confiance dynamiques
- Animations fluides + grille/particules
- Thème sombre/clair
- Responsive

🧠 Simulation d'intelligence :
- idle → thinking → analyzing → completed
- Métriques neuronales évolutives
- Scoring de confiance contextuel
"""
        with st.expander("🧾 Note de projet — Résumé exécutif (aperçu/copier)"):
            st.code(note, language="markdown")

# ============================= FOOTER =============================
conf = f"{agent.confidence_level:.1f}%" if agent.confidence_level>0 else "—"
st.markdown(f"""
<div class="card" style="margin-top:16px; text-align:center">
  <b>ARIA</b> • Real-time Market Intelligence • Confidence: {conf} • Neural: {agent.neural_activity} • Sources: 1,247
</div>
""", unsafe_allow_html=True)
