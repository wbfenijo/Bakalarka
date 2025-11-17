from openai_client import *
from load_data import *

client = OpenAIClient()

sequenceDiagram_1 = client.prompt("gpt-5", "Generate PlantUML code for a sequence diagram from the following use case:" + useCase1)
