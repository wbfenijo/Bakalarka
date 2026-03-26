import pandas as pd
import csv
import os

GPT_DATA = r"data-folder\Evaluation\Final CSV_gpt.csv"
TOOL_FOLDER = r"data-folder\Results\Our Tool\Scripts"

with open("selected.txt") as f:
    selected = [line.strip() for line in f]

df = pd.read_csv(GPT_DATA)

def build_row(entry):
    source, sid = entry.split("-")
    sid = int(sid[6:-4])

    row = df[df["ID"] == sid].iloc[0]
    user_story = row["User story"]

    if source == "GPT":
        plantuml = row["GPT Generated seq in PlantUML format"]

    else:
        filename = f"SD{sid}.txt"
        path = os.path.join(TOOL_FOLDER, filename)

        with open(path, encoding="utf-8") as f:
            plantuml = f.read().strip()

    return user_story, plantuml


def write_csv(filename, entries):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["story_num", "user_story", "plantuml"])

        for i, e in enumerate(entries, 1):
            user_story, plantuml = build_row(e)
            writer.writerow([i, user_story, plantuml])


def main():

    all_entries = []
    for sid in df["ID"]:
        all_entries.append(f"GPT-story_{sid}.csv")
        all_entries.append(f"TOOL-story_{sid}.csv")

    remaining = [x for x in all_entries if x not in selected]
    
    write_csv("rag_examples.csv", selected)
    write_csv("evaluation_data.csv", remaining)


if __name__ == "__main__":
    main()