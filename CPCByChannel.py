
import pandas as pd
from scipy.stats import ttest_ind, levene, mannwhitneyu

df = pd.read_csv('lead_experiment_dataset.csv')

# CPC only exists for paid channels, Email Direct and Organic are always 0
paid = df[df['ad_spend_cpc'] > 0].copy()

summary_cpc = paid.groupby('channel')['ad_spend_cpc'].agg(['count', 'mean', 'std'])
print("=== CPC by Channel ===")
print(summary_cpc, "\n")

search = paid.loc[paid['channel'] == 'Paid Search', 'ad_spend_cpc']
social = paid.loc[paid['channel'] == 'Paid Social', 'ad_spend_cpc']

# Check equal variance assumption before trusting standard t-test
stat_lev, p_lev = levene(search, social)
print(f"Levene's test for equal variances: stat={stat_lev:.3f}  p={p_lev:.4f}")
print("(p < 0.05 means variances differ, use Welch's t-test instead of Student's)\n")

# Standard independent t-test, Welch correction applied if variances are unequal
equal_var = p_lev >= 0.05
t_stat, p_val = ttest_ind(search, social, equal_var=equal_var)
test_used = "Student's t-test" if equal_var else "Welch's t-test"
print(f"=== {test_used} ===")
print(f"t = {t_stat:.3f}   p-value = {p_val:.6f}")
print(f"Paid Search mean: ${search.mean():.2f}   Paid Social mean: ${social.mean():.2f}")
print(f"Difference: ${search.mean() - social.mean():.2f}\n")

# Non-parametric fallback, listed as an option in the plan table
u_stat, p_mw = mannwhitneyu(search, social, alternative='two-sided')
print("=== Mann-Whitney U (non-parametric check) ===")
print(f"U = {u_stat:.1f}   p-value = {p_mw:.6f}")
