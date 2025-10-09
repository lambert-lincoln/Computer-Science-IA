from figure import Figure
from data_fetcher import DataFetcher
import streamlit as st

def display_price_chart(ticker: str):
    fetcher = DataFetcher(ticker)
    figure = Figure()
    
    col1, col2, col3 = st.columns(3)
    price_data = fetcher.get_technical()
    
    st.title(f"Price Data {ticker}")
    st.header(f"Daily Chart for {ticker}")
    st.plotly_chart(figure.plot_chart(price_data), use_container_width=True)
    st.divider()
    st.header("Price Data")
    st.data_editor(price_data)
    with col1:
        st.metric(label="Opening Price", value=price_data["Open"].iloc[-1])
    st.markdown("If you need help interpreting this data, you can ask your AI Financial Mentor")
    st.button(label="Ask AI Financial Mentor", icon="↗")
      
    
