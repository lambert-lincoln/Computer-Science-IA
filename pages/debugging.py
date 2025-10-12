import yfinance as yf

ticker_to_test = "AAPL"
stock = yf.Ticker(ticker_to_test)
print(stock.balance_sheet)
