"""Shared helpers: config loading and seeding."""

import json
import random
from pathlib import Path

import numpy as np
import yaml


def load_config(path="config.yaml"):
    """Read the YAML config into a dictionary."""
    with open(path, "r") as f:
        return yaml.safe_load(f)


def set_seed(seed):
    """Set every random seed we control, so runs are repeatable."""
    random.seed(seed)
    np.random.seed(seed)


def save_json(obj, path):
    """Write a dictionary to disk as JSON, creating folders if needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
