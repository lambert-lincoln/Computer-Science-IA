import streamlit as st
from data_fetcher import DataFetcher

fetcher = DataFetcher(st.session_state.ticker)

if "stmt.type" not in st.session_state:
    st.session_state.stmt_type = ''

st.title("Financial Statements", anchor=False)
st.write(
    f"This is where you analyze the financial statements for {st.session_state.ticker}")


def display_stmt():
    stmt_dict = fetcher.statement_config.get(st.session_state.stmt_type, None)
    stmt = stmt_dict.get("attr", None)
    cols = stmt_dict.get("cols")

    if not stmt.empty and cols:
        df = stmt.loc[cols]

    st.dataframe(df)


tab1, tab2, tab3 = st.tabs(
    ["Income Statement", "Balance Sheet", "Cash Flow Statement"])

with tab1:
    st.session_state.stmt_type = "INCOME STATEMENT"
    display_stmt()

    if st.button(label="Ask AI Financial Mentor", icon="↗", key="income_statement"):
        st.switch_page("./pages/AI_mentor.py")

    st.divider()
    markdown = '''
    
    ## Income Statement
    An income statement is a financial report used by a business. It tracks the company's revenue, expenses, gains, and losses during a set period.
    It provides valuable insights into a company's operations, the efficiency of its management, underperforming sectors, and its performance relative to industry peers.
    
    '''
    st.markdown(markdown) # description of income statement

with tab2:
    st.session_state.stmt_type = "BALANCE SHEET"
    display_stmt()

    if st.button(label="Ask AI Financial Mentor", icon="↗", key="balance_sheet"):
        st.switch_page("./pages/AI_mentor.py")

    st.divider()
    markdown = '''
    
    ## Balance Sheet
    A balance sheet lists a company's assets, liabilities, and shareholders' equity for an operating period. Balance sheets provide the basis for computing rates of return for investors and evaluating a company's capital structure.
    
    '''
    st.markdown(markdown) # description of balance sheet


with tab3:
    st.session_state.stmt_type = "CASH FLOW"
    display_stmt()

    if st.button(label="Ask AI Financial Mentor", icon="↗", key="cash_flow"):
        st.switch_page("./pages/AI_mentor.py")

    st.divider()
    markdown = '''
    
    ## Cash Flow Statement
    A cash flow statement shows how money flows in and out of a company through operations, investments, and financing activities. The cash flow statement highlights liquidity, how well a business generates cash to fund growth and meet obligations, and helps investors and analysts gauge financial strength and stability.
    
    '''
    st.markdown(markdown) # description of cash flow statement