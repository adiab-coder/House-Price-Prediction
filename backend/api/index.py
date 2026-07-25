from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "House Price Prediction API is running!"}

@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}