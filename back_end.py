from APIkey import _ApiKey as AK
from zai import ZaiClient

class BackEnd:
    def __init__(self):
        # Prompt for LLM
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
                
    def chatbot(self, messages):
        try:
            api = AK()
            ZAI_KEY = api.get_ZAI_key()

            client = ZaiClient(api_key=ZAI_KEY)
            
            # Full message list to be referenced as memory by the LLM
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
