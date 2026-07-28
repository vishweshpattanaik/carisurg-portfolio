# # Handover Document

## 1. What this project is

An AI-assisted triage tool that re-stratifies middle-acuity (ESI 3) patients in a resource-constrained Caribbean emergency department. ESI 3 is the largest group of arrivals (about 49% in the reference data) and the band where triage separates patients least reliably, so it is where a second opinion is most useful. The tool produces a risk flag to support a triage nurse's decision, in particular to catch patients who should be moved up in urgency. It is decision support, not an autonomous decision maker, and it is a pilot, not a deployed system. The current model is a baseline: it is honest about its limits and is not yet safe to use on real patients (see section 5).

## 2. The final model decision

**Pinned model:** logistic regression with balanced class weights, defined in `config.yaml`.

**Why in one sentence:** across every model tested it catches by far the most of the sickest (ESI 1) patients and can explain any single prediction to a clinician in one line, which on a triage problem matters more than the fractional overall-accuracy advantage a gradient-boosted model holds.

Full comparison table: [`model-selection.md`](model-selection.md). Full reasoning and what would reverse the decision: [`decision-journal.md`](decision-journal.md), entry 4.

## 3. How to run it

```bash
git clone https://github.com/vishweshpattanaik/carisurg-portfolio.git
cd carisurg-portfolio
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# place the dataset in data/ (see section 4), then:
python scripts/train.py --config config.yaml
```

Expected result: a trained model at `artifacts/model.joblib`, metrics at `artifacts/metrics.json`, and a summary printed to the terminal (accuracy, macro F1, ESI-1 recall, under-triage rate).

- Reproduce the full model comparison: `python scripts/compare_models.py --config config.yaml`
- Run the tests: `pytest tests/`

To change what is trained, edit `config.yaml`, not the code. The seed, the split, the feature lists and the model choice all live there.

## 4. Where the data lives and its governance status

- The dataset is **not committed** to this repository. It is git-ignored for size and sensitivity.
- Expected location: `data/yaleemmlc_admissionprediction_triage.csv`. See `data/README.md`.
- It is a de-identified, publicly released research dataset. **No real Mercer patient data has been used at any point in this project.**
- The pipeline fails with a clear message if the file is absent, rather than failing silently.
- The `disposition` column is excluded from the features because it is the outcome, known only after triage. Using it would leak the answer.

## 5. Known limitations

1. **Not safe to deploy.** Even the pinned model misses roughly a third of ESI-1 patients, and the estimate is unstable: there are only 16 ESI-1 cases in the test set, and the bootstrap 95% confidence interval on the plain model runs from 0.06 to 0.50.
2. **The training data is not Mercer's.** It comes from a single US academic emergency department with a different case mix, and it arrived pre-processed, with vitals already imputed and complaints already encoded. Those choices cannot be audited and will not carry over to a real local extract.
3. **Higher recall was bought with over-triage.** The pinned model raises more false alarms on the less urgent classes than the unweighted version. The added alert burden has not yet been measured against real clinical workflow, and alert fatigue is a documented cause of clinical AI failure (see the Week 4 harm case study).

## 6. Where to take it next

- Validate on a real local extract before trusting any figure, and re-check performance by patient subgroup for equity.
- Run a shadow-mode evaluation (log the tool's suggestions alongside live nurse triage without acting on them) to measure real-world value and alert burden safely.
- Revisit the model choice only if a tuned gradient-boosted model can beat logistic regression on ESI-1 recall with reliable per-patient explanations.

## 7. Who to contact

Vishwesh Pattanaik, Clinical AI and Innovation Unit. Project supervisor: Dr De Freitas. For questions about a specific decision, start with `docs/decision-journal.md`; for the model comparison, `docs/model-selection.md`.
