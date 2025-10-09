import pandas as pd
import yfinance as yf
from data_fetcher import DataFetcher
import streamlit as st
from figure import Figure as fig

figure = fig()
ticker_to_test = "AAPL"
stock = yf.Ticker(ticker=ticker_to_test)
fetcher = DataFetcher(ticker_to_test)
price_data = fetcher.get_technical()
st.plotly_chart(figure.plot_chart(price_data), use_container_width=True, height=800)
st.write(price_data)
st.metric(label="Opening Price", value=price_data["Open"].iloc[-1])

