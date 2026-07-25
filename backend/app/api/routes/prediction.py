from fastapi import APIRouter

from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.inference import predict_price
from app.services.preprocessing import request_to_dataframe

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest):
    row = request_to_dataframe(payload)
    price = predict_price(row)
    return PredictionResponse(predicted_price=price)
