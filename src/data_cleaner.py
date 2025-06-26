import pandas as pd
import re
import os

def clean_budget(budget_str):
    numbers=re.findall(r"\d+", str(budget_str))
    return int(numbers[0]) if numbers else 0

def clean_text(text):
    text = re.sub(r"[^a-zA-Z]", " ", str(text).lower())
    return text.strip()

def cleaned_dataset():
    input_path= os.path.join("..", "data", "raw", "freelancer_raw.csv")
    output_path= os.path.join("..", "data", "processed", "cleaned_data.csv")

    df= pd.read_csv(input_path)
    df["budget_cleaned"]= df["budget"].apply(clean_budget)
    df["skills"]= df["skills"].fillna("")
    df["description_cleaned"]= df["description"].apply(clean_text)

    df.to_csv(output_path, index=False)
    print("Cleaned dataset saved to ", output_path)

if __name__=="__main__":
    cleaned_dataset()