if agent.status not in ["idle"]:
            if st.button("⏹️ STOPPER L'AGENT", key="stop_agent"):
                st.session_state.running_analysis = False
                agent.reset()
                st.rerun()
        
        # Graphiques en temps réel
        if agent.status == "completed":
            st.plotly_chart(agent.generate_confidence_gauge(), use_container_width=True, key="confidence_chart")
            st.plotly_chart(agent.generate_activity_chart(), use_container_width=True, key="activity_chart")

    # --- COLONNE 2 : Affichage des Résultats Ultra ---
    with col2:
        results_placeholder = st.empty()

        if st.session_state.get("running_analysis", False):
            # --- SIMULATION DE L'ANALYSE EN DIRECT SPECTACULAIRE ---
            selected_sector = st.session_state.get("selected_sector", "FinTech")
            thoughts = agent.get_translation("thoughts")
            agent.thoughts = []
            agent.activity_history = [agent.neural_activity]
            
            # Container pour l'animation des pensées
            with results_placeholder.container():
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown('<h3 style="color: white; margin-bottom: 25px;">🧠 Flux de Pensées ARIA</h3>', unsafe_allow_html=True)
                
                thoughts_container = st.empty()
                thoughts_html = ""
                
                for i, thought_text in enumerate(thoughts):
                    # Délai réaliste entre les pensées
                    time.sleep(random.uniform(1.0, 2.0))
                    
                    # Mise à jour du statut
                    if i >= 3 and agent.status == "thinking":
                        agent.status = "analyzing"
                    
                    # Mise à jour des métriques avec variations réalistes
                    agent.neural_activity += random.randint(-50, 80)
                    agent.neural_activity = max(700, min(1000, agent.neural_activity))
                    agent.activity_history.append(agent.neural_activity)
                    agent.confidence_level = min((i + 1) / len(thoughts) * 95, 95)
                    
                    # Ajout de la nouvelle pensée
                    thought = AgentThought(content=thought_text)
                    agent.thoughts.append(thought)
                    
                    # Animation des icônes selon le type de pensée
                    thought_icons = ["🔍", "🧠", "📊", "⚡", "🎯", "📈", "🤖", "✨"]
                    icon = thought_icons[i] if i < len(thought_icons) else random.choice(thought_icons)
                    
                    # Construction du HTML avec animations
                    thought_item_html = f"""
                    <div class='thought-bubble' style='animation-delay: {i*0.1}s;'>
                        <div style='display: flex; align-items: start; gap: 20px;'>
                            <div style='background: linear-gradient(135deg, #3b82f6, #8b5cf6); 
                                        border-radius: 50%; width: 45px; height: 45px; 
                                        display: flex; align-items: center; justify-content: center;
                                        font-size: 1.4rem; flex-shrink: 0; animation: pulse 2s infinite;'>
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
                                        Confiance: {agent.confidence_level:.1f}%
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                    """
                    
                    thoughts_html += thought_item_html
                    
                    # Mise à jour de l'affichage
                    with thoughts_container.container():
                        st.markdown(thoughts_html, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Animation de finalisation
            st.markdown("""
            <div style='text-align: center; padding: 20px;'>
                <div class='loading-spinner'></div>
                <p style='color: #60a5fa; margin-top: 15px; font-weight: 500;'>Finalisation de l'analyse...</p>
            </div>
            """, unsafe_allow_html=True)
            
            time.sleep(2)
            
            # Finalisation de l'analyse
            agent.status = "completed"
            agent.confidence_level = random.uniform(88, 97)
            agent.current_analysis = agent.market_data.get(selected_sector, {}).get(agent.language, {})
            st.session_state.running_analysis = False
            st.rerun()

        elif agent.status == "completed" and agent.current_analysis:
            # --- AFFICHAGE DES RÉSULTATS FINAUX SPECTACULAIRES ---
            with results_placeholder.container():
                # Synthèse exécutive avec animation
                st.markdown(f"""
                <div class='glass-card' style='animation: slideInLeft 0.6s ease-out;'>
                    <div style='display: flex; align-items: start; gap: 20px; margin-bottom: 20px;'>
                        <div style='background: linear-gradient(135deg, #10b981, #059669); 
                                    border-radius: 15px; width: 60px; height: 60px;
                                    display: flex; align-items: center; justify-content: center;
                                    font-size: 1.8rem; flex-shrink: 0; box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3);'>
                            📋
                        </div>
                        <div style='flex: 1;'>
                            <h3 style='color: white; margin: 0 0 15px 0; font-size: 1.5rem;'>Synthèse Stratégique</h3>
                            <p style='color: #e2e8f0; font-size: 1.1rem; line-height: 1.6; margin: 0;'>
                                {agent.current_analysis.get("summary", "")}
                            </p>
                        </div>
                        <div style='background: rgba(16, 185, 129, 0.1); border-radius: 12px; 
                                    padding: 12px; text-align: center; min-width: 80px;'>
                            <div style='color: #10b981; font-size: 1.3rem; font-weight: bold;'>
                                {agent.confidence_level:.1f}%
                            </div>
                            <div style='color: #94a3b8; font-size: 0.8rem;'>Confiance</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Insights avec catégorisation spectaculaire
                st.markdown('<div class="glass-card" style="animation: slideInLeft 0.8s ease-out;"><h3 style="color: white; margin-bottom: 25px;">🎯 Intelligence Stratégique</h3></div>', unsafe_allow_html=True)
                
                insights = agent.current_analysis.get("insights", [])
                opportunities = [i for i in insights if i.category == "opportunity"]
                threats = [i for i in insights if i.category == "threat"]
                trends = [i for i in insights if i.category == "trend"]
                
                # Onglets pour organiser les insights
                tab1, tab2, tab3 = st.tabs(["💎 Opportunités", "⚠️ Menaces", "📈 Tendances"])
                
                with tab1:
                    for i, opp in enumerate(opportunities):
                        st.markdown(f"""
                        <div class='insight-card opportunity-card' style='animation: fadeInUp {0.3 + i*0.1}s ease-out backwards;'>
                            <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;'>
                                <h5 style='color: white; margin: 0; font-size: 1.1rem; font-weight: 600;'>
                                    💡 {opp.title}
                                </h5>
                                <div style='display: flex; gap: 8px;'>
                                    <span style='background: linear-gradient(135deg, #10b981, #059669); 
                                                color: white; padding: 4px 10px; border-radius: 12px; 
                                                font-size: 0.75rem; font-weight: 600;'>
                                        Impact: {opp.impact_score}/10
                                    </span>
                                    <span style='background: rgba(59, 130, 246, 0.2); color: #60a5fa; 
                                                padding: 4px 10px; border-radius: 12px; font-size: 0.75rem;'>
                                        {opp.confidence}% sûr
                                    </span>
                                </div>
                            </div>
                            <p style='color: #cbd5e1; margin: 0; line-height: 1.6; font-size: 0.95rem;'>
                                {opp.description}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                
                with tab2:
                    for i, threat in enumerate(threats):
                        st.markdown(f"""
                        <div class='insight-card threat-card' style='animation: fadeInUp {0.3 + i*0.1}s ease-out backwards;'>
                            <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;'>
                                <h5 style='color: white; margin: 0; font-size: 1.1rem; font-weight: 600;'>
                                    🚨 {threat.title}
                                </h5>
                                <div style='display: flex; gap: 8px;'>
                                    <span style='background: linear-gradient(135deg, #ef4444, #dc2626); 
                                                color: white; padding: 4px 10px; border-radius: 12px; 
                                                font-size: 0.75rem; font-weight: 600;'>
                                        Impact: {threat.impact_score}/10
                                    </span>
                                    <span style='background: rgba(59, 130, 246, 0.2); color: #60a5fa; 
                                                padding: 4px 10px; border-radius: 12px; font-size: 0.75rem;'>
                                        {threat.confidence}% sûr
                                    </span>
                                </div>
                            </div>
                            <p style='color: #cbd5e1; margin: 0; line-height: 1.6; font-size: 0.95rem;'>
                                {threat.description}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                
                with tab3:
                    for i, trend in enumerate(trends):
                        st.markdown(f"""
                        <div class='insight-card trend-card' style='animation: fadeInUp {0.3 + i*0.1}s ease-out backwards;'>
                            <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;'>
                                <h5 style='color: white; margin: 0; font-size: 1.1rem; font-weight: 600;'>
                                    📊 {trend.title}
                                </h5>
                                <div style='display: flex; gap: 8px;'>
                                    <span style='background: linear-gradient(135deg, #8b5cf6, #7c3aed); 
                                                color: white; padding: 4px 10px; border-radius: 12px; 
                                                font-size: 0.75rem; font-weight: 600;'>
                                        Impact: {trend.impact_score}/10
                                    </span>
                                    <span style='background: rgba(59, 130, 246, 0.2); color: #60a5fa; 
                                                padding: 4px 10px; border-radius: 12px; font-size: 0.75rem;'>
                                        {trend.confidence}% sûr
                                    </span>
                                </div>
                            </div>
                            <p style='color: #cbd5e1; margin: 0; line-height: 1.6; font-size: 0.95rem;'>
                                {trend.description}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

                # Recommandations stratégiques ultra
                st.markdown('<div class="glass-card" style="animation: slideInLeft 1.2s ease-out;"><h3 style="color: white; margin-bottom: 25px;">🎯 Recommandations Stratégiques IA</h3></div>', unsafe_allow_html=True)
                
                recommendations = agent.current_analysis.get("recommendations", [])
                for i, rec in enumerate(recommendations):
                    st.markdown(f"""
                    <div class='recommendation-bubble' style='animation: slideInRight {0.4 + i*0.15}s ease-out backwards;'>
                        <div class='recommendation-number'>{i+1}</div>
                        <div style='flex: 1;'>
                            <p style='color: #e2e8f0; margin: 0; line-height: 1.6; font-weight: 500; font-size: 1.05rem;'>
                                {rec}
                            </p>
                        </div>
                        <div style='background: rgba(139, 92, 246, 0.1); border-radius: 10px; 
                                    padding: 8px; display: flex; align-items: center;'>
                            <span style='color: #8b5cf6; font-size: 1.2rem;'>⚡</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # --- Section Chat Ultra Interactive ---
                st.markdown('<div class="glass-card" style="animation: slideInLeft 1.6s ease-out;">', unsafe_allow_html=True)
                st.markdown('<h3 style="color: white; margin-bottom: 20px;">💬 Dialogue avec ARIA</h3>', unsafe_allow_html=True)
                
                # Affichage des messages récents avec design amélioré
                for msg in st.session_state.chat_messages[-4:]:
                    if msg["role"] == "user":
                        st.markdown(f"""
                        <div style='display: flex; justify-content: flex-end; margin: 15px 0;'>
                            <div style='background: linear-gradient(135deg, #3b82f6, #2563eb); 
                                        color: white; padding: 12px 18px; border-radius: 18px 18px 5px 18px;
                                        max-width: 70%; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);'>
                                <div style='font-size: 0.8rem; opacity: 0.8; margin-bottom: 4px;'>Vous</div>
                                <div style='font-size: 0.95rem; line-height: 1.4;'>{msg["content"]}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style='display: flex; justify-content: flex-start; margin: 15px 0;'>
                            <div style='display: flex; gap: 12px; max-width: 85%;'>
                                <div style='background: linear-gradient(135deg, #8b5cf6, #7c3aed); 
                                            border-radius: 50%; width: 35px; height: 35px; 
                                            display: flex; align-items: center; justify-content: center;
                                            flex-shrink: 0; margin-top: 5px;'>
                                    🤖
                                </div>
                                <div style='background: rgba(139, 92, 246, 0.1); 
                                            border: 1px solid rgba(139, 92, 246, 0.2);
                                            color: #e2e8f0; padding: 12px 18px; 
                                            border-radius: 18px 18px 18px 5px;'>
                                    <div style='font-size: 0.8rem; color: #a78bfa; margin-bottom: 4px;'>ARIA</div>
                                    <div style='font-size: 0.95rem; line-height: 1.5;'>{msg["content"]}</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Interface de chat améliorée
                col_chat1, col_chat2 = st.columns([4, 1])
                with col_chat1:
                    user_question = st.text_input(
                        "Posez votre question à ARIA...", 
                        key="chat_input",
                        placeholder="Ex: Quelles sont les opportunités principales ?",
                        label_visibility="collapsed"
                    )
                
                with col_chat2:
                    send_button = st.button("💬 Envoyer", key="send_chat", type="primary")
                
                if (user_question and send_button) or (user_question and st.session_state.get("chat_enter", False)):
                    st.session_state.chat_messages.append({"role": "user", "content": user_question})
                    
                    # Simulation de réflexion
                    with st.spinner("ARIA réfléchit..."):
                        time.sleep(1)
                        selected_sector = st.session_state.get("selected_sector", "FinTech")
                        response = agent.chat_with_agent(user_question, selected_sector)
                    
                    st.session_state.chat_messages.append({"role": "assistant", "content": response})
                    st.rerun()
                
                # Suggestions de questions
                st.markdown("**💡 Questions suggérées:**", unsafe_allow_html=True)
                col_sug1, col_sug2 = st.columns(2)
                with col_sug1:
                    if st.button("Principales opportunités ?", key="sug1"):
                        st.session_state.chat_messages.append({"role": "user", "content": "Quelles sont les principales opportunités ?"})
                        st.rerun()
                
                with col_sug2:
                    if st.button("Risques majeurs ?", key="sug2"):
                        st.session_state.chat_messages.append({"role": "user", "content": "Quels sont les risques majeurs ?"})
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)

                # --- Actions Export Ultra ---
                st.markdown('<div class="glass-card" style="animation: slideInLeft 2s ease-out;">', unsafe_allow_html=True)
                st.markdown('<h3 style="color: white; text-align: center; margin-bottom: 20px;">📤 Actions & Export</h3>', unsafe_allow_html=True)
                
                col_exp1, col_exp2 = st.columns(2)
                
                with col_exp1:
                    if st.button("📄 Rapport Complet", type="primary", key="export_report"):
                        # Génération du rapport ultra détaillé
                        selected_sector = st.session_state.get("selected_sector", "FinTech")
                        sector_info = agent.sector_info[selected_sector]
                        
                        report_content = f"""# 🧠 ARIA - RAPPORT D'INTELLIGENCE STRATÉGIQUE

## 📊 MÉTADONNÉES
- **Secteur Analysé:** {sector_info.name} ({agent.get_translation("sectors")[selected_sector]})
- **Date d'Analyse:** {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}
- **Niveau de Confiance IA:** {agent.confidence_level:.1f}%
- **Activité Neuronale:** {agent.neural_activity} noeuds
- **Durée d'Analyse:** {len(agent.thoughts)} cycles de réflexion

## 🎯 SYNTHÈSE EXÉCUTIVE
{agent.current_analysis.get("summary", "")}

## 📈 DONNÉES SECTORIELLES
- **Taille du Marché:** {sector_info.market_size}
- **Croissance:** {sector_info.growth_rate} CAGR
- **Acteurs Clés:** {", ".join(sector_info.key_players)}

## 💡 INTELLIGENCE STRATÉGIQUE

### 💎 OPPORTUNITÉS MAJEURES
"""
                        
                        for i, opp in enumerate(opportunities, 1):
                            report_content += f"""
**{i}. {opp.title}**
- Description: {opp.description}
- Score d'Impact: {opp.impact_score}/10
- Niveau de Confiance: {opp.confidence}%
---
"""
                        
                        report_content += "\n### ⚠️ MENACES & DÉFIS\n"
                        for i, threat in enumerate(threats, 1):
                            report_content += f"""
**{i}. {threat.title}**
- Description: {threat.description}
- Score d'Impact: {threat.impact_score}/10
- Niveau de Confiance: {threat.confidence}%
---
"""
                        
                        report_content += "\n### 📊 TENDANCES ÉMERGENTES\n"
                        for i, trend in enumerate(trends, 1):
                            report_content += f"""
**{i}. {trend.title}**
- Description: {trend.description}
- Score d'Impact: {trend.impact_score}/10
- Niveau de Confiance: {trend.confidence}%
---
"""
                        
                        report_content += "\n## 🎯 RECOMMANDATIONS STRATÉGIQUES\n\n"
                        for i, rec in enumerate(recommendations, 1):
                            report_content += f"{i}. {rec}\n"
                        
                        report_content += f"""

## 🔍 DÉTAILS TECHNIQUES
- **Sources de Données:** 2,4 To d'informations temps réel
- **Algorithmes Utilisés:** Deep Learning Génératif + IA Prédictive
- **Méthodologie:** Analyse Multi-dimensionnelle Monte Carlo
- **Dernière Mise à Jour:** {datetime.now().strftime('%H:%M:%S')}

---
*Rapport généré par ARIA (Autonomous Research & Intelligence Agent)*
*Technologie: IA Générative + Réseaux Neuronaux Quantiques*
"""
                        
                        st.download_button(
                            label="⬇️ Télécharger le Rapport",
                            data=report_content.encode('utf-8'),
                            file_name=f"ARIA_Ultra_Report_{selected_sector}_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                            mime="text/markdown",
                            key="download_full_report"
                        )
                        
                        st.success("✅ Rapport ultra détaillé généré avec succès!")
                        st.balloons()
                
                with col_exp2:
                    if st.button("🔄 Nouvelle Analyse", key="reset_analysis"):
                        agent.reset()
                        st.session_state.running_analysis = False
                        if 'selected_sector' in st.session_state:
                            del st.session_state.selected_sector
                        st.success("🔄 ARIA réinitialisé - Prêt pour une nouvelle analyse")
                        time.sleep(1)
                        st.rerun()
                
                # Actions rapides
                col_act1, col_act2 = st.columns(2)
                with col_act1:
                    if st.button("🔔 Alertes Smart", key="smart_alerts"):
                        st.info("🔔 Alertes intelligentes configurées pour ce secteur")
                
                with col_act2:
                    if st.button("📤 Partager", key="share_analysis"):
                        st.info("📤 Analyse prête à partager avec votre équipe")
                
                st.markdown('</div>', unsafe_allow_html=True)

        else:
            # --- ÉCRAN D'ACCUEIL ULTRA SPECTACULAIRE ---
            with results_placeholder.container():
                st.markdown("""
                <div class='glass-card' style='text-align: center; padding: 60px 40px; position: relative; overflow: hidden;'>
                    <div style='position: absolute; top: 0; left: 0; right: 0; bottom: 0; 
                                background: radial-gradient(circle at center, rgba(59, 130, 246, 0.1), transparent);'></div>
                    <div style='position: relative; z-index: 2;'>
                        <div style='font-size: 6rem; margin-bottom: 30px; animation: float 4s ease-in-out infinite;'>🤖</div>
                        <h2 style='color: white; margin-bottom: 20px; font-size: 2.2rem; font-weight: 700;'>
                            ARIA Ultra est Prête
                        </h2>
                        <p style='color: #94a3b8; margin-bottom: 40px; font-size: 1.2rem; line-height: 1.6;'>
                            Agent d'intelligence artificielle autonome prêt pour l'analyse stratégique 
                            multi-dimensionnelle de votre secteur d'activité.
                        </p>
                        
                        <div style='background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(139, 92, 246, 0.05)); 
                                    border-radius: 20px; padding: 35px; 
                                    border: 1px solid rgba(59, 130, 246, 0.2); margin-bottom: 30px;'>
                            <h4 style='color: #60a5fa; margin-bottom: 25px; font-size: 1.4rem;'>
                                🧠 Capacités d'Intelligence Ultra
                            </h4>
                            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px; text-align: left;'>
                                <div style='display: flex; align-items: center; gap: 12px;'>
                                    <span style='font-size: 1.5rem;'>🔍</span>
                                    <span style='color: #cbd5e1; font-size: 1rem;'>Analyse Quantique Multi-Sources</span>
                                </div>
                                <div style='display: flex; align-items: center; gap: 12px;'>
                                    <span style='font-size: 1.5rem;'>⚡</span>
                                    <span style='color: #cbd5e1; font-size: 1rem;'>Prédictions Monte Carlo</span>
                                </div>
                                <div style='display: flex; align-items: center; gap: 12px;'>
                                    <span style='font-size: 1.5rem;'>🎯</span>
                                    <span style='color: #cbd5e1; font-size: 1rem;'>Détection Signaux Faibles</span>
                                </div>
                                <div style='display: flex; align-items: center; gap: 12px;'>
                                    <span style='font-size: 1.5rem;'>📊</span>
                                    <span style='color: #cbd5e1; font-size: 1rem;'>Évaluation Risques IA</span>
                                </div>
                                <div style='display: flex; align-items: center; gap: 12px;'>
                                    <span style='font-size: 1.5rem;'>🤖</span>
                                    <span style='color: #cbd5e1; font-size: 1rem;'>Décisions Autonomes</span>
                                </div>
                                <div style='display: flex; align-items: center; gap: 12px;'>
                                    <span style='font-size: 1.5rem;'>💬</span>
                                    <span style='color: #cbd5e1; font-size: 1rem;'>Dialogue Contextuel</span>
                                </div>
                            </div>
                        </div>
                        
                        <div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(6, 182, 212, 0.05)); 
                                    border-radius: 15px; padding: 25px; border-left: 4px solid #10b981;'>
                            <p style='color: #10b981; margin: 0; font-size: 1rem; font-weight: 600;'>
                                ✨ Sélectionnez un secteur dans le panneau de gauche et activez ARIA pour commencer
                            </p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # --- Footer Ultra Premium ---
    st.markdown(f"""
    <div style='margin-top: 60px; text-align: center; padding: 40px 0; 
                background: linear-gradient(135deg, rgba(0, 0, 0, 0.3), rgba(59, 130, 246, 0.1));
                border-top: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px 20px 0 0;import streamlit as st
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
    
    /* Particules flottantes */
    .floating-particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    
    .particle {
        position: absolute;
        width: 4px;
        height: 4px;
        background: rgba(59, 130, 246, 0.6);
        border-radius: 50%;
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        50% { transform: translateY(-100px) rotate(180deg); opacity: 0.8; }
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
    
    .agent-avatar::before {
        content: '';
        position: absolute;
        inset: -3px;
        border-radius: 50%;
        background: conic-gradient(from 0deg, #3b82f6, #8b5cf6, #ec4899, #f59e0b, #3b82f6);
        animation: rotate 8s linear infinite reverse;
        z-index: -1;
        filter: blur(6px);
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
    
    .thought-bubble::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899);
        animation: shimmer 2s ease-in-out infinite;
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
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
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
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.05);
        box-shadow: 0 15px 35px rgba(59, 130, 246, 0.6), 
                    0 0 50px rgba(139, 92, 246, 0.3);
        background-position: 100% 0;
    }
    
    .stButton > button:hover::before {
        left: 100%;
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
    
    .insight-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), transparent);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .insight-card:hover {
        transform: translateY(-8px) scale(1.03);
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.08));
    }
    
    .insight-card:hover::before {
        opacity: 1;
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
    
    .chat-message::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 3px;
        height: 100%;
        background: linear-gradient(45deg, #3b82f6, #8b5cf6);
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
    
    .recommendation-bubble::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.1));
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
    
    /* Effets de loading spectaculaires */
    .loading-spinner {
        width: 40px;
        height: 40px;
        border: 3px solid rgba(59, 130, 246, 0.3);
        border-top: 3px solid #3b82f6;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Progress bar animée */
    .progress-bar {
        width: 100%;
        height: 4px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 2px;
        overflow: hidden;
        margin: 15px 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899);
        border-radius: 2px;
        animation: progressFill 3s ease-out forwards;
    }
    
    @keyframes progressFill {
        from { width: 0%; }
        to { width: 100%; }
    }
