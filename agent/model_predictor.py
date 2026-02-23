# agent/model_predictor.py

import json
import joblib
import pandas as pd
from agent.model_router import get_model_config

_MODEL_CACHE = {}


def _load_model(model_id: str):
    if model_id in _MODEL_CACHE:
        return _MODEL_CACHE[model_id]

    cfg = get_model_config(model_id)
    model = joblib.load(cfg["model_path"])

    with open(cfg["feature_path"], "r", encoding="utf-8") as f:
        features = json.load(f)

    _MODEL_CACHE[model_id] = (model, features)
    return model, features


def predict_risk(model_id: str, feature_rows: list) -> list:
    """
    feature_rows: List[dict]
    """
    model, features = _load_model(model_id)

    df = pd.DataFrame(feature_rows)
    df = df[features]  # 强制特征对齐

    scores = model.predict_proba(df)[:, 1]
    return scores.tolist()
