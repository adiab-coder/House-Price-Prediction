from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "House Price Prediction API is running!"}

@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}

# دعم كلا المسارين بنفس الـ function
@app.post("/predict")
@app.post("/api/predict")
def predict(data: dict):
    # كود التوقع بتاعك هنا
    return {"prediction": 250000}