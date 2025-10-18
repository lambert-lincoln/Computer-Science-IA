import streamlit as st

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
Welcome to your **comprehensive stock analysis platform** — designed to bridge fundamental and technical analysis for smarter investment decisions.

## 🎯 What This Platform Offers

### 📊 **Multi-Dimensional Analysis**
Analyze stocks from every angle with professional-grade tools that combine Wall Street methodologies with cutting-edge technical indicators.

### 🔬 **Core Analysis Modules**

**📈 Price Ratios & Valuation Metrics**
- **Enterprise Value-to-EBITDA (EV/EBITDA)** — A comprehensive valuation metric that accounts for debt, cash, and operating performance. Ideal for comparing companies with different capital structures and tax situations
- **Price-to-Sales (P/S) Analysis** — Perfect for evaluating growth companies and pre-profit businesses
- **Price-to-Earnings (P/E) Trends** — Track valuation changes over time with moving averages
- **Daily ratio tracking** with 20, 50, 100, and 200-day SMAs for trend identification

**💼 Financial Statement Analysis**
- **Income Statement** — Revenue, profit margins, and earnings trends
- **Balance Sheet** — Assets, liabilities, and equity structure
- **Cash Flow Statement** — Operating, investing, and financing activities
- **Quarter-over-quarter comparisons** to spot trends early

**📉 Technical Analysis Tools**
- **Golden Cross & Death Cross detection** — Identify major trend reversals
- **Support & Resistance levels** — Dynamic price barriers based on moving averages
- **Momentum indicators** — RSI, MACD, and custom oscillators
- **Interactive charts** with zoom, pan, and time-range selection

**🎓 AI Financial Mentor**
- **Built-in chatbot** to clarify financial related questions
- **Trading signal explanations** — Learn what you can do with the provided metrics.

## 🚀 How to Get Started

**Step 1:** Enter a stock ticker symbol in the sidebar (e.g., AAPL, MSFT, TSLA, NVDA)

**Step 2:** Navigate through different analysis pages using the sidebar menu

**Step 3:** If in doubt, navigate to the AI Mentor page and ask a question! 

**Step 4:** Combine multiple metrics for a holistic view before making investment decisions

## ⚡ Key Features

✅ **1+ years of historical analysis** — Spot long-term trends and patterns  
✅ **Hybrid fundamental-technical metrics** — Combine the best of both worlds  
✅ **Professional-grade visualizations** — Publication-ready interactive charts  
✅ **Beginner-friendly explanations** — Learn as you analyze  
✅ **Export-ready data tables** — Download data for your own analysis  

## 💡 Who Is This For?

**🎓 Students & Learners** — Master financial analysis with hands-on tools and guides  
**📊 Value Investors** — Find undervalued stocks using fundamental ratios  
**📈 Technical Traders** — Identify entry/exit points with precise timing signals  
**🏢 Finance Professionals** — Quick reference tool for client meetings and research  
**💼 DIY Investors** — Take control of your portfolio with institutional-grade analysis  

## ⚠️ Important Disclaimer

This platform provides **analytical tools and educational content only**. It does not constitute financial advice, investment recommendations, or trading signals. Always:
- This is not real time data!
- Conduct your own due diligence
- Consider your risk tolerance and investment horizon
- Consult with licensed financial advisors for personalized guidance
- Diversify your portfolio appropriately

Past performance does not guarantee future results. All investments carry risk, including potential loss of principal.

---

**👈 Enter a stock ticker in the sidebar to unlock the full analysis suite!**

**📌 Pro Tip:** Start with the P/B or P/S ratio pages to get a quick valuation overview, then dive deeper into financial statements and DCF models for comprehensive analysis.

**Once you've entered the ticker and explored the sidebar menu, you can close this landing page and navigate between analysis modules!**
""")