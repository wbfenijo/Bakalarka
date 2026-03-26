import pandas as pd
import csv
from router import query_model
from prompts import *
from evaluator import MODELS

PROMPTS = [PROMPT_ZS1,
           PROMPT_ZS2,
           PROMPT_ZS3,
           PROMPT_ZS4,
           PROMPT_ZS5]

MODELS = MODELS[:4]

INPUT_FILE = "evaluation_data.csv"
OUTPUT_FILE = "generated_results.csv"
MEMO_FILE = "memo.txt"

user_stories = []

def load_memo():
    try:
        with open(MEMO_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()
    
def save_to_memo(entry):
    with open(MEMO_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")




def main():
    df = pd.read_csv(INPUT_FILE)

    memo = load_memo()

    with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if f.tell() == 0:
            writer.writerow(["model", "prompt_id", "story_id", "user_story", "plantuml"])

        for model in MODELS:
            print(f"\n=== MODEL: {model} ===")

            for p_id, prompt_template in enumerate(PROMPTS, start=1):
                print(f"  Prompt {p_id}")

                for _, row in df.iterrows():
                    story_id = row["story_num"]
                    user_story = row["user_story"]

                    key = f"{story_id},{p_id},{model}"

                    if key in memo:
                        continue

                    prompt = prompt_template.format(USER_STORY=user_story)

                    try:
                        result = query_model(model, prompt)
                    except Exception as e:
                        result = f"ERROR: {e}"

                    writer.writerow([
                        model,
                        p_id,
                        story_id,
                        user_story,
                        result
                    ])

                    f.flush()

                    save_to_memo(key)
                    memo.add(key)

                    print(f"    Saved story {story_id}")

    print("\nDONE")


if __name__ == "__main__":
    main()