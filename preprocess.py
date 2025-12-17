import pandas as pd

def preprocess_catalogue(df):
    """
    Preprocess SHL catalogue:
    - Combine skills, name, test type for similarity matching
    - Convert skills from ; to space-separated text
    """
    df["skills_text"] = df["skills"].str.replace(";", " ")
    df["combined_text"] = df["assessment_name"] + " " + df["skills_text"] + " " + df["test_type"]
    return df
