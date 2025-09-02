# app.py — ARIA (définitif, lisible & futuriste)
# pip install streamlit plotly reportlab
import os, io, base64, asyncio, random, textwrap
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Optional

import streamlit as st
import plotly.graph_objects as go

# =============== CONFIG PAGE ===============
st.set_page_config(
    page_title="🤖 ARIA – AI Strategic Intelligence Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =============== THEME / CSS (FOND + LISIBILITÉ) ===============
CSS = """
<style>
/* Immersion (masque topbar/side) — désactive si tu veux */
header, footer, [data-testid="stToolbar"] { visibility: hidden; }

/* Palette forte lisible */
:root{
  --bg:#0b1120; --panel:#0f172a; --panel2:#111827;
  --txt:#ecf2ff; --muted:#b6c2e7;
  --blue:#3b82f6; --violet:#8b5cf6; --teal:#06b6d4; --green:#22c55e; --red:#ef4444; --amber:#f59e0b;
  --ring:rgba(59,130,246,.42);
}

/* Fond animé: halos + grille */
html, body, .main { background: var(--bg); color: var(--txt); }
.main::before{
  content:""; position:fixed; inset:0; pointer-events:none; opacity:.23; z-index:-1;
  background:
    radial-gradient(700px 300px at 16% 24%, rgba(139,92,246,.22), transparent 60%),
    radial-gradient(700px 300px at 80% 30%, rgba(6,182,212,.18), transparent 60%),
    linear-gradient(120deg, rgba(59,130,246,.10), rgba(139,92,246,.10), rgba(6,182,212,.10));
  background-size:200% 200%;
  animation: gradShift 20s ease-in-out infinite;
}
.main::after{
  content:""; position:fixed; inset:0; pointer-events:none; opacity:.18; z-index:-1;
  background-image: radial-gradient(circle at 24px 24px, rgba(122,162,255,.30) 1.2px, transparent 1.2px);
  background-size:48px 48px; animation: gridMove 26s linear infinite;
}
@keyframes gradShift { 0%,100%{background-position:0% 50%} 50%{background-position:100% 50%} }
@keyframes gridMove { 0%{transform:translate(0,0)} 100%{transform:translate(48px,48px)} }

/* Overlay lisible si image/GIF de fond est activé (ajout dynamique via Python) */

/* Cartes propres (zéro flou baveux) */
.card{
  background: var(--panel);
  border:1px solid var(--ring);
  border-radius:16px; padding:16px; margin:10px 0;
  box-shadow:0 10px 28px rgba(0,0,0,.35);
}

/* Titres: contraste + ombre nette */
h1,h2,h3,h4,h5,h6{
  color:#eef2ff !important;
  text-shadow:0 1px 0 rgba(0,0,0,.55);
  margin-top:0; margin-bottom:.35rem;
}

/* Badges */
.badge{ padding:4px 10px; border-radius:999px; font-weight:800; font-size:.78rem }
.b-green{ background:rgba(34,197,94,.16); color:#cffff0; border:1px solid rgba(34,197,94,.45) }
.b-blue { background:rgba(59,130,246,.16); color:#d7e6ff; border:1px solid rgba(59,130,246,.45) }
.b-red  { background:rgba(239,68,68,.16); color:#ffd6d6; border:1px solid rgba(239,68,68,.45) }

/* Boutons */
.stButton > button{
  background:linear-gradient(90deg, var(--blue), var(--teal)) !important; color:#061229 !important;
  border:none !important; border-radius:12px !important; font-weight:900 !important;
  box-shadow:0 12px 24px rgba(59,130,246,.35) !important;
}

/* Inputs lisibles */
.stSelectbox > div > div, .stTextInput input, .stNumberInput input, .stTextArea textarea{
  background:#0d162b !important; color:#ecf2ff !important; border-radius:10px !important;
  border:1px solid var(--ring) !important;
}

/* Pensées style Framer (slide/fade) */
.thought{
  border-left:5px solid var(--blue); background:#0d162b;
  border-radius:12px; padding:12px 14px; margin:10px 0;
  animation: fadeSlide .28s ease-out;
}
@keyframes fadeSlide{ from{opacity:0; transform:translateY(7px)} to{opacity:1; transform:translateY(0)} }

/* Insight cards avec glow net */
.insight.opportunity{ border:1px solid rgba(34,197,94,.55); box-shadow:0 0 14px rgba(34,197,94,.18); }
.insight.threat     { border:1px solid rgba(239,68,68,.55); box-shadow:0 0 14px rgba(239,68,68,.18); }
.insight.trend      { border:1px solid rgba(139,92,246,.55); box-shadow:0 0 14px rgba(139,92,246,.18); }

/* Light mode */
.light .card{ background:#ffffff; color:#0a1020; border-color:rgba(59,130,246,.28) }
.light body,.light .main{ background:#f6f8ff; color:#0a1020 }
.light h1,h2,h3,h4,h5,h6{ color:#0a1020 !important; text-shadow:none }
.light .thought{ background:#ffffff; border-left-color:#3b82f6 }

/* Footer */
.footer{ text-align:center; color:#b6c2e7; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

def set_background_image(url_or_path: str = "", overlay_opacity: float = 0.28):
    """Option: image/GIF perso en fond, avec overlay lisible."""
    if not url_or_path:
        return
    if url_or_path.startswith("http"):
        url = url_or_path
    else:
        if not os.path.exists(url_or_path): return
        with open(url_or_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        mime = "image/gif" if url_or_path.lower().endswith(".gif") else ("image/png" if url_or_path.lower().endswith(".png") else "image/jpeg")
        url = f"data:{mime};base64,{b64}"
    st.markdown(f"""
    <style>
    .main {{
      background-image:
        linear-gradient(rgba(11,17,32,{overlay_opacity}), rgba(11,17,32,{overlay_opacity})),
        url('{url}');
      background-size: cover; background-position: center; background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)

def toggle_light_mode(is_light: bool):
    st.markdown(
        "<script>document.documentElement.classList."
        + ("add" if is_light else "remove")
        + "('light')</script>",
        unsafe_allow_html=True,
    )

# =============== MODELES ===============
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

# =============== AGENT ===============
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
                "name":"ARIA","desc":"Autonomous Research & Intelligence Agent",
                "status_idle":"🤖 En veille — prêt à analyser",
                "status_thinking":"🧠 Réflexion stratégique…",
                "status_analyzing":"⚡ Analyse multi-dimensionnelle…",
                "status_completed":"✨ Mission accomplie — insights générés",
                "sectors":{"FinTech":"Technologies Financières","SaaS":"Logiciels en Service","E-commerce":"Commerce Électronique","AI":"Intelligence Artificielle"},
                "thoughts":[
                    "Initialisation des capteurs de marché…",
                    "Activation des réseaux neuronaux sectoriels…",
                    "Ingestion de 1 247 sources en temps réel…",
                    "Traitement par modèles de deep learning…",
                    "Corrélation des signaux faibles…",
                    "Modélisation prédictive des tendances…",
                    "Scan concurrentiel multi-axes…",
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
                "sectors":{"FinTech":"Financial Technologies","SaaS":"Software as a Service","E-commerce":"E-commerce","AI":"Artificial Intelligence"},
                "thoughts":[
                    "Initializing market sensors…","Activating sector neural nets…","Ingesting 1,247 live sources…",
                    "Processing via deep learning…","Correlating weak signals…","Predictive trend modeling…",
                    "Competitive multi-axis scan…","Generating actionable insights…","High-confidence synthesis."
                ]
            }
        }

        self.market_data = {
            "FinTech":{
                "fr":{
                    "summary":"La FinTech s’accélère (IA conversationnelle, DeFi institutionnelle, Super-apps) tandis que MiCA renforce la confiance et avantage les acteurs conformes.",
                    "insights":[
                        MarketInsight("IA Conversationnelle Bancaire","KYC & support augmentés, scoring temps réel.",9.5,91,"opportunity"),
                        MarketInsight("DeFi Institutionnelle","Tokenisation & paiements programmables.",8.8,87,"opportunity"),
                        MarketInsight("Super-apps Financières","Plateformes unifiées (paiement, crédit, épargne).",8.2,79,"trend"),
                        MarketInsight("Durcissement Réglementaire","MiCA/AML = barrières mais avantage aux conformes.",7.9,94,"threat")
                    ],
                    "reco":[
                        "Investir dans l’IA conversationnelle avant T2 2025",
                        "Anticiper MiCA 6–9 mois à l’avance",
                        "Recruter talents blockchain avant pénurie"
                    ]
                },
                "en":{
                    "summary":"FinTech accelerates (Conversational AI, Institutional DeFi, Super-apps) while MiCA raises trust and rewards compliance.",
                    "insights":[
                        MarketInsight("Conversational Banking AI","Augmented KYC/support, real-time scoring.",9.5,91,"opportunity"),
                        MarketInsight("Institutional DeFi","Tokenization & programmable payments.",8.8,87,"opportunity"),
                        MarketInsight("Financial Super-apps","Unified platforms (payments, credit, savings).",8.2,79,"trend"),
                        MarketInsight("Regulatory Tightening","MiCA/AML barriers yet rewards compliance.",7.9,94,"threat")
                    ],
                    "reco":[
                        "Invest in conversational AI before Q2 2025",
                        "Prepare MiCA 6–9 months ahead",
                        "Hire blockchain talent pre-shortage"
                    ]
                }
            },
            "AI":{
                "fr":{
                    "summary":"Agents autonomes, Edge AI et intégration entreprise portent la croissance.",
                    "insights":[
                        MarketInsight("Agents IA Autonomes","Copilotes métiers & orchestration d’outils.",9.8,96,"opportunity"),
                        MarketInsight("IA Enterprise","ROI à 18 mois via productivité & qualité.",9.4,89,"opportunity"),
                        MarketInsight("Edge AI","Traitement proche source: latence/coûts/privacy.",8.7,83,"trend"),
                        MarketInsight("Pénurie de Talents","+423% de demande senior.",9.2,94,"threat"),
                    ],
                    "reco":[
                        "Capitaliser sur les agents IA",
                        "Investir dans l’Edge AI (décentralisation)",
                        "Bâtir expertise AI Act & gouvernance",
                        "Acquérir des équipes IA avant l’explosion des coûts"
                    ]
                },
                "en":{
                    "summary":"Autonomous agents, Edge AI and enterprise integration fuel growth.",
                    "insights":[
                        MarketInsight("Autonomous AI Agents","Domain copilots & tool orchestration.",9.8,96,"opportunity"),
                        MarketInsight("Enterprise AI","18-month ROI via productivity/quality.",9.4,89,"opportunity"),
                        MarketInsight("Edge AI","Near-source processing gains.",8.7,83,"trend"),
                        MarketInsight("Talent Shortage","+423% senior demand.",9.2,94,"threat"),
                    ],
                    "reco":[
                        "Leverage sector agents",
                        "Invest in edge AI",
                        "Build AI Act compliance expertise",
                        "Acquire AI teams before cost explosion"
                    ]
                }
            }
        }

    def t(self,key): return self.translations[self.language].get(key,key)

    async def activate(self, sector:str):
        self.status="thinking"; self.thoughts=[]; self.analysis_progress=0.0
        self.neural_activity = random.randint(820, 1180)
        items = self.translations[self.language]["thoughts"]
        for i, base in enumerate(items):
            await asyncio.sleep(random.uniform(.35,.70))
            content = await maybe_llm_thought(base, self.language, sector)
            self.thoughts.append(AgentThought(content, datetime.now(), random.uniform(.86,.97)))
            self.analysis_progress = (i+1)/len(items)*100
            if i==3: self.status="analyzing"
        self.status="completed"
        self.current_analysis = self.market_data.get(sector,{}).get(self.language,{})
        self.confidence_level = float(random.uniform(88.0, 97.0))
        self.neural_activity += random.randint(-30, 60)

    def generate_confidence_gauge(self) -> go.Figure:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=float(self.confidence_level),
            title={'text':"Confidence", 'font':{'size':18, 'color':'#EAF0FF'}},
            number={'font':{'size':36, 'color':'#DCE6FF'}},
            gauge={
                'axis': {'range':[0,100], 'tickcolor':'#B6C2E7', 'tickwidth':1},
                'bar':  {'color':"#3b82f6", 'thickness':0.78},
                'steps':[
                    {'range':[0,60],  'color':"rgba(239,68,68,.25)"},
                    {'range':[60,85], 'color':"rgba(245,158,11,.25)"},
                    {'range':[85,100],'color':"rgba(34,197,94,.28)"}
                ],
                'threshold': {'line':{'color':"#8b5cf6",'width':5}, 'value':90}
            }
        ))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          height=320, margin=dict(l=12,r=12,t=40,b=10), font={'color':"#EAF0FF"})
        return fig

