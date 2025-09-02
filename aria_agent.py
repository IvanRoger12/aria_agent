"summary": "The AI sector is experiencing explosive growth with the emergence of autonomous agents and enterprise integration. Generative AI is transforming all sectors with a European market of $52B projected by 2027.",
                    "insights": [
                        MarketInsight("Autonomous AI Agents", "AI agent market explosion with 340% growth and adoption by 78% of Fortune 500 companies", 9.8, 96, "opportunity"),
                        MarketInsight("Enterprise AI", "Massive integration into business processes with average ROI of 287% over 18 months", 9.4, 89, "opportunity"),
                        MarketInsight("Edge AI Computing", "AI processing decentralization to devices with 156% edge market growth", 8.7, 83, "trend"),
                        MarketInsight("AI Act Regulation", "New European regulation creates opportunities for compliant-by-design solutions", 8.1, 91, "threat"),
                        MarketInsight("Talent War", "Critical shortage of AI developers with 423% increase in senior salaries", 9.2, 94, "threat")
                    ],
                    "recommendations": [
                        "Capitalize on AI agent wave by developing specialized sectoral solutions",
                        "Invest in edge AI to anticipate intelligent computing decentralization",
                        "Build AI Act compliance expertise to become strategic enterprise partner",
                        "Acquire or train AI teams before recruitment cost explosion"
                    ]
                }
            }
        }
    
    def get_translation(self, key: str) -> str:
        return self.translations[self.language].get(key, key)
    
    async def activate(self, sector: str) -> None:
        self.status = "thinking"
        self.thoughts = []
        self.analysis_progress = 0
        self.neural_activity = random.randint(800, 1200)
        
        thoughts = self.get_translation("thoughts")
        
        for i, thought_text in enumerate(thoughts):
            await asyncio.sleep(random.uniform(1.0, 2.0))
            
            thought = AgentThought(
                content=thought_text,
                timestamp=datetime.now(),
                confidence=random.uniform(0.8, 0.97)
            )
            
            self.thoughts.append(thought)
            self.analysis_progress = ((i + 1) / len(thoughts)) * 100
            
            if i == 3:
                self.status = "analyzing"
            elif i == len(thoughts) - 1:
                self.status = "completed"
                self.current_analysis = self.market_data.get(sector, {}).get(self.language, {})
                self.confidence_level = random.uniform(88, 97)
            
            self.neural_activity += random.randint(-50, 80)
    
    def generate_confidence_gauge(self) -> go.Figure:
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = self.confidence_level,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Confidence Level", 'font': {'size': 20, 'color': 'white'}},
            number = {'font': {'size': 36, 'color': 'white'}},
            gauge = {
                'axis': {'range': [None, 100], 'tickcolor': 'white'},
                'bar': {'color': "#667eea", 'thickness': 0.8},
                'steps': [
                    {'range': [0, 60], 'color': "rgba(239, 68, 68, 0.3)"},
                    {'range': [60, 85], 'color': "rgba(245, 158, 11, 0.3)"},
                    {'range': [85, 100], 'color': "rgba(16, 185, 129, 0.3)"}
                ],
                'threshold': {
                    'line': {'color': "#f093fb", 'width': 6},
                    'thickness': 0.8,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "white"},
            height=350,
            margin=dict(l=20, r=20, t=60, b=20)
        )
        
        return fig
    
    def generate_neural_network_viz(self) -> go.Figure:
        n_nodes = 25
        x = [random.uniform(0, 10) for _ in range(n_nodes)]
        y = [random.uniform(0, 8) for _ in range(n_nodes)]
        
        edge_x = []
        edge_y = []
        
        for i in range(n_nodes):
            for j in range(i+1, min(i+5, n_nodes)):
                if random.random() > 0.7:
                    edge_x.extend([x[i], x[j], None])
                    edge_y.extend([y[i], y[j], None])
        
        # Connections avec gradient
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1.5, color='rgba(102, 126, 234, 0.6)'),
            hoverinfo='none',
            mode='lines'
        )
        
        # Noeuds avec différentes tailles selon l'activité
        node_sizes = [random.uniform(8, 20) if self.status == "analyzing" else random.uniform(6, 12) for _ in range(n_nodes)]
        node_colors = ['#667eea' if random.random() > 0.3 else '#f093fb' for _ in range(n_nodes)]
        
        node_trace = go.Scatter(
            x=x, y=y,
            mode='markers',
            hoverinfo='none',
            marker=dict(
                size=node_sizes,
                color=node_colors,
                line=dict(width=2, color='rgba(255, 255, 255, 0.3)'),
                opacity=0.8
            )
        )
        
        fig = go.Figure(data=[edge_trace, node_trace])
        fig.update_layout(
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=250
        )
        
        return fig

