from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)  # triggers lifespan -> loads the model


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_happy_path():
    payload = {
        "location": "thane",
        "area_sqft": 750,
        "floor_num": 3,
        "bathroom_num": 2,
        "balcony_num": 1,
        "car_parking_num": 1,
        "furnishing": "Semi-Furnished",
        "transaction": "Resale",
        "ownership": "Freehold",
        "facing": "East",
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "predicted_price" in body
    assert body["predicted_price"] > 0


def test_predict_invalid_input():
    # area_sqft must be > 0
    payload = {
        "location": "thane",
        "area_sqft": -10,
        "floor_num": 3,
        "bathroom_num": 2,
        "furnishing": "Semi-Furnished",
        "transaction": "Resale",
        "ownership": "Freehold",
        "facing": "East",
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
