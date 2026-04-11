import pandas as pd

for i in range(1, 6):
    df = pd.read_csv(f"generated_outputs_eval\prompt_{i}.csv")

    df_clean = df.drop_duplicates(  
        subset=["model", "user_story", "PromptID"],
        keep="first"
    )
    for _, row in df_clean.iterrows():
        model = row["model"]
        user_story = row["user_story"]
        prompt_id = row["PromptID"]
        entry = f"{model},{user_story},{prompt_id}"
        with open("memo_judge_ZS.txt", "a", encoding="utf-8") as f:
            f.write(entry + "\n")
    df_clean.to_csv(f"generated_outputs_eval\prompt_{i}_clean.csv", index=False)