# =============== LLM (optionnel) ===============
async def maybe_llm_thought(base:str, lang:str, sector:str)->str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return base
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        prompt = (f"Lang={lang}. Expand into ONE concise sentence for sector {sector}. "
                  f"Concrete, with one metric if relevant. Thought: {base}")
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":"You are ARIA: concise, clear, technical."},
                      {"role":"user","content":prompt}],
            max_tokens=50, temperature=0.7)
        return resp.choices[0].message.content.strip()
    except Exception:
        return base

# =============== CHARTS ===============
def sparkline(series: List[float])->go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=series, mode="lines", line={'shape':'spline'}))
    fig.update_layout(
        height=120, margin=dict(l=0,r=0,t=0,b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis={'visible':False}, yaxis={'visible':False}
    )
    return fig

# =============== STATE INIT ===============
if "agent" not in st.session_state: st.session_state.agent = ARIAAgent("fr")
if "language" not in st.session_state: st.session_state.language = "fr"
if "neural_series" not in st.session_state: st.session_state.neural_series = [1.2,1.3,1.25,1.4,1.35,1.45]
if "chat" not in st.session_state: st.session_state.chat = []
if "last_run" not in st.session_state: st.session_state.last_run = None

agent: ARIAAgent = st.session_state.agent
agent.language = st.session_state.language

# =============== HEADER (TITRE + CONTROLES) ===============
top1, top2, top3, top4 = st.columns([1.8, 1, 1, 1.2])

with top1:
    st.markdown(f"""
    <div class="card" style="display:flex;align-items:center;gap:12px;">
      <div style="width:48px;height:48px;border-radius:12px;border:1px solid rgba(255,255,255,.2);
                  display:flex;align-items:center;justify-content:center;background:linear-gradient(120deg,#3b82f6,#8b5cf6)">🤖</div>
      <div>
        <h2 style="margin:0">{agent.t('name')} • {agent.t('desc')}</h2>
        <div style="color:#b6c2e7">🧠 Neural: {agent.neural_activity} • 📚 Sources: 1,247 • ⚡ Real-time</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with top2:
    lang = st.selectbox("🌐 Lang / Language", ["🇫🇷 Français","🇺🇸 English"])
    new_lang = "fr" if "Français" in lang else "en"
    if new_lang != st.session_state.language:
        st.session_state.language = new_lang
        st.rerun()

with top3:
    is_light = st.toggle("🌗 Light", value=False)
    toggle_light_mode(is_light)

with top4:
    BG_URL = st.text_input("🎞️ Fond (GIF/Photo URL)", value="", help="Optionnel: GIF/image en fond")
    set_background_image(BG_URL, overlay_opacity=0.28 if BG_URL else 0.0)

# Autonome: cadence
aux1, aux2 = st.columns([1,1])
with aux1:
    sectors = agent.translations[agent.language]["sectors"]
    sector = st.selectbox("🎯 Sector", list(sectors.keys()), format_func=lambda k: sectors[k])
with aux2:
    autonomous = st.toggle("🤖 Autonomous", value=False, help="Relance l’analyse périodiquement")
    every_hours = st.number_input("⏱️ Every (hours)", min_value=1, max_value=24, value=6, step=1)

# Auto-refresh UI si autonome
if autonomous:
    st.autorefresh(interval=30_000, key="autorefresh")  # 30s UI refresh (démo)
    last = st.session_state.last_run
    if (not last) or (datetime.now() - last > timedelta(hours=every_hours)):
        asyncio.run(agent.activate(sector))
        st.session_state.last_run = datetime.now()

# =============== LAYOUT PRINCIPAL ===============
left, right = st.columns([1, 2], vertical_alignment="top")

# ---- LEFT: Panel agent + actions + métriques + sparkline ----
with left:
    # Panel statut + progress
    st.markdown(f"""
    <div class="card" style="text-align:center">
      <div class="badge b-blue">{agent.t('status_'+agent.status)}</div>
      <div style="height:10px"></div>
      <div style="border:1px solid var(--ring);border-radius:12px;overflow:hidden">
        <div style="height:12px;width:{agent.analysis_progress:.1f}%;background:linear-gradient(90deg,#3b82f6,#06b6d4)"></div>
      </div>
      <div style="margin-top:6px;color:#b6c2e7">Progress: {agent.analysis_progress:.1f}%</div>
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

    # Mini métriques
    m1, m2 = st.columns(2)
    with m1:
        st.markdown(f"""<div class="card"><div>Neural Activity</div><div style="font-weight:900;font-size:22px">{agent.neural_activity}</div></div>""", unsafe_allow_html=True)
    with m2:
        conf_txt = f"{agent.confidence_level:.1f}%" if agent.confidence_level>0 else "—"
        st.markdown(f"""<div class="card"><div>Confidence</div><div style="font-weight:900;font-size:22px">{conf_txt}</div></div>""", unsafe_allow_html=True)

    # Sparkline live (neural series)
    new_val = max(0.8, min(2.2, st.session_state.neural_series[-1] + random.uniform(-0.1, 0.1)))
    st.session_state.neural_series.append(new_val)
    st.session_state.neural_series = st.session_state.neural_series[-40:]
    st.plotly_chart(sparkline(st.session_state.neural_series), use_container_width=True)

# ---- RIGHT: Pensées + Résultats + Jauge + Insights + Reco + Chat + Export ----
with right:
    # Thoughts process
    if agent.status != "idle" and agent.thoughts:
        st.markdown('<div class="card"><h3>🧠 Agent Thought Process</h3></div>', unsafe_allow_html=True)
        for th in agent.thoughts:
            st.markdown(f"""
            <div class="thought">
              <div style="display:flex;justify-content:space-between;align-items:center">
                <div>{th.content}</div>
                <div class="badge b-green">{th.confidence:.1%}</div>
              </div>
              <div style="color:#b6c2e7;font-size:.86rem;margin-top:4px">{th.timestamp.strftime("%H:%M:%S")}</div>
            </div>
            """, unsafe_allow_html=True)

    # Results
    if agent.current_analysis and agent.status == "completed":
        st.markdown(f"""
        <div class="card">
          <h3>📋 Executive Summary <span class="badge b-green" style="margin-left:6px">High confidence</span></h3>
          <div style="border:1px solid var(--ring);border-radius:12px;padding:14px;margin-top:6px;background:#0d162b">
            {agent.current_analysis.get("summary","")}
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="card"><h3 style="text-align:center">📈 Analysis Confidence</h3></div>', unsafe_allow_html=True)
        st.plotly_chart(agent.generate_confidence_gauge(), use_container_width=True)

        insights: List[MarketInsight] = agent.current_analysis.get("insights") or []
        if insights:
            st.markdown('<div class="card"><h3>🎯 Strategic Insights</h3></div>', unsafe_allow_html=True)
            def render(cat, label, bclass):
                st.markdown(f'<h4 style="margin:.4rem 0">{label}</h4>', unsafe_allow_html=True)
                for ins in [i for i in insights if i.category==cat]:
                    st.markdown(f"""
                    <div class="card insight {cat}">
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
            render("trend","📈 Emerging Trends","b-blue")

        recos = agent.current_analysis.get("reco") or []
        if recos:
            st.markdown('<div class="card"><h3>🧭 AI Strategic Recommendations</h3></div>', unsafe_allow_html=True)
            for i, rec in enumerate(recos, 1):
                st.markdown(f"""
                <div class="card" style="border-color:rgba(139,92,246,.45);box-shadow:0 0 14px rgba(139,92,246,.18)">
                    <div style="display:flex;gap:10px">
                        <div class="badge b-blue">{i}</div>
                        <div style="font-weight:700">{rec}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Mini-chat
        st.markdown('<div class="card"><h3>💬 Ask ARIA</h3></div>', unsafe_allow_html=True)
        q = st.text_input("Pose une question (tendance, risque, concurrence)…")
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
            color = "rgba(59,130,246,.35)" if m["role"]=="user" else "rgba(34,197,94,.35)"
            st.markdown(f"""<div class="card" style="border-color:{color}">
                <b>{who}</b> <span style="float:right;color:#b6c2e7">{m['time']}</span><div>{m['content']}</div></div>""",
                unsafe_allow_html=True)

        # Export PDF avec QR code
        st.markdown('<div class="card"><h3>📤 Export & Actions</h3></div>', unsafe_allow_html=True)
        e1, e2 = st.columns(2)
        with e1:
            if st.button("🧾 Export PDF"):
                try:
                    from reportlab.lib.pagesizes import A4
                    from reportlab.pdfgen import canvas
                    from reportlab.lib.units import cm
                    from reportlab.lib.colors import HexColor
                    from reportlab.graphics.barcode import qr
                    fn = f"ARIA_{sector}_{datetime.now():%Y%m%d_%H%M}.pdf"
                    buff = io.BytesIO()
                    c = canvas.Canvas(buff, pagesize=A4)
                    W,H=A4
                    # Fond
                    c.setFillColor(HexColor("#0b1120")); c.rect(0,0,W,H,stroke=0,fill=1)
                    # Titre
                    c.setFillColor(HexColor("#3b82f6")); c.setFont("Helvetica-Bold",22)
                    c.drawString(2*cm, H-2.5*cm, "ARIA — Strategic Intelligence Report")
                    c.setFillColor(HexColor("#eef2ff")); c.setFont("Helvetica",10)
                    c.drawString(2*cm, H-3.2*cm, f"Sector: {sector}  |  Confidence: {agent.confidence_level:.1f}%  |  Generated: {datetime.now():%Y-%m-%d %H:%M}")
                    # QR code (lien démo)
                    try:
                        code = qr.QrCodeWidget("https://share.streamlit.io/")  # remplace par ton lien démo
                        from reportlab.graphics.shapes import Drawing
                        bounds = code.getBounds()
                        d = Drawing(2.5*cm, 2.5*cm)
                        d.add(code)
                        renderPDF = __import__("reportlab.graphics.renderPDF", fromlist=["renderPDF"]).graphics.renderPDF
                        renderPDF.draw(d, c, W-4*cm, H-4.5*cm)
                    except Exception:
                        pass
                    # Contenu
                    text=c.beginText(2*cm, H-4.6*cm); text.setFont("Helvetica-Bold",12); text.setFillColor(HexColor("#eef2ff"))
                    text.textLine("Executive Summary"); text.setFont("Helvetica",10); text.setFillColor(HexColor("#d7e0ff"))
                    for line in textwrap.wrap(agent.current_analysis.get("summary",""), 95): text.textLine(line)
                    text.textLine(""); text.setFont("Helvetica-Bold",12); text.setFillColor(HexColor("#eef2ff")); text.textLine("Insights")
                    for ins in insights:
                        text.setFont("Helvetica-Bold",10); text.setFillColor(HexColor("#7aa2ff")); text.textLine(f"• {ins.title} [{ins.category}]")
                        text.setFont("Helvetica",10); text.setFillColor(HexColor("#d7e0ff"))
                        for line in textwrap.wrap(f"Impact {ins.impact_score}/10 | Conf {ins.confidence}% — {ins.description}", 95): text.textLine(line)
                        text.textLine("")
                    text.setFont("Helvetica-Bold",12); text.setFillColor(HexColor("#eef2ff")); text.textLine("Recommendations")
                    for i,r in enumerate(recos,1):
                        text.setFont("Helvetica",10); text.setFillColor(HexColor("#d7e0ff")); text.textLine(f"{i}. {r}")
                    c.drawText(text); c.showPage(); c.save(); buff.seek(0)
                    st.download_button("⬇️ Download PDF", data=buff, file_name=fn, mime="application/pdf")
                except Exception as e:
                    st.error(f"PDF error: {e}")

        with e2:
            if st.button("🔔 Setup Alerts"):
                st.success("✅ Alerts ON — ARIA te notifie si les insights changent.")

# =============== NOTE DE PROJET (Résumé exécutif) ===============
note_md = f"""
🧾 **NOTE DE PROJET — ARIA : Autonomous Research & Intelligence Agent**

Agent IA autonome pour l'analyse stratégique de marchés

**🎯 Fonctionnalités core**
- Agent IA autonome avec processus de pensée visible  
- Analyse sectorielle (FinTech, SaaS, E-commerce, AI)  
- Interface futuriste (glass + néon) avec animations  
- Multilingue FR/EN automatique  
- Visualisations temps réel (neural, confiance, métriques)  
- Insights (opportunités, menaces, tendances) + recommandations  
- Export automatique de rapports (PDF stylé + QR)  

**🛠️ Stack**
- Frontend → Streamlit + CSS/JS  
- Backend  → Python + Architecture d'agent  
- Dataviz  → Plotly  
- IA Logic → Processus décisionnel + scoring  
- Deploy   → Streamlit Cloud  

**🎨 Design & UX**
- Avatar/visuel qui pulse  
- Pensées en temps réel (slide/fade)  
- Graphiques confiance dynamiques  
- Arrière-plan animé (grille + halos)  
- Thème sombre/clair  

**🧠 Simulation**
- idle → thinking → analyzing → completed  
- Métriques neuronales évolutives  
- Scoring de confiance contextuel  
"""
st.markdown(f'<div class="card"><h3>🧾 Note de projet — Résumé exécutif</h3><div style="white-space:pre-wrap">{note_md}</div></div>', unsafe_allow_html=True)

# =============== FOOTER ===============
conf = f"{agent.confidence_level:.1f}%" if agent.confidence_level>0 else "—"
st.markdown(f"""
<div class="card footer">
  ARIA • Real-time Market Intelligence • Confidence: {conf} • Neural: {agent.neural_activity} • Sources: 1,247
</div>
""", unsafe_allow_html=True)
