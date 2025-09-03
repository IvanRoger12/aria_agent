"Intégrer l'IA conversationnelle avant Q2 2025 pour capturer l'avantage first-mover",
                        "Développer une stratégie de conformité MiCA 8 mois avant l'entrée en vigueur",
                        "Acquérir des fintechs spécialisées en DeFi avant la consolidation du marché"
                    ]
                }
            else:
                return {
                    "summary": f"The {sector_name} sector revolutionizes financial services with generative AI, neo-banks and institutional DeFi. MiCA regulation structures the European market.",
                    "insights": [
                        MarketInsight("Conversational Banking AI", "AI assistant integration generates +34% client engagement and represents a €3.2B market", 9.4, 91, "opportunity"),
                        MarketInsight("Institutional DeFi", "€45.8B in institutional assets under management adopt DeFi", 8.7, 85, "opportunity"),
                        MarketInsight("Financial Super-Apps", "Convergence towards integrated ecosystems", 8.2, 79, "trend"),
                        MarketInsight("MiCA Regulation", "+23% compliance costs but elimination of 40% of competitors", 7.9, 88, "threat")
                    ],
                    "recommendations": [
                        "Integrate conversational AI before Q2 2025 to capture first-mover advantage",
                        "Develop MiCA compliance strategy 8 months before enforcement",
                        "Acquire specialized DeFi fintechs before market consolidation"
                    ]
                }
        
        # Template générique pour les autres secteurs
        sector_info = self.sector_info[sector_key]
        return {
            "summary": f"Le secteur {sector_name} ({sector_info.market_size}, {sector_info.growth_rate} CAGR) connaît une transformation majeure avec l'IA et la durabilité comme moteurs principaux." if is_fr else f"The {sector_name} sector ({sector_info.market_size}, {sector_info.growth_rate} CAGR) is experiencing major transformation with AI and sustainability as key drivers.",
            "insights": [
                MarketInsight(f"IA dans {sector_name}" if is_fr else f"AI in {sector_name}", 
                             f"L'intégration IA pourrait débloquer {random.uniform(2, 5):.1f}B€ de marché" if is_fr else f"AI integration could unlock €{random.uniform(2, 5):.1f}B market", 
                             9.1, 86, "opportunity"),
                MarketInsight("Solutions Durables" if is_fr else "Sustainable Solutions", 
                             "Demande croissante pour options éco-responsables" if is_fr else "Growing demand for eco-responsible options", 
                             8.3, 79, "opportunity"),
                MarketInsight("Transformation Digitale" if is_fr else "Digital Transformation", 
                             "Accélération post-COVID maintenue" if is_fr else "Post-COVID acceleration maintained", 
                             8.7, 83, "trend"),
                MarketInsight("Régulation Accrue" if is_fr else "Increased Regulation", 
                             "Nouvelles lois sectorielles augmentent coûts +18%" if is_fr else "New sectoral laws increase costs +18%", 
                             7.4, 88, "threat")
            ],
            "recommendations": [
                f"Investir dans l'IA spécialisée {sector_name} avant T4 2025" if is_fr else f"Invest in specialized {sector_name} AI before Q4 2025",
                "Audit conformité réglementaire complet" if is_fr else "Complete regulatory compliance audit",
                "Stratégie durabilité différenciante" if is_fr else "Differentiating sustainability strategy"
            ]
        }
        
    def _generate_all_sector_data(self) -> Dict:
        """Génère des données complètes pour tous les secteurs."""
        all_data = {}
        sectors = list(self.sector_info.keys())
        
        for sector_key in sectors:
            sector_name_fr = self.get_translation("sectors", "fr")[sector_key]
            sector_name_en = self.get_translation("sectors", "en")[sector_key]
            
            all_data[sector_key] = {
                "fr": self._generate_sector_data(sector_name_fr, "fr", sector_key),
                "en": self._generate_sector_data(sector_name_en, "en", sector_key)
            }
            
        return all_data

    def reset(self):
        """Réinitialise l'agent à son état initial."""
        self.status = "idle"
        self.thoughts = []
        self.current_analysis = None
        self.confidence_level = 0.0
        self.neural_activity = 850
        self.activity_history = []
        if 'chat_messages' in st.session_state:
            st.session_state.chat_messages = []

    def generate_confidence_gauge(self) -> go.Figure:
        """Génère un graphique de confiance spectaculaire."""
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=self.confidence_level,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Niveau de Confiance IA", 'font': {'color': 'white', 'size': 20}},
            delta={'reference': 85, 'valueformat': '.1f'},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 2, 'tickcolor': "white"},
                'bar': {'color': "#3b82f6", 'thickness': 0.8},
                'bgcolor': "rgba(0,0,0,0.1)",
                'borderwidth': 3,
                'bordercolor': "rgba(59, 130, 246, 0.3)",
                'steps': [
                    {'range': [0, 70], 'color': 'rgba(239, 68, 68, 0.3)'},
                    {'range': [70, 85], 'color': 'rgba(245, 158, 11, 0.3)'},
                    {'range': [85, 100], 'color': 'rgba(16, 185, 129, 0.3)'}
                ],
                'threshold': {
                    'line': {'color': "#8b5cf6", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            },
            number={'font': {'color': 'white', 'size': 28}}
        ))
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "white"},
            height=280,
            margin=dict(t=50, b=30, l=30, r=30)
        )
        return fig

    def generate_activity_chart(self) -> go.Figure:
        """Génère un graphique spectaculaire de l'activité neuronale."""
        if not self.activity_history:
            self.activity_history = [self.neural_activity]
            
        fig = go.Figure()
        
        # Ligne principale
        fig.add_trace(go.Scatter(
            x=list(range(len(self.activity_history))), 
            y=self.activity_history,
            mode='lines+markers',
            line=dict(color='#3b82f6', width=4, shape='spline'),
            marker=dict(size=8, color='#60a5fa', line=dict(width=2, color='white')),
            fill='tonexty',
            fillcolor='rgba(59, 130, 246, 0.2)',
            name='Activité Neuronale'
        ))
        
        fig.update_layout(
            title={
                'text': "Activité Neuronale Temps Réel", 
                'font': {'color': 'white', 'size': 20},
                'x': 0.5
            },
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0.05)",
            font={'color': "white"},
            height=280,
            margin=dict(t=60, b=40, l=40, r=40),
            xaxis=dict(
                showgrid=True, 
                gridcolor='rgba(255, 255, 255, 0.1)',
                title="Temps",
                tickfont=dict(color='white')
            ),
            yaxis=dict(
                showgrid=True, 
                gridcolor='rgba(255, 255, 255, 0.1)',
                title="Noeuds Actifs",
                tickfont=dict(color='white')
            ),
            showlegend=False
        )
        return fig
        
    def chat_with_agent(self, message: str, sector: str) -> str:
        """Chat ultra intelligent avec l'agent."""
        message = message.lower()
        insights = self.current_analysis.get("insights", [])
        sector_info = self.sector_info.get(sector, None)
        
        # Réponses contextuelles avancées
        if any(keyword in message for keyword in ["opportunit", "opportunity", "chance"]):
            opps = [i for i in insights if i.category == "opportunity"]
            if opps and sector_info:
                return f"J'ai identifié {len(opps)} opportunités majeures dans {sector_info.name}. La plus prometteuse : **{opps[0].title}** avec un impact de {opps[0].impact_score}/10 et {opps[0].confidence}% de confiance. {opps[0].description}"
        
        if any(keyword in message for keyword in ["menace", "threat", "risk", "danger"]):
            threats = [i for i in insights if i.category == "threat"]
            if threats:
                return f"Attention ! Le risque principal identifié : **{threats[0].title}** (impact {threats[0].impact_score}/10). {threats[0].description} Je recommande une surveillance active."
        
        if any(keyword in message for keyword in ["tendance", "trend", "évolution"]):
            trends = [i for i in insights if i.category == "trend"]
            if trends:
                return f"Tendance clé détectée : **{trends[0].title}** avec {trends[0].confidence}% de certitude. {trends[0].description}"
        
        if any(keyword in message for keyword in ["recommand", "conseil", "advice"]):
            recs = self.current_analysis.get("recommendations", [])
            if recs:
                return f"Ma recommandation prioritaire : {recs[0]} Voulez-vous que je détaille les autres recommandations stratégiques ?"
        
        if any(keyword in message for keyword in ["marché", "market", "taille"]):
            if sector_info:
                return f"Le marché {sector_info.name} représente {sector_info.market_size} avec une croissance de {sector_info.growth_rate} CAGR. Leaders : {', '.join(sector_info.key_players[:3])}."
        
        # Réponse par défaut intelligente
        if sector_info:
            hot_trend = random.choice(sector_info.hot_trends)
            return f"Dans le secteur {sector_info.name}, je vois particulièrement {hot_trend} comme un axe stratégique majeur. Mon analyse révèle un potentiel de transformation significatif avec {self.confidence_level:.1f}% de confiance."
        
        return f"Basé sur mon analyse avec {self.confidence_level:.1f}% de confiance, le secteur {sector} présente des opportunités exceptionnelles en IA et durabilité. Que souhaitez-vous approfondir ?"

