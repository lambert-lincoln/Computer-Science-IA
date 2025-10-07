from APIkey import _ApiKey as AK
from zai import ZaiClient

class AI_mentor():
     def chatbot(self, messages: list):
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