
import pandas as pd
import pingouin as pg

df = pd.read_csv('lead_experiment_dataset.csv')
conv_df = df[df['converted'] == 1].copy()

welch = pg.welch_anova(dv='lead_quality_score', between='variant', data=conv_df)
print("=== Welch's ANOVA (robust to unequal variances) ===")
print(welch)

games_howell = pg.pairwise_gameshowell(dv='lead_quality_score', between='variant', data=conv_df)
print("\n=== Games-Howell Post-Hoc (robust equivalent of Tukey) ===")
print(games_howell)
