#!/usr/bin/env python3
"""
Training script for SageMaker XGBoost script mode (iris-style CSV with header).
The container sets SM_CHANNEL_TRAIN, SM_MODEL_DIR, and optional hyperparameters.

This file lives in container_source/ alone so SageMaker does NOT pick up a
top-level requirements.txt (pip installing sagemaker in the container breaks numpy/xgboost).
"""
import argparse
import json
import os

import pandas as pd
import xgboost as xgb


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--max_depth",
        type=int,
        default=5,
    )
    parser.add_argument(
        "--eta",
        type=float,
        default=0.2,
    )
    parser.add_argument(
        "--objective",
        type=str,
        default="multi:softmax",
    )
    parser.add_argument(
        "--num_class",
        type=int,
        default=3,
    )
    parser.add_argument(
        "--num_round",
        type=int,
        default=10,
    )
    return parser.parse_known_args()


def main():
    args, _ = parse_args()

    train_path = os.environ.get("SM_CHANNEL_TRAIN", "/opt/ml/input/data/train")
    model_dir = os.environ.get("SM_MODEL_DIR", "/opt/ml/model")

    csv_file = os.path.join(train_path, "train.csv")
    df = pd.read_csv(csv_file)
    target_col = "target"
    feature_cols = [c for c in df.columns if c != target_col]
    X = df[feature_cols].values
    y = df[target_col].values

    dtrain = xgb.DMatrix(X, label=y)

    params = {
        "max_depth": args.max_depth,
        "eta": args.eta,
        "objective": args.objective,
        "num_class": args.num_class,
    }

    booster = xgb.train(
        params,
        dtrain,
        num_boost_round=args.num_round,
    )

    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "xgboost-model")
    booster.save_model(model_path)

    config_path = os.path.join(model_dir, "xgboost-model.json")
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump({"model_path": "xgboost-model"}, f)


if __name__ == "__main__":
    main()
