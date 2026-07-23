import pandas as pd
from scipy.stats import chi2_contingency
from statsmodels.stats.proportion import proportions_ztest, proportion_confint

df = pd.read_csv('lead_experiment_dataset.csv')

# Omnibus test: is there a difference among all 3 arms at all?
ct = pd.crosstab(df['variant'], df['converted'])
chi2, p_omnibus, dof, _ = chi2_contingency(ct)
print("=== Omnibus Chi-Square (all 3 variants) ===")
print(ct)
print(f"chi2 = {chi2:.3f}, p-value = {p_omnibus:.6f}\n")

# Summary per variant
summary = df.groupby('variant')['converted'].agg(['count', 'sum', 'mean'])
summary.columns = ['visitors', 'conversions', 'conversion_rate']
print("=== Conversion Rate by Variant ===")
print(summary, "\n")

# Pairwise one-sided z-tests vs Control (testing for improvement, not just difference)
control_n = summary.loc['Control', 'visitors']
control_conv = summary.loc['Control', 'conversions']

print("=== Pairwise vs Control (one-sided: testing for lift) ===")
for v in ['VarA_ShortForm', 'VarB_Interactive']:
    n = summary.loc[v, 'visitors']
    conv = summary.loc[v, 'conversions']
    z, pval = proportions_ztest([conv, control_conv], [n, control_n], alternative='larger')
    ci_low, ci_high = proportion_confint(conv, n, method='wilson')
    lift_abs = (conv/n - control_conv/control_n) * 100
    lift_rel = lift_abs / (control_conv/control_n*100) * 100
    print(f"{v}: rate={conv/n*100:.2f}%  95% CI=[{ci_low*100:.2f}, {ci_high*100:.2f}]  "
          f"z={z:.3f}  p={pval:.6f}  lift_abs={lift_abs:.2f}pp  lift_rel={lift_rel:.1f}%")
