
import matplotlib.pyplot as plt
from config import PLOTS_DIR

def ensure_plots_dir():
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

def plot_boxplot_merge_time(merged_ai, merged_human, max_hours=72):
    """
    Boxplot AI vs Human sur une fenêtre raisonnable (0 à max_hours),
    avec une échelle log pour mieux voir les différences.
    """
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
    """
    Histogramme AI vs Human sur 0–max_hours, normalisé (densité)
    pour comparer les formes de distribution.
    """
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
