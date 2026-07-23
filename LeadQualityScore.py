
import pandas as pd
from scipy.stats import f_oneway, levene
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd

df = pd.read_csv('lead_experiment_dataset.csv')

# Guardrail metric only applies to converters (non-converters are scored 0 by definition)
conv_df = df[df['converted'] == 1].copy()

# Summary by variant
summary_q = conv_df.groupby('variant')['lead_quality_score'].agg(['count', 'mean', 'std'])
print("=== Lead Quality Score by Variant (converters only) ===")
print(summary_q, "\n")

# Check variance assumption before trusting a standard ANOVA
groups = [conv_df.loc[conv_df['variant'] == v, 'lead_quality_score'] for v in df['variant'].unique()]
stat_lev, p_lev = levene(*groups)
print(f"Levene's test for equal variances: stat={stat_lev:.3f}  p={p_lev:.4f}")
print("(p > 0.05 means variances are roughly equal, ANOVA's assumption holds)\n")

# One-way ANOVA across all three variants
f_stat, p_anova = f_oneway(*groups)
print(f"=== One-Way ANOVA ===")
print(f"F = {f_stat:.3f}   p-value = {p_anova:.6f}\n")

# If significant, run Tukey HSD to see which specific pairs differ
if p_anova < 0.05:
    tukey = pairwise_tukeyhsd(endog=conv_df['lead_quality_score'], groups=conv_df['variant'], alpha=0.05)
    print("=== Tukey HSD Post-Hoc (pairwise comparisons) ===")
    print(tukey)
