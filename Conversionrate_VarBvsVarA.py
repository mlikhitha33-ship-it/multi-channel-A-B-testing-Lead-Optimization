from statsmodels.stats.proportion import proportions_ztest, proportion_confint

n_a = summary.loc['VarA_ShortForm', 'visitors']
conv_a = summary.loc['VarA_ShortForm', 'conversions']
n_b = summary.loc['VarB_Interactive', 'visitors']
conv_b = summary.loc['VarB_Interactive', 'conversions']

# One-sided: testing whether VarB beats VarA specifically
z, pval = proportions_ztest([conv_b, conv_a], [n_b, n_a], alternative='larger')

rate_a = conv_a / n_a * 100
rate_b = conv_b / n_b * 100
lift_abs = rate_b - rate_a
lift_rel = lift_abs / rate_a * 100

print("=== VarB_Interactive vs VarA_ShortForm (one-sided: does B beat A?) ===")
print(f"VarA rate: {rate_a:.2f}%   VarB rate: {rate_b:.2f}%")
print(f"z = {z:.3f}   p-value = {pval:.6f}")
print(f"lift_abs = {lift_abs:.2f}pp   lift_rel = {lift_rel:.1f}%")
