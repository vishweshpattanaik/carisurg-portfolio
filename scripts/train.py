"""Entry point: train the pinned triage model from config.yaml.

Usage:
    python scripts/train.py --config config.yaml
"""

import argparse
import sys
from pathlib import Path

import joblib

# Allow "python scripts/train.py" to find src/ without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.data import get_data
from src.features import build_features, split_and_scale
from src.model import build_model, evaluate_model, train_model
from src.utils import load_config, save_json, set_seed


def main():
    parser = argparse.ArgumentParser(description="Train the CariSurg triage model.")
    parser.add_argument("--config", default="config.yaml", help="path to config file")
    args = parser.parse_args()

    config = load_config(args.config)
    set_seed(config["split"]["seed"])

    print(f"Loading data from {config['data']['path']} ...")
    df = get_data(config)
    print(f"  {df.shape[0]} patients, {df.shape[1]} columns")

    X, y, numeric = build_features(df, config)
    X_train, X_test, y_train, y_test, scaler = split_and_scale(X, y, numeric, config)
    print(f"  train {len(X_train)} / test {len(X_test)}, {X.shape[1]} features")

    print(f"Training {config['model']['name']} ...")
    model = build_model(config)
    model, train_seconds = train_model(model, X_train, y_train)
    print(f"  done in {train_seconds}s")

    metrics = evaluate_model(model, X_test, y_test)
    metrics["train_seconds"] = train_seconds
    metrics["model"] = config["model"]["name"]
    metrics["params"] = config["model"].get("params", {})

    print("\n--- Results ---")
    print(f"Accuracy   : {metrics['accuracy']}")
    print(f"Macro F1   : {metrics['macro_f1']}")
    print(f"ESI-1 recall: {metrics['esi1_recall']}   <-- the metric that matters")
    print(f"Under-triage rate: {metrics['under_triage_rate']}")
    print()
    print(metrics.pop("report"))

    model_path = Path(config["output"]["model_path"])
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "scaler": scaler, "columns": list(X.columns)}, model_path)
    save_json(metrics, config["output"]["metrics_path"])
    print(f"Saved model  -> {model_path}")
    print(f"Saved metrics -> {config['output']['metrics_path']}")


if __name__ == "__main__":
    main()
