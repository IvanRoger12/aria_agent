# app.py — ARIA Futuriste (net, néon, animations, LLM-ready, PDF, live graph)
# pip install streamlit plotly reportlab (reportlab optionnel)
import os, asyncio, random, textwrap
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Optional

import streamlit as st
import plotly.graph_objects as go

# ====== CONFIG ======
st.set_page_config(page_title="🤖 ARIA – Strategic Intelligence Agent", page_icon="🧠", layout="wide")
AUTONOMY_KEY = "autonomous_enabled"

# ====== CSS – Net, contrasté, glow néon, particules & grille subtile ======
st.markdown("""
<style>
/* Hide Streamlit top & footer for immersive mode */
header, [data-testid="stToolbar"], footer {visibility:hidden;}
/* Base */
:root{
  --bg:#0b1020; --panel:#121a2e; --panel-2:#0f1829; --txt:#e6edf7; --muted:#96a2c6;
  --primary:#7aa2ff; --accent:#a78bfa; --teal:#22d3ee; --green:#34d399; --red:#ef4444; --amber:#f59e0b;
  --ring:rgba(122,162,255,.45);
}
html, body, .main { background: var(--bg); color: var(--txt); }
.main::before, .main::after{content:"";position:fixed;inset:0;pointer-events:none;}
/* moving grid */
.main::after{
  background-image: radial-gradient(circle at 25px 25px, rgba(122,162,255,.08) 1px, transparent 0);
  background-size: 50px 50px; opacity:.35; filter:contrast(105%);
  animation:gridMove 26s linear infinite;
}
@keyframes gridMove { 0%{transform:translate(0,0)}100%{transform:translate(50px,50px)} }
/* soft particles */
.main::before{
  background:
    radial-gradient(600px 300px at 15% 20%, rgba(167,139,250,.14), transparent 60%),
    radial-gradient(600px 300px at 80% 30%, rgba(34,211,238,.12), transparent 60%),
    radial-gradient(500px 260px at 30% 80%, rgba(52,211,153,.12), transparent 60%);
  filter:saturate(110%);
  animation:float 18s ease-in-out infinite;
}
@keyframes float{0%,100%{transform:translate(0,0)}50%{transform:translate(10px,-8px)}}

/* Header */
.hero{
  border:1px solid var(--ring); border-radius:22px; padding:22px 22px 16px;
  background:linear-gradient(180deg, rgba(18,26,46,.85), rgba(12,18,34,.85));
  box-shadow:0 10px 40px rgba(0,0,0,.35), 0 0 80px rgba(122,162,255,.08);
}
.title{
  font-size:34px; font-weight:800;
  background:linear-gradient(90deg, #7aa2ff 0%, #a78bfa 50%, #22d3ee 100%);
  -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;
  letter-spacing:.3px; margin:0;
}
.sub{color:var(--muted); margin:.3rem 0 0 0}

/* Card */
.card{
  background:linear-gradient(180deg, rgba(14,20,40,.9), rgba(12,18,34,.9));
  border:1px solid rgba(122,162,255,.20); border-radius:18px; padding:18px; box-shadow:
  0 8px 28px rgba(0,0,0,.35), inset 0 0 0 1px rgba(255,255,255,.03);
}

/* Neon glow categories */
.card.opportunity{ border-color: rgba(52,211,153,.45); box-shadow:0 0 24px rgba(52,211,153,.16); }
.card.threat{ border-color: rgba(239,68,68,.45); box-shadow:0 0 24px rgba(239,68,68,.16); }
.card.trend{ border-color: rgba(167,139,250,.45); box-shadow:0 0 24px rgba(167,139,250,.16); }

/* Badges */
.badge{padding:4px 10px;border-radius:999px;font-size:.78rem;font-weight:700;letter-spacing:.2px}
.b-green{background:rgba(52,211,153,.18); color:#8bffd0; border:1px solid rgba(52,211,153,.35)}
.b-red{background:rgba(239,68,68,.18); color:#ffb0b0; border:1px solid rgba(239,68,68,.35)}
.b-violet{background:rgba(167,139,250,.18); color:#d7c9ff; border:1px solid rgba(167,139,250,.35)}
.b-blue{background:rgba(122,162,255,.20); color:#cfe0ff; border:1px solid rgba(122,162,255,.38)}

/* Thought item (Framer-like) */
.thought{
  border-left:4px solid #7aa2ff; background:rgba(122,162,255,.08);
  border-radius:14px; padding:12px 14px; margin:10px 0;
  animation:slideIn .45s cubic-bezier(.175,.885,.32,1.275);
}
@keyframes slideIn{0%{opacity:0;transform:translateY(10px)}100%{opacity:1;transform:translateY(0)}}

/* Buttons */
.btn{border:none;border-radius:12px;padding:10px 16px;font-weight:800;color:#071225;
  background:linear-gradient(90deg,#7aa2ff,#22d3ee); box-shadow:0 10px 30px rgba(124,181,255,.3)}
.btn:active{transform:translateY(1px)}

.metric{ text-align:center; border:1px solid rgba(122,162,255,.25); border-radius:14px; padding:12px }
.metric .k{font-size:22px;font-weight:900}

/* Light mode override */
.light .hero,.light .card{ background:linear-gradient(180deg, rgba(255,255,255,.92), rgba(255,255,255,.92));
  color:#0a0f1f; border-color: rgba(82,109,255,.28) }
.light body,.light .main{ background:#f6f8ff; color:#0a0f1f }
.light .thought{ background:rgba(122,162,255,.12)}
</style>
""", unsafe_allow_html=True)

