import sys
import os

# إضافة فولدر backend للـ Path عشان يعرف يشوف الملفات اللي جنبه
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# استدعاء الـ app من ملف الـ FastAPI الرئيسي عندك (سواء اسمه main أو app)
try:
    from main import app
except ImportError:
    from app import app