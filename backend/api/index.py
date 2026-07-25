from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 1. إضافة الـ CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # بيسمح لجميع الدومينات
    allow_credentials=True,
    allow_methods=["*"],  # بيسمح بـ POST, GET, OPTIONS, إلخ
    allow_headers=["*"],
)

# 2. معالج يدوي لطلبات الـ OPTIONS (Preflight) عشان Vercel ما يرفضهاش
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

@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.post("/predict")
@app.post("/api/predict")
def predict(data: dict):
    # كود التوقعات بتاعك هيرجع هنا
    return {"status": "success", "data": data}