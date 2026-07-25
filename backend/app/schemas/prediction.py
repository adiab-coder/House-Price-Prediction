from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    location: str = Field(..., examples=["thane"])
    area_sqft: float = Field(..., gt=0, description="Carpet/super area in square feet")
    floor_num: int = Field(..., ge=-1, description="Floor number (0 = Ground, -1 = Basement)")
    bathroom_num: int = Field(..., ge=0)
    balcony_num: int = Field(0, ge=0)
    car_parking_num: int = Field(0, ge=0)
    furnishing: str = Field(..., examples=["Semi-Furnished"])  # Furnished | Semi-Furnished | Unfurnished
    transaction: str = Field(..., examples=["Resale"])  # New Property | Resale
    ownership: str = Field(..., examples=["Freehold"])
    facing: str = Field(..., examples=["East"])


class PredictionResponse(BaseModel):
    predicted_price: float
