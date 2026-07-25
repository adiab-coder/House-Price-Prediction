from pathlib import Path

import joblib
import numpy as np
import pandas as pd

_MODEL_PATH = Path(__file__).resolve().parent.parent.parent / "models" / "house_price.pkl"

_model = None


def load_model():
    """Load the pipeline once (called from the FastAPI lifespan on startup)."""
    global _model
    _model = joblib.load(_MODEL_PATH)
    return _model


def get_model():
    if _model is None:
        raise RuntimeError("Model not loaded yet. Call load_model() at startup.")
    return _model


def predict_price(row: pd.DataFrame) -> float:
    model = get_model()
    # The model was trained on log1p(price); invert with expm1.
    pred_log = model.predict(row)
    pred = np.expm1(pred_log)
    return float(pred[0])
