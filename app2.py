import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="AI Tools KPI Dashboard for PMO",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #3B82F6;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f8f9fa;
        border-left: 5px solid #3B82F6;
        margin-bottom: 1rem;
    }
    .kpi-box {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem;
    }
    .tooltip {
        cursor: help;
        border-bottom: 1px dotted #666;
    }
</style>
""", unsafe_allow_html=True)

# Title and Introduction
st.markdown('<h1 class="main-header">📊 AI Tools Success Dashboard for PMO</h1>', unsafe_allow_html=True)
st.markdown("""
<div class="card">
    <p><b>Welcome!</b> This dashboard helps you measure how well your AI tools are performing in your Project Management Office (PMO).</p>
    <p>Think of it as a report card for your AI tools - showing what's working and where you can improve.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for navigation and input
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2091/2091663.png", width=100)
    st.title("Navigation")
    
    section = st.radio(
        "Choose what you want to do:",
        ["📈 View Current KPIs", "➕ Add New AI Tool", "📊 Calculate ROI", "🎯 Set Targets", "📋 View Recommendations"]
    )
    
    st.markdown("---")
    st.markdown("### Quick Guide")
    st.info("""
    **KPI** = Key Performance Indicator  
    **ROI** = Return on Investment  
    
    Simply follow the steps to:
    1. Add your AI tools
    2. Set targets
    3. Track performance
    4. See results
    """)

# Sample data initialization
if 'ai_tools' not in st.session_state:
    st.session_state.ai_tools = [
        {
            "name": "AI Task Assistant",
            "category": "Productivity",
            "investment": 50000,
            "date_implemented": "2024-01-15",
            "kpis": {
                "Time Saved": {"current": 120, "target": 100, "unit": "hours/week"},
                "Accuracy": {"current": 92, "target": 90, "unit": "%"},
                "User Adoption": {"current": 75, "target": 80, "unit": "%"},
                "Cost Reduction": {"current": 15000, "target": 12000, "unit": "$/month"}
            }
        },
        {
            "name": "Risk Predictor",
            "category": "Risk Management",
            "investment": 75000,
            "date_implemented": "2024-02-01",
            "kpis": {
                "Risk Detection": {"current": 85, "target": 80, "unit": "%"},
                "False Alarms": {"current": 15, "target": 20, "unit": "%"},
                "Time to Detect": {"current": 2, "target": 3, "unit": "days"},
                "Cost Avoided": {"current": 50000, "target": 40000, "unit": "$/quarter"}
            }
        }
    ]

# Main content based on selection
if section == "📈 View Current KPIs":
    st.markdown('<h2 class="sub-header">Current AI Tools Performance</h2>', unsafe_allow_html=True)
    
    # Tool selection
    tool_names = [tool["name"] for tool in st.session_state.ai_tools]
    selected_tool_name = st.selectbox("Select AI Tool to View:", tool_names)
    
    if selected_tool_name:
        selected_tool = next(tool for tool in st.session_state.ai_tools if tool["name"] == selected_tool_name)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Tool Name", selected_tool["name"])
        with col2:
            st.metric("Category", selected_tool["category"])
        with col3:
            st.metric("Investment", f"${selected_tool['investment']:,}")
        
        st.markdown("### 📊 Performance Indicators")
        
        # Create columns for KPIs
        kpis = selected_tool["kpis"]
        cols = st.columns(len(kpis))
        
        for idx, (kpi_name, kpi_data) in enumerate(kpis.items()):
            with cols[idx]:
                delta = kpi_data["current"] - kpi_data["target"]
                delta_text = f"{'+' if delta > 0 else ''}{delta:.1f} vs target"
                
                st.metric(
                    label=kpi_name,
                    value=f"{kpi_data['current']} {kpi_data['unit']}",
                    delta=delta_text,
                    delta_color="normal" if delta >= 0 else "inverse"
                )
        
        # Visualization
        st.markdown("### 📈 Performance Trend")
        
        # Create sample trend data
        months = pd.date_range(start='2024-01-01', periods=6, freq='M')
        trend_data = pd.DataFrame({
            'Month': months,
            'Performance': np.random.rand(6) * 20 + 80  # Random performance between 80-100
        })
        
        fig = px.line(trend_data, x='Month', y='Performance', 
                     title=f"{selected_tool_name} Performance Over Time",
                     markers=True)
        fig.update_layout(yaxis_title="Performance Score", xaxis_title="Month")
        st.plotly_chart(fig, use_container_width=True)

elif section == "➕ Add New AI Tool":
    st.markdown('<h2 class="sub-header">Add a New AI Tool to Track</h2>', unsafe_allow_html=True)
    
    with st.form("add_tool_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            tool_name = st.text_input("AI Tool Name", placeholder="e.g., AI Reporting Assistant")
            category = st.selectbox("Category", 
                                   ["Productivity", "Risk Management", "Reporting", 
                                    "Scheduling", "Budgeting", "Other"])
            investment = st.number_input("Total Investment ($)", min_value=0, value=10000)
        
        with col2:
            implementation_date = st.date_input("Implementation Date")
            team_size = st.number_input("Team Size Using Tool", min_value=1, value=5)
            description = st.text_area("Brief Description")
        
        st.markdown("### 📝 Add Your First KPIs")
        
        kpi_cols = st.columns(2)
        kpis_to_add = {}
        
        with kpi_cols[0]:
            st.subheader("KPI 1")
            kpi1_name = st.text_input("Name", key="kpi1_name", placeholder="e.g., Time Saved")
            kpi1_current = st.number_input("Current Value", key="kpi1_current", value=0.0)
            kpi1_target = st.number_input("Target Value", key="kpi1_target", value=0.0)
            kpi1_unit = st.text_input("Unit", key="kpi1_unit", placeholder="e.g., hours/week")
            
            if kpi1_name:
                kpis_to_add[kpi1_name] = {
                    "current": kpi1_current,
                    "target": kpi1_target,
                    "unit": kpi1_unit
                }
        
        with kpi_cols[1]:
            st.subheader("KPI 2")
            kpi2_name = st.text_input("Name", key="kpi2_name", placeholder="e.g., Cost Reduction")
            kpi2_current = st.number_input("Current Value", key="kpi2_current", value=0.0)
            kpi2_target = st.number_input("Target Value", key="kpi2_target", value=0.0)
            kpi2_unit = st.text_input("Unit", key="kpi2_unit", placeholder="e.g., $/month")
            
            if kpi2_name:
                kpis_to_add[kpi2_name] = {
                    "current": kpi2_current,
                    "target": kpi2_target,
                    "unit": kpi2_unit
                }
        
        submitted = st.form_submit_button("Add AI Tool to Dashboard")
        
        if submitted and tool_name:
            new_tool = {
                "name": tool_name,
                "category": category,
                "investment": investment,
                "date_implemented": implementation_date.strftime("%Y-%m-%d"),
                "team_size": team_size,
                "description": description,
                "kpis": kpis_to_add
            }
            
            st.session_state.ai_tools.append(new_tool)
            st.success(f"✅ {tool_name} has been added to your dashboard!")
            st.balloons()

elif section == "📊 Calculate ROI":
    st.markdown('<h2 class="sub-header">Return on Investment Calculator</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
    <p><b>ROI Formula:</b> (Benefits - Investment) ÷ Investment × 100%</p>
    <p><i>Example:</i> If an AI tool saves $50,000 and costs $20,000, ROI = (50,000 - 20,000) ÷ 20,000 × 100% = 150%</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Simple ROI Calculator")
        investment = st.number_input("Total Cost of AI Tool ($)", min_value=0, value=50000, key="roi_investment")
        monthly_savings = st.number_input("Monthly Savings ($)", min_value=0, value=10000, key="monthly_savings")
        months_used = st.slider("Months in Use", 1, 36, 6)
        
        total_benefits = monthly_savings * months_used
        roi = ((total_benefits - investment) / investment * 100) if investment > 0 else 0
        
        st.metric("Total Benefits", f"${total_benefits:,.0f}")
        st.metric("ROI", f"{roi:.1f}%")
        
        if roi > 0:
            st.success(f"🎉 Positive ROI! For every $1 invested, you get back ${1 + roi/100:.2f}")
        else:
            st.warning("⚠️ Negative ROI - consider optimizing or reassessing the tool")
    
    with col2:
        st.subheader("Tool Comparison")
        
        if st.session_state.ai_tools:
            roi_data = []
            for tool in st.session_state.ai_tools:
                # Estimate benefits from KPIs
                total_benefits_est = 0
                for kpi_name, kpi_data in tool["kpis"].items():
                    if "cost" in kpi_name.lower() or "saving" in kpi_name.lower():
                        total_benefits_est += kpi_data["current"] * 3  # Estimate quarterly benefits
                
                roi_est = ((total_benefits_est - tool["investment"]) / tool["investment"] * 100) if tool["investment"] > 0 else 0
                roi_data.append({
                    "Tool": tool["name"],
                    "ROI": roi_est,
                    "Investment": tool["investment"]
                })
            
            roi_df = pd.DataFrame(roi_data)
            
            fig = px.bar(roi_df, x='Tool', y='ROI', 
                        title="Estimated ROI by Tool",
                        color='ROI',
                        color_continuous_scale='RdYlGn')
            st.plotly_chart(fig, use_container_width=True)

elif section == "🎯 Set Targets":
    st.markdown('<h2 class="sub-header">Set or Update KPI Targets</h2>', unsafe_allow_html=True)
    
    if not st.session_state.ai_tools:
        st.warning("Please add an AI tool first!")
    else:
        tool_names = [tool["name"] for tool in st.session_state.ai_tools]
        selected_tool_name = st.selectbox("Select AI Tool:", tool_names, key="target_tool")
        
        if selected_tool_name:
            selected_tool = next(tool for tool in st.session_state.ai_tools if tool["name"] == selected_tool_name)
            
            st.info(f"Current KPIs for {selected_tool_name}:")
            
            # Display current KPIs and allow updates
            for kpi_name, kpi_data in selected_tool["kpis"].items():
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.text_input("KPI Name", value=kpi_name, key=f"name_{kpi_name}", disabled=True)
                with col2:
                    new_current = st.number_input("Current Value", 
                                                 value=float(kpi_data["current"]),
                                                 key=f"current_{kpi_name}")
                with col3:
                    new_target = st.number_input("Target Value",
                                                value=float(kpi_data["target"]),
                                                key=f"target_{kpi_name}")
                
                # Update values
                selected_tool["kpis"][kpi_name]["current"] = new_current
                selected_tool["kpis"][kpi_name]["target"] = new_target
            
            # Add new KPI
            st.markdown("### Add New KPI")
            new_kpi_cols = st.columns(4)
            with new_kpi_cols[0]:
                new_kpi_name = st.text_input("New KPI Name", placeholder="e.g., Error Rate")
            with new_kpi_cols[1]:
                new_kpi_current = st.number_input("Current", value=0.0)
            with new_kpi_cols[2]:
                new_kpi_target = st.number_input("Target", value=0.0)
            with new_kpi_cols[3]:
                new_kpi_unit = st.text_input("Unit", placeholder="e.g., %")
            
            if st.button("Add New KPI") and new_kpi_name:
                selected_tool["kpis"][new_kpi_name] = {
                    "current": new_kpi_current,
                    "target": new_kpi_target,
                    "unit": new_kpi_unit
                }
                st.success(f"Added {new_kpi_name} to {selected_tool_name}")

elif section == "📋 View Recommendations":
    st.markdown('<h2 class="sub-header">Recommendations for Improvement</h2>', unsafe_allow_html=True)
    
    recommendations = []
    
    for tool in st.session_state.ai_tools:
        for kpi_name, kpi_data in tool["kpis"].items():
            performance = (kpi_data["current"] / kpi_data["target"]) * 100 if kpi_data["target"] != 0 else 0
            
            if performance < 80:
                recommendations.append({
                    "tool": tool["name"],
                    "kpi": kpi_name,
                    "issue": f"Underperforming by {100-performance:.0f}%",
                    "suggestion": "Consider additional training or tool optimization"
                })
            elif performance > 120:
                recommendations.append({
                    "tool": tool["name"],
                    "kpi": kpi_name,
                    "issue": f"Exceeding target by {performance-100:.0f}%",
                    "suggestion": "Could expand usage to other teams/projects"
                })
    
    if recommendations:
        st.warning("### 🚨 Areas Needing Attention")
        for rec in recommendations[:3]:  # Show top 3
            with st.expander(f"{rec['tool']} - {rec['kpi']}"):
                st.write(f"**Issue:** {rec['issue']}")
                st.write(f"**Suggestion:** {rec['suggestion']}")
    
    st.success("### ✅ Best Practices")
    
    best_practices = [
        "📅 Review KPIs monthly with your team",
        "🎯 Set realistic targets - aim for 10-20% improvement initially",
        "👥 Involve end-users in KPI selection",
        "🔄 Update targets quarterly based on performance",
        "📊 Use visual dashboards for team communication",
        "💰 Focus on both cost savings AND productivity gains"
    ]
    
    for practice in best_practices:
        st.write(practice)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>📞 Need help? Remember: KPIs should be SMART - Specific, Measurable, Achievable, Relevant, Time-bound</p>
    <p>Dashboard refreshes automatically. Data is saved in your browser session.</p>
</div>
""", unsafe_allow_html=True)