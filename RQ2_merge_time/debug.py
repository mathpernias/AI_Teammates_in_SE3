from data_loader import load_ai_pull_requests, load_human_pull_requests
import pandas as pd

# Charger les datasets séparés
df_ai = load_ai_pull_requests()
df_human = load_human_pull_requests()

print("\n=== AI Dataset (first 10 rows) ===")
print(df_ai.head(10))

print("\n=== Human Dataset (first 10 rows) ===")
print(df_human.head(10))

# Version combinée
df_ai["agent_type"] = "AI"
df_human["agent_type"] = "Human"

df_all = pd.concat([df_ai, df_human], ignore_index=True)

print("\n=== Combined Dataset (first 10 rows) ===")
print(df_all.head(10))

print("\n=== Column names (combined) ===")
print(df_all.columns)
