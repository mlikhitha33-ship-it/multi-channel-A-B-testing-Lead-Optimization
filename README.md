# Multi-Channel A/B Testing & Lead Optimization

This repository contains an end-to-end A/B testing framework designed to evaluate lead generation performance across multiple marketing channels. It includes the raw experimental dataset, statistical testing scripts, and a post-test analysis pipeline.

---

## 📊 Understanding the Dataset First

Before jumping into code or statistical tests, it helps to understand what the underlying data represents and how it was collected.

The dataset (`lead_experiment_dataset.csv`) contains **45,000 unique visitor sessions** logged during a controlled landing page experiment. The goal of the experiment was to test whether changing the layout of a lead generation form alters conversion rates, dwell time, and downstream lead quality across different acquisition channels.

### Experimental Setup
Visitors were randomly split evenly across three test arms (~15,000 visitors per arm):

* **`Control`**: A standard 6-field static lead form asking for full contact and company details up front.
* **`VarA_ShortForm`**: A stripped-down 3-field static form designed to minimize immediate effort.
* **`VarB_Interactive`**: A multi-step interactive qualification module that breaks questions into bite-sized steps before asking for contact info.

### Data Dictionary

Each row in the dataset records a single visitor session.

| Column Name | Data Type | Analytical Role | What It Measures |
| :--- | :--- | :--- | :--- |
| `lead_id` | Text (ID) | Primary Key | Unique session ID (e.g., `LD-010000`). Used to count sample size ($N$). |
| `timestamp` | Datetime | Time-Series | Arrival time of the visitor. Helps track trends over time. |
| `channel` | Text | Segment | Acquisition source (`Paid Search`, `Paid Social`, `Email Direct`, or `Organic`). |
| `variant` | Text | Test Arm | Form version shown to the visitor (`Control`, `VarA_ShortForm`, or `VarB_Interactive`). |
| `device` | Text | Segment | Hardware device used (`Mobile` or `Desktop`). |
| `time_spent_sec` | Float | Engagement | Total seconds spent on the page before converting or exiting. |
| `converted` | Integer | Primary KPI | Binary conversion flag ($1 = \text{Form Submitted}, 0 = \text{Bounced/Left}$). |
| `lead_quality_score` | Integer | Guardrail KPI | Qualification score ($50\text{--}100$ for converted leads, $0$ for non-converts). |
| `ad_spend_cpc` | Float | Economics | Cost-Per-Click incurred for that specific traffic hit. |

---

## 🎯 The Core Problem & Hypothesis

In lead generation, growth teams face a classic trade-off:

1. **Fewer fields** lower friction and boost overall form submissions--but often increase spam and low-intent leads.
2. **More fields** filter out unqualified users and raise lead quality--but cause steep drop-offs in submission volume.

### Hypothesis
> *If we replace a long static form with a multi-step interactive qualification module, overall conversion rates will increase without dropping downstream lead quality scores below our guardrail threshold (80/100).*

### Metric Structure
* **Primary Metric:** Lead Conversion Rate ($\text{Total Converted Leads} / \text{Total Visitors}$).
* **Secondary Metrics:** Cost-Per-Lead (CPL) and Dwell Time (`time_spent_sec`).
* **Guardrail Metric:** Average Lead Quality Score ($0\text{--}100$). If conversion rates rise but quality falls below 80, the variant fails validation.

---

## 🧪 Statistical Approach & Analysis

To evaluate whether performance differences between variants were real or just random sampling noise, we ran a **Two-Sample Z-Test for Proportions** ($\alpha = 0.05$, $95\%$ Confidence Interval) comparing each treatment variant against the `Control` baseline.

### Key Results Summary

| Variant Group | Visitors ($N$) | Total Leads | Conversion Rate | Lift vs. Control | $p$-value | Significance Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Control (Static Form)** | 15,312 | 643 | **4.20%** | Baseline | 1.0000 | Baseline |
| **Variant A (Short Form)** | 14,838 | 727 | **4.90%** | **+16.6%** | $0.0028$ | Statistically Significant |
| **Variant B (Interactive)** | 14,850 | 861 | **5.80%** | **+38.1%** | $< 0.0001$ | Statistically Significant |

### Primary Takeaways

1. **Variant B is the Clear Winner:** It generated a **+38.1% lift** in conversion rate over Control ($p < 0.0001$) while keeping an average lead quality score of **82.1/100**--passing our guardrail requirement.
2. **Paid Social Impact:** Variant B saw its strongest performance on Paid Social traffic (+44% lift), where mobile users naturally prefer tapping interactive elements over typing into traditional text inputs.
3. **Unit Economics:** The increase in conversion efficiency dropped overall Cost-Per-Lead (CPL) by **$12.40**, significantly boosting return on ad spend across paid channels.

---

## 🛠️ How to Run the Analysis Locally

### 1. Requirements
Ensure you have Python 3.8+ installed along with the required libraries:

```bash
pip install pandas numpy matplotlib seaborn scipy statsmodels
