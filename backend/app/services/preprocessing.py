import json
from pathlib import Path

import pandas as pd

from app.schemas.prediction import PredictionRequest

_LOCATIONS_PATH = Path(__file__).resolve().parent.parent / "locations.json"
with open(_LOCATIONS_PATH) as f:
    ALLOWED_LOCATIONS = set(json.load(f))

# Must match the column names/order used when training the pipeline in the notebook.
NUMERIC_FEATURES = ["area_sqft", "floor_num", "bathroom_num", "balcony_num", "car_parking_num"]
CATEGORICAL_FEATURES = ["location_grouped", "Furnishing", "Transaction", "Ownership", "facing"]


def request_to_dataframe(payload: PredictionRequest) -> pd.DataFrame:
    """Turn a validated request into the one-row DataFrame the exported
    scikit-learn Pipeline expects. Unknown locations are mapped to 'other',
    exactly like the grouping step in the training notebook."""
    location_grouped = payload.location if payload.location in ALLOWED_LOCATIONS else "other"

    row = {
        "area_sqft": payload.area_sqft,
        "floor_num": payload.floor_num,
        "bathroom_num": payload.bathroom_num,
        "balcony_num": payload.balcony_num,
        "car_parking_num": payload.car_parking_num,
        "location_grouped": location_grouped,
        "Furnishing": payload.furnishing,
        "Transaction": payload.transaction,
        "Ownership": payload.ownership,
        "facing": payload.facing,
    }
    return pd.DataFrame([row], columns=NUMERIC_FEATURES + CATEGORICAL_FEATURES)
