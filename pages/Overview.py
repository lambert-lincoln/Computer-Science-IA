import streamlit as st
from data_fetcher import DataFetcher

def display_overview(ticker: str):
    fetcher = DataFetcher(ticker)
    info = fetcher.get_company_overview()

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


st.title(f"Overview of {st.session_state.ticker}")
display_overview(st.session_state.ticker)