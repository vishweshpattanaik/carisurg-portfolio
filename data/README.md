# Data

The triage dataset is **not committed** to this repository, for size and sensitivity reasons.

## Expected file

```
data/yaleemmlc_admissionprediction_triage.csv
```

`config.yaml` points here by default. If your copy lives elsewhere, change `data.path` in the config rather than editing the code.

## What it is

A de-identified, publicly released emergency department dataset: 55,121 patient arrivals and 226 columns, covering demographics, triage vital signs, 200 one-hot chief-complaint flags, and the ESI triage level.

No real patient data from Mercer General has been used at any point in this project.

## Note on `disposition`

The `disposition` column is dropped before training (see `config.yaml`). It records what happened to the patient after triage, so it is only known after the decision the model is meant to support. Including it would leak the answer into the features.
