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
        self.set_text_color(0, 191, 255) # Bleu clair
        self.cell(0, 10, 'PROJET ARIA', 0, 1, 'L')
        self.set_font('helvetica', '', 12)
        self.set_text_color(230, 230, 230)
        self.cell(0, 8, 'Rapport d\'Analyse Stratégique', 0, 1, 'L')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title, color):
        self.set_font('helvetica', 'B', 14)
        self.set_fill_color(color[0], color[1], color[2])
        self.set_text_color(255,255,255)
        self.cell(0, 10, f'  {title}', 0, 1, 'L', True)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('helvetica', '', 12)
        self.set_text_color(230, 230, 230)
        self.multi_cell(0, 8, body)
        self.ln()

def get_aria_response(user_question):
    """Simule une réponse de l'agent IA basée sur des mots-clés."""
    user_question = user_question.lower()
    if "opportunité" in user_question:
        return "L'opportunité principale identifiée est l'expansion des services 'Buy Now, Pay Later' (BNPL) pour les petites et moyennes entreprises, un segment actuellement sous-exploité."
    elif "menace" in user_question or "risque" in user_question:
        return "La menace la plus significative est l'intensification de la régulation sur la protection des données (type RGPD), qui pourrait imposer des contraintes coûteuses en matière de conformité."
    elif "tendance" in user_question:
        return "Une tendance de fond est l'adoption croissante de l'IA générative pour créer des expériences client ultra-personnalisées, ce qui redéfinit les attentes du marché."
    else:
        return "Je suis programmé pour répondre à des questions sur les opportunités, menaces et tendances du secteur analysé. Pouvez-vous reformuler votre question ?"

def generate_report_pdf():
    """Génère un rapport PDF stylé."""
    pdf = PDF('P', 'mm', 'A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_fill_color(5, 8, 22) # Fond très sombre
    pdf.rect(0, 0, 210, 297, 'F')

    # Contenu
    pdf.chapter_title('1. Opportunites Cles', (52, 211, 153))
    pdf.chapter_body("- Expansion des services BNPL pour les TPE/PME: Marche a fort potentiel de croissance.\n- Integration de l'IA dans les outils de gestion financiere: Demande croissante pour l'automatisation.")
    
    pdf.chapter_title('2. Menaces Potentielles', (248, 113, 113))
    pdf.chapter_body("- Intensification de la regulation RGPD: Risque de couts de conformite eleves et de sanctions.\n- Concurrence accrue des GAFAM: Arrivee d'acteurs majeurs avec des solutions integrees.")

    pdf.chapter_title('3. Recommandations Strategiques', (96, 165, 250))
    pdf.chapter_body("- Developper un partenariat strategique avec une neo-banque pour offrir des solutions BNPL B2B.\n- Investir dans une R&D axee sur l'IA pour maintenir un avantage concurrentiel.")

    pdf.ln(10)
    pdf.set_font('helvetica', 'I', 10)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 10, f'Rapport genere le {time.strftime("%d/%m/%Y a %H:%M:%S")}', 0, 1, 'C')
    
    return pdf.output()

