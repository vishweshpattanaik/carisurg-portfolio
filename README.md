# CariSurg MedTech Pathways 2026 — Portfolio
**Name:** Vishwesh Pattanaik  
**Programme:** CariSurg MedTech Pathways 2026  
**Hospital:** Mercer General Hospital — Clinical AI & Innovation Unit

**Project:** An AI-assisted triage tool for middle-acuity patients in a Caribbean emergency department. The middle band (ESI 3) is the biggest group coming through the door and the one triage sorts worst. The aim is to flag the patients in that band who need moving up, validate it on local data, and shadow-test it against the nurses before it touches a single decision.

---

## Quickstart

The dataset is not included in this repository (it is git-ignored for size and sensitivity). Supply your own copy, then:

```bash
# 1. clone and enter
git clone https://github.com/vishweshpattanaik/carisurg-portfolio.git
cd carisurg-portfolio

# 2. environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. place the dataset here (name must match config.yaml):
#    data/yaleemmlc_admissionprediction_triage.csv
#    if your file is named differently, change data.path in config.yaml

# 4. train the pinned model
python scripts/train.py --config config.yaml
```

This prints accuracy, macro F1, ESI-1 recall and under-triage rate, and writes the model to `artifacts/model.joblib` and metrics to `artifacts/metrics.json`.

```bash
# reproduce the full model comparison table
python scripts/compare_models.py --config config.yaml

# run the tests
pytest tests/
```

If the data is missing or has the wrong columns, the pipeline stops with a clear message rather than failing silently. Everything that can be changed (seed, split, features, model) lives in `config.yaml`, not in the code.

---

## Week 0 — Data Exploration and Cleaning

Cleaned a raw emergency triage dataset from Mercer General's ED. The Gender column held inconsistent entries (Male, MALE, Female, FEMALE, 0, 1) and was mapped to integers. The Diastolic Blood Pressure column had 22 missing values and clinically invalid entries, 8 below 40 mmHg and 29 above 120 mmHg. Invalid values were replaced with NaN and imputed with the median to avoid skewing on the extremes. Two clinical visualisations followed: a DBP histogram with hypotension and hypertension reference lines, and a DBP against age scatter plot. A plain language write-up on what DBP means and why a triage nurse cares. A list of metrics missing from the dataset, including SpO2, pain score, Glasgow Coma Scale, and Caribbean specific indicators like dengue markers. Finally a rule-based algorithm that flags a patient as at-risk if any vital sign falls outside the WHO normal range.

**Skills used:** Python, pandas, matplotlib, Google Colab, data cleaning, clinical literacy, algorithm design

---

## Week 1 — Preliminary Proposal

Wrote the first proposal. Problem statement, literature review, identified gaps, and a four-phase solution. The two gaps that drive the whole project: every AI triage model in the literature is validated on a single well-resourced site, and almost none are tested prospectively at the bedside. Neither has been done in a Caribbean ED.

**Skills used:** Research literacy, technical writing, gap analysis

---

## Week 2 — Project Setup and Documentation

Set up this repository properly. README, LICENSE, .gitignore, requirements.txt, and a branch to pull request to merge cycle. Built a Zotero library and regenerated the proposal so no citation is typed by hand.

**Skills used:** Git, GitHub, Zotero, technical documentation

---

## Week 3 — Workflow and Systems Thinking

Mapped the current ED triage process from door to disposition in Mermaid, and marked five points where an AI tool could plausibly sit. Points 2 and 3, flagging likely up-triage at assessment and re-scoring middle-band patients while they wait, are the core of this project. Named three workflow constraints any design has to respect: vitals go on paper before the EHR, triage runs under constant interruption, and vitals capture is often incomplete. Mapped five clinical stakeholders and what each actually cares about.

**Skills used:** Mermaid, systems thinking, stakeholder analysis

---

## Week 4 — Ethics, Safety and Risk

Built a 12-risk register across AI-technical, operational, ethical and equity categories, each with a likelihood, an impact, a mitigation, and a signal that tells you the mitigation is working. Root-caused a real AI harm case: the Epic Sepsis Model, deployed to hundreds of US hospitals, which on independent validation scored an AUC of 0.63, missed two thirds of sepsis cases, and ran at 12% precision until staff learned to ignore it. Four root causes, and every one of them maps onto a risk in the register.

**Skills used:** Risk analysis, responsible AI, critical appraisal

---

## Week 5 — Data Exploration

