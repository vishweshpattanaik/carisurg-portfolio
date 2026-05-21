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

## Tools and Libraries
- Python 3.10
- pandas
- numpy
- matplotlib
- Google Colab
- GitHub
