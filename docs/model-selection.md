# Model Selection

Every model trained across Weeks 6 and 7, on the same data and the same 80/20 stratified split, seed 42. This is the audit trail behind the pinned model.

Regenerate with:

```
python scripts/compare_models.py --config config.yaml
```

| Model | Key hyperparameters | Accuracy | Macro precision | Macro recall | Macro F1 | ESI-1 recall | Train time (s) | Inference (ms/pred) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Random guess (stratified) | strategy=stratified | 0.375 | 0.204 | 0.204 | 0.204 | 0.000 | 0.0 | 0.0002 |
| Decision tree | max_depth=6 | 0.560 | 0.252 | 0.251 | 0.226 | 0.000 | 0.3 | 0.0009 |
| Logistic regression | max_iter=2000 | 0.685 | 0.663 | 0.476 | 0.518 | 0.250 | 5.5 | 0.0010 |
| **Logistic regression (weighted)** ✅ | max_iter=2000, class_weight=balanced | 0.585 | 0.426 | 0.637 | **0.688** | **0.688** | 6.0 | 0.0012 |
| XGBoost | n_estimators=300, max_depth=6, lr=0.1 | **0.693** | **0.692** | 0.441 | 0.470 | 0.062 | 20.3 | 0.0330 |

✅ **Winner: logistic regression with balanced class weights.** Pinned in `config.yaml`.

Accuracy and recall figures are deterministic under seed 42 and will reproduce exactly. Training and inference times depend on the machine and will differ from run to run.

## Why this one

XGBoost has the best overall accuracy (0.693) and the best macro precision. It is not the winner, because on a triage problem those are not the numbers that decide patient safety.

**ESI-1 recall is the deciding metric.** ESI 1 patients need a resuscitation bay within minutes. Missing one can be fatal; over-triaging an ESI 4 wastes a bed. The two errors are not equal, so the metric must not treat them equally. On that measure the pinned model catches roughly 11 of every 16 critical patients, against 4 for plain logistic regression and 1 for XGBoost.

**The cost of that choice is honest and stated.** The pinned model gives up 10 points of overall accuracy (0.585 against 0.685) and raises false alarms on the less urgent classes. That trade, more critical patients caught in exchange for more over-triage, is the ED Board's decision to make, and the numbers to make it with are in this table.

**Interpretability was a hard requirement.** Logistic regression gives one coefficient per feature, so a clinician can be told why a specific patient was flagged in a single sentence. XGBoost is 300 trees and needs a separate tool to explain any individual prediction, which is a poor fit for a bedside decision at 3am.

Full reasoning, including what would change this decision, is in [`decision-journal.md`](decision-journal.md), entry 4.
