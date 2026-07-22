# Decision Journal
Vishwesh Pattanaik | CariSurg MedTech Pathways 2026

A running log of the real decisions made on this project, why they were made, what was rejected, and what would change my mind. Newest last.

---

## 1. Is the dataset good enough to build on?
**Week 5**

**Decision:** Proceed with the Yale ED dataset, with caveats documented.

**Why:** 55,121 patients, complete target, and the middle band (ESI 3) is 49% of arrivals, exactly where the project is aimed. The data behaves sensibly (chest pain and shortness of breath correlate with higher acuity).

**What worried me:** Zero missing values anywhere. That is not what real ED data looks like. This is the processed release, so vitals were imputed and complaints encoded before it reached me, and I cannot audit those choices. Mercer's own extract will be messier.

**What would change my mind:** If the pre-processing turned out to have leaked outcome information, or if a Mercer sample looked nothing like this distribution, I would treat the dataset as a rehearsal only.

**Lesson:** Clean data is not automatically good data. The useful question is what happened to it before it reached me.

---

## 2. Exclude `disposition` from the features
**Week 6**

**Decision:** Drop the `disposition` column before training.

**Why:** Disposition (admitted, discharged, transferred) is the outcome, known only after triage. Feeding it to the model would let it predict the answer from the answer, inflating scores that would collapse in real use.

**What I rejected:** Keeping it for a higher accuracy number. That number would have been a lie.

**Lesson:** A feature that would not be available at the moment of prediction is leakage, however predictive it looks.

---

## 3. Primary metric: recall on ESI 1, not accuracy
**Week 6**

**Decision:** Judge the model on recall for the sickest patients (ESI 1) and on under-triage rate, not on overall accuracy.

**Why:** Accuracy is dominated by the large ESI 3 group, so a model can score 0.68 while missing three quarters of Level 1 patients. In triage, under-triaging a critical patient can be fatal; over-triage only wastes a bed. The two errors are not equal, so the metric should not treat them equally.

**What I rejected:** Reporting overall accuracy as the headline. It hides the failure that matters.

**What would change my mind:** Nothing on the metric choice. This is a safety property of the problem, not a modelling preference.

**Lesson:** Choose the metric from the consequences of being wrong, not from what looks best.

---

## 4. Keep logistic regression, reject XGBoost
**Week 7**

**Decision:** Use logistic regression for Phase 3, with class weighting. Keep XGBoost as a documented comparison, not the deployed model.

**Why:** I compared three base models on six axes plus interpretability. XGBoost won overall accuracy by less than a point but was worse on macro F1 and on recall for ESI 1 (0.06 vs 0.25), cost about 11x the inference time per prediction, and cannot explain a single decision to a clinician without an extra tool. On a triage problem, catching the sickest patients and being explainable beat a fractional accuracy gain.

**What I rejected:** Tuning XGBoost hard to chase a higher number, and deep learning. The team's guidance was not to tunnel on accuracy, and a leaderboard gain is the wrong use of a 13-week pilot. Deep learning was rejected as unnecessary for this data size and not interpretable.

**What would change my mind:** A tuned gradient-boosted model that clearly beats logistic regression on ESI-1 recall, with explanations made reliable for clinicians.

**Lesson:** The professional move was building the complex model and then recommending against it. Choosing the right model is a decision, not a default.
