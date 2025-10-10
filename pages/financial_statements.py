import streamlit as st
from data_fetcher import DataFetcher

fetcher = DataFetcher(st.session_state.ticker)

if "stmt.type" not in st.session_state:
    st.session_state.stmt_type = ''

st.title("Financial Statements")
st.write(f"This is where you analyze the financial statements for {st.session_state.ticker}")

def display_stmt():
    stmt_dict = fetcher.statement_config.get(st.session_state.stmt_type, None)
    stmt = stmt_dict.get("attr", None)
    cols = stmt_dict.get("cols")
    
    if not stmt.empty and cols:
        df = stmt.loc[cols]
        
    st.dataframe(df)

tab1, tab2, tab3 = st.tabs(["Income Statement", "Balance Sheet", "Cash Flow Statement"])

with tab1:
    st.session_state.stmt_type = "INCOME STATEMENT"
    display_stmt()
    
    if st.button(label="Ask AI Financial Mentor", icon="↗", key="income_statement"):
        st.switch_page("./pages/AI_mentor.py")

with tab2:
    st.session_state.stmt_type = "BALANCE SHEET"
    display_stmt()
    
    if st.button(label="Ask AI Financial Mentor", icon="↗", key="balance_sheet"):
        st.switch_page("./pages/AI_mentor.py")
    
with tab3:
    st.session_state.stmt_type = "CASH FLOW"
    display_stmt()

    if st.button(label="Ask AI Financial Mentor", icon="↗", key="cash_flow"):
        st.switch_page("./pages/AI_mentor.py")
    
