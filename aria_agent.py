import streamlit as st
import streamlit.components.v1 as components
import time
import json
from fpdf import FPDF
import base64
import random
from datetime import datetime
import asyncio
from dataclasses import dataclass

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Projet ARIA",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- STRUCTURES DE DONNÉES DE L'AGENT ---

@dataclass
class AgentThought:
    content: str
    timestamp: datetime
    confidence: float = 0.0

@dataclass
class MarketInsight:
    title: str
    description: str
    impact_score: float
    confidence: float
    category: str  # opportunity, threat, trend

# --- CLASSE DE L'AGENT ARIA ---

class ARIAAgent:
    """
    ARIA - Autonomous Research & Intelligence Agent
    Agent IA autonome pour l'analyse stratégique de marché
    """
    def __init__(self, language: str = "fr"):
        self.language = language
        self.status = "idle"
        self.thoughts = []
        self.current_analysis = None
        self.confidence_level = 0.0
        self.neural_activity = 0
        self.translations = {
            "fr": {
                "sectors": {
                    "FinTech": "Technologies Financières", "SaaS": "Logiciels en Service", "E-commerce": "Commerce Électronique"
                },
                "thoughts": [
                    "🔍 Initialisation des capteurs de marché...", "🧠 Activation des réseaux neuronaux sectoriels...",
                    "📊 Ingestion de sources de données temps réel...", "⚡ Traitement par algorithmes de deep learning...",
                    "🎯 Corrélation des signaux faibles détectés...", "📈 Modélisation prédictive des tendances...",
                    "🤖 Génération d'insights actionnables...", "✨ Synthèse stratégique finalisée"
                ]
            },
            "en": {
                "sectors": {
                    "FinTech": "Financial Technologies", "SaaS": "Software as a Service", "E-commerce": "Electronic Commerce"
                },
                "thoughts": [
                    "🔍 Initializing market sensors...", "🧠 Activating sectoral neural networks...",
                    "📊 Ingesting real-time data sources...", "⚡ Processing via deep learning algorithms...",
                    "🎯 Correlating detected weak signals...", "📈 Predictive modeling of trends...",
                    "🤖 Generating actionable insights...", "✨ Strategic synthesis completed"
                ]
            }
        }
        self.market_data = {
            "FinTech": {
                "fr": {
                    "summary": "Le secteur FinTech connaît une consolidation majeure avec l'émergence de super-apps et l'intégration massive de l'IA. Les régulations créent des opportunités.",
                    "insights": [
                        MarketInsight("IA Conversationnelle Bancaire", "L'intégration d'assistants IA représente une opportunité majeure.", 9.2, 87, "opportunity"),
                        MarketInsight("Durcissement Réglementaire", "De nouvelles régulations créent des barrières d'entrée mais favorisent les acteurs conformes.", 7.8, 91, "threat")
                    ]
                },
                "en": {
                    "summary": "The FinTech sector is experiencing major consolidation with the emergence of super-apps and massive AI integration. Regulations create opportunities.",
                    "insights": [
                        MarketInsight("Conversational Banking AI", "AI assistant integration in banking represents a major opportunity.", 9.2, 87, "opportunity"),
                        MarketInsight("Regulatory Tightening", "New regulations create entry barriers but favor compliant players.", 7.8, 91, "threat")
                    ]
                }
            }
        }

    def get_translation(self, key: str, subkey: str = None):
        if subkey:
            return self.translations[self.language].get(key, {}).get(subkey, subkey)
        return self.translations[self.language].get(key, key)

    async def activate(self, sector: str):
        self.status = "thinking"
        self.thoughts = []
        self.current_analysis = None
        self.neural_activity = random.randint(800, 900)
        
        thoughts_list = self.get_translation("thoughts")
        for i, thought_text in enumerate(thoughts_list):
            await asyncio.sleep(random.uniform(0.8, 1.2))
            self.thoughts.append(AgentThought(content=thought_text, timestamp=datetime.now(), confidence=random.uniform(70, 95)))
            self.neural_activity += random.randint(-30, 50)
            if i > 1: self.status = "analyzing"
            st.rerun()

        self.status = "completed"
        self.current_analysis = self.market_data.get(sector, {}).get(self.language, {})
        self.confidence_level = random.uniform(85, 95)
        st.rerun()

    def get_chat_response(self, user_question):
        user_question = user_question.lower()
        if self.current_analysis:
            insights = self.current_analysis.get("insights", [])
            if "opportunité" in user_question:
                opps = [i.description for i in insights if i.category == "opportunity"]
                return opps[0] if opps else "Aucune opportunité spécifique trouvée."
            elif "menace" in user_question:
                threats = [i.description for i in insights if i.category == "threat"]
                return threats[0] if threats else "Aucune menace spécifique trouvée."
        return "Je ne peux répondre qu'après une analyse complète. Veuillez activer l'agent."


