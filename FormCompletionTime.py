
import pandas as pd
from scipy.stats import f_oneway, levene, kruskal
import pingouin as pg

df = pd.read_csv('lead_experiment_dataset.csv')

# Only converters have a meaningful completion time tied to actually finishing the form
conv_df = df[df['converted'] == 1].copy()

summary_time = conv_df.groupby('variant')['time_spent_sec'].agg(['count', 'mean', 'std'])
print("=== Form Completion Time by Variant (converters only) ===")
print(summary_time, "\n")

groups = [conv_df.loc[conv_df['variant'] == v, 'time_spent_sec'] for v in df['variant'].unique()]

# Check variance assumption before trusting standard ANOVA
stat_lev, p_lev = levene(*groups)
print(f"Levene's test for equal variances: stat={stat_lev:.3f}  p={p_lev:.4f}")
print("(p < 0.05 means variances differ, use Welch's ANOVA instead of standard)\n")

# Standard one-way ANOVA
f_stat, p_anova = f_oneway(*groups)
print(f"=== One-Way ANOVA ===")
print(f"F = {f_stat:.3f}   p-value = {p_anova:.6f}\n")

# Welch's ANOVA as a robustness check, same approach as lead quality score
welch = pg.welch_anova(dv='time_spent_sec', between='variant', data=conv_df)
print("=== Welch's ANOVA (robust to unequal variances) ===")
print(welch, "\n")

# Post-hoc, robust version since we expect unequal variance here too
games_howell = pg.pairwise_gameshowell(dv='time_spent_sec', between='variant', data=conv_df)
print("=== Games-Howell Post-Hoc ===")
print(games_howell)
