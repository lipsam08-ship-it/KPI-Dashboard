import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="AI Tools Success Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for data storage
if 'ai_tools' not in st.session_state:
    st.session_state.ai_tools = []
if 'kpi_data' not in st.session_state:
    st.session_state.kpi_data = {}

# Load sample data if empty
if not st.session_state.ai_tools:
    st.session_state.ai_tools = [
        {
            'id': 1,
            'name': 'AI Task Assistant',
            'category': 'Productivity',
            'total_investment': 15000,
            'implementation_date': '2024-01-15',
            'team_size': 45,
            'description': 'Automates routine tasks and improves team productivity'
        },
        {
            'id': 2,
            'name': 'Risk Predictor',
            'category': 'Risk Management',
            'total_investment': 25000,
            'implementation_date': '2024-02-01',
            'team_size': 22,
            'description': 'Predicts project risks and suggests mitigation strategies'
        }
    ]
    
    # Initialize KPI data for sample tools
    st.session_state.kpi_data = {
        1: [
            {'name': 'Time Saved', 'current': 120, 'target': 150, 'unit': 'hours/month'},
            {'name': 'Task Completion Rate', 'current': 85, 'target': 90, 'unit': '%'},
            {'name': 'User Satisfaction', 'current': 4.2, 'target': 4.5, 'unit': 'rating'}
        ],
        2: [
            {'name': 'Risk Detection Accuracy', 'current': 88, 'target': 92, 'unit': '%'},
            {'name': 'False Positives', 'current': 12, 'target': 10, 'unit': 'cases/month'},
            {'name': 'Cost Avoidance', 'current': 35000, 'target': 40000, 'unit': '$/quarter'}
        ]
    }

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #374151;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .welcome-card {
        background-color: #F3F4F6;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin-bottom: 2rem;
    }
    .step-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #10B981;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        text-align: center;
    }
    .stButton button {
        width: 100%;
        background-color: #3B82F6;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🤖 Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["🏠 Dashboard Home", "📈 View Current KPIs", "➕ Add New AI Tool", 
     "📊 Calculate ROI", "🎯 Set Targets", "📋 View Recommendations"]
)

# Helper functions
def calculate_roi(tool):
    """Calculate ROI for a tool"""
    if tool['id'] in st.session_state.kpi_data:
        kpis = st.session_state.kpi_data[tool['id']]
        cost_savings_kpi = next((kpi for kpi in kpis if 'cost' in kpi['name'].lower()), None)
        if cost_savings_kpi:
            monthly_savings = cost_savings_kpi['current']
            months_in_use = max(1, (datetime.now() - datetime.strptime(tool['implementation_date'], '%Y-%m-%d')).days / 30)
            total_savings = monthly_savings * months_in_use
            roi = ((total_savings - tool['total_investment']) / tool['total_investment']) * 100
            return roi
    return 0

def get_performance_percentage(kpis):
    """Calculate overall performance percentage"""
    if not kpis:
        return 0
    total_performance = 0
    for kpi in kpis:
        if kpi['target'] > 0:
            performance = min(100, (kpi['current'] / kpi['target']) * 100)
            total_performance += performance
    return total_performance / len(kpis)