def main():
    if 'agent' not in st.session_state:
        st.session_state.agent = ARIAAgent()
    
    if 'language' not in st.session_state:
        st.session_state.language = 'fr'
    
    agent = st.session_state.agent
    agent.language = st.session_state.language
    
    # Header Ultra Premium
    st.markdown(f"""
    <div class='premium-header'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div style='flex: 1;'>
                <h1 class='title-gradient'>🧠 {agent.get_translation('agent_name')}</h1>
                <p class='subtitle-glow'>{agent.get_translation('agent_desc')}</p>
                <div style='display: flex; gap: 20px; margin-top: 20px; font-size: 0.9rem; color: #64748b;'>
                    <span>💡 Neural Activity: {agent.neural_activity}</span>
                    <span>🔍 Sources: 1,247</span>
                    <span>⚡ Real-time Analysis</span>
                </div>
            </div>
            <div style='text-align: right;'>
                <div style='margin-bottom: 15px;'>
                    <span style='color: #a3a3a3; font-size: 0.9rem; margin-right: 10px;'>Language</span>
                </div>
    """, unsafe_allow_html=True)
    
    # Language selector inline
    lang_col1, lang_col2 = st.columns([3, 1])
    with lang_col2:
        lang = st.selectbox("", ["🇫🇷 Français", "🇺🇸 English"], key="lang_select", label_visibility="collapsed")
        new_language = "fr" if "Français" in lang else "en"
        if new_language != st.session_state.language:
            st.session_state.language = new_language
            st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Layout principal
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Agent Control Panel Premium
        st.markdown(f"""
        <div class='premium-card'>
            <h3 style='color: white; text-align: center; margin-bottom: 30px; font-size: 1.4rem; font-weight: 600;'>
                🤖 Agent Control Panel
            </h3>
            <div style='text-align: center; margin: 30px 0;'>
                <div class='agent-avatar {"active" if agent.status != "idle" else ""}'>
                    <span style='font-size: 3rem;'>🤖</span>
                </div>
                <div class='status-dot {agent.status}'></div>
                <h4 style='color: white; margin: 15px 0 5px 0; font-size: 1.2rem;'>{agent.get_translation("agent_name")}</h4>
                <p style='color: #94a3b8; font-size: 0.95rem; margin: 0;'>Autonomous Intelligence System</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Status display premium
        status_text = agent.get_translation(f"status_{agent.status}")
        st.markdown(f"""
        <div style='background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 16px; padding: 20px; margin: 25px 0; text-align: center; backdrop-filter: blur(10px);'>
            <p style='color: #e2e8f0; margin: 0; font-weight: 500; font-size: 1rem;'>{status_text}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress bar si actif
        if agent.status != "idle" and hasattr(agent, 'analysis_progress'):
            st.markdown(f"""
            <div class='progress-premium'>
                <div class='progress-fill' style='width: {agent.analysis_progress}%'></div>
            </div>
            <p style='text-align: center; color: #94a3b8; font-size: 0.85rem; margin: 10px 0;'>
                Analysis Progress: {agent.analysis_progress:.1f}%
            </p>
            """, unsafe_allow_html=True)
        
        # Sector selection
        st.markdown("<p style='color: white; font-weight: 500; margin: 25px 0 15px 0; font-size: 1.1rem;'>🎯 Target Sector</p>", unsafe_allow_html=True)
        sectors = agent.get_translation("sectors")
        selected_sector = st.selectbox(
            "Select sector",
            list(sectors.keys()),
            format_func=lambda x: sectors[x],
            label_visibility="collapsed"
        )
        
        # Activation button
        st.markdown("<div style='margin: 30px 0;'>", unsafe_allow_html=True)
        if agent.status in ["idle", "completed"]:
            if st.button("🚀 Activate ARIA Agent", key="activate_btn", type="primary"):
                with st.spinner("🤖 Agent activation in progress..."):
                    try:
                        loop = asyncio.get_event_loop()
                    except RuntimeError:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                    
                    loop.run_until_complete(agent.activate(selected_sector))
                    st.rerun()
        else:
            if st.button("⏹️ Stop Agent", key="stop_btn"):
                agent.status = "idle"
                agent.thoughts = []
                agent.current_analysis = None
                agent.analysis_progress = 0
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Real-time metrics premium
        if agent.status != "idle":
            st.markdown("<h4 style='color: white; margin: 25px 0 20px 0; font-size: 1.2rem;'>📊 Real-time Metrics</h4>", unsafe_allow_html=True)
            
            metrics = [
                ("Neural Activity", f"{agent.neural_activity}", "🧠"),
                ("Data Sources", "1,247", "📊"),
                ("Insights Generated", f"{len([t for t in agent.thoughts if t.confidence > 0.85])}", "💡"),
                ("Confidence", f"{agent.confidence_level:.1f}%" if agent.confidence_level > 0 else "N/A", "⚡")
            ]
            
            for label, value, icon in metrics:
                st.markdown(f"""
                <div class='metric-premium'>
                    <div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;'>
                        <span style='color: #94a3b8; font-size: 0.85rem;'>{label}</span>
                        <span style='font-size: 1.2rem;'>{icon}</span>
                    </div>
                    <p style='color: white; margin: 0; font-size: 1.4rem; font-weight: 700;'>{value}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Neural network visualization
        if agent.status in ["thinking", "analyzing"]:
            st.markdown("""
            <div class='neural-container'>
                <h4 style='color: white; margin-bottom: 20px; text-align: center;'>🧠 Neural Network Activity</h4>
            </div>
            """, unsafe_allow_html=True)
            neural_fig = agent.generate_neural_network_viz()
            st.plotly_chart(neural_fig, use_container_width=True)
    
    with col2:
        # Zone principale - Pensées et résultats
        if agent.status != "idle" and agent.thoughts:
            st.markdown("""
            <div class='premium-card'>
                <h3 style='color: white; margin-bottom: 25px; font-size: 1.4rem; display: flex; align-items: center; gap: 10px;'>
                    🧠 Agent Thought Process
                    <div style='margin-left: auto; display: flex; gap: 8px;'>
                        <div style='width: 8px; height: 8px; background: #10b981; border-radius: 50%; animation: statusBlink 1s ease-in-out infinite;'></div>
                        <div style='width: 8px; height: 8px; background: #3b82f6; border-radius: 50%; animation: statusBlink 1.2s ease-in-out infinite;'></div>
                        <div style='width: 8px; height: 8px; background: #8b5cf6; border-radius: 50%; animation: statusBlink 1.4s ease-in-out infinite;'></div>
                    </div>
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Affichage des pensées avec animations
            for i, thought in enumerate(agent.thoughts):
                st.markdown(f"""
                <div class='thought-bubble' style='animation-delay: {i * 0.1}s;'>
                    <div style='display: flex; align-items: flex-start; gap: 15px;'>
                        <div style='background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);'>
                            <span style='font-size: 1.2rem;'>🤖</span>
                        </div>
                        <div style='flex: 1;'>
                            <p style='color: white; margin: 0 0 8px 0; font-size: 1rem; font-weight: 500; line-height: 1.4;'>{thought.content}</p>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <span style='color: #94a3b8; font-size: 0.8rem;'>{thought.timestamp.strftime("%H:%M:%S")}</span>
                                <span style='color: #10b981; font-size: 0.8rem; background: rgba(16, 185, 129, 0.1); padding: 2px 8px; border-radius: 12px;'>
                                    {thought.confidence:.1%} confidence
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Résultats d'analyse premium
        if agent.current_analysis and agent.status == "completed":
            st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
            
            # Executive Summary premium
            st.markdown(f"""
            <div class='premium-card'>
                <h3 style='color: white; margin-bottom: 25px; font-size: 1.4rem; display: flex; align-items: center; gap: 10px;'>
                    📋 Executive Summary
                    <span style='margin-left: auto; background: rgba(16, 185, 129, 0.2); color: #10b981; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem;'>
                        High Confidence
                    </span>
                </h3>
                <div style='background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(139, 92, 246, 0.15)); border: 1px solid rgba(59, 130, 246, 0.3); border-left: 4px solid #667eea; padding: 25px; border-radius: 16px; backdrop-filter: blur(10px);'>
                    <p style='color: #e2e8f0; margin: 0; font-size: 1.1rem; line-height: 1.6;'>{agent.current_analysis.get("summary", "")}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Confidence gauge
            if agent.confidence_level > 0:
                st.markdown("""
                <div class='premium-card'>
                    <h3 style='color: white; margin-bottom: 25px; text-align: center; font-size: 1.4rem;'>📊 Analysis Confidence</h3>
                </div>
                """, unsafe_allow_html=True)
                confidence_fig = agent.generate_confidence_gauge()
                st.plotly_chart(confidence_fig, use_container_width=True)
            
            # Insights premium
            insights = agent.current_analysis.get("insights", [])
            if insights:
                st.markdown("""
                <div class='premium-card'>
                    <h3 style='color: white; margin-bottom: 25px; font-size: 1.4rem;'>🎯 Strategic Insights</h3>
                </div>
                """, unsafe_allow_html=True)
                
                opportunities = [i for i in insights if i.category == "opportunity"]
                threats = [i for i in insights if i.category == "threat"]
                trends = [i for i in insights if i.category == "trend"]
                
                if opportunities:
                    st.markdown("<h4 style='color: #10b981; margin: 25px 0 20px 0; font-size: 1.2rem; display: flex; align-items: center; gap: 8px;'>💡 Market Opportunities</h4>", unsafe_allow_html=True)
                    for opp in opportunities:
                        st.markdown(f"""
                        <div class='insight-card opportunity'>
                            <h5 style='color: white; margin: 0 0 12px 0; font-size: 1.1rem; font-weight: 600;'>{opp.title}</h5>
                            <p style='color: #d1d5db; margin: 0 0 15px 0; font-size: 0.95rem; line-height: 1.5;'>{opp.description}</p>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <div style='display: flex; gap: 20px;'>
                                    <span style='color: #94a3b8; font-size: 0.85rem;'>Impact: <strong style='color: #10b981;'>{opp.impact_score}/10</strong></span>
                                    <span style='color: #94a3b8; font-size: 0.85rem;'>Confidence: <strong style='color: #10b981;'>{opp.confidence}%</strong></span>
                                </div>
                                <div style='background: rgba(16, 185, 129, 0.2); color: #10b981; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 500;'>
                                    High Priority
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                if threats:
                    st.markdown("<h4 style='color: #ef4444; margin: 25px 0 20px 0; font-size: 1.2rem; display: flex; align-items: center; gap: 8px;'>⚠️ Strategic Threats</h4>", unsafe_allow_html=True)
                    for threat in threats:
                        st.markdown(f"""
                        <div class='insight-card threat'>
                            <h5 style='color: white; margin: 0 0 12px 0; font-size: 1.1rem; font-weight: 600;'>{threat.title}</h5>
                            <p style='color: #d1d5db; margin: 0 0 15px 0; font-size: 0.95rem; line-height: 1.5;'>{threat.description}</p>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <div style='display: flex; gap: 20px;'>
                                    <span style='color: #94a3b8; font-size: 0.85rem;'>Impact: <strong style='color: #ef4444;'>{threat.impact_score}/10</strong></span>
                                    <span style='color: #94a3b8; font-size: 0.85rem;'>Confidence: <strong style='color: #ef4444;'>{threat.confidence}%</strong></span>
                                </div>
                                <div style='background: rgba(239, 68, 68, 0.2); color: #ef4444; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 500;'>
                                    Monitor
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                if trends:
                    st.markdown("<h4 style='color: #8b5cf6; margin: 25px 0 20px 0; font-size: 1.2rem; display: flex; align-items: center; gap: 8px;'>📈 Emerging Trends</h4>", unsafe_allow_html=True)
                    for trend in trends:
                        st.markdown(f"""
                        <div class='insight-card trend'>
                            <h5 style='color: white; margin: 0 0 12px 0; font-size: 1.1rem; font-weight: 600;'>{trend.title}</h5>
                            <p style='color: #d1d5db; margin: 0 0 15px 0; font-size: 0.95rem; line-height: 1.5;'>{trend.description}</p>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <div style='display: flex; gap: 20px;'>
                                    <span style='color: #94a3b8; font-size: 0.85rem;'>Impact: <strong style='color: #8b5cf6;'>{trend.impact_score}/10</strong></span>
                                    <span style='color: #94a3b8; font-size: 0.85rem;'>Confidence: <strong style='color: #8b5cf6;'>{trend.confidence}%</strong></span>
                                </div>
                                <div style='background: rgba(139, 92, 246, 0.2); color: #8b5cf6; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 500;'>
                                    Track
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Recommendations premium
            recommendations = agent.current_analysis.get("recommendations", [])
            if recommendations:
                st.markdown("""
                <div class='premium-card'>
                    <h3 style='color: white; margin-bottom: 25px; font-size: 1.4rem; display: flex; align-items: center; gap: 10px;'>
                        🎯 AI Strategic Recommendations
                        <span style='margin-left: auto; background: rgba(139, 92, 246, 0.2); color: #8b5cf6; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem;'>
                            Actionable
                        </span>
                    </h3>
                </div>
                """, unsafe_allow_html=True)
                
                for i, rec in enumerate(recommendations, 1):
                    st.markdown(f"""
                    <div style='display: flex; align-items: flex-start; gap: 20px; background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.2); border-radius: 16px; padding: 24px; margin: 16px 0; backdrop-filter: blur(10px);'>
                        <div style='background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);'>
                            <span style='color: white; font-weight: bold; font-size: 1.1rem;'>{i}</span>
                        </div>
                        <div style='flex: 1;'>
                            <p style='color: #e2e8f0; margin: 0; font-size: 1rem; line-height: 1.6;'>{rec}</p>
                            <div style='margin-top: 12px; display: flex; gap: 12px;'>
                                <span style='background: rgba(16, 185, 129, 0.2); color: #10b981; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem;'>High Impact</span>
                                <span style='background: rgba(59, 130, 246, 0.2); color: #3b82f6; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem;'>Strategic</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Export actions premium
            st.markdown("""
            <div class='premium-card'>
                <h3 style='color: white; margin-bottom: 25px; font-size: 1.4rem;'>📤 Export & Actions</h3>
                <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;'>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📄 Export Report", key="export_btn"):
                    report_content = f"""
🤖 ARIA - STRATEGIC INTELLIGENCE REPORT
═══════════════════════════════════════════════
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Sector: {selected_sector}
Confidence Level: {agent.confidence_level:.1f}%
Neural Activity: {agent.neural_activity} nodes

EXECUTIVE SUMMARY:
{agent.current_analysis.get('summary', '')}

KEY STRATEGIC INSIGHTS:
═══════════════════════════════════════════════"""
                    
                    for insight in insights:
                        report_content += f"\n\n🎯 {insight.title.upper()}"
                        report_content += f"\n   Category: {insight.category.title()}"
                        report_content += f"\n   Impact Score: {insight.impact_score}/10"
                        report_content += f"\n   Confidence: {insight.confidence}%"
                        report_content += f"\n   Description: {insight.description}"
                    
                    report_content += "\n\nAI STRATEGIC RECOMMENDATIONS:\n═══════════════════════════════════════════════"
                    for i, rec in enumerate(recommendations, 1):
                        report_content += f"\n\n{i}. {rec}"
                    
                    report_content += f"\n\n═══════════════════════════════════════════════\nGenerated by ARIA - Autonomous Research & Intelligence Agent\nConfidence Level: {agent.confidence_level:.1f}% | Neural Network: {agent.neural_activity} active nodes"
                    
                    st.download_button(
                        label="⬇️ Download Report",
                        data=import streamlit as st
import json
import time
import random
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional
import asyncio
import requests
from dataclasses import dataclass
import base64
from io import BytesIO

# Configuration de la page
st.set_page_config(
    page_title="🤖 ARIA - AI Strategic Intelligence Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Ultra Premium avec animations d'arrière-plan
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #0f1419 0%, #1a1625 25%, #2d1b69 50%, #1a1625 75%, #0f1419 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        color: white;
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
        position: relative;
        overflow: hidden;
    }
    
    /* Animations d'arrière-plan */
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(120, 219, 255, 0.1) 0%, transparent 50%);
        animation: floatingOrbs 20s ease-in-out infinite;
        pointer-events: none;
        z-index: 1;
    }
    
    .main::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: url('data:image/svg+xml,<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"><g fill="none" fill-rule="evenodd"><g fill="%234f46e5" fill-opacity="0.05"><circle cx="7" cy="7" r="1"/><circle cx="27" cy="7" r="1"/><circle cx="47" cy="7" r="1"/><circle cx="7" cy="27" r="1"/><circle cx="27" cy="27" r="1"/><circle cx="47" cy="27" r="1"/><circle cx="7" cy="47" r="1"/><circle cx="27" cy="47" r="1"/><circle cx="47" cy="47" r="1"/></g></g></svg>');
        animation: gridMove 30s linear infinite;
        pointer-events: none;
        z-index: 1;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    @keyframes floatingOrbs {
        0%, 100% { transform: translate(0px, 0px) scale(1); }
        33% { transform: translate(30px, -30px) scale(1.1); }
        66% { transform: translate(-20px, 20px) scale(0.9); }
    }
    
    @keyframes gridMove {
        0% { transform: translateX(0) translateY(0); }
        100% { transform: translateX(60px) translateY(60px); }
    }
    
    /* Container principal avec backdrop blur */
    .stApp > div > div {
        position: relative;
        z-index: 2;
        backdrop-filter: blur(1px);
    }
    
    /* Header ultra premium */
    .premium-header {
        background: rgba(15, 20, 25, 0.8);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .premium-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.5), transparent);
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { opacity: 0; }
        50% { opacity: 1; }
    }
    
    /* Selectbox améliorée */
    .stSelectbox > div > div {
        background: rgba(15, 20, 25, 0.9) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: rgba(139, 92, 246, 0.6) !important;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.2) !important;
    }
    
    /* Boutons ultra premium */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 16px !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 16px 32px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Cards ultra premium */
    .premium-card {
        background: rgba(15, 20, 25, 0.7);
        backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 32px;
        margin: 20px 0;
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        transition: all 0.4s ease;
    }
    
    .premium-card:hover {
        transform: translateY(-5px);
        box-shadow: 
            0 30px 80px rgba(0, 0, 0, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    
    /* Agent Avatar Premium */
    .agent-avatar {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 20px;
        position: relative;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .agent-avatar.active {
        animation: agentPulse 2s ease-in-out infinite;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.5);
    }
    
    .agent-avatar::before {
        content: '';
        position: absolute;
        top: -5px;
        left: -5px;
        right: -5px;
        bottom: -5px;
        border-radius: 50%;
        background: linear-gradient(45deg, #667eea, #764ba2, #f093fb, #667eea);
        background-size: 300% 300%;
        animation: gradientRotate 3s linear infinite;
        z-index: -1;
        opacity: 0;
    }
    
    .agent-avatar.active::before {
        opacity: 1;
    }
    
    @keyframes agentPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes gradientRotate {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Status indicator amélioré */
    .status-dot {
        position: absolute;
        bottom: 10px;
        right: 10px;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        border: 3px solid rgba(15, 20, 25, 0.8);
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
    }
    
    .status-dot.idle { background: #6b7280; }
    .status-dot.thinking { 
        background: #f59e0b; 
        animation: statusBlink 1.5s ease-in-out infinite;
        box-shadow: 0 0 20px rgba(245, 158, 11, 0.5);
    }
    .status-dot.analyzing { 
        background: #3b82f6; 
        animation: statusBlink 1s ease-in-out infinite;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
    }
    .status-dot.completed { 
        background: #10b981;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.5);
    }
    
    @keyframes statusBlink {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.1); }
    }
    
    /* Thought bubbles premium */
    .thought-bubble {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-left: 4px solid #3b82f6;
        border-radius: 16px;
        padding: 20px;
        margin: 16px 0;
        backdrop-filter: blur(10px);
        animation: slideInLeft 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .thought-bubble::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.1), transparent);
        transform: translateX(-100%);
        animation: thoughtShimmer 2s ease-in-out infinite;
    }
    
    @keyframes slideInLeft {
        0% {
            opacity: 0;
            transform: translateX(-30px);
        }
        100% {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes thoughtShimmer {
        0% { transform: translateX(-100%); }
        50% { transform: translateX(100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Métriques premium */
    .metric-premium {
        background: rgba(15, 20, 25, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin: 12px 0;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-premium::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.5), transparent);
    }
    
    .metric-premium:hover {
        border-color: rgba(139, 92, 246, 0.3);
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    
    /* Insights cards */
    .insight-card {
        background: rgba(15, 20, 25, 0.8);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 24px;
        margin: 16px 0;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .insight-card.opportunity {
        border: 1px solid rgba(16, 185, 129, 0.3);
        box-shadow: 0 0 30px rgba(16, 185, 129, 0.1);
    }
    
    .insight-card.threat {
        border: 1px solid rgba(239, 68, 68, 0.3);
        box-shadow: 0 0 30px rgba(239, 68, 68, 0.1);
    }
    
    .insight-card.trend {
        border: 1px solid rgba(139, 92, 246, 0.3);
        box-shadow: 0 0 30px rgba(139, 92, 246, 0.1);
    }
    
    .insight-card:hover {
        transform: translateY(-3px) scale(1.01);
    }
    
    /* Progress bar améliorée */
    .progress-premium {
        background: rgba(15, 20, 25, 0.8);
        border-radius: 20px;
        padding: 4px;
        margin: 20px 0;
        box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    .progress-fill {
        height: 12px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 16px;
        transition: width 0.3s ease;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
        position: relative;
        overflow: hidden;
    }
    
    .progress-fill::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        animation: progressShine 2s ease-in-out infinite;
    }
    
    @keyframes progressShine {
        0% { transform: translateX(-100%); }
        50% { transform: translateX(100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Typography améliorée */
    .title-gradient {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.1;
        text-shadow: 0 0 40px rgba(102, 126, 234, 0.3);
    }
    
    .subtitle-glow {
        color: #a3a3a3;
        font-size: 1.3rem;
        font-weight: 400;
        margin: 0;
        text-shadow: 0 0 20px rgba(163, 163, 163, 0.2);
    }
    
    /* Neural network visualization premium */
    .neural-container {
        background: rgba(15, 20, 25, 0.9);
        border-radius: 20px;
        padding: 24px;
        position: relative;
        overflow: hidden;
        min-height: 200px;
    }
    
    .neural-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 30% 30%, rgba(59, 130, 246, 0.1) 0%, transparent 30%),
            radial-gradient(circle at 70% 70%, rgba(139, 92, 246, 0.1) 0%, transparent 30%);
        animation: neuralGlow 4s ease-in-out infinite alternate;
    }
    
    @keyframes neuralGlow {
        0% { opacity: 0.3; }
        100% { opacity: 0.7; }
    }
    
    /* Footer premium */
    .footer-premium {
        background: rgba(15, 20, 25, 0.9);
        backdrop-filter: blur(30px);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding: 40px 0;
        margin-top: 60px;
        text-align: center;
        position: relative;
    }
    
    .footer-premium::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.5), transparent);
    }
    
    /* Scrollbar personnalisée */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 20, 25, 0.5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #f093fb);
    }
    
    /* Responsive améliorations */
    @media (max-width: 768px) {
        .title-gradient { font-size: 2.5rem; }
        .subtitle-glow { font-size: 1.1rem; }
        .premium-card { padding: 20px; margin: 12px 0; }
        .agent-avatar { width: 100px; height: 100px; }
    }
</style>
""", unsafe_allow_html=True)

@dataclass
class AgentThought:
    content: str
    timestamp: datetime
    thought_type: str = "analysis"
    confidence: float = 0.0

@dataclass
class MarketInsight:
    title: str
    description: str
    impact_score: float
    confidence: float
    category: str

class ARIAAgent:
    """ARIA - Autonomous Research & Intelligence Agent Premium"""
    
    def __init__(self, language: str = "fr"):
        self.language = language
        self.status = "idle"
        self.thoughts = []
        self.current_analysis = None
        self.confidence_level = 0.0
        self.neural_activity = 0
        self.analysis_progress = 0
        
        self.translations = {
            "fr": {
                "agent_name": "ARIA",
                "agent_desc": "Agent de Recherche et Intelligence Autonome",
                "status_idle": "🤖 Agent en veille - Prêt à analyser",
                "status_thinking": "🧠 Réflexion stratégique en cours...",
                "status_analyzing": "⚡ Analyse multi-dimensionnelle active",
                "status_completed": "✨ Mission accomplie - Insights générés",
                "sectors": {
                    "FinTech": "Technologies Financières",
                    "HealthTech": "Technologies Médicales",
                    "SaaS": "Logiciels en Service",
                    "E-commerce": "Commerce Électronique",
                    "PropTech": "Technologies Immobilières",
                    "EdTech": "Technologies Éducatives",
                    "AI": "Intelligence Artificielle",
                    "Crypto": "Cryptomonnaies & Blockchain"
                },
                "thoughts": [
                    "🔍 Initialisation des capteurs de marché avancés...",
                    "🧠 Activation des réseaux neuronaux sectoriels...",
                    "📊 Ingestion de 1,247 sources de données temps réel...",
                    "⚡ Traitement par algorithmes de deep learning...",
                    "🎯 Corrélation des signaux faibles détectés...",
                    "📈 Modélisation prédictive des tendances émergentes...",
                    "🔬 Analyse des patterns concurrentiels...",
                    "🤖 Génération d'insights actionnables...",
                    "✨ Synthèse stratégique finalisée avec confiance élevée"
                ]
            },
            "en": {
                "agent_name": "ARIA",
                "agent_desc": "Autonomous Research & Intelligence Agent",
                "status_idle": "🤖 Agent on standby - Ready to analyze",
                "status_thinking": "🧠 Strategic thinking in progress...",
                "status_analyzing": "⚡ Multi-dimensional analysis active",
                "status_completed": "✨ Mission accomplished - Insights generated",
                "sectors": {
                    "FinTech": "Financial Technologies",
                    "HealthTech": "Health Technologies",
                    "SaaS": "Software as a Service",
                    "E-commerce": "Electronic Commerce",
                    "PropTech": "Property Technologies",
                    "EdTech": "Education Technologies",
                    "AI": "Artificial Intelligence",
                    "Crypto": "Cryptocurrency & Blockchain"
                },
                "thoughts": [
                    "🔍 Initializing advanced market sensors...",
                    "🧠 Activating sectoral neural networks...",
                    "📊 Ingesting 1,247 real-time data sources...",
                    "⚡ Processing via deep learning algorithms...",
                    "🎯 Correlating detected weak signals...",
                    "📈 Predictive modeling of emerging trends...",
                    "🔬 Analyzing competitive patterns...",
                    "🤖 Generating actionable insights...",
                    "✨ Strategic synthesis completed with high confidence"
                ]
            }
        }
        
        # Données d'analyse enrichies
        self.market_data = {
            "FinTech": {
                "fr": {
                    "summary": "Le secteur FinTech connaît une révolution avec l'émergence d'agents IA conversationnels et l'intégration massive de technologies blockchain. Les régulations MiCA créent un cadre favorable aux acteurs innovants et conformes.",
                    "insights": [
                        MarketInsight("IA Conversationnelle Bancaire", "L'intégration d'agents IA dans les services bancaires représente une opportunité de 4.7B€ d'ici 2027 avec 89% de taux d'adoption prévu", 9.5, 91, "opportunity"),
                        MarketInsight("DeFi Institutionnelle", "Les institutions financières adoptent massivement la DeFi avec un potentiel de 2.8B€ et +156% de croissance annuelle", 8.8, 87, "opportunity"),
                        MarketInsight("Super-Apps Européennes", "Émergence de plateformes financières unifiées avec 73% d'intention d'usage chez les millennials", 8.2, 79, "trend"),
                        MarketInsight("Durcissement Réglementaire", "MiCA et nouvelles régulations créent des barrières d'entrée mais favorisent les acteurs conformes (+34% avantage concurrentiel)", 7.9, 94, "threat"),
                        MarketInsight("Consolidation Accélérée", "Vague d'acquisitions prévue Q2-Q3 2025 avec 23+ opérations majeures identifiées", 9.1, 88, "trend")
                    ],
                    "recommendations": [
                        "Investir massivement dans l'IA conversationnelle avant Q2 2025 pour capturer 67% du marché adressable",
                        "Préparer la conformité MiCA 8 mois avant les concurrents pour un avantage first-mover de 2.3M€",
                        "Acquérir des talents blockchain senior avant la pénurie annoncée (salaires +45% d'ici fin 2025)",
                        "Développer une stratégie super-app pour unifier 5+ services financiers sous une plateforme unique"
                    ]
                },
                "en": {
                    "summary": "The FinTech sector is experiencing a revolution with the emergence of conversational AI agents and massive blockchain technology integration. MiCA regulations create a favorable framework for innovative and compliant players.",
                    "insights": [
                        MarketInsight("Conversational Banking AI", "AI agent integration in banking services represents a $5.2B opportunity by 2027 with 89% adoption rate projected", 9.5, 91, "opportunity"),
                        MarketInsight("Institutional DeFi", "Traditional financial institutions are massively adopting DeFi with $3.1B potential and +156% annual growth", 8.8, 87, "opportunity"),
                        MarketInsight("European Super-Apps", "Emergence of unified financial platforms with 73% usage intention among millennials", 8.2, 79, "trend"),
                        MarketInsight("Regulatory Tightening", "MiCA and new regulations create entry barriers but favor compliant players (+34% competitive advantage)", 7.9, 94, "threat"),
                        MarketInsight("Accelerated Consolidation", "Wave of acquisitions expected Q2-Q3 2025 with 23+ major operations identified", 9.1, 88, "trend")
                    ],
                    "recommendations": [
                        "Invest heavily in conversational AI before Q2 2025 to capture 67% of addressable market",
                        "Prepare MiCA compliance 8 months ahead of competitors for $2.5M first-mover advantage",
                        "Acquire senior blockchain talent before predicted shortage (salaries +45% by end 2025)",
                        "Develop super-app strategy to unify 5+ financial services under single platform"
                    ]
                }
            },
            "AI": {
                "fr": {
                    "summary": "Le secteur IA connaît une croissance explosive avec l'émergence d'agents autonomes et l'intégration enterprise. L'IA générative transforme tous les secteurs avec un marché européen de 47B€ prévu d'ici 2027.",
                    "insights": [
                        MarketInsight("Agents IA Autonomes", "Explosion du marché des agents IA avec 340% de croissance et adoption par 78% des entreprises Fortune 500", 9.8, 96, "opportunity"),
                        MarketInsight("IA Enterprise", "Intégration massive dans les processus métier avec ROI moyen de 287% sur 18 mois", 9.4, 89, "opportunity"),
                        MarketInsight("Edge AI Computing", "Décentralisation du processing IA vers les devices avec 156% de croissance du marché edge", 8.7, 83, "trend"),
                        MarketInsight("Régulation IA Act", "Nouvelle réglementation européenne crée des opportunités pour les solutions compliant-by-design", 8.1, 91, "threat"),
                        MarketInsight("Talent War", "Pénurie critique de développeurs IA avec 423% d'augmentation des salaires seniors", 9.2, 94, "threat")
                    ],
                    "recommendations": [
                        "Capitaliser sur la vague d'agents IA en développant des solutions sectorielles spécialisées",
                        "Investir dans l'edge AI pour anticiper la décentralisation du computing intelligent",
                        "Créer une expertise IA Act compliance pour devenir partenaire stratégique des enterprises",
                        "Acquérir ou former des équipes IA avant l'explosion des coûts de recrutement"
                    ]
                },
                "en": {
                    "summary": "The AI sector is experiencing explosive growth with the emergence of autonomous agents