class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 20); self.set_text_color(0, 191, 255)
        self.cell(0, 10, 'PROJET ARIA', 0, 1, 'L')
        self.set_font('helvetica', '', 12); self.set_text_color(230, 230, 230)
        self.cell(0, 8, 'Rapport d\'Analyse Stratégique', 0, 1, 'L'); self.ln(10)
    def footer(self):
        self.set_y(-15); self.set_font('helvetica', 'I', 8); self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    def chapter_title(self, title, color):
        self.set_font('helvetica', 'B', 14); self.set_fill_color(color[0], color[1], color[2])
        self.set_text_color(255,255,255); self.cell(0, 10, f'  {title}', 0, 1, 'L', True); self.ln(4)
    def chapter_body(self, body):
        self.set_font('helvetica', '', 12); self.set_text_color(230, 230, 230)
        self.multi_cell(0, 8, body); self.ln()

def generate_report_pdf(agent):
    pdf = PDF('P', 'mm', 'A4'); pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page(); pdf.set_fill_color(5, 8, 22); pdf.rect(0, 0, 210, 297, 'F')
    if agent.current_analysis:
        insights = agent.current_analysis.get("insights", [])
        opps = "\n".join([f"- {i.title}: {i.description}" for i in insights if i.category == "opportunity"])
        threats = "\n".join([f"- {i.title}: {i.description}" for i in insights if i.category == "threat"])
        pdf.chapter_title('1. Opportunites Cles', (52, 211, 153)); pdf.chapter_body(opps)
        pdf.chapter_title('2. Menaces Potentielles', (248, 113, 113)); pdf.chapter_body(threats)
    pdf.ln(10); pdf.set_font('helvetica', 'I', 10); pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 10, f'Rapport genere le {datetime.now().strftime("%d/%m/%Y a %H:%M:%S")}', 0, 1, 'C')
    return bytes(pdf.output())

