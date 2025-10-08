from figure import Figure
from data_fetcher import DataFetcher
import streamlit as st

def display_price_chart(ticker: str):
    fetcher = DataFetcher(ticker)
    figure = Figure()
    
    price_data = fetcher.get_technical()
    st.plotly_chart(figure.plot_chart(price_data), use_container_width=True)
      
    
