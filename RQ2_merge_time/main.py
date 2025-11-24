# main.py

from data_loader import load_all_pull_requests
import preprocessing
from analysis_rq2 import split_ai_human, compute_stats, save_stats_report
from plots_rq2 import plot_boxplot_merge_time, plot_hist_merge_time

def main():
    # 1) Charger AI + Human
    print("[INFO] Chargement du dataset (AI + Human)...")
    raw_df = load_all_pull_requests()
    print(f"[INFO] Dataset combiné : {raw_df.shape[0]} lignes, {raw_df.shape[1]} colonnes")

    # 2) Prétraitement + merge_time
    print("[INFO] Prétraitement et calcul du merge_time...")
    merged_df = preprocessing.add_datetime_and_merge_time(raw_df)
    print(f"[INFO] PR mergés : {len(merged_df)}")

    # 3) Sauvegarder CSV enrichi
    preprocessing.save_merged_df(merged_df)

    # 4) Split IA vs humain
    merged_ai, merged_human = split_ai_human(merged_df)

    # 5) Stats + test
    report_text = compute_stats(merged_ai, merged_human)
    save_stats_report(report_text)

    # 6) Graphiques
    plot_boxplot_merge_time(merged_ai, merged_human)
    plot_hist_merge_time(merged_ai, merged_human)

    print("\n[OK] Analyse RQ2 (AI vs Human) terminée.")

if __name__ == "__main__":
    main()
