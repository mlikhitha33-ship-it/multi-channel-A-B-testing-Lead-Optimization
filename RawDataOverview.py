
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('lead_experiment_dataset.csv')
sns.set_style('whitegrid')

fig, axes = plt.subplots(2, 3, figsize=(16, 9))

# 1. Variant split — is it really ~33/33/33?
df['variant'].value_counts().plot(kind='bar', ax=axes[0,0], color='#2E7D6E')
axes[0,0].set_title('Visitors per Variant')

# 2. Channel mix
df['channel'].value_counts().plot(kind='bar', ax=axes[0,1], color='#1F3864')
axes[0,1].set_title('Visitors per Channel')

# 3. Device mix
df['device'].value_counts().plot(kind='bar', ax=axes[0,2], color='#7A5195')
axes[0,2].set_title('Visitors per Device')

# 4. Time on page — full distribution (bounce + convert mixed together)
df['time_spent_sec'].plot(kind='hist', bins=50, ax=axes[1,0], color='#BC5090')
axes[1,0].set_title('Time on Page — All Visitors')

# 5. Lead quality score — converters only (non-converters are all 0, would swamp the plot)
df.loc[df['converted']==1, 'lead_quality_score'].plot(kind='hist', bins=30, ax=axes[1,1], color='#FF6361')
axes[1,1].set_title('Lead Quality Score — Converters Only')

# 6. Ad spend CPC — paid channels only (organic/email are always 0)
df.loc[df['ad_spend_cpc']>0, 'ad_spend_cpc'].plot(kind='hist', bins=30, ax=axes[1,2], color='#FFA600')
axes[1,2].set_title('CPC — Paid Channels Only')

plt.tight_layout()
plt.savefig('eda_overview.png', dpi=120)
plt.show()
