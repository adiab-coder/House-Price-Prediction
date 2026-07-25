from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# تفعيل الـ CORS لتسمح للفرونت إند يكلم الباك إند
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # أو حط رابط الفرونت إند بتاعك صراحة
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.post("/predict")
@app.post("/api/predict")
def predict(data: dict):
    # كود التوقع بتاعك
    return {"status": "success"}