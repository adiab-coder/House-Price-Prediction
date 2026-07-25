from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 1. إعطاء تصريح كامل للمتصفح إنه يقبل الطلبات من أي مكان
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "Backend is running fine!"}

@app.post("/predict")
@app.post("/api/predict")
def predict(data: dict):
    # رجع أي رد مؤقت عشان نتأكد إن الاتصال نجح
    return {"result": "success", "data": data}