def apply_light_mode(is_light: bool):
    if is_light:
        st.markdown("<script>document.documentElement.classList.add('light')</script>", unsafe_allow_html=True)
    else:
        st.markdown("<script>document.documentElement.classList.remove('light')</script>", unsafe_allow_html=True)

# ====== MODELS ======
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

# ====== AGENT ======
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
                        MarketInsight("IA Conversationnelle Bancaire","KYC, support client, scoring temps réel.",9.5,91,"opportunity"),
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
                        MarketInsight("Dynamic Pricing","+2–4 pts de marge sur familles sensibles.",8.7,85,"opportunity"),
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
        self.neural_activity = random.randint(780, 1180)
        for i,txt in enumerate(self.translations[self.language]["thoughts"]):
            await asyncio.sleep(random.uniform(.35,.75))
            # Option LLM : si OPENAI_API_KEY présent, on enrichit la pensée
            content = await maybe_llm_thought(txt, self.language, sector)
            self.thoughts.append(AgentThought(content, datetime.now(), random.uniform(.86,.97)))
            self.analysis_progress = (i+1)/len(self.translations[self.language]["thoughts"])*100
            if i==3: self.status="analyzing"
        self.status="completed"
        self.current_analysis = self.market_data.get(sector,{}).get(self.language,{})
        self.confidence_level = float(random.uniform(88.0, 97.0))
        self.neural_activity += random.randint(-30, 70)

# ====== (Optionnel) LLM – génère des pensées uniques si OPENAI_API_KEY défini ======
async def maybe_llm_thought(base:str, lang:str, sector:str)->str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:  # fallback sans LLM
        return base
    try:
        # Lazy import pour éviter l’erreur si non installé
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        prompt = (f"Lang={lang}. You are ARIA, an autonomous market agent. Expand this thought (1 sentence) "
                  f"about sector {sector}, with a concrete angle and metric if relevant. Thought: {base}")
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":"You are ARIA – concise, technical, insightful."},
                      {"role":"user","content":prompt}],
            max_tokens=50, temperature=0.7)
        return resp.choices[0].message.content.strip()
    except Exception:
        return base

# ====== UI HELPERS ======
def gauge(value: float)->go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=max(0.0, float(value)),
        number={'font':{'size':38,'color':'#cfe0ff'}},
        title={'text':"Confidence","font":{'size':18,'color':'#cfe0ff'}},
        gauge={
            'axis':{'range':[0,100],'tickcolor':'#7aa2ff'},
            'bar':{'color':"#7aa2ff",'thickness':0.78},
            'steps':[
                {'range':[0,60],'color':'rgba(239,68,68,.25)'},
                {'range':[60,85],'color':'rgba(245,158,11,.25)'},
                {'range':[85,100],'color':'rgba(52,211,153,.25)'}
            ],
            'threshold':{'line':{'color':'#a78bfa','width':5},'value':90}
        }
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                      height=320, margin=dict(l=15,r=15,t=40,b=10), font={'color':'#e6edf7'})
    return fig

