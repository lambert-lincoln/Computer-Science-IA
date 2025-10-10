import streamlit as st
from streamlit_option_menu import option_menu

if "ticker" not in st.session_state:
    st.session_state.ticker = ''

# ---- PAGE CONFIGURATION ----

st.set_page_config(
    page_title="Financial Dashboard",
    page_icon=":material/analytics:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---- NAV BAR ----
with st.sidebar:
    ticker_input = st.sidebar.text_input(
        label="Enter Stock Ticker:",
        help="Please enter a valid ticker symbol",
        placeholder="eg. MSFT, AAPL, PLTR",
        icon=":material/search:",
    )
        
    st.session_state.ticker = ticker_input.upper()

st.title("Financial Dashboard", anchor=False)

st.markdown("""
    This dashboard provides comprehensive financial analysis including:
    - 📈 Real-time stock prices and technical indicators
    - 📋 Financial statements (Income, Balance Sheet, Cash Flow)
    - 📊 Financial ratios and metrics
    - 💰 DCF valuation models
    - 📉 Interactive charts and visualizations
    
    **👈 Enter a stock ticker in the sidebar to get started!**
    
    Once you enter the ticker, **don't forget to close this page!**
    """)