
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('lead_experiment_dataset.csv')
sns.set_style('whitegrid')

# Matches the palette used in the executive dashboard, so a variant's color
# means the same thing in every chart across the repo
VARIANT_PALETTE = {
    'Control': '#9AA1AB',
    'VarA_ShortForm': '#C08A2E',
    'VarB_Interactive': '#2F6F5E',
}
VARIANT_ORDER = ['Control', 'VarA_ShortForm', 'VarB_Interactive']

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

sns.boxplot(
    data=df[df['converted']==1],
    x='variant', y='time_spent_sec', order=VARIANT_ORDER,
    ax=axes[0], hue='variant', palette=VARIANT_PALETTE, legend=False
)
axes[0].set_title('Time on Page — Converters Only, by Variant')
axes[0].set_xlabel('')
axes[0].tick_params(axis='x', rotation=20)

sns.boxplot(
    data=df[df['converted']==1],
    x='variant', y='lead_quality_score', order=VARIANT_ORDER,
    ax=axes[1], hue='variant', palette=VARIANT_PALETTE, legend=False
)
axes[1].set_title('Lead Quality Score — Converters Only, by Variant')
axes[1].set_xlabel('')
axes[1].tick_params(axis='x', rotation=20)

sns.histplot(
    data=df[df['ad_spend_cpc']>0],
    x='ad_spend_cpc', hue='channel',
    element='step', bins=30, ax=axes[2]
)
axes[2].set_title('CPC — Paid Channels Only, by Channel')

plt.tight_layout()
plt.savefig('eda_updated.png', dpi=120)
plt.show()
