import pandas as pd

humans = pd.read_csv('human_prs_enriched.csv')

humans_summary = humans.describe()
print(humans_summary)