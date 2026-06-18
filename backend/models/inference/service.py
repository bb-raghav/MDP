import os
from datetime import datetime

import joblib
import pandas as pd

from backend.services.aqi import get_category


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
MODEL_PATH = os.path.join(BASE_DIR, "saved", "aqi_regression_model.pkl")
CITY_ENCODER_PATH = os.path.join(BASE_DIR, "saved", "city_encoder.pkl")
RAW_DATA_PATH = os.path.join(ROOT_DIR, "data", "external", "data_1055_rows.csv")

FEATURE_COLUMNS = [
    "pm2_5",
    "pm10",
    "no2",
    "so2",
    "co",
    "temperature",
    "humidity",
    "pressure",
    "wind_speed",
    "apparent_temperature",
    "year",
    "month",
    "day",
    "weekday",
    "city_encoded",
]


def _load_model():
    try:
        return joblib.load(MODEL_PATH), None
    except Exception as exc:
        return None, str(exc)


def _build_city_encoder_from_data():
    if not os.path.exists(RAW_DATA_PATH):
        return {"mapping": {}, "default_code": 0}

    df = pd.read_csv(RAW_DATA_PATH, usecols=["city"])
    cities = df["city"].astype(str).str.strip().str.lower().astype("category")
    mapping = {city: int(index) for index, city in enumerate(cities.cat.categories)}
    return {"mapping": mapping, "default_code": 0}


def _load_city_encoder():
    if os.path.exists(CITY_ENCODER_PATH):
        try:
            return joblib.load(CITY_ENCODER_PATH)
        except Exception:
            pass

    return _build_city_encoder_from_data()


model, model_error = _load_model()
city_encoder = _load_city_encoder()


def get_model_status():
    return {
        "model_loaded": model is not None,
        "model_error": model_error,
        "feature_columns": FEATURE_COLUMNS,
        "known_cities": len(city_encoder.get("mapping", {})),
    }


def encode_city(city):
    mapping = city_encoder.get("mapping", {})
    default_code = city_encoder.get("default_code", 0)
    normalized_city = city.strip().split(",")[0].strip().lower()
    return int(mapping.get(normalized_city, default_code))


def _bounded(value, default, minimum=None, maximum=None):
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return default

    if minimum is not None and numeric < minimum:
        return default
    if maximum is not None and numeric > maximum:
        return default

    return numeric


def normalize_live_features(city, live_data, now=None):
    now = now or datetime.now()
    temperature = _bounded(live_data.get("temperature"), 30, -20, 55)

    features = {
        "pm2_5": _bounded(live_data.get("pm25"), 0, 0, 1000),
        "pm10": _bounded(live_data.get("pm10"), 0, 0, 1200),
        "no2": _bounded(live_data.get("no2"), 0, 0, 500),
        "so2": _bounded(live_data.get("so2"), 0, 0, 500),
        "co": _bounded(live_data.get("co"), 0, 0, 100),
        "temperature": temperature,
        "humidity": _bounded(live_data.get("humidity"), 60, 0, 100),
        "pressure": _bounded(live_data.get("pressure"), 1008, 850, 1100),
        "wind_speed": _bounded(live_data.get("wind_speed"), 5, 0, 80),
        "apparent_temperature": _bounded(
            live_data.get("apparent_temperature"),
            temperature,
            -30,
            65
        ),
        "year": now.year,
        "month": now.month,
        "day": now.day,
        "weekday": now.weekday(),
        "city_encoded": encode_city(city),
    }

    return {column: features[column] for column in FEATURE_COLUMNS}


def predict_from_features(features):
    if model is None:
        return {"error": f"Model is not available: {model_error}"}

    df = pd.DataFrame([{column: features[column] for column in FEATURE_COLUMNS}])
    prediction = round(float(model.predict(df)[0]), 1)

    return {
        "predicted_aqi": prediction,
        "category": get_category(prediction),
        "features": features,
    }


def calibrate_prediction(raw_prediction, live_aqi):
    """Anchor same-city predictions to live AQI while preserving model direction."""
    try:
        live = float(live_aqi)
        raw = float(raw_prediction)
    except (TypeError, ValueError):
        return raw_prediction

    delta = raw - live
    max_delta = max(12, live * 0.35)
    clipped_delta = max(-max_delta, min(max_delta, delta))

    return round(live + clipped_delta * 0.55, 1)


def predict_city(city, live_data):
    features = normalize_live_features(city, live_data)
    prediction = predict_from_features(features)

    if prediction.get("error"):
        return prediction

    live_aqi = live_data.get("live_aqi", 0)
    raw_prediction = prediction["predicted_aqi"]
    calibrated_prediction = calibrate_prediction(raw_prediction, live_aqi)

    prediction["raw_predicted_aqi"] = raw_prediction
    prediction["predicted_aqi"] = calibrated_prediction
    prediction["category"] = get_category(calibrated_prediction)
    prediction["live_aqi"] = live_aqi
    prediction["delta"] = round(calibrated_prediction - live_aqi, 1)
    prediction["calibrated"] = True
    prediction["city"] = city
    prediction["model_version"] = os.path.basename(MODEL_PATH)

    return prediction
