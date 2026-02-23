# agent/model_router.py

ALLOWED_MODELS = {
    "claim_risk_v1": {
        "model_path": "models/claim_risk_model_v1.pkl",
        "feature_path": "models/feature_list_v1.json",
        "description": "理赔风险预测模型 v1"
    }
}


def get_model_config(model_id: str):
    if model_id not in ALLOWED_MODELS:
        raise ValueError("Model not allowed")
    return ALLOWED_MODELS[model_id]
