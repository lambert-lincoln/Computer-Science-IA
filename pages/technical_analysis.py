from figure import Figure
from data_fetcher import DataFetcher
import streamlit as st
import pages.AI_mentor as ai_mentor_page

def display_price_chart(ticker: str):
    fetcher = DataFetcher(ticker)
    figure = Figure()
    
    price_data = fetcher.get_technical()
    
    st.title(f"Price Data {ticker}")
    st.header(f"Daily Chart for {ticker}")
    st.plotly_chart(figure.plot_chart(price_data), use_container_width=True)
    st.divider()
    st.header("Price Data")
    st.data_editor(price_data)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        change = price_data["Close"].iloc[-1]- price_data["Close"].iloc[-2]
        percentage = (change/price_data["Close"].iloc[-1])*100
        st.metric(label="Opening Price", value=price_data["Open"].iloc[-1], delta=percentage)
    with col2: 
        st.metric(label="Closing Price", value=price_data["Close"].iloc[-1])
    with col3:
        st.metric(label="Highest Price", value=price_data["High"].iloc[-1])
    with col4:
        st.metric(label="Lowest Price", value=price_data["Low"].iloc[-1])
    
    st.markdown("If you need help interpreting this data, you can ask your AI Financial Mentor")
    st.button(label="Ask AI Financial Mentor", icon="↗", on_click=ai_mentor_page.initiate_chatbot(input=price_data))
      
    
