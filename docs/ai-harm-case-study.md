# Documented AI-Harm Case Study: The Epic Sepsis Model

**Author:** Vishwesh Pattanaik
**Project:** AI-assisted re-stratification of middle-band patients, Mercer General ED

## What happened

The Epic Sepsis Model (ESM) is a proprietary early-warning tool built into the Epic electronic health record. It raises automated alerts when a hospitalised patient may be developing sepsis. Sepsis carries an in-hospital mortality of roughly 12 to 15 percent, and early treatment reduces that risk. The model was deployed across hundreds of US hospitals. Adoption rested largely on vendor-reported performance, with Epic citing an area under the curve (AUC) of 0.76 to 0.83.

Wong et al. published an independent external validation in JAMA Internal Medicine in 2021. They examined 38,455 hospitalisations at Michigan Medicine between December 2018 and October 2019. The model performed well below its reported figures. It returned an AUC of 0.63, a sensitivity of 33 percent, a specificity of 83 percent, and a positive predictive value of 12 percent. It therefore missed about two-thirds of sepsis cases, and roughly seven in eight of its alerts were false. It also alerted on a large share of admitted patients, which placed a heavy load on clinicians. A later emergency department validation across two county EDs, covering 145,885 encounters in 2024, reported sensitivity near 15 percent within the recommended six-hour window.

The harm took two forms. Patients faced missed or delayed sepsis recognition from a tool clinicians had been told to trust. Clinicians faced alert fatigue from a high volume of false alarms, which reduces attention to later alerts.

## Root-cause analysis

**Deployment at scale without independent external validation.** The reported AUC of 0.76 to 0.83 was developer-reported on Epic's own data. No broad independent validation preceded wide adoption. On a different population, performance fell to 0.63. This is distribution shift. It was not detected because it was not tested before go-live.

**Target definition and label leakage.** The sepsis label and several features were entangled with clinician behaviour, including actions that occur only after a clinician already suspects sepsis. A model that partly learns prior clinician actions confirms cases late and provides little early warning.

**Low precision and alert fatigue.** A positive predictive value of 12 percent means most alerts are false. An interruptive alert at that precision, fired on a large share of patients, leads staff to dismiss it. High sensitivity on paper has no value once the alert is ignored.

**Proprietary opacity.** The model was a closed product. Hospitals could not inspect its training, calibration or thresholds, and could not anticipate these failures.

## What would have caught it

External and prospective validation at each site before go-live would have exposed the performance gap. Local recalibration, a shadow-mode period measuring sensitivity, positive predictive value and alert burden against real outcomes, transparency requirements for proprietary models, and continuous post-deployment monitoring would have caught the remaining failures. These safeguards are built into the Mercer plan. The model is validated locally and run in shadow mode before it is allowed to influence any triage decision.

## Source

Wong A, Otles E, Donnelly JP, et al. External validation of a widely implemented proprietary sepsis prediction model in hospitalized patients. JAMA Internal Medicine. 2021;181(8):1065-1070. doi:10.1001/jamainternmed.2021.2626. See also the accompanying editorial: Habib AR, Lin AL, Grant RW. The Epic Sepsis Model falls short: the importance of external validation. JAMA Internal Medicine. 2021;181(8):1040-1041.
