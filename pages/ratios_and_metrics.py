from data_fetcher import DataFetcher
from figure import Figure
import streamlit as st

fetcher = DataFetcher(st.session_state.ticker)
fig = Figure()

def display_ratios_and_metrics():
    st.title("Important Ratios and Metrics",
             help="You can ask more on these metrics using our AI Financial Mentor")
    st.markdown(
        "The following are important ratios and metrics. For more information, you can consult out AI Financial Mentor")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["General Metrics", "Price-to-Sales Ratio", "Price-to-Book Ratio", "EV-EBITDA Ratio"])
    
    with tab1:
        st.subheader(f"Profitability Ratios for {st.session_state.ticker}")
        
        quarterly_income_stmt = fetcher.statement_config.get("INCOME STATEMENT").get("quarter")
        quarterly_balance_sheet = fetcher.statement_config.get("BALANCE SHEET").get("quarter")
        
        col1, col2, col3, col4= st.columns(4)
        
        with col1:
            gross_profit = quarterly_income_stmt.loc["Gross Profit"]
            total_rev = quarterly_income_stmt.loc["Total Revenue"]
            gpm = (gross_profit/total_rev) * 100
            if len(gpm) > 0:
                latest_gpm = gpm.iloc[0]
                if len(gpm) >= 2 and gpm.iloc[1] != 0:
                    change = ((latest_gpm - gpm.iloc[1]) / gpm.iloc[1]) * 100
                else:
                    change = 0
            
            st.metric(label="Gross Profit Margin", value=f"{latest_gpm:.2f}%", delta=f"{change:.2f}%")
        
        with col2:
            operating_profit = quarterly_income_stmt.loc["Operating Income"]
            total_rev = quarterly_income_stmt.loc["Total Revenue"]
            opm = (operating_profit/total_rev) * 100
            if len(opm) > 0:
                latest_opm = opm.iloc[0]
                if len(opm) >= 2 and opm.iloc[1] != 0:
                    change = ((latest_opm - opm.iloc[1]) / opm.iloc[1]) * 100
                else:
                    change = 0
            
            st.metric(label="Operating Margin", value=f"{latest_opm:.2f}%", delta=f"{change:.2f}%")
        
        with col3:
            net_income = quarterly_income_stmt.loc["Net Income"]
            total_rev = quarterly_income_stmt.loc["Total Revenue"]
            npm = (net_income/total_rev) * 100
            if len(npm) > 0:
                latest_npm = npm.iloc[0]
                if len(npm) >= 2 and npm.iloc[1] != 0:
                    change = ((latest_npm - npm.iloc[1]) / npm.iloc[1]) * 100
                else:
                    change = 0
            
            st.metric(label="Net Profit Margin", value=f"{latest_npm:.2f}%", delta=f"{change:.2f}%")
            
        with col4:
            net_income = quarterly_income_stmt.loc["Net Income"]
            equity = quarterly_balance_sheet.loc["Stockholders Equity"]
            roe = (net_income/equity) * 100
            if len(roe) > 0:
                latest_roe = roe.iloc[-1]
                if len(roe) >= 2 and roe.iloc[-2] != 0:
                    change = ((latest_roe - roe.iloc[1]) / roe.iloc[-2]) * 100
                else:
                    change = 0
                    
            st.metric(label="Return on Equity", value=f"{latest_roe:.2f}%", delta=f"{change:.2f}%")
    
        st.subheader(f"Liquidity Ratios for {st.session_state.ticker}")
        
        col5, col6 = st.columns(2)
        
        with col5:
            ca = quarterly_balance_sheet.loc["Current Assets"]
            cl = quarterly_balance_sheet.loc["Current Liabilities"]
            cr = ca/cl

            if len(cr) > 0:
                latest_cr = cr.iloc[0]
                if len(cr) >= 2 and cr.iloc[1] != 0:
                    change = ((latest_cr - cr.iloc[1]) / cr.iloc[1]) * 100
                else:
                    change = 0
            
            st.metric(label="Current Ratio", value=f"{latest_cr:.2f}", delta=f"{change:.2f}%")
        
        with col6:
            cce = quarterly_balance_sheet.loc["Cash And Cash Equivalents"]
            cl = quarterly_balance_sheet.loc["Current Liabilities"]
            cash_ratio = cce/cl
            
            if len(cash_ratio) > 0:
                latest_cash_ratio = cr.iloc[0]
                if len(cash_ratio) >=2 and cash_ratio.iloc[1] != 0:
                    change = ((latest_cash_ratio - cash_ratio.iloc[1]) / cash_ratio.iloc[1]) * 100
                else:
                    change = 0
            st.metric(label="Cash Ratio", value=f"{latest_cash_ratio:.2f}", delta=f"{change:.2f}%")
         
        st.subheader("Efficiency Ratios")

        total_rev = quarterly_income_stmt.loc["Total Revenue"]
        total_assets = quarterly_balance_sheet.loc["Total Assets"]
        asset_turnover = total_rev / total_assets
            
        if len(asset_turnover) > 0:
            latest_asset_turnover = asset_turnover.iloc[-1]
            if len(asset_turnover) >= 2 and asset_turnover.iloc[-2] != 0:
                change = ((latest_asset_turnover - asset_turnover.iloc[-2]) / asset_turnover.iloc[-2]) * 100
            else:
                change = 0

        st.metric(label="Asset Turnover", value=f"{latest_asset_turnover:.2f}", delta=f"{change:.2f}%")
                            
    with tab2:
        st.subheader(f"Price-to-Sales Chart for {st.session_state.ticker}")
        ps_df = fetcher.get_ps_ratio()
        ps_df = fetcher.SMA_calculation(ps_df)
        st.plotly_chart(fig.make_fig(ps_df))
        st.divider()
        st.subheader("Price-to-Sales Dataframe")
        st.dataframe(ps_df.iloc[99:])
        st.markdown("If you need help interpreting this data, you can ask your AI Financial Mentor")
        if st.button(label="Ask AI Financial Mentor", icon="↗", key="price-to-sales"):
            st.switch_page("./pages/AI_mentor.py")
    
    with tab3:
        st.subheader(f"Price-to-Book Chart for {st.session_state.ticker}")
        df = fetcher.get_pb_ratio()
        pb_df = fetcher.SMA_calculation(df=df)
        st.plotly_chart(fig.make_fig(pb_df))
        st.divider()
        st.subheader("Price-to-Book Dataframe")
        st.dataframe(pb_df.iloc[99:])
        st.markdown("If you need help interpreting this data, you can ask your AI Financial Mentor")
        if st.button(label="Ask AI Financial Mentor", icon="↗", key="price-to-book"):
            st.switch_page("./pages/AI_mentor.py")
        
    with tab4:
        st.subheader(f"EV-to-EBITDA Chart for {st.session_state.ticker}")
        df = fetcher.get_ev_ebitda_ratio()
        ev_ebitda_df = fetcher.SMA_calculation(df=df)
        st.plotly_chart(fig.make_fig(ev_ebitda_df))
        st.divider()
        st.subheader("EV-to-EBITDA Dataframe")
        st.dataframe(ev_ebitda_df.iloc[99:])
        if st.button(label="Ask AI Financial Mentor", icon="↗", key="ev-ebitda"):
            st.switch_page("./pages/AI_mentor.py")
        
display_ratios_and_metrics()
