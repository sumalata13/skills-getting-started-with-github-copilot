"""
Streamlit Dashboard for Employee Management System.
Displays employee, salary, and department information with interactive visualizations.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from database import (
    get_all_employees,
    get_all_salaries,
    get_all_departments,
    get_department_salary_stats,
    get_employee_by_id
)

# Page configuration
st.set_page_config(
    page_title="Employee Management Dashboard",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)


def check_database_exists():
    """Check if the database file exists."""
    return os.path.exists("employee_database.db")


def main():
    """Main application function."""
    
    # Title and description
    st.title("👥 Employee Management Dashboard")
    st.markdown("---")
    
    # Check if database exists
    if not check_database_exists():
        st.error("⚠️ Database not found! Please run `python init_db.py` first to initialize the database.")
        st.info("Run the following command in your terminal:\n```bash\npython init_db.py\n```")
        return
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select a page:",
        ["Overview", "Employees", "Salaries", "Departments", "Analytics"]
    )
    
    # Page routing
    if page == "Overview":
        show_overview()
    elif page == "Employees":
        show_employees()
    elif page == "Salaries":
        show_salaries()
    elif page == "Departments":
        show_departments()
    elif page == "Analytics":
        show_analytics()


def show_overview():
    """Display overview dashboard with key metrics."""
    st.header("📊 Overview")
    
    # Get data
    employees_df = get_all_employees()
    salaries_df = get_all_salaries()
    departments_df = get_all_departments()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Employees", len(employees_df))
    
    with col2:
        st.metric("Total Departments", len(departments_df))
    
    with col3:
        avg_salary = salaries_df['total_compensation'].mean()
        st.metric("Avg. Total Compensation", f"${avg_salary:,.0f}")
    
    with col4:
        total_payroll = salaries_df['total_compensation'].sum()
        st.metric("Total Payroll", f"${total_payroll:,.0f}")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Employees by Department")
        dept_employee_count = departments_df[['department_name', 'employee_count']]
        fig = px.bar(
            dept_employee_count,
            x='department_name',
            y='employee_count',
            labels={'department_name': 'Department', 'employee_count': 'Number of Employees'},
            color='employee_count',
            color_continuous_scale='Blues'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Salary Distribution")
        fig = px.histogram(
            salaries_df,
            x='total_compensation',
            nbins=10,
            labels={'total_compensation': 'Total Compensation ($)'},
            color_discrete_sequence=['#1f77b4']
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


def show_employees():
    """Display employee information."""
    st.header("👤 Employees")
    
    # Get employee data
    employees_df = get_all_employees()
    
    # Search functionality
    search_term = st.text_input("🔍 Search employees by name or email:")
    if search_term:
        mask = (
            employees_df['first_name'].str.contains(search_term, case=False, na=False) |
            employees_df['last_name'].str.contains(search_term, case=False, na=False) |
            employees_df['email'].str.contains(search_term, case=False, na=False)
        )
        employees_df = employees_df[mask]
    
    # Display employee table
    st.dataframe(
        employees_df,
        use_container_width=True,
        hide_index=True
    )
    
    st.info(f"Showing {len(employees_df)} employee(s)")


def show_salaries():
    """Display salary information."""
    st.header("💰 Salaries")
    
    # Get salary data
    salaries_df = get_all_salaries()
    
    # Filter options
    col1, col2 = st.columns(2)
    
    with col1:
        min_salary = st.number_input(
            "Minimum Total Compensation ($)",
            min_value=0,
            value=0,
            step=1000
        )
    
    with col2:
        max_salary = st.number_input(
            "Maximum Total Compensation ($)",
            min_value=0,
            value=int(salaries_df['total_compensation'].max()),
            step=1000
        )
    
    # Apply filters
    filtered_df = salaries_df[
        (salaries_df['total_compensation'] >= min_salary) &
        (salaries_df['total_compensation'] <= max_salary)
    ]
    
    # Display salary table
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )
    
    st.info(f"Showing {len(filtered_df)} salary record(s)")
    
    # Salary breakdown chart
    st.subheader("Salary Breakdown")
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Base Salary',
        x=filtered_df['employee_name'],
        y=filtered_df['base_salary'],
        marker_color='lightblue'
    ))
    
    fig.add_trace(go.Bar(
        name='Bonus',
        x=filtered_df['employee_name'],
        y=filtered_df['bonus'],
        marker_color='darkblue'
    ))
    
    fig.update_layout(
        barmode='stack',
        xaxis_title="Employee",
        yaxis_title="Amount ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def show_departments():
    """Display department information."""
    st.header("🏢 Departments")
    
    # Get department data
    departments_df = get_all_departments()
    dept_stats_df = get_department_salary_stats()
    
    # Display department table
    st.subheader("Department Overview")
    st.dataframe(
        departments_df,
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    
    # Department salary statistics
    st.subheader("Department Salary Statistics")
    st.dataframe(
        dept_stats_df,
        use_container_width=True,
        hide_index=True
    )
    
    # Visualization
    st.subheader("Average Compensation by Department")
    fig = px.bar(
        dept_stats_df,
        x='department_name',
        y='avg_total_compensation',
        labels={
            'department_name': 'Department',
            'avg_total_compensation': 'Average Total Compensation ($)'
        },
        color='avg_total_compensation',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def show_analytics():
    """Display advanced analytics and insights."""
    st.header("📈 Analytics")
    
    # Get data
    salaries_df = get_all_salaries()
    dept_stats_df = get_department_salary_stats()
    
    # Department comparison
    st.subheader("Department Compensation Comparison")
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Min',
        x=dept_stats_df['department_name'],
        y=dept_stats_df['min_compensation'],
        marker_color='lightcoral'
    ))
    
    fig.add_trace(go.Bar(
        name='Average',
        x=dept_stats_df['department_name'],
        y=dept_stats_df['avg_total_compensation'],
        marker_color='lightskyblue'
    ))
    
    fig.add_trace(go.Bar(
        name='Max',
        x=dept_stats_df['department_name'],
        y=dept_stats_df['max_compensation'],
        marker_color='lightgreen'
    ))
    
    fig.update_layout(
        barmode='group',
        xaxis_title="Department",
        yaxis_title="Compensation ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Pie chart for total compensation by department
    st.subheader("Total Compensation Distribution by Department")
    
    fig = px.pie(
        dept_stats_df,
        values='total_compensation',
        names='department_name',
        title='Total Payroll by Department',
        hole=0.4
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Top earners
    st.subheader("Top 5 Earners")
    top_earners = salaries_df.nlargest(5, 'total_compensation')[
        ['employee_name', 'department_name', 'base_salary', 'bonus', 'total_compensation']
    ]
    st.dataframe(
        top_earners,
        use_container_width=True,
        hide_index=True
    )


if __name__ == "__main__":
    main()
