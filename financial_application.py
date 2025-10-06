import streamlit as st
from back_end import BackEnd as BE
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import yfinance as yf
import pandas as pd



if 'ticker' not in st.session_state:
    st.session_state.ticker = ''

if "messages" not in st.session_state:
        st.session_state.messages = []

def chatbot_help():
    cta = '''Don't know what to make of this data? Ask our AI Mentor!'''
    st.subheader(cta)

def display_overview():
    if st.session_state.ticker and st.session_state.ticker != '':
        try:
            info = get_company_overview()

            metrics = [
                ("Current Price", info.get("regularMarketPrice", 0)),
                ("Market Cap", info.get("marketCap", 0)),
                ("Dividend Yield", info.get("dividendYield") *
                 100 if isinstance(info.get("dividendYield"), float) else 0)
            ]
            col1, col2, col3 = st.columns(3)

            for col, (label, value) in zip([col1, col2, col3], metrics):
                with col:
                    if label == "Dividend Yield":
                        st.metric(label=f"{label}", value=f"{value}%")
                    elif label == "Current Price":
                        st.metric(label=f"{label}", value=f"${value:,.2f}")
                    elif label == "Market Cap":
                        if value > 1e9:
                            st.metric(label=f"{label}",
                                      value=f"${(value/1e9):.2f}B")
                        else:
                            st.metric(label=f"{label}",
                                      value=f"${(value/1e6):.2f}M")

            with st.expander(label="About the Business"):
                st.write(info.get("longBusinessSummary"))

        except Exception as e:
            st.write(f"There is an error: {e}")


def get_company_overview():
    try:
        stock = yf.Ticker(st.session_state.ticker)
        return stock.info

    except Exception as e:
        message = f"There is an error: {e}"
        return message


def display_financial_statements():
    try:
        # Creating tabs
        tab1, tab2, tab3 = st.tabs(
            ["Income Statement", "Balance Sheet", "Cash Flow"])

        with tab1:
            st.header("Income Statement")
            st.dataframe(display_statements("INCOME STATEMENT"))
            chatbot_help()
            st.button(label="Ask AI", key="Income Statement Help", icon="🤖", help="Automatically take necessary data and ask AI to analyze them for you.")

        with tab2:
            st.header("Balance Sheet")
            st.dataframe(display_statements("BALANCE SHEET"))
            chatbot_help()
            st.button(label="Ask AI", key="Balance Sheet Help", icon="🤖", help="Automatically take necessary data and ask AI to analyze them for you.")

        with tab3:
            st.header("Cash Flow")
            st.dataframe(display_statements("CASH FLOW"))
            chatbot_help()
            st.button(label="Ask AI", key="Cash Flow Help", icon="🤖", help="Automatically take necessary data and ask AI to analyze them for you.")

    except Exception as e:
        st.write(f"There is an error: {e}")


def display_statements(data_type):
    # Financial Statements
    stock = yf.Ticker(st.session_state.ticker)

    if data_type == "INCOME STATEMENT":
        important_cols = ["Total Revenue", "Cost Of Revenue", "Gross Profit", "Research And Development",
                          "Selling And Marketing Expense", "General And Administrative Expense",
                          "Operating Expense", "Operating Income", "Net Income"]
        income_stmt = stock.income_stmt
        
        # Filter which type of data exists
        available_cols = [
            col for col in important_cols if col in income_stmt.index]
        # DataFrame is returned bcoz multiple row labels are specififed
        filtered_stmt = income_stmt.loc[available_cols]

        return filtered_stmt

    elif data_type == "BALANCE SHEET":
        important_cols = ["Total Assets", "Current Assets", "Cash And Cash Equivalents", "Accounts Receivable",
                          "Inventory", "Total Liabilities", "Current Liabilities", "Accounts Payable",
                          "Total Debt", "Stockholders Equity", "Retained Earnings"]
        balance_sheet = stock.balance_sheet

        available_cols = [
            col for col in important_cols if col in balance_sheet.index]
        # DataFrame is returned bcoz multiple row labels are specififed
        filtered_stmt = balance_sheet.loc[available_cols]

        return filtered_stmt

    elif data_type == "CASH FLOW":
        important_cols = ["Operating Cash Flow", "Investing Cash Flow", "Financing Cash Flow",
                          "Free Cash Flow", "Capital Expenditure", "Depreciation And Amortization"]
        cash_flow = stock.cash_flow

        available_cols = [
            col for col in important_cols if col in cash_flow.index]
        # DataFrame is returned bcoz multiple row labels are specififed
        filtered_stmt = cash_flow.loc[available_cols]

        return filtered_stmt


