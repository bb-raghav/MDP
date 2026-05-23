from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

import requests
import joblib
import pandas as pd

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
# LOAD MODEL
# =========================================

model_path = os.path.join(
    os.path.dirname(__file__),
    "models",
    "saved",
    "aqi_regression_model.pkl"
)
model = joblib.load(model_path)


# =========================================
# AQI CATEGORY
# =========================================

def get_category(aqi):

    if aqi <= 50:
        return "Good"

    elif aqi <= 100:
        return "Moderate"

    elif aqi <= 150:
        return "Poor"

    else:
        return "Very Poor"


# =========================================
# ROOT
# =========================================

@app.get("/")
def root():

    return {
        "message": "AQI Backend Running"
    }


# =========================================
# GEOCODE
# =========================================

@app.get("/geocode/{city}")

def geocode(city: str):

    url = (
        f"https://nominatim.openstreetmap.org/search"
        f"?q={city}&format=json&limit=1"
    )

    headers = {
        "User-Agent": "aqi-ai-project"
    }

    response = requests.get(
        url,
        headers=headers
    )

    data = response.json()

    if len(data) == 0:

        return {
            "error": "City not found"
        }

    return {

        "lat":
            float(data[0]["lat"]),

        "lon":
            float(data[0]["lon"]),

        "name":
            city.title(),
    }


# =========================================
# LIVE AQI
# =========================================

WAQI_TOKEN = os.getenv("WAQI_API_KEY", "")
if not WAQI_TOKEN:
    raise ValueError("WAQI_API_KEY environment variable is required")


@app.get("/live-aqi/{city}")

def get_live_aqi(city: str):

    city = city.strip()

    url = (
        f"https://api.waqi.info/feed/"
        f"{city}/?token={WAQI_TOKEN}"
    )

    response = requests.get(url)

    data = response.json()

    if data["status"] != "ok":

        return {
            "error":
            f"WAQI could not find {city}"
        }

    iaqi = data["data"].get("iaqi", {})

    return {

        "live_aqi":
            data["data"].get("aqi", 0),

        "pm25":
            iaqi.get("pm25", {}).get("v", 0),

        "pm10":
            iaqi.get("pm10", {}).get("v", 0),

        "no2":
            iaqi.get("no2", {}).get("v", 0),

        "so2":
            iaqi.get("so2", {}).get("v", 0),

        "co":
            iaqi.get("co", {}).get("v", 0),

        "temperature":
            round(
                iaqi.get("t", {}).get("v", 30),
                1
            ),

        "humidity":
            iaqi.get("h", {}).get("v", 60),

        "pressure":
            iaqi.get("p", {}).get("v", 1008),

        "wind_speed":
            iaqi.get("w", {}).get("v", 5),

        "apparent_temperature":
            round(
                iaqi.get("t", {}).get("v", 30),
                1
            ),
    }


# =========================================
# PREDICT
# =========================================

@app.post("/predict")
def predict(payload: dict):
    try:
        if not payload:
            return {"error": "Empty payload"}

        df = pd.DataFrame([payload])
        prediction = model.predict(df)[0]

        return {
            "predicted_aqi": round(float(prediction), 1),
            "category": get_category(prediction),
        }

    except Exception as e:
        return {"error": str(e)}