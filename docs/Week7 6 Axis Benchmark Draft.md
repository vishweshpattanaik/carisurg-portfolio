# Week 7 - Six-axis benchmark (draft)


| Model               |   Accuracy |   Macro precision |   Macro recall |   Macro F1 |   ESI-1 recall |   Train time (s) |   Inference (ms/pred) | Interpretability       |
|:--------------------|-----------:|------------------:|---------------:|-----------:|---------------:|-----------------:|----------------------:|:-----------------------|
| Logistic regression |      0.685 |             0.663 |          0.476 |      0.518 |          0.25  |              7.1 |                 0.001 | High (per-patient)     |
| Decision tree (d=6) |      0.56  |             0.252 |          0.251 |      0.226 |          0     |              0.3 |                 0.001 | Medium (readable path) |
| XGBoost             |      0.693 |             0.692 |          0.441 |      0.47  |          0.062 |             17.4 |                 0.026 | Low (needs SHAP)       |

**Note:** XGBoost adds <1 point of accuracy but is worse on macro F1 and ESI-1 recall, the numbers that matter for triage safety, while costing more compute and all interpretability.