# --- INJECTION DU CSS PERSONNALISÉ (THÈME HAUT CONTRASTE)---
CSS_CODE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700&family=Orbitron:wght@400;700&display=swap');

    :root {
        --bg-color: #050816; /* Fond bleu très sombre, presque noir */
        --card-bg-color: rgba(20, 25, 50, 0.85); /* Cartes plus opaques pour la lisibilité */
        --text-color: #FFFFFF; /* Texte blanc pur */
        --text-color-light: #bdc3c7;
        --border-color: rgba(255, 255, 255, 0.2);
        --glow-color: #00BFFF; /* Bleu électrique vif */
        --glow-color-accent: #FFD700; /* Jaune/Or pour l'accent */
    }
    
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 2rem;}
    header, footer { visibility: hidden; }

    body {
        font-family: 'Inter', sans-serif;
        background-color: var(--bg-color);
        color: var(--text-color);
        overflow: hidden;
    }

    #bg-canvas {
        position: fixed; top: 0; left: 0;
        width: 100%; height: 100%;
        z-index: -1; opacity: 0.3; /* Particules plus présentes */
    }

    .font-orbitron { font-family: 'Orbitron', sans-serif; }

    .glass-card {
        background: var(--card-bg-color);
        backdrop-filter: blur(8px); /* Flou réduit pour plus de clarté */
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
        padding: 1.5rem; border-radius: 1rem;
        height: 100%;
    }
    
    .glass-card:hover {
        border-color: var(--glow-color);
        box-shadow: 0 0 20px rgba(0, 191, 255, 0.2);
    }
    
    .agent-avatar {
        width: 160px; height: 160px; border-radius: 50%;
        position: relative;
        overflow: hidden;
        background: radial-gradient(circle at center, rgba(10, 10, 30, 1) 30%, transparent 70%),
                    conic-gradient(from 180deg at 50% 50%, var(--glow-color-accent) 0%, var(--glow-color) 50%, var(--glow-color-accent) 100%);
        box-shadow: 0 0 15px -5px var(--glow-color), 0 0 30px -5px var(--glow-color), 
                    inset 0 0 10px rgba(0, 191, 255, 0.5);
        animation: spin 10s linear infinite;
        margin: 1rem auto;
    }
    .agent-avatar::before {
        content: ''; position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        width: 70%; height: 70%;
        background: var(--bg-color); border-radius: 50%;
        box-shadow: inset 0 0 20px #000;
        z-index: 1;
    }
    .agent-avatar::after {
        content: ''; position: absolute;
        top: -5px; left: -5px; right: -5px; bottom: -5px;
        border-radius: 50%;
        border: 2px solid var(--glow-color);
        opacity: 0.5;
        animation: pulse-ring 3s infinite alternate;
    }
    
    .scanline {
        position: absolute;
        width: 100%;
        height: 4px;
        background: var(--glow-color);
        box-shadow: 0 0 20px 5px var(--glow-color);
        animation: scan 4s ease-in-out infinite;
        z-index: 2;
    }

    @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    @keyframes pulse-ring { from { transform: scale(1); opacity: 0.5; } to { transform: scale(1.1); opacity: 0.2; } }
    @keyframes scan {
        0% { top: -10%; }
        50% { top: 110%; }
        100% { top: -10%; }
    }
    
    .neon-border {
        border: 1px solid var(--glow-color);
        box-shadow: 0 0 5px var(--glow-color), inset 0 0 5px var(--glow-color);
        animation: pulse-border 3s infinite alternate;
    }
    @keyframes pulse-border {
        from { box-shadow: 0 0 8px -2px var(--glow-color), inset 0 0 8px -2px var(--glow-color); }
        to { box-shadow: 0 0 25px 3px var(--glow-color), inset 0 0 15px 3px var(--glow-color); }
    }
</style>
"""
st.markdown(CSS_CODE, unsafe_allow_html=True)


# --- HTML & JAVASCRIPT POUR LE FOND ANIMÉ ---
components.html("""
    <canvas id="bg-canvas"></canvas>
    <script>
        const canvas = document.getElementById('bg-canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        let particlesArray;
        function initParticles() {
            particlesArray = [];
            let n = (canvas.height * canvas.width) / 9000;
            for (let i = 0; i < n; i++) {
                particlesArray.push({
                    x: Math.random() * canvas.width, y: Math.random() * canvas.height,
                    dX: (Math.random() * 0.4) - 0.2, dY: (Math.random() * 0.4) - 0.2,
                    size: (Math.random() * 2) + 1
                });
            }
        }
        function animateParticles() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for (let p of particlesArray) {
                p.x += p.dX; p.y += p.dY;
                if (p.x > canvas.width || p.x < 0) p.dX = -p.dX;
                if (p.y > canvas.height || p.y < 0) p.dY = -p.dY;
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                const rand = Math.random();
                if (rand > 0.66) {
                    ctx.fillStyle = 'rgba(0, 191, 255, 0.8)'; // Blue
                } else if (rand > 0.33) {
                    ctx.fillStyle = 'rgba(255, 215, 0, 0.8)'; // Yellow/Gold
                } else {
                    ctx.fillStyle = 'rgba(230, 230, 250, 0.7)'; // White
                }
                ctx.fill();
            }
            requestAnimationFrame(animateParticles);
        }
        window.addEventListener('resize', () => { canvas.width = window.innerWidth; canvas.height = window.innerHeight; initParticles(); });
        initParticles();
        animateParticles();
    </script>
""", height=0, width=0)


# --- CORPS DE L'APPLICATION ---

# Header
st.markdown("""
<div class="glass-card" style="margin-bottom: 1rem;">
    <h1 class="font-orbitron" style="font-size: 2.25rem; font-weight: bold; color: var(--text-color); letter-spacing: 0.1em; margin: 0;">
        PROJET <span style="color: var(--glow-color); text-shadow: 0 0 15px var(--glow-color);">ARIA</span>
    </h1>
    <p style="color: var(--text-color-light); margin: 0;">Autonomous Research & Intelligence Agent 🤖</p>
