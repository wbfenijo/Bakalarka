import os
import pandas as pd
import csv
from router import query_model

TOOL_DIR = r"data-folder\Results\Our Tool\Scripts"
count = 0
MODELS = [
    "llama3.1:8b",
    "mistral",

    "gpt-4o-mini",
    "gpt-5",

    "azure/gpt-4.1",
    "azure/gpt-4.1-mini",
    "azure/gpt-4o",
    "azure/gpt-5.1",
    #"devstral-small-2",
    "Gemma3-27b",
    "google/claude-haiku-4-5",
    "google/claude-sonnet-4-5",
    "google/gemini-2.5-flash",
    "google/gemini-2.5-pro",
    "GPT-oss-120b",
    "GPT-oss-20b",
    "Granite-4.0-tiny",
    "Llama-3.1-70b",
    #"minimax-m2.1",
    "Ministral-3-14B-Instruct",
    "Mistral-Small-3.2-24B-Instruct",
    "ollama-embedding-qwen3-06",
    "vision/Qwen3-32b-VL"
]



def make_prompt(user_story: str, generated_code: str) -> str:
    return f"""
You are an expert evaluator of UML sequence diagrams.

Your task is to carefully compare a User Story with a generated PlantUML Sequence Diagram and evaluate how accurately the diagram represents the intended system behavior.

You should evaluate:
- whether the diagram captures the main functionality described in the user story,
- whether the correct actors, objects, and system components are included,
- whether the exchanged messages are meaningful and logically correct,
- whether the interaction order follows a realistic execution flow,
- and whether the generated diagram would be practically useful during software design.

USER STORY:
{user_story}

SEQUENCE DIAGRAM (PlantUML):
{generated_code}

Evaluation principles:

- Evaluate the diagram as if you were reviewing documentation created by a junior software engineer.
- Reward diagrams that are complete, logically consistent, and aligned with the user story.
- Penalize missing participants, incorrect interactions, unrealistic message flow, fabricated functionality, or syntax that suggests misunderstanding of the scenario.
- Use the full scoring range when appropriate.

Detailed guidance:

QE1:
- Return 1 only if the generated diagram is clearly relevant to the described user story.
- Return 0 if the diagram is unrelated, incomplete to the point of being unusable, or models a different scenario.

QE2:
- Evaluate the correctness and completeness of the participants represented in the sequence diagram.
- Focus on whether the diagram contains the appropriate actors, objects, services, system components, or external systems required by the user story.
- Verify that interactions occur between logically correct participants.
- Minor naming differences should not significantly reduce the score if the intended participant roles are clear.
- Penalize missing essential participants, incorrect system entities, redundant objects, or unrealistic communication relationships.
- High scores should correspond to diagrams where the represented objects and their interactions closely match the intended system structure described in the user story.

QE3:
- Focus on the semantic correctness of messages and interactions.
- Determine whether the exchanged messages correctly model the intended behavior and communication.
- Higher scores indicate realistic and meaningful interaction logic.

QE4:
- Focus on temporal and logical ordering of interactions.
- Verify whether the sequence of messages follows the expected workflow from the user story.
- Penalize misplaced, reversed, or inconsistent interaction order.

QE5:
- Evaluate practical usefulness from the perspective of a software engineer creating sequence diagrams during analysis or design.
- Return 1 if the generated diagram already provides a mostly correct and reusable interaction structure, even if small corrections would still be necessary.
- Return 1 when the diagram captures the main workflow, important participants, and meaningful interactions well enough to reduce manual modeling effort.
- Return 0 only if the diagram is largely incorrect, misleading, missing critical interactions, or would require substantial rework before it could be used.
- Focus on whether the diagram accelerates the modeling process, not whether it is perfect.

QE1: Is the generated Sequence Diagram (SD) relevant to the given User Story (US)? 0/1 (Yes/No)

QE2: Rate the accuracy of object representation and interactions between them on a scale of 1 to 10.

QE3: Rate the accuracy of message and interaction representation on a scale of 1 to 10.

QE4: Rate the accuracy of the message sequence order on a scale of 1 to 10.

QE5: Do you think this tool will save time for the Software Engineers to model SD for this particular user story? 0/1 (Yes/No)

Return ONLY the following format exactly:

QE1: ...
QE2: ...
QE3: ...
QE4: ...
QE5: ...
"""




