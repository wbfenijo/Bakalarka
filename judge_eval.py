from evaluator import make_prompt, parse_response
import os, csv, pandas as pd
from router import query_model

EVAL_FILE = "generated_results_clean.csv"

MODEL = "azure/gpt-4.1"

#MODEL = "gpt-4o-mini"


df = pd.read_csv("generated_results.csv")

df_clean = df.drop_duplicates(
    subset=["model", "user_story", "prompt_id"],
    keep="first"
)

df_clean.to_csv("generated_results_clean.csv", index=False)



def evaluate_model(model, user_story, generated_plantuml, writer, prompt_id):

    print(f"Model: {model}:  {user_story} generated with prompt {prompt_id}")
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
        qe["QE5"],
        prompt_id
    ])


    


def evaluate_story(idx, row):
    user_story = row["user_story"]
    model = row["model"]
    generated_plantuml = row["plantuml"]
    promt_id = row["prompt_id"]

    os.makedirs("generated_outputs_eval", exist_ok=True)
    csv_path = os.path.join("generated_outputs_eval", f"prompt_{promt_id}.csv")

    with open(csv_path, "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["model", "user_story", "QE1", "QE2", "QE3", "QE4", "QE5", "PromptID"])
        evaluate_model(model, user_story, generated_plantuml, writer, promt_id)
        file.flush()
        os.fsync(file.fileno())

    print(f"Finished")




if __name__ == "__main__":
    df = pd.read_csv(EVAL_FILE)

    for idx, row in df.iterrows():
        print(f"\n=== Evaluating ===")
        evaluate_story(idx, row)