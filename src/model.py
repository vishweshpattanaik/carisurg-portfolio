"""Building, training and evaluating the triage model."""

import time

from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, f1_score, precision_score,
                             recall_score)
from sklearn.tree import DecisionTreeClassifier

# Models the config is allowed to name. Adding one here is the only change
# needed to try it from config.yaml.
REGISTRY = {
    "logistic_regression": LogisticRegression,
    "decision_tree": DecisionTreeClassifier,
    "dummy": DummyClassifier,
}


def build_model(config):
    """Create an unfitted model from the config."""
    name = config["model"]["name"]
    if name not in REGISTRY:
        raise ValueError(f"Unknown model '{name}'. Options: {list(REGISTRY)}")
    return REGISTRY[name](**config["model"].get("params", {}))


def train_model(model, X_train, y_train):
    """Fit the model and report how long it took."""
    start = time.time()
    model.fit(X_train, y_train)
    return model, round(time.time() - start, 2)


def evaluate_model(model, X_test, y_test, urgent_class=1):
    """Score the model.

    Reports macro averages and the recall on the most urgent class separately,
    because overall accuracy is dominated by the large middle band and hides
    how the model performs on the sickest patients.
    """
    start = time.time()
    preds = model.predict(X_test)
    inference_ms = (time.time() - start) / len(X_test) * 1000

    # Under-triage: predicted a less urgent level than the truth. This is the
    # clinically dangerous error, so it is measured explicitly.
    under_triage = float((preds > y_test).mean())

    return {
        "accuracy": round(accuracy_score(y_test, preds), 3),
        "macro_precision": round(precision_score(y_test, preds, average="macro", zero_division=0), 3),
        "macro_recall": round(recall_score(y_test, preds, average="macro", zero_division=0), 3),
        "macro_f1": round(f1_score(y_test, preds, average="macro", zero_division=0), 3),
        "esi1_recall": round(
            recall_score(y_test, preds, labels=[urgent_class], average=None, zero_division=0)[0], 3
        ),
        "under_triage_rate": round(under_triage, 3),
        "inference_ms_per_prediction": round(inference_ms, 4),
        "confusion_matrix": confusion_matrix(y_test, preds).tolist(),
        "report": classification_report(y_test, preds, digits=3, zero_division=0),
    }
