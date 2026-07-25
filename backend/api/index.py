from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# تعريف الشكل اللي البيانات جاية بيه من الفرونت إند
class HouseData(BaseModel):
    # حط هنا الأقسام اللي جاية من الفرونت أو سيبها فاضية لو بتبعت dict
    pass

@app.get("/")
def read_root():
    return {"message": "House Price Prediction API is running!"}

@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}

# الـ Endpoint المطلوبة للتوقع
@app.post("/predict")
def predict(data: dict):
    # هنا حط كود التوقع بتاعك، ودلوقتي بيرجع قيمة وهمية عشان تتأكد إن الربط شغال
    return {"prediction": 250000}