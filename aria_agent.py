import streamlit as st
import time
import random
from datetime import datetime
from dataclasses import dataclass
import plotly.graph_objects as go
from typing import Dict, List, Optional

# --- Configuration de la Page ---
st.set_page_config(
    page_title="🤖 ARIA - AI Strategic Intelligence Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS (Mise en forme que vous aimez, avec la correction pour les métriques) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 25%, #3b82f6 50%, #1e40af 75%, #0f172a 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        color: white;
        font-family: 'Inter', sans-serif;
    }
    @keyframes gradientShift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    
    #MainMenu, footer, header { visibility: hidden; }
    
    .block-container { padding-top: 2rem; max-width: 1400px; }
    
    .glass-card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 25px; margin: 15px 0; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
    .glass-card:hover { transform: translateY(-5px); box-shadow: 0 12px 40px rgba(59, 130, 246, 0.25); border-color: rgba(59, 130, 246, 0.4); }
    
    .agent-avatar { position: relative; width: 100px; height: 100px; margin: 20px auto; border-radius: 50%; background: conic-gradient(from 0deg, #3b82f6, #8b5cf6, #ec4899, #3b82f6); display: flex; align-items: center; justify-content: center; animation: rotate 10s linear infinite; }
    .agent-avatar.active { animation: rotate 2s linear infinite, pulse 1.5s ease-in-out infinite; box-shadow: 0 0 50px rgba(59, 130, 246, 0.8); }
    @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.1); } }
    .agent-core { width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(45deg, #1e40af, #3b82f6); display: flex; align-items: center; justify-content: center; font-size: 2rem; }
    
    .thought-bubble { background: rgba(59, 130, 246, 0.1); border-left: 4px solid #3b82f6; padding: 20px; margin-bottom: 15px; border-radius: 0 15px 15px 0; box-shadow: 0 5px 15px rgba(59, 130, 246, 0.1); }
    
    /* NOUVEAU : Correction pour rendre les valeurs des métriques en blanc */
    [data-testid="stMetricValue"] {
        color: white;
        font-family: 'Orbitron', monospace;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    }
    
    .stButton > button { background: linear-gradient(45deg, #3b82f6, #8b5cf6); color: white; border: none; border-radius: 12px; font-weight: 600; font-family: 'Inter', sans-serif; padding: 12px 30px; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3); text-transform: uppercase; letter-spacing: 1px; width: 100%; }
    .stButton > button:hover { transform: translateY(-3px) scale(1.02); box-shadow: 0 10px 25px rgba(59, 130, 246, 0.5); background: linear-gradient(45deg, #2563eb, #7c3aed); }
    
    .premium-title { font-size: 3.5rem; font-weight: 900; font-family: 'Orbitron', sans-serif; background: linear-gradient(45deg, #60a5fa, #a78bfa, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; text-shadow: none; animation: titleGlow 3s ease-in-out infinite alternate; }
    @keyframes titleGlow { from { filter: drop-shadow(0 0 15px rgba(96, 165, 250, 0.6)); } to { filter: drop-shadow(0 0 30px rgba(167, 139, 250, 0.9)); } }
    
    .status-indicator { display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 10px; animation: statusBlink 1.5s infinite; }
    .status-idle { background: #6b7280; } .status-thinking { background: #f59e0b; } .status-analyzing { background: #3b82f6; } .status-completed { background: #10b981; }
    @keyframes statusBlink { 0% { opacity: 1; box-shadow: 0 0 8px currentColor; } 50% { opacity: 0.5; box-shadow: none; } 100% { opacity: 1; box-shadow: 0 0 8px currentColor; } }
    
    .insight-card { background: rgba(255, 255, 255, 0.06); border-radius: 15px; padding: 20px; margin: 12px 0; border-left: 4px solid; transition: all 0.3s ease; }
    .insight-card:hover { transform: translateY(-3px) scale(1.01); background: rgba(255, 255, 255, 0.1); }
    .opportunity-card { border-left-color: #10b981; } .threat-card { border-left-color: #ef4444; } .trend-card { border-left-color: #8b5cf6; }
    
    .recommendation-bubble { display: flex; align-items: start; gap: 20px; background: rgba(139, 92, 246, 0.1); border-radius: 15px; padding: 20px; margin: 15px 0; border-left: 4px solid #8b5cf6; }
    .recommendation-number { background: linear-gradient(45deg, #8b5cf6, #ec4899); border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-weight: bold; font-size: 1.2rem; box-shadow: 0 0 15px rgba(139, 92, 246, 0.5); }

    @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    .welcome-capability { display: inline-block; background: rgba(255, 255, 255, 0.1); padding: 8px 15px; margin: 5px; border-radius: 15px; font-weight: 500; animation: fadeInUp 0.5s ease-out backwards; }
</style>
""", unsafe_allow_html=True)


# --- Data Classes ---
@dataclass
class MarketInsight:
    title: str
    description: str
    impact_score: float
    confidence: float
    category: str

# --- ARIA Agent Class (Finalisée) ---
class ARIAAgent:
    def __init__(self):
        self.status = "idle"
        self.current_analysis: Optional[Dict] = None
        self.confidence_level: float = 0.0
        self.neural_activity: int = 850
        
        self.translations = {
            'fr': {
                "agent_desc": "Agent de Recherche et Intelligence Autonome", "status_idle": "En veille", "status_thinking": "Réflexion...", "status_analyzing": "Analyse...", "status_completed": "Terminé",
                "sectors": { "FinTech": "🏦 Technologies Financières", "HealthTech": "❤️ Technologies de la Santé", "SaaS": "☁️ Logiciels (SaaS)", "E-commerce": "🛒 Commerce Électronique", "PropTech": "🏠 Technologies Immobilières", "EdTech": "🎓 Technologies de l'Éducation" },
                "thoughts": [ "Initialisation des capteurs...", "Activation des réseaux neuronaux...", "Ingestion des données...", "Traitement par algorithmes...", "Corrélation des signaux...", "Modélisation prédictive...", "Génération d'insights...", "Synthèse finale..." ],
                "activate_button": "🚀 ACTIVER ARIA", "stop_button": "⏹️ STOPPER L'AGENT",
                "analysis_sector_title": "🎯 Secteur d'Analyse",
                "welcome_message": "ARIA est prête à analyser le marché.", "welcome_capabilities": ["Intelligence de Marché", "Analyse Prédictive", "Identification d'Opportunités", "Synthèse Stratégique"],
                "agent_thoughts_title": "🧠 Pensées de l'Agent", "summary_title": "📋 Synthèse Stratégique", "insights_title": "⚡ Insights Clés", "recommendations_title": "🎯 Recommandations IA",
                "metrics_title": "📊 Métriques", "nodes": "Noeuds", "confidence": "Confiance", "spinner_text": "Analyse en cours..."
            },
            'en': {
                "agent_desc": "Autonomous Research & Intelligence Agent", "status_idle": "On Standby", "status_thinking": "Thinking...", "status_analyzing": "Analyzing...", "status_completed": "Completed",
                "sectors": { "FinTech": "🏦 Financial Technologies", "HealthTech": "❤️ Health Technologies", "SaaS": "☁️ Software (SaaS)", "E-commerce": "🛒 E-commerce", "PropTech": "🏠 Property Technologies", "EdTech": "🎓 Education Technologies" },
                "thoughts": [ "Initializing sensors...", "Activating neural networks...", "Ingesting data...", "Processing via algorithms...", "Correlating signals...", "Predictive modeling...", "Generating insights...", "Final synthesis..." ],
                "activate_button": "🚀 ACTIVATE ARIA", "stop_button": "⏹️ STOP AGENT",
                "analysis_sector_title": "🎯 Analysis Sector",
                "welcome_message": "ARIA is ready to analyze the market.", "welcome_capabilities": ["Market Intelligence", "Predictive Analysis", "Opportunity Identification", "Strategic Synthesis"],
                "agent_thoughts_title": "🧠 Agent Thoughts", "summary_title": "📋 Executive Summary", "insights_title": "⚡ Key Insights", "recommendations_title": "🎯 AI Recommendations",
                "metrics_title": "📊 Metrics", "nodes": "Nodes", "confidence": "Confidence", "spinner_text": "Analysis in progress..."
            }
        }
        self.market_data = self._generate_all_sector_data()

    def get_translation(self, key: str, lang: str) -> str:
        return self.translations[lang].get(key, f"<{key}>")

    def _generate_sector_data(self, sector_key: str, lang: str) -> Dict:
        name = self.get_translation("sectors", lang)[sector_key]
        if lang == 'fr':
            return {
                "summary": f"Le secteur {name} connaît une transformation majeure, tirée par l'IA et une demande accrue pour des solutions personnalisées.",
                "insights": [ MarketInsight("IA dans le secteur", f"L'intégration de l'IA pourrait débloquer un marché de {random.uniform(1.5, 5.0):.1f}B€.", 9.2, 88, "opportunity"), MarketInsight("Régulation Accrue", f"De nouvelles lois pourraient augmenter les coûts de conformité de 20%.", 7.8, 91, "threat"), MarketInsight("Hyper-personnalisation", f"Les clients exigent des expériences sur mesure.", 8.9, 84, "trend") ],
                "recommendations": [ "Investir dans une plateforme d'IA avant le T3 2026.", "Lancer un audit de conformité réglementaire.", "Développer un pilote de solution durable." ],
            }
        else: # English
            return {
                "summary": f"The {name} sector is undergoing a major transformation, driven by AI and an increased demand for personalized solutions.",
                "insights": [ MarketInsight("AI in the sector", f"AI integration could unlock a ${random.uniform(1.8, 5.8):.1f}B market.", 9.2, 88, "opportunity"), MarketInsight("Increased Regulation", f"New laws could increase compliance costs by 20%.", 7.8, 91, "threat"), MarketInsight("Hyper-personalization", f"Customers are demanding tailored experiences.", 8.9, 84, "trend") ],
                "recommendations": [ "Invest in an AI platform before Q3 2026.", "Initiate a regulatory compliance audit.", "Develop a sustainable solution pilot." ],
            }

    def _generate_all_sector_data(self) -> Dict:
        all_data = {}
        for lang in ['fr', 'en']:
            for key in self.get_translation("sectors", lang).keys():
                if key not in all_data: all_data[key] = {}
                all_data[key][lang] = self._generate_sector_data(key, lang)
        return all_data

    def reset(self):
        self.status = "idle"; self.current_analysis = None; self.confidence_level = 0.0; self.neural_activity = 850

# --- Interface Principale ---
def main():
    if 'agent' not in st.session_state:
        st.session_state.agent = ARIAAgent()
    if 'language' not in st.session_state:
        st.session_state.language = 'fr'
    
    agent = st.session_state.agent
    lang = st.session_state.language

    # --- Header avec sélecteur de langue ---
    header_cols = st.columns([0.85, 0.15])
    with header_cols[0]:
        st.markdown(f"<div style='text-align: center;'><h1 class='premium-title'>ARIA</h1><p style='color: #cbd5e1; font-size: 1.3rem;'>{agent.get_translation('agent_desc', lang)}</p></div>", unsafe_allow_html=True)
    with header_cols[1]:
        lang_choice = st.selectbox("Language", ["🇫🇷 Français", "🇺🇸 English"], index=0 if lang == 'fr' else 1, label_visibility="collapsed")
        new_lang = 'fr' if 'Français' in lang_choice else 'en'
        if new_lang != lang:
            st.session_state.language = new_lang
            st.rerun()

    # --- Layout ---
    col1, col2 = st.columns([0.4, 0.6])

    with col1: # Colonne de gauche (Contrôles)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        avatar_class = "agent-avatar active" if agent.status != "idle" else "agent-avatar"
        st.markdown(f"<div style='text-align: center; margin-bottom: 25px;'><div class='{avatar_class}'><div class='agent-core'>🧠</div></div><div><span class='status-indicator status-{agent.status}'></span><span style='color: white; font-weight: 500;'>{agent.get_translation(f'status_{agent.status}', lang)}</span></div></div>", unsafe_allow_html=True)
        
        st.markdown(f"<h4 style='color: white; text-align: center;'>{agent.get_translation('analysis_sector_title', lang)}</h4>", unsafe_allow_html=True)
        sectors = agent.get_translation("sectors", lang)
        selected_sector = st.selectbox("Secteur", list(sectors.keys()), format_func=lambda x: sectors[x], label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)
        if agent.status in ["idle", "completed"]:
            if st.button(agent.get_translation("activate_button", lang), type="primary"):
                st.session_state.running_analysis = True
                st.session_state.selected_sector = selected_sector
                agent.reset(); agent.status = "thinking"
                st.rerun()
        else:
            if st.button(agent.get_translation("stop_button", lang)):
                st.session_state.running_analysis = False
                agent.reset()
                st.rerun()
        
        if agent.status != "idle":
            st.markdown(f"<h4 style='color: white; margin-top: 20px;'>{agent.get_translation('metrics_title', lang)}</h4>", unsafe_allow_html=True)
            m_col1, m_col2 = st.columns(2)
            m_col1.metric(agent.get_translation("nodes", lang), f"{agent.neural_activity}")
            m_col2.metric(agent.get_translation("confidence", lang), f"{agent.confidence_level:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2: # Colonne de droite (Affichage)
        results_placeholder = st.empty()

        if st.session_state.get("running_analysis", False):
            # --- Simulation avec Spinner ---
            with st.spinner(agent.get_translation("spinner_text", lang)):
                thoughts = agent.get_translation("thoughts", lang)
                thoughts_html = f"<div class='glass-card'><h3 style='color: white;'>{agent.get_translation('agent_thoughts_title', lang)}</h3>"
                for i, thought_text in enumerate(thoughts):
                    time.sleep(random.uniform(0.4, 0.7))
                    agent.neural_activity += random.randint(-40, 60)
                    agent.confidence_level = (i + 1) / len(thoughts) * 85 + random.uniform(-5, 5)
                    if i >= 2: agent.status = "analyzing"
                    
                    thought_html_item = f"<div class='thought-bubble' style='animation: fadeInUp 0.5s ease-out backwards;'>... {thought_text}</div>"
                    thoughts_html += thought_html_item
                    with results_placeholder.container():
                        st.markdown(thoughts_html + "</div>", unsafe_allow_html=True)
                
            agent.status = "completed"
            agent.current_analysis = agent.market_data[st.session_state.selected_sector][lang]
            st.session_state.running_analysis = False
            st.rerun()

        elif agent.status == "completed":
            # --- Affichage des résultats finaux ---
            with results_placeholder.container():
                analysis = agent.current_analysis
                st.markdown(f"<div class='glass-card' style='animation: fadeInUp 0.5s ease-out;'><h3>{agent.get_translation('summary_title', lang)}</h3><p style='font-size: 1.1rem;'>{analysis['summary']}</p></div>", unsafe_allow_html=True)
                
                st.markdown(f"<div class='glass-card'><h3 style='color: white;'>{agent.get_translation('insights_title', lang)}</h3>", unsafe_allow_html=True)
                for i, insight in enumerate(analysis["insights"]):
                    icon = {"opportunity": "💡", "threat": "🚨", "trend": "📊"}.get(insight.category)
                    st.markdown(f"<div class='insight-card {insight.category}-card' style='animation: fadeInUp {0.6 + i*0.1}s ease-out backwards;'><h5>{icon} {insight.title}</h5><p>{insight.description}</p></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown(f"<div class='glass-card'><h3 style='color: white;'>{agent.get_translation('recommendations_title', lang)}</h3>", unsafe_allow_html=True)
                for i, rec in enumerate(analysis["recommendations"]):
                    st.markdown(f"<div class='recommendation-bubble' style='animation: fadeInUp {0.8 + i*0.15}s ease-out backwards;'><div class='recommendation-number'>{i+1}</div><p style='margin: auto 0;'>{rec}</p></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        else:
            # --- Écran d'accueil animé ---
            with results_placeholder.container():
                st.markdown("<div class='glass-card' style='text-align: center; padding: 40px;'>", unsafe_allow_html=True)
                welcome_message_placeholder = st.empty()
                
                msg = agent.get_translation('welcome_message', lang)
                displayed_msg = ""
                for char in msg:
                    displayed_msg += char
                    welcome_message_placeholder.markdown(f"<h2 style='font-size: 2rem;'>{displayed_msg}</h2>", unsafe_allow_html=True)
                    time.sleep(0.05)
                
                time.sleep(0.5)
                capabilities = agent.get_translation("welcome_capabilities", lang)
                caps_html = "<div>" + "".join([f"<span class='welcome-capability' style='animation-delay: {i*0.2}s;'>{cap}</span>" for i, cap in enumerate(capabilities)]) + "</div>"
                st.markdown(caps_html, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
