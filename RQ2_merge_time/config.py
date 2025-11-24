from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

OUTPUT_DIR = PROJECT_ROOT / "outputs"
PLOTS_DIR = OUTPUT_DIR / "plots"

MERGED_CSV = OUTPUT_DIR / "merged_pr_with_merge_time.csv"

# Dataset HuggingFace
DATASET_NAME = "hao-li/AIDev"
DATASET_CONFIG_AI = "all_pull_request"      
DATASET_CONFIG_HUMAN = "human_pull_request" 
SPLIT = "train"
