from openai import OpenAI
from load_data import *

with open("bckey.txt") as f:
    token = f.read().strip()



client = OpenAI(api_key=token)
response = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "user", "content": "Generate a PlantUML code for a sequence diagram from the following use case: " + useCase1}
    ]
)
with open(r"data/outputsAI/SD1.puml", "w") as file:
    file.write(response.choices[0].message.content)