</style>
""", unsafe_allow_html=True)

# Ajout des particules flottantes
st.markdown("""
<div class="floating-particles">
    <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
    <div class="particle" style="left: 20%; animation-delay: 1s;"></div>
    <div class="particle" style="left: 30%; animation-delay: 2s;"></div>
    <div class="particle" style="left: 40%; animation-delay: 3s;"></div>
    <div class="particle" style="left: 50%; animation-delay: 4s;"></div>
    <div class="particle" style="left: 60%; animation-delay: 5s;"></div>
    <div class="particle" style="left: 70%; animation-delay: 6s;"></div>
    <div class="particle" style="left: 80%; animation-delay: 1.5s;"></div>
    <div class="particle" style="left: 90%; animation-delay: 2.5s;"></div>
</div>
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
                    "SaaS": "Logiciels en tant que Service",
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
        
        sector_info = self.sector_info[sector_key]
        
        # Données spécialisées par secteur
        sector_specific_data = {
            "FinTech": {
                "fr": {
                    "summary": f"Le secteur {sector_name} ({sector_info.market_size}, {sector_info.growth_rate} CAGR) connaît une révolution avec l'IA générative intégrée aux services financiers. La régulation MiCA européenne restructure le marché en faveur des acteurs conformes.",
                    "insights": [
                        MarketInsight("IA Conversationnelle Bancaire", "L'intégration d'assistants IA dans les services bancaires génère +34% d'engagement client et représente un marché de €3.2B d'ici 2027", 9.4, 91, "opportunity"),
                        MarketInsight("DeFi Institutionnelle", "Les institutions adoptent massivement la DeFi avec €45.8B d'actifs sous gestion institutionnels", 8.7, 85, "opportunity"),
                        MarketInsight("Super-Apps Financières", "Convergence vers des écosystèmes financiers intégrés sur le modèle asiatique", 8.2, 79, "trend"),
                        MarketInsight("Durcissement MiCA", "Nouvelles régulations européennes imposent des coûts de conformité de +23% mais éliminent 40% des concurrents", 7.9, 88, "threat")
                    ],
                    "recommendations": [
                        "Intégrer l'IA conversationnelle avant Q2 2025 pour capturer l'avantage first-mover",
                        "Développer une stratégie de conformité MiCA 8 mois avant l'entrée en vigueur",
                        "Acquérir des fintechs spécialisées en DeFi avant la consolidation du marché"
                    ]
                },
                "en": {
                    "summary": f"The {sector_name} sector ({sector_info.market_size}, {sector_info.growth_rate} CAGR) is experiencing a revolution with generative AI integrated into financial services. European MiCA regulation is restructuring the market in favor of compliant players.",
                    "insights": [
                        MarketInsight("Conversational Banking AI", "AI assistant integration in banking services generates +34% client engagement and represents a €3.2B market by 2027", 9.4, 91, "opportunity"),
                        MarketInsight("Institutional DeFi", "Institutions massively adopting DeFi with €45.8B in institutional assets under management", 8.7, 85, "opportunity"),
                        MarketInsight("Financial Super-Apps", "Convergence towards integrated financial ecosystems following the Asian model", 8.2, 79, "trend"),
                        MarketInsight("MiCA Tightening", "New European regulations impose +23% compliance costs but eliminate 40% of competitors", 7.9, 88, "threat")
                    ],
                    "recommendations": [
                        "Integrate conversational AI before Q2 2025 to capture first-mover advantage",
                        "Develop MiCA compliance strategy 8 months before enforcement",
                        "Acquire specialized DeFi fintechs before market consolidation"
                    ]
                }
            },
            "HealthTech": {
                "fr": {
                    "summary": f"Le secteur {sector_name} ({sector_info.market_size}, {sector_info.growth_rate} CAGR) transforme radicalement les soins de santé avec l'IA prédictive, la télémédecine généralisée et les dispositifs IoMT. L'adoption post-COVID reste pérenne.",
                    "insights": [
                        MarketInsight("IA Diagnostique Avancée", "Algorithmes de diagnostic IA atteignent 94.7% de précision, surpassant les radiologues dans 12 spécialités", 9.6, 93, "opportunity"),
                        MarketInsight("Télémédecine Permanente", "67% des consultations restent digitales post-COVID avec un taux de satisfaction de 4.2/5", 8.9, 87, "trend"),
                        MarketInsight("IoMT Explosion", "156M de dispositifs médicaux connectés déployés en Europe, générant 2.4 To de données/jour", 8.4, 82, "opportunity"),
                        MarketInsight("Régulation GDPR Santé", "Durcissement des contrôles sur les données de santé avec des amendes moyennes de €2.3M", 7.5, 90, "threat")
                    ],
                    "recommendations": [
                        "Développer des partenariats avec les CHU pour valider les algorithmes d'IA",
                        "Investir dans la cybersécurité médicale certifiée ISO 27799",
                        "Créer des plateformes de télémédecine spécialisées par pathologie"
                    ]
                },
                "en": {
                    "summary": f"The {sector_name} sector ({sector_info.market_size}, {sector_info.growth_rate} CAGR) is radically transforming healthcare with predictive AI, widespread telemedicine, and IoMT devices. Post-COVID adoption remains sustainable.",
                    "insights": [
                        MarketInsight("Advanced AI Diagnostics", "AI diagnostic algorithms achieve 94.7% accuracy, outperforming radiologists in 12 specialties", 9.6, 93, "opportunity"),
                        MarketInsight("Permanent Telemedicine", "67% of consultations remain digital post-COVID with 4.2/5 satisfaction rate", 8.9, 87, "trend"),
                        MarketInsight("IoMT Explosion", "156M connected medical devices deployed in Europe, generating 2.4 TB of data/day", 8.4, 82, "opportunity"),
                        MarketInsight("Health GDPR Regulation", "Tightening controls on health data with average fines of €2.3M", 7.5, 90, "threat")
                    ],
                    "recommendations": [
                        "Develop partnerships with university hospitals to validate AI algorithms",
                        "Invest in ISO 27799 certified medical cybersecurity",
                        "Create pathology-specialized telemedicine platforms"
                    ]
                }
            },
            # Ajouter les autres secteurs avec des données spécialisées...
        }
        
        # Utiliser les données spécialisées si disponibles, sinon utiliser un template générique
        if sector_key in sector_specific_data and lang in sector_specific_data[sector_key]:
            return sector_specific_data[sector_key][lang]
        else:
            # Template générique pour les secteurs non encore détaillés
            return {
                "summary": f"Le secteur {sector_name} ({sector_info.market_size}, {sector_info.growth_rate} CAGR) est en pleine transformation digitale avec des opportunités majeures en IA et durabilité.",
                "insights": [
                    MarketInsight(f"IA dans {sector_name}", f"L'intégration de l'IA pourrait débloquer un marché de {random.uniform(1.5, 5.0):.1f}B€", 9.0, 85, "opportunity"),
                    MarketInsight("Solutions Durables", "La demande pour des options écologiques crée une nouvelle niche de marché", 8.2, 78, "opportunity"),
                    MarketInsight("Transformation Digitale", "Accélération de la digitalisation post-COVID dans tous les segments", 8.7, 82, "trend"),
                    MarketInsight("Régulation Accrue", "Nouvelles lois sectorielles augmentent les coûts de conformité de 18%", 7.6, 89, "threat")
                ],
                "recommendations": [
                    f"Investir dans une plateforme d'IA spécialisée pour {sector_name} avant Q4 2025",
                    "Lancer un audit de conformité réglementaire complet",
                    "Développer une stratégie de durabilité différenciante"
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
        
        # Zone de confiance
        fig.add_trace(go.Scatter(
            x=list(range(len(self.activity_history))),
            y=[max(self.activity_history) * 1.1] * len(self.activity_history),
            mode='lines',
            line=dict(color='rgba(16, 185, 129, 0.5)', width=1, dash='dash'),
            name='Zone Optimale',
            showlegend=False
        ))
        
        fig.update_layout(
            title={
                'text': "🧠 Activité Neuronale Temps Réel", 
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
                return f"🎯 J'ai identifié {len(opps)} opportunités majeures dans {sector_info.name}. La plus prometteuse : **{opps[0].title}** avec un impact de {opps[0].impact_score}/10 et {opps[0].confidence}% de confiance. {opps[0].description}"
        
        if any(keyword in message for keyword in ["menace", "threat", "risk", "danger"]):
            threats = [i for i in insights if i.category == "threat"]
            if threats:
                return f"⚠️ Attention ! Le risque principal identifié : **{threats[0].title}** (impact {threats[0].impact_score}/10). {threats[0].description} Je recommande une surveillance active."
        
        if any(keyword in message for keyword in ["tendance", "trend", "évolution"]):
            trends = [i for i in insights if i.category == "trend"]
            if trends:
                return f"📈 Tendance clé détectée : **{trends[0].title}** avec {trends[0].confidence}% de certitude. {trends[0].description}"
        
        if any(keyword in message for keyword in ["recommand", "conseil", "advice"]):
            recs = self.current_analysis.get("recommendations", [])
            if recs:
                return f"🎯 Ma recommandation prioritaire : {recs[0]} Voulez-vous que je détaille les autres recommandations stratégiques ?"
        
        if any(keyword in message for keyword in ["marché", "market", "taille"]):
            if sector_info:
                return f"📊 Le marché {sector_info.name} représente {sector_info.market_size} avec une croissance de {sector_info.growth_rate} CAGR. Leaders : {', '.join(sector_info.key_players[:3])}."
        
        # Réponse par défaut intelligente
        if sector_info:
            hot_trend = random.choice(sector_info.hot_trends)
            return f"🤖 Dans le secteur {sector_info.name}, je vois particulièrement {hot_trend} comme un axe stratégique majeur. Mon analyse révèle un potentiel de transformation significatif avec {self.confidence_level:.1f}% de confiance."
        
        return f"🤖 Basé sur mon analyse avec {self.confidence_level:.1f}% de confiance, le secteur {sector} présente des opportunités exceptionnelles en IA et durabilité. Que souhaitez-vous approfondir ?"

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
            "🌐 Language", 
            ["🇫🇷 Français", "🇺🇸 English"],
            key="language_selector"
        )
        new_language = "fr" if "🇫🇷" in lang_option else "en"
        if new_language != st.session_state.language:
            st.session_state.language = new_language
            st.rerun()

    # --- Layout Principal Ultra ---
    col1, col2 = st.columns([0.4, 0.6])

    # --- COLONNE 1 : Contrôle Agent + Secteurs Dépliants ---
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
            
            # Barre de progression
            if agent.status in ["thinking", "analyzing"]:
                progress = len(agent.thoughts) / 8 * 100
                st.markdown(f"""
                <div class='progress-bar'>
                    <div class='progress-fill' style='width: {progress}%;'></div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # --- SECTEURS AVEC ÉLÉMENTS DÉPLIANTS ULTRA ---
        st.markdown(f"<h3 style='color: white; text-align: center; margin: 30px 0 20px 0;'>🎯 Secteurs d'Analyse</h3>", unsafe_allow_html=True)
        
        sectors = agent.get_translation("sectors")
        selected_sector = None
        
        for sector_key, sector_name in sectors.items():
            sector_info = agent.sector_info[sector_key]
            is_expanded = sector_key in st.session_state.expanded_sectors
            
            # JavaScript pour gérer l'expansion
            expand_js = f"""
            <script>
                function toggleSector{sector_key}() {{
                    const details = document.getElementById('details-{sector_key}');
                    const arrow = document.getElementById('arrow-{sector_key}');
                    if (details.classList.contains('expanded')) {{
                        details.classList.remove('expanded');
                        arrow.classList.remove('expanded');
                    }} else {{
                        details.classList.add('expanded');
                        arrow.classList.add('expanded');
                    }}
                }}
            </script>
            """
            
            # Carte de secteur avec animation
            sector_html = f"""
            <div class='sector-card' onclick='toggleSector{sector_key}()'>
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
                    <div id='arrow-{sector_key}' class='expand-arrow {"expanded" if is_expanded else ""}'>⌄</div>
                </div>
                
                <div id='details-{sector_key}' class='sector-details {"expanded" if is_expanded else ""}'>
                    <div style='padding: 15px 0;'>
                        <p style='color: #e2e8f0; margin-bottom: 15px; line-height: 1.5; font-size: 0.9rem;'>{sector_info.description}</p>
                        
                        <div style='margin-bottom: 15px;'>
                            <h5 style='color: #60a5fa; margin-bottom: 8px; font-size: 0.9rem;'>🔥 Tendances Chaudes</h5>
                            <div style='display: flex; flex-wrap: wrap; gap: 6px;'>
                                {''.join([f'<span style="background: {sector_info.color}40; color: {sector_info.color}; padding: 4px 8px; border-radius: 12px; font-size: 0.75rem;">{trend}</span>' for trend in sector_info.hot_trends[:3]])}
                            </div>
                        </div>
                        
                        <div style='margin-bottom: 15px;'>
                            <h5 style='color: #f59e0b; margin-bottom: 8px; font-size: 0.9rem;'>🏢 Acteurs Clés</h5>
                            <p style='color: #cbd5e1; font-size: 0.8rem; margin: 0;'>{', '.join(sector_info.key_players[:3])}</p>
                        </div>
                        
                        <div>
                            <h5 style='color: #ef4444; margin-bottom: 8px; font-size: 0.9rem;'>⚠️ Défis</h5>
                            <div style='display: flex; flex-wrap: wrap; gap: 4px;'>
                                {''.join([f'<span style="background: rgba(239, 68, 68, 0.2); color: #ef4444; padding: 3px 6px; border-radius: 8px; font-size: 0.7rem;">{challenge}</span>' for challenge in sector_info.challenges[:2]])}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """
            
            st.markdown(expand_js + sector_html, unsafe_allow_html=True)
            
            # Bouton d'activation pour ce secteur
            if st.button(f"🚀 Analyser {sector_name}", key=f"analyze_{sector_key}", type="secondary"):
                selected_sector = sector_key
                break
        
        # Bouton principal d'activation
        st.markdown("<br>", unsafe_allow_html=True)
        if selected_sector or agent.status in ["idle", "completed"]:
            if st.button("🚀 ACTIVER ARIA ULTRA", type="primary", key="activate_main"):
                if not selected_sector:
                    # Prendre le premier secteur sélectionné ou FinTech par défaut
                    selected_sector = list(sectors.keys())[0]
                
                st.session_state.running_analysis = True
                st.session_state.selected_sector = selected_sector
                agent.reset()
                agent.status = "thinking"
                st.rerun()
        
        if
