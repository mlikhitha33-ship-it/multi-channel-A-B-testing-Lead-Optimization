# Multi-Channel A/B Testing & Lead Optimization

This repository contains an end-to-end experimentation framework, raw dataset, and post-test analytics pipeline designed to evaluate lead generation performance across paid and organic acquisition channels.

---

## 📋 Campaign Background & Execution Strategy

To understand the dataset, we first need to establish the real-world campaign setup, user journey, and ad mechanics behind the experiment.

* **The Business Offer:** An enterprise growth consultation and audit request form hosted on a dedicated landing page.
* **The Campaign Window:** A 30-day live paid media campaign run from June 1, 2026, to June 30, 2026.
* **Ad Mechanics & Timing:** Ads ran continuously across Google Search, LinkedIn/Meta Social feeds, and dedicated email sends. When a user clicked an ad or email link, they landed on the campaign page where the lead form was displayed immediately above the fold in the main hero section.

---

## 📊 Acquisition Channels & Form Tolerances

Marketing traffic is not homogeneous. A user actively seeking a solution responds differently to friction than a user casually scrolling a social feed. 

In this campaign, 45,000 unique visitor sessions were logged across four acquisition channels:

* **Paid Search (40% of traffic):** High-intent visitors arriving from Google Search ads. These users were actively looking for a solution and demonstrated tolerance for a **moderate form length** (defined as 6 standard fields capturing both contact details and initial business context), provided every field felt directly relevant to their search query.
* **Paid Social (30% of traffic):** Mobile-heavy visitors arriving from LinkedIn and Meta feed ads. Because social ads interrupt active scrolling, these users exhibited low tolerance for traditional forms and responded best to quick, tap-based interactions.
* **Email Direct (15% of traffic):** Warm leads arriving from existing subscriber newsletters. These users already possessed brand familiarity, yielding stable conversion rates across all form layouts.
* **Organic (15% of traffic):** Unpaid search and direct referral visitors, serving as a baseline group uninfluenced by paid ad positioning.

---

## 🧪 Experimental Setup & Form Variants

Visitors were routed equally across three experimental variants (~15,000 sessions per group) using a split-URL experiment router:

* **`Control` (Moderate Form Length - 6 Fields):** The standard industry baseline asking for Full Name, Work Email, Phone Number, Company Name, Team Size, and Primary Business Goal.
* **`VarA_ShortForm` (Short Form Length - 3 Fields):** A low-friction layout requesting only Full Name, Work Email, and Company Name.
* **`VarB_Interactive` (Multi-Step Diagnostic Flow):** A four-screen interactive widget asking 3 tap-to-select diagnostic questions (e.g., "What is your main growth bottleneck?") before prompting for a final contact screen (Name, Email, and Phone Number).

---

## 📁 Data Dictionary (`lead_experiment_dataset.csv`)

Each row in the dataset represents a single visitor session.

| Column Name | Data Type | Analytical Role | Description |
| :--- | :--- | :--- | :--- |
| `lead_id` | Text (ID) | Primary Key | Unique session identifier (e.g., `LD-010000`). Used to calculate sample size ($N$). |
| `timestamp` | Datetime | Time-Series | Visitor arrival timestamp across the 30-day test window. |
| `channel` | Text | Segment | Acquisition source (`Paid Search`, `Paid Social`, `Email Direct`, or `Organic`). |
| `variant` | Text | Test Arm | Assigned landing page layout (`Control`, `VarA_ShortForm`, or `VarB_Interactive`). |
| `device` | Text | Segment | Visitor hardware category (`Mobile` or `Desktop`). |
| `time_spent_sec` | Float | Engagement | Total landing page dwell time in seconds before converting or exiting. |
| `converted` | Integer | Primary KPI | Binary indicator ($1 = \text{Lead Submitted}, 0 = \text{Exited Without Submitting}$). |
| `lead_quality_score` | Integer | Guardrail KPI | Downstream qualification score ($50\text{--}100$ for converted leads, $0$ for non-converts). |
| `ad_spend_cpc` | Float | Economics | Cost-Per-Click incurred for that specific visitor click. |

---

## 🎯 Strategic Hypothesis & Metric Structure

### The Core Trade-Off
Reducing form fields lowers submission friction and increases lead volume, but often introduces spam or unqualified leads. Increasing form fields improves lead qualification, but causes steep drop-offs in total volume.

### Hypothesis
> *Replacing a standard 6-field static form with a multi-step interactive qualification module will increase overall lead conversion rates without dropping average lead quality scores below our guardrail threshold of 80/100.*

### Metric Hierarchy
1. **Primary KPI:** Lead Conversion Rate ($\text{Total Converted Leads} / \text{Total Unique Visitors}$).
2. **Secondary KPIs:** Cost-Per-Lead (CPL) and Dwell Time (`time_spent_sec`).
3. **Guardrail KPI:** Average Lead Quality Score ($0\text{--}100$). A variant must maintain an average score of $\ge 80/100$ among converted leads to be considered viable.

---

## 📈 Statistical Findings & Performance Summary

We evaluated the test results using a **Two-Sample Z-Test for Proportions** ($\alpha = 0.05$, $95\%$ Confidence Interval) comparing each treatment variant against the `Control` baseline.

| Test Group | Visitors ($N$) | Total Leads | Conversion Rate | Lift vs. Control | $p$-value | Significance Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Control (6-Field Static)** | 15,312 | 643 | **4.20%** | Baseline | 1.0000 | Baseline |
| **Variant A (3-Field Short)** | 14,838 | 727 | **4.90%** | **+16.6%** | $0.0028$ | Statistically Significant |
| **Variant B (Interactive)** | 14,850 | 861 | **5.80%** | **+38.1%** | $< 0.0001$ | Statistically Significant |

### Strategic Key Takeaways

1. **Variant B Achieved Maximum Efficiency:** It produced a **+38.1% conversion rate lift** over Control ($p < 0.0001$) while keeping an average lead quality score of **82.1/100**, successfully passing our quality guardrail.
2. **Channel-Specific Resonance:** Variant B recorded its highest relative lift on **Paid Social (+44%)**, proving that mobile feed traffic responds better to progressive disclosure than to traditional form fields.
3. **Financial Outcome:** Higher conversion efficiency reduced overall Cost-Per-Lead (CPL) by **$12.40**, significantly boosting return on ad spend across paid search and paid social campaigns.

---

## 🛠️ How to Run the Analysis Locally

### 1. Requirements
Install the required Python packages:

```bash
pip install pandas numpy matplotlib seaborn scipy statsmodels
