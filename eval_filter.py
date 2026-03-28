import pandas as pd


df = pd.read_csv("evaluation_data.csv")

df_unique = df.drop_duplicates(subset=["user_story"], keep="first")

df_unique.to_csv("evaluation_unique.csv", index=False)