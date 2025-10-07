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
                         "Inventory", "Total Liabilities", "Current Liabilities", "Accounts Payable",
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

    def get_financial_statements(self, statement_type: str) -> pd.DataFrame:
        try:
            statement_type = statement_type.upper()
            config = self.statement_config.get(statement_type)

            if not config:
                raise ValueError(f"Invalid statement type: {statement_type}")

            raw_stmt = config.get("attr")

            if not raw_stmt:
                raise ValueError(f"Data for {statement_type} cannot be found")

            available_cols = [col for col in config.get(
                "cols") if col in raw_stmt.index]
            filtered_stmt = raw_stmt.loc[available_cols]

            return filtered_stmt

        except Exception as e:
            return pd.DataFrame({"error": [f"Could not fetch {statement_type}: {e}"]})

    def get_ps_ratio(self) -> pd.DataFrame:
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
        daily_dates = pd.date_range(
            start=hist.index.min(),
            end=hist.index.max(),
            freq='D'
        )
        daily_bvps = quarterly_bvps.reindex(daily_dates)
        daily_bvps = daily_bvps.interpolate(method="time").ffill().bfill()
        # End of interpolation

        # P/S Ratio = Market Value Per Share (Price of Stock) / Sales per share
        aligned_hist, aligned_bvps = hist.align(daily_bvps, join='inner')
        
        ps_ratio_series = aligned_hist.loc['Close'] / aligned_bvps
        
        result_df = pd.DataFrame({
            "Close": aligned_hist.loc['Close'],
             "BVPS": aligned_bvps,
             "P/B Ratio": ps_ratio_series,
        })
        
        return result_df

    def get_pb_ratio(self) -> pd.DataFrame:
        # P/B ratio = Price / Book Value per share
        hist = self.get_hist()
        balance_sheet = self.statement_config.get(
            "BALANCE SHEET").get("quarter")

        if balance_sheet.empty:
            raise ValueError(
                f"The balance sheet for {self.ticker} cannot be found")

        if not balance_sheet.empty and "Stockholders Equity" in balance_sheet.index:
            # Book Value = Stockholders Equity
            stockholders_equity = balance_sheet.loc["Stockholders Equity"]
            ordinary_shares = balance_sheet.loc["Ordinary Shares Number"]
            # Book Value per share = Book Value / Ordinary Shares Number
            quarterly_bvps = stockholders_equity / ordinary_shares
        else:
            raise ValueError(
                f"Stockholders Equity not found in balance sheet for {self.ticker}")

        # Start of interpolation
        daily_dates = pd.date_range(
            start=hist.index.min(),
            end=hist.index.max(),
            freq='D',
        )

        daily_bvps = quarterly_bvps.reindex(daily_dates)
        daily_bvps = daily_bvps.interpolate(method="linear")
        daily_bvps = daily_bvps.ffill().bfill()

        pb_data = []

        # P/B ratio = Price / Book Value per share
        for date in hist.index:
            if date in daily_bvps.index:
                pb_ratio = hist.loc[date, "Close"] / daily_bvps.loc[date]
                pb_data.append({
                    'Date': date,
                    'P/B Ratio': pb_ratio,
                })
            else:
                raise ValueError(f"No common dates found")

        return pd.DataFrame(pb_data)

    def get_intangible_pb_ratio(self) -> pd.DataFrame:
        pass

    def get_hist(self) -> pd.DataFrame:
        hist = self.stock.history(period="2y")
        hist.index = hist.index.tz_localize(None)


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
