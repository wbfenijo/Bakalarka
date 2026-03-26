import os
import pandas as pd
from sklearn.model_selection import train_test_split
from correlation import normalize_row
EVAL_DIR = "evaluation_outputs/"
all_files = [f for f in os.listdir(EVAL_DIR) if f.endswith(".csv")]

with open("selected.txt") as f:
    selected = [line.strip().split("-")[1] for line in f]



df_list = []

for file in all_files:
    if file in selected:
        continue
    path = os.path.join(EVAL_DIR, file)
    df = pd.read_csv(path)
    df_list.append(df)

all_combined_df = pd.concat(df_list, ignore_index=True)

all_combined_df.to_csv( "all_combined.csv", index=False)
print(f"Combined {len(all_files)} CSVs into all_combined.csv")


df = all_combined_df.copy()


cols = ['QE1','QE2','QE3','QE4','QE5']

df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

df_norm = df.apply(normalize_row, axis=1, result_type='expand')
df['avg_rating'] = df_norm.mean(axis=1)



df['stratified'] = pd.cut(df['avg_rating'], bins=3, labels=['low','med','high']).astype(str)


train_df, judge_df = train_test_split(df, test_size=0.2, stratify=df['stratified'], random_state=42)