def parse_response(response: str) -> dict:
    qe = {"QE1": "0", "QE2": "1", "QE3": "1", "QE4": "1", "QE5": "0"}

    for line in response.splitlines():
        t = line.strip()
        if ":" not in t:
            continue
        key, val = t.split(":", 1)
        val = val.strip()

        digits = "".join(filter(str.isdigit, val))

        if key == "QE1" or key == "QE5":
            qe[key] = "1" if digits == "" or digits[0] == "1" else "0"
        elif key in ["QE2", "QE3", "QE4"]:
            if digits == "":
                qe[key] = "1"
            else:
                n = int(digits)
                qe[key] = str(min(max(n, 1), 10))
    return qe



def write_human_scores(row, writer):
    writer.writerow([
        "GPT",
        "Human",
        row["QE1 (GPT)"],
        row["QE2 (GPT)"],
        row["QE3 (GPT)"],
        row["QE4 (GPT)"],
        row["QE5 (GPT)"],
        "None"
    ])
    writer.writerow([
        "Tool",
        "Human",
        row["QE1(Our Tool)"],
        row["QE2 (Our Tool)"],
        row["QE3 (Our Tool)"],
        row["QE4 (Our Tool)"],
        row["QE5 (Our Tool)"],
        "None"
    ])



def evaluate_diagram(user_story, diagram_code, generated_by, csv_path):
    global count
    if os.path.exists(csv_path):
        df_existing = pd.read_csv(csv_path)
        existing_pairs = set(zip(df_existing["Generated by"], df_existing["Model"]))
    else:
        existing_pairs = set()

    with open(csv_path, "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["Generated by", "Model", "QE1", "QE2", "QE3", "QE4", "QE5", "Prompt"])

        for model_name in MODELS:
            count += 1
            if (generated_by, model_name) in existing_pairs:
                print(f"Skipping {model_name} for {generated_by} — already done")
                continue
            print(f"Model: {model_name} evaluating {generated_by}")
            prompt = make_prompt(user_story, diagram_code)
            response = query_model(model_name, prompt)
            qe = parse_response(response)

            writer.writerow([
                generated_by,
                model_name,
                qe["QE1"],
                qe["QE2"],
                qe["QE3"],
                qe["QE4"],
                qe["QE5"],
                prompt
            ])

            file.flush()
            os.fsync(file.fileno())




def evaluate_story(idx, row):
    global count
    user_story = row["User story"]

    with open(TOOL_DIR + f"/SD{idx + 1}.txt") as file:
        generated_tool = file.read()

    generated_gpt = row["GPT Generated seq in PlantUML format"]

    os.makedirs("evaluation_outputs", exist_ok=True)
    csv_path = os.path.join("evaluation_outputs", f"story_{idx}.csv")

    with open(csv_path, "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["Generated by", "Model", "QE1", "QE2", "QE3", "QE4", "QE5", "Prompt"])
            write_human_scores(row, writer)

    evaluate_diagram(user_story, generated_tool, "Tool", csv_path)
    evaluate_diagram(user_story, generated_gpt, "GPT", csv_path)

    print(f"Finished Story {idx} - {count} / {len(MODELS) * 200}")



if __name__ == "__main__":
    print(len(MODELS))
    df = pd.read_csv(r"data-folder\Evaluation\Final CSV_gpt.csv")
    for idx, row in df.iterrows():

        print(f"\n=== Evaluating Story {idx} ===")
        evaluate_story(idx, row)