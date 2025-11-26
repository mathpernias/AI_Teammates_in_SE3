
import matplotlib.pyplot as plt
from config import PLOTS_DIR
import pandas as pd
def ensure_plots_dir():
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

def plot_boxplot_merge_time(merged_ai, merged_human, max_hours=72):

    ensure_plots_dir()

    # On coupe les valeurs extrêmes pour mieux voir la "zone normale"
    ai_trimmed = merged_ai[merged_ai["merge_time_hours"] <= max_hours]
    human_trimmed = merged_human[merged_human["merge_time_hours"] <= max_hours]

    plt.figure(figsize=(8, 6))
    plt.boxplot(
        [ai_trimmed["merge_time_hours"], human_trimmed["merge_time_hours"]],
        labels=["AI", "Human"],
        showfliers=False,
    )
    plt.ylabel("Merge Time (hours)")
    plt.title(f"Merge Time Comparison (0–{max_hours} hours)")

    out_path = PLOTS_DIR / f"boxplot_merge_time_ai_vs_human_{max_hours}h.png"
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()
    print(f"[INFO] Boxplot AI vs Human sauvegardé : {out_path}")

    # Variante en log-scale pour voir encore mieux
    plt.figure(figsize=(8, 6))
    plt.boxplot(
        [ai_trimmed["merge_time_hours"], human_trimmed["merge_time_hours"]],
        labels=["AI", "Human"],
        showfliers=False,
    )
    plt.yscale("log")
    plt.ylabel("Merge Time (hours, log scale)")
    plt.title(f"Merge Time Comparison (0–{max_hours} hours, log-scale)")

    out_path_log = PLOTS_DIR / f"boxplot_merge_time_ai_vs_human_{max_hours}h_log.png"
    plt.savefig(out_path_log, bbox_inches="tight")
    plt.close()
    print(f"[INFO] Boxplot log-scale AI vs Human sauvegardé : {out_path_log}")

def plot_hist_merge_time(merged_ai, merged_human, max_hours=72, bins=50):

    ensure_plots_dir()

    ai_trimmed = merged_ai[merged_ai["merge_time_hours"] <= max_hours]
    human_trimmed = merged_human[merged_human["merge_time_hours"] <= max_hours]

    plt.figure(figsize=(10, 6))
    plt.hist(
        ai_trimmed["merge_time_hours"],
        bins=bins,
        alpha=0.6,
        label="AI",
        density=True,
    )
    plt.hist(
        human_trimmed["merge_time_hours"],
        bins=bins,
        alpha=0.6,
        label="Human",
        density=True,
    )
    plt.xlabel("Merge Time (hours)")
    plt.ylabel("Density")
    plt.xlim(0, max_hours)
    plt.legend()
    plt.title(f"Merge Time Distribution: AI vs Human (0–{max_hours} hours)")

    out_path = PLOTS_DIR / f"hist_merge_time_ai_vs_human_{max_hours}h.png"
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()
    print(f"[INFO] Histogramme AI vs Human sauvegardé : {out_path}")


def plot_cumulative_approvals(merged_ai, merged_human):

    ensure_plots_dir()

    # Convertir merged_at en datetime
    merged_ai["merged_at"] = pd.to_datetime(merged_ai["merged_at"], utc=True)
    merged_human["merged_at"] = pd.to_datetime(merged_human["merged_at"], utc=True)

    # Grouper par jour
    ai_daily = merged_ai.groupby(merged_ai["merged_at"].dt.date).size().cumsum()
    human_daily = merged_human.groupby(merged_human["merged_at"].dt.date).size().cumsum()

    # 1. GRAPHIQUE NORMALISÉ
    ai_norm = ai_daily / ai_daily.max()
    human_norm = human_daily / human_daily.max()

    plt.figure(figsize=(12, 6))
    plt.plot(ai_norm.index, ai_norm.values, label="AI", linewidth=3)
    plt.plot(human_norm.index, human_norm.values, label="Human", linewidth=3)

    plt.xlabel("Date")
    plt.ylabel("Normalized Cumulative Approvals (0 → 1)")
    plt.title("Normalized Cumulative PR Approvals Over Time (AI vs Human)")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    out_path = PLOTS_DIR / "cumulative_normalized_ai_vs_human.png"
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()

    print(f"[INFO] Normalized cumulative plot saved: {out_path}")

    # 2. GRAPHIQUE AVEC AXE LOGARITHMIQUE
    plt.figure(figsize=(12, 6))
    plt.plot(ai_daily.index, ai_daily.values, label="AI", linewidth=2)
    plt.plot(human_daily.index, human_daily.values, label="Human", linewidth=2)

    plt.yscale("log")
    plt.xlabel("Date")
    plt.ylabel("Cumulative merged PRs (log scale)")
    plt.title("Cumulative PR Approvals Over Time (AI vs Human) - Log Scale")
    plt.legend()
    plt.grid(True, which="both", ls="--")
    plt.xticks(rotation=45)
    plt.tight_layout()

    out_path = PLOTS_DIR / "cumulative_log_ai_vs_human.png"
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()

    print(f"[INFO] Log-scale cumulative plot saved: {out_path}")

    # 3. GRAPHIQUE CLASSIQUE AMÉLIORÉ
    plt.figure(figsize=(12, 6))
    plt.plot(ai_daily.index, ai_daily.values, label="AI", linewidth=2)
    plt.plot(human_daily.index, human_daily.values, label="Human", linewidth=2)

    plt.xlabel("Date")
    plt.ylabel("Cumulative merged PRs")
    plt.title("Cumulative PR Approvals Over Time (AI vs Human)")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    out_path = PLOTS_DIR / "cumulative_raw_ai_vs_human.png"
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()

    print(f"[INFO] Raw cumulative plot saved: {out_path}")

