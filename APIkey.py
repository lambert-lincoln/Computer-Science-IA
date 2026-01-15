from dotenv import load_dotenv
import os
load_dotenv()

class _ApiKey:
    def __init__(self):
        self.api_dict = {
            # see README.md
            "ZAI KEY" : f'{os.getenv("GLM_API_KEY")}', # configured in your .env
        }
    def get_ZAI_key(self):
        return self.api_dict.get('ZAI KEY', 'key not found')
        