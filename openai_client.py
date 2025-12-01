from openai import OpenAI
from load_data import *

class OpenAIClient:
    def __init__(self, key_file: str = "bckey.txt"):
        with open(key_file) as f:
            token = f.read().strip()

        self.client = OpenAI(api_key=token)
        self.model = "gpt-4o-mini"

    def prompt(self, message: str) -> str:
        response = self.client.chat.completions.create(
            model = self.model,
            messages = [
                {"role": "user", "content": "Create sequence diagram in plantuml without any comments and without any markdown code fences for the following user story:" + message},
                ]
        )
        return response.choices[0].message.content
    
    def prompt_eval(self, user_story: str, plantuml_code: str) -> str:
        response = self.client.chat.completions.create(
            model = self.model,
            messages = [
                {"role": "user", "content": f"""
            You are an assistant that evaluates a PlantUML sequence diagram based on a given user story.

            USER STORY:
            {user_story}

            SEQUENCE DIAGRAM (PlantUML):
            {plantuml_code}

            Evaluate how well the sequence diagram represents the user story using the following criteria:

            QE1: Is the generated Sequence Diagram (SD) relevant to the given User Story (US)? (Yes/No)
            QE2: Rate the accuracy of object representation and interactions between them (1–10).
            QE3: Rate the accuracy of message and interaction representation (1–10).
            QE4: Rate the accuracy of the message sequence order (1–10).
            QE5: Do you think this tool will save time for Software Engineers when modeling SDs for this user story? (Yes/No)

            FINAL OUTPUT FORMAT (exactly this format) - use only numbers, do not use any comments:
            QE1: ...
            QE2: ...
            QE3: ...
            QE4: ...
            QE5: ...
        """},
                ]
        )
        return response.choices[0].message.content



