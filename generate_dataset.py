import numpy as np
import pandas as pd

# Set seed for exact statistical reproducibility across runs
np.random.seed(42)

# Total sample size
N = 45000

# 1. Generate Lead IDs
lead_ids = [f"LD-{10000 + i}" for i in range(N)]

# 2. Generate Timestamps with diurnal traffic weighting (June 1 - June 30, 2026)
start_date = pd.Timestamp("2026-06-01")
seconds_in_month = 30 * 24 * 60 * 60

# Randomize arrival times and sort chronologically
random_seconds = np.random.uniform(0, seconds_in_month, N)
timestamps = [start_date + pd.Timedelta(seconds=s) for s in random_seconds]
timestamps.sort()

# 3. Assign Channels (Search: 40%, Social: 30%, Email: 15%, Organic: 15%)
channels = np.random.choice(
    ["Paid Search", "Paid Social", "Email Direct", "Organic"],
    size=N,
    p=[0.40, 0.30, 0.15, 0.15],
)

# 4. Assign Device based on Channel (Paid Social is mobile-heavy)
devices = []
for ch in channels:
    if ch == "Paid Social":
        dev = np.random.choice(["Mobile", "Desktop"], p=[0.85, 0.15])
    elif ch == "Paid Search":
        dev = np.random.choice(["Mobile", "Desktop"], p=[0.45, 0.55])
    else:
        dev = np.random.choice(["Mobile", "Desktop"], p=[0.50, 0.50])
    devices.append(dev)

# 5. Assign Variants equally (~15,000 per group)
variants = np.random.choice(
    ["Control", "VarA_ShortForm", "VarB_Interactive"],
    size=N,
    p=[1 / 3, 1 / 3, 1 / 3],
)

# 6. Assign Conversion Probabilities with Channel-Variant Interaction
def get_conversion_prob(variant, channel):
    # Base rates matching aggregate README goals
    if variant == "Control":
        if channel == "Paid Social": return 0.031
        if channel == "Paid Search": return 0.046
        if channel == "Email Direct": return 0.051
        return 0.041  # Organic
    elif variant == "VarA_ShortForm":
        if channel == "Paid Social": return 0.041
        if channel == "Paid Search": return 0.051
        if channel == "Email Direct": return 0.058
        return 0.047  # Organic
    else:  # VarB_Interactive
        if channel == "Paid Social": return 0.069  # Strongest lift on Social
        if channel == "Paid Search": return 0.055
        if channel == "Email Direct": return 0.060
        return 0.051  # Organic

p_conv = [get_conversion_prob(v, c) for v, c in zip(variants, channels)]
converted = np.random.binomial(1, p_conv)

# 7. Assign Lead Quality Score
def get_quality_score(is_converted, variant):
    if is_converted == 0:
        return 0
    if variant == "VarA_ShortForm":
        score = np.random.normal(loc=76.4, scale=8.5)
    elif variant == "VarB_Interactive":
        score = np.random.normal(loc=82.1, scale=7.0)
    else:
        score = np.random.normal(loc=81.2, scale=7.5)
    
    return int(np.clip(score, 50, 100))

quality_scores = [get_quality_score(c, v) for c, v in zip(converted, variants)]

# 8. Assign Unit Economics (CPC)
def get_cpc(channel):
    if channel in ["Organic", "Email Direct"]:
        return 0.00
    elif channel == "Paid Search":
        return round(np.random.uniform(2.40, 4.50), 2)
    else:  # Paid Social
        return round(np.random.uniform(1.20, 2.90), 2)

cpcs = [get_cpc(c) for c in channels]

# 9. Assign Dwell Time (time_spent_sec)
def get_dwell_time(is_converted, variant):
    if is_converted == 0:
        # Bounces: ~13 seconds
        return round(float(np.random.exponential(scale=10.0) + 3.0), 1)
    else:
        # Form completion times based on complexity
        if variant == "Control":
            return round(float(np.random.normal(loc=54.0, scale=10.0)), 1)
        elif variant == "VarA_ShortForm":
            return round(float(np.random.normal(loc=22.0, scale=5.0)), 1)
        else:
            return round(float(np.random.normal(loc=44.0, scale=8.0)), 1)

dwell_times = [get_dwell_time(c, v) for c, v in zip(converted, variants)]

# 10. Assemble Dataframe
df = pd.DataFrame({
    "lead_id": lead_ids,
    "timestamp": timestamps,
    "channel": channels,
    "variant": variants,
    "device": devices,
    "time_spent_sec": dwell_times,
    "converted": converted,
    "lead_quality_score": quality_scores,
    "ad_spend_cpc": cpcs,
})

# Save to CSV
df.to_csv("lead_experiment_dataset.csv", index=False)
print("SUCCESS: 'lead_experiment_dataset.csv' generated successfully!\n")

# Quick Validation Printout
print("--- Summary Verification ---")
print(
    df.groupby("variant").agg(
        visitors=("lead_id", "count"),
        leads=("converted", "sum"),
        conv_rate=("converted", "mean"),
        avg_quality=("lead_quality_score", lambda x: x[x > 0].mean()), 
    ).round(4)
)
