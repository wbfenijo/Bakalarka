from openai import OpenAI
from load_data import *

class OpenAIClient:
    def __init__(self, key_file = "bckey.txt"):
        with open(key_file) as f:
            api_key = f.read().strip()

        self.client = OpenAI(api_key=api_key)

    def prompt(self, model, message):
        response = self.client.chat.completions.create(
            model = model,
            messages = [{"role": "user", "content": message}]
        )
        return response.choices[0].message.content



