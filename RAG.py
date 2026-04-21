import numpy as np
import pandas as pd
import os, csv, ast
from router import query_model
from evaluator import MODELS


MODELS = MODELS[:4]
MEMO_FILE = "memo_RAG.txt"
EXAMPLES_FILE = "examples.txt"
TOTAL = len(MODELS) * 80
EXAMPLES = []
count = 0



def load_examples():
    global EXAMPLES
    df = pd.read_csv("rag_examples.csv")
    for _, row in df.iterrows():
        EXAMPLES.append(row["user_story"])




def load_memo():
    try:
        with open(MEMO_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()
    
def save_to_memo(entry):
    with open(MEMO_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")



def cosine_similarity(a, b):
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_top_k_examples(query, embedding, k=3):
    global rag_df
    df = rag_df
    df["similarity"] = df["embedding"].apply(
    lambda x: cosine_similarity(np.array(ast.literal_eval(x), dtype=float), np.array(ast.literal_eval(embedding), dtype=float))
    )

    top_k = df.sort_values("similarity", ascending=False).head(k)

    return top_k

def build_rag_prompt(user_story, examples_df):
    examples_text = ""

    for _, row in examples_df.iterrows():
        examples_text += f"""
    Example:
    User story:
    {row['user_story']}

    Sequence diagram:
    {row['plantuml']}
    """

        return f"""
    You are a software engineer specialized in UML modeling.

    Here are examples of correct sequence diagrams:

    {examples_text}

    Now generate a sequence diagram for the following user story:

    {user_story}

    Rules:
    - Return only valid PlantUML
    - Start with @startuml and end with @enduml
    """


rag_df = pd.read_csv("rag_with_embeddings.csv")

def generate_with_rag(user_story, model):
    top_examples = get_top_k_examples(user_story, k=3)

    prompt = build_rag_prompt(user_story, top_examples)

    return query_model(model, prompt)

def main():
    INPUT_FILE = "rag_input_embeddings.csv"
    OUTPUT_FILE = "rag_generated_results.csv"

    global count
    load_examples()
    df = pd.read_csv(INPUT_FILE)
    memo = load_memo()

    with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow([
                "model",
                "story_id",
                "user_story",
                "plantuml"
            ])

        for model in MODELS:
            print(f"\n=== MODEL: {model} ===")

            for idx, row in df.iterrows():
                story_id = row["story_num"]
                user_story = row["user_story"]
                embeddings = row["embedding"]
                key = f"{model},{user_story}"
                if user_story in EXAMPLES:
                    count += 1
                    print(f"  Skipping {user_story} - user story as example")
                    continue
                if key in memo:
                    count += 1
                    print(f"  Skipping {key} - already done")
                    continue
                print(f"  Story {story_id}")

                try:
                    examples = get_top_k_examples(user_story, embeddings)
                    prompt = build_rag_prompt(user_story, examples)
                    result = query_model(model, prompt)

                except Exception as e:
                    quit()

                writer.writerow([
                    model,
                    story_id,
                    user_story,
                    result
                ])
                save_to_memo(key)
                f.flush()
                os.fsync(f.fileno())

    print("\nDONE")


if __name__ == "__main__":
    main()