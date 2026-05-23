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

## Tools and Libraries

- Python 3.10
- pandas
- numpy
- matplotlib
- Google Colab
- GitHub