# --- INJECTION DU CSS & JS ---
CSS_CODE = """<style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700&family=Orbitron:wght@400;700&display=swap');:root{--bg-color:#050816;--card-bg-color:rgba(20,25,50,0.9);--text-color:#FFFFFF;--text-color-light:#bdc3c7;--border-color:rgba(255,255,255,0.2);--glow-color:#00BFFF;--glow-color-accent:#FFD700;}#root>div:nth-child(1)>div>div>div>div>section>div{padding-top:2rem;}header,footer{visibility:hidden;}body{font-family:'Inter',sans-serif;background-color:var(--bg-color);color:var(--text-color);overflow:hidden;}#bg-canvas{position:fixed;top:0;left:0;width:100%;height:100%;z-index:-1;opacity:0.4;}.font-orbitron{font-family:'Orbitron',sans-serif;}.glass-card{background:var(--card-bg-color);backdrop-filter:blur(5px);-webkit-backdrop-filter:blur(5px);border:1px solid var(--border-color);transition:all 0.3s ease;padding:1.5rem;border-radius:1rem;height:100%;box-shadow:0 8px 32px 0 rgba(0,0,0,0.37);}.glass-card:hover{border-color:var(--glow-color);box-shadow:0 0 25px rgba(0,191,255,0.3);}.agent-avatar{width:160px;height:160px;border-radius:50%;position:relative;overflow:hidden;background:radial-gradient(circle at center,rgba(10,10,30,1) 30%,transparent 70%),conic-gradient(from 180deg at 50% 50%,var(--glow-color-accent) 0%,var(--glow-color) 50%,var(--glow-color-accent) 100%);box-shadow:0 0 15px -5px var(--glow-color),0 0 30px -5px var(--glow-color),inset 0 0 10px rgba(0,191,255,0.5);animation:spin 10s linear infinite;margin:1rem auto;}.agent-avatar::before{content:'';position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:70%;height:70%;background:var(--bg-color);border-radius:50%;box-shadow:inset 0 0 20px #000;z-index:1;}.agent-avatar::after{content:'';position:absolute;top:-5px;left:-5px;right:-5px;bottom:-5px;border-radius:50%;border:2px solid var(--glow-color);opacity:0.5;animation:pulse-ring 3s infinite alternate;}.scanline{position:absolute;width:100%;height:4px;background:var(--glow-color);box-shadow:0 0 20px 5px var(--glow-color);animation:scan 4s ease-in-out infinite;z-index:2;}@keyframes spin{from{transform:rotate(0deg);}to{transform:rotate(360deg);}}@keyframes pulse-ring{from{transform:scale(1);opacity:0.5;}to{transform:scale(1.1);opacity:0.2;}}@keyframes scan{0%{top:-10%;}50%{top:110%;}100%{top:-10%;}}.neon-border{border:1px solid var(--glow-color);box-shadow:0 0 5px var(--glow-color),inset 0 0 5px var(--glow-color);animation:pulse-border 3s infinite alternate;}@keyframes pulse-border{from{box-shadow:0 0 8px -2px var(--glow-color),inset 0 0 8px -2px var(--glow-color);}to{box-shadow:0 0 25px 3px var(--glow-color),inset 0 0 15px 3px var(--glow-color);}}.thought-bubble{background:rgba(20,25,50,0.9);border-left:3px solid var(--glow-color);padding:0.5rem 1rem;margin-bottom:0.5rem;border-radius:0.5rem;font-size:0.85rem;}</style>"""
st.markdown(CSS_CODE, unsafe_allow_html=True)
components.html("""<canvas id="bg-canvas"></canvas><script>const canvas=document.getElementById('bg-canvas'),ctx=canvas.getContext('2d');canvas.width=window.innerWidth;canvas.height=window.innerHeight;let particlesArray;function initParticles(){particlesArray=[];let n=canvas.height*canvas.width/9e3;for(let i=0;i<n;i++)particlesArray.push({x:Math.random()*canvas.width,y:Math.random()*canvas.height,dX:.4*Math.random()-.2,dY:.4*Math.random()-.2,size:2*Math.random()+1})}function animateParticles(){ctx.clearRect(0,0,canvas.width,canvas.height);for(let p of particlesArray){p.x+=p.dX,p.y+=p.dY,(p.x>canvas.width||p.x<0)&&(p.dX=-p.dX),(p.y>canvas.height||p.y<0)&&(p.dY=-p.dY),ctx.beginPath(),ctx.arc(p.x,p.y,p.size,0,2*Math.PI);const rand=Math.random();ctx.fillStyle=rand>.66?"rgba(0, 191, 255, 0.8)":rand>.33?"rgba(255, 215, 0, 0.8)":"rgba(230, 230, 250, 0.7)",ctx.fill()}requestAnimationFrame(animateParticles)}window.addEventListener('resize',()=>{canvas.width=window.innerWidth,canvas.height=window.innerHeight,initParticles()}),initParticles(),animateParticles();</script>""", height=0, width=0)

# --- CORPS DE L'APPLICATION ---
if 'agent' not in st.session_state:
    st.session_state.agent = ARIAAgent()
agent = st.session_state.agent

# Header
st.markdown("""<div class="glass-card" style="margin-bottom: 1rem;"><h1 class="font-orbitron" style="font-size: 2.25rem; font-weight: bold; color: var(--text-color); letter-spacing: 0.1em; margin: 0;">PROJET <span style="color: var(--glow-color); text-shadow: 0 0 15px var(--glow-color);">ARIA</span></h1><p style="color: var(--text-color-light); margin: 0;">Autonomous Research & Intelligence Agent 🤖</p></div>""", unsafe_allow_html=True)

# Main Dashboard
col1, col2, col3 = st.columns([1, 1.2, 1])