</div>
""", unsafe_allow_html=True)


# Main Dashboard
col1, col2, col3 = st.columns(3)

# Colonne 1: Contrôles & Stack
with col1:
    with st.container(border=False):
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("""<h2 class="font-orbitron" style="font-size: 1.25rem; font-weight: bold; color: var(--text-color); border-bottom: 2px solid var(--glow-color); padding-bottom: 0.5rem; margin-bottom: 1rem;">🎛️ Panneau de Contrôle</h2>""", unsafe_allow_html=True)
        
        st.download_button(
            label="📄 Télécharger le Rapport PDF",
            data=generate_report_pdf(),
            file_name="rapport_strategique_ARIA.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        
        autonomous_mode = st.toggle("Mode autonome", help="ARIA relance l’analyse toutes les X heures et prévient si les insights changent.")
        if autonomous_mode:
            st.info("Mode autonome activé. ARIA surveille le secteur en arrière-plan.", icon="🛰️")

        st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
        
        st.markdown("""<h2 class="font-orbitron" style="font-size: 1.25rem; font-weight: bold; color: var(--text-color); border-bottom: 2px solid var(--glow-color-accent); padding-bottom: 0.5rem; margin-bottom: 1rem;">🛠️ Stack Technique</h2>""", unsafe_allow_html=True)
        st.markdown("""
        <ul style="list-style: none; padding: 0; font-size: 0.9rem;">
            <li><b>Frontend:</b> Streamlit + CSS/JS</li>
            <li><b>Backend:</b> Python + FPDF</li>
            <li><b>Dataviz:</b> Chart.js (via JS)</li>
            <li><b>IA Logic:</b> Simulation Python</li>
        </ul>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# Colonne 2: Simulation IA
with col2:
    st.markdown("""
    <div class="glass-card" style="text-align: center;">
        <h2 class="font-orbitron" style="font-size: 1.25rem; font-weight: bold; color: var(--text-color);">🧠 Simulation Agent IA</h2>
        <div class="agent-avatar">
            <div class="scanline"></div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; width: 100%; margin-top: 1rem;">
            <div class="glass-card" style="padding: 0.75rem">
                <div class="font-orbitron" id="neural-activity" style="font-size: 1.875rem; color: var(--glow-color); font-weight: bold;">1.38</div>
                <div style="font-size: 0.7rem; color: var(--text-color-light); text-transform: uppercase;">Activité Neuronale</div>
                <canvas id="neural-chart" height="30" class="w-full mt-2"></canvas>
            </div>
            <div class="glass-card" style="padding: 0.75rem">
                <div class="font-orbitron" id="confidence-score" style="font-size: 1.875rem; color: var(--glow-color-accent); font-weight: bold;">92.7%</div>
                <div style="font-size: 0.7rem; color: var(--text-color-light); text-transform: uppercase;">Score de Confiance</div>
                <div style="width: 100%; background: #374151; border-radius: 999px; height: 6px; margin-top: 10px;">
                    <div id="confidence-bar" style="background: var(--glow-color-accent); height: 6px; border-radius: 999px; width: 92.7%; transition: width 0.5s ease;"></div>
                </div>
            </div>
        </div>
        <h3 class="font-orbitron" style="font-size: 1.125rem; color: var(--text-color); margin-top: 1rem; margin-bottom: 0.5rem; text-align: left;">Processus de Pensée...</h3>
        <div id="thinking-process" class="glass-card" style="height: 120px; overflow-y: auto; text-align: left; padding: 1rem; font-size: 0.875rem;"></div>
    </div>
    """, unsafe_allow_html=True)

