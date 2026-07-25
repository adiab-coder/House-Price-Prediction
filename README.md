# House Price Prediction — End-to-End ML Web App

Predict Indian residential property prices from a notebook-trained scikit-learn
pipeline, served through a FastAPI backend and a React + TypeScript frontend.

## Overview

```
Raw CSV (Kaggle) → Jupyter notebook (clean, EDA, train, export .pkl)
                 → FastAPI backend (loads .pkl, exposes /predict)
                 → React frontend (form → prediction → result page)
```

## Architecture

```
┌─────────────┐      HTTP POST /predict      ┌──────────────┐      joblib.load     ┌────────────────┐
│   React     │ ────────────────────────────▶│   FastAPI    │ ───────────────────▶ │ house_price.pkl │
│  frontend   │◀──────────────────────────── │   backend    │                      │ (sklearn Pipeline)│
└─────────────┘      { predicted_price }      └──────────────┘                      └────────────────┘
```

## Tech stack

- **Notebook:** Python, pandas, scikit-learn, matplotlib, seaborn, joblib
- **Backend:** FastAPI, Pydantic, uvicorn
- **Frontend:** React 18, TypeScript, Vite, react-router-dom

## Project structure

```
house-price-project/
├── notebooks/
│   ├── house_price_model.ipynb   # cleaning, EDA, training, export
│   └── data/                     # raw + cleaned CSV (gitignored)
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI app, CORS, lifespan model load
│   │   ├── api/routes/prediction.py   # GET /health, POST /predict
│   │   ├── core/config.py             # settings from .env
│   │   ├── schemas/prediction.py      # request/response models
│   │   ├── services/preprocessing.py  # request -> one-row DataFrame
│   │   ├── services/inference.py      # load .pkl, predict
│   │   └── locations.json             # allowed location dropdown values
│   ├── models/house_price.pkl
│   ├── tests/test_prediction.py
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
└── frontend/
    └── src/
        ├── api/predictionClient.ts
        ├── components/PredictionForm.tsx
        ├── pages/HomePage.tsx | ResultPage.tsx | NotFoundPage.tsx
        ├── types/prediction.ts
        └── App.tsx
```

## Dataset

[House Price](https://www.kaggle.com/datasets/juhibhojani/house-price) by Juhi Bhojani (Kaggle).

```bash
pip install kaggle
# Get your API token: Kaggle -> Settings -> API -> "Create New Token"
# Place kaggle.json in ~/.kaggle/ (macOS/Linux) or C:\Users\<you>\.kaggle\ (Windows)
kaggle datasets download -d juhibhojani/house-price -p notebooks/data --unzip
```

> This project was trained on a ~16k-row extract of the dataset, dominated by
> listings in Ahmedabad, Thane, Mumbai, Bangalore, Navi Mumbai, and Nagpur.
> If you download the full ~187k-row dataset from Kaggle, re-run the notebook —
> `location_grouped`, the `.pkl`, and `locations.json` will change.

## Notebook

```bash
cd notebooks
python -m venv .venv && source .venv/bin/activate   # source .venv/Scripts/activate on Windows
pip install jupyter pandas numpy scikit-learn matplotlib seaborn joblib
jupyter notebook house_price_model.ipynb
```

Run all cells top-to-bottom. It cleans the data, produces 6 plots, trains and
compares 3 models, and exports `house_price.pkl` + `locations.json` — copy both
into `backend/models/` and `backend/app/` respectively (already done in this repo).

### Model metrics (test set)

| Model | MAE (₹) | RMSE (₹) | R² |
|---|---|---|---|
| **GradientBoostingRegressor (chosen)** | 3,251,325 | 5,930,474 | **0.863** |
| RandomForestRegressor | 3,260,228 | 6,354,727 | 0.842 |
| LinearRegression | 25,410,012 | 709,645,896 | -1963.16 |

`GradientBoostingRegressor` was selected: both tree ensembles handle the
skewed price distribution and high-cardinality categoricals far better than
plain linear regression, and gradient boosting edges out the random forest on
every metric. 5-fold cross-validation on the log-transformed target gives a
mean R² of 0.71, somewhat lower than the single test split — a sign that some
of the smaller cities in this dataset have too few listings to generalize
perfectly.

## Backend setup

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
# open http://localhost:8000/docs
```

Run tests:

```bash
pytest
```

### Environment variables

| Variable | Description | Default |
|---|---|---|
| `CORS_ALLOWED_ORIGINS` | Origin allowed to call the API | `http://localhost:5173` |

### API reference

**GET /health**

```bash
curl http://localhost:8000/health
# {"status": "ok"}
```

**POST /predict**

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "location": "thane",
    "area_sqft": 750,
    "floor_num": 3,
    "bathroom_num": 2,
    "balcony_num": 1,
    "car_parking_num": 1,
    "furnishing": "Semi-Furnished",
    "transaction": "Resale",
    "ownership": "Freehold",
    "facing": "East"
  }'
# {"predicted_price": 8112584.23}
```

## Frontend setup

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
# open http://localhost:5173
```

### Environment variables

| Variable | Description | Default |
|---|---|---|
| `VITE_API_BASE_URL` | Base URL of the FastAPI backend | `http://localhost:8000` |

Build for production with `npm run build`.

## Running the full app

1. Start the backend on port 8000 (`uvicorn app.main:app --reload`).
2. Start the frontend on port 5173 (`npm run dev`).
3. Open `http://localhost:5173`, fill in the property form, and submit to see
   a real prediction from the trained model.

## Notes on data quality

This dataset is messy by design and required several cleaning steps handled
in the notebook: parsing `"42 Lac"` / `"1.2 Cr"` price strings, extracting and
normalizing area units (`sqft`/`sqm`), parsing `"3 out of 10"` floor strings,
grouping high-cardinality locations into a top-N + "other" bucket, trimming
price-per-sqft outliers, and — importantly — dropping ~9.8k exact duplicate
rows that would otherwise leak across the train/test split and inflate
reported accuracy.
