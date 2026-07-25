from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "House Price Prediction API is running!"}

@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}

@app.post("/predict")  # أو /api/predict حسب اللي انت مستخدمه في الفرونت
def predict(data: HouseData):
    # كود التوقع بتاعك
    return {"prediction": result}