import streamlit as st

# ---- PAGE SETUP ----
landing_page = st.Page(
    page="./pages/financial_dashboard.py",
    title= "Dashboard",
    icon="🏚️",
    default=True,
)

company_overview_page = st.Page(
    page="./pages/Overview.py",
    title="Overview",
    icon="📊",
)
chatbot_page = st.Page(
    page="./pages/AI_mentor.py",
    title="AI Mentor",
    icon="🤖",
)
statements_page = st.Page(
    page="./pages/financial_statements.py",
    title="Financial Statements",
    icon="🧾",
)

ratio_analysis_page = st.Page(
    page="./pages/ratios_and_metrics.py",
    title="Ratio Analysis",
    icon="⚙️",
)
price_chart_page = st.Page(
    page="./pages/technical_analysis.py",
    title="Price Chart",
    icon="📈",
)

# ---- NAV BAR ----
pg = st.navigation({
    "Home": [landing_page],
    "Analyze": [company_overview_page, chatbot_page, statements_page, ratio_analysis_page, price_chart_page], 
})

pg.run()