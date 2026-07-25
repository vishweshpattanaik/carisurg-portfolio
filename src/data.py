"""Loading and basic validation of the triage dataset."""

from pathlib import Path

import pandas as pd

# Columns the pipeline cannot run without.
REQUIRED_COLUMNS = [
    "esi",
    "age",
    "gender",
    "arrivalmode",
    "triage_vital_hr",
    "triage_vital_sbp",
    "triage_vital_rr",
    "triage_vital_o2",
    "triage_vital_temp",
]

VALID_ESI = {1, 2, 3, 4, 5}


def load_data(path):
    """Read the triage CSV from disk.

    Raises FileNotFoundError with a useful message if the data is missing,
    because the dataset is not committed to the repository.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {path}. The data is not committed to this "
            "repository. See data/README.md for where to put it."
        )
    return pd.read_csv(path)


def validate_schema(df):
    """Check the dataframe has what the pipeline needs, and fail loudly if not."""
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")

    if df["esi"].isna().any():
        raise ValueError("Target column 'esi' contains missing values.")

    found = set(df["esi"].dropna().astype(int).unique())
    if not found.issubset(VALID_ESI):
        raise ValueError(f"'esi' has unexpected values: {sorted(found - VALID_ESI)}")

    return True


def clean_data(df, drop_columns=None):
    """Drop leakage and index columns. Returns a new dataframe."""
    df = df.copy()
    for col in (drop_columns or []):
        if col in df.columns:
            df = df.drop(columns=col)
    return df


def get_data(config):
    """Load, validate and clean in one call, driven by the config."""
    df = load_data(config["data"]["path"])
    validate_schema(df)
    return clean_data(df, config["data"].get("drop_columns"))
