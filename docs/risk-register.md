# Risk Register: AI-Assisted Triage Re-stratification, Mercer General ED
 
**Author:** Vishwesh Pattanaik
**Project:** AI-assisted re-stratification of middle-band patients, Mercer General ED
**Scope:** single-site pilot, read across to a possible Saint Cedric nationwide rollout
 
Likelihood and impact are rated Low, Medium or High for the pilot context. Each mitigation carries a measurable signal that indicates whether it is working.
 
## Risk table
 
| # | Risk | Category | Likelihood | Impact | Mitigation | Signal of success |
|---|------|----------|:----------:|:------:|------------|-------------------|
| 1 | Distribution shift. The model degrades as case-mix, seasonality (for example dengue surges) or documentation habits change | AI-technical | M | H | Local validation before use. Rolling performance and drift monitoring. Periodic recalibration | Monthly AUC and calibration remain within preset bounds on a rolling validation sample |
| 2 | Label leakage. Training on disposition or downstream actions teaches the model clinician behaviour rather than deterioration | AI-technical | M | H | Outcomes defined from objective events (ICU transfer, critical intervention) with a time gap after triage. Features audited for leakage | Leakage audit passes. Performance holds on a leakage-controlled holdout |
| 3 | Poor calibration. Overconfident scores mislead nurses | AI-technical | M | M | Calibration curves. Isotonic or Platt scaling. A confidence band is displayed, not a bare flag | Calibration slope near 1.0. Brier score below threshold |
| 4 | Missing or dirty inputs degrade predictions | AI-technical | H | M | Explicit missing-data handling. Output is suppressed below a data-completeness threshold | Share of scores on incomplete records is tracked. Performance gap, complete against incomplete, stays within tolerance |
| 5 | Alert fatigue. Too many false up-triage flags lead nurses to ignore the tool | Operational | H | H | Threshold tuned for high positive predictive value. Alert rate capped. Passive, non-interruptive display | Alert rate per shift and flag PPV are monitored. Nurse dismiss rate trends down |
| 6 | Workflow disruption. The tool adds clicks or slows triage | Operational | M | M | Passive flag inside the existing triage screen. No new data entry | Added seconds per triage near zero. Nurse usability rating |
| 7 | EHR lag. Paper-to-EHR delay means the model scores on stale data | Operational | H | M | Inference triggered only on EHR-confirmed data, or vitals captured at point of care | Median data-to-score latency. Share of scores on confirmed data |
| 8 | Silent failure and over-reliance. Staff who lean on the tool miss deterioration when it fails | Operational | M | H | A clear tool-unavailable state. Nurse-led triage remains primary. Downtime drills | Documented fallback adherence during simulated outages |
| 9 | Automation bias. Nurses defer to the model and under-triage when it is wrong | Ethical | M | H | Decision-support framing, with the nurse deciding. A brief rationale required on override. Shadow mode first | Nurse-model agreement against independent judgement is tracked. Up-triage catches the model missed |
| 10 | Accountability and consent. Liability for an AI-influenced decision is unclear, and patients are unaware AI is involved | Ethical | M | M | Governance policy assigning clinician accountability. Patient-facing notice. Board sign-off | Accountability policy in place. Consent process audited |
| 11 | Training-data bias. Data skewed by age, sex, language or rural-urban access under-serves some groups | Equity | M | H | Subgroup performance audits. Reweighting. Cost and utilisation proxies avoided | Sensitivity equalised across age, sex and locale within tolerance |
| 12 | Proxy outcomes encode access inequity. Using admitted or resources-used as a label bakes in who historically received care | Equity | M | H | Labels based on clinical deterioration, not resource receipt. Equity review of the outcome definition | No systematic score gap by protected subgroup after acuity is controlled for |
 
## Top three risks
 
**1. Alert fatigue (operational).** A model that flags too many patients who are not deteriorating trains staff to ignore it. Once the flag is routinely dismissed, the tool misses the patient who matters. The Epic Sepsis Model failed in this way, as most of its alerts were false. The pilot will keep the alert rate low, favour precision over raw sensitivity, and monitor how often nurses dismiss the flag.
 
**2. Distribution shift (AI-technical).** A model can score well on Mercer's past data and still degrade as patients, seasons and recording habits change. The decay is gradual and easy to miss. The model will be validated locally before use and monitored month to month. Recalibration follows when performance slips.
 
**3. Training-data bias (equity).** If the data under-represents some groups by age, sex, language or location, the tool can serve them worse while average performance looks acceptable. Performance will be measured per subgroup, not only in aggregate. Outcome labels based on resource receipt will be avoided.
