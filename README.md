# SmartCare Health Monitoring  Power BI Analytics Dashboard
---
##  Table of Contents
1. [Project Overview](#-project-overview)
2. [Business Problem & Objectives](#-business-problem--objectives)
3. [Data Model](#-data-model)
4. [DAX Measures](#-dax-measures)
5. [Power BI Report Pages](#-power-bi-report-pages)
6. [Custom & Embedded Visuals](#-custom--embedded-visuals)
7. [Interactivity & UX Design](#-interactivity--ux-design)
8. [Key Insights](#-key-insights)
9. [Repository Structure](#-repository-structure)
---

## Project Overview

SmartCare monitors 50 patients via smartwatch telemetry  heart rate, step count, sleep, stress index, and fall alerts  and needs a way to turn raw daily readings into a **clinically actionable risk view** a care coordinator can actually use.

This project is a **5-page Power BI report** built on a feature set (risk scoring, clustering, health categorization), designed to answer: *which patients need intervention first, and why?*

While the underlying data pipeline (cleaning, feature engineering, risk scoring, clustering) is in Python (see [`Code/`](Code)), **this README focuses on the Power BI layer**  the data model, DAX measures, custom visuals, and interactive report design that turn that pipeline's output into a usable decision-support tool.

---

## Business Problem & Objectives

**Business question:** 
*Q.1 Which patients are at highest risk of a health decline or fall event?*
*Q.2 What specific intervention should a care team prioritize for each?*

**Target audience:** Clinical/care-coordination staff triaging patient risk, and a mobile-using care team that needs the same view on a phone.

| # | Objective | Delivered via |
|---|-----------|----------------|
| 1 | Give a single-glance fleet health status | Executive Overview page  KPI cards + distribution charts |
| 2 | Rank and surface the highest-risk patients by name | Risk Assessment page  scatter quadrant + ranked table |
| 3 | Show *why*  which health metrics actually drive risk | Health Matrix Deep Dive  correlation heatmap, box plots |
| 4 | Group patients into actionable intervention cohorts | Predictive Insights  cluster profiling + intervention lookup table |
| 5 | Make the same overview usable on a phone in the field | Mobile Executive View  phone-layout page |

---

## Data Model

The report is built on a small but genuine **relational model**, not a single flat table:

| Table | Role |
|---|---|
| `smartcare_cleaned_data` | Main fact table  one row per patient, 21 columns (demographics, vitals, engineered features, `Risk_Score`, `RiskCategory`, `Health Cluster`) |
| `InterventionTable` | Lookup table  maps `Cluster` → `Cluster_Name` → `Priority` → `Primary_Need`, joined into the model to translate a numeric cluster ID into a care-team-readable action |

---

## DAX Measures
<img width="1361" height="467" alt="image" src="https://github.com/user-attachments/assets/4e1cba31-3b6f-4040-ba47-3244f28539b1" />

<img width="1365" height="352" alt="image" src="https://github.com/user-attachments/assets/d0e67bc0-d4c0-44ad-bcd3-b4ac85b6b4dd" />

<img width="1355" height="352" alt="image" src="https://github.com/user-attachments/assets/51877806-fd18-479b-8cfa-7f1ff8f9701d" />

<img width="1370" height="510" alt="image" src="https://github.com/user-attachments/assets/54e664c8-be1b-4e42-b7d8-d13fb3070151" />

<img width="1350" height="342" alt="image" src="https://github.com/user-attachments/assets/998b66d3-1039-4c16-a2fc-060a44075e36" />


## Power BI Report Pages

**1. Executive Overview**
Fleet-level KPI cards (Total Patients, Avg Health Score, High/Critical Risk %, Fall Alert %) plus health score, risk category, age, activity level, and gender distributions  with a full slicer panel (Age Group, Gender, Risk Category, Activity Level, Weekly Health Score range, Age range) driving every visual on the page.

<img width="1384" height="800" alt="1_executive_overview" src="https://github.com/user-attachments/assets/f2006a7e-879c-4699-aa01-09d550203564" />

**2. Risk Assessment**
A **quadrant scatter plot** (Age × Risk Score, with a "High Risk Threshold" reference line at 50 and an "Age 70" reference line) isolates patients who are both older *and* high-risk  the two-line annotation turns a generic scatter into an actual clinical decision boundary. Paired with a **Top 10 Highest Risk Patients** ranked table (urgency-flagged) and a full conditionally-formatted patient list.

<img width="1384" height="800" alt="2_risk_assessment" src="https://github.com/user-attachments/assets/09051a6e-b1c6-4f2d-abc9-a9f7de7b8e35" />

**3. Health Matrix Deep Dive**
A correlation heatmap across 11 health metrics (rendered via an **embedded Python visual**  see below), box-and-whisker plots of health score by age group and steps by activity level (via an AppSource custom visual), and scatter/bar breakdowns of sleep, steps, and stress.

<img width="1384" height="800" alt="3_health_matrix_deep_dive" src="https://github.com/user-attachments/assets/c338fad7-09f5-43ec-9e4b-b0b9df84443f" />

**4. Predictive Insights**
Drills into the 4 patient clusters produced by the Python clustering model (`Healthy & Active`, `Moderate Risk – General Monitoring`, `High Risk – Needs Intervention`, `Moderate Risk – Stress Management`), with a **heat-mapped cluster-profile matrix** (color-scaled by metric, powered by the `InterventionTable` relationship) and a **Back navigation button** for bookmark-style drill-through UX.

<img width="1384" height="800" alt="4_predictive_insights" src="https://github.com/user-attachments/assets/675d8cd5-c618-41c6-8e89-3569f8a596fd" />

**5. Mobile Executive View**
A dedicated phone-layout page  the KPI cards and distribution charts re-flowed for a vertical mobile viewport, so the same fleet overview works for a care coordinator checking the dashboard on a phone.

<img width="455" height="747" alt="Screenshot 2026-08-26 070058" src="https://github.com/user-attachments/assets/97abc529-4136-4b71-b45f-d7091996fd59" />

*(Full 5-page export: [`PowerBI_Output/PowerBI_Output/MBI806_Assessment_2_PowerBI_Dashboard.pdf`](PowerBI_Output/PowerBI_Output/MBI806_Assessment_2_PowerBI_Dashboard.pdf))*

---

## Custom & Embedded Visuals
Beyond Power BI's native visual set, the report installs and uses **three AppSource custom visuals**, plus one **embedded Python script visual**  a meaningfully more advanced toolkit than a default-visuals-only report:

| Visual | Type | Used for |
|---|---|---|
| **Box and Whisker Chart** | AppSource custom visual | Health score by age group, steps by activity level  shows median, quartiles, and outliers that a bar chart can't |
| **Inforiver Filter** | AppSource advanced slicer | Richer multi-select filtering than the native slicer, used alongside the standard filter panel |
| **Table Heat Map** | AppSource custom visual | The cluster-profile matrix  conditionally color-scales every metric column independently so patterns jump out at a glance |
| **Python visual (embedded)** | Native Power BI + Python | Renders a `seaborn` correlation heatmap *inside* the report canvas  real analysis code executing at report-render time, not a static image import |

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = dataset

numeric_cols = ['Age', 'DailyStepCount', 'HeartRate_Min', 'HeartRate_Max',
                'HeartRate_Avg', 'SleepDuration_Hours', 'SleepQualityScore',
                'StressIndex', 'CalorieBurn', 'WeeklyHealthScore', 'Risk_Score']

correlation_matrix = df[numeric_cols].corr()

plt.figure(figsize=(16, 12))
sns.heatmap(correlation_matrix,
            annot=True, fmt='.2f', cmap='RdYlGn', center=0,
            square=True, linewidths=1.5, linecolor='white',
            cbar_kws={"shrink": 0.8, "label": "Correlation Coefficient"},
            vmin=-1, vmax=1)

plt.title('Correlation Heatmap - Health Metrics', fontsize=18, fontweight='bold', pad=25)
plt.xticks(rotation=45, ha='right', fontsize=11)
plt.yticks(rotation=0, fontsize=11)
plt.tight_layout()
plt.show()
```

Power BI feeds this script a live `dataset` dataframe bound to 11 report columns and re-renders the figure whenever a slicer changes the underlying filter context  combining a Python data-science workflow with Power BI's native interactivity.

---

## Interactivity & UX Design

- **Slicers** across the report (Age Group, Gender  button-style, Risk Category, Activity Level, a Weekly Health Score range slider, and an Age range slider), all cross-filtering every visual on their page
- **Cross-filtering enabled on every visual** (`drillFilterOtherVisuals`)  clicking any chart segment filters the rest of the page
- **Bookmark-style "Back" navigation button** on the Predictive Insights page, enabling a drill-down → detail → back UX pattern rather than a flat set of tabs
- **Dedicated mobile layout** (Mobile Executive View)  a genuinely separate phone-optimized page layout
- **Reference lines on the risk scatter plot** ("High Risk Threshold" at 50, "Age 70" marker)  turning a plain scatter chart into an annotated decision-support visual
- **Conditional formatting** on the patient table (red-highlighted `FallAlerts`, color-scaled `Risk_Score`) so risk is visible without reading every cell

---

## Key Insights

| # | Insight (from the dashboard) |
|---|---|
| 1 | **52% of patients (26 of 50) fall into High or Critical risk**  this is not a long-tail problem, it's roughly half the monitored population |
| 2 | The risk-quadrant view shows risk is **not simply age-driven**  several patients under 60 register above the High Risk Threshold, while a cluster of patients over 70 sit in the Low Risk zone, meaning age alone is a poor triage filter |
| 3 | The correlation heatmap shows **Risk Score correlates most strongly with Stress Index and inversely with Sleep Duration/Quality**  sleep and stress interventions are more actionable levers than trying to change age or activity level |
| 4 | Patient segmentation resolves into 4 clusters, with **"High Risk – Needs Intervention" the single largest cluster**  larger than the "Healthy & Active" group  reinforcing that this population skews toward needing active management, not passive monitoring |
| 5 | Only **10% of patients have triggered a fall alert**, but this group overlaps heavily with the Critical Risk category  fall alerts function as a strong leading indicator, not a noisy one |

---

## Repository Structure

```
SmartCare_Health_Monitoring_with_Smartwatches/
│
├── Code/
│   ├── data_preprocessing_cleaning.py      # Raw smartwatch data → cleaned dataset
│   ├── exploratory_data_analysis.py        # EDA feeding the Power BI data model
│   ├── predictive_modeling.py              # Risk scoring + patient clustering
│   └── advanced_visualization.py           # Python-side chart generation (mirrors the in-BI Python visual)
│
├── Data/
│   ├── smartwatch_health_data.csv          # Raw input
│   ├── smartcare_cleaned_data.csv          # Cleaned, feature-engineered dataset (feeds Power BI)
│   └── smartcare_with_predictions.csv      # + risk score, cluster assignment
│
├── PowerBI_Output/PowerBI_Output/
│   ├── MBI806_Assessment_2.pbix            # Full Power BI report file
│   ├── MBI806_Assessment_2_Template.pbit   # Reusable Power BI template
│   └── MBI806_Assessment_2_PowerBI_Dashboard.pdf   # All 5 pages, exported
│
├── Output/                                 # Python-generated charts (EDA, clustering, model performance)
├── Visual_Console_Output/                  # Full console/run logs for each Python script
├── code_etl_visual.ipynb                   # Notebook version of the ETL/analysis pipeline
├── LICENSE
└── README.md
```

---

## How to Open This Project

**1. Clone the repository**
```bash
git clone https://github.com/UmrikarS/SmartCare_Health_Monitoring_with_Smartwatches.git
cd SmartCare_Health_Monitoring_with_Smartwatches
```

**2. Open the Power BI report**

Open [`PowerBI_Output/PowerBI_Output/MBI806_Assessment_2.pbix`](PowerBI_Output/PowerBI_Output/MBI806_Assessment_2.pbix) directly in **Power BI Desktop**. On first open, Power BI will prompt to download the 3 AppSource custom visuals (Box and Whisker Chart, Inforiver Filter, Table Heat Map) if they aren't already installed  accept this to see the report exactly as designed.

> **Python visual note:** to see the embedded correlation heatmap render live (rather than its cached image), Power BI Desktop needs a local Python installation with `pandas`, `numpy`, `matplotlib`, and `seaborn` registered under **File → Options → Python scripting**.

**3. (Optional) Regenerate the underlying data**
```bash
pip install pandas numpy scikit-learn matplotlib seaborn openpyxl
python Code/data_preprocessing_cleaning.py
python Code/exploratory_data_analysis.py
python Code/predictive_modeling.py
```
This regenerates `Data/smartcare_cleaned_data.csv`, which the `.pbix` can be pointed at to refresh with new data.

**4. No Power BI Desktop available?**

View the static export: [`MBI806_Assessment_2_PowerBI_Dashboard.pdf`](PowerBI_Output/PowerBI_Output/MBI806_Assessment_2_PowerBI_Dashboard.pdf)

---
