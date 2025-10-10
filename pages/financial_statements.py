import streamlit as st
from data_fetcher import DataFetcher

fetcher = DataFetcher(st.session_state.ticker)

col1, col2, col3 = st.columns(3)

with col1:
    button1 = st.button("Show Income Statement")
    
with col2:
    button2 = st.button("Show Balance Sheet")
    
with col3:
    button3 = st.button("Show Cash Flow Statement")
    
if "stmt_type" not in st.session_state:
    st.session_state.stmt_type = ''

if button1:
    st.session_state.stmt_type = 'INCOME STATEMENT'

def display_income_stmt():
    stmt_dict = fetcher.statement_config.get(st.session_state.stmt_type, None)
    stmt = stmt_dict.get("attr", None)
    cols = stmt_dict.get("cols")
    
    if not stmt.empty and cols:
        df = stmt[cols]
        
    st.dataframe(df)
    
