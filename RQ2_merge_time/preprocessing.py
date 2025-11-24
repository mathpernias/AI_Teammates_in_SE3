# preprocessing.py

import pandas as pd
from config import OUTPUT_DIR, MERGED_CSV

def ensure_output_dirs():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def add_datetime_and_merge_time(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convertit les dates en datetime, filtre les PR mergés,
    calcule merge_time_hours et merge_time_days.
    """
    df = df.copy()

    # Conversion en datetime
    df["created_at"] = pd.to_datetime(df["created_at"], utc=True, errors="coerce")
    df["merged_at"]  = pd.to_datetime(df["merged_at"],  utc=True, errors="coerce")
    df["closed_at"]  = pd.to_datetime(df["closed_at"],  utc=True, errors="coerce")

    # Garde seulement les PR mergés
    merged_df = df[df["merged_at"].notna()].copy()

    # Calcul du delta
    delta = merged_df["merged_at"] - merged_df["created_at"]
    merged_df["merge_time_hours"] = delta.dt.total_seconds() / 3600
    merged_df["merge_time_days"]  = merged_df["merge_time_hours"] / 24

    # Enlever les temps négatifs
    merged_df = merged_df[merged_df["merge_time_hours"] >= 0]

    return merged_df

def save_merged_df(merged_df: pd.DataFrame):
    ensure_output_dirs()
    merged_df.to_csv(MERGED_CSV, index=False)
    print(f"[INFO] Fichier sauvegardé : {MERGED_CSV}")
