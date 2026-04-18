from openai_client import OpenAIClient
import pandas as pd
import numpy as np

client = OpenAIClient("gpt-4.1")

df = pd.read_csv("rag_examples.csv")
df_stories = pd.read_csv("evaluation_unique.csv")
embeddings = []

for story in df["user_story"]:
    response = client.client.embeddings.create(
        model="text-embedding-3-large",
        input=story
    )
    embeddings.append(response.data[0].embedding)

df["embedding"] = embeddings

df.to_csv("rag_with_embeddings.csv")  
#stories
embeddings = []

for story in df_stories["user_story"]:
    response = client.client.embeddings.create(
        model="text-embedding-3-large",
        input=story
    )
    embeddings.append(response.data[0].embedding)


df_stories["embedding"] = embeddings

df_stories.to_csv("rag_input_embeddings.csv")