def live_neural_chart(series: List[int])->go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=series, mode="lines+markers", line={'shape':'spline'}))
    fig.update_layout(
        height=220, margin=dict(l=10,r=10,t=20,b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(12,18,34,.6)",
        font={'color':'#cfe0ff'}, xaxis={'visible':False}, yaxis={'gridcolor':'rgba(122,162,255,.2)'}
    )
    return fig

# ====== STATE INIT ======
if "agent" not in st.session_state: st.session_state.agent = ARIAAgent("fr")
if "language" not in st.session_state: st.session_state.language = "fr"
if "neural_series" not in st.session_state: st.session_state.neural_series = [800, 820, 790, 860, 910]
if "chat" not in st.session_state: st.session_state.chat = []

agent: ARIAAgent = st.session_state.agent
agent.language = st.session_state.language

# ====== HEADER ======
with st.container():
    st.markdown(f"""
    <div class="hero">
      <div style="display:flex;align-items:center;gap:14px;">
        <div style="width:44px;height:44px;border-radius:12px;border:1px solid rgba(255,255,255,.12);
             display:flex;align-items:center;justify-content:center;background:linear-gradient(120deg,#7aa2ff,#a78bfa);">🤖</div>
        <div style="flex:1 1 auto;">
          <h1 class="title">{agent.t('name')} • {agent.t('desc')}</h1>
          <p class="sub">🧠 Neural: {agent.neural_activity} &nbsp;&nbsp;|&nbsp;&nbsp; 📚 Sources: 1,247 &nbsp;&nbsp;|&nbsp;&nbsp; ⚡ Real-time</p>
        </div>
        <div style="display:flex;gap:8px;align-items:center;">
          <!-- Dark/Light toggle rendered below -->
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# Top controls
colA, colB, colC, colD = st.columns([1.1, 1.2, .9, 1.1])
with colA:
    lang = st.selectbox("🌐 Language / Langue", ["🇫🇷 Français","🇺🇸 English"])
    new_lang = "fr" if "Français" in lang else "en"
    if new_lang != st.session_state.language:
        st.session_state.language = new_lang
        st.rerun()
with colB:
    sectors = agent.translations[agent.language]["sectors"]
    sector = st.selectbox("🎯 Sector", list(sectors.keys()), format_func=lambda k: sectors[k])
with colC:
    light = st.toggle("🌗 Light mode", value=False)
    apply_light_mode(light)
with colD:
    autonomous = st.toggle("🤖 Autonomous (every 5 min)", value=st.session_state.get(AUTONOMY_KEY, False))
    st.session_state[AUTONOMY_KEY] = autonomous

# Autorefresh for live chart & autonomy
if autonomous:
    st.experimental_set_query_params(_=str(datetime.now().timestamp()))  # avoid caching
    st.autorefresh(interval=5_000, key="autorefresh")  # 5s refresh for demo
    # Optionally relaunch analysis every 5 minutes:
    last = st.session_state.get("last_run")
    if (not last) or (datetime.now() - last > timedelta(minutes=5)):
        asyncio.run(agent.activate(sector))
        st.session_state.last_run = datetime.now()

# ====== LAYOUT ======
left, right = st.columns([1,2], vertical_alignment="top")

# LEFT — Control, Metrics, Live Neural
with left:
    st.markdown(f"""
    <div class="card" style="text-align:center">
      <div style="font-size:42px;margin-bottom:8px">🧠</div>
      <div class="badge b-blue">{agent.t('status_'+agent.status)}</div>
      <div style="height:8px"></div>
      <div style="border:1px solid var(--ring);border-radius:12px;overflow:hidden">
        <div style="height:12px;width:{agent.analysis_progress:.1f}%;background:linear-gradient(90deg,#7aa2ff,#22d3ee)"></div>
      </div>
      <div style="margin-top:6px;color:var(--muted)">Progress: {agent.analysis_progress:.1f}%</div>
      <div style="height:10px"></div>
      <div style="display:flex;gap:10px;justify-content:center">
        <form action="#" method="get"></form>
      </div>
    </div>
    """, unsafe_allow_html=True)

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

    st.markdown("#### 📊 Real-time Metrics")
    mcol1, mcol2 = st.columns(2)
    with mcol1:
        st.markdown(f"""<div class="metric"><div>Neural Activity</div><div class="k">{agent.neural_activity}</div></div>""", unsafe_allow_html=True)
    with mcol2:
        conf_txt = f"{agent.confidence_level:.1f}%" if agent.confidence_level>0 else "—"
        st.markdown(f"""<div class="metric"><div>Confidence</div><div class="k">{conf_txt}</div></div>""", unsafe_allow_html=True)

    # Live neural series (demo)
    new_point = max(700, min(1250, (st.session_state.neural_series[-1] + random.randint(-40, 50))))
    st.session_state.neural_series.append(new_point)
    st.plotly_chart(live_neural_chart(st.session_state.neural_series[-30:]), use_container_width=True)

# RIGHT — Thought process, Summary, Gauge, Insights, Recos, Chat & Export
with right:
    # Thoughts
    if agent.status != "idle" and agent.thoughts:
        st.markdown('<div class="card"><h3>🧠 Agent Thought Process</h3></div>', unsafe_allow_html=True)
        for th in agent.thoughts:
            st.markdown(f"""
            <div class="thought">
              <div style="display:flex;justify-content:space-between;align-items:center">
                <div>{th.content}</div>
                <div class="badge b-green">{th.confidence:.1%}</div>
              </div>
              <div style="color:var(--muted);font-size:.85rem;margin-top:4px">{th.timestamp.strftime("%H:%M:%S")}</div>
            </div>
            """, unsafe_allow_html=True)

    # Results
    if agent.current_analysis and agent.status == "completed":
        st.markdown(f"""
        <div class="card">
          <h3>📋 Executive Summary <span class="badge b-green" style="margin-left:6px">High confidence</span></h3>
          <div style="border:1px solid var(--ring);border-radius:14px;padding:14px;margin-top:6px;background:rgba(122,162,255,.08)">
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
                      <div style="color:var(--muted)">{ins.description}</div>
                      <div style="display:flex;gap:16px;margin-top:8px;color:#cfe0ff">
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
                <div class="card" style="border-color:rgba(167,139,250,.38);box-shadow:0 0 18px rgba(167,139,250,.12)">
                    <div style="display:flex;gap:10px">
                        <div class="badge b-blue">{i}</div>
                        <div>{rec}</div>
                    </div>
                    <div style="margin-top:8px;display:flex;gap:8px">
                        <span class="badge b-green">High Impact</span>
                        <span class="badge b-blue">Strategic</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Mini chat (poser une question à l’agent)
        st.markdown('<div class="card"><h3>💬 Ask ARIA</h3></div>', unsafe_allow_html=True)
        q = st.text_input("Pose une question sur le secteur (ex. risque, concurrence, tendances)…", key="ask")
        if st.button("Send"):
            user_msg = {"role":"user","content":q,"time":datetime.now().strftime("%H:%M:%S")}
            st.session_state.chat.append(user_msg)
            # Simple answer (LLM si clé, sinon heuristique)
            ans = asyncio.run(maybe_llm_thought(f"Question: {q}", agent.language, sector))
            if ans == f"Question: {q}":
                # fallback heuristic
                ans = f"{'🔎' if agent.language=='fr' else '🔎'} " \
                      f"{'Indicateur clé' if agent.language=='fr' else 'Key indicator'}: " \
                      f"{random.randint(8,12)}% {'CAGR estimé' if agent.language=='fr' else 'estimated CAGR'} • " \
                      f"{'Priorité' if agent.language=='fr' else 'Priority'}: {'haute' if random.random()>0.5 else 'moyenne'}."
            bot_msg = {"role":"assistant","content":ans,"time":datetime.now().strftime("%H:%M:%S")}
            st.session_state.chat.append(bot_msg)
            st.rerun()
        # render chat
        for m in st.session_state.chat[-6:]:
            if m["role"]=="user":
                st.markdown(f"""<div class="card" style="border-color:rgba(122,162,255,.35)"><b>👤 You</b> <span style="float:right;color:var(--muted)">{m['time']}</span><div>{m['content']}</div></div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div class="card" style="border-color:rgba(52,211,153,.35)"><b>🤖 ARIA</b> <span style="float:right;color:var(--muted)">{m['time']}</span><div>{m['content']}</div></div>""", unsafe_allow_html=True)

        # Export
        st.markdown('<div class="card"><h3>📤 Export & Actions</h3></div>', unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        with c1:
            if st.button("📄 Export TXT"):
                insights = agent.current_analysis.get("insights") or []
                lines = [
                    "ARIA – Strategic Intelligence Report",
                    f"Generated: {datetime.now()}",
                    f"Sector: {sector}",
                    f"Confidence: {agent.confidence_level:.1f}%",
                    "",
                    "Executive Summary:",
                    agent.current_analysis.get("summary",""), "",
                    "Insights:"
                ]
                for ins in insights:
                    lines.append(f"- [{ins.category}] {ins.title} | Impact {ins.impact_score}/10 | Conf {ins.confidence}% — {ins.description}")
                lines.append("\nRecommendations:")
                for i,r in enumerate(recos,1): lines.append(f"{i}. {r}")
                st.download_button("⬇️ Download .txt", "\n".join(lines).encode("utf-8"),
                                   file_name=f"ARIA_{sector}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt", mime="text/plain")
        with c2:
            # PDF (reportlab) with graceful fallback
            if st.button("🧾 Export PDF"):
                try:
                    from reportlab.lib.pagesizes import A4
                    from reportlab.pdfgen import canvas
                    from reportlab.lib.units import cm
                    from reportlab.lib.colors import HexColor
                    fn = f"ARIA_{sector}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
                    import io
                    buff = io.BytesIO()
                    c = canvas.Canvas(buff, pagesize=A4)
                    W,H = A4
                    c.setFillColor(HexColor("#0b1020")); c.rect(0,0,W,H,stroke=0,fill=1)
                    c.setFillColor(HexColor("#7aa2ff")); c.setFont("Helvetica-Bold",22)
                    c.drawString(2*cm, H-2.5*cm, "ARIA — Strategic Intelligence Report")
                    c.setFillColor(HexColor("#dbe7ff")); c.setFont("Helvetica",10)
                    c.drawString(2*cm, H-3.2*cm, f"Sector: {sector}  |  Confidence: {agent.confidence_level:.1f}%  |  Generated: {datetime.now():%Y-%m-%d %H:%M}")
                    text = c.beginText(2*cm, H-4.2*cm); text.setFont("Helvetica",11); text.setFillColor(HexColor("#e6edf7"))
                    text.textLine("Executive Summary")
                    text.setFont("Helvetica",10); text.setFillColor(HexColor("#cfe0ff"))
                    for line in textwrap.wrap(agent.current_analysis.get("summary",""), 95): text.textLine(line)
                    text.textLine(""); text.setFont("Helvetica",11); text.setFillColor(HexColor("#e6edf7")); text.textLine("Insights")
                    for ins in agent.current_analysis.get("insights") or []:
                        text.setFont("Helvetica-Bold",10); text.setFillColor(HexColor("#7aa2ff")); text.textLine(f"• {ins.title} [{ins.category}]")
                        text.setFont("Helvetica",10); text.setFillColor(HexColor("#cfe0ff"))
                        for line in textwrap.wrap(f"Impact {ins.impact_score}/10 | Conf {ins.confidence}% — {ins.description}", 95): text.textLine(line)
                        text.textLine("")
                    text.setFont("Helvetica",11); text.setFillColor(HexColor("#e6edf7")); text.textLine("Recommendations")
                    for i,r in enumerate(recos,1):
                        text.setFont("Helvetica",10); text.setFillColor(HexColor("#cfe0ff")); text.textLine(f"{i}. {r}")
                    c.drawText(text); c.showPage(); c.save(); buff.seek(0)
                    st.download_button("⬇️ Download PDF", data=buff, file_name=fn, mime="application/pdf")
                except Exception as e:
                    st.warning("Reportlab non dispo — téléchargement Markdown.")
                    md = f"# ARIA Report — {sector}\n\n**Confidence:** {agent.confidence_level:.1f}%\n\n## Executive Summary\n{agent.current_analysis.get('summary','')}\n\n## Insights\n" + \
                         "\n".join([f"- **{i.title}** [{i.category}] — Impact {i.impact_score}/10, Conf {i.confidence}%\n  {i.description}" for i in (agent.current_analysis.get('insights') or [])]) + \
                         "\n\n## Recommendations\n" + "\n".join([f"1. {r}" for r in recos])
                    st.download_button("⬇️ Download .md", md.encode("utf-8"), file_name="ARIA_report.md", mime="text/markdown")
        with c3:
            if st.button("🔔 Setup Alerts"):
                st.success("✅ Alerts enabled — ARIA will notify on major changes.")