def display_ratios_and_metrics():
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Basic Ratios", "P/B Ratio", "I-P/B Ratio", "P/S Ratio"])
    with tab1:
        st.header("Basic Ratios")
        basic_ratios_and_metrics()
    with tab2:
        st.header("Price-to-Book Ratio")
        pb_ratio()
    with tab3:
        st.header("Market Implied Intangible Price-to-Book Ratio")
        intangible_pb_ratio()
    with tab4:
        st.header("Price-to-Sales Ratio")
        ps_ratio()


def basic_ratios_and_metrics():
    if st.session_state.ticker and st.session_state.ticker !='':
        stock = yf.Ticker(st.session_state.ticker)
        info = stock.info
        ratio_categories = {
            "Profitability": ["grossMargins", "operatingMargins",
                              "returnOnAssets", "returnOnEquity"],
            "Liquidity": ["currentRatio", "quickRatio", "freeCashflow"],
            "Leverage": ["debtToEquity"]
        }

        income_stmt = stock.income_stmt
        balance_sheet = stock.balance_sheet
        cashflow_stmt = stock.cash_flow

        for category, ratio_list in ratio_categories.items():
            with st.expander(f"📈 {category} Ratios", expanded=True):
                cols = st.columns(len(ratio_list))
                for col, ratio in zip(cols, ratio_list):
                    with col:
                        value = info.get(ratio, 0)

                        if category == "Profitability":
                            formatted_value = f"{value * 100:.2f}%" if value else "N/A"
                        elif category == "Liquidity" and ratio == "freeCashflow":
                            if value > 1e9:
                                formatted_value = f"${value/1e9:.2f}B"
                            elif value > 1e6:
                                formatted_value = f"${value/1e6:.2f}M"
                            else:
                                formatted_value = f"${value:,.0f}" if value else "N/A"
                        else:
                            formatted_value = f"{value:.2f}" if value else "N/A"

                        clean_name = ratio.replace("Margins", " Margin").replace(
                            "Ratio", " Ratio").title()
                        st.metric(label=clean_name, value=formatted_value)

        # Add more ratios later

# P/S Ratio = Market Value Per Share (Price of Stock) / Sales per share