# Main Page Content
if page == "🏠 Dashboard Home":
    # Header
    st.markdown('<h1 class="main-header">AI Tools Success Dashboard for PMO</h1>', unsafe_allow_html=True)
    
    # Welcome Card
    st.markdown("""
    <div class="welcome-card">
        <h2 style="color: #1E3A8A;">Welcome to Your AI Performance Command Center</h2>
        <p style="font-size: 1.1rem; color: #374151;">
            This dashboard empowers PMO leaders to track, measure, and optimize AI tool investments 
            across your organization. Transform raw data into actionable insights and demonstrate 
            clear ROI for every AI initiative.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats
    st.markdown('<h2 class="sub-header">📊 At a Glance</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_tools = len(st.session_state.ai_tools)
        st.metric("Total AI Tools", total_tools)
    
    with col2:
        if st.session_state.ai_tools:
            avg_performance = np.mean([
                get_performance_percentage(st.session_state.kpi_data.get(tool['id'], []))
                for tool in st.session_state.ai_tools
            ])
            st.metric("Avg Performance", f"{avg_performance:.1f}%")
    
    with col3:
        total_investment = sum(tool['total_investment'] for tool in st.session_state.ai_tools)
        st.metric("Total Investment", f"${total_investment:,.0f}")
    
    # Quick Start Guide
    st.markdown('<h2 class="sub-header">🚀 Quick Start Guide</h2>', unsafe_allow_html=True)
    
    # Step 1
    with st.expander("**Step 1: Launch the Dashboard**", expanded=True):
        st.markdown("""
        **Access your performance hub**
        - Open this dashboard in your browser
        - You'll see this main welcome screen with navigation instructions
        """)
    
    # Step 2
    with st.expander("**Step 2: Navigate Using the Sidebar**"):
        st.markdown("""
        **Your control panel for all activities**
        On the left sidebar, you'll find 5 core functions:
        - **📈 View Current KPIs** – Monitor real-time performance metrics
        - **➕ Add New AI Tool** – Onboard additional AI solutions
        - **📊 Calculate ROI** – Quantify financial impact
        - **🎯 Set Targets** – Define and adjust success metrics
        - **📋 View Recommendations** – Get actionable improvement insights
        """)
    
    # Step 3
    with st.expander("**Step 3: Explore Sample Tools (For First-Time Users)**"):
        st.markdown("""
        **See how it works with pre-loaded examples**
        - Click "📈 View Current KPIs" in the sidebar
        - Examine the two sample tools:
          - **AI Task Assistant** (Productivity category)
          - **Risk Predictor** (Risk Management category)
        - Review their KPIs to understand the tracking format
        """)
    
    # Step 4
    with st.expander("**Step 4: Add Your First AI Tool**"):
        st.markdown("""
        **Begin tracking your own investments**
        - Navigate to "➕ Add New AI Tool" in the sidebar
        - Complete the simple form with:
          - Tool name and category
          - Investment details
          - Implementation date and team size
          - Initial KPIs like "Time Saved" or "Cost Reduction"
        - Click "Add AI Tool to Dashboard"
        """)
    
    # Step 5
    with st.expander("**Step 5: Set Performance Targets**"):
        st.markdown("""
        **Define what success looks like**
        - Go to "🎯 Set Targets" in the sidebar
        - Select your AI tool from the dropdown
        - For each KPI:
          - Update current performance
          - Adjust target goals
        - Add new KPIs as needed
        """)
    
    # Call to Action
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h3 style="color: #1E3A8A;">Ready to Get Started?</h3>
        <p style="color: #374151; margin-bottom: 1rem;">
            Use the navigation sidebar to begin exploring your AI tools' performance.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Other Pages (minimal implementation for demonstration)
elif page == "📈 View Current KPIs":
    st.title("📈 View Current KPIs")
    st.write("Select an AI tool to view its KPIs:")
    
    if st.session_state.ai_tools:
        tool_names = [tool['name'] for tool in st.session_state.ai_tools]
        selected_tool_name = st.selectbox("Select AI Tool", tool_names)
        
        selected_tool = next(tool for tool in st.session_state.ai_tools if tool['name'] == selected_tool_name)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader(f"📊 KPIs for {selected_tool['name']}")
            
            if selected_tool['id'] in st.session_state.kpi_data:
                kpis = st.session_state.kpi_data[selected_tool['id']]
                
                for kpi in kpis:
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric(f"Current {kpi['name']}", f"{kpi['current']} {kpi['unit']}")
                    with col_b:
                        st.metric(f"Target {kpi['name']}", f"{kpi['target']} {kpi['unit']}")
                    with col_c:
                        percentage = (kpi['current'] / kpi['target']) * 100 if kpi['target'] > 0 else 0
                        st.metric("Progress", f"{min(100, percentage):.1f}%")
        
        with col2:
            st.subheader("Tool Info")
            st.write(f"**Category:** {selected_tool['category']}")
            st.write(f"**Investment:** ${selected_tool['total_investment']:,}")
            st.write(f"**Team Size:** {selected_tool['team_size']} users")
            st.write(f"**Implemented:** {selected_tool['implementation_date']}")
            st.write(f"**Description:** {selected_tool['description']}")
    
    else:
        st.info("No AI tools added yet. Use the 'Add New AI Tool' page to get started.")

elif page == "➕ Add New AI Tool":
    st.title("➕ Add New AI Tool")
    
    with st.form("add_ai_tool"):
        col1, col2 = st.columns(2)
        
        with col1:
            tool_name = st.text_input("Tool Name *")
            category = st.selectbox("Category *", ["Productivity", "Risk Management", "Analytics", "Automation", "Quality Control", "Other"])
            total_investment = st.number_input("Total Investment ($) *", min_value=0, step=1000)
        
        with col2:
            implementation_date = st.date_input("Implementation Date *")
            team_size = st.number_input("Team Size (users) *", min_value=1, step=1)
            description = st.text_area("Description")
        
        st.subheader("Add Initial KPIs")
        
        kpi_cols = st.columns(3)
        with kpi_cols[0]:
            kpi1_name = st.text_input("KPI 1 Name", value="Time Saved")
            kpi1_current = st.number_input("KPI 1 Current Value", value=0.0)
        with kpi_cols[1]:
            kpi1_target = st.number_input("KPI 1 Target Value", value=100.0)
            kpi1_unit = st.text_input("KPI 1 Unit", value="hours/month")
        with kpi_cols[2]:
            add_more_kpis = st.checkbox("Add more KPIs?")
        
        if add_more_kpis:
            st.subheader("Additional KPIs")
            additional_kpis = st.number_input("Number of additional KPIs", min_value=0, max_value=5, value=0)
            
            for i in range(additional_kpis):
                cols = st.columns(4)
                with cols[0]:
                    kpi_name = st.text_input(f"KPI {i+2} Name", key=f"kpi_name_{i}")
                with cols[1]:
                    kpi_current = st.number_input(f"KPI {i+2} Current", key=f"kpi_current_{i}")
                with cols[2]:
                    kpi_target = st.number_input(f"KPI {i+2} Target", key=f"kpi_target_{i}")
                with cols[3]:
                    kpi_unit = st.text_input(f"KPI {i+2} Unit", key=f"kpi_unit_{i}")
        
        submitted = st.form_submit_button("Add AI Tool to Dashboard")
        
        if submitted:
            if tool_name and category and total_investment > 0:
                # Generate new ID
                new_id = max([tool['id'] for tool in st.session_state.ai_tools], default=0) + 1
                
                new_tool = {
                    'id': new_id,
                    'name': tool_name,
                    'category': category,
                    'total_investment': total_investment,
                    'implementation_date': implementation_date.strftime('%Y-%m-%d'),
                    'team_size': team_size,
                    'description': description
                }
                
                st.session_state.ai_tools.append(new_tool)
                
                # Add initial KPI
                st.session_state.kpi_data[new_id] = [
                    {
                        'name': kpi1_name,
                        'current': kpi1_current,
                        'target': kpi1_target,
                        'unit': kpi1_unit
                    }
                ]
                
                st.success(f"✅ {tool_name} has been added to the dashboard!")
                st.rerun()
            else:
                st.error("Please fill in all required fields (*)")

elif page == "📊 Calculate ROI":
    st.title("📊 Calculate ROI")
    
    if not st.session_state.ai_tools:
        st.info("No AI tools added yet. Add tools first to calculate ROI.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Simple ROI Calculator")
            selected_tool_name = st.selectbox(
                "Select Tool to Calculate ROI",
                [tool['name'] for tool in st.session_state.ai_tools]
            )
            
            selected_tool = next(tool for tool in st.session_state.ai_tools if tool['name'] == selected_tool_name)
            
            total_cost = st.number_input("Total Cost ($)", value=float(selected_tool['total_investment']))
            monthly_savings = st.number_input("Monthly Savings ($)", value=5000.0)
            
            implementation_date = datetime.strptime(selected_tool['implementation_date'], '%Y-%m-%d')
            months_in_use = max(1, (datetime.now() - implementation_date).days / 30)
            st.write(f"**Months in Use:** {months_in_use:.1f}")
            
            total_savings = monthly_savings * months_in_use
            roi = ((total_savings - total_cost) / total_cost) * 100
            
            st.metric("Total Savings", f"${total_savings:,.0f}")
            st.metric("Return on Investment (ROI)", f"{roi:.1f}%")
        
        with col2:
            st.subheader("Tool Comparison")
            
            # Calculate ROI for all tools
            roi_data = []
            for tool in st.session_state.ai_tools:
                roi_value = calculate_roi(tool)
                roi_data.append({
                    'Tool': tool['name'],
                    'ROI': roi_value,
                    'Status': 'Positive' if roi_value > 0 else 'Negative'
                })
            
            if roi_data:
                df = pd.DataFrame(roi_data)
                fig = px.bar(
                    df,
                    x='Tool',
                    y='ROI',
                    color='Status',
                    color_discrete_map={'Positive': '#10B981', 'Negative': '#EF4444'},
                    title="ROI Comparison Across Tools"
                )
                fig.update_layout(showlegend=True)
                st.plotly_chart(fig, use_container_width=True)

elif page == "🎯 Set Targets":
    st.title("🎯 Set Targets")
    
    if not st.session_state.ai_tools:
        st.info("No AI tools added yet. Add tools first to set targets.")
    else:
        selected_tool_name = st.selectbox(
            "Select AI Tool",
            [tool['name'] for tool in st.session_state.ai_tools]
        )
        
        selected_tool = next(tool for tool in st.session_state.ai_tools if tool['name'] == selected_tool_name)
        tool_id = selected_tool['id']
        
        st.subheader(f"Current KPIs for {selected_tool_name}")
        
        if tool_id in st.session_state.kpi_data:
            kpis = st.session_state.kpi_data[tool_id]
            
            for i, kpi in enumerate(kpis):
                st.markdown(f"**{kpi['name']}**")
                cols = st.columns(4)
                with cols[0]:
                    new_current = st.number_input(
                        f"Current Value ({kpi['unit']})",
                        value=float(kpi['current']),
                        key=f"current_{tool_id}_{i}"
                    )
                with cols[1]:
                    new_target = st.number_input(
                        f"Target Value ({kpi['unit']})",
                        value=float(kpi['target']),
                        key=f"target_{tool_id}_{i}"
                    )
                with cols[2]:
                    new_unit = st.text_input(
                        f"Unit",
                        value=kpi['unit'],
                        key=f"unit_{tool_id}_{i}"
                    )
                with cols[3]:
                    performance = (new_current / new_target * 100) if new_target > 0 else 0
                    st.metric("Performance", f"{min(100, performance):.1f}%")
                
                # Update values
                kpis[i]['current'] = new_current
                kpis[i]['target'] = new_target
                kpis[i]['unit'] = new_unit
            
            st.session_state.kpi_data[tool_id] = kpis
            
            # Add new KPI section
            st.subheader("Add New KPI")
            with st.form(f"add_kpi_{tool_id}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    new_kpi_name = st.text_input("KPI Name")
                with col2:
                    new_kpi_current = st.number_input("Current Value", value=0.0)
                with col3:
                    new_kpi_target = st.number_input("Target Value", value=100.0)
                new_kpi_unit = st.text_input("Unit", value="units")
                
                if st.form_submit_button("Add New KPI"):
                    if new_kpi_name:
                        kpis.append({
                            'name': new_kpi_name,
                            'current': new_kpi_current,
                            'target': new_kpi_target,
                            'unit': new_kpi_unit
                        })
                        st.session_state.kpi_data[tool_id] = kpis
                        st.success(f"✅ Added new KPI: {new_kpi_name}")
                        st.rerun()
        else:
            st.info("No KPIs defined for this tool yet. Add KPIs using the form below.")

elif page == "📋 View Recommendations":
    st.title("📋 View Recommendations")
    
    if not st.session_state.ai_tools:
        st.info("No AI tools added yet. Add tools first to view recommendations.")
    else:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("🚨 Areas Needing Attention")
            
            underperforming_tools = []
            for tool in st.session_state.ai_tools:
                if tool['id'] in st.session_state.kpi_data:
                    kpis = st.session_state.kpi_data[tool['id']]
                    for kpi in kpis:
                        if kpi['target'] > 0:
                            performance = (kpi['current'] / kpi['target']) * 100
                            if performance < 80:  # Underperforming threshold
                                underperforming_tools.append({
                                    'tool': tool['name'],
                                    'kpi': kpi['name'],
                                    'performance': performance,
                                    'current': kpi['current'],
                                    'target': kpi['target']
                                })
            
            if underperforming_tools:
                for item in underperforming_tools:
                    with st.expander(f"⚠️ {item['tool']} - {item['kpi']} ({item['performance']:.1f}%)", expanded=True):
                        st.write(f"**Current:** {item['current']} vs **Target:** {item['target']}")
                        st.write("**Suggestions:**")
                        if item['performance'] < 50:
                            st.write("- Consider training or onboarding support")
                            st.write("- Review implementation approach")
                            st.write("- Check tool configuration")
                        elif item['performance'] < 80:
                            st.write("- Optimize current usage patterns")
                            st.write("- Gather user feedback for improvements")
                            st.write("- Consider minor configuration adjustments")
            else:
                st.success("✅ All KPIs are meeting or exceeding targets!")
        
        with col2:
            st.subheader("✅ Best Practices")
            
            best_practices = [
                "**1. Regular Monitoring**\nUpdate KPI values monthly to track progress",
                "**2. Target Adjustment**\nReview and adjust targets quarterly based on performance",
                "**3. User Training**\nEnsure adequate training for maximum tool adoption",
                "**4. ROI Calculation**\nCalculate ROI quarterly to justify continued investment",
                "**5. Feedback Collection**\nGather user feedback for continuous improvement",
                "**6. Tool Integration**\nEnsure tools integrate well with existing workflows"
            ]
            
            for practice in best_practices:
                st.info(practice)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #6B7280; font-size: 0.9rem;">
        <p>AI Tools Success Dashboard for PMO • Version 1.0 • Data updates in real-time</p>
    </div>
    """,
    unsafe_allow_html=True
)