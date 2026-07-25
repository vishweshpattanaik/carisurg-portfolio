"""Sanity check: the data loads and has the schema the pipeline expects."""

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.data import clean_data, validate_schema


def make_valid_df():
    """A tiny dataframe with the shape the real data has."""
    return pd.DataFrame({
        "esi": [1, 2, 3, 4, 5],
        "age": [45, 60, 33, 71, 28],
        "gender": ["Male", "Female", "Male", "Female", "Male"],
        "arrivalmode": ["Ambulance", "Walk-in", "Walk-in", "Ambulance", "Walk-in"],
        "triage_vital_hr": [88, 102, 75, 66, 91],
        "triage_vital_sbp": [120, 98, 135, 145, 118],
        "triage_vital_rr": [18, 22, 16, 14, 20],
        "triage_vital_o2": [98, 91, 99, 97, 96],
        "triage_vital_temp": [98.6, 101.2, 97.8, 98.1, 99.0],
        "disposition": ["Admit", "Admit", "Discharge", "Admit", "Discharge"],
        "cc_chestpain": [1, 0, 0, 1, 0],
    })


def test_valid_schema_passes():
    assert validate_schema(make_valid_df()) is True


def test_missing_column_fails_loudly():
    df = make_valid_df().drop(columns="triage_vital_o2")
    with pytest.raises(ValueError, match="missing required columns"):
        validate_schema(df)


def test_bad_esi_value_fails_loudly():
    df = make_valid_df()
    df.loc[0, "esi"] = 9          # not a real triage level
    with pytest.raises(ValueError, match="unexpected values"):
        validate_schema(df)


def test_missing_target_fails_loudly():
    df = make_valid_df()
    df.loc[0, "esi"] = None
    with pytest.raises(ValueError, match="missing values"):
        validate_schema(df)


def test_leakage_column_is_dropped():
    """'disposition' is the outcome and must never reach the model."""
    cleaned = clean_data(make_valid_df(), drop_columns=["disposition"])
    assert "disposition" not in cleaned.columns
