"""Reproduce the full Week 6-7 model comparison that led to the pinned model.

Usage:
    python scripts/compare_models.py --config config.yaml

This regenerates the audit trail in docs/model-selection.md.
"""

import argparse
import sys
import time
from pathlib import Path

import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, f1_score, precision_score,
                             recall_score)
from sklearn.tree import DecisionTreeClassifier

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.data import get_data
from src.features import build_features, split_and_scale
from src.utils import load_config, set_seed

SEED = 42

CANDIDATES = [
    ("Random guess (stratified)", "strategy=stratified",
     DummyClassifier(strategy="stratified", random_state=SEED)),
    ("Decision tree", "max_depth=6",
     DecisionTreeClassifier(max_depth=6, random_state=SEED)),
    ("Logistic regression", "max_iter=2000",
     LogisticRegression(max_iter=2000, random_state=SEED)),
    ("Logistic regression (weighted)", "max_iter=2000, class_weight=balanced",
     LogisticRegression(max_iter=2000, class_weight="balanced", random_state=SEED)),
]

try:
    from xgboost import XGBClassifier
    HAS_XGB = True
except ImportError:
    HAS_XGB = False


def score(name, params, model, X_tr, y_tr, X_te, y_te, shift=False):
    """Fit, time, and score one model. shift handles XGBoost's 0-indexed labels."""
    y_fit = y_tr - 1 if shift else y_tr
    t0 = time.time(); model.fit(X_tr, y_fit); train_s = time.time() - t0
    t0 = time.time(); preds = model.predict(X_te); infer_ms = (time.time() - t0) / len(X_te) * 1000
    if shift:
        preds = preds + 1
    return {
        "Model": name,
        "Key hyperparameters": params,
        "Accuracy": round(accuracy_score(y_te, preds), 3),
        "Macro precision": round(precision_score(y_te, preds, average="macro", zero_division=0), 3),
        "Macro recall": round(recall_score(y_te, preds, average="macro", zero_division=0), 3),
        "Macro F1": round(f1_score(y_te, preds, average="macro", zero_division=0), 3),
        "ESI-1 recall": round(recall_score(y_te, preds, labels=[1], average=None, zero_division=0)[0], 3),
        "Train time (s)": round(train_s, 1),
        "Inference (ms/pred)": round(infer_ms, 4),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    config = load_config(args.config)
    set_seed(SEED)

    df = get_data(config)
    X, y, numeric = build_features(df, config)
    X_tr, X_te, y_tr, y_te, _ = split_and_scale(X, y, numeric, config)

    rows = [score(n, p, m, X_tr, y_tr, X_te, y_te) for n, p, m in CANDIDATES]

    if HAS_XGB:
        rows.append(score(
            "XGBoost", "n_estimators=300, max_depth=6, lr=0.1",
            XGBClassifier(n_estimators=300, max_depth=6, learning_rate=0.1,
                          subsample=0.8, colsample_bytree=0.8, random_state=SEED,
                          eval_metric="mlogloss", n_jobs=4),
            X_tr, y_tr, X_te, y_te, shift=True))

    table = pd.DataFrame(rows)
    print(table.to_string(index=False))

    out = Path("docs/model-selection.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(out, index=False)
    print(f"\nSaved -> {out}")


if __name__ == "__main__":
    main()
