import streamlit as st

# ---- PAGE SETUP ----
landing_page = st.Page(
    page="./pages/financial_dashboard.py",
    title= "Dashboard",
    icon=":material/home:",
    default=True,
)

company_overview_page = st.Page(
    page="./pages/Overview.py",
    title="Overview",
    icon=":material/person:",
)
chatbot_page = st.Page(
    page="./pages/AI_mentor.py",
    title="AI Mentor",
    icon=":material/smart_toy:",
)
statements_page = st.Page(
    page="./pages/financial_statements.py",
    title="Financial Statements",
    icon=":material/description:",
)

ratio_analysis_page = st.Page(
    page="./pages/ratios_and_metrics.py",
    title="Ratio Analysis",
    icon=":material/analytics:",
)
price_chart_page = st.Page(
    page="./pages/technical_analysis.py",
    title="Price Chart",
    icon=":material/insights:",
)

# ---- NAV BAR ----
pg = st.navigation({
    "Home": [landing_page],
    "Data": [company_overview_page, statements_page], 
    "Analysis": [price_chart_page, ratio_analysis_page],
    "AI Chatbot": [chatbot_page]
})

pg.run()