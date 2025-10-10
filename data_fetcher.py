import streamlit as st
import yfinance as yf
import pandas as pd


class DataFetcher:
    def __init__(self, ticker: str):

        self.ticker = ticker.upper()
        self.stock = yf.Ticker(self.ticker)

        self.statement_config = {
            "INCOME STATEMENT": {
                "attr": self.stock.income_stmt,
                "quarter": self.stock.quarterly_income_stmt,
                "cols": ["Total Revenue", "Cost Of Revenue", "Gross Profit", "Research And Development",
                         "Selling And Marketing Expense", "General And Administrative Expense",
                         "Operating Expense", "Operating Income", "Net Income"]
            },
            "BALANCE SHEET": {
                "attr": self.stock.balance_sheet,
                "quarter": self.stock.quarterly_balance_sheet,
                "cols": ["Total Assets", "Current Assets", "Cash And Cash Equivalents", "Accounts Receivable",
                         "Net PPE", "Total Liabilities Net Minority Interest", "Total Non Current Liabilities Net Minority Interest", "Current Liabilities", "Accounts Payable",
                         "Total Debt", "Stockholders Equity", "Retained Earnings"]
            },
            "CASH FLOW": {
                "attr": self.stock.cash_flow,
                "quarter": self.stock.quarterly_cash_flow,
                "cols": ["Operating Cash Flow", "Investing Cash Flow", "Financing Cash Flow",
                         "Free Cash Flow", "Capital Expenditure", "Depreciation And Amortization"]
            }
        }

    def get_company_overview(self) -> dict:
        try:
            return self.stock.info

        except Exception as e:
            message = {"error": f"Could not fetch company overview {e}"}
            return message

    def get_hist(self) -> pd.DataFrame:
        hist = self.stock.history(period="2y")
        hist.index = hist.index.tz_localize(None)
        return hist

    def get_financial_statements(self, statement_type: str) -> pd.DataFrame:
        type = statement_type.upper()
        config = self.statement_config.get(type)

        if not config:
            raise ValueError(f"Invalid statement type: {statement_type}")

        raw_stmt = config.get("attr")

        if raw_stmt.empty:
            raise ValueError(f"Data for {statement_type} cannot be found")

        available_cols = [col for col in config.get(
            "cols") if col in raw_stmt.index]
        filtered_stmt = raw_stmt.loc[available_cols]

        return filtered_stmt

    def get_pb_ratio(self) -> pd.DataFrame:
        # P/S Ratio = Market Value Per Share (Price of Stock) / Sales per share
        hist = self.get_hist()
        balance_sheet = self.statement_config.get(
            "BALANCE SHEET").get("quarter")
        income_stmt = self.statement_config.get(
            "INCOME STATEMENT").get("quarter")

        if balance_sheet.empty or income_stmt.empty:
            raise ValueError(
                f"Either the balance sheet or the income statement is empty")

        # Search for proper indeces
        equity_label = next((label for label in balance_sheet.index if "stockholder" in label.lower(
        ) and "equity" in label.lower()), None)
        shares_label = next((label for label in balance_sheet.index if "ordinary" in label.lower(
        ) and "shares" in label.lower() and "number" in label.lower()), None)

        stockholders_equity = balance_sheet.loc[equity_label]
        ordinary_shares = balance_sheet.loc[shares_label]

        stockholders_equity.index = pd.to_datetime(stockholders_equity.index)
        ordinary_shares.index = pd.to_datetime(ordinary_shares.index)

        quarterly_bvps = stockholders_equity / ordinary_shares

        # Start of interpolation
        daily_dates = hist.index
        
        daily_bvps = quarterly_bvps.reindex(daily_dates)
        daily_bvps = daily_bvps.ffill().bfill()
        # End of interpolation

        # P/S Ratio = Market Value Per Share (Price of Stock) / Sales per share
        ps_ratio_series = hist['Close'] / daily_bvps

        result_df = pd.DataFrame({
            "Close": hist['Close'],
            "BVPS": daily_bvps,
            "P/B Ratio": ps_ratio_series,
        }).dropna()

        return result_df

    def get_ev_ebitda_ratio(self) -> pd.DataFrame:
        
        # Daily EV-EBITDA Ratio = daily EV / daily EBITDA
        
        hist = self.get_hist()
        quarterly_bs = self.statement_config.get("BALANCE SHEET").get("quarter")
        quarterly_is = self.statement_config.get("INCOME STATEMENT").get("quarter")

        if quarterly_bs.empty or quarterly_is.empty:
            raise ValueError("Balance sheet or income statement is empty")
        
        daily_dates = hist.index
        
        daily_close = hist['Close']
        daily_shares = quarterly_bs.loc["Share Issued"].reindex(daily_dates).ffill().bfill()
        daily_debt = quarterly_bs.loc["Total Debt"].reindex(daily_dates).ffill().bfill()
        daily_cash = quarterly_bs.loc["Cash And Cash Equivalents"].reindex(daily_dates).ffill().bfill()
        daily_ebitda = quarterly_is.loc["EBITDA"].reindex(daily_dates).ffill().bfill()
        
        daily_ev = (daily_close * daily_shares) + daily_debt - daily_cash
        daily_ev_ebitda = daily_ev / daily_ebitda
        
        result_df = pd.DataFrame({
            "Daily EBITDA": daily_ebitda,
            "Daily EV": daily_ev,
            "Daily EV/EBITDA Ratio": daily_ev_ebitda,
        }).dropna()
        
        return result_df
            
    def get_ps_ratio(self) -> pd.DataFrame:
        # P/S = Price per share / Sales per share

        # Obtaining materials needed
        hist = self.get_hist()
        balance_sheet = self.statement_config.get(
            "BALANCE SHEET").get("quarter")
        income_stmt = self.statement_config.get(
            "INCOME STATEMENT").get("quarter")

        if balance_sheet.empty or income_stmt.empty:
            raise ValueError(
                f"The balance sheet or income statement for this ticker: {self.ticker} cannot be found.")

        sales_label = next((label for label in income_stmt.index if "total" in label.lower(
        ) and "revenue" in label.lower()), None)
        shares_label = next((label for label in balance_sheet.index if "ordinary" in label.lower(
        ) and "shares" in label.lower() and "number" in label.lower()), None)

        total_sales = income_stmt.loc[sales_label]
        shares_outstanding = balance_sheet.loc[shares_label]
        quarterly_sps = total_sales / shares_outstanding

        daily_dates = hist.index

        daily_sps = quarterly_sps.reindex(daily_dates)
        daily_sps = daily_sps.ffill().bfill()

        ps_series = hist['Close'] / daily_sps

        result_df = pd.DataFrame({
            "Close": hist['Close'],
            "Sales Per Share": daily_sps,
            "P/S Ratio": ps_series,
        }).dropna()

        return result_df
    
    def SMA_calculation(
        self, 
        df: pd.DataFrame,
        periods: list = [20, 50, 100]
    ):
        
        metric_columns = None
        
        found_columns = [col for col in df.columns if "ratio" in col.lower()]
        
        if found_columns:
            metric_columns = found_columns
        
        else:
            found_columns = [col for col in df.columns if "close" in col.lower()]
            if found_columns:
                metric_columns = found_columns
        
        df = df.sort_index()
        
        for col in metric_columns:
            for period in periods:
                sma_col_name = f"{col} {period}-day SMA"
                df[sma_col_name] = df[col].rolling(window=period).mean()
                
        return df

    def get_technical(self) -> pd.DataFrame:
        df = self.SMA_calculation(df=self.get_hist()).iloc[99:]
        return df

'''
   def get_basic_ratios_and_metrics(self):
        info = self.stock.info
        ratio_categories = {
            "Profitability": ["grossMargins", "operatingMargins",
                              "returnOnAssets", "returnOnEquity"],
            "Liquidity": ["currentRatio", "quickRatio", "freeCashflow"],
            "Leverage": ["debtToEquity"]
        }
        
        income_stmt = self.statement_config.get("INCOME STATEMENT").get("attr")
        balance_sheet = self.statement_config.get("BALANCE SHEET").get("attr")
        cash_flow = self.statement_config.get("CASH FLOW").get("attr")
    
'''
