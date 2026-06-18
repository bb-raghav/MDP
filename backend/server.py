from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

import pandas as pd

from backend.models.inference.service import (
    get_model_status,
    predict_city,
    predict_from_features,
)
from backend.services.aqi import fetch_live_aqi, get_category
from backend.services.geocoding import geocode_city, suggest_places

load_dotenv()


# =========================================
# APP
# =========================================

app = FastAPI()


# =========================================
# CORS
# =========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


# =========================================
# ROOT
# =========================================

@app.get("/")
def root():

    return {
        "message": "AQI Backend Running"
    }


@app.get("/health")
def health():
    model_status = get_model_status()

    return {
        "status": "ok",
        "waqi_configured": bool(WAQI_TOKEN),
        **model_status,
    }


# =========================================
# GEOCODE
# =========================================

@app.get("/geocode/{city}")

def geocode(city: str):
    return geocode_city(city)



@app.get("/geocode-suggest/{query}")
def geocode_suggest(query: str):
    return suggest_places(query)


# =========================================
# LIVE AQI
# =========================================

WAQI_TOKEN = os.getenv("WAQI_API_KEY") or os.getenv("VITE_WAQI_API_KEY", "")


@app.get("/live-aqi/{city}")

def get_live_aqi(city: str):
    return fetch_live_aqi(city, WAQI_TOKEN)


@app.get("/predict-city/{city}")
def predict_city_aqi(city: str):
    live_data = fetch_live_aqi(city, WAQI_TOKEN)

    if live_data.get("error"):
        return live_data

    return predict_city(city, live_data)


# =========================================
# PREDICT
# =========================================

@app.post("/predict")
def predict(payload: dict):
    try:
        if not payload:
            return {"error": "Empty payload"}

        df = pd.DataFrame([payload])
        result = predict_from_features(df.iloc[0].to_dict())

        if result.get("error"):
            return result

        return {
            "predicted_aqi": result["predicted_aqi"],
            "category": get_category(result["predicted_aqi"]),
        }

    except Exception as e:
        return {"error": str(e)}
