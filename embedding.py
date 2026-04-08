from openai import OpenAI
import pandas as pd
import numpy as np

client = OpenAI()

df = pd.read_csv("rag_examples.csv")

embeddings = []

for story in df["user_story"]:
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=story
    )
    embeddings.append(response.data[0].embedding)

df["embedding"] = embeddings

df.to_pickle("rag_with_embeddings.pkl")  