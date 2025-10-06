import yfinance as yf
from APIkey import _ApiKey as AK
import requests
from zai import ZaiClient

class BackEnd:
    def __init__(self):
        self.ticker_object = None
        self.ticker = None
        self.prompt = '''
You are an expert financial analyst AI integrated into a financial dashboard application. Your purpose is to analyze and interpret various financial metrics and visualizations including Discounted Cash Flow (DCF) vs price comparisons, Price-to-Sales (P/S) graphs, Price-to-Book (P/B) graphs, and comprehensive financial ratios.

When responding to queries:
1. Provide clear, concise financial analysis based on the data presented
2. Explain complex financial concepts in an accessible manner
3. Highlight key insights, trends, and potential red flags in the financial data
4. Offer context for the metrics by comparing to industry standards when relevant
5. Maintain objectivity and avoid making definitive investment recommendations
6. Use appropriate financial terminology while ensuring clarity
7. Structure your responses to be easily digestible in a dashboard interface

Your responses should be accurate, insightful, and focused on helping users understand the financial health and valuation of the companies being analyzed. Always acknowledge limitations in the data when appropriate and suggest additional analysis that might be beneficial.

Remember that you are providing analytical support, not financial advice, and users should make their own investment decisions based on comprehensive research and consultation with qualified financial advisors.
'''

    def set_ticker(self, ticker):
        self.ticker = ticker.upper()
        self.ticker_object = yf.Ticker(self.ticker)

    def get_income_statement(self):
        self.ticker_object.get_income_stmt(
            as_dict=False,
            pretty=True,
            freq="yearly",
        )

    def get_cashflow(self):
        self.ticker_object.get_cashflow(
            as_dict=False,
            pretty=True,
            freq="yearly",
        )

    def get_balance_sheet(self):
        self.ticker_object.get_balance_sheet(
            as_dict=False,
            pretty=True,
            freq="yearly",
        )

    def get_earnings(self):
        self.ticker_object.get_earnings(
            as_dict=False,
            pretty=True,
            freq="yearly",
        )

    def get_growth_estimate(self):
        self.ticker_object.get_growth_estimates(
            as_dict=False
        )

    def get_analysts_price_targets(self):
        self.ticker_object.get_analyst_price_targets()

    def get_major_holders(self):
        self.ticker_object.get_major_holders(
            as_dict=False
        )

    def get_institutional_holders(self):
        self.ticker_object.get_institutional_holders(
            as_dict=False
        )

    def get_DCF(self):
        try:
            api = AK()
            api_key = api.get_FMP_key()

            base_url = "https://financialmodelingprep.com/api/v3/"
            endpoint = "discounted-cash-flow"
            url = f"{base_url}{endpoint}/{self.ticker}?apikey={api_key}"

            response = requests.get(url)

            data = response.json()

            if data:
                dcf_data = data[0] if isinstance(data, list) else data
                return dcf_data.get("dcf", 0)
            else:
                return None

        except Exception as e:
            print(f"Error fetching DCF data: {e}")
            return None
    
                
    def chatbot(self, messages):
        try:
            api = AK()
            ZAI_KEY = api.get_ZAI_key()

            client = ZaiClient(api_key=ZAI_KEY)
            
            full_messages = [
                    {"role": "system", "content": f"{self.prompt}"},
                ] + messages

            response = client.chat.completions.create(
                model="glm-4.5-flash",
                messages=full_messages,
                thinking={
                    "type": "enabled",
                },
                max_tokens=4096,
                temperature=0.6,
                stream= True
            )

            # Stream response
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                            

        except Exception as e:
            yield f"An error occured {e}"