# Colonne 3: Insights & Chat
with col3:
    st.markdown("""
    <div class="glass-card">
        <h2 class="font-orbitron" style="font-size: 1.25rem; font-weight: bold; color: var(--text-color); border-bottom: 2px solid var(--glow-color); padding-bottom: 0.5rem; margin-bottom: 1rem;">✨ Insights Stratégiques</h2>
        <div style="display: flex; flex-direction: column; gap: 0.75rem;">
            <div class="glass-card neon-border" style="--glow-color: #34d399;">
                <h3 style="font-weight: bold; font-size: 1.1rem; color: #6ee7b7;">Opportunités</h3>
                <p style="font-size: 0.8rem; color: var(--text-color); margin: 0;">Expansion des services BNPL pour les TPE/PME.</p>
            </div>
            <div class="glass-card neon-border" style="--glow-color: #f87171;">
                <h3 style="font-weight: bold; font-size: 1.1rem; color: #fca5a5;">Menaces</h3>
                <p style="font-size: 0.8rem; color: var(--text-color); margin: 0;">Intensification de la régulation RGPD.</p>
            </div>
        </div>
        <h2 class="font-orbitron" style="font-size: 1.25rem; font-weight: bold; color: var(--text-color); border-bottom: 2px solid var(--glow-color-accent); padding-bottom: 0.5rem; margin-top: 1.5rem; margin-bottom: 1rem;">🤖 Chat avec l'Agent</h2>
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
        with chat_container.chat_message("user"):
            st.markdown(prompt)

        with chat_container.chat_message("assistant"):
            with st.spinner("ARIA réfléchit..."):
                response = get_aria_response(prompt)
                st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# --- JAVASCRIPT POUR LES SIMULATIONS VISUELLES ---
thoughts_data = [
    { "state": 'INITIALIZING', "text": "Activation des protocoles d'analyse..." },
    { "state": 'THINKING', "text": "Définition du périmètre : FinTech & SaaS." },
    { "state": 'ANALYZING', "text": "Croisement des données de marché en cours..." },
    { "state": 'ANALYZING', "text": "Détection d'une anomalie positive (BNPL)..." },
    { "state": 'THINKING', "text": "Évaluation du risque réglementaire (RGPD)." },
    { "state": 'ANALYZING', "text": "Modélisation des scénarios de croissance." },
    { "state": 'COMPLETED', "text": "Synthèse des insights terminée." }
]
thoughts_json = json.dumps(thoughts_data)

components.html(f"""
<script>
    const thoughts = JSON.parse('{thoughts_json}');
    let thoughtIndex = 0;

    function runSimulations() {{
        const neuralEl = document.getElementById('neural-activity');
        const confidenceEl = document.getElementById('confidence-score');
        const confidenceBar = document.getElementById('confidence-bar');
        const thinkingEl = document.getElementById('thinking-process');
        const chartCanvas = document.getElementById('neural-chart');
        
        if (!neuralEl || !confidenceEl || !confidenceBar || !thinkingEl || !chartCanvas) return;

        let activityData = Array(20).fill(1.5);
        const chartCtx = chartCanvas.getContext('2d');

        function drawNeuralChart() {{
            if (!chartCtx) return;
            chartCtx.clearRect(0, 0, chartCanvas.width, chartCanvas.height);
            chartCtx.beginPath();
            chartCtx.moveTo(0, chartCanvas.height / 2);
            chartCtx.strokeStyle = 'rgba(0, 191, 255, 0.8)';
            chartCtx.lineWidth = 2;
            const sliceWidth = chartCanvas.width / (activityData.length - 1);
            activityData.forEach((v, i) => chartCtx.lineTo(i * sliceWidth, (1 - (v - 0.5) / 2) * chartCanvas.height));
            chartCtx.stroke();
        }}
        
        if(window.ariaSimulationInterval) clearInterval(window.ariaSimulationInterval);

        window.ariaSimulationInterval = setInterval(() => {{
            const newActivity = (Math.random() * 1.5 + 0.8);
            const newConfidence = (Math.random() * 10 + 90);
            neuralEl.textContent = newActivity.toFixed(2);
            confidenceEl.textContent = `${{newConfidence.toFixed(1)}}%`;
            confidenceBar.style.width = `${{newConfidence}}%`;
            
            activityData.push(newActivity);
            if(activityData.length > 20) activityData.shift();
            drawNeuralChart();

            if (thoughtIndex >= thoughts.length) {{
                 thoughtIndex = 0;
                 // CORRECTION ERREUR JAVASCRIPT: Remplacer innerHTML = ''
                 while (thinkingEl.firstChild) {{
                     thinkingEl.removeChild(thinkingEl.firstChild);
                 }}
            }}
            const thought = thoughts[thoughtIndex];
            
            const p = document.createElement('p');
            p.style.margin = '0 0 0.5rem 0';
            p.style.opacity = '0';
            p.style.transform = 'translateX(-20px)';
            p.style.transition = 'opacity 0.5s, transform 0.5s';
            p.textContent = `> ${{thought.text}}`;
            thinkingEl.appendChild(p);
            thinkingEl.scrollTop = thinkingEl.scrollHeight;
            setTimeout(() => {{ p.style.opacity = '1'; p.style.transform = 'translateX(0)'; }}, 50);
            thoughtIndex++;
        }}, 2000);
        drawNeuralChart();
    }}
    
    // Utiliser un observateur pour relancer la simulation si le DOM est modifié par Streamlit
    const observer = new MutationObserver((mutations) => {{
        for (const mutation of mutations) {{
            if (mutation.addedNodes.length > 0) {{
                const target = document.getElementById('neural-activity');
                if(target) {{
                    runSimulations();
                    observer.disconnect(); // Exécuter une seule fois
                    break;
                }}
            }}
        }}
    }});

    observer.observe(document.body, {{ childList: true, subtree: true }});
</script>
""", height=0)

