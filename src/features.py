"""Turning the raw dataframe into a model-ready feature matrix."""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def build_features(df, config):
    """Assemble X and y from the config.

    X = numeric vitals + the 200 one-hot chief-complaint flags + encoded categoricals.
    y = the ESI triage level.
    """
    feat = config["features"]
    target = config["data"]["target"]

    numeric = [c for c in feat["numeric"] if c in df.columns]
    complaints = [c for c in df.columns if c.startswith(feat["complaint_prefix"])]
    categorical = [c for c in feat["categorical"] if c in df.columns]

    encoded = pd.get_dummies(df[categorical], drop_first=True) if categorical else pd.DataFrame(index=df.index)

    X = pd.concat([df[numeric], df[complaints], encoded], axis=1)
    y = df[target].astype(int)
    return X, y, numeric


def split_and_scale(X, y, numeric, config):
    """80/20 stratified split, then scale only the numeric columns.

    The scaler is fitted on the training set alone, so no information from the
    test set leaks into training.
    """
    split = config["split"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=split["test_size"],
        stratify=y if split.get("stratify", True) else None,
        random_state=split["seed"],
    )

    X_train, X_test = X_train.copy(), X_test.copy()
    scaler = StandardScaler().fit(X_train[numeric])
    X_train[numeric] = scaler.transform(X_train[numeric])
    X_test[numeric] = scaler.transform(X_test[numeric])

    return X_train, X_test, y_train, y_test, scaler
