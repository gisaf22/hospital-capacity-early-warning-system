# Hospital Capacity Early Warning System

Predicts whether California's adult ICU system will enter a high-stress state within the next 1–7 days — giving hospital administrators time to act **before** capacity strain arrives.

## Why This Matters

ICU surges catch hospitals off guard. By the time utilization spikes, it's too late to adjust staffing, reroute patients, or reschedule surgeries. A missed surge (false negative) is far costlier than a false alarm — it means delayed care, overwhelmed staff, and worse patient outcomes. That makes **recall** the priority metric: the system must catch stress episodes even at the cost of occasional over-alerting. This project uses publicly available hospital data to build a **proactive** alert system that flags stress **days before** it hits.

## What It Does

- Pulls daily California hospital reports from the [HHS Protect Public Data Hub](https://healthdata.gov/Hospital/COVID-19-Reported-Patient-Impact-and-Hospital-Capa/g62h-syeh) via the Socrata Open Data API (SODA)
- Defines "high stress" as ICU utilization exceeding its 85th-percentile value within the next 7 days
- Trains logistic regression models on ICU utilization trends and upstream respiratory demand signals (influenza/COVID admissions and hospitalizations)
- Detects **all 3 stress episodes** in the test period with **4–5 days of advance warning**

## Results

| Metric | Heuristic Baseline | Logistic v1 (ICU) | Logistic v2 (ICU + Respiratory) |
|---|---|---|---|
| F1 Score | 0.564 | 0.804 | 0.812 |
| Avg Lead Time | 3.3 days | 4.3 days | 5.0 days |
| Episodes Detected | 2 / 3 | 3 / 3 | 3 / 3 |

> Evaluated on unseen test data with a locked threshold and strict chronological split — no data leakage.

## Project Structure

```
notebooks/
  hhs_data_wrangling.ipynb               # Data acquisition & cleaning
  feature_eng_modeling.ipynb              # Exploratory feature engineering & modeling
  icu_stress_early_warning_modeling.ipynb  # Controlled experimental framework
reports/
  final_report.md                        # Written report
  Capstone3_Presentation.pptx            # Slide deck
src/
  data_reader/get_hhs_data.py            # HHS Protect API client
  schema/handle_schema.py                # Column selection & schema handling
```

## Quick Start

```bash
git clone https://github.com/<your-username>/hospital-capacity-early-warning-system.git
cd hospital-capacity-early-warning-system
python -m venv .venv && source .venv/bin/activate
pip install pandas numpy matplotlib seaborn scikit-learn pyarrow requests
```

Run the notebooks in order: data wrangling → feature engineering → controlled experiment.

## Tech Stack

Python · pandas · scikit-learn · matplotlib · seaborn · Socrata Open Data API (SODA)

## Author

Springboard Data Science Career Track — Capstone Project
