import streamlit as st
from streamlit_option_menu import option_menu

if "ticker" not in st.session_state:
    st.session_state.ticker = ''


st.set_page_config(
    page_title="Trading Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Nav bar
with st.sidebar:
    ticker_input = st.sidebar.text_input(
        label="Enter Stock Ticker:",
        help="Please enter a valid ticker symbol",
        placeholder="eg. MSFT, AAPL, PLTR",
    )
    st.session_state.ticker = ticker_input.upper()

    selected = option_menu(
        menu_title="Main Menu",
        options=["Dashboard", "Overview", "Financial Statements",
                 "Ratios & Metrics", "Technical Analysis", "DCF Valuation", "AI Mentor"],
        icons=["house", "book", "file-text", "calculator",
               "graph-up", "cash-coin", "robot"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "10px"},
            "icon": {"color": "orange", "font-size": "20px"},
            "nav-link": {"font-size": "14px", "text-align": "left", "margin": "2px", "--hover-color": "#1B2035"},
            "nav-link-selected": {"background-color": "#02ab21"},
        }
    )

# --- Page Content Based on Selection ---
if selected == "Dashboard":
    st.title(f"Welcome to the {selected} page")
    st.markdown("""
    This dashboard provides comprehensive financial analysis including:
    - 📈 Real-time stock prices and technical indicators
    - 📋 Financial statements (Income, Balance Sheet, Cash Flow)
    - 📊 Financial ratios and metrics
    - 💰 DCF valuation models
    - 📉 Interactive charts and visualizations

    **👈 Enter a stock ticker in the sidebar to get started!**
    """)

if selected == "Overview" and st.session_state.ticker != '':
    from pages.Overview import display_overview
    display_overview(st.session_state.ticker)

if selected == "AI Mentor":
    import pages.AI_mentor as ai_mentor_page
    ai_mentor_page.show_ai_mentor_page()

if selected == "Technical Analysis" and st.session_state.ticker != '':
    from pages.technical_analysis import display_price_chart
    display_price_chart(st.session_state.ticker)
