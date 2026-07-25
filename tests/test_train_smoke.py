"""Smoke test: the whole pipeline runs on a tiny slice of data."""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.features import build_features, split_and_scale
from src.model import build_model, evaluate_model, train_model

CONFIG = {
    "data": {"target": "esi"},
    "features": {
        "numeric": ["age", "triage_vital_hr", "triage_vital_o2"],
        "categorical": ["gender"],
        "complaint_prefix": "cc_",
    },
    "split": {"test_size": 0.2, "stratify": True, "seed": 42},
    "model": {
        "name": "logistic_regression",
        "params": {"max_iter": 500, "class_weight": "balanced", "random_state": 42},
    },
}


def make_small_df(n=50):
    """50 synthetic rows - enough to prove the pipeline runs, not to learn anything."""
    rng = np.random.default_rng(42)
    return pd.DataFrame({
        "esi": np.tile([1, 2, 3, 4, 5], n // 5),
        "age": rng.integers(18, 90, n),
        "gender": rng.choice(["Male", "Female"], n),
        "triage_vital_hr": rng.integers(50, 130, n),
        "triage_vital_o2": rng.integers(88, 100, n),
        "cc_chestpain": rng.integers(0, 2, n),
        "cc_fall": rng.integers(0, 2, n),
    })


def test_pipeline_runs_end_to_end():
    df = make_small_df()
    X, y, numeric = build_features(df, CONFIG)
    X_tr, X_te, y_tr, y_te, scaler = split_and_scale(X, y, numeric, CONFIG)

    model, seconds = train_model(build_model(CONFIG), X_tr, y_tr)
    metrics = evaluate_model(model, X_te, y_te)

    # We do not assert the model is good on 50 random rows, only that it ran
    # and produced metrics in a sensible range.
    assert 0.0 <= metrics["accuracy"] <= 1.0
    assert 0.0 <= metrics["macro_f1"] <= 1.0
    assert seconds >= 0
    assert len(metrics["confusion_matrix"]) == 5


def test_split_is_reproducible():
    """Same seed, same split. This is what makes results comparable week to week."""
    df = make_small_df()
    X, y, numeric = build_features(df, CONFIG)
    a = split_and_scale(X, y, numeric, CONFIG)[0]
    b = split_and_scale(X, y, numeric, CONFIG)[0]
    assert list(a.index) == list(b.index)