def ps_ratio():
    if st.session_state.ticker and st.session_state.ticker != '':
        stock = yf.Ticker(st.session_state.ticker)
        hist = stock.history(period="2y")
        # Convert to timezone-naive (ignore +GMT)
        hist.index = hist.index.tz_localize(None)
        # Balance sheet to get market cap
        balance_sheet = stock.quarterly_balance_sheet
        # st.write(balance_sheet)
        # Income statement to get sales
        income_stmt = stock.quarterly_income_stmt
        # st.write(income_stmt)

        if balance_sheet.empty or income_stmt.empty:
            st.error(
                "Data from Balance Sheet or the Income Statement are not available"
            )

        if not balance_sheet.empty and not income_stmt.empty:
            # Common dates between balance sheet and income statement
            common_dates = [
                dates for dates in income_stmt.columns if dates in balance_sheet.columns
            ]
            # Sales per share = Total Revenue / Ordinary Shares
            sales_per_share = (income_stmt.loc["Total Revenue", common_dates] /
                               balance_sheet.loc["Ordinary Shares Number", common_dates])

            daily_dates = pd.date_range(
                start=hist.index.min(),
                end=hist.index.max(),
                freq="D"
            )
            sales_per_share = sales_per_share.reindex(daily_dates)
            sales_per_share = sales_per_share.interpolate(method='linear')
            sales_per_share = sales_per_share.ffill().bfill()

            ps_data = []
            for date in hist.index:
                # P/S Ratio = Market Value Per Share (Price of Stock) / Sales per share
                if date in sales_per_share.index:
                    ps_ratio = (hist.loc[date, "Close"] /
                                sales_per_share.loc[date])
                    ps_data.append({
                        "Date": date,
                        "P/S Ratio": ps_ratio,
                    })

            ps_df = pd.DataFrame(ps_data)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=ps_df["Date"].iloc[99:],
                y=ps_df["P/S Ratio"].iloc[99:],
                name="P/S Ratio",
                line=dict(color='#2E86AB', width=2),
            ))

            # Calculation for SMAs
            sma_periods = [20, 50, 100]
            colors = ['#A23B72', '#F18F01', '#C73E1D']
            for period, color in zip(sma_periods, colors):
                ps_df[f"SMA {period}"] = ps_df["P/S Ratio"].rolling(
                    window=period).mean()
                fig.add_trace(go.Scatter(
                    x=ps_df["Date"].iloc[99:],
                    y=ps_df[f"SMA {period}"].iloc[99:],
                    mode='lines',
                    line=dict(color=f"{color}"),
                    line_shape='spline',
                    name=f"{period}-day SMA",
                ))
            fig.update_layout(title='Price-to-Sales Ratio Over Time',
                              xaxis_title='Date', yaxis_title='P/S Ratio', height=650)

            st.plotly_chart(fig)

            # Educational content
            st.info(
                "💡 **New to P/S ratios?** Start with 'What is P/S?' then move through the tabs!")

            with st.expander("📊 What is P/S Ratio?", expanded=False):
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown("""
                    ### 💡 Simple Explanation
                    **Price-to-Sales (P/S) Ratio = How much investors pay for each dollar of company sales**

                    Think of it like this:
                    - If P/S ratio = **30**, investors pay **USD 30** for every **USD 1** of sales
                    - **Higher P/S** = Expected strong growth (or expensive stock)
                    - **Lower P/S** = Cheap stock OR investor concerns
                    """)
                with col2:
                    st.markdown("""
                    ### 🏪 Real-World Example
                    Two identical stores:
                    - **Store A**: USD 100k sales, selling for USD 3M → P/S = 30x
                    - **Store B**: USD 100k sales, selling for USD 1.5M → P/S = 15x

                    Store B might be better value... unless Store A has special advantages!
                    """)

                st.success(
                    "✅ **Your P/S around 30-40x suggests**: High-growth company OR potentially overvalued stock")

            with st.expander("🎨 Understanding the Lines", expanded=False):
                tab1, tab2 = st.tabs(["Line Meanings", "Why SMAs Matter"])

                with tab1:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("""
                        **🔵 Blue Line (P/S Ratio)**
                        - Daily P/S changes (jagged is normal!)
                        - Immediate price reactions
                        - Shows exact current valuation

                        **🔴 Red Line (20-day SMA)**
                        - Short-term trend (~1 month)
                        - Most responsive to changes
                        - Best for entry/exit timing
                        """)
                    with col2:
                        st.markdown("""
                        **🟠 Orange Line (50-day SMA)**
                        - Medium-term trend (~2.5 months)
                        - Balance of speed vs stability
                        - Good for trend confirmation

                        **🟤 Brown Line (100-day SMA)**
                        - Long-term trend (~5 months)
                        - Most stable, changes slowly
                        - Shows overall market sentiment
                        """)

                with tab2:
                    st.markdown("""
                    ### 📈 Why Moving Averages Matter
                    - **Smooth out noise** - daily moves can mislead
                    - **Show true direction** - is stock getting expensive or cheap?
                    - **Support/Resistance** - prices often bounce off SMA lines
                    """)

            with st.expander("🎯 Trading Signals", expanded=False):
                tab1, tab2, tab3 = st.tabs(
                    ["Buy Signals", "Sell Signals", "Golden/Death Cross"])

                with tab1:
                    st.success("🟢 **Strong Buy Signals**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("""
                        **What to Look For:**
                        - P/S above all SMA lines
                        - SMAs sloping upward
                        - 20-day > 50-day > 100-day SMAs
                        """)
                    with col2:
                        st.markdown("""
                        **What It Means:**
                        - Investors getting optimistic
                        - Valuation trending higher
                        - Expecting better performance
                        """)

                with tab2:
                    st.error("🔴 **Strong Sell Signals**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("""
                        **What to Look For:**
                        - P/S below all SMA lines
                        - SMAs sloping downward
                        - 100-day > 50-day > 20-day SMAs
                        """)
                    with col2:
                        st.markdown("""
                        **What It Means:**
                        - Investors getting pessimistic
                        - Valuation trending lower
                        - Growth concerns emerging
                        """)

                with tab3:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.success("🏆 **Golden Cross (Buy)**")
                        st.markdown("""
                        - 20-day crosses **above** 50-day SMA
                        - 50-day crosses **above** 100-day SMA
                        - Strong momentum building
                        """)
                    with col2:
                        st.error("☠️ **Death Cross (Sell)**")
                        st.markdown("""
                        - 20-day crosses **below** 50-day SMA
                        - 50-day crosses **below** 100-day SMA
                        - Momentum weakening
                        """)

            with st.expander("⚠️ Risk Management", expanded=False):
                st.warning("🛡️ **Essential Rules for Safe Trading**")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown("""
                    **Position Sizing**
                    - Max 2-3% risk per trade
                    - Scale into positions
                    - Use stop losses
                    """)
                with col2:
                    st.markdown("""
                    **Don't Rely on P/S Alone**
                    - Check other metrics
                    - Consider market trend
                    - Watch company news
                    """)
                with col3:
                    st.markdown("""
                    **Common Mistakes**
                    - Chasing breakouts
                    - No stop losses
                    - Emotional trading
                    """)


def intangible_pb_ratio():
    if st.session_state.ticker and st.session_state.ticker != '':
        stock = yf.Ticker(st.session_state.ticker)

        hist = stock.history(period="2y")
        # Convert to timezone-naive
        hist.index = hist.index.tz_localize(None)
        # st.write(hist)
        balance_sheet = stock.quarterly_balance_sheet
        # st.write(balance_sheet)

        if balance_sheet.empty:
            st.error("Balance sheet data is not available!")

        # Historical Market Cap = Price x Number of Shares Outstanding
        common_dates = [
            dates for dates in balance_sheet.columns if dates in hist.index]

        if not balance_sheet.empty and not hist.empty:
            market_cap = (hist.loc[common_dates, "Close"] *
                          balance_sheet.loc["Ordinary Shares Number", common_dates])
            market_cap.name = "Historical Market Cap"

        # Market-Implied Intangible Value = Market Cap - Tangible Book Value
        # Find common dates between market_cap and balance_sheet
        final_common_dates = [
            dates for dates in market_cap.index if dates in balance_sheet.columns]

        if not balance_sheet.empty and "Tangible Book Value" in balance_sheet.index and len(final_common_dates) > 0:
            market_cap_filtered = market_cap.loc[final_common_dates]
            tangible_book_value = balance_sheet.loc["Tangible Book Value",
                                                    final_common_dates]
            intangible_BV = (market_cap_filtered - tangible_book_value)
            intangible_BV.name = "Intangible Book Value"
            quarterly_intangible_BV_per_share = (
                intangible_BV.loc[final_common_dates] / balance_sheet.loc["Ordinary Shares Number", final_common_dates])
            quarterly_intangible_BV_per_share.name = "Market-Implied Intangible Book Value per Share"
        else:
            st.error("No common dates found or Tangible Book Value not available")

        daily_dates = pd.date_range(
            start=hist.index.min(),
            end=hist.index.max(),
            freq='D'
        )

        # Reindex and interpolate
        daily_intangible_bvps = quarterly_intangible_BV_per_share.reindex(
            daily_dates)
        daily_intangible_bvps = daily_intangible_bvps.interpolate(
            method="linear")
        # Forward and backward fill
        daily_intangible_bvps = daily_intangible_bvps.ffill().bfill()

        intangible_pb_data = []
        for date in hist.index:
            if date in daily_intangible_bvps.index:
                intangible_pb_ratio = (
                    hist.loc[date, "Close"] / daily_intangible_bvps.loc[date])
                intangible_pb_data.append({
                    'Date': date,
                    'Close': hist.loc[date, "Close"],
                    'Intangible BVPS': daily_intangible_bvps.loc[date],
                    'Intangible P/B Ratio': intangible_pb_ratio,
                })
            else:
                pass

        intangible_pb_df = pd.DataFrame(intangible_pb_data)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=intangible_pb_df["Date"].iloc[99:],
            y=intangible_pb_df["Intangible P/B Ratio"].iloc[99:],
            name="Intangible P/B Ratio",
            mode='lines',
            line=dict(color='#2E86AB', width=2),
        ))

        # Calculation for SMAs
        sma_periods = [20, 50, 100]
        colors = ['#A23B72', '#F18F01', '#C73E1D']

        for period, color in zip(sma_periods, colors):
            intangible_pb_df[f"SMA {period}"] = intangible_pb_df["Intangible P/B Ratio"].rolling(
                window=period).mean()
            fig.add_trace(go.Scatter(
                x=intangible_pb_df["Date"].iloc[99:],
                y=intangible_pb_df[f"SMA {period}"].iloc[99:],
                mode='lines',
                line=dict(color=f"{color}"),
                name=f"{period}-day SMA",
            ))

        fig.update_layout(title='Market-Implied Intangible Price-to-Book Ratio Over Time',
                          xaxis_title='Date', yaxis_title='Market-Implied Intangible P/B Ratio', height=650)

        st.plotly_chart(fig)

        # Educational content
        st.info("🔬 **Advanced Topic**: This measures 'hidden value' like patents, brand power, and intellectual property!")

        with st.expander("🧠 What is Intangible P/B?", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                ### 💡 Simple Explanation
                **Intangible P/B = How much investors pay for a company's "hidden assets"**

                This includes:
                - 🧬 Patents and R&D
                - 🏷️ Brand reputation
                - 💼 Customer relationships
                - 🤖 Proprietary technology
                """)
            with col2:
                st.markdown("""
                ### 🏢 Real Example
                Think of Apple vs generic phone maker:
                - Both make phones with similar costs
                - Apple commands premium for brand/ecosystem
                - That premium = intangible value
                - Higher intangible P/B = More brand power
                """)

        with st.expander("📊 Understanding This Chart", expanded=False):
            tab1, tab2 = st.tabs(["Line Colors", "What High/Low Values Mean"])

            with tab1:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                    **🔵 Blue Line (Intangible P/B)**
                    - Daily intangible value changes
                    - Shows market's view of "hidden assets"

                    **🔴 Red Line (20-day SMA)**
                    - Short-term intangible value trend
                    - Best for timing decisions
                    """)
                with col2:
                    st.markdown("""
                    **🟠 Orange Line (50-day SMA)**
                    - Medium-term intangible trend
                    - Good for trend confirmation

                    **🟤 Brown Line (100-day SMA)**
                    - Long-term intangible value trend
                    - Shows overall brand strength
                    """)

            with tab2:
                col1, col2 = st.columns(2)
                with col1:
                    st.success("📈 **High Intangible P/B**")
                    st.markdown("""
                    **Means:**
                    - Strong brand/IP value
                    - Market believes in intangibles
                    - Premium for innovation

                    **Good for:** Tech, pharma, consumer brands
                    """)
                with col2:
                    st.warning("📉 **Low Intangible P/B**")
                    st.markdown("""
                    **Means:**
                    - Limited brand premium
                    - Commodity-like business
                    - Focus on tangible assets

                    **Common in:** Manufacturing, utilities, basic materials
                    """)

        with st.expander("🎯 Trading This Metric", expanded=False):
            tab1, tab2 = st.tabs(["Entry Signals", "Exit Signals"])

            with tab1:
                st.success("🟢 **Consider Buying When:**")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                    **Technical Signals:**
                    - Intangible P/B above SMAs
                    - Golden cross (20 > 50 SMA)
                    - Bounce off SMA support
                    """)
                with col2:
                    st.markdown("""
                    **Fundamental Support:**
                    - New patents filed
                    - Brand strength growing
                    - Innovation pipeline strong
                    """)

            with tab2:
                st.error("🔴 **Consider Selling When:**")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                    **Technical Signals:**
                    - Intangible P/B below SMAs
                    - Death cross (20 < 50 SMA)
                    - Break below support
                    """)
                with col2:
                    st.markdown("""
                    **Fundamental Concerns:**
                    - Patent expirations
                    - Brand reputation issues
                    - Competitive pressure
                    """)
            st.divider()
            st.markdown('''
                            #### Key Lines Explained:
                            - Black Line: Raw daily intangible P/B ratio (actual market data)
                            - Blue Line: 20-day SMA (short-term trend)
                            - Purple Line: 50-day SMA (medium-term trend)
                            - Red Line: 100-day SMA (long-term trend)
                            ''')
            st.divider()
            st.markdown('''
                            ## 🔍 Reading the Signals
                            ### 1. Trend Direction Analysis
                            #### 📈 Bullish Signals (Market Getting More Optimistic)
                            - Price consistently stays above the SMAs
                            - SMAs are sloping upward
                            - Shorter SMAs (20-day) are above longer SMAs (100-day)
                            #### 📉 Bearish Signals (Market Getting Pessimistic)
                            - Price consistently stays below the SMAs
                            - SMAs are sloping downward
                            - Shorter SMAs (20-day) are below longer SMAs (100-day)
                            ### 2. Golden Cross vs Death Cross
                            #### 🟢 Golden Cross (Strong Buy Signal)
                            - When: 20-day SMA crosses ABOVE 50-day SMA
                            - What it means: Short-term momentum is building
                            - Action: Consider this a strong bullish signal
                            #### 🔴 Death Cross (Strong Sell Signal)
                            - When: 20-day SMA crosses BELOW 50-day SMA  
                            - What it means: Short-term momentum is weakening
                            - Action: Consider this a bearish warning
                            ### 3. Support and Resistance Levels
                            #### Support (Price Floor)
                            - When the intangible P/B ratio bounces off an SMA line
                            - The SMA acts like a "safety net" preventing further decline
                            - Best Support: 50-day and 100-day SMAs
                            #### Resistance (Price Ceiling)
                            - When the intangible P/B ratio gets rejected at an SMA line
                            - The SMA acts like a "barrier" preventing upward movement
                            - Common Resistance: Previous high levels around 1.0-1.2 range
                            ## 📋 Step-by-Step Analysis Workflow
                            ### Step 1: Identify the Overall Trend
                            ✅ Look at the 100-day SMA (red line)
                            - Upward slope = Long-term bullish trend
                            - Downward slope = Long-term bearish trend
                            - Flat = Sideways/consolidation
                            ### Step 2: Check Short-term Momentum
                            ✅ Compare 20-day vs 50-day SMAs
                            - 20-day above 50-day = Building momentum
                            - 20-day below 50-day = Weakening momentum
                            - Recent crossover = Potential trend change
                            ### Step 3: Analyze Current Position
                            ✅ Where is the current price relative to SMAs?
                            - Above all SMAs = Strong bullish position
                            - Below all SMAs = Weak bearish position  
                            - Between SMAs = Transition/uncertainty
                            ### Step 4: Look for Entry/Exit Points
                            ✅ Entry Signals:
                            - Price bounces off SMA support
                            - Golden cross formation
                            - Break above resistance with volume

                            ✅ Exit Signals:
                            - Price breaks below SMA support
                            - Death cross formation
                            - Rejection at resistance levels
                            
                            ## 🎯 Specific Trading Strategies
                            
                            ### Strategy 1: SMA Crossover System
                            - BUY when: 20-day SMA > 50-day SMA AND trending up
                            - SELL when: 20-day SMA < 50-day SMA AND trending down
                            - HOLD when: SMAs are flat or converging
                            
                            ### Strategy 2: Support/Resistance Bounce
                            - BUY when: Price bounces off 50-day SMA support
                            - SELL when: Price gets rejected at SMA resistance
                            - STOP LOSS: Below the supporting SMA
                            
                            ### Strategy 3: Trend Following
                            - LONG BIAS when: Price > 100-day SMA
                            - SHORT BIAS when: Price < 100-day SMA  
                            - NEUTRAL when: Price near 100-day SMA
                            
                            ## ⚠️ Important Warnings & Limitations
                            
                            ### 🚨 Red Flags to Watch
                            1. False Breakouts: Price briefly crosses SMA but immediately reverses
                            2. Whipsaws: Rapid back-and-forth crossovers (common in sideways markets)
                            3. Low Volume: Signals are weaker without confirmation from trading volume
                            4. Market Context: Always consider broader market conditions
                            
                            ### 📊 Data Quality Checks
                            - Missing Data: Gaps in the chart can create false signals
                            - Calculation Errors: Ensure SMAs are properly calculated
                            - Time Frame: Signals are only valid for the timeframe being analyzed
                            ''')


def pb_ratio():
    if st.session_state.ticker and st.session_state != '':
        stock = yf.Ticker(st.session_state.ticker)
        info = stock.info

        hist = stock.history(period="2y")
        # Convert to timezone-naive (ignore +GMTs)
        hist.index = hist.index.tz_localize(None)
        balance_sheet = stock.quarterly_balance_sheet

        # P/B ratio = Price / Book Value per share
        # Book Value per share = Book Value / Shares Outstanding

        if balance_sheet.empty:
            st.error("Balance sheet data is not available for this ticker")
            return None

        # Book Value = Stockholders Equity
        if not balance_sheet.empty and "Stockholders Equity" in balance_sheet.index:
            stockholders_equity = balance_sheet.loc["Stockholders Equity"]
            shares_outstanding = info.get("sharesOutstanding", 1)

            # Book Values per Share
            quarterly_bvps = (stockholders_equity / shares_outstanding)
            quarterly_bvps.name = "Book Value Per Share"
            daily_dates = pd.date_range(
                start=hist.index.min(),
                end=hist.index.max(),
                freq='D'
            )

            # Reindex and interpolate
            # sets new index w/ values NaN since not specified
            daily_bvps = quarterly_bvps.reindex(daily_dates)
            # Fill NaN values using interpolation
            daily_bvps = daily_bvps.interpolate(method='linear')
            daily_bvps = daily_bvps.ffill().bfill()  # Forward/backward fill

            # Calculate daily P/B ratio
            pb_data = []
            for date in hist.index:
                if date in daily_bvps.index:
                    pb_ratio = hist.loc[date, 'Close'] / daily_bvps[date]
                    pb_data.append({
                        'Date': date,
                        'Close': hist.loc[date, 'Close'],
                        'BVPS': daily_bvps[date],
                        'P/B Ratio': pb_ratio
                    })
                else:
                    st.error("No matching dates found")

            pb_df = pd.DataFrame(pb_data)

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=pb_df["Date"].iloc[99:],
                y=pb_df['P/B Ratio'].iloc[99:],
                name='P/B Ratio',
                line=dict(color='#2E86AB', width=2),
            ))

            # Calculation for SMAs
            sma_periods = [20, 50, 100]
            colors = ['#A23B72', '#F18F01', '#C73E1D']
            for period, color in zip(sma_periods, colors):
                pb_df[f"SMA {period}"] = pb_df["P/B Ratio"].rolling(
                    window=period).mean()
                fig.add_trace(go.Scatter(
                    x=pb_df["Date"].iloc[99:],
                    y=pb_df[f"SMA {period}"].iloc[99:],
                    mode='lines',
                    line=dict(color=f"{color}"),
                    name=f"{period}-day SMA",
                ))

            fig.update_layout(title='Tangible Price-to-Book Ratio Over Time',
                              xaxis_title='Date', yaxis_title='Tangible P/B Ratio', height=650)

            st.plotly_chart(fig)

            # Educational content
            st.info(
                "📚 **P/B Ratio**: The classic 'value investing' metric - how much you pay for each dollar of company assets!")

            with st.expander("📖 What is P/B Ratio?", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                    ### 💡 Simple Explanation
                    **Price-to-Book (P/B) = Stock Price ÷ Book Value per Share**

                    **Book Value = Company's net worth**
                    - Total assets minus total debts
                    - What shareholders own if company liquidated
                    - P/B shows if stock is cheap/expensive vs assets
                    """)
                with col2:
                    st.markdown("""
                    ### 🏠 Real Estate Analogy
                    Buying a house worth $200k:
                    - **Pay USD 150k** → P/B = 0.75 (Great deal!)
                    - **Pay USD 200k** → P/B = 1.0 (Fair price)
                    - **Pay USD 300k** → P/B = 1.5 (Expensive, but maybe great location?)

                    Same logic applies to stocks!
                    """)

            with st.expander("🎨 Reading the Chart Lines", expanded=False):
                tab1, tab2 = st.tabs(
                    ["Line Colors & Meanings", "Time Periods"])

                with tab1:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("""
                        **🔵 Blue Line (P/B Ratio)**
                        - Daily price-to-book changes
                        - Raw, unfiltered data
                        - Can be very volatile

                        **🔴 Red Line (20-day SMA)**
                        - Short-term trend
                        - Smooths daily noise
                        - Most reactive to changes
                        """)
                    with col2:
                        st.markdown("""
                        **🟠 Orange Line (50-day SMA)**
                        - Medium-term trend
                        - Balance of speed vs stability
                        - Good confirmation tool

                        **🟤 Brown Line (100-day SMA)**
                        - Long-term trend
                        - Very stable
                        - Shows major direction
                        """)

                with tab2:
                    st.markdown("""
                    ### ⏰ Why Different Time Periods Matter
                    - **20-day**: Quick changes, day-trader friendly
                    - **50-day**: Swing trading, weekly decisions
                    - **100-day**: Long-term investing, monthly reviews
                    - **All together**: Complete picture of momentum
                    """)

            with st.expander("📊 What P/B Values Mean", expanded=False):
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.success("🟢 **P/B < 1.0**")
                    st.markdown("""
                    **Potentially Undervalued**
                    - Stock cheaper than book value
                    - Could be bargain
                    - Or company in trouble

                    **Check:** Why so cheap?
                    """)

                with col2:
                    st.info("🔵 **P/B = 1.0-3.0**")
                    st.markdown("""
                    **Fair to Moderately Priced**
                    - Reasonable valuation
                    - Most stocks trade here
                    - Good for steady companies

                    **Typical:** Banks, industrials
                    """)

                with col3:
                    st.warning("🟡 **P/B > 3.0**")
                    st.markdown("""
                    **Potentially Expensive**
                    - Paying premium for assets
                    - Growth expectations high
                    - Or asset-light business

                    **Common:** Tech companies
                    """)

            with st.expander("🎯 Trading Signals", expanded=False):
                tab1, tab2, tab3 = st.tabs(
                    ["Entry Points", "Exit Points", "Support/Resistance"])

                with tab1:
                    st.success("🟢 **Good Entry Signals**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("""
                        **Strong Signals:**
                        - P/B crosses above all SMAs
                        - Golden cross (20>50 SMA)
                        - Low P/B + upward trend
                        """)
                    with col2:
                        st.markdown("""
                        **What to Confirm:**
                        - Company financials solid?
                        - Industry doing well?
                        - Overall market bullish?
                        """)

                with tab2:
                    st.error("🔴 **Consider Exit Signals**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("""
                        **Warning Signals:**
                        - P/B crosses below SMAs
                        - Death cross (20<50 SMA)
                        - Very high P/B levels
                        """)
                    with col2:
                        st.markdown("""
                        **Risk Factors:**
                        - Fundamentals deteriorating?
                        - Industry headwinds?
                        - Market turning bearish?
                        """)

                with tab3:
                    st.markdown("""
                    ### 🏗️ Support and Resistance
                    **🛡️ Support (Price Floor):** P/B bounces UP when touching SMA line
                    **🚧 Resistance (Price Ceiling):** P/B gets rejected DOWN at SMA line

                    **💡 Trading Tip:** Buy near support, sell near resistance
                    """)

            st.success(
                "💡 **Remember**: P/B works best for asset-heavy companies. For tech/service companies, also check Intangible P/B!")

    else:
        st.warning("Please fill in ticker")


def display_technical_analysis():
    try:
        hist = yf.Ticker(st.session_state.ticker).history(period="2y")
        data = []
        for date in hist.index:
            data.append({
                "Date": date,
                "Open": hist.loc[date, "Open"],
                "Close": hist.loc[date, "Close"],
                "High": hist.loc[date, "High"],
                "Low": hist.loc[date, "Low"],
            })

        df = pd.DataFrame(data)

        fig = go.Figure(go.Candlestick(
            x=df["Date"].iloc[49:],
            open=df["Open"].iloc[49:],
            close=df["Close"].iloc[49:],
            high=df["High"].iloc[49:],
            low=df["Low"].iloc[49:],
            name="Price",
        ))

        sma_periods = [20, 30, 50]
        colors = ['#A23B72', '#F18F01', '#C73E1D']

        for period, color in zip(sma_periods, colors):
            df[f"SMA {period}"] = df["Close"].rolling(window=period).mean()
            fig.add_trace(go.Scatter(
                x=df["Date"].iloc[49:],
                y=df[f"SMA {period}"].iloc[49:],
                name=f"{period} day SMA",
                line=dict(color=color, width=2),
            ))

        fig.update_layout(title='Daily Chart',
                          xaxis_title='Date', yaxis_title='Price ($)', height=700)

        # Consider adding Bollinger Bands

        st.plotly_chart(fig)

        # RSI Indicator

    except Exception as e:
        return f"There is an error: {e}"


def display_DCF_valuation():
    try:
        info = get_company_overview()
        be = BE()
        be.set_ticker(st.session_state.ticker)

        price = info.get("regularMarketPrice", 0)
        dcf = be.get_DCF()

        # Columns for elegance
        col1, col2 = st.columns(2)

        metrics = [
            ("Current Price", price),
            ("DCF Valuation", dcf),
        ]
        for col, (label, value) in zip([col1, col2], metrics):
            # ((col1, ("Current Price", x)),(col2, ("DCF Valuation", y)))
            with col:
                st.metric(label=f"{label}", value=f"${value:,.2f}")
                # Valuation
        if price < dcf:
            st.success(
                "🟢 Stock appears to be UNDERVALUED based on DCF analysis")
        elif price > dcf:
            st.warning("🔴 Stock appears to be OVERVALUED based on DCF analysis")

        with st.expander(label="About Discounted Cashflow", icon="📊"):
            st.write("""
                The DCF (Discounted Cash Flow) model values a company based on 
                the present value of its expected future cash flows. Key components include:
                - Free Cash Flow projections
                - Terminal Value
                - Discount Rate (WACC)
                - Growth Rate assumptions
                """)

    except Exception as e:
        print(f"There is an error: {e}")

def AI_mentor():
    
    be = BE()
           
    # Displays chat in history        
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # User input handling        
    if input := st.chat_input("Ask something"):
        st.session_state.messages.append({"role": "user", "content": input})
        with st.chat_message("user"):
            st.markdown(input)
            
        # Streaming response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for chunk in be.chatbot(st.session_state.messages):
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
st.set_page_config(
    page_title="Financial Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.sidebar.title("🏦 Financial Dashboard")

with st.sidebar:
    ticker_input = st.sidebar.text_input(
        label="Enter Stock Ticker:",
        help="Please enter a valid ticker symbol",
        placeholder="eg. MSFT, AAPL, PLTR",
    )
    st.session_state.ticker = ticker_input.upper()

    options = option_menu(
        menu_title="Options",
        menu_icon="cast",
        options=["Overview", "Financial Statements",
                 "Ratios & Metrics", "Technical Analysis", "DCF Valuation", "Financial Mentor"],
        icons=["house", "file-text", "calculator", "graph-up", "cash-coin", "robot"],
    )

if options == "Overview":

    st.markdown("""
    # 📊 Welcome to Financial Analysis Dashboard

    This dashboard provides comprehensive financial analysis including:
    - 📈 Real-time stock prices and technical indicators
    - 📋 Financial statements (Income, Balance Sheet, Cash Flow)
    - 📊 Financial ratios and metrics
    - 💰 DCF valuation models
    - 📉 Interactive charts and visualizations

    **👈 Enter a stock ticker in the sidebar to get started!**
    """)
    display_overview()
elif options == "Financial Statements":
    st.title("Financial Statements")
    display_financial_statements()
elif options == "Ratios & Metrics":
    st.title("Ratios and Metrics")
    st.write("This is where you will be performing Fundamental Analysis")
    display_ratios_and_metrics()
elif options == "Technical Analysis":
    st.title("Technical Analysis")
    st.write("This is where you will be performing Technical Analysis")
    display_technical_analysis()
elif options == "DCF Valuation":
    st.title("DCF Valuation")
    display_DCF_valuation()
elif options == "Financial Mentor":
    st.title("Your AI Financial Mentor")
    st.write("Ask anything you want!")
    st.divider()
    AI_mentor()
