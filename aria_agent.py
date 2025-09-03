import streamlit as st
import time
import random
from datetime import datetime
from dataclasses import dataclass, field
import plotly.graph_objects as go
from typing import Dict, List, Optional
from fpdf import FPDF # NOUVEAU : Pour la génération de PDF

# --- Configuration de la Page ---
st.set_page_config(
    page_title="🤖 ARIA - AI Strategic Intelligence Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS (Identique à la version précédente) ---
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
    .metric-value { font-size: 2.2rem; font-weight: 700; font-family: 'Orbitron', monospace; color: #60a5fa; text-shadow: 0 0 10px rgba(96, 165, 250, 0.5); }
    .stButton > button { background: linear-gradient(45deg, #3b82f6, #8b5cf6); color: white; border: none; border-radius: 12px; font-weight: 600; padding: 12px 30px; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3); text-transform: uppercase; letter-spacing: 1px; width: 100%; }
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
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
</style>
""", unsafe_allow_html=True)

# --- Classes de Données ---
@dataclass
class AgentThought:
    content: str
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class MarketInsight:
    title: str
    description: str
    impact_score: float
    confidence: float
    category: str

# --- Classe de Génération PDF ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.set_text_color(255, 255, 255)
        self.set_fill_color(15, 23, 42)
        self.cell(0, 15, '🧠 RAPPORT D\'INTELLIGENCE STRATÉGIQUE - ARIA', 0, 1, 'C', True)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def section_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(30, 64, 175)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f' {title}', 0, 1, 'L', True)
        self.ln(4)
        self.set_text_color(0, 0, 0)

    def section_body(self, body):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 5, body.encode('latin-1', 'replace').decode('latin-1'))
        self.ln()

    def insight_card(self, insight: MarketInsight):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 5, f"{insight.title} ({insight.category.capitalize()})", 0, 1)
        self.set_font('Arial', '', 9)
        self.multi_cell(0, 5, insight.description.encode('latin-1', 'replace').decode('latin-1'))
        self.set_font('Arial', 'I', 9)
        self.cell(0, 5, f"Impact: {insight.impact_score}/10 | Confiance: {insight.confidence}%", 0, 1)
        self.ln(2)

# --- Classe de l'Agent ARIA ---
class ARIAAgent:
    def __init__(self, language: str = "fr"):
        self.language = language
        self.status = "idle"
        self.thoughts: List[AgentThought] = []
        self.current_analysis: Optional[Dict] = None
        self.confidence_level: float = 0.0
        self.neural_activity: int = 850
        self.activity_history: List[int] = []
        
        self.translations = {
            "fr": {
                "agent_name": "ARIA", "agent_desc": "Agent de Recherche et Intelligence Autonome",
                "status_idle": "En veille", "status_thinking": "Réflexion...", "status_analyzing": "Analyse...", "status_completed": "Terminé",
                "sectors": {
                    "FinTech": "🏦 Technologies Financières", "HealthTech": "❤️ Technologies de la Santé", "SaaS": "☁️ Logiciels (SaaS)",
                    "E-commerce": "🛒 Commerce Électronique", "PropTech": "🏠 Technologies Immobilières", "EdTech": "🎓 Technologies de l'Éducation"
                },
                "thoughts": [
                    "Initialisation des capteurs...", "Activation des réseaux neuronaux...", "Ingestion de données temps réel...",
                    "Traitement par algorithmes...", "Corrélation des signaux faibles...", "Modélisation prédictive...",
                    "Génération d'insights...", "Synthèse stratégique..."
                ]
            }
            # Version anglaise omise pour la concision
        }
        self.market_data = self._generate_all_sector_data()

    def get_translation(self, key: str) -> str:
        return self.translations["fr"].get(key, key)

    def _generate_sector_data(self, sector_name: str) -> Dict:
        return {
            "summary": f"Le secteur {sector_name} est en pleine mutation, tiré par l'IA et une demande accrue pour des solutions hyper-personnalisées.",
            "insights": [
                MarketInsight(f"IA dans {sector_name}", f"L'intégration de l'IA pourrait débloquer un marché de {random.uniform(1.5, 5.0):.1f}B€.", 9.2, 88, "opportunity"),
                MarketInsight("Solutions Durables", "La demande pour des options écologiques crée une nouvelle niche.", 8.5, 75, "opportunity"),
                MarketInsight("Régulation Accrue", "De nouvelles lois pourraient augmenter les coûts de conformité de 20%.", 7.8, 91, "threat"),
                MarketInsight("Hyper-personnalisation", "Les clients exigent des expériences sur mesure.", 8.9, 84, "trend")
            ],
            "recommendations": [f"Investir dans une plateforme d'IA avant le T3 2026.", f"Lancer un audit de conformité réglementaire.", f"Développer un pilote de solution durable."],
            "key_metrics": {"Taux d'Adoption": f"{random.randint(15, 40)}%", "Croissance Annuelle (YoY)": f"{random.randint(5, 25)}%"},
            "key_players": ["Acteur Alpha", "Beta Corp", "Gamma Solutions"],
            "investment_trend": random.choice(["En forte hausse", "Stable", "Hausse modérée"])
        }

    def _generate_all_sector_data(self) -> Dict:
        all_data = {}
        for sector_key, sector_name in self.get_translation("sectors").items():
            all_data[sector_key] = self._generate_sector_data(sector_name.split(" ")[1])
        return all_data

    def reset(self):
        self.status = "idle"
        self.thoughts = []
        self.current_analysis = None
        self.confidence_level = 0.0
        self.neural_activity = 850
        self.activity_history = []

    def generate_swot_chart(self) -> go.Figure:
        insights = self.current_analysis.get("insights", [])
        fig = go.Figure()

        opps = [i for i in insights if i.category == "opportunity"]
        thrs = [i for i in insights if i.category == "threat"]

        fig.add_trace(go.Scatter(
            x=[i.impact_score for i in opps], y=[i.confidence for i in opps],
            mode='markers+text', text=[f"💡 {i.title}" for i in opps],
            marker=dict(color='#10b981', size=15, symbol='circle'), name='Opportunités',
            textposition="top right"
        ))
        fig.add_trace(go.Scatter(
            x=[i.impact_score for i in thrs], y=[i.confidence for i in thrs],
            mode='markers+text', text=[f"🚨 {i.title}" for i in thrs],
            marker=dict(color='#ef4444', size=15, symbol='diamond'), name='Menaces',
            textposition="bottom right"
        ))

        fig.update_layout(
            title={'text': "Matrice Stratégique (Impact / Confiance)", 'font': {'color': 'white'}},
            xaxis_title="Impact Stratégique", yaxis_title="Niveau de Confiance de l'IA (%)",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.05)",
            font={'color': "white"}, legend_title_text='Catégories'
        )
        return fig

    def generate_pdf_report(self, sector_name: str) -> bytes:
        pdf = PDF()
        pdf.add_page()
        
        # En-tête du rapport
        pdf.set_font('Arial', '', 11)
        pdf.cell(0, 6, f"Secteur Analysé : {sector_name}", 0, 1)
        pdf.cell(0, 6, f"Date du Rapport : {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1)
        pdf.cell(0, 6, f"Niveau de Confiance Global : {self.confidence_level:.1f}%", 0, 1)
        pdf.ln(10)

        # Sections
        analysis = self.current_analysis
        pdf.section_title("Synthèse Stratégique")
        pdf.section_body(analysis["summary"])

        pdf.section_title("Insights Clés")
        for insight in analysis["insights"]:
            pdf.insight_card(insight)

        pdf.section_title("Recommandations Stratégiques")
        for i, rec in enumerate(analysis["recommendations"], 1):
            pdf.section_body(f"{i}. {rec}")
        
        pdf.section_title("Métriques et Contexte du Marché")
        metrics = analysis['key_metrics']
        pdf.section_body(
            f"Tendances d'Investissement VC : {analysis['investment_trend']}\n"
            f"Acteurs Majeurs : {', '.join(analysis['key_players'])}\n"
            f"KPIs Notables : " + ", ".join([f"{k}: {v}" for k,v in metrics.items()])
        )

        return pdf.output(dest='S').encode('latin-1')

# --- Interface Principale ---
def main():
    if 'agent' not in st.session_state:
        st.session_state.agent = ARIAAgent()

    agent = st.session_state.agent

    st.markdown(f"<div style='text-align: center; margin-bottom: 30px;'><h1 class='premium-title'>ARIA</h1><p style='color: #cbd5e1;'>{agent.get_translation('agent_desc')}</p></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([0.35, 0.65])

    # --- COLONNE 1 : Panneau de Contrôle ---
    with col1:
        with st.container():
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            
            avatar_class = "agent-avatar active" if agent.status != "idle" else "agent-avatar"
            st.markdown(f"<div style='text-align: center; margin-bottom: 25px;'><div class='{avatar_class}'><div class='agent-core'>🧠</div></div><div><span class='status-indicator status-{agent.status}'></span><span style='font-weight: 500;'>{agent.get_translation(f'status_{agent.status}')}</span></div></div>", unsafe_allow_html=True)
            
            sectors = agent.get_translation("sectors")
            selected_sector = st.selectbox("🎯 Secteur d'Analyse", list(sectors.keys()), format_func=lambda x: sectors[x])

            # NOUVEAU : Slider de profondeur
            depth_map = {"Rapide": 0.5, "Normale": 1.0, "Profonde": 1.5}
            depth_choice = st.select_slider("⚙️ Profondeur d'Analyse", options=depth_map.keys(), value="Normale")
            analysis_speed = depth_map[depth_choice]

            st.markdown("<br>", unsafe_allow_html=True)
            if agent.status in ["idle", "completed"]:
                if st.button("🚀 ACTIVER ARIA"):
                    st.session_state.running_analysis = True
                    st.session_state.analysis_speed = analysis_speed
                    agent.reset()
                    agent.status = "thinking"
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        if agent.status == "completed":
             with st.container():
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown('<h4 style="color: white; text-align: center;">📥 Export du Rapport</h4>', unsafe_allow_html=True)
                pdf_bytes = agent.generate_pdf_report(sectors[selected_sector])
                st.download_button(
                    label="📄 Télécharger le Rapport PDF",
                    data=pdf_bytes,
                    file_name=f"Rapport_ARIA_{selected_sector}_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                st.markdown('</div>', unsafe_allow_html=True)

    # --- COLONNE 2 : Affichage ---
    with col2:
        results_placeholder = st.empty()

        if st.session_state.get("running_analysis", False):
            # ... (Logique de simulation identique à la version précédente, mais utilise st.session_state.analysis_speed pour le time.sleep)
            thoughts = agent.get_translation("thoughts")
            thoughts_html = '<div class="glass-card"><h3 style="color: white;">🧠 Pensées de l\'Agent</h3>'
            for i, thought_text in enumerate(thoughts):
                time.sleep(random.uniform(0.4, 0.8) * st.session_state.analysis_speed)
                if i >= 2: agent.status = "analyzing"
                agent.neural_activity += random.randint(-40, 60)
                thought = AgentThought(content=thought_text)
                thoughts_html += f"<div class='thought-bubble' style='animation: fadeInUp 0.5s ease-out backwards;'>{thought.content}</div>"
                with results_placeholder.container():
                    st.markdown(thoughts_html + '</div>', unsafe_allow_html=True)
            
            agent.status = "completed"
            agent.confidence_level = random.uniform(88, 97)
            agent.current_analysis = agent.market_data.get(selected_sector, {})
            st.session_state.running_analysis = False
            st.rerun()

        elif agent.status == "completed" and agent.current_analysis:
            with results_placeholder.container():
                analysis = agent.current_analysis
                st.markdown(f"<div class='glass-card' style='animation: fadeInUp 0.5s ease-out;'><h3>📋 Synthèse Stratégique</h3><p>{analysis['summary']}</p></div>", unsafe_allow_html=True)

                # NOUVEAU : Affichage des métriques enrichies
                st.markdown("<div class='glass-card' style='animation: fadeInUp 0.6s ease-out;'><h3>📊 Contexte du Marché</h3></div>", unsafe_allow_html=True)
                m_cols = st.columns(3)
                with m_cols[0]:
                    st.metric("📈 Tendance Invest. VC", analysis['investment_trend'])
                for i, (k, v) in enumerate(analysis['key_metrics'].items()):
                     with m_cols[i+1]:
                        st.metric(f"🔑 {k}", v)
                st.markdown(f"**Acteurs Majeurs:** {', '.join(analysis['key_players'])}")

                # NOUVEAU : Matrice SWOT
                st.plotly_chart(agent.generate_swot_chart(), use_container_width=True)

                # ... (Affichage des insights et recommandations comme avant) ...
                st.markdown('<div class="glass-card"><h3 style="color: white;">⚡ Insights Clés</h3></div>', unsafe_allow_html=True)
                for i, insight in enumerate(analysis.get("insights", [])):
                    icon = {"opportunity": "💡", "threat": "🚨", "trend": "📊"}.get(insight.category, "🔹")
                    st.markdown(f"<div class='insight-card {insight.category}-card'><h5>{icon} {insight.title}</h5><p>{insight.description}</p></div>", unsafe_allow_html=True)
                
                st.markdown('<div class="glass-card"><h3 style="color: white;">🎯 Recommandations IA</h3></div>', unsafe_allow_html=True)
                for i, rec in enumerate(analysis.get("recommendations", [])):
                    st.markdown(f"<div class='recommendation-bubble'><div class='recommendation-number'>{i+1}</div><p style='margin: auto 0;'>{rec}</p></div>", unsafe_allow_html=True)

        else:
            # NOUVEAU : Page d'accueil dynamique
            with results_placeholder.container():
                st.markdown("<div class='glass-card' style='text-align: center; padding: 40px;'>", unsafe_allow_html=True)
                
                title_placeholder = st.empty()
                subtitle_placeholder = st.empty()
                
                title_text = "ARIA est prête à analyser le marché."
                displayed_text = ""
                for char in title_text:
                    displayed_text += char
                    title_placeholder.markdown(f"<h2>{displayed_text}</h2>", unsafe_allow_html=True)
                    time.sleep(0.04)
                
                subtitle_placeholder.markdown("<p style='color: #94a3b8;'>Sélectionnez un secteur et configurez l'analyse pour commencer.</p>", unsafe_allow_html=True)
                
                st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 25px 0;'>", unsafe_allow_html=True)
                
                capabilities = ["🔍 Intelligence de Marché en Temps Réel", "⚡ Analyse Prédictive Avancée", "🎯 Identification d'Opportunités", "📊 Visualisation de Données Stratégiques"]
                cap_placeholder = st.empty()
                for i in range(len(capabilities) + 1):
                    caps_html = "".join([f"<div style='margin: 5px; padding: 8px 12px; background: rgba(59,130,246,0.2); border-radius: 10px; display: inline-block;'>{cap}</div>" for cap in capabilities[:i]])
                    cap_placeholder.markdown(f"<div style='text-align: center;'>{caps_html}</div>", unsafe_allow_html=True)
                    time.sleep(0.5)

                st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
