from openai_client import OpenAIClient
import pandas as pd
import numpy as np

client = OpenAIClient("gpt-4.1")

df = pd.read_csv("rag_examples.csv")

embeddings = []

for story in df["user_story"]:
    response = client.client.embeddings.create(
        model="text-embedding-3-large",
        input=story
    )
    embeddings.append(response.data[0].embedding)

df["embedding"] = embeddings

df.to_pickle("rag_with_embeddings.pkl")  