# --- Interface Principale Ultra ---
def main():
    # Initialisation de l'état de session
    if 'agent' not in st.session_state:
        st.session_state.agent = ARIAAgent()
    if 'language' not in st.session_state:
        st.session_state.language = 'fr'
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    if 'expanded_sectors' not in st.session_state:
        st.session_state.expanded_sectors = set()

    agent = st.session_state.agent
    agent.language = st.session_state.language

    # --- Header Ultra Spectaculaire ---
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 40px; position: relative;'>
        <h1 class='premium-title'>{agent.get_translation('agent_name')}</h1>
        <p style='color: #cbd5e1; font-size: 1.4rem; font-weight: 300; margin-top: 15px;'>{agent.get_translation('agent_desc')}</p>
        <div style='width: 100px; height: 2px; background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899); margin: 20px auto; border-radius: 1px;'></div>
    </div>
    """, unsafe_allow_html=True)

    # Sélecteur de langue élégant
    col_lang1, col_lang2, col_lang3 = st.columns([1, 2, 1])
    with col_lang2:
        lang_option = st.selectbox(
            "Language", 
            ["Français", "English"],
            key="language_selector"
        )
        new_language = "fr" if "Français" in lang_option else "en"
        if new_language != st.session_state.language:
            st.session_state.language = new_language
            st.rerun()

    # --- Layout Principal Ultra ---
    col1, col2 = st.columns([0.4, 0.6])

    # --- COLONNE 1 : Contrôle Agent + Secteurs ---
    with col1:
        # Panel de contrôle agent
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        # Avatar et Statut Ultra
        avatar_class = "agent-avatar active" if agent.status != "idle" else "agent-avatar"
        st.markdown(f"""
        <div style='text-align: center; margin-bottom: 30px;'>
            <div class='{avatar_class}'>
                <div class='agent-core'>🧠</div>
            </div>
            <h3 style='color: white; margin: 20px 0 10px 0; font-family: "Orbitron", sans-serif;'>{agent.get_translation("agent_name")}</h3>
            <div style='display: flex; align-items: center; justify-content: center; gap: 10px;'>
                <span class='status-indicator status-{agent.status}'></span>
                <span style='color: #e2e8f0; font-weight: 500; font-size: 0.95rem;'>{agent.get_translation(f"status_{agent.status}")}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Métriques temps réel
        if agent.status != "idle":
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.markdown(f"""
                <div style='text-align: center; padding: 15px;'>
                    <div class='metric-value'>{agent.neural_activity}</div>
                    <div style='color: #94a3b8; font-size: 0.85rem; font-weight: 500;'>Noeuds Neuronaux</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_m2:
                st.markdown(f"""
                <div style='text-align: center; padding: 15px;'>
                    <div class='metric-value'>{agent.confidence_level:.1f}%</div>
                    <div style='color: #94a3b8; font-size: 0.85rem; font-weight: 500;'>Niveau Confiance</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # --- SECTEURS AVEC BOUTONS D'ANALYSE ---
        st.markdown(f"<h3 style='color: white; text-align: center; margin: 30px 0 20px 0;'>Secteurs d'Analyse</h3>", unsafe_allow_html=True)
        
        sectors = agent.get_translation("sectors")
        selected_sector = None
        
        for sector_key, sector_name in sectors.items():
            sector_info = agent.sector_info[sector_key]
            
            # Carte de secteur
            st.markdown(f"""
            <div class='sector-card'>
                <div class='sector-header'>
                    <div style='display: flex; align-items: center;'>
                        <div class='sector-icon' style='background: linear-gradient(135deg, {sector_info.color}, {sector_info.color}80);'>
                            {sector_info.icon}
                        </div>
                        <div>
                            <h4 style='color: white; margin: 0; font-weight: 600;'>{sector_name}</h4>
                            <p style='color: #94a3b8; margin: 5px 0 0 0; font-size: 0.85rem;'>{sector_info.market_size} • {sector_info.growth_rate}</p>
                        </div>
                    </div>
                </div>
                
                <p style='color: #e2e8f0; margin-bottom: 15px; font-size: 0.9rem;'>{sector_info.description}</p>
                
                <div style='margin-bottom: 15px;'>
                    <h5 style='color: #60a5fa; margin-bottom: 8px; font-size: 0.9rem;'>Tendances Chaudes</h5>
                    <div style='display: flex; flex-wrap: wrap; gap: 6px;'>
                        {''.join([f'<span style="background: {sector_info.color}40; color: {sector_info.color}; padding: 4px 8px; border-radius: 12px; font-size: 0.75rem;">{trend}</span>' for trend in sector_info.hot_trends[:3]])}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Bouton d'activation pour ce secteur
            if st.button(f"🚀 Analyser {sector_name}", key=f"analyze_{sector_key}", type="secondary"):
                selected_sector = sector_key
                break
        
        # Bouton d'arrêt si analyse en cours
        if agent.status not in ["idle"]:
            if st.button("⏹️ STOPPER L'AGENT", key="stop_agent"):
                st.session_state.running_analysis = False
                agent.reset()
                st.rerun()
        
        # Graphiques en temps réel
        if agent.status == "completed":
            st.plotly_chart(agent.generate_confidence_gauge(), use_container_width=True, key="confidence_chart")
            st.plotly_chart(agent.generate_activity_chart(), use_container_width=True, key="activity_chart")

    # --- COLONNE 2 : Affichage des Résultats ---
    with col2:
        results_placeholder = st.empty()

        if selected_sector or st.session_state.get("running_analysis", False):
            if selected_sector:
                st.session_state.running_analysis = True
                st.session_state.selected_sector = selected_sector
                agent.reset()
                agent.status = "thinking"
            
            # --- SIMULATION DE L'ANALYSE EN DIRECT ---
            selected_sector = st.session_state.get("selected_sector", "FinTech")
            thoughts = agent.get_translation("thoughts")
            
            with results_placeholder.container():
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown('<h3 style="color: white; margin-bottom: 25px;">Flux de Pensées ARIA</h3>', unsafe_allow_html=True)
                
                thoughts_container = st.empty()
                thoughts_html = ""
                
                for i, thought_text in enumerate(thoughts):
                    time.sleep(random.uniform(1.0, 1.5))
                    
                    if i >= 3 and agent.status == "thinking":
                        agent.status = "analyzing"
                    
                    agent.neural_activity += random.randint(-50, 80)
                    agent.neural_activity = max(700, min(1000, agent.neural_activity))
                    agent.activity_history.append(agent.neural_activity)
                    agent.confidence_level = min((i + 1) / len(thoughts) * 95, 95)
                    
                    thought = AgentThought(content=thought_text)
                    agent.thoughts.append(thought)
                    
                    icon = ["🔍", "🧠", "📊", "⚡", "🎯", "📈", "🤖", "✨"][i] if i < 8 else "🤖"
                    
                    thought_item_html = f"""
                    <div class='thought-bubble'>
                        <div style='display: flex; align-items: start; gap: 20px;'>
                            <div style='background: linear-gradient(135deg, #3b82f6, #8b5cf6); 
                                        border-radius: 50%; width: 45px; height: 45px; 
                                        display: flex; align-items: center; justify-content: center;
                                        font-size: 1.4rem; flex-shrink: 0;'>
                                {icon}
                            </div>
                            <div style='flex: 1;'>
                                <p style='color: white; margin: 0 0 12px 0; font-weight: 500; line-height: 1.5;'>
                                    {thought.content}
                                </p>
                                <div style='display: flex; justify-content: space-between; align-items: center;'>
                                    <span style='color: #94a3b8; font-size: 0.8rem;'>
                                        {thought.timestamp.strftime("%H:%M:%S")}
                                    </span>
                                    <span style='background: rgba(59, 130, 246, 0.2); color: #60a5fa; 
                                                padding: 2px 8px; border-radius: 10px; font-size: 0.75rem;'>
                                        {agent.confidence_level:.1f}% confiance
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                    """
                    
                    thoughts_html += thought_item_html
                    
                    with thoughts_container.container():
                        st.markdown(thoughts_html, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            time.sleep(1)
            
            # Finalisation
            agent.status = "completed"
            agent.confidence_level = random.uniform(88, 97)
            agent.current_analysis = agent.market_data.get(selected_sector, {}).get(agent.language, {})
            st.session_state.running_analysis = False
            st.rerun()

        elif agent.status == "completed" and agent.current_analysis:
            # --- AFFICHAGE DES RÉSULTATS FINAUX ---
            with results_placeholder.container():
                # Synthèse exécutive
                st.markdown(f"""
                <div class='glass-card'>
                    <h3 style='color: white; margin-bottom: 20px;'>📋 Synthèse Stratégique</h3>
                    <p style='color: #e2e8f0; font-size: 1.1rem; line-height: 1.6;'>
                        {agent.current_analysis.get("summary", "")}
                    </p>
                    <div style='text-align: right; margin-top: 15px;'>
                        <span style='background: rgba(16, 185, 129, 0.2); color: #10b981; 
                                    padding: 8px 16px; border-radius: 20px; font-weight: 600;'>
                            {agent.confidence_level:.1f}% Confiance
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Insights avec onglets
                st.markdown('<div class="glass-card"><h3 style="color: white; margin-bottom: 25px;">Intelligence Stratégique</h3></div>', unsafe_allow_html=True)
                
                insights = agent.current_analysis.get("insights", [])
                opportunities = [i for i in insights if i.category == "opportunity"]
                threats = [i for i in insights if i.category == "threat"]
                trends = [i for i in insights if i.category == "trend"]
                
                tab1, tab2, tab3 = st.tabs(["💎 Opportunités", "⚠️ Menaces", "📈 Tendances"])
                
                with tab1:
                    for i, opp in enumerate(opportunities):
                        st.markdown(f"""
                        <div class='insight-card opportunity-card'>
                            <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;'>
                                <h5 style='color: white; margin: 0; font-weight: 600;'>{opp.title}</h5>
                                <div style='display: flex; gap: 8px;'>
                                    <span style='background: #10b981; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem;'>
                                        Impact: {opp.impact_score}/10
                                    </span>
                                    <span style='background: rgba(59, 130, 246, 0.2); color: #60a5fa; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem;'>
                                        {opp.confidence}% sûr
                                    </span>
                                </div>
                            </div>
                            <p style='color: #cbd5e1; margin: 0; line-height: 1.6;'>{opp.description}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                with tab2:
                    for threat in threats:
                        st.markdown(f"""
                        <div class='insight-card threat-card'>
                            <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;'>
                                <h5 style='color: white; margin: 0; font-weight: 600;'>{threat.title}</h5>
                                <div style='display: flex; gap: 8px;'>
                                    <span style='background: #ef4444; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem;'>
                                        Impact: {threat.impact_score}/10
                                    </span>
                                </div>
                            </div>
                            <p style='color: #cbd5e1; margin: 0; line-height: 1.6;'>{threat.description}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                with tab3:
                    for trend in trends:
                        st.markdown(f"""
                        <div class='insight-card trend-card'>
                            <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;'>
                                <h5 style='color: white; margin: 0; font-weight: 600;'>{trend.title}</h5>
                                <div style='display: flex; gap: 8px;'>
                                    <span style='background: #8b5cf6; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem;'>
                                        Impact: {trend.impact_score}/10
                                    </span>
                                </div>
                            </div>
                            <p style='color: #cbd5e1; margin: 0; line-height: 1.6;'>{trend.description}</p>
                        </div>
                        """, unsafe_allow_html=True)

                # Recommandations
                st.markdown('<div class="glass-card"><h3 style="color: white; margin-bottom: 25px;">Recommandations Stratégiques</h3></div>', unsafe_allow_html=True)
                
                recommendations = agent.current_analysis.get("recommendations", [])
                for i, rec in enumerate(recommendations):
                    st.markdown(f"""
                    <div class='recommendation-bubble'>
                        <div class='recommendation-number'>{i+1}</div>
                        <div style='flex: 1;'>
                            <p style='color: #e2e8f0; margin: 0; line-height: 1.6; font-weight: 500;'>{rec}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Chat Interface
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown('<h3 style="color: white; margin-bottom: 20px;">💬 Dialogue avec ARIA</h3>', unsafe_allow_html=True)
                
                for msg in st.session_state.chat_messages[-3:]:
                    if msg["role"] == "user":
                        st.markdown(f"""
                        <div style='text-align: right; margin: 10px 0;'>
                            <div style='background: #3b82f6; color: white; padding: 12px 18px; 
                                        border-radius: 18px 18px 5px 18px; display: inline-block; max-width: 70%;'>
                                {msg["content"]}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style='display: flex; gap: 12px; margin: 10px 0;'>
                            <div style='background: #8b5cf6; border-radius: 50%; width: 35px; height: 35px; 
                                        display: flex; align-items: center; justify-content: center; flex-shrink: 0;'>
                                🤖
                            </div>
                            <div style='background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.import streamlit as st
import json
import time
import random
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional
import asyncio
from dataclasses import dataclass, field
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="🤖 ARIA - AI Strategic Intelligence Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS ultra avancé avec animations spectaculaires
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Background ultra dynamique */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 25%, #3b82f6 50%, #1e40af 75%, #0f172a 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        color: white;
        font-family: 'Inter', sans-serif;
        position: relative;
        overflow-x: hidden;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle at 20% 50%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(139, 92, 246, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 40% 80%, rgba(236, 72, 153, 0.1) 0%, transparent 50%);
        z-index: -1;
        animation: pulseGlow 8s ease-in-out infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes pulseGlow {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    
    /* Cache éléments Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Conteneur principal */
    .block-container {
        padding-top: 2rem;
        max-width: 1600px;
    }
    
    /* Cartes avec glassmorphism ultra */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.4), 
                    0 0 0 1px rgba(255, 255, 255, 0.05) inset;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
    }
    
    .glass-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 60px rgba(59, 130, 246, 0.3), 
                    0 0 40px rgba(59, 130, 246, 0.1) inset;
        border-color: rgba(59, 130, 246, 0.4);
    }
    
    /* Avatar agent spectaculaire */
    .agent-avatar {
        position: relative;
        width: 120px;
        height: 120px;
        margin: 25px auto;
        border-radius: 50%;
        background: conic-gradient(from 0deg, #3b82f6, #8b5cf6, #ec4899, #f59e0b, #3b82f6);
        display: flex;
        align-items: center;
        justify-content: center;
        animation: rotate 12s linear infinite;
        box-shadow: 0 0 40px rgba(59, 130, 246, 0.6);
    }
    
    .agent-avatar.active {
        animation: rotate 3s linear infinite, pulse 2s ease-in-out infinite;
        box-shadow: 0 0 60px rgba(59, 130, 246, 1), 
                    0 0 100px rgba(139, 92, 246, 0.6);
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); box-shadow: 0 0 80px rgba(59, 130, 246, 1); }
    }
    
    .agent-core {
        width: 90px;
        height: 90px;
        border-radius: 50%;
        background: linear-gradient(145deg, #1e40af, #3b82f6, #6366f1);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        position: relative;
        z-index: 2;
        box-shadow: 0 0 30px rgba(59, 130, 246, 0.8) inset;
    }
    
    /* Secteurs avec éléments dépliants */
    .sector-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .sector-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.12);
        box-shadow: 0 15px 35px rgba(59, 130, 246, 0.2);
        border-color: rgba(59, 130, 246, 0.4);
    }
    
    .sector-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 15px;
    }
    
    .sector-icon {
        width: 50px;
        height: 50px;
        border-radius: 15px;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-right: 15px;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
    }
    
    .sector-details {
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .sector-details.expanded {
        max-height: 600px;
        animation: slideDown 0.4s ease-out;
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .expand-arrow {
        transition: transform 0.3s ease;
        font-size: 1.2rem;
        color: #60a5fa;
    }
    
    .expand-arrow.expanded {
        transform: rotate(180deg);
    }
    
    /* Pensées avec animations spectaculaires */
    .thought-bubble {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(139, 92, 246, 0.1));
        border-left: 4px solid #3b82f6;
        padding: 25px;
        margin-bottom: 20px;
        border-radius: 0 20px 20px 0;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.2);
        position: relative;
        overflow: hidden;
        animation: slideInLeft 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    
    @keyframes slideInLeft {
        from {
            transform: translateX(-100px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    /* Métriques en temps réel ultra */
    .metric-value {
        font-size: 2.8rem;
        font-weight: 900;
        font-family: 'Orbitron', monospace;
        background: linear-gradient(45deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 20px rgba(96, 165, 250, 0.5);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 10px rgba(96, 165, 250, 0.8)); }
        to { filter: drop-shadow(0 0 25px rgba(167, 139, 250, 1)); }
    }
    
    /* Boutons ultra premium */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6, #ec4899);
        background-size: 200% 200%;
        color: white;
        border: none;
        border-radius: 16px;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
        padding: 16px 36px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4), 
                    0 0 0 1px rgba(255, 255, 255, 0.1) inset;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        width: 100%;
        position: relative;
        overflow: hidden;
        animation: gradientShift 3s ease infinite;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.05);
        box-shadow: 0 15px 35px rgba(59, 130, 246, 0.6), 
                    0 0 50px rgba(139, 92, 246, 0.3);
        background-position: 100% 0;
    }
    
    /* Titre spectaculaire */
    .premium-title {
        font-size: 4.5rem;
        font-weight: 900;
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(45deg, #60a5fa, #a78bfa, #ec4899, #f59e0b);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 4s ease infinite, titleFloat 6s ease-in-out infinite;
        text-shadow: none;
        position: relative;
    }
    
    @keyframes titleFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* Statut avec pulsations */
    .status-indicator {
        display: inline-block;
        width: 14px;
        height: 14px;
        border-radius: 50%;
        margin-right: 12px;
        position: relative;
    }
    
    .status-indicator::after {
        content: '';
        position: absolute;
        inset: -3px;
        border-radius: 50%;
        background: inherit;
        animation: statusPulse 2s ease-in-out infinite;
        z-index: -1;
        opacity: 0.6;
    }
    
    .status-idle { background: #6b7280; }
    .status-thinking { background: #f59e0b; }
    .status-analyzing { background: #3b82f6; }
    .status-completed { background: #10b981; }
    
    @keyframes statusPulse {
        0% { transform: scale(1); opacity: 0.6; }
        50% { transform: scale(1.5); opacity: 0; }
        100% { transform: scale(1); opacity: 0.6; }
    }
    
    /* Cartes d'insights spectaculaires */
    .insight-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        border-left: 5px solid;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .insight-card:hover {
        transform: translateY(-8px) scale(1.03);
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.08));
    }
    
    .opportunity-card { 
        border-left-color: #10b981; 
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.2); 
    }
    .threat-card { 
        border-left-color: #ef4444; 
        box-shadow: 0 8px 25px rgba(239, 68, 68, 0.2); 
    }
    .trend-card { 
        border-left-color: #8b5cf6; 
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.2); 
    }
    
    /* Chat ultra moderne */
    .chat-message {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(139, 92, 246, 0.1));
        padding: 18px 22px;
        border-radius: 20px;
        margin: 12px 0;
        animation: messageSlide 0.5s ease-out;
        border: 1px solid rgba(59, 130, 246, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    @keyframes messageSlide {
        from {
            transform: translateX(-30px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    /* Recommandations spectaculaires */
    .recommendation-bubble {
        display: flex;
        align-items: start;
        gap: 25px;
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(236, 72, 153, 0.1));
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        border-left: 5px solid #8b5cf6;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .recommendation-bubble:hover {
        transform: translateX(10px);
        box-shadow: 0 12px 30px rgba(139, 92, 246, 0.3);
    }
    
    .recommendation-number {
        background: linear-gradient(135deg, #8b5cf6, #ec4899, #f59e0b);
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        font-weight: 900;
        font-size: 1.4rem;
        box-shadow: 0 8px 20px rgba(139, 92, 246, 0.4);
        animation: numberPulse 2s ease-in-out infinite;
    }
    
    @keyframes numberPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
</style>
""", unsafe_allow_html=True)

# --- Data Classes ---
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
    category: str  # "opportunity", "threat", "trend"

@dataclass
class SectorInfo:
    name: str
    icon: str
    color: str
    market_size: str
    growth_rate: str
    key_players: List[str]
    description: str
    hot_trends: List[str]
    challenges: List[str]

# --- ARIA Agent Class Ultra ---
class ARIAAgent:
    def __init__(self, language: str = "fr"):
        self.language = language
        self.status = "idle"  # idle, thinking, analyzing, completed
        self.thoughts: List[AgentThought] = []
        self.current_analysis: Optional[Dict] = None
        self.confidence_level: float = 0.0
        self.neural_activity: int = 850
        self.activity_history: List[int] = []
        
        self.translations = {
            "fr": {
                "agent_name": "ARIA",
                "agent_desc": "Agent de Recherche et Intelligence Autonome Ultra",
                "status_idle": "En veille - Systèmes prêts",
                "status_thinking": "Réflexion stratégique profonde...",
                "status_analyzing": "Analyse multi-dimensionnelle...",
                "status_completed": "Mission accomplie ✨",
                "sectors": {
                    "FinTech": "Technologies Financières",
                    "HealthTech": "Technologies de la Santé",
                    "SaaS": "Logiciels en Service",
                    "E-commerce": "Commerce Électronique",
                    "PropTech": "Technologies Immobilières",
                    "EdTech": "Technologies de l'Éducation",
                    "GreenTech": "Technologies Vertes",
                    "SpaceTech": "Technologies Spatiales",
                    "AI/ML": "Intelligence Artificielle"
                },
                "thoughts": [
                    "🔍 Initialisation des capteurs quantiques de marché...",
                    "🧠 Activation des réseaux neuronaux sectoriels avancés...",
                    "📊 Ingestion de 2.4 To de données temps réel multi-sources...",
                    "⚡ Traitement par algorithmes de deep learning génératif...",
                    "🎯 Corrélation des signaux faibles via IA prédictive...",
                    "📈 Modélisation Monte Carlo des tendances futures...",
                    "🤖 Génération d'insights actionnables par GPT quantique...",
                    "✨ Synthèse stratégique holistique finalisée..."
                ]
            },
            "en": {
                "agent_name": "ARIA",
                "agent_desc": "Ultra Autonomous Research & Intelligence Agent",
                "status_idle": "On standby - Systems ready",
                "status_thinking": "Deep strategic thinking...",
                "status_analyzing": "Multi-dimensional analysis...",
                "status_completed": "Mission accomplished ✨",
                "sectors": {
                    "FinTech": "Financial Technologies",
                    "HealthTech": "Health Technologies",
                    "SaaS": "Software as a Service",
                    "E-commerce": "Electronic Commerce",
                    "PropTech": "Property Technologies",
                    "EdTech": "Education Technologies",
                    "GreenTech": "Green Technologies",
                    "SpaceTech": "Space Technologies",
                    "AI/ML": "Artificial Intelligence"
                },
                "thoughts": [
                    "🔍 Initializing quantum market sensors...",
                    "🧠 Activating advanced sectoral neural networks...",
                    "📊 Ingesting 2.4 TB of real-time multi-source data...",
                    "⚡ Processing via generative deep learning algorithms...",
                    "🎯 Correlating weak signals through predictive AI...",
                    "📈 Monte Carlo modeling of future trends...",
                    "🤖 Generating actionable insights via quantum GPT...",
                    "✨ Holistic strategic synthesis completed..."
                ]
            }
        }
        
        # Informations détaillées des secteurs
        self.sector_info = {
            "FinTech": SectorInfo(
                name="FinTech",
                icon="💳",
                color="#10b981",
                market_size="€156.2B",
                growth_rate="+23.4%",
                key_players=["Stripe", "Klarna", "Revolut", "N26", "Adyen"],
                description="Révolution des services financiers par la technologie",
                hot_trends=["IA Conversationnelle", "DeFi 2.0", "Néo-banques", "Crypto institutionnel"],
                challenges=["Régulation MiCA", "Cybersécurité", "Concurrence BigTech"]
            ),
            "HealthTech": SectorInfo(
                name="HealthTech",
                icon="🏥",
                color="#3b82f6",
                market_size="€89.7B",
                growth_rate="+18.9%",
                key_players=["Doctolib", "Teladoc", "Philips Health", "Siemens Healthineers"],
                description="Transformation digitale de la santé et du bien-être",
                hot_trends=["IA Diagnostique", "Télémédecine", "IoMT", "Médecine personnalisée"],
                challenges=["RGPD Santé", "Interopérabilité", "Adoption médicale"]
            ),
            "SaaS": SectorInfo(
                name="SaaS",
                icon="☁️",
                color="#8b5cf6",
                market_size="€93.1B",
                growth_rate="+21.7%",
                key_players=["Salesforce", "Microsoft", "ServiceNow", "Workday", "Atlassian"],
                description="Logiciels en tant que service pour entreprises",
                hot_trends=["IA Générative intégrée", "Vertical SaaS", "API-first", "No-code/Low-code"],
                challenges=["Saturation marché", "Retention clients", "Sécurité cloud"]
            ),
            "E-commerce": SectorInfo(
                name="E-commerce",
                icon="🛍️",
                color="#f59e0b",
                market_size="€887.3B",
                growth_rate="+12.3%",
                key_players=["Amazon", "Shopify", "Zalando", "Otto", "Allegro"],
                description="Commerce électronique et marketplace",
                hot_trends=["Commerce Conversationnel", "Social Commerce", "AR/VR Shopping", "Durabilité"],
                challenges=["Inflation logistique", "Retours produits", "Concurrence"]
            ),
            "PropTech": SectorInfo(
                name="PropTech",
                icon="🏢",
                color="#ec4899",
                market_size="€12.3B",
                growth_rate="+31.2%",
                key_players=["Zillow", "Compass", "Opendoor", "WeWork", "Airbnb"],
                description="Technologies révolutionnant l'immobilier",
                hot_trends=["Valorisation IA", "VR/AR Visites", "Smart Buildings", "Blockchain Titres"],
                challenges=["Régulation Airbnb", "Bulle immobilière", "Adoption agents"]
            ),
            "EdTech": SectorInfo(
                name="EdTech",
                icon="🎓",
                color="#06b6d4",
                market_size="€24.5B",
                growth_rate="+16.8%",
                key_players=["Coursera", "Udemy", "Duolingo", "Khan Academy", "Byju's"],
                description="Transformation numérique de l'éducation",
                hot_trends=["IA Pédagogique", "Métaverse Éducatif", "Micro-learning", "Gamification"],
                challenges=["Fracture numérique", "Engagement", "Certification"]
            ),
            "GreenTech": SectorInfo(
                name="GreenTech",
                icon="🌱",
                color="#22c55e",
                market_size="€47.1B",
                growth_rate="+28.5%",
                key_players=["Tesla", "Vestas", "Beyond Meat", "Ørsted", "Northvolt"],
                description="Technologies pour un futur durable",
                hot_trends=["IA Efficacité Énergétique", "Carbon Tracking", "Smart Grid", "Économie Circulaire"],
                challenges=["Coût transition", "Greenwashing", "Scalabilité"]
            ),
            "SpaceTech": SectorInfo(
                name="SpaceTech",
                icon="🚀",
                color="#a855f7",
                market_size="€8.3B",
                growth_rate="+45.7%",
                key_players=["SpaceX", "Blue Origin", "Rocket Lab", "Planet Labs", "Relativity Space"],
                description="Nouvelle économie spatiale commerciale",
                hot_trends=["Constellations Satellites", "Tourisme Spatial", "Space Mining", "Lanceurs Réutilisables"],
                challenges=["Débris spatiaux", "Coûts R&D", "Régulation spatiale"]
            ),
            "AI/ML": SectorInfo(
                name="AI/ML",
                icon="🤖",
                color="#f97316",
                market_size="€156.8B",
                growth_rate="+42.1%",
                key_players=["OpenAI", "Anthropic", "Google DeepMind", "Microsoft", "NVIDIA"],
                description="Intelligence artificielle et apprentissage automatique",
                hot_trends=["IA Générative", "AGI Progress", "Quantum-AI", "Edge AI", "Multimodal AI"],
                challenges=["AI Act EU", "Bias algorithmes", "Compute shortage"]
            )
        }
        
        self.market_data = self._generate_all_sector_data()

    def get_translation(self, key: str, lang: Optional[str] = None) -> str:
        if lang is None:
            lang = self.language
        return self.translations[lang].get(key, key)

    def _generate_sector_data(self, sector_name: str, lang: str, sector_key: str) -> Dict:
        """Génère des données d'analyse détaillées pour un secteur."""
        is_fr = lang == "fr"
        
        # Données spécialisées par secteur
        if sector_key == "FinTech":
            if is_fr:
                return {
                    "summary": f"Le secteur {sector_name} révolutionne les services financiers avec l'IA générative, les néo-banques et la DeFi institutionnelle. La régulation MiCA structure le marché européen.",
                    "insights": [
                        MarketInsight("IA Conversationnelle Bancaire", "L'intégration d'assistants IA génère +34% d'engagement client et représente un marché de €3.2B", 9.4, 91, "opportunity"),
                        MarketInsight("DeFi Institutionnelle", "€45.8B d'actifs sous gestion institutionnels adoptent la DeFi", 8.7, 85, "opportunity"),
                        MarketInsight("Super-Apps Financières", "Convergence vers des écosystèmes intégrés", 8.2, 79, "trend"),
                        MarketInsight("Régulation MiCA", "Coûts de conformité +23% mais élimination de 40% des concurrents", 7.9, 88, "threat")
                    ],
                    "recommendations": [
                        "Intég