# Colonne 1: Contrôles
with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("""<h2 class="font-orbitron" style="font-size: 1.25rem; color: var(--text-color); border-bottom: 2px solid var(--glow-color); padding-bottom: 0.5rem; margin-bottom: 1rem;">🎛️ Panneau de Contrôle</h2>""", unsafe_allow_html=True)
    
    lang_map = {"🇫🇷 Français": "fr", "🇺🇸 English": "en"}
    lang_selection = st.selectbox("Langue / Language", options=list(lang_map.keys()))
    agent.language = lang_map[lang_selection]
    
    sectors = agent.get_translation("sectors")
    sector_selection = st.selectbox("Secteur Cible", options=list(sectors.keys()), format_func=lambda x: sectors[x])

    if agent.status in ["idle", "completed"]:
        if st.button("🚀 Activer ARIA", use_container_width=True):
            asyncio.run(agent.activate(sector_selection))
            st.rerun()
    else:
        st.button("⏹️ Analyse en cours...", disabled=True, use_container_width=True)
    
    st.download_button(label="📄 Télécharger le Rapport PDF", data=generate_report_pdf(agent), file_name="rapport_strategique_ARIA.pdf", mime="application/pdf", use_container_width=True, disabled=agent.status != "completed")
    st.markdown('</div>', unsafe_allow_html=True)

# Colonne 2: Simulation IA
with col2:
    st.markdown('<div class="glass-card" style="text-align: center;">', unsafe_allow_html=True)
    status_map = {"idle": "EN VEILLE", "thinking": "RÉFLEXION", "analyzing": "ANALYSE", "completed": "TERMINÉ"}
    st.markdown(f'<h2 class="font-orbitron" style="font-size: 1.25rem; color: var(--text-color);">🧠 Agent IA - Statut : {status_map.get(agent.status)}</h2>', unsafe_allow_html=True)
    st.markdown('<div class="agent-avatar"><div class="scanline"></div></div>', unsafe_allow_html=True)
    
    # Métriques
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.markdown(f"""<div class="glass-card" style="padding: 0.75rem"><div class="font-orbitron" style="font-size: 1.875rem; color: var(--glow-color);">{agent.neural_activity}</div><div style="font-size: 0.7rem; text-transform: uppercase;">Activité Neuronale</div></div>""", unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"""<div class="glass-card" style="padding: 0.75rem"><div class="font-orbitron" style="font-size: 1.875rem; color: var(--glow-color-accent);">{agent.confidence_level:.1f}%</div><div style="font-size: 0.7rem; text-transform: uppercase;">Score de Confiance</div></div>""", unsafe_allow_html=True)
    
    st.markdown('<h3 class="font-orbitron" style="font-size: 1.125rem; margin-top: 1rem; text-align: left;">Processus de Pensée...</h3>', unsafe_allow_html=True)
    thought_container = st.container(height=140)
    for thought in agent.thoughts:
        thought_container.markdown(f'<div class="thought-bubble">> {thought.content}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Colonne 3: Insights & Chat
with col3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("""<h2 class="font-orbitron" style="font-size: 1.25rem; color: var(--text-color); border-bottom: 2px solid var(--glow-color); padding-bottom: 0.5rem; margin-bottom: 1rem;">✨ Insights Stratégiques</h2>""", unsafe_allow_html=True)
    
    if agent.status == "completed" and agent.current_analysis:
        for insight in agent.current_analysis.get("insights", []):
            color = "#34d399" if insight.category == "opportunity" else "#f87171"
            st.markdown(f"""<div class="glass-card neon-border" style="--glow-color: {color}; margin-bottom: 0.75rem;"><h3 style="font-weight: bold; font-size: 1.1rem; color: {color};">{insight.title.upper()}</h3><p style="font-size: 0.8rem; margin:0;">{insight.description}</p></div>""", unsafe_allow_html=True)
    else:
        st.info("Les insights apparaîtront ici après l'analyse.", icon="💡")

    st.markdown("""<h2 class="font-orbitron" style="font-size: 1.25rem; margin-top: 1.5rem; color: var(--text-color); border-bottom: 2px solid var(--glow-color-accent); padding-bottom: 0.5rem; margin-bottom: 1rem;">🤖 Chat avec l'Agent</h2>""", unsafe_allow_html=True)
    
    chat_container = st.container(height=200)
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Posez-moi une question après l'analyse."}]

    for message in st.session_state.messages:
        with chat_container.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Votre question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container.chat_message("user"): st.markdown(prompt)
        with chat_container.chat_message("assistant"):
            with st.spinner("ARIA réfléchit..."): response = agent.get_chat_response(prompt)
            st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    st.markdown('</div>', unsafe_allow_html=True)

