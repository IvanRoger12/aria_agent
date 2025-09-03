import streamlit as st
import time
import random
from datetime import datetime
from dataclasses import dataclass
import plotly.graph_objects as go
from typing import Dict, List, Optional
from fpdf import FPDF

# --- Configuration de la Page ---
st.set_page_config(
    page_title="🤖 ARIA - AI Strategic Intelligence Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS (Identique, pas de changement nécessaire) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap');
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 25%, #3b82f6 50%, #1e40af 75%, #0f172a 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        color: #e2e8f0; font-family: 'Inter', sans-serif;
    }
    @keyframes gradientShift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 1rem; max-width: 1400px; }
    .glass-card { background: rgba(255, 255, 255, 0.08); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 20px; padding: 25px; margin: 15px 0; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4); }
    .premium-title { font-size: 3.5rem; font-weight: 900; font-family: 'Orbitron', sans-serif; background: linear-gradient(45deg, #60a5fa, #a78bfa, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; animation: titleGlow 3s ease-in-out infinite alternate; }
    @keyframes titleGlow { from { filter: drop-shadow(0 0 15px rgba(96, 165, 250, 0.8)); } to { filter: drop-shadow(0 0 30px rgba(167, 139, 250, 1)); } }
    .insight-card { background: rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 20px; margin: 12px 0; border-left: 4px solid; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
    .opportunity-card { border-left-color: #10b981; } .threat-card { border-left-color: #ef4444; } .trend-card { border-left-color: #8b5cf6; }
    .recommendation-bubble { display: flex; align-items: start; gap: 20px; background: rgba(139, 92, 246, 0.15); border-radius: 15px; padding: 20px; margin: 15px 0; border-left: 4px solid #8b5cf6; }
    .recommendation-number { background: linear-gradient(45deg, #8b5cf6, #ec4899); border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-weight: bold; font-size: 1.2rem; color: white; }
    .glass-card p, .insight-card p, .recommendation-bubble p { color: #f8fafc; } .glass-card h2, .glass-card h3, .glass-card h4, .insight-card h5 { color: white; }
    .typewriter-text { font-size: 2.2rem; font-weight: 700; color: white; min-height: 1.2em; }
    .capabilities-list { margin-top: 30px; display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; }
    .capability-item { padding: 10px 18px; background: linear-gradient(45deg, rgba(59,130,246,0.3), rgba(139,92,246,0.3)); border-radius: 25px; color: white; font-weight: 500; font-size: 0.9rem; }
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
</style>
""", unsafe_allow_html=True)

# --- Classes de Données ---
@dataclass
class MarketInsight:
    title: str
    description: str
    impact_score: float
    confidence: float
    category: str

# --- Classe PDF (inchangée) ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15); self.set_fill_color(15, 23, 42); self.set_text_color(255, 255, 255)
        self.cell(0, 15, 'STRATEGIC INTELLIGENCE REPORT - ARIA', 0, 1, 'C', True); self.ln(5)
    def footer(self):
        self.set_y(-15); self.set_font('Arial', 'I', 8); self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    def section_title(self, title):
        self.set_font('Arial', 'B', 12); self.set_fill_color(30, 64, 175); self.set_text_color(255, 255, 255)
        self.cell(0, 10, f' {title}', 0, 1, 'L', True); self.ln(4); self.set_text_color(0, 0, 0)
    def section_body(self, body):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 5, body.encode('latin-1', 'replace').decode('latin-1')); self.ln()

# --- Classe de l'Agent ARIA (Maintenant Multilingue) ---
class ARIAAgent:
    def __init__(self):
        self.status = "idle"
        self.current_analysis: Optional[Dict] = None
        self.confidence_level: float = 0.0
        
        # Dictionnaire centralisé pour toutes les traductions
        self.translations = {
            'fr': {
                "agent_desc": "Agent de Recherche et Intelligence Autonome",
                "status_idle": "En veille", "status_thinking": "Réflexion...", "status_analyzing": "Analyse...", "status_completed": "Terminé",
                "sectors": { "FinTech": "🏦 Technologies Financières", "HealthTech": "❤️ Technologies de la Santé", "SaaS": "☁️ Logiciels (SaaS)", "E-commerce": "🛒 Commerce Électronique", "PropTech": "🏠 Technologies Immobilières", "EdTech": "🎓 Technologies de l'Éducation" },
                "thoughts": [ "Initialisation...", "Activation des réseaux neuronaux...", "Ingestion des données...", "Traitement par algorithmes...", "Corrélation des signaux...", "Modélisation prédictive...", "Génération d'insights...", "Synthèse finale..." ],
                "activate_button": "🚀 ACTIVER ARIA", "analysis_sector": "🎯 Secteur d'Analyse",
                "welcome_title": "ARIA est prête à analyser le marché.", "welcome_subtitle": "Sélectionnez un secteur pour démarrer une exploration stratégique.",
                "welcome_caps": ["Intelligence de Marché", "Analyse Prédictive", "Identification d'Opportunités", "Rapports Stratégiques"],
                "summary_title": "📋 Synthèse Stratégique", "swot_title": "Matrice Stratégique (Impact / Confiance)",
                "insights_title": "⚡ Insights & Recommandations", "pdf_button": "📄 Télécharger le Rapport PDF",
            },
            'en': {
                "agent_desc": "Autonomous Research & Intelligence Agent",
                "status_idle": "On Standby", "status_thinking": "Thinking...", "status_analyzing": "Analyzing...", "status_completed": "Completed",
                "sectors": { "FinTech": "🏦 Financial Technologies", "HealthTech": "❤️ Health Technologies", "SaaS": "☁️ Software (SaaS)", "E-commerce": "🛒 E-commerce", "PropTech": "🏠 Property Technologies", "EdTech": "🎓 Education Technologies" },
                "thoughts": [ "Initializing...", "Activating neural networks...", "Ingesting real-time data...", "Processing via algorithms...", "Correlating weak signals...", "Predictive modeling...", "Generating actionable insights...", "Final synthesis..." ],
                "activate_button": "🚀 ACTIVATE ARIA", "analysis_sector": "🎯 Analysis Sector",
                "welcome_title": "ARIA is ready to analyze the market.", "welcome_subtitle": "Select a sector to begin a strategic exploration.",
                "welcome_caps": ["Market Intelligence", "Predictive Analysis", "Opportunity Identification", "Strategic Reports"],
                "summary_title": "📋 Executive Summary", "swot_title": "Strategic Matrix (Impact / Confidence)",
                "insights_title": "⚡ Key Insights & Recommendations", "pdf_button": "📄 Download PDF Report",
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
                "insights": [ MarketInsight("IA dans le secteur", f"L'intégration de l'IA pourrait débloquer un marché de {random.uniform(1.5, 5.0):.1f}B€.", 9.2, 88, "opportunity"), MarketInsight("Régulation Accrue", f"De nouvelles lois pourraient augmenter les coûts de 20%.", 7.8, 91, "threat"), MarketInsight("Hyper-personnalisation", f"Les clients exigent des expériences sur mesure.", 8.9, 84, "trend") ],
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
        self.status = "idle"; self.current_analysis = None; self.confidence_level = 0.0

    def generate_swot_chart(self, lang: str) -> go.Figure:
        # (Cette fonction reste la même, les textes sont déjà génériques ou iconiques)
        insights = self.current_analysis.get("insights", [])
        fig = go.Figure()
        opps = [i for i in insights if i.category == "opportunity"]
        thrs = [i for i in insights if i.category == "threat"]
        if opps: fig.add_trace(go.Scatter(x=[o.impact_score for o in opps], y=[o.confidence for o in opps], mode='markers+text', text=[f"💡 {o.title}" for o in opps], marker=dict(color='#10b981', size=15), name='Opportunities'))
        if thrs: fig.add_trace(go.Scatter(x=[t.impact_score for t in thrs], y=[t.confidence for t in thrs], mode='markers+text', text=[f"🚨 {t.title}" for t in thrs], marker=dict(color='#ef4444', size=15, symbol='diamond'), name='Threats'))
        fig.update_layout(title={'text': self.get_translation("swot_title", lang)}, xaxis_title="Impact", yaxis_title="Confidence (%)", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0.1)", font={'color': "white"}, legend=dict(font=dict(color='white')), xaxis=dict(range=[0, 10]), yaxis=dict(range=[50, 100]))
        return fig

    def generate_pdf_report(self, lang: str) -> bytes:
        pdf = PDF()
        pdf.add_page()
        analysis = self.current_analysis
        pdf.section_title("Executive Summary" if lang == 'en' else "Synthese Strategique")
        pdf.section_body(analysis["summary"])
        pdf.section_title("Key Insights" if lang == 'en' else "Insights Cles")
        for insight in analysis["insights"]:
            pdf.section_body(f"{insight.title} ({insight.category.upper()})\n{insight.description}\nImpact: {insight.impact_score}/10 | Confidence: {insight.confidence}% \n")
        pdf.section_title("Strategic Recommendations" if lang == 'en' else "Recommandations Strategiques")
        for i, rec in enumerate(analysis["recommendations"], 1):
            pdf.section_body(f"{i}. {rec}")
        return pdf.output(dest='S').encode('latin-1')

# --- Interface Principale ---
def main():
    # Initialisation de l'état de session
    if 'agent' not in st.session_state:
        st.session_state.agent = ARIAAgent()
    if 'language' not in st.session_state:
        st.session_state.language = 'fr'
    
    agent = st.session_state.agent
    lang = st.session_state.language

    # --- Header avec sélecteur de langue ---
    header_cols = st.columns([0.8, 0.2])
    with header_cols[0]:
        st.markdown(f"<div style='text-align: left; margin-left: 10%;'><h1 class='premium-title'>ARIA</h1><p style='color: #cbd5e1;'>{agent.get_translation('agent_desc', lang)}</p></div>", unsafe_allow_html=True)
    with header_cols[1]:
        lang_choice = st.selectbox("Language", ["🇫🇷 Français", "🇺🇸 English"], label_visibility="collapsed")
        new_lang = 'fr' if 'Français' in lang_choice else 'en'
        if new_lang != lang:
            st.session_state.language = new_lang
            st.rerun()

    # --- Layout ---
    col1, col2 = st.columns([0.4, 0.6])

    # --- Colonne 1 : Contrôles ---
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        sectors = agent.get_translation("sectors", lang)
        selected_sector_key = st.selectbox(agent.get_translation("analysis_sector", lang), list(sectors.keys()), format_func=lambda x: sectors[x])
        
        if st.button(agent.get_translation("activate_button", lang), use_container_width=True):
            agent.reset()
            st.session_state.running_analysis = True
            st.session_state.selected_sector = selected_sector_key
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Colonne 2 : Affichage ---
    with col2:
        results_placeholder = st.empty()

        # Logique de simulation de l'analyse
        if st.session_state.get("running_analysis", False):
            agent.status = "analyzing"
            thoughts = agent.get_translation("thoughts", lang)
            thoughts_html = f"<div class='glass-card'><h3>{agent.get_translation('status_analyzing', lang)}</h3>"
            for thought_text in thoughts:
                time.sleep(random.uniform(0.5, 0.8))
                thoughts_html += f"<div>{random.choice(['🔍', '🧠', '📊', '⚡'])} {thought_text}</div>"
                with results_placeholder.container():
                    st.markdown(thoughts_html + "</div>", unsafe_allow_html=True)
            
            agent.status = "completed"
            agent.current_analysis = agent.market_data[st.session_state.selected_sector][lang]
            agent.confidence_level = random.uniform(88, 97)
            st.session_state.running_analysis = False
            st.rerun()

        # Affichage des résultats après l'analyse
        elif agent.status == "completed":
            with results_placeholder.container():
                analysis = agent.current_analysis
                st.markdown(f"<div class='glass-card'><h3>{agent.get_translation('summary_title', lang)}</h3><p>{analysis['summary']}</p></div>", unsafe_allow_html=True)
                st.plotly_chart(agent.generate_swot_chart(lang), use_container_width=True)
                
                st.markdown(f"<div class='glass-card'><h3>{agent.get_translation('insights_title', lang)}</h3></div>", unsafe_allow_html=True)
                for insight in analysis["insights"]:
                    icon = {"opportunity": "💡", "threat": "🚨", "trend": "📊"}.get(insight.category)
                    st.markdown(f"<div class='insight-card {insight.category}-card'><h5>{icon} {insight.title}</h5><p>{insight.description}</p></div>", unsafe_allow_html=True)

                for i, rec in enumerate(analysis["recommendations"], 1):
                    st.markdown(f"<div class='recommendation-bubble'><div class='recommendation-number'>{i}</div><p>{rec}</p></div>", unsafe_allow_html=True)

                pdf_bytes = agent.generate_pdf_report(lang)
                st.download_button(label=agent.get_translation("pdf_button", lang), data=pdf_bytes, file_name="Report_ARIA.pdf", mime="application/pdf", use_container_width=True)

        # Page d'accueil dynamique
        else:
            with results_placeholder.container():
                st.markdown("<div class='glass-card' style='text-align: center; padding: 40px;'>", unsafe_allow_html=True)
                st.markdown(f"<h2 class='typewriter-text'>{agent.get_translation('welcome_title', lang)}</h2>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: #cbd5e1;'>{agent.get_translation('welcome_subtitle', lang)}</p>", unsafe_allow_html=True)
                
                capabilities = agent.get_translation("welcome_caps", lang)
                caps_html = "<div class='capabilities-list'>" + "".join([f"<div class='capability-item'>{cap}</div>" for cap in capabilities]) + "</div>"
                st.markdown(caps_html, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
