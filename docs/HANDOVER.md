# Handover Document (outline — interim)

> Draft for Week 8 interim. Sections marked TODO are being completed for the final submission.

## 1. What this project is

One paragraph: an AI-assisted triage tool that re-stratifies middle-acuity (ESI 3) patients in a resource-constrained Caribbean emergency department. ESI 3 is the largest group of arrivals and the band where triage separates patients least reliably. The model flags patients in that band who may need moving up. It is decision support for a triage nurse, not an autonomous decision maker.

## 2. The final model decision

**Pinned model:** logistic regression with balanced class weights (`config.yaml`).

**Why in one sentence:** it catches far more of the sickest patients than the alternatives and can explain any single prediction to a clinician, which matters more on a triage problem than the fractional accuracy advantage XGBoost holds.

Full comparison: [`model-selection.md`](model-selection.md). Full reasoning: [`decision-journal.md`](decision-journal.md).

## 3. How to run it

```bash
git clone https://github.com/vishweshpattanaik/carisurg-portfolio.git
cd carisurg-portfolio
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# place the dataset in data/ (see section 4), then:
python scripts/train.py --config config.yaml
```

Expected output: a trained model at `artifacts/model.joblib`, metrics at `artifacts/metrics.json`, and a summary printed to the terminal.

To reproduce the full model comparison: `python scripts/compare_models.py --config config.yaml`
To run the tests: `pytest tests/`

## 4. Where the data lives and its governance status

- The dataset is **not committed** to this repository. It is git-ignored for size and sensitivity.
- Expected location: `data/yaleemmlc_admissionprediction_triage.csv`. See `data/README.md`.
- It is a de-identified, publicly released research dataset. No real Mercer patient data has been used at any point in this project.
- The pipeline fails with a clear message if the file is absent rather than failing silently.
- TODO (final): confirm the governance wording with the programme before handover.

## 5. Known limitations

1. **The model is not safe to deploy.** Even the pinned model misses roughly a third of ESI-1 patients, and the estimate is unstable because there are only 16 ESI-1 cases in the test set (bootstrap 95% CI on the plain model: 0.06 to 0.50).
2. **The training data is not Mercer's.** It comes from a single US academic emergency department with a different case mix, and it arrived pre-processed, with vitals already imputed and complaints already encoded. Those choices cannot be audited and will not carry over to a real local extract.
3. **Higher recall was bought with over-triage.** The pinned model raises more false alarms on the less urgent classes than the unweighted version. The alert burden this creates has not yet been measured against real clinical workflow.

## 6. TODO for final submission

- [ ] Expand section 1 into the full project summary
- [ ] Confirm data governance wording
- [ ] Add a "who to contact" line
- [ ] Sense-check the whole document against Martina's "new hire Monday" test