Profiled the Yale ED dataset: 55,121 patients, 226 columns, 200 of them one-hot chief-complaint flags. ESI 3 is 49% of arrivals, which is the project premise confirmed in the data. Not one missing cell anywhere, which sounds good and is not. This is the processed release, so the vitals were imputed and the complaints encoded before it reached me, and Mercer's own extract will not look like this. Wrote a three-page feasibility memo for the ED Board and a top-10 feature shortlist ranked on correlation and clinical sense.

**Skills used:** pandas, matplotlib, EDA, data quality assessment, clinical reasoning

---

## Week 6 — Baseline Models

Trained two baselines and compared them against a stratified random guess.

| Model | Accuracy | Macro F1 | ESI-1 recall |
| --- | --- | --- | --- |
| Random guess | 0.375 | 0.204 | 0.00 |
| Logistic regression | 0.685 | 0.518 | 0.25 |
| Decision tree (depth 6) | 0.560 | 0.226 | 0.00 |
| Logistic regression (class-weighted) | 0.585 | 0.428 | 0.69 |

It beats the coin flip, so the signal is real. That is not the number that matters. Recall on ESI 1 is 0.25, meaning the model catches one in four of the sickest patients and sends the other three to wait. Class weighting takes that to 0.69 but costs accuracy, and that trade is the Board's call, not the model's. Also went past the standard evaluation: split every prediction into over-triage against under-triage, bootstrapped a confidence interval on ESI-1 recall (0.06 to 0.50, because there are only 16 of them in the test set), and checked the coefficients point the way physiology says they should. They do.

**Skills used:** scikit-learn, logistic regression, decision trees, model evaluation, bootstrap, clinical communication

---

## Week 7 — Optimisation and Trade-offs

Trained a more complex model and then recommended against it. Reused the exact Week 6 split (seed 42) and benchmarked three base models on six axes plus interpretability.

| Model | Accuracy | Macro F1 | ESI-1 recall | Inference (ms/pred) | Explainable? |
| --- | --- | --- | --- | --- | --- |
| Logistic regression | 0.685 | 0.518 | 0.250 | 0.003 | Yes, per patient |
| Decision tree (d=6) | 0.560 | 0.226 | 0.000 | 0.001 | Path, but weak |
| XGBoost | 0.693 | 0.470 | 0.062 | 0.034 | No, needs SHAP |

Picked the candidates from the shape of the data, not at random: wide sparse tabular features, an imbalanced 5-level target, and a hard need for per-patient explanations. That points to logistic regression and gradient-boosted trees, which is also what the published triage models use. Deep learning was ruled out as unnecessary here and not interpretable.

XGBoost wins overall accuracy by less than a point but is worse on the numbers that matter for triage safety (macro F1 and recall on the sickest patients), costs about 11x the inference time per prediction, and cannot explain a single decision at the bedside. Decision: keep logistic regression for Phase 3, with class weighting to lift recall on the urgent classes. Choosing the right model is a decision, not a default.

**Skills used:** scikit-learn, XGBoost, model benchmarking, engineering trade-off analysis, technical writing

---

## Week 8 — Reproducibility and Packaging

Refactored the whole project out of notebooks into a modular, config-driven codebase that a stranger can clone and run. One `config.yaml` drives everything (seed, split, features, model), `scripts/train.py` is the single entry point, the logic lives in `src/` split by job (data, features, model, utils), and `tests/` proves the pipeline still works. The notebooks stay as a record of the exploration, not the source of truth. Added a handover document, a model-selection audit trail regenerable from one script, and a running decision journal.

```
carisurg-portfolio/
├── config.yaml            one file drives training
├── scripts/train.py       entry point
├── src/                   data.py, features.py, model.py, utils.py
├── tests/                 pipeline and schema tests
├── docs/                  proposal, memos, risk register, decisions, handover
└── notebooks/             exploration only, not the solution
```

**Skills used:** software engineering, refactoring, pytest, YAML config, reproducibility, technical documentation

---

## Reproducibility

- **Random seed: 42.** Every split, model fit, dummy baseline and bootstrap.
- **Split:** 80/20, stratified on `esi`.
- `disposition` is excluded from the features. It is the outcome, known only after triage, so using it leaks the answer.
- Package versions are pinned in `requirements.txt`.

## Data

No patient data is in this repository. Datasets are git-ignored for size and sensitivity. See `data/README.md` for the expected file and where it goes. The pipeline reads from `data/`. In Colab, mount Drive and point `read_csv` at your copy.

## Tools and Libraries

Python 3.10, pandas, numpy, matplotlib, scikit-learn, XGBoost, PyYAML, joblib, pytest, Google Colab, Git and GitHub, Zotero, Mermaid.

## Licence

MIT. See `LICENSE`.
