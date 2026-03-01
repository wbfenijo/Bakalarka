from openai import OpenAI
from load_data import *

class OpenAIClient:
    def __init__(self, model, key_file: str = "bckey.txt"):
        with open(key_file) as f:
            token = f.read().strip()

        self.client = OpenAI(api_key=token)
        self.model = model

    def prompt(self, message: str) -> str:
        response = self.client.chat.completions.create(
            model = self.model,
            messages = [
                {"role": "user", "content": "Create sequence diagram in plantuml without any comments and without any markdown code fences for the following user story:" + message},
                ]
        )
        return response.choices[0].message.content
    
    def prompt_eval(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model = self.model,
            messages = [
                {"role": "user", "content": prompt},
                ]
        )
        return response.choices[0].message.content



