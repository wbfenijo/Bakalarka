from openai import OpenAI
from load_data import *

class OpenAIClient:
    def __init__(self, key_file = "bckey.txt"):
        with open(key_file) as f:
            token = f.read().strip()

        self.client = OpenAI(api_key=token)
        self.model = "gpt-4o-mini"

    def prompt(self, message):
        response = self.client.chat.completions.create(
            model = self.model,
            messages = [
                {"role": "user", "content": "Create sequence diagram in plantuml without any comments and without any markdown code fences for the following use case:" + message},
                ]
        )
        return response.choices[0].message.content



