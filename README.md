# CariSurg MedTech Pathways 2026 — Portfolio

**Name:** Vishwesh Pattanaik  
**Programme:** CariSurg MedTech Pathways 2026  
**Hospital:** Mercer General Hospital — Clinical AI & Innovation Unit

---

## Week 0 — Data Exploration and Cleaning

### Assignment 1 — Gender Column Cleaning

The first task involved loading a raw emergency triage dataset from Mercer General Hospital's ED and cleaning the Gender column. The column contained inconsistent string entries such as Male, MALE, Female, FEMALE, 0 and 1. All variations were mapped to integers where male = 1 and female = 0 using a mapping dictionary in pandas.

**Skills used:** Python, pandas, Google Colab, data cleaning

---

### Assignment 2 — DBP Column Cleaning

The second task involved cleaning the Diastolic Blood Pressure (DBP) column. The column was already stored as a float but contained 22 missing values and clinically invalid entries — 8 values below 40 mmHg and 29 values above 120 mmHg. Invalid values were replaced with NaN and all missing values were imputed using the median to avoid skewing the data with extreme values.

**Skills used:** Python, pandas, clinical data validation, median imputation

---

### Assignment 3 — Data Visualisation

The third task involved creating two clinical visualisations from the triage dataset to explore patterns in diastolic blood pressure across ED patients. A histogram was produced to show the distribution of DBP values with clinical reference lines marking the hypotension and hypertension thresholds. A scatter plot was then created to explore whether DBP increases with age in the ED, with the same clinical thresholds marked as reference lines.

**Skills used:** Python, pandas, matplotlib, data visualisation, clinical reference lines

---
### Assignment 4 — Clinical Context: Diastolic Blood Pressure

A plain language explanation of Diastolic Blood Pressure was written covering what it measures, what the normal range looks like and why a triage nurse would care. Normal DBP sits between 60 and 80 mmHg. Below 60 can indicate hypotension or shock and above 90 can indicate hypertension which increases the risk of stroke and heart attack.

**Skills used:** Clinical literacy, technical writing

---

### Assignment 5 — Metrics Not in the Dataset

A short write-up identifying important clinical metrics missing from the dataset. Key metrics identified include SpO2 for blood oxygen saturation, pain score, and the Glasgow Coma Scale. Caribbean specific indicators such as dengue fever markers and recent travel history were also flagged as valuable additions given the regional health context.

**Skills used:** Clinical literacy, critical thinking, Caribbean health context

---

### Assignment 6 — At-Risk Patient Logic

A rule-based algorithm was designed to flag patients as at-risk based on vital sign thresholds aligned with WHO emergency triage guidelines. The algorithm checks pulse, temperature, respiratory rate, systolic blood pressure and DBP. If any single vital sign falls outside the normal range the patient is flagged as at-risk. DBP was included to connect directly to the cleaning and visualisation work in Assignments 2 and 3.

**Skills used:** Python, pseudocode, clinical logic, algorithm design

---

### Assignment 7 — Final Notebook and Career Slide Deck

All tasks from the week were combined into a single documented Jupyter notebook and pushed to this repository. A career slide deck on time management for MedTech students was also submitted covering a two week time audit, a proposed weekly schedule for Weeks 1 to 12, and a triage inspired prioritisation framework.

**Skills used:** Python, Jupyter, GitHub, time management, presentation

---

## Tools and Libraries

- Python 3.10
- pandas
- numpy
- matplotlib
- Google Colab
- GitHub
