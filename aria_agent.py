import streamlit as st
import streamlit.components.v1 as components
import time
import json
from fpdf import FPDF
import base64

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Projet ARIA",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- LOGIQUE DE L'AGENT IA & RAPPORT PDF ---
class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 20)
        self.set_text_color(0, 191, 255)  # Bleu clair
        self.cell(0, 10, 'PROJET ARIA', 0, 1, 'L')
        self.set_font('helvetica', '', 12)
        self.set_text_color(230, 230, 230)
        self.cell(0, 8, "Rapport d'Analyse Stratégique", 0, 1, 'L')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title, color):
        self.set_font('helvetica', 'B', 14)
        self.set_fill_color(color[0], color[1], color[2])
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f'  {title}', 0, 1, 'L', True)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('helvetica', '', 12)
        self.set_text_color(230, 230, 230)
        self.multi_cell(0, 8, body)
        self.ln()

def get_aria_response(user_question):
    user_question = user_question.lower()
    if "opportunité" in user_question:
        return "L'opportunité principale identifiée est l'expansion des services BNPL pour les PME, un segment sous-exploité."
    elif "menace" in user_question or "risque" in user_question:
        return "La menace clé est l'intensification de la régulation RGPD, qui augmente les coûts de conformité."
    elif "tendance" in user_question:
        return "La tendance actuelle est l'adoption croissante de l'IA générative pour personnaliser l'expérience client."
    else:
        return "Je peux répondre aux questions sur les opportunités, menaces et tendances. Reformulez votre question."

def generate_report_pdf():
    pdf = PDF('P', 'mm', 'A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_fill_color(5, 8, 22)
    pdf.rect(0, 0, 210, 297, 'F')
    pdf.chapter_title("1. Opportunités Clés", (52, 211, 153))
    pdf.chapter_body("- Expansion des services BNPL\n- Intégration IA dans la finance")
    pdf.chapter_title("2. Menaces Potentielles", (248, 113, 113))
    pdf.chapter_body("- Renforcement RGPD\n- Concurrence accrue des GAFAM")
    pdf.chapter_title("3. Recommandations", (96, 165, 250))
    pdf.chapter_body("- Partenariat avec une néo-banque\n- Investir en R&D IA")
    return bytes(pdf.output())

# --- CSS : BLANC / JAUNE + LISIBILITÉ AMÉLIORÉE ---
CSS_CODE = """
<style>
:root {
    --bg-color: #050816;
    --card-bg-color: rgba(15, 20, 40, 0.95);
    --text-color: #ffffff;
    --text-color-light: #f5f5f5;
    --accent-yellow: #FFD700;
    --glow-color: #00BFFF;
}

body {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
}

h1, h2, h3, h4 {
    color: var(--text-color) !important;
    text-shadow: 0 0 6px rgba(0, 0, 0, 0.7);
    font-weight: 700;
}

.title-yellow {
    color: var(--accent-yellow) !important;
    text-shadow: 0 0 10px rgba(255, 215, 0, 0.8);
}

.glass-card {
    background: var(--card-bg-color);
    backdrop-filter: blur(2px);
    border: 1px solid rgba(255, 255, 255, 0.25);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.6);
    padding: 1.5rem; border-radius: 1rem;
}

.neon-border {
    border: 1px solid var(--glow-color);
    box-shadow: 0 0 12px var(--glow-color);
}
</style>
"""
st.markdown(CSS_CODE, unsafe_allow_html=True)

# --- FOND ANIMÉ AVEC PARTICULES ---
components.html("""
<canvas id="bg-canvas"></canvas>
<script>
const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
let particles = [];

function initParticles() {
    particles = [];
    let n = (canvas.height * canvas.width) / 9000;
    for (let i = 0; i < n; i++) {
        particles.push({
            x: Math.random() * canvas.width, y: Math.random() * canvas.height,
            dx: (Math.random() * 0.4) - 0.2, dy: (Math.random() * 0.4) - 0.2,
            size: (Math.random() * 2) + 1
        });
    }
}

function animateParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let p of particles) {
        p.x += p.dx; p.y += p.dy;
        if (p.x > canvas.width || p.x < 0) p.dx *= -1;
        if (p.y > canvas.height || p.y < 0) p.dy *= -1;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = Math.random() > 0.5 ? 'rgba(0, 191, 255, 0.7)' : 'rgba(255, 215, 0, 0.7)';
        ctx.fill();
    }
    requestAnimationFrame(animateParticles);
}

window.addEventListener('resize', () => {
    canvas.width = window.innerWidth; canvas.height = window.innerHeight;
    initParticles();
});
initParticles();
animateParticles();
</script>
""", height=0, width=0)

# --- INTERFACE ---
st.markdown("""
<div class="glass-card">
    <h1 class="font-orbitron">PROJET <span class="title-yellow">ARIA</span></h1>
    <p style="color: var(--text-color-light); margin: 0;">Autonomous Research & Intelligence Agent 🤖</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="title-yellow">🎛 Panneau de Contrôle</h2>', unsafe_allow_html=True)
    st.download_button("📄 Télécharger le Rapport PDF", data=generate_report_pdf(),
                       file_name="rapport_ARIA.pdf", mime="application/pdf")
    auto_mode = st.toggle("Mode autonome")
    if auto_mode:
        st.info("Mode autonome activé. ARIA surveille le secteur en arrière-plan.", icon="🛰️")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card" style="text-align: center;">
        <h2 class="title-yellow">🧠 Simulation Agent IA</h2>
        <div style="width:120px;height:120px;border-radius:50%;margin:0 auto;
        background:conic-gradient(from 180deg,#FFD700,#00BFFF);box-shadow:0 0 15px #00BFFF;"></div>
        <p style="margin-top:1rem;">Activité neuronale et score de confiance en temps réel.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="glass-card">
        <h2 class="title-yellow">✨ Insights Stratégiques</h2>
        <div class="glass-card neon-border">
            <h3 style="color:#6ee7b7;">💡 Opportunités</h3>
            <p>Expansion des services BNPL pour les PME.</p>
        </div>
        <div class="glass-card neon-border" style="margin-top:10px;">
            <h3 style="color:#fca5a5;">⚠️ Menaces</h3>
            <p>Renforcement des régulations RGPD.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

chat_container = st.container(height=230)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Bonjour. Posez-moi une question sur le secteur analysé."}]

for message in st.session_state.messages:
    with chat_container.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Votre question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_container.chat_message("assistant"):
        st.write(get_aria_response(prompt))
