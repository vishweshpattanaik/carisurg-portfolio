# carisurg-portfolio

Portfolio of work completed during the **CariSurg MedTech Pathways** clinical AI programme, in the role of Clinical AI Engineer trainee within the Clinical AI & Innovation Unit at Mercer General Hospital.

The focus of the early work is **AI-assisted emergency triage** for a Caribbean emergency department setting.

## Who this is for

Clinical reviewers, programme tutors, and colleagues in the Clinical AI & Innovation Unit who want to understand, reproduce, or audit the work. No deep technical background is assumed.

## What is in here

| Folder | Contents |
| --- | --- |
| `notebooks/` | Week 0 exploratory data analysis on emergency triage data: cleaning, basic logic, and visualisation. |
| `docs/` | Week 1 memo and proposal on AI-assisted emergency triage for a Caribbean ED. |
| `data/` | Placeholder for the Week 0 dataset. No real patient data is committed (see `data/README.md`). |

## How to run the notebook

1. Clone the repository:
   ```
   git clone https://github.com/vishwesh-pattanaik/carisurg-portfolio.git
   cd carisurg-portfolio
   ```
2. Create a virtual environment and install dependencies:
   ```
   python -m venv .venv
   source .venv/bin/activate    # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Launch Jupyter and open the notebook in `notebooks/`:
   ```
   jupyter notebook
   ```

The notebook can also be opened directly in Google Colab.

## Data

The dataset is not included in this repository for privacy reasons. The expected file and its location are described in `data/README.md`.

## Licence

Released under the MIT Licence. See `LICENSE`.
