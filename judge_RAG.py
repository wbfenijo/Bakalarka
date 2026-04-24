from evaluator import make_prompt, parse_response
import os, csv, pandas as pd
from router import query_model

EVAL_FILE = "rag_generated_results.csv"
MEMO_FILE = "memo_judge_RAG.txt"

MODEL = "azure/gpt-4.1"

#MODEL = "gpt-4o-mini"

count = 0
TOTAL = 0 


def load_memo():
    try:
        with open(MEMO_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()


def save_to_memo(entry):
    with open(MEMO_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")


def evaluate_model(model, user_story, generated_plantuml, writer):
    global count
    count += 1

    print(f"Model: {model}:  {user_story} - {count} / {TOTAL}")

    prompt = make_prompt(user_story, generated_plantuml)
    response = query_model(MODEL, prompt)
    qe = parse_response(response)

    writer.writerow([
        model,
        user_story,
        qe["QE1"],
        qe["QE2"],
        qe["QE3"],
        qe["QE4"],
        qe["QE5"]
    ])


def evaluate_story(row):
    global count

    memo = load_memo()

    user_story = row["user_story"]
    model = row["model"]
    generated_plantuml = row["plantuml"]

    key = f"{model},{user_story}"

    if key in memo:
        print(f"Skipping {key}")
        count += 1
        return

    save_to_memo(key)

    os.makedirs("rag_outputs_eval", exist_ok=True)
    csv_path = os.path.join("rag_outputs_eval", "rag_eval.csv")

    with open(csv_path, "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)

        if file.tell() == 0:
            writer.writerow([
                "model",
                "user_story",
                "QE1",
                "QE2",
                "QE3",
                "QE4",
                "QE5"
            ])

        evaluate_model(model, user_story, generated_plantuml, writer)

        file.flush()
        os.fsync(file.fileno())


if __name__ == "__main__":
    df = pd.read_csv(EVAL_FILE)
    df = df.drop_duplicates(subset=["model", "user_story"])

    TOTAL = len(df)

    for _, row in df.iterrows():
        evaluate_story(row)