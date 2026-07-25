from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# معالجة طلب الـ OPTIONS عشان الـ Preflight CORS ينجح
@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        },
    )

@app.post("/predict")
@app.post("/api/predict")
def predict(data: dict):
    # 1. لو الموديل جاهز عندك، بتعمل الحسابات هنا:
    # input_features = prepare_features(data)
    # predicted_val = float(model.predict(input_features)[0])
    
    # مؤقتاً للتجربة (أو حط متغير السعر من الموديل بتاعك):
    predicted_val = 1500000  # ضع هنا نتيجة model.predict()

    return {
        "status": "success",
        "predicted_price": predicted_val
    }