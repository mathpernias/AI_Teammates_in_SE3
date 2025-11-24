# data_loader.py

import pandas as pd
from datasets import load_dataset
from config import (
    DATASET_NAME,
    DATASET_CONFIG_AI,
    DATASET_CONFIG_HUMAN,
    SPLIT,
)

def load_ai_pull_requests() -> pd.DataFrame:
    ds_ai = load_dataset(DATASET_NAME, DATASET_CONFIG_AI)[SPLIT]
    df_ai = ds_ai.to_pandas()

    # Ajoute le type
    df_ai["agent_type"] = "AI"
    df_ai["agent_name"] = df_ai["agent"]  # OpenAI_Codex, Copilot, etc.
    return df_ai

def load_human_pull_requests() -> pd.DataFrame:
    ds_human = load_dataset(DATASET_NAME, DATASET_CONFIG_HUMAN)[SPLIT]
    df_human = ds_human.to_pandas()

    # Certains subsets n'ont pas la colonne 'agent'
    if "agent" not in df_human.columns:
        df_human["agent"] = None

    df_human["agent_type"] = "Human"
    df_human["agent_name"] = "Human"
    return df_human

def load_all_pull_requests() -> pd.DataFrame:
    """
    Retourne un seul DataFrame contenant :
      - PR IA (agent_type = 'AI')
      - PR humains (agent_type = 'Human')
    """
    df_ai = load_ai_pull_requests()
    df_human = load_human_pull_requests()

    df_all = pd.concat([df_ai, df_human], ignore_index=True)
    return df_all

