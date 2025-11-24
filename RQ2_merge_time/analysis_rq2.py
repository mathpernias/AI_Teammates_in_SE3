
import pandas as pd
from scipy.stats import mannwhitneyu
from config import OUTPUT_DIR

def split_ai_human(merged_df: pd.DataFrame):
    """
    Utilise la colonne agent_type pour séparer AI vs Human.
    """
    merged_ai = merged_df[merged_df["agent_type"] == "AI"]
    merged_human = merged_df[merged_df["agent_type"] == "Human"]

    print(f"[DEBUG] PR IA détectés : {len(merged_ai)}")
    print(f"[DEBUG] PR humains détectés : {len(merged_human)}")

    return merged_ai, merged_human

def compute_stats(merged_ai: pd.DataFrame, merged_human: pd.DataFrame) -> str:
    lines = []

    lines.append(f"PR IA : {len(merged_ai)}")
    lines.append(f"PR humains : {len(merged_human)}\n")

    lines.append("=== Merge Time (hours) – IA ===")
    lines.append(str(merged_ai["merge_time_hours"].describe()))
    lines.append("\n=== Merge Time (hours) – Human ===")
    lines.append(str(merged_human["merge_time_hours"].describe()))

    stat, p = mannwhitneyu(
        merged_ai["merge_time_hours"],
        merged_human["merge_time_hours"],
        alternative="two-sided",
    )
    lines.append("\n=== Mann-Whitney U Test ===")
    lines.append(f"stat = {stat}")
    lines.append(f"p-value = {p}")

    return "\n".join(lines)

def save_stats_report(report_text: str, filename: str = "stats_rq2_ai_vs_human.txt"):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / filename
    path.write_text(report_text, encoding="utf-8")
    print(f"[INFO] Stats sauvegardées dans : {